# Lame Duck State

**Summary**: SRE Chapter 20's *quasi-operational* backend state: the task is still listening on its port and still processing in-flight requests, but is explicitly asking its clients to stop sending *new* requests. It is the mechanism that makes clean shutdown possible without serving errors to the unlucky requests that happen to be in flight when a backend starts shutting down. The internal RPC framework propagates the state change to every client in 1-2 RTT via piggybacked UDP health checks, so even idle clients learn about the drain before they try to send the next request.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## What lame-duck state is

Lame duck is the third of [[backend-task-states|three backend states]] a client can observe (source: chapter-20-load-balancing-in-the-datacenter.md). Unlike "healthy" (serve normally) and "refusing connections" (drop new traffic — process is starting, stopping, or broken), lame duck is **backend-initiated** and **explicit**:

- The backend is still listening on its port.
- The backend can still serve requests that have already started.
- The backend has broadcast to all its clients that it no longer wants new requests.

The name comes from US politics — an elected official in the interval between a lost election and the successor's inauguration, still technically in office but without a mandate for new initiatives. The backend analogue is the same: still serving, but not accepting new work.

## Why it exists: clean shutdown without errors

The motivating problem is that restarting a backend with active requests, absent this state, either:

- *Drops the active requests* (SIGKILL semantics) — serving errors to users who happened to be mid-request.
- *Blocks the restart indefinitely* — waiting for every request to finish, with no forward progress if any request is long-lived.

Neither is acceptable at the rate Google does code pushes, maintenance, and machine reboots. The lame-duck state makes shutdown a *graceful drain*: new requests stop arriving, in-flight requests complete, and only then does the process exit (source: chapter-20-load-balancing-in-the-datacenter.md).

## The shutdown protocol

The shutdown sequence has five steps (source: chapter-20-load-balancing-in-the-datacenter.md):

1. **The [[borg|job scheduler]] sends SIGTERM to the backend task.**
2. **The backend enters lame-duck state and asks clients to send new requests to other backend tasks.** This is an explicit RPC-framework API call invoked in the SIGTERM handler.
3. **In-flight requests execute normally.** Requests that started before the backend entered lame duck — or just after, but before the client noticed — run to completion.
4. **As responses flow back, the active-request count drops to zero.**
5. **After a configured interval, the backend exits cleanly** (or the scheduler kills it if it didn't). The interval should be large enough for typical requests to finish — *10 to 150 seconds* depending on client complexity.

Notice that the protocol uses the normal request/response flow as its completion signal: the scheduler doesn't need special knowledge of what the backend is doing; it just waits for the interval or gives up.

## Propagation to inactive clients

Chapter 20 flags a subtlety: step 2 works obviously for *active* clients (they see the lame-duck response on their very next request), but what about clients that currently have no TCP connections? Google's RPC implementation (source: chapter-20-load-balancing-in-the-datacenter.md):

- Even idle connections still send **periodic UDP health checks**.
- The lame-duck signal rides on those health checks.
- Inactive clients learn about the state change in **1 or 2 round trips**.

Without this, a currently-idle client would discover the drain only by sending a request and getting a refusal — which defeats the point of the graceful-shutdown contract. The RPC layer makes the signal *push*-like, not pull-like.

## Lame duck on the way up

Chapter 20 notes a symmetric use of the state (source: chapter-20-load-balancing-in-the-datacenter.md): a starting backend may want to accept TCP connections early (so clients don't pay connection-negotiation latency later) while still performing long-running initialisation. It can listen immediately in a pre-lame-duck-like mode and signal "I'm ready" explicitly when init finishes. This amortises connection setup across the warm-up period.

This is the same idea Chapter 17 [[fake-backend-versions|mentions in passing for production probe infrastructure]] and Chapter 8's [[push-on-green|release process]] relies on implicitly: a backend has a distinct "connection-ready" and "request-ready" moment, and the load-balancing substrate knows how to use both.

## Relationship to existing wiki concepts

### Lame duck and readiness probes

Kubernetes's [[health-probes|readiness probe]] expresses a similar idea — "is this replica ready to receive traffic?" — but in the *pull* direction. The load balancer asks, and the replica answers. Lame duck is the *push* direction: the backend tells every client about the state change, and the clients update their routing. Push is faster (1-2 RTT instead of one probe interval), matters more at the scale and request rate Chapter 20 is designed for, and is what the RPC framework can do that a generic orchestrator cannot.

Under a pure readiness model, the shutdown case requires the orchestrator to:

- Mark the pod "terminating" so the load balancer deregisters it.
- Wait a grace period (the Kubernetes `terminationGracePeriodSeconds`).
- SIGTERM the pod.

The SRE book's lame-duck API collapses the "deregister" step into a single backend-initiated RPC call, and the drain happens without the load balancer needing to participate.

### Lame duck and clean shutdown more generally

Outside Google's stack, the closest analogues are:

- **HAProxy's server draining mode** — a healthy server is marked as "drain" and receives no new connections while existing ones finish.
- **nginx's graceful shutdown** — workers finish their current requests and then exit.
- **Kafka's controlled shutdown** — a broker notifies the controller before leaving the cluster so partitions can be reassigned.

All three are special cases of the same pattern: the component signals "I'm going away" and receives a finite grace window to finish its work. Chapter 20's contribution is putting this mechanism in the RPC framework itself, so every Google service inherits it without per-service implementation work.

### Lame duck and change management

[[change-management-sre|Chapter 1's change-management tenet]] ("70% of outages come from change") singles out *progressive rollouts*, *fast detection*, and *safe rollback* as the automation trio. Lame duck is the micro-level mechanism that makes the first leg of that trio zero-cost: each task update within a progressive rollout is a graceful drain-and-restart, not an abrupt kill. Without it, a rolling deployment would generate a steady stream of served errors proportional to the rollout speed.

### Lame duck and Chapter 17 zero-MTTR testing

[[zero-mttr-testing]] catches bugs at push time so users never see them. Lame duck catches the *in-flight request* at push time so users never see its error. Both are "reliability through the release pipeline" mechanisms, operating at different layers.

## Related pages

- [[backend-task-states]]
- [[datacenter-load-balancing]]
- [[health-probes]]
- [[change-management-sre]]
- [[rapid-release-system]]
- [[site-reliability-engineering]]
