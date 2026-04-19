# Ingestion Frequency

**Summary**: How often data flows from source to destination — one of the first architectural decisions in [[data-ingestion]]. Reis and Housley lay out a spectrum from yearly batch at one extreme to continuous near-real-time at the other, name the three practical modes (batch, micro-batch, real-time), and warn that "real-time" is always *near* real-time because every pipeline has inherent latency.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The spectrum

Ingestion frequencies "vary dramatically from slow to fast" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

| Frequency | Example |
|---|---|
| Yearly | A business ships its tax data to an accounting firm once a year |
| Daily / hourly | Classic overnight ETL for daily reporting |
| Minute-scale | A [[change-data-capture|CDC]] system pulls log updates every minute |
| Seconds | Continuous processing of IoT sensor events as they arrive |

Frequencies are "often mixed in a company, depending on the use case and technologies" — there is no single right answer for an enterprise (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## The three practical modes

- **Batch.** Data is processed in discrete, time- or size-bounded chunks. The default for traditional ETL.
- **Micro-batch.** Batches over very short intervals (seconds or a few minutes). The compromise mode.
- **Real-time / streaming.** Events are processed one by one (or in micro-batches) as they arrive.

Ch 7 uses **real-time** and **streaming** interchangeably and notes the pattern is "becoming increasingly common" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## "Real-time" is always near-real-time

Reis and Housley put quotes around "real-time" deliberately: **no ingestion system is genuinely real-time**. Every database, queue, and pipeline introduces some latency in delivering data to a target. Near-real-time "does away with an explicit update frequency" — events are processed either one by one or in micro-batches as they arrive (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Batch is usually somewhere in every pipeline

Even with streaming ingestion, "batch processing downstream is relatively standard." Ch 7 observes that ML models are typically trained on a batch basis (though continuous online training is becoming more common), and that engineers "rarely have the option to build a purely near-real-time pipeline with no batch components." Instead, they **choose where batch boundaries will occur** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Once data reaches a batch process, **the batch frequency becomes a bottleneck for all downstream processing** — a critical architectural constraint.

## When streaming is the natural fit

Even though batch is often the practical default (see [[data-ingestion]]'s discussion of the streaming-first checklist), Ch 7 names two clear streaming-native cases (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **IoT.** Each sensor writes events or measurements as they happen; a streaming ingestion platform (Kinesis, Kafka) is a better fit than writing each event directly to a database.
- **Event-driven applications.** Software that already exchanges messages through queues can adopt the pattern natively — writing events to a message queue as they happen rather than waiting for an extraction process to pull state from a backend database.

This second case aligns directly with [[event-driven-microservices]] and the [[data-liberation]] patterns — publishing events at the source is the modern alternative to extracting them out of the transactional database later.

## Relation to synchronous vs asynchronous

Frequency and sync/async are distinct but related. Low-frequency (daily batch) ingestion tends to be synchronous — extract, transform, load, each step waiting on the last. High-frequency streaming ingestion is almost always [[event-driven-architecture|asynchronous]] — each event flows through the pipeline as it arrives, buffered by the streaming platform. See [[data-ingestion]] for the sync/async axis.

## Related pages

- [[data-ingestion]]
- [[batch-processing]]
- [[stream-processing]]
- [[change-data-capture]]
- [[event-streams]]
- [[message-brokers]]
- [[data-pipeline]]
