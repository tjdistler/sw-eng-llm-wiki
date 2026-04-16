# Actual Serial Execution

**Summary**: An approach to [[serializability]] that eliminates concurrency entirely by executing [[transactions]] one at a time on a single thread -- made feasible around 2007 by in-memory datasets and the realization that OLTP transactions are typically short and fast.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## What changed

For 30 years, single-threaded execution was considered impractical for databases. Two developments around 2007 changed this (source: chapter-07-transactions.md):

1. **RAM became cheap enough** to keep the entire active dataset in memory. When transactions don't wait for disk I/O, they execute much faster.
2. **OLTP transactions are short**: database designers realized that OLTP transactions typically make only a small number of reads and writes (see [[oltp-vs-olap]]). Long-running analytic queries can run separately on a consistent snapshot using [[snapshot-isolation]].

## Implementations

Used by VoltDB/H-Store, Redis, and Datomic. A system designed for single-threaded execution can sometimes outperform concurrent systems by avoiding lock coordination overhead. (source: chapter-07-transactions.md)

## Stored procedures

Single-threaded execution cannot afford network round-trips between the application and database during a transaction. Interactive, multi-statement transactions would cause the single thread to idle waiting for the application to send the next query. (source: chapter-07-transactions.md)

The solution: the application submits the entire transaction as a **stored procedure** -- all logic is sent to the database ahead of time and executed without network waits. Provided all required data is in memory, the stored procedure runs very fast. (source: chapter-07-transactions.md)

### Stored procedure trade-offs

Traditional stored procedures have a bad reputation due to (source: chapter-07-transactions.md):

- Vendor-specific languages (PL/SQL, T-SQL, PL/pgSQL) that are archaic and lack library ecosystems
- Difficulty managing code in a database (debugging, version control, deployment, monitoring)
- Performance sensitivity -- a poorly written stored procedure affects all users sharing the database

Modern implementations address this by using general-purpose languages: VoltDB uses Java/Groovy, Datomic uses Java/Clojure, Redis uses Lua. (source: chapter-07-transactions.md)

## Partitioning for throughput

Serial execution limits throughput to a single CPU core. To scale, data can be partitioned (see [[partitioning]]) so each partition has its own transaction-processing thread. If transactions only touch one partition, throughput scales linearly with CPU cores. (source: chapter-07-transactions.md)

Cross-partition transactions require coordination across all involved partitions (executed in lock-step to ensure serializability). VoltDB reports roughly 1,000 cross-partition writes per second -- orders of magnitude below single-partition throughput. Whether single-partition transactions are feasible depends on data structure: simple key-value data partitions easily, but data with multiple secondary indexes often requires cross-partition coordination. (source: chapter-07-transactions.md)

## Constraints

Serial execution is viable only when (source: chapter-07-transactions.md):

- Every transaction is **small and fast** -- one slow transaction stalls all processing
- The **active dataset fits in memory** (rarely accessed data on disk would cause blocking I/O)
- **Write throughput** fits on a single CPU core, or transactions can be partitioned without cross-partition coordination
- Cross-partition transactions are used sparingly

## Related pages

- [[serializability]]
- [[transactions]]
- [[partitioning]]
- [[snapshot-isolation]]
- [[oltp-vs-olap]]
- [[storage-engines]]
