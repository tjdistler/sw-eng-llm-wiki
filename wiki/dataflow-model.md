# Dataflow Model

**Summary**: Google's programming model (and the Apache Beam framework that implements it) for unifying batch and stream processing under a single API. The central move: treat all data as events, treat batches as bounded streams, and let the engine choose the execution substrate. "Batch as a special case of streaming" — the position Chapter 3 names as the current trajectory for unifying these two worlds.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The idea

Chapter 3 credits Google with the Dataflow model and Apache Beam as its open-source implementation (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> The core idea in the Dataflow model is to view all data as events, as the aggregation is performed over various types of windows. Ongoing real-time event streams are unbounded data. Data batches are simply bounded event streams, and the boundaries provide a natural window.

Engineers choose from various windows for real-time aggregation — **sliding**, **tumbling**, **session**, etc. See [[windowing]]. Real-time and batch processing happen in the same system with **nearly identical code** — no dual codebase (unlike [[lambda-architecture]]), no streaming-only substrate (unlike [[kappa-architecture]]).

## Why it succeeded where Kappa stalled

Chapter 3 frames the progression (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- [[lambda-architecture]] duct-taped tools that weren't natural fits
- [[kappa-architecture]] unified the **storage** layer but still forced a particular execution substrate
- Dataflow unifies the **programming model** and lets the engine make the execution choice

The philosophy of "batch as a special case of streaming" is now pervasive. Chapter 3 names Flink and Spark as frameworks that have adopted a similar approach. Spark breaks streams into microbatches; Flink performs batch processing atop a streaming engine.

## Cross-book framing

[[lambda-architecture]]'s page quotes DDIA Chapter 12's own take on unified batch and stream processing, which arrives at the same three requirements:

- Replay historical events through the same engine that handles live events ([[log-based-message-brokers]])
- [[exactly-once-semantics]]
- [[windowing]] by event time rather than processing time

The Dataflow model is the practical delivery of those requirements.

## Theoretical backbone of the live data stack (Chapter 11)

Chapter 11's [[live-data-stack]] prediction leans directly on the Dataflow model's unification. Once you accept that batch is a bounded stream, [[stream-transform-load|STL]] (the streaming-era transformation shape) becomes the default and batch becomes the special case used for model training, quarterly reporting, and other bounded workloads. Managed stream processors (Kinesis Data Analytics, Google Cloud Dataflow — the namesake!) are the commodified operational layer that makes the programming model practical for companies that aren't Google (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

The Dataflow model is also the bridge between the [[modern-data-stack|MDS]] and the live data stack. The MDS's ELT still fits Dataflow's programming model (it's batch = bounded-stream); the live data stack's STL is the same model with extraction set to "unbounded."

## Relation to [[event-driven-architecture]]

In Richards and Ford's architecture-style vocabulary, a Dataflow/Beam job sits comfortably inside [[event-driven-architecture|event-driven]] territory — events flow through channels, processors transform and aggregate them. The difference is that Dataflow is a *programming model* and execution engine, whereas event-driven architecture is an architectural style covering a much broader design surface.

## Related pages

- [[lambda-architecture]]
- [[kappa-architecture]]
- [[stream-processing]]
- [[batch-processing]]
- [[windowing]]
- [[watermarks]]
- [[exactly-once-semantics]]
- [[dataflow-engines]]
- [[event-driven-architecture]]
- [[data-architecture]]
- [[live-data-stack]]
- [[stream-transform-load]]
- [[future-of-data-engineering]]
