# Basic Producer and Consumer Microservice

**Summary**: A **BPC** microservice is an [[event-driven-microservices|EDM]] built directly on the event broker's basic producer and consumer clients, without the event scheduling, watermarks, internal state materialization, changelog management, or partition-aware horizontal scaling that a full stream-processing framework (Chapters 11–12 of BEDM) provides. BPCs are simple, portable across languages, and excel when the data layer does most of the work or when integrating with legacy systems. When you need deterministic ordering or rich local state, reach for a framework instead.

**Sources**: `raw/building-event-driven-microservices/chapter-10-basic-producer-and-consumer-microservices.md`

**Last updated**: 2026-04-17

---

## What "basic" means

A BPC is defined by what its client library *doesn't* do (source: chapter-10-basic-producer-and-consumer-microservices.md):

- No event scheduling across streams (no cross-stream timestamp coordination — contrast [[event-scheduling]] / [[watermarks]]).
- No built-in materialization of state ([[changelog-stream]] / [[internal-state-store]] management is manual).
- No horizontal scaling primitives for *local* state — repartitioning a stateful BPC across instances is hard without framework support.
- No library-level support for things like [[stream-joins]] or [[windowing]].

What it *does* offer is a raw `consume(partition) → transform → produce(output)` loop in whatever language the team prefers, plus whatever business logic the developer writes. Producer and consumer clients are broadly available (Kafka, Pulsar, Kinesis SDKs in nearly every mainstream language), which is a big part of the pattern's appeal.

The entire bounded-context workflow lives in one application binary, typically one container, managed by the team's [[container-management-system]]. Responsibilities stay local and easy to reason about.

## When BPCs work well

Chapter 10 enumerates five good fits (source: chapter-10-basic-producer-and-consumer-microservices.md):

### 1. Stateless transformations

Any [[stateless-stream-processing]] topology — filtering, projection, enrichment by static lookup, simple [[event-transformations]] — is a natural fit. No state to manage, no framework needed.

### 2. Integration with existing and legacy systems

A legacy codebase can adopt the event broker as its [[event-as-single-source-of-truth|single source of truth]] by embedding a basic producer/consumer client. This is often how [[data-liberation]] begins: the legacy system starts producing its domain data to a stream and consuming back events it needs from others. When the legacy codebase cannot be safely modified, the [[sidecar-pattern]] is the usual escape hatch — a BPC sidecar container reads events and writes to the legacy system's data store without touching its source.

### 3. Stateful logic that doesn't depend on event order

The **[[gating-pattern]]** — wait for a known set of events to all arrive (in any order) before emitting an outcome — is the canonical BPC-friendly stateful pattern. BPCs can handle this because there is no need for deterministic cross-stream scheduling; each incoming event simply updates a table and checks the other tables.

### 4. When the data layer does most of the work

If the business logic lives in a geospatial database, a full-text search engine, a machine-learning classifier, or some other specialized data store, the processing layer's job is just to shuttle events in and out. The BPC is a thin integration seam; the *work* is in the store. Correlating user-location events with a geospatial store to pick nearby retailers, or classifying scraped products through a batch-trained categorizer, are both prototypical BPC uses.

### 5. Independent scaling of processing and data layers

When compute needs vary independently from storage needs — for example, the sleep/wake cycle of a user population makes daytime 10× busier than nighttime, but the *size* of per-user state stays constant — the BPC pattern pairs well with an [[external-state-store]]. You scale processing instances up and down freely; the store holds the full domain regardless of how many instances are running. Hosted pay-per-read/write stores (DynamoDB, Bigtable, Cosmos DB) accommodate this naturally.

## External state is the usual pairing

BPCs typically use an [[external-state-store]] rather than an [[internal-state-store]]. Scaling local state across multiple instances, and recovering it after instance failures, is difficult without framework support. An external store gives every instance uniform access, backup/restore, and off-the-shelf recovery semantics — at the cost of network latency on every lookup (source: chapter-10-basic-producer-and-consumer-microservices.md).

This is why Chapter 7's [[external-state-store]] page explicitly calls out BPC and [[functions-as-a-service]] as its best-fit consumers.

## Hybrid BPC + external stream processing

When a BPC hits a problem that a real stream-processing framework solves well — joining large materialized streams, aggregating across partitions, running SQL over streams — the **[[hybrid-bpc-stream-processing|hybrid pattern]]** is available: the BPC instantiates a client that submits the heavy work to an external framework (Kafka Streams, Flink, KSQL), reads the output back from an intermediate event stream, and carries on. Bellemare uses this as an explicit escape valve rather than a replacement for the BPC model.

## What you give up

Choosing BPC over a framework means accepting that you will **build by hand** any of the following that your service ends up needing (source: chapter-10-basic-producer-and-consumer-microservices.md):

- State materialization and changelog management.
- Event scheduling and watermark-based timestamp ordering.
- [[effectively-once-processing]] — broker transactions and offsets-in-state must be wired manually.
- Horizontal scaling of local state (usually solved by switching to an external store, which has its own costs).
- [[stream-joins|Stream-table]] and stream-stream joins.

The pattern is *flexible*, not *featureful*. The question each team must answer up front is: how much of the above will we end up needing, and is it cheaper to write it ourselves in a BPC or to adopt a full framework?

## Where BPC sits in the EDM family

| Implementation style | Typical features | Chapter |
|---|---|---|
| **BPC** (this page) | Raw producer/consumer clients; external state the default; language-flexible | 10 |
| [[functions-as-a-service]] | BPC-ish but per-event; ephemeral compute; managed runtime | 9 |
| [[heavyweight-framework-microservice\|Heavyweight framework]] | Full stream-processing cluster (Spark, Flink, Storm, Heron, Beam) | 11 |
| [[lightweight-framework-microservice\|Lightweight framework]] | BPC plus some framework amenities (e.g. Kafka Streams as a library) | 12 |

The BPC is the lowest rung on this ladder. It is often the *right* rung — especially for integration work, sidecars, and data-layer-dominant services — but it is deliberately spartan.

## Related pages

- [[event-driven-microservices]]
- [[microservice-topology]]
- [[stateless-stream-processing]]
- [[stateful-stream-processing]]
- [[external-state-store]]
- [[gating-pattern]]
- [[hybrid-bpc-stream-processing]]
- [[sidecar-pattern]]
- [[data-liberation]]
- [[event-sinking]]
- [[effectively-once-processing]]
- [[functions-as-a-service]]
- [[event-broker]]
- [[consumer-group]]
- [[lightweight-framework-microservice]]
- [[heavyweight-framework-microservice]]
