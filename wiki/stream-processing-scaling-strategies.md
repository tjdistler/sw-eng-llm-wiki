# Stream-Processing Scaling Strategies

**Summary**: Two strategies for scaling a stateful [[heavyweight-framework-microservice|heavyweight streaming]] application — **scaling while running** and **scaling by restart** — plus **autoscaling** as an orthogonal axis that automates either. Stateless applications scale trivially (rebalance the consumer group); stateful applications must coordinate state reload with new partition assignments, which is what makes the two strategies meaningfully different (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## Why stateless is easy and stateful is hard

A **stateless** stream processor ([[stateless-stream-processing]]) scales up or down simply by joining or leaving the [[consumer-group]]. The broker's [[partition-assignor]] rebalances partitions, and the instances resume. No state to move.

A **stateful** stream processor ([[stateful-stream-processing]]) must, for every newly assigned partition, **load the matching state before processing resumes.** The state store in the new instance must reflect exactly the events consumed so far — not a prefix, not a superset. That is why stateful scaling is a framework-level concern (source: chapter-11-heavyweight-framework-microservices.md).

## Strategy 1: Scale while running

Add, remove, or reassign application instances **without stopping the job** or affecting processing accuracy (source: chapter-11-heavyweight-framework-microservices.md).

Requirements:

- Redistribute stream partitions among the new instance set.
- Reload state for newly-assigned partitions from the last [[checkpointing-stream-processing|checkpoint]].
- Handle **in-flight shuffled events** correctly — the hard part. See [[external-shuffle-service]] for why decoupling shuffles from specific executors is necessary for this strategy.

Available only in some frameworks:

- **Spark's dynamic resource allocation** — requires coarse-grained mode and historically required an [[external-shuffle-service]]. Spark 3.0+ relaxes the ESS requirement.
- **Google Cloud Dataflow** (Beam runner) — built-in scaling of both resources and worker instances.
- **Heron Health Manager** — experimental real-time, stateful topology scaling.

Shuffle handling is the active area of development. Lightweight frameworks resolve it by using the [[event-broker]] itself as the shuffle service — see [[broker-as-shuffle-service]].

## Strategy 2: Scale by restart

Universally supported across heavyweight frameworks (source: chapter-11-heavyweight-framework-microservices.md):

1. Pause stream consumption.
2. [[checkpointing-stream-processing|Checkpoint]] the current state.
3. Stop the application.
4. Restart it with new parallelism / resources.
5. Each task reloads its assigned partitions' state from the checkpoint and resumes.

This is simpler to implement (no coordination of in-flight shuffles) but has a **downtime window** while the application restarts and reloads state. For large state stores, that window can be non-trivial.

Flink exposes a REST API for this flow; Storm provides a `rebalance` command.

## Autoscaling

Automating either strategy based on runtime metrics — processing latency, consumer lag ([[consumer-offset]]), memory usage, CPU usage (source: chapter-11-heavyweight-framework-microservices.md).

Built-in options:

- Google Dataflow autoscaling.
- Heron Health Manager.
- Spark Streaming dynamic allocation.

Otherwise, wire your own: collect performance/lag metrics and feed them into the framework's scaling mechanism. Consumer-offset lag monitoring is the usual starting signal — if lag grows, scale up; if lag is persistently zero with spare capacity, scale down.

## Lightweight frameworks: the strategies collapse

[[lightweight-framework-microservice|Lightweight frameworks]] (Kafka Streams, Samza embedded) don't run a dedicated cluster. Scaling and failure recovery are **the same process** — instances join or leave a [[consumer-group]], the [[partition-assignor]] rebalances, and new owners replay the [[changelog-stream]] before resuming. No restart is required; the pause is just the state-restoration phase (source: chapter-12-lightweight-framework-microservices.md).

Internal shuffles are routed through broker topics ([[broker-as-shuffle-service]]), so "scale while running" has no special executor-lifetime problem — the shuffle data survives independent of any upstream instance. [[hot-replicas]] eliminate the rematerialization pause for both failover and scale-up.

See [[lightweight-framework-microservice]] for the full treatment.

## Application scaling vs cluster scaling

Bellemare's warning: **scaling an application is not the same as scaling the cluster.** Every strategy here assumes the cluster already has capacity to grant. If the cluster itself is saturated, the application cannot grow regardless of how the scaling strategy is configured. Framework-specific cluster-scaling docs live alongside these application-scaling docs and must be considered together (source: chapter-11-heavyweight-framework-microservices.md).

## Related pages

- [[heavyweight-framework-microservice]]
- [[stream-processing-cluster]]
- [[checkpointing-stream-processing]]
- [[external-shuffle-service]]
- [[stateful-stream-processing]]
- [[stateless-stream-processing]]
- [[consumer-group]]
- [[partition-assignor]]
- [[consumer-offset]]
- [[scaling-approaches]]
- [[dynamic-worker-scaling]]
- [[lightweight-framework-microservice]]
- [[broker-as-shuffle-service]]
- [[hot-replicas]]
