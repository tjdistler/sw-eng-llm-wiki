# Data Lake

**Summary**: An architectural pattern where raw data is dumped into a shared distributed file system or object store with little upfront modeling; consumers decide how to interpret it at read time. Historically built on HDFS; now overwhelmingly on cloud object storage (S3, GCS, ADLS). Originally sold as the warehouse replacement; in practice, **data lake 1.0** frequently degenerated into **data swamps** (see [[data-modeling]]). **Data lake 2.0 / the [[data-lakehouse]]** retrofits transactional guarantees, governance, and schema to address those failures.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`, `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-18

---

## The pattern

Data from operational systems is dumped in raw form into a shared store — historically HDFS, now cloud object storage. Analytics code reads the raw data and interprets it; the schema is applied at read time rather than write time. This is the **schema-on-read** approach; see [[schema-on-read-vs-write]] (source: raw/designing-data-intensive-applications/chapter-10-batch-processing.md).

Contrasts with the [[data-warehousing|data warehouse]] approach, where an ETL process carefully models and normalises data before loading.

Alternative names: enterprise data hub, enterprise data lake.

## The "sushi principle"

The framing that made data lakes appealing: **"raw data is better."** Keeping data raw preserves optionality — future consumers may find new questions to ask that the original data model would have foreclosed. See [[data-warehousing]] for the contrast with up-front modeling.

## What Chapter 2 adds — the archival problem

Chapter 2's specific contribution: "The advent of data lakes **encouraged organizations to ignore data archival and destruction**. Why discard data when you can simply add more storage ad infinitum?" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Two forces have pushed engineers to pay attention again:

1. **Cloud pay-as-you-go pricing.** When every byte hits the AWS bill monthly, CFOs notice. See [[data-lifecycle-management]] and [[data-temperature]].
2. **Privacy regulation.** GDPR and CCPA require engineers to actively destroy data in response to user requests. Destruction was **harder in classic data lakes** where write-once-read-many was the default — but new tools like **Hive ACID and Delta Lake** now support scalable deletion transactions (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Data vanity projects

Chapter 2's blunter framing, under the [[data-serving|serving]] stage: "Many companies pursued vanity projects in the big data era, gathering massive datasets in data lakes that were never consumed in any useful way." The cure: data projects must be intentional across the lifecycle, pointed at a business purpose (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 3: data lake 1.0 and its failures

Chapter 3 explicitly labels the first-generation pattern as **"data lake 1.0"** — starting with HDFS, then moving to cloud object storage for cheap virtually-limitless capacity (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). The promise was immense: any data of any size or type, queryable later with any engine (MapReduce, Spark, Ray, Presto, Hive).

The reality had **serious shortcomings**:

- **Data swamp dumping ground** — terms like "data swamp," "dark data," and **WORN (write once, read never)** emerged to describe once-promising projects that failed
- **Unmanageable sizes** with little schema management, cataloguing, or discovery
- **Write-only semantics** — a huge problem under GDPR, which requires targeted deletion of user records
- **Data manipulation pain** — joins, updates, and deletes were painful to express as MapReduce jobs; even basic DML usually meant writing entirely new tables
- **Cost inversion** — big data costs ballooned as managing Hadoop clusters forced companies to hire large teams at high salaries, contradicting the "cheap off-the-shelf hardware beats expensive MPP" pitch

Chapter 3 is careful to note that **lake 1.0 did work for the companies that had the resources to invest in it** — Netflix and Facebook used data lakes successfully. The problem was universalising a pattern that only paid off at that scale.

## Chapter 3: data lake 2.0 and convergence

Chapter 3 describes the response (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **[[data-lakehouse|Data lakehouse]]** (Databricks' term): ACID transactions, data management, and warehouse-like schema grafted onto object storage with pluggable query engines
- **Converged cloud data warehouses** (Snowflake, BigQuery): compute-storage separation, petabyte-scale queries, storage of unstructured text and rich JSON, integration with Spark/Beam
- **Converged data platforms**: AWS, Azure, Google Cloud, Snowflake, and Databricks as class leaders offering constellations of tools spanning relational through unstructured

Chapter 3's conclusion: the lake and the warehouse will still exist as different *architectures*, but in practice their capabilities converge so "few users will notice a boundary between them in their day-to-day work" (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## Ch 6 — the WORM exit and the convergence with object storage

Chapter 6 gives the cleanest retrospective on lake 1.0's design (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> Object stores are now the gold standard of storage for data lakes. In the early days of data lakes, write once, read many (WORM) was the operational standard, but this had more to do with the complexities of managing data versions and files than the limitations of HDFS and object stores.

WORM was a workaround for the *absence* of update tooling, not a fundamental constraint of the underlying storage. Once [[lakehouse-table-formats|Apache Hudi, Delta Lake, and Iceberg]] emerged to manage versioning, schema, and deletion at scale, and once GDPR/CCPA made deletion capabilities mandatory, the WORM era ended. "Update management for object storage is the central idea behind the data lakehouse concept" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

Chapter 6 also underscores what the data lake is uniquely *for* beyond structured analytics: **"Object storage is an ideal repository for unstructured data in any format"** — images, video, audio, raw text. ML pipelines lean on this heavily. A lake is the only practical home for this data at scale; warehouses can handle rich JSON but not arbitrary binary objects.

## Relationship to other patterns

- The **[[data-warehousing|data warehouse]]** is the schema-on-write counterpart.
- The **[[data-lakehouse|data lakehouse]]** is a convergent pattern that grafts warehouse-like schema, transactions, and governance onto a lake.
- **[[etl-vs-elt|ELT]]** is the ingestion pattern that goes with lakes and lakehouses — load raw, transform later.
- **[[modern-data-stack]]** is the surrounding ecosystem of plug-and-play tooling that typically sits on top of a converged lake/warehouse.

## Cross-book connections

- [[hadoop-vs-mpp-databases]] (DDIA) covers the Hadoop-vs-MPP-warehouse trade-off that birthed the data lake.
- [[column-oriented-storage]] is common in lake-table formats (Parquet, ORC).
- [[event-sinking]] (Bellemare) names sinking event streams into HDFS / cloud lakes as a bridge from streaming to batch analytics.

## Related pages

- [[data-storage-stage]]
- [[data-warehousing]]
- [[data-lakehouse]]
- [[lakehouse-table-formats]]
- [[object-storage]]
- [[modern-data-stack]]
- [[hadoop-vs-mpp-databases]]
- [[distributed-filesystems]]
- [[schema-on-read-vs-write]]
- [[etl-vs-elt]]
- [[data-lifecycle-management]]
- [[data-retention]]
- [[data-temperature]]
- [[data-architecture]]
- [[data-mesh]]
- [[storage-compute-separation]]
