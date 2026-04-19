# OLTP vs OLAP

**Summary**: OLTP (online transaction processing) and OLAP (online analytic processing) describe two fundamentally different database access patterns that favor different storage architectures.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The distinction

| Property | OLTP | OLAP |
|---|---|---|
| Primary users | End-user applications | Business analysts |
| Query volume | Very high (millions/day) | Low (few per day) |
| Data touched per query | Small (a few records) | Huge (millions–billions of rows) |
| Access pattern | Random reads/writes by key | Sequential scans across many rows |
| Data written | Latest event, user input | Bulk-loaded from OLTP systems (ETL) |
| Dataset size | Gigabytes to terabytes | Terabytes to petabytes |
| Bottleneck | Disk seek time | Disk bandwidth |
| Optimized by | [[indexes]] ([[b-trees]], [[sstables-and-lsm-trees|LSM-trees]]) | [[column-oriented-storage]] |

## OLTP

Online transaction processing is the original use case for databases: recording commercial transactions (sales, orders, payments) and later generalized to any user-facing application with low-latency reads and writes.

An OLTP query typically looks up a small number of records by key using an index. Records are inserted or updated based on user input. Disk seek time is the bottleneck.

OLTP databases need to be highly available and low-latency because they're often critical to business operations. Business analysts querying an OLTP database directly with large analytic queries can harm the performance of concurrent transactions.

## OLAP

Online analytic processing involves queries that scan large fractions of a dataset, read only a few columns per row, and compute aggregate statistics (COUNT, SUM, AVG, MIN, MAX) rather than returning individual records.

Examples:
- What was total revenue per store in January?
- How many more bananas than usual sold during the last promotion?
- Which product is most often bought with brand X?

OLAP queries are typically written by business analysts and feed into business intelligence reports. They can be expensive — scanning billions of rows — and can run for minutes. Disk bandwidth (not seek time) is the bottleneck.

## Why separate systems?

In the late 1980s and early 1990s, companies began running analytics on a separate database — a [[data-warehousing|data warehouse]] — rather than directly on OLTP systems. Reasons:
- OLTP database administrators don't want ad hoc analytic queries harming transaction performance.
- Analytic workloads benefit from a completely different storage architecture ([[column-oriented-storage]]).
- A warehouse can be optimized for read-heavy bulk scans without the write-optimization constraints of OLTP.

On the surface, both OLTP databases and data warehouses often offer a SQL interface. Internally, their storage engines are completely different.

## FoDE framing: the source-system lens

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* treats OLTP and OLAP explicitly as **source-system categories**, not just storage-engine categories, adding a data-engineer-specific layer on top of DDIA's storage-internals framing (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **OLTP as the application-backend source.** An OLTP database is typically the place where application state lives. "OLTP databases work well as application backends when thousands or even millions of users might be interacting with the application simultaneously" — and the data engineer's job is to extract from them without degrading that primary workload. See [[application-database-as-source]].
- **OLAP as an upstream too.** The chapter points out that OLAPs are typically *storage and query* systems, not generation systems — yet engineers regularly read from them as sources. A data warehouse may serve data used to train an ML model, or OLAP may feed a [[reverse-etl]] workflow that pushes derived data back to CRM or operational applications. OLAP-as-source is most visible in reverse-ETL and ML training pipelines (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).
- **"Online" is literal.** The *online* in OLAP means the system "constantly listens for incoming queries," making it suitable for interactive analytics — distinct from batch-only offline analytics systems (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).
- **OLAP is not just cubes.** Reis and Housley use OLAP broadly to mean "any database system that supports high-scale interactive analytics queries," not specifically systems supporting multidimensional OLAP cubes.
- **Running analytics directly on OLTP works — briefly.** Small companies routinely do it. It stops working due to OLTP's structural limits or contention with the transactional workload. The engineer's first major architectural decision is often *when* to stand up a separate analytics system (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

### Data applications: the hybrid

Reis and Housley coin **data application** for the emerging class of SaaS products that "hybridize transactional and analytics workloads" — in-app analytics running on live operational data. These erode the clean OLTP/OLAP split and create new challenges: quick updates *combined with* analytics, no clean boundary, and analytics performance expectations baked into the primary product (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). See [[analytics]] for the embedded-analytics framing.

## Related pages

- [[storage-engines]]
- [[data-warehousing]]
- [[column-oriented-storage]]
- [[indexes]]
- [[application-database-as-source]]
- [[analytics]]
- [[reverse-etl]]
- [[source-systems]]
