# Cold Start and Warm Start

**Summary**: A function's lifecycle in a FaaS framework. A cold start is the function's first startup, or startup after a long inactivity window — the container must be launched, code loaded, and client connections established. A warm start reuses a suspended instance whose connections are still live, eliminating most of the startup cost.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The lifecycle

A function moves through four states (source: chapter-09-microservices-using-function-as-a-service.md):

1. **Cold start.** Container launch, code load, event-broker connections, state-store clients, authentication handshakes — all done from scratch. The dominant latency contributor for a first invocation or after long inactivity.
2. **Warm / running.** The function processes a batch of events.
3. **Suspended / hibernating.** On timeout or completion, the instance is paused but kept in a hibernation cache; connections may remain open.
4. **Revived (warm start) or evicted.** A new trigger either reuses the hibernating instance — near-zero latency — or, if the cache has evicted it, forces a cold start again.

## Why this matters in EDM

A steady stream of events typically produces a cycle of short hibernations punctuated by immediate revivals, so most events are processed by warm instances and broker connections survive across timeouts. But the guarantee is weak: there is no promise a specific instance will stay warm, and in particular there is no guarantee that in-memory state from the last run will be available to the next. This is why Bellemare's [[functions-as-a-service]] treatment insists state be externalized (source: chapter-09-microservices-using-function-as-a-service.md).

## Termination discipline

When a function reaches the end of its allocated lifespan (typically 5–10 minutes) it is suspended. The designer must decide whether the function should close its broker connections and relinquish partition assignments, or leave them open for the probable imminent revival (source: chapter-09-microservices-using-function-as-a-service.md):

- **Almost-always-on functions** — leave connections open; the consumer group rebalance cost of relinquishing would dominate.
- **Intermittent functions** — close everything. The next invocation will re-establish regardless of whether it is warm or cold, and dangling partition assignments cause processing delays for the whole consumer group until the broker's assignment timeout fires.

When in doubt, Bellemare's rule is to clean up: lighter load on state stores and brokers, fewer zombie partition claims.

## Interaction with scaling policies

Aggressive autoscaling policies can create a "virtual deadlock" of rebalancing — new function instances repeatedly joining and leaving the [[consumer-group]], none of them making forward progress (source: chapter-09-microservices-using-function-as-a-service.md). The mitigations are the same as the [[faas-triggers]] section: step-based scaling, hysteresis loops, scaling up or down at most once every few minutes, and (most decisively) static partition assignment to skip rebalancing entirely.

## Relationship to other patterns

- **[[functions-as-a-service]]** — the parent pattern; warm starts are the reason the cost-per-invocation model works for anything other than bursty loads.
- **[[faas-triggers]]** — trigger cadence directly drives how often cold starts happen.
- **[[consumer-group]]** — rebalancing is the source of the startup cost you feel most acutely as your function fleet churns.
- **[[stateful-stream-processing]]** — the reason stateful FaaS generally externalizes state: local state survives warm starts but never cold starts.

## Related pages

- [[functions-as-a-service]]
- [[faas-triggers]]
- [[event-stream-listener]]
- [[faas-batch-processing]]
- [[consumer-group]]
- [[stateful-stream-processing]]
- [[event-driven-microservices]]
