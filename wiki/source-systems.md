# Source Systems

**Summary**: The first stage of the [[data-engineering-lifecycle|data engineering lifecycle]] — **generation**. A source system is the origin of the data a data engineer consumes: application databases, SaaS APIs, IoT swarms, message queues, flat files. The data engineer usually does **not** own or control the source system, which makes understanding its behaviour (schema, velocity, failure modes, evolution) one of the most important and difficult parts of the job.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The role of the source system

A source system generates data that the engineer must consume, but the engineer typically does not own it. The owning team may migrate to a new database, restructure fields, or introduce new event types without coordinating with the data team. Keeping an open line of communication with source-system owners — about changes that could break pipelines and analytics — is a core part of the job (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

A major challenge of data engineering is simply the **variety** of source systems a single engineer must work with (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Two canonical examples

Chapter 2 anchors the category with two contrasting examples (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Traditional: application + database.** Several application servers backed by a relational database. Popularised in the 1980s with the rise of RDBMSs; today often decomposed into per-service database pairs under [[microservices]] rather than one monolith. See [[oltp-vs-olap]].
- **Modern: IoT swarm + message queue.** A fleet of sensors and smart devices streaming events into a central collection system. Schema and volume profiles are very different from an application DB — high cardinality of producers, event-shaped payloads, messaging-queue transport.

## Key engineering considerations

Chapter 2 lists a starting set of evaluation questions for any source system (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Essential characteristics** — is it an application, IoT swarm, API, spreadsheet, file feed?
- **Persistence** — long-term or ephemeral? Deleted after N days?
- **Generation rate** — events per second, gigabytes per hour.
- **Output consistency** — nulls where unexpected? bad formatting? duplicates? late-arriving data?
- **Error frequency** — how often does the source produce bad or missing records?
- **Schema** — fixed or schemaless? Will joins across tables/systems be required? How are schema changes communicated?
- **Read frequency** — how often to pull? Push or pull pattern?
- **Stateful systems** — periodic snapshots or [[change-data-capture|CDC]] update events? How are changes tracked internally?
- **Data provider identity** — which team/system is responsible for transmitting the data downstream?
- **Read impact** — will querying the source hurt its performance?
- **Upstream dependencies** — does the source itself depend on other systems whose quirks propagate down?
- **Data-quality checks** — in place at the source? downstream?

The common thread: a data engineer must know the source well enough to predict when and how it will misbehave.

## Schema handling at the source

The **schema** defines the hierarchical organisation of data, from whole system down to individual fields. Chapter 2 calls schema "one of the most challenging nuances of source data" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Two dominant handling models:

- **Schemaless** — the application defines the schema as data is written (to a message queue, flat file, blob, or document store like MongoDB). Schemaless does not mean no schema; it means the schema is not enforced by the storage layer.
- **Fixed schema** — enforced by the database (the relational model); all writes must conform.

Both models cause trouble because schemas evolve. Agile development actively encourages [[schema-evolution]], and the engineer's job is to keep pipelines working through those evolutions (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). See [[schema-on-read-vs-write]] for the dual of this choice at the storage layer.

## Coupling to source-system load

Analytical queries run against a source application database can cause resource contention and performance issues for the application itself. The engineer needs to understand the limits of source systems they are consuming from, and often must move data out before running analysis rather than querying in place (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). [[change-data-capture|Log-based CDC]] is popular partly because it sidesteps this coupling — the CDC reader watches the write-ahead log rather than issuing queries.

## Connection to the rest of the lifecycle

Source systems feed directly into [[data-ingestion|ingestion]]. The source-system characteristics (batch vs stream, push vs pull, schema, consistency, error rate) constrain every ingestion choice downstream. Chapter 2 names **source systems and ingestion together** as "the most significant bottlenecks of the data engineering lifecycle" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Categories of source system (Chapter 5)

Chapter 5 enumerates the varieties of source systems a data engineer will meet. The coarse taxonomy (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **[[file-sources|Files and unstructured data]]** — Excel, CSV, JSON, XML, TXT. Despite decades of better alternatives, still universal for cross-organizational data exchange.
- **APIs** — REST, [[graphql|GraphQL]], [[rpc|gRPC]], and [[webhooks]]. The "modern" path but still loaded with custom-integration work.
- **[[application-database-as-source|Application databases]]** — [[oltp-vs-olap|OLTP]] systems backing software applications; the canonical source-system shape.
- **OLAP systems** — [[data-warehousing|data warehouses]] and derived analytics stores, which show up as sources to [[reverse-etl|reverse ETL]] and ML training pipelines.
- **[[change-data-capture|CDC]]** — the source-as-event-stream technique.
- **[[log|Logs]]** — operating system, application, server, container, network, and IoT logs; rich metadata for downstream analysis.
- **[[crud|CRUD]] vs [[insert-only|insert-only]] table patterns** — the state-overwrite vs history-preserving choice at the table level.
- **Messages and streams** — [[message-brokers|message queues]] (discrete, acknowledged delivery) and [[event-streams|event-streaming platforms]] (ordered, retained append-only logs). See both pages for the distinction.
- **[[data-sharing]]** — cloud-native multitenant data access; the emerging alternative to APIs and file feeds.
- **Third-party data sources** — SaaS vendors' and government agencies' data, typically via API, sharing, or download.
- **[[nosql]] database families** — [[key-value-store|key-value]], [[document-model|document]], [[wide-column-database|wide-column]], [[graph-data-models|graph]], [[search-database|search]], [[time-series-database|time-series]].

Chapter 5 explicitly notes the enumeration is **not exhaustive** — new source system types will continue to emerge (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## The Chapter 5 considerations checklist

Chapter 2's starting set of evaluation questions is expanded in Chapter 5 into a fuller practical checklist spanning database characteristics, data shape and volume, cadence and delivery, reliability and quality, source-load impact, and ownership. The expanded list lives on its own page — see [[source-system-considerations]].

## Working with source-system owners

Chapter 5 elevates the stakeholder relationship from a nice-to-have to a core competency. Two classes to identify (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Systems stakeholders.** The software engineers, application developers, or third parties who build and maintain the source system itself.
- **Data stakeholders.** IT, data governance, or third parties who own and control access to the data.

These may or may not be the same people. Reis and Housley: "good diplomacy and relationships with the stakeholders of source systems are an underrated and crucial part of successful data engineering" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). The engineer's goals:

- A bidirectional feedback loop — the source team hears how their data is consumed; the data team hears about impending schema and application changes.
- A [[data-contract]] — written agreement on what data is extracted, by what method (full / incremental), how often, and who to contact. Store it somewhere easy to find; ideally format it so it can be queried programmatically.
- An [[service-level-agreement|SLA]] and [[service-level-objective|SLO]] — expectations for uptime and data quality, measurable and reviewable.

## The undercurrents lens on source systems

Chapter 5 runs each of the six [[data-engineering-lifecycle|lifecycle undercurrents]] against source systems explicitly (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). Headline concerns:

- **[[data-security|Security]]** — encryption at rest and in flight; VPN vs public internet; secret-manager hygiene for credentials; verify the source is legitimate.
- **[[data-management]]** — governance, quality, schema-change communication, MDM, privacy/ethics, regulatory fit.
- **[[dataops]]** — monitor source uptime; alert on schema or quality drift; incident response when the source misbehaves.
- **[[data-architecture]]** — reliability, durability, availability; who owns architectural decisions; SLA with the source-system team.
- **[[orchestration]]** — access cadence; shared Kubernetes clusters or Airflow deployments between application and data workloads.
- **[[software-engineering-for-data]]** — networking, auth, access patterns, retries, deployment of extraction code.

See [[source-system-considerations]] for the expanded per-undercurrent question list.

## Cross-book connections

- [[event-driven-microservices]] invert the framing: rather than the data engineer reverse-engineering the source, the source team is expected to expose a first-class [[event-streams|event stream]] as a proper product. Bellemare's [[data-liberation]] and [[outbox-table-pattern]] are both explicit proposals for graduating from "source system as unknowable black box" to "source system as event producer" — the mature end-state of the source-system problem this page names.
- [[change-data-capture]] is the most common technical pattern for extracting data from a source system without cooperation from its owners.
- Reis and Housley's Chapter 5 closing observation: "better collaboration with source system teams can lead to higher-quality data, more successful outcomes, and better data products." Build shared systems where it makes sense; look for user-facing data products that make application teams stakeholders in data engineering (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Related pages

- [[data-engineering-lifecycle]]
- [[data-ingestion]]
- [[source-system-considerations]]
- [[application-database-as-source]]
- [[change-data-capture]]
- [[schema-evolution]]
- [[schema-on-read-vs-write]]
- [[data-liberation]]
- [[event-streams]]
- [[oltp-vs-olap]]
- [[file-sources]]
- [[nosql]]
- [[data-sharing]]
- [[webhooks]]
- [[graphql]]
- [[data-contract]]
- [[data-engineer-stakeholders]]
- [[crud]]
- [[insert-only]]
