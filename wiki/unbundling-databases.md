# Unbundling Databases

**Summary**: The idea of decomposing the features traditionally bundled inside a monolithic database (indexes, materialized views, replication, full-text search) into separate, composable systems connected by event logs and change data capture -- the "database inside-out" approach.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## The parallel between databases and dataflow

Databases internally maintain secondary indexes, materialized views, replication logs, and full-text search indexes. Batch and stream processing systems build the same things externally: search indexes, materialized view maintenance, and data replication across derived systems. The parallel is deep -- running `CREATE INDEX` is remarkably similar to bootstrapping [[change-data-capture]] in a streaming system. Both reprocess existing data to derive a new view (source: chapter-12-the-future-of-data-systems.md).

## The meta-database of everything

The dataflow across an entire organization looks like one huge database. Batch, stream, and ETL processes that transport data from one place to another are acting like database subsystems that keep indexes and materialized views up to date. Stream processors are like elaborate implementations of triggers and stored procedures. The derived data systems they maintain are like different index types (source: chapter-12-the-future-of-data-systems.md).

## Two approaches to composition

Since no single data model or storage format suits all access patterns, there are two ways to compose different tools into a cohesive system (source: chapter-12-the-future-of-data-systems.md):

### Federated databases (unifying reads)

A unified query interface over multiple underlying storage engines -- also called a **polystore**. PostgreSQL's foreign data wrappers are an example. This follows the relational tradition: a single high-level query language with elegant semantics but complicated implementation. Federation addresses read-only querying but has no good answer for synchronizing writes (source: chapter-12-the-future-of-data-systems.md).

### Unbundled databases (unifying writes)

Reliably synchronizing writes across disparate technologies using [[change-data-capture]] and event logs -- like unbundling a database's index-maintenance features so they can work across heterogeneous systems. This follows the [[unix-philosophy]]: small tools that do one thing well, communicating through a uniform low-level API (source: chapter-12-the-future-of-data-systems.md).

## Making unbundling work

The traditional approach to write synchronization is [[distributed-transactions]] across heterogeneous systems, which Kleppmann considers the wrong solution. An asynchronous event log with [[exactly-once-semantics|idempotent writes]] is more robust and practical (source: chapter-12-the-future-of-data-systems.md).

The advantage of log-based integration is **loose coupling** at two levels:

1. **System level**: asynchronous event streams buffer messages during outages or slowdowns. A failing consumer can catch up when fixed without affecting producers or other consumers. By contrast, [[distributed-transactions]] escalate local faults into large-scale failures.
2. **Human level**: different teams can develop, improve, and maintain components independently, with event logs as the interface between them.

## What's missing

The ecosystem lacks a "Unix shell" for data systems -- a high-level declarative language for composing storage and processing systems. Kleppmann imagines declaring `mysql | elasticsearch` (by analogy to Unix pipes) to mean: take all documents in MySQL, index them in Elasticsearch, and continuously apply changes. Differential dataflow is early-stage research in this direction (source: chapter-12-the-future-of-data-systems.md).

## Designing applications around dataflow

The "database inside-out" design pattern (term coined by Jay Kreps) treats application code as a derivation function. Examples of derivation functions (source: chapter-12-the-future-of-data-systems.md):

- A **secondary index** picks out field values and sorts by them
- A **full-text search index** applies NLP (stemming, synonyms) and builds an inverted index
- A **machine learning model** is derived from training data via feature extraction
- A **cache** aggregates data in the form displayed by the UI

### Separation of application code and state

Rather than embedding application logic inside the database (stored procedures, triggers), modern practice separates stateless application logic (deployed on Kubernetes, Mesos, YARN) from durable state management (databases). Stream processing and messaging systems bridge the two, allowing application code to respond to state changes (source: chapter-12-the-future-of-data-systems.md).

### Dataflow vs microservices

Composing [[stream-processing|stream operators]] into dataflow systems resembles the microservices approach but uses **asynchronous, one-directional message streams** instead of synchronous request/response (REST). The dataflow approach can be both faster and more fault-tolerant -- for example, subscribing to exchange rate updates and querying a local copy instead of making a synchronous RPC to a remote service (source: chapter-12-the-future-of-data-systems.md).

## Unbundled vs integrated

Unbundling does not replace databases. Specialized query engines (MPP data warehouses, etc.) remain important for particular workloads. The goal of unbundling is **breadth**, not depth: combining several databases to achieve good performance across a wider range of workloads than any single system can provide. If one technology does everything you need, use it (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[data-integration]]
- [[derived-data]]
- [[unix-philosophy]]
- [[distributed-transactions]]
- [[change-data-capture]]
- [[stream-processing]]
- [[batch-processing]]
- [[exactly-once-semantics]]
- [[lambda-architecture]]
