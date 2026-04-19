# Partitioning

**Summary**: Partitioning (also called sharding) splits a large dataset across multiple nodes so that data and query load can scale beyond what a single machine can handle.

**Sources**: raw/designing-data-intensive-applications/chapter-06-partitioning.md, raw/designing-data-intensive-applications/chapter-11-stream-processing.md, raw/designing-distributed-systems/chapter-03-ambassadors.md, raw/designing-distributed-systems/chapter-06-sharded-services.md, raw/designing-distributed-systems/chapter-07-scattergather.md, raw/fundamentals-of-data-engineering/chapter-06-storage.md

**Last updated**: 2026-04-18

---

## What partitioning is

Partitioning means intentionally breaking a large database into smaller subsets, where each record belongs to exactly one partition. In effect, each partition is a small database of its own, although the database may support operations that touch multiple partitions at the same time (source: chapter-06-partitioning.md).

| System | Term for partition |
|---|---|
| MongoDB, Elasticsearch, SolrCloud | shard |
| HBase | region |
| Bigtable | tablet |
| Cassandra, Riak | vnode |
| Couchbase | vBucket |

Partitioning is distinct from network partitions (netsplits), which are fault conditions, not a design choice.

## Why partition

The primary motivation is [[scalability]]. Distributing data across many nodes in a shared-nothing cluster means:

- A large dataset can span many disks.
- Query load can spread across many processors.
- Queries on a single partition can execute independently, so throughput scales with nodes.

Partitioned databases were pioneered in the 1980s (Teradata, Tandem NonStop SQL) and rediscovered by NoSQL systems and Hadoop-based warehouses. The approach applies equally to [[oltp-vs-olap|OLTP and OLAP]] workloads.

## Relationship to replication

Partitioning is almost always combined with [[replication]] so that each partition has copies on multiple nodes for fault tolerance. A node typically acts as leader for some partitions and follower for others (see [[leader-based-replication]]). The choice of partitioning scheme is largely independent of the replication scheme.

## Core challenge: avoiding skew and hot spots

The goal of partitioning is to spread data and load *evenly*. When some partitions carry more data or queries than others, the distribution is *skewed*. A partition with disproportionately high load is a *hot spot*. A single hot spot can negate the benefits of partitioning entirely — 9 out of 10 nodes sit idle while one is overloaded.

See [[hot-spots]] and [[partitioning-strategies]] for the mechanisms that cause and prevent skew.

## Key decisions

| Concern | Concept page |
|---|---|
| How to assign records to partitions | [[partitioning-strategies]] |
| Skew and hot spots | [[hot-spots]] |
| Secondary indexes across partitions | [[partitioning-secondary-indexes]] |
| Moving partitions when topology changes | [[rebalancing-partitions]] |
| Routing client requests to the right node | [[request-routing]] |

## Parallel query execution

Most NoSQL distributed datastores support only simple queries that read or write a single key (plus scatter/gather for document-partitioned secondary indexes — see [[partitioning-secondary-indexes]] and the general [[scatter-gather-pattern]]). However, massively parallel processing (MPP) relational database products, often used for [[data-warehousing|analytics]], support much more sophisticated queries. The MPP query optimizer breaks complex queries -- involving joins, filtering, grouping, and aggregation -- into execution stages and partitions, many of which run in parallel on different nodes. Queries that scan large parts of the dataset particularly benefit from parallel execution (source: chapter-06-partitioning.md). MPP query execution is effectively scatter/gather at the analytics layer — see [[hadoop-vs-mpp-databases]].

## Partitioning in batch processing

Partitioning is central to [[batch-processing]] systems. In [[mapreduce]], the input is partitioned by file blocks (each block is a separate map task), and mapper output is repartitioned by a hash of the key to assign key-value pairs to reducers. The shuffle process — partitioning, sorting, and copying data from mappers to reducers — brings all records with the same key to the same place (source: designing-data-intensive-applications, chapter 10).

[[map-side-joins]] require specific partitioning properties of input datasets: matching partition count, same key, same hash function. Metadata about how datasets are partitioned (maintained in HCatalog / Hive metastore) is essential for optimizing join strategies (source: designing-data-intensive-applications, chapter 10).

[[dataflow-engines]] (Spark, Tez, Flink) take a similar approach to partitioning but avoid unnecessary sorting and can repartition without it when only the partitioning matters (e.g., for partitioned hash joins) (source: designing-data-intensive-applications, chapter 10).

## Partitioning in stream processing

[[log-based-message-brokers]] use partitioning to scale beyond a single disk's throughput. A topic is divided into partitions, each hosted on a different machine. Within each partition, messages are assigned monotonically increasing offsets and are totally ordered; there is no ordering guarantee across partitions (source: chapter-11-stream-processing.md).

Load balancing in log-based brokers works at the partition level rather than per-message: entire partitions are assigned to consumer nodes. This means the maximum parallelism is bounded by the number of partitions (unlike AMQP/JMS-style [[message-brokers]] where individual messages can be distributed). See [[log-based-message-brokers]] (source: chapter-11-stream-processing.md).

Stream processing state can also be partitioned to match the event log: if events for a customer in partition 3 only require updating partition 3 of the application state, a single-threaded log consumer needs no concurrency control for writes. See [[event-sourcing]] (source: chapter-11-stream-processing.md).

## Partitioning and clustering for analytics

Chapter 6 of *Fundamentals of Data Engineering* frames analytics-side partitioning as the complement to [[column-oriented-storage|columnar storage]]: columnar scans the needed columns, partitioning further shrinks the scanned *rows* (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

- **Time-based partitioning** dominates. "It is quite common in analytics and data science use cases to scan over a time range, so date- and time-based partitioning is extremely common."
- **Clustering** is the finer-grained sibling: within a partition, data is sorted by one or more fields so similar values are colocated. This speeds filters, sorts, and joins on those fields.
- The trade-off is the same as with [[indexes]] — partitioning and clustering add write overhead and storage layout cost for better read performance.

### Snowflake's micro-partitioning

Chapter 6 calls out Snowflake's **micro-partitioning** as a recent evolution (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Instead of the naive "partition on a single designated field" approach, Snowflake:

- Groups rows into 50–500 MB micro-partitions.
- Algorithmically clusters micro-partitions on repeated-value fields across many rows.
- Supports overlapping micro-partitions, allowing effective partitioning on multiple fields.
- Maintains a metadata database of per-micro-partition value ranges and row counts.
- At query time, prunes micro-partitions whose metadata rules them out of the predicate — "Snowflake excludes any micro-partitions that don't include this date."

Chapter 6 labels this **hybrid columnar storage**: columnar at the byte layout, but broken into small row groups governed by a metadata index. The metadata serves the same role a traditional index serves in an OLTP database.

This architecture is also the shape the [[lakehouse-table-formats|Delta Lake / Iceberg / Hudi]] table formats converge toward — file-level metadata that lets the query engine skip irrelevant data.

## Client integration via ambassadors

Connecting clients to a sharded backend is itself a design decision. One option is to build the sharding logic into a server-side load balancer; another is to run a **client-side sharding ambassador** in each client's pod that presents the sharded cluster as a single `localhost` endpoint. Burns covers the ambassador option in Chapter 3 of *Designing Distributed Systems* with a worked twemproxy/Redis/ketama example (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). Either approach is valid; the trade-off is complexity on the client pod vs complexity on the sharded service. See [[client-side-sharding]] and [[ambassador-pattern]].

## Partitioning applied to stateful serving tiers

DDIA's partitioning is framed in terms of databases, but the same ideas recur in the design of stateful **serving** tiers — caches, session stores, game worlds, any service whose working-set exceeds one machine. Burns's Chapter 6 of *Designing Distributed Systems* names this the [[sharded-service-pattern]]: a root routes each request to one shard based on a sharding function, each shard owns a subset of the state, and losing a shard takes out the requests mapped to it. The design questions (shard count, shard key, re-sharding cost, hot shards) are the same as at the database layer, and the same vocabulary applies: [[partitioning-strategies]], [[consistent-hashing]], [[hot-spots]], [[rebalancing-partitions]], [[request-routing]]. What is distinctive at the service layer is the operational story — how you roll out a new shard, how you replicate shards for reliability ([[replicated-sharded-service]]), and how you respond to organic traffic skew ([[hot-sharding]]) — which Burns's chapter treats directly (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## Related pages

- [[replication]]
- [[scalability]]
- [[partitioning-strategies]]
- [[hot-spots]]
- [[partitioning-secondary-indexes]]
- [[rebalancing-partitions]]
- [[request-routing]]
- [[indexes]]
- [[batch-processing]]
- [[mapreduce]]
- [[sort-merge-joins]]
- [[map-side-joins]]
- [[data-warehousing]]
- [[service-discovery]]
- [[stream-processing]]
- [[log-based-message-brokers]]
- [[event-sourcing]]
- [[client-side-sharding]]
- [[ambassador-pattern]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
- [[shard-key-selection]]
- [[sharded-cache]]
- [[scatter-gather-pattern]]
- [[tail-latency-amplification]]
