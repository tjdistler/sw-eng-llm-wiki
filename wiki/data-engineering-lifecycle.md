# Data Engineering Lifecycle

**Summary**: Reis and Housley's organising idea for the entire discipline — a five-stage pipeline (generation, storage, ingestion, transformation, serving) crossed by six "undercurrents" that apply at every stage (security, data management, DataOps, data architecture, orchestration, software engineering). The lifecycle is deliberately technology-agnostic: its point is to shift the conversation from tools to the data itself and the end goals it serves.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## Why a lifecycle framing

It is easy to fixate on technology and miss the bigger picture. The lifecycle forces the conversation up one level — away from "which streaming engine?" and toward "what does this data do for the business, and what does it need along the way?" (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

The data engineering lifecycle is a **subset** of the broader data lifecycle. The full data lifecycle covers data across its entire lifespan (from creation by an end user to archival or destruction); the data engineering lifecycle focuses on the stages a data engineer controls (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The five stages are rarely a clean linear flow. Storage in particular underpins the other stages rather than sitting beside them; ingestion, transformation, and storage can get "jumbled" in practice, and stages may repeat, overlap, or occur out of order (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## The five stages

Raw data enters at **generation** and exits at **serving**. Between those endpoints it is persisted, moved, and reshaped (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

1. **Generation** — source systems create the data: application databases, SaaS APIs, event streams, IoT devices, logs. See [[source-systems]].
2. **Storage** — persisting the data at each stage where it lives at rest: object stores, warehouses, lakes, caches, streaming logs. See [[data-storage-stage]].
3. **Ingestion** — moving data from generators into storage. Batch or streaming; push or pull. See [[data-ingestion]].
4. **Transformation** — shaping data into something analytics- or ML-ready: joins, aggregations, feature engineering, modeling. See [[data-transformation]].
5. **Serving** — delivering data to consumers: analysts, ML systems, reverse-ETL back to operational systems. See [[data-serving]].

Compare with the [[event-driven-microservices]] view, where the [[event-broker]] serves as the central substrate and producers/consumers are microservices; the FoDE lifecycle is the same kinds of concerns framed as a pipeline rather than a mesh.

### Why the stages entangle

Chapter 2 is explicit that the stages interleave in real systems (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Storage runs across everything.** Data is stored during ingestion (staging areas, object stores), between transformations (intermediate tables), and at the serving layer (warehouses, caches). Some systems collapse two stages into one — [[data-warehousing|cloud data warehouses]] store, transform, and serve all from the same engine; [[log-based-message-brokers|Kafka]] and Pulsar ingest, store, and query streams all at once.
- **Transformations happen in flight.** A source system may stamp an event timestamp before emitting; an ingestion pipeline may enrich records in flight; a streaming job may calculate aggregates on the way to the warehouse. Transformation is not confined to a single step.

## The six undercurrents

Concerns that cut across every stage, not confined to any one step (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md) (elaborated in source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **[[data-security|Security]]** — encryption, access control, [[least-privilege]], multi-tenant isolation, timing of access.
- **[[data-management|Data management]]** — [[data-governance|governance]], [[data-quality|quality]], [[master-data-management|master data]], [[data-lineage|lineage]], [[data-modeling|modeling]], [[metadata|metadata]], [[data-lifecycle-management|lifecycle management]], ethics and privacy.
- **[[dataops|DataOps]]** — automation, observability and monitoring, incident response.
- **[[data-architecture|Data architecture]]** — big-picture choices about where data lives and how it moves.
- **[[orchestration|Orchestration]]** — scheduling, dependency management, and triggering of pipelines (Airflow, Dagster, Prefect-style tools).
- **[[software-engineering-for-data|Software engineering]]** — version control, testing, code review, CI/CD, [[infrastructure-as-code|IaC]], pipelines-as-code, general-purpose problem solving applied to data code.

No part of the data engineering lifecycle can adequately function without these undercurrents (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Mapping to existing wiki concepts

The lifecycle concretely touches concepts already in the wiki:

| Lifecycle stage | Related existing pages |
|---|---|
| Generation | [[source-systems]], [[change-data-capture]], [[event-driven-architecture]], [[data-liberation]] |
| Storage | [[data-storage-stage]], [[data-warehousing]], [[data-lake]], [[data-lakehouse]], [[column-oriented-storage]], [[distributed-filesystems]], [[log-based-message-brokers]], [[data-temperature]] |
| Ingestion | [[data-ingestion]], [[batch-processing]], [[stream-processing]], [[change-data-capture]], [[etl-vs-elt]] |
| Transformation | [[data-transformation]], [[mapreduce]], [[dataflow-engines]], [[stream-processing]], [[windowing]], [[data-modeling]] |
| Serving | [[data-serving]], [[analytics]], [[reverse-etl]], [[feature-store]], [[oltp-vs-olap]], [[serving-state-from-edm]], [[materialized-state]] |

| Undercurrent | Related existing pages |
|---|---|
| Security | [[data-security]], [[least-privilege]], [[defense-in-depth-data]], [[event-stream-acls]] |
| Data management | [[data-management]], [[data-governance]], [[data-quality]], [[metadata]], [[master-data-management]], [[data-lineage]], [[data-contract]], [[schema-registry]], [[data-integrity-principles]], [[data-ethics]], [[data-lifecycle-management]] |
| DataOps | [[dataops]], [[data-observability]], [[data-validation-pipelines]] |
| Data architecture | [[data-architecture]], [[lambda-architecture]], [[unbundling-databases]] |
| Orchestration | [[orchestration]], [[distributed-cron]], [[data-processing-pipelines]], [[google-workflow]] |
| Software engineering | [[software-engineering-for-data]], [[infrastructure-as-code]], [[continuous-integration-delivery-deployment]], [[schema-evolution]], [[backward-forward-compatibility]] |

## The "data lifecycle engineer"

Chapter 1 argues that the modern data engineer is more precisely described as a **data lifecycle engineer** — no longer spending most time on low-level framework internals (Hadoop, Informatica, early Spark), but instead on everything above them: security, data management, DataOps, architecture, orchestration, and general lifecycle management. As cloud services absorb the plumbing, the value moves up the stack (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Top-level goals

Chapter 2's conclusion names three top-level goals a data engineer pursues across the lifecycle (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

1. **Produce optimum ROI and reduce costs** — financial and opportunity cost.
2. **Reduce risk** — security breaches, data quality defects.
3. **Maximise data value and utility** — ensure data gets used, not merely stored.

## The lifecycle in the live data stack (Chapter 11)

Chapter 11's closing prediction explicitly preserves the lifecycle while collapsing the time between its stages (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

> The data engineering lifecycle won't necessarily change, but the time between stages of the lifecycle will drastically shorten.

In the [[live-data-stack]]:

- **Generation** and **serving** fuse into each other via [[data-application-fusion|data-application fusion]]. Applications emit events; stream processors react; ML models infer; the result flows back into the application.
- **Ingestion** is continuous, not scheduled. See [[ingestion-frequency]].
- **Transformation** moves into the stream — [[stream-transform-load|STL]] replaces ELT.
- **Storage** adds [[real-time-olap|real-time OLAP]] as a new dominant abstraction for the live backend.
- **All five stages are instrumented by [[enterprisey-data-engineering|enterprisey]] governance and quality** as the technology hard parts get abstracted away.

Chapter 11's framing: the lifecycle is the durable idea; the shape of each stage evolves as the tooling matures. See [[future-of-data-engineering]].

## Related pages

- [[data-engineer]]
- [[data-maturity]]
- [[dataops]]
- [[fundamentals-of-data-engineering]]
- [[data-engineering-history]]
- [[event-driven-microservices]]
- [[event-as-single-source-of-truth]]
- [[future-of-data-engineering]]
- [[live-data-stack]]
