# Connection-Level Load

**Summary**: SRE Chapter 21's final overload-handling topic: the CPU and memory cost of *maintaining* and *churning* client-backend connections, separate from the cost of the requests those connections carry. In large-scale RPC systems, a service with many low-rate clients can spend more resources on connection health-checking than on actual work; a batch job that brings up thousands of workers simultaneously can overwhelm a backend's new-connection-acceptance path. Chapter 21 names two mitigations: tune connection parameters (slower health checks, idle TCP teardown with UDP health checks, dynamic connection creation/destruction), and the **batch proxy** pattern — a forwarding tier that absorbs the batch job's connection storm and presents a small stable connection pool to the real backend.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## Why connection load matters

Chapter 21 flags the problem late in the chapter (source: chapter-21-handling-overload.md):

> The load associated with connections is one last factor worth mentioning. We sometimes only take into account load at the backends that is caused directly by the requests they receive (which is one of the problems with approaches that model load based upon queries per second). However, doing so overlooks the CPU and memory costs of maintaining a large pool of connections or the cost of a fast rate of churn of connections. Such issues are negligible in small systems, but quickly become problematic when running very large-scale RPC systems.

Two costs that go unaccounted for if you only measure request-handling:

- **Steady-state connection maintenance.** Each open connection consumes some CPU (health checks, TCP keepalive, encryption contexts) and some memory (socket buffers, per-connection state).
- **Connection churn.** Opening and tearing down connections is much more expensive per-event than sending a single request — TLS handshake, RPC-level negotiation, authentication, state setup.

These costs are invisible in a QPS-centric model but become dominant at sufficient scale.

## The health-check-exceeds-work pathology

Chapter 21's concrete example (source: chapter-21-handling-overload.md):

> Our RPC protocol requires inactive clients to perform periodic health checks. After a connection has been idle for a configurable amount of time, the client drops its TCP connection and switches to UDP for health checking. Unfortunately, this behavior is problematic when you have a very large number of client tasks that issue a very low rate of requests: health checking on the connections can require more resources than actually serving the requests.

The shape of the problem:

- Each client maintains a connection (TCP or UDP-health-check) to each backend in its [[subsetting|subset]].
- If there are 10,000 clients each with a subset of 100 backends, the backend fleet sees 10,000 × 100 = 1,000,000 connection endpoints.
- Even if each client sends only one request per minute, the constant health-check traffic across a million connections is substantial.
- At some ratio of request-rate to connection-count, health checking becomes the dominant CPU consumer.

The system works as designed — health checking is necessary — but the economics flip in a direction the original design didn't anticipate.

## Mitigations for steady-state connection load

Chapter 21's suggested knobs (source: chapter-21-handling-overload.md):

> Approaches such as carefully tuning the connection parameters (e.g., significantly decreasing the frequency of health checks) or even creating and destroying the connections dynamically can significantly improve this situation.

The two options:

### Tune health-check frequency

If health checks run every second and requests arrive once per minute, 60 health checks happen per useful request. Dropping health-check frequency (e.g., to every 10 seconds for idle connections) reduces this ratio by an order of magnitude at modest cost in how quickly a backend failure is detected for currently-idle clients.

The RPC framework's idle-connection optimisation (described in Chapter 20's [[backend-task-states]] material) is the first step: switch idle TCP connections to cheaper UDP health checks with lower frequency. Chapter 21 suggests going further when load demands it.

### Create and destroy connections dynamically

Instead of maintaining long-lived connections for every client-backend pair, the client creates a connection when it has a request to send and tears it down after. This eliminates the steady-state connection cost at the price of extra per-request setup.

The trade-off:

- **Long-lived connections.** Connection setup amortised across many requests; steady-state maintenance cost.
- **Dynamic connections.** No steady-state cost; connection setup cost paid per request.

The cross-over point is at some ratio of per-connection maintenance cost to per-connection setup cost. For high-rate clients the long-lived approach wins; for sporadic clients the dynamic approach may win.

## The batch-proxy fuse pattern

Chapter 21's second connection problem is different: bursts of *new* connection establishment (source: chapter-21-handling-overload.md):

> Handling bursts of new connection requests is a second (but related) problem. We've seen bursts of this type happen in the case of very large batch jobs that create a very large number of worker client tasks all at once. The need to negotiate and maintain an excessive number of new connections simultaneously can easily overload a group of backends.

A MapReduce or similar batch job spawning 5,000 workers, each of which tries to connect to a backend subset, produces an instantaneous burst of handshake work that can exceed the backend's connection-accept capacity even though the steady-state request rate is modest.

Chapter 21 lists two mitigations (source: chapter-21-handling-overload.md):

### Feed connection load into cross-datacenter balancing

> Expose the load to the cross-datacenter load balancing algorithm (e.g., base load balancing on the utilization of the cluster, rather than just on the number of requests). In this case, load from requests is effectively rebalanced away to other datacenters that have spare capacity.

The connection-setup load is part of "utilisation." [[gslb|GSLB]] routes based on utilisation rather than request rate, so a datacenter whose backends are burning CPU on handshakes gets less new traffic. This is the [[weighted-round-robin]] idea at the cross-datacenter level: include all costs, not just request costs, in the routing signal.

### The batch-proxy fuse

> Mandate that batch client jobs use a separate set of batch proxy backend tasks that do nothing but forward requests to the underlying backends and hand their responses back to the clients in a controlled way. Therefore, instead of "batch client → backend," you have "batch client → batch proxy → backend." In this case, when the very large job starts, only the batch proxy job suffers, shielding the actual backends (and higher-priority clients). Effectively, the batch proxy acts like a fuse.

The topology:

```
batch workers (5,000) → batch proxy (50)  →  real backend (100)
                         (connection storm  ↑
                          absorbed here)    │
                                            │
interactive clients (200) ─────────────────→┘
```

Connection properties:

- **Batch workers → batch proxy**: 5,000 workers × few connections each = 25,000 batch-side connections, absorbed by 50 proxy tasks.
- **Batch proxy → real backend**: only 50 proxies × subset size ≈ 5,000 connections to the real backend — a small pool that looks to the backend like a few extra "clients." Interactive clients are not affected by the batch job.

The batch proxy converts a burst into a bounded pool. It also has two nice side effects the chapter mentions:

- **Reduces total connections against the backend.** Real backends see many fewer clients, which also improves [[datacenter-load-balancing|balancing]] (larger subsets are viable, better view of backend state).
- **Acts as a fuse.** If the batch proxy itself is overloaded, the batch job is the only thing that suffers; the rest of the system is unaffected. The proxy is a [[bulkhead]] between batch and interactive workloads.

## Why connections belong in the overload chapter

Chapter 21 could have treated connections as an infrastructure-tuning topic unrelated to overload. Putting them here makes a specific argument: **overload handling that ignores connection load is incomplete.** A backend can have plenty of CPU for its *requests* but still be overloaded by the *connection storm* that accompanies them. The [[queries-per-second-pitfalls|QPS-pitfalls argument]] from the start of the chapter returns here — QPS doesn't see connections, but connections are part of the actual load.

The mitigations (health-check tuning, dynamic connections, cross-datacenter utilisation routing, batch proxies) are all structural rather than per-request. They don't replace the rest of the Chapter 21 machinery; they complement it by covering a cost axis the other mechanisms don't see.

## Relationship to existing wiki concepts

### Connection load and [[bulkhead]]

The batch proxy is a textbook [[bulkhead]]: isolating the batch workload so its resource demands cannot starve the interactive workload. The bulkhead boundary is at the network tier (separate proxy fleet) rather than at thread pools, but the pattern is the same: cap the blast radius of a single workload class by giving it its own resource pool.

### Connection load and [[subsetting]]

[[subsetting]] from Chapter 20 is the primary mechanism for bounding the connection-count problem: each client connects to a subset of backends rather than all of them. Chapter 21 picks up where subsetting stops helping — when even the subsetted connection pool is too large, or when the pool churns rapidly.

### Connection load and the RPC framework

The RPC framework's idle-connection optimisation (switch idle TCP to UDP health checks, lower frequency) is the first-line defence against the health-check-dominates pathology. Chapter 21's recommendation to "significantly decrease the frequency of health checks" is tuning the framework's idle-path parameters. This is an example of the pattern that recurs throughout Chapter 20-21: cross-cutting concerns live in the RPC framework so every service benefits without custom code.

### Connection load and [[dynamic-worker-scaling]]

Burns's [[dynamic-worker-scaling]] for batch work queues considers how fast workers scale relative to work arrival. The batch proxy pattern here is a connection-dimension analogue: scaling up worker count fast doesn't just affect the work-queue throughput, it also creates an orthogonal connection-storm load on downstream services. A worker-scaling policy that doesn't account for this can cause the very backends the workers depend on to fail.

### Connection load and [[fallacies-of-distributed-computing]]

Two of Deutsch's fallacies apply directly: "bandwidth is infinite" (connection setup is not free) and "the network is reliable" (failed handshakes amplify as retries). Chapter 21's connection section is what happens when both fallacies are taken seriously in a production system.

## Related pages

- [[handling-overload]]
- [[subsetting]]
- [[bulkhead]]
- [[datacenter-load-balancing]]
- [[weighted-round-robin]]
- [[gslb]]
- [[dynamic-worker-scaling]]
- [[fallacies-of-distributed-computing]]
- [[queries-per-second-pitfalls]]
- [[site-reliability-engineering]]
