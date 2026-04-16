# OLTP vs OLAP

**Summary**: OLTP (online transaction processing) and OLAP (online analytic processing) describe two fundamentally different database access patterns that favor different storage architectures.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[storage-engines]]
- [[data-warehousing]]
- [[column-oriented-storage]]
- [[indexes]]
