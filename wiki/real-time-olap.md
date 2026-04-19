# Real-Time OLAP

**Summary**: A class of analytical database purpose-built for streaming ingestion and subsecond queries on rapidly moving data — the backend of Reis and Housley's predicted [[live-data-stack]]. Named examples in Chapter 11: Apache Druid, ClickHouse, Rockset, Firebolt. Distinct from both [[data-warehousing|cloud warehouses]] (batch-oriented, high latency) and [[data-lake|data lakes]] (not optimised for fast point queries).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## What it is

A **real-time analytical database** combines two capabilities most analytical systems sacrifice one of (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Fast streaming ingestion** — data lands and is queryable within seconds of being produced.
- **Subsecond analytical queries** — OLAP-shaped scans, aggregations, and joins with low latency.

In a [[live-data-stack]] setup, a real-time OLAP database is the storage layer that sits behind streaming pipelines and in front of live applications and dashboards. It can enrich incoming data against historical datasets without the 15-minute lag of a traditional warehouse.

## Why the warehouse and lake don't fit

Reis and Housley are blunt: "While the data warehouse and data lake are great for housing large amounts of data and performing ad hoc queries, they are not so well optimized for low-latency data ingestion or queries on rapidly moving data" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

The warehouse optimises for batch loads and large scans; its ingestion model generally assumes bounded commits, not continuous appends at high rate. The lake optimises for cheap storage and ad-hoc processing; point queries and concurrency are not its strength.

Real-time OLAP databases are **purpose-built for streaming** — a third category.

## Named examples

Chapter 11 cites four databases as "leading the way in powering the backend of the next generation of data applications" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Apache Druid** — distributed, column-oriented, time-series-aware analytical store. Popular for operational analytics.
- **ClickHouse** — Yandex-origin open-source columnar DB; extreme ingestion rates and very fast aggregations.
- **Rockset** — converged indexing across analytical and search workloads; SQL over semistructured data.
- **Firebolt** — cloud-warehouse-shaped analytical DB optimised for subsecond queries.

The list is illustrative, not exhaustive — the space is young and evolving rapidly.

## Where it fits in the lifecycle

Real-time OLAP sits at the intersection of three [[data-engineering-lifecycle|lifecycle stages]]:

- **[[data-storage-stage|Storage]]** — a storage abstraction purpose-built for streaming.
- **[[data-ingestion|Ingestion]]** — ingests directly from streams (Kafka, Pulsar, Kinesis).
- **[[data-serving|Serving]]** — powers [[embedded-analytics|embedded analytics]], [[operational-analytics|operational analytics]], and application backends.

It's also related to [[storage-compute-separation]] (it tends to use tiered storage) and to [[streaming-storage]] (the upstream substrate it reads from).

## Connection to streaming queries and modeling

Real-time OLAP databases run [[streaming-queries|streaming queries]] — continuous queries over arriving data — and demand [[streaming-data-modeling|streaming-friendly modeling]]. Chapter 11 flags data modeling as "ripe for disruption" precisely because the traditional Kimball / Inmon / Vault paradigms assume bounded batch data (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Why it matters in Reis and Housley's prediction

Without real-time OLAP, the [[live-data-stack]] has nowhere to land its data. The chapter frames the emergence of managed real-time OLAP — alongside managed stream processors (Kinesis Data Analytics, Dataflow) — as a necessary condition for the democratisation of real-time architectures that elite tech companies already run in custom form (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Related pages

- [[live-data-stack]]
- [[future-of-data-engineering]]
- [[stream-processing]]
- [[streaming-queries]]
- [[streaming-data-modeling]]
- [[streaming-storage]]
- [[operational-analytics]]
- [[embedded-analytics]]
- [[data-warehousing]]
- [[data-lake]]
- [[column-oriented-storage]]
- [[storage-compute-separation]]
