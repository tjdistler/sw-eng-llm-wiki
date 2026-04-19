# Kappa Architecture

**Summary**: Jay Kreps's 2014 counter-proposal to [[lambda-architecture]]: use a single stream-processing platform as the backbone for **all** data handling — ingestion, storage, and serving — and apply real-time or batch processing to the same event stream by replaying as needed. Influential in shaping unified batch/stream thinking; less adopted in practice than its descendants.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The thesis

Chapter 3 quotes the central idea (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> Why not just use a stream-processing platform as the backbone for all data handling — ingestion, storage, and serving?

This facilitates a true event-based architecture. Real-time and batch processing are applied to **the same stream** by:

- Reading the live event stream directly for real-time
- Replaying large chunks of the stored stream for batch

There is one codebase, one storage layer, and one execution model — the motivation for Kreps's original objection to [[lambda-architecture]]'s dual maintenance burden.

## Why it didn't take over

Chapter 3 names two reasons the architecture has not been widely adopted, despite appearing in 2014 (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Streaming is still a bit of a mystery for many companies** — the operational expertise required is scarce
2. **Complicated and expensive in practice** — streaming systems scale to huge volumes but cost more per unit of work than batch; batch storage and processing remain more efficient and cost-effective for enormous historical datasets

The pure Kappa ideal gave way to hybrid approaches — see [[dataflow-model]] — that preserve the single-codebase property without forcing the single-storage-layer property.

## Relationship to Lambda and Dataflow

- [[lambda-architecture]] — the predecessor Kappa was reacting against; runs batch and stream in parallel, merges outputs
- **Kappa** — rejects the dual path; one stream-processing backbone
- [[dataflow-model]] — treats batch as a special case of streaming at the **programming-model** level, letting the engine pick the right execution substrate for each workload

The progression is what Chapter 3 calls the trajectory of unifying batch and streaming (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## The live data stack revival (Chapter 11)

Chapter 11's [[live-data-stack]] prediction is the practical, cloud-managed descendant of the Kappa idea. Where Kappa struggled because streaming was "a bit of a mystery" and expensive, the live data stack arrives after a decade of managed cloud stream processors (Kinesis Data Analytics, Dataflow, Pulsar) and purpose-built [[real-time-olap|real-time OLAP databases]] (Druid, ClickHouse, Rockset, Firebolt) that make the Kappa shape economically viable (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

Specifically the live data stack adopts from Kappa:

- **Streaming substrate** as the backbone of all data handling.
- **[[stream-transform-load|STL]]** — a streaming-native successor to ELT that moves transformation into the stream.
- **Unified event source** between application, analytics, and ML.

But extends beyond Kappa:

- Purpose-built real-time OLAP for the read side (Kappa left the serving layer vague).
- Fusion with ML feedback loops — see [[data-application-fusion]].
- Managed cloud services, not self-hosted Kafka clusters.

## Cross-book connections

- DDIA's discussion of unifying batch and stream (see [[lambda-architecture]]) independently arrives at the same Kappa-adjacent conclusions
- [[log-based-message-brokers]] (Kafka) is the enabling technology that made Kreps's replay story operationally credible
- [[event-sourcing]] shares the "events as the system of record" posture

## Related pages

- [[lambda-architecture]]
- [[dataflow-model]]
- [[stream-processing]]
- [[batch-processing]]
- [[log-based-message-brokers]]
- [[event-sourcing]]
- [[data-architecture]]
- [[live-data-stack]]
- [[real-time-olap]]
- [[stream-transform-load]]
- [[future-of-data-engineering]]
