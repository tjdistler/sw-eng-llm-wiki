# Hybrid BPC with External Stream Processing

**Summary**: A hybrid pattern in which a [[basic-producer-consumer-microservice|BPC]] microservice outsources operations that are awkward or impossible to perform locally — multi-stream joins, large aggregations, SQL over streams — to an **external stream-processing framework** (Kafka Streams, Flink, KSQL). The BPC instantiates a client that submits the work to the framework, receives results back via an intermediate event stream, and continues its own local processing. The pattern buys access to framework-only capabilities from a language or stack that wouldn't otherwise have them.

**Sources**: `raw/building-event-driven-microservices/chapter-10-basic-producer-and-consumer-microservices.md`

**Last updated**: 2026-04-17

---

## Shape

Three components (source: chapter-10-basic-producer-and-consumer-microservices.md):

1. The **BPC microservice** — the primary application, owning the bounded context and writing most of the business logic in the team's preferred language.
2. An **external stream-processing framework** — a separate cluster capable of materializing streams into tables, joining large keyed datasets, and emitting results back into the broker.
3. An **intermediate event stream** in the broker that carries results from the framework back to the BPC.

The BPC uses a framework client to **submit a stream-processing job** — for example, "materialize streams A and B as tables, join them on key, emit the joined rows to stream C." The framework takes over the heavy lifting. The BPC consumes the resulting stream C as just another input.

Bellemare's canonical example: a BPC needs a stream-stream join across large materialized datasets. Rather than implement framework-level [[stream-joins]] by hand, it delegates the join to Kafka Streams or KSQL and reads the joined output back (source: chapter-10-basic-producer-and-consumer-microservices.md).

## Lifecycle coupling

A subtle but important discipline: **when the BPC terminates, it must also terminate the external stream-processing job it started** (source: chapter-10-basic-producer-and-consumer-microservices.md). Otherwise ghost jobs accumulate on the framework cluster, continuing to consume partitions, produce events, and rack up compute. The BPC "owns" the external job the way a process owns a child — termination is part of the bounded-context lifecycle.

## What the pattern unlocks

- **Stream-processing features in any language.** A Python or Go BPC gets access to framework-level joins and aggregations without being rewritten in Java/Scala.
- **SQL over streams.** KSQL and similar tools let non-Java teams compose stream operations declaratively.
- **Scale boundaries shift.** The framework runs on its own cluster, so the BPC's compute footprint doesn't have to expand to accommodate a large join.

## What the pattern costs

Chapter 10 is unusually direct about the downsides (source: chapter-10-basic-producer-and-consumer-microservices.md):

- **Testing complexity.** The test environment must include the external framework. See Chapter 15's testing discussion.
- **Debugging complexity.** More moving parts, more logs to correlate, more places for bugs to hide.
- **Deployment and rollback complexity.** The framework job and the BPC must be versioned and rolled together, or the bounded-context boundary leaks.
- **Language/feature coverage gaps.** Not every framework supports every language client, and not every feature is available through every client.

The hybrid pattern is a *deliberate* escape hatch, not a default. If you need framework features pervasively, adopt a framework-native microservice — a [[heavyweight-framework-microservice|heavyweight]] (Chapter 11) or lightweight (Chapter 12) framework implementation — instead of stapling one onto a BPC.

## Related pages

- [[basic-producer-consumer-microservice]]
- [[heavyweight-framework-microservice]]
- [[stateless-stream-processing]]
- [[stateful-stream-processing]]
- [[stream-joins]]
- [[event-broker]]
- [[microservice-topology]]
