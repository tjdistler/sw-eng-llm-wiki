# Watermarks

**Summary**: A watermark is a declaration propagated through a [[stream-processing|stream-processing]] topology that **all events with timestamp ≤ t have been processed**. Watermarks are the mechanism Spark, Flink, Samza, and Beam use to track event-time progress and decide when [[late-arriving-events|late events]] should be treated as late.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## What a watermark is

A watermark `W(t)` emitted by a processing node tells every downstream node: *I have processed all events of [[event-timestamps|event time]] `t` and earlier; you should update your own event time accordingly* (source: chapter-06-deterministic-stream-processing.md).

Watermarks originate at **source** operators — the nodes consuming from raw [[event-streams|event streams]]. Each source's watermark reflects the highest event-time boundary it has observed so far. Watermarks then flow through the topology alongside events.

New watermarks are generated periodically — after some amount of wall-clock or event time passes, or after a minimum number of events has been processed (source: chapter-06-deterministic-stream-processing.md).

## Propagation

As a watermark arrives at a downstream node, the node:

1. Updates its internal event time.
2. Decides what to do with any buffered events whose timestamps fall before the new watermark — those are now late. See [[late-arriving-events]].
3. Generates its own outgoing watermark and forwards it further downstream (source: chapter-06-deterministic-stream-processing.md).

A node with **multiple upstream inputs** (e.g., after a shuffle or aggregate) must wait for watermarks from all inputs. Its event time is the **minimum** of its inputs' event times, so it cannot get ahead of its slowest source (source: chapter-06-deterministic-stream-processing.md).

## Parallel / shuffled topologies

Watermarks shine in parallel topologies where a `groupByKey → aggregate` forces a shuffle. Each aggregate instance has multiple upstream feeders (one per source instance post-shuffle). Once the watermark from the slowest upstream arrives, every aggregate instance can safely advance its event time and commit that window's result (source: chapter-06-deterministic-stream-processing.md).

Watermark-based frameworks (Spark, Flink, Beam) typically require a **dedicated processing cluster**, because shuffles happen via cluster-internal networking rather than round-tripping through the [[event-broker]].

## Watermarks vs stream time

Kafka Streams takes a different approach — see [[stream-time]]. Key differences (source: chapter-06-deterministic-stream-processing.md):

| | Watermarks (Flink/Spark/Beam/Samza) | Stream time (Kafka Streams) |
|---|---|---|
| Event-time tracking | Per node; each node has its own watermark | Per subtopology; one value |
| Propagation | Explicit watermark messages flow with events | Implicit — advanced by each processed event |
| Shuffle mechanism | Cluster-internal network | Repartition event stream through the broker |
| Buffering | Events buffered at each node's input | Depth-first — one event at a time per subtopology |
| Cluster requirement | Dedicated cluster typical | Microservice-friendly, no cluster needed |

Apache Samza offers both modes — a standalone (Kafka-Streams-like) deployment that still uses watermarking.

## When a watermark makes an event late

Given an event at time `t'` arriving after watermark `W(t)` with `t' < t`: the event is **late**, and the receiving node decides (per its [[late-arriving-events|late-event policy]]) whether to drop it, update a prior window, or otherwise accommodate it (source: chapter-06-deterministic-stream-processing.md).

A watermark does not reshuffle event dispatch order — it only signals completeness for time-bounded downstream logic like [[windowing|windowed aggregations]].

## Further reading

Bellemare recommends the Google Dataflow watermarks whitepaper and chapters 2–3 of *Streaming Systems* (Akidau, Chernyak, Lax, O'Reilly 2018) for a deeper treatment (source: chapter-06-deterministic-stream-processing.md).

## Related pages

- [[stream-time]]
- [[deterministic-stream-processing]]
- [[event-timestamps]]
- [[event-scheduling]]
- [[late-arriving-events]]
- [[out-of-order-events]]
- [[windowing]]
- [[stream-processing]]
- [[repartitioning]]
- [[dataflow-engines]]
