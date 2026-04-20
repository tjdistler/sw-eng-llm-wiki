# Health Probes

**Summary**: Container orchestrators like Kubernetes distinguish two kinds of health checks. A **liveness probe** tells the orchestrator whether the process is still usable or needs to be restarted. A **readiness probe** tells the load balancer whether the replica is ready to receive user traffic. The two answer different questions and should be implemented as distinct endpoints.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`, `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## Two questions, two probes

Burns introduces the distinction in Chapter 5 while describing how a replicated, load-balanced service integrates with its load balancer (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **Liveness (health) probe.** Used by the container orchestrator to decide when an application needs to be *restarted*. Answers: "is this process beyond repair?"
- **Readiness probe.** Used by the load balancer to decide when an application is ready to *receive user requests*. Answers: "is this replica ready to serve traffic right now?"

The two are related but not the same, and Burns is emphatic that designers of a replicated service must build and deploy both. A single probe answering both questions leads to the wrong behaviour at the wrong time.

## Why readiness is not just liveness

Many applications are *alive* long before they are *ready* (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- They may need to connect to databases.
- They may need to load plugins.
- They may need to download serving files from the network.

The containers are running and their processes have not crashed — a liveness probe would reasonably report "OK" — but routing traffic to them yields errors or timeouts. The chapter's worked example illustrates this concretely: Burns's `brendanburns/dictionary-server` container starts listening immediately but only reports ready after downloading an 8 MB dictionary from the network. Until readiness flips to true, the load balancer must keep that replica out of rotation.

A readiness endpoint is thus application-aware: it returns success only when all the initialisation the application needs has actually completed.

## Liveness without readiness is also wrong

The inverse mistake — using readiness for restart decisions — is equally damaging. A replica that is temporarily not ready (a long GC pause, a brief connectivity blip to a dependency) does not necessarily need to be killed. Restarting it throws away warm caches and in-progress work and adds more churn to the system. Liveness should reflect a condition the application cannot recover from without a restart; readiness should reflect whether *right now* the replica should get requests.

## Kubernetes implementation

In Kubernetes, the two probes are declared separately on a container spec (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). Burns's Chapter 5 Deployment for the dictionary server:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

The load-balancer `Service` object selects pods via labels and uses the readiness result to decide which pods to include in its pool. A `livenessProbe` is declared alongside in the same shape when present; a failing liveness probe causes Kubernetes to restart the container rather than deregister it from the load balancer.

Both probes can be HTTP GETs, TCP socket checks, or exec commands. The HTTP-GET form is the most common and integrates cleanly with the [[adapter-pattern]]-style health-check adapter described in Chapter 4.

## Designing the endpoints

Three practical rules that follow from Burns's treatment:

1. **Make the readiness check actually exercise dependencies that matter for serving.** If the service cannot function without its database, the readiness endpoint should fail when the database is unreachable. Otherwise you are back to a liveness-flavoured signal.
2. **Keep the liveness check cheap and local.** A liveness probe failing will restart the container; a probe that itself depends on a flaky dependency will cause restart storms during dependency outages. Liveness should reflect only the application's own internal health, not the health of every downstream.
3. **Include both in the deployment from the start.** A replicated service without a readiness probe routes traffic to unfinished replicas during rollouts; without a liveness probe, it keeps sending traffic to stuck processes. Both come with the pattern.

## Relationship to the adapter pattern

Chapter 4 already introduced the [[health-check-adapter]] — an adapter container that exposes a rich, application-specific health endpoint to the orchestrator without modifying the upstream image. That pattern is a concrete way to implement *either* probe (liveness or readiness) when the application itself cannot be changed. For a third-party database container like MySQL, for example, a Go adapter running a representative SQL query can supply the kind of deep signal that makes the probes meaningful — instead of a trivial "is port 3306 open" check (source: raw/designing-distributed-systems/chapter-04-adapters.md).

## Relationship to existing wiki concepts

### Health probes and replicated services

Readiness probes are an *integral* part of the [[replicated-load-balanced-service]] pattern, not an add-on. Without one, the load-balancer pool admits unfinished replicas and rolling upgrades inject errors into production (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

### Health probes and desired-state management

Newman's [[desired-state-management]] page describes orchestrators that continuously reconcile observed state with declared state. Liveness probes are the observability half of that loop for restart decisions; readiness probes are the observability half for load-balancer membership. Both give the declarative control loop a signal to act on.

### Health probes and fault tolerance

By allowing replicas to temporarily leave the load-balancer pool without being killed, readiness probes give the service graceful degradation behaviour: a slow replica is removed, recovers, and returns — without the state reset that a restart would cause. This complements [[fault-tolerance]] at the orchestrator level.

### Health probes and the singleton pattern

Burns's Chapter 9 uses liveness probes as load-bearing machinery for the [[singleton-pattern]]: a single-replica service running under Kubernetes relies on a liveness probe to trigger restart when the container hangs, which is one of the three automatic recovery behaviours the orchestrator provides. Without a liveness probe, a hung singleton stays hung — the pattern's "pretty good" three- to four-nines uptime assumes the probe is in place (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

### Health probes and the SRE three-state backend model

SRE Chapter 20 frames the same territory as a three-state model ([[backend-task-states]]): *healthy*, *refusing connections*, and *[[lame-duck-state|lame duck]]* (source: raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md). The binary readiness probe collapses two of those states into "not ready" without distinguishing them, which loses information that matters for graceful shutdown. Chapter 20's contribution is making the shutdown case explicit:

- **Refusing connections** is the failure/startup case that readiness was designed for. The load balancer drops the replica; the orchestrator may restart it.
- **Lame duck** is a backend *choosing* to stop receiving new work while still serving in-flight requests. There is no vanilla Kubernetes equivalent — the closest is the termination grace period during which the pod is being shut down.
- **Healthy** is "readiness true."

The SRE book pushes the state model into the RPC framework itself, which gives every service graceful shutdown for free and propagates state changes to inactive clients via UDP health checks in 1-2 RTT. Burns's Kubernetes-level machinery gets you the healthy/unhealthy distinction; Chapter 20 adds the backend-initiated drain signal on top.

### Health probes and monitoring

Probes are narrow: one bit per probe per replica. [[monitoring-and-observability]] covers the richer telemetry that an application should still expose separately. Probes and monitoring are complements, not substitutes.

## Related pages

- [[replicated-load-balanced-service]]
- [[health-check-adapter]]
- [[adapter-pattern]]
- [[desired-state-management]]
- [[fault-tolerance]]
- [[monitoring-and-observability]]
- [[pod]]
- [[service-discovery]]
- [[singleton-pattern]]
- [[backend-task-states]]
- [[lame-duck-state]]
- [[designing-distributed-systems]]
