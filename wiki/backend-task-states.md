# Backend Task States

**Summary**: SRE Chapter 20's three-state model of an RPC backend as seen by its clients: **healthy** (serving normally), **refusing connections** (unresponsive — starting up, shutting down, or broken), and **[[lame-duck-state|lame duck]]** (listening and serving but explicitly asking clients to drain off). The model makes clean shutdown possible and is the richer RPC-world counterpart to Kubernetes's [[health-probes|liveness/readiness probes]]. Chapter 20 also describes a cruder predecessor — **active-request flow control** — that every client implements as a last-resort safeguard even with the three-state model in place.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The three states

From a client's perspective, a given backend task is in one of three states (source: chapter-20-load-balancing-in-the-datacenter.md):

1. **Healthy.** The backend task has initialised correctly and is processing requests.
2. **Refusing connections.** The backend task is unresponsive. This can happen because it is starting up, shutting down, or in an abnormal state (rare for a backend to stop listening on its port without shutting down).
3. **Lame duck.** The backend task is listening on its port and can serve, but is explicitly asking clients to stop sending requests. See [[lame-duck-state]] for the full protocol and rationale.

The key novelty relative to "the process is up or it's down" is the third state. A process that is up and serving but *asks* not to receive new work is the abstraction that makes [[change-management-sre|rolling deployments]], maintenance, and machine draining non-disruptive.

## Active-request flow control: the cruder safeguard

Before introducing the three-state model, Chapter 20 describes a simpler mechanism that clients use to avoid hopeless backends (source: chapter-20-load-balancing-in-the-datacenter.md):

- Each client tracks the number of active requests it has sent on each connection to a backend.
- When the active-request count reaches a configured limit (**100 is a reasonable default**), the client treats the backend as unhealthy and stops sending it requests.

In normal operation this limit is rarely hit — requests usually finish fast enough — so the mechanism doubles as a crude form of load balancing: if a backend gets overloaded and its queue grows, clients naturally back off and the workload spreads elsewhere.

### Why flow control alone is insufficient

The Chapter 20 critique is sharp (source: chapter-20-load-balancing-in-the-datacenter.md):

- **It kicks in too late.** Backends can become overloaded well before the 100-request limit is ever reached.
- **It has false positives.** Services with long-lived requests can pile up 100 outstanding requests with backends still healthy.
- **It can cause total unavailability.** The chapter cites cases where the limit drove *all* backend tasks into the "unreachable" state simultaneously, with requests blocked in clients until they timed out and failed.

Raising the limit avoids the false positive but doesn't solve the core problem: the count of active requests does not cleanly distinguish "truly unhealthy" from "slow to respond." That gap is what the lame-duck state (explicit backend-initiated signal) and the [[load-balancing-policies|weighted-round-robin policy]] (richer signal via utilisation reporting) are each designed to close.

Flow control remains as a last-resort safeguard even when the richer signals are in place.

## Why the three states beat a readiness-style binary

The simplest binary health model — "is this backend ready to serve?" — conflates several distinct situations:

- A backend that crashed or is starting up is *not ready* and should not receive any traffic.
- A backend that is shutting down is *ready to handle in-flight work but should not receive new work*. This is the lame-duck case. A binary model cannot express it, so under a binary model a graceful shutdown loses the window during which the backend could still complete outstanding requests.
- A backend that is healthy but overloaded is *ready but should get proportionally less traffic*. This is what [[weighted-round-robin]] handles via capability scoring rather than by changing state.

The three-state model picks out the shutdown case as its own thing; the rest is left to the [[load-balancing-policies|policies]].

## Propagation of state

State transitions have to reach every client that might route a request to the backend, including *inactive clients* that currently have no requests in flight. Google's RPC implementation handles this via periodic UDP health checks even on idle connections, so lame-duck signals propagate in **1 or 2 RTT** regardless of whether a client currently has traffic going to the backend (source: chapter-20-load-balancing-in-the-datacenter.md).

Without this, a scheduled restart could tell only the actively-sending clients to drain; the first request from a currently-idle client would arrive mid-shutdown.

## Relationship to existing wiki concepts

### Three-state model vs liveness/readiness probes

Burns's [[health-probes]] distinguish liveness (restart decision, owned by orchestrator) from readiness (routing decision, owned by load balancer). Chapter 20's model maps to this as follows:

- **Refusing connections** is observed indirectly (TCP refused, timeouts) — it is the *symptom* that readiness and liveness probes are designed to detect. Google's orchestrator restarts the task; clients meanwhile stop trying to route to it.
- **Lame duck** has no Kubernetes counterpart in the base probe model. In Kubernetes terms it is "readiness is false but the container is still running, and the platform gives the pod a termination grace period to drain." The three-state model names this explicitly and makes it backend-initiated.
- **Healthy** is "readiness is true."

The SRE book's version is pushed deeper into the RPC framework itself, so every Google service gets the behaviour for free.

### Three-state model and clean shutdown

The lame-duck state is the RPC-level equivalent of a process trapping SIGTERM to finish its work before exiting. Chapter 20's shutdown sequence shows that the internal RPC framework exposes a lame-duck API call that is invoked in the SIGTERM handler; the connection-draining negotiation and the process exit itself are handled by the framework, not by every application. This is an instance of Chapter 9's [[virtue-of-boring]] and [[minimal-apis]] thinking applied to a shutdown API.

### Three-state model and least-loaded policies

The [[least-loaded-round-robin]] policy has a failure mode — "sinkholing traffic" — where an unhealthy backend fast-fails requests and thus appears to have a very small number of active requests. The fix is to count recent errors as though they were active requests, which essentially treats an error-flooding backend as if it were in a fourth hidden "degraded" state. The three states are the explicit states; the policies are responsible for handling the "silently broken" case that doesn't trip any explicit signal.

## Related pages

- [[lame-duck-state]]
- [[datacenter-load-balancing]]
- [[load-balancing-policies]]
- [[least-loaded-round-robin]]
- [[weighted-round-robin]]
- [[health-probes]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
