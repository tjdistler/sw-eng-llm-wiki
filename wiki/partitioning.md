# Partitioning

**Summary**: Partitioning (also called sharding) splits a large dataset across multiple nodes so that data and query load can scale beyond what a single machine can handle.

**Sources**: raw/designing-data-intensive-applications/chapter-06-partitioning.md, raw/designing-data-intensive-applications/chapter-11-stream-processing.md

**Last updated**: 2026-04-15

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

Most NoSQL distributed datastores support only simple queries that read or write a single key (plus scatter/gather for document-partitioned secondary indexes). However, massively parallel processing (MPP) relational database products, often used for [[data-warehousing|analytics]], support much more sophisticated queries. The MPP query optimizer breaks complex queries -- involving joins, filtering, grouping, and aggregation -- into execution stages and partitions, many of which run in parallel on different nodes. Queries that scan large parts of the dataset particularly benefit from parallel execution (source: chapter-06-partitioning.md).

## Partitioning in batch processing

Partitioning is central to [[batch-processing]] systems. In [[mapreduce]], the input is partitioned by file blocks (each block is a separate map task), and mapper output is repartitioned by a hash of the key to assign key-value pairs to reducers. The shuffle process — partitioning, sorting, and copying data from mappers to reducers — brings all records with the same key to the same place (source: designing-data-intensive-applications, chapter 10).

[[map-side-joins]] require specific partitioning properties of input datasets: matching partition count, same key, same hash function. Metadata about how datasets are partitioned (maintained in HCatalog / Hive metastore) is essential for optimizing join strategies (source: designing-data-intensive-applications, chapter 10).

[[dataflow-engines]] (Spark, Tez, Flink) take a similar approach to partitioning but avoid unnecessary sorting and can repartition without it when only the partitioning matters (e.g., for partitioned hash joins) (source: designing-data-intensive-applications, chapter 10).

## Partitioning in stream processing

[[log-based-message-brokers]] use partitioning to scale beyond a single disk's throughput. A topic is divided into partitions, each hosted on a different machine. Within each partition, messages are assigned monotonically increasing offsets and are totally ordered; there is no ordering guarantee across partitions (source: chapter-11-stream-processing.md).

Load balancing in log-based brokers works at the partition level rather than per-message: entire partitions are assigned to consumer nodes. This means the maximum parallelism is bounded by the number of partitions (unlike AMQP/JMS-style [[message-brokers]] where individual messages can be distributed). See [[log-based-message-brokers]] (source: chapter-11-stream-processing.md).

Stream processing state can also be partitioned to match the event log: if events for a customer in partition 3 only require updating partition 3 of the application state, a single-threaded log consumer needs no concurrency control for writes. See [[event-sourcing]] (source: chapter-11-stream-processing.md).

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
