# Serializability

**Summary**: The strongest [[isolation-levels|isolation level]] for [[transactions]], guaranteeing that the result of concurrent execution is the same as if transactions had run one at a time in some serial order -- preventing all possible race conditions including [[write-skew]] and [[phantoms]].

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Why serializability matters

Weaker [[isolation-levels]] protect against some race conditions but not all. [[write-skew|Write skew]] and [[phantoms]] can only be prevented by serializable isolation. The fundamental promise: if transactions behave correctly when run individually, they continue to be correct when run concurrently. The database prevents all possible race conditions. (source: chapter-07-transactions.md)

Despite this, serializable isolation is not universally used because it historically carried significant performance penalties. Some databases (e.g., Oracle 11g) do not even implement it -- Oracle's "serializable" level is actually [[snapshot-isolation]]. (source: chapter-07-transactions.md)

## Three implementation approaches

Most databases that provide serializability use one of three techniques (source: chapter-07-transactions.md):

### 1. Actual serial execution

Execute transactions one at a time on a single thread, completely eliminating concurrency. See [[actual-serial-execution]].

- Became feasible around 2007 when RAM prices dropped enough to keep active datasets in memory
- Used by VoltDB/H-Store, Redis, and Datomic
- Requires transactions to be fast (stored procedures), and write throughput must fit on a single CPU core (or data must be partitionable)

### 2. Two-phase locking (2PL)

Readers and writers block each other via shared and exclusive locks. See [[two-phase-locking]].

- The standard approach for serializability for roughly 30 years
- Uses predicate locks or index-range locks to prevent [[phantoms]]
- Significant performance overhead: reduced concurrency, unstable latencies, frequent deadlocks

### 3. Serializable snapshot isolation (SSI)

An optimistic concurrency control technique built on [[snapshot-isolation]]. See [[serializable-snapshot-isolation]].

- First described in 2008
- Transactions proceed without blocking; conflicts are detected at commit time
- Used by PostgreSQL (since 9.1) and FoundationDB
- Combines good performance with full serializability

## Pessimistic vs optimistic

Two-phase locking and serial execution are **pessimistic** -- they prevent conflicts by blocking or eliminating concurrency. SSI is **optimistic** -- it allows concurrency and checks for conflicts at commit time, aborting transactions that would violate serializability. (source: chapter-07-transactions.md)

Optimistic approaches perform better when contention is low and there is spare capacity. They perform worse under high contention because many transactions abort and retry. (source: chapter-07-transactions.md)

## Serializability vs linearizability

These two terms are easily confused but refer to different guarantees (source: designing-data-intensive-applications, chapter 9):

- **Serializability** is an isolation property of [[transactions]]. It applies to multi-object operations and guarantees they behave as if executed serially. The serial order can differ from the actual execution order.
- **[[Linearizability]]** is a recency guarantee on individual objects (registers). It does not group operations into transactions and does not prevent [[write-skew]] on its own.

A database providing both is said to have **strict serializability** (strong one-copy serializability). Implementations based on [[two-phase-locking]] or [[actual-serial-execution]] are typically linearizable. [[Serializable-snapshot-isolation]] is NOT linearizable, because it reads from a consistent snapshot that excludes recent writes. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[actual-serial-execution]]
- [[two-phase-locking]]
- [[serializable-snapshot-isolation]]
- [[isolation-levels]]
- [[write-skew]]
- [[phantoms]]
- [[snapshot-isolation]]
- [[transactions]]
- [[linearizability]]
