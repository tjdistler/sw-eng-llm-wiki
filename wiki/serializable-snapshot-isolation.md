# Serializable Snapshot Isolation (SSI)

**Summary**: An optimistic concurrency control algorithm that provides full [[serializability]] with only a small performance penalty compared to [[snapshot-isolation]], by allowing [[transactions]] to proceed without blocking and detecting serialization conflicts at commit time.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Overview

SSI was first described in 2008 (Michael Cahill's PhD thesis). It is used by PostgreSQL (since version 9.1) for its serializable isolation level and by FoundationDB for distributed transactions. (source: chapter-07-transactions.md)

SSI is built on top of [[snapshot-isolation]]: all reads within a transaction are made from a consistent snapshot (via [[mvcc]]). On top of this, SSI adds an algorithm for detecting serialization conflicts among writes and determining which transactions to abort. (source: chapter-07-transactions.md)

## Optimistic vs pessimistic

SSI is **optimistic**: transactions proceed without blocking, and conflicts are checked only when a transaction wants to commit. If the execution was not serializable, the transaction is aborted and must be retried. (source: chapter-07-transactions.md)

This contrasts with **pessimistic** approaches like [[two-phase-locking]] (which blocks on potential conflicts) and [[actual-serial-execution]] (which eliminates concurrency entirely). (source: chapter-07-transactions.md)

Optimistic concurrency control performs well when contention is low and there is spare capacity. It performs poorly under high contention because many transactions abort and retry, wasting work. Commutative atomic operations (e.g., incrementing a counter) can reduce contention by allowing concurrent increments without conflict. (source: chapter-07-transactions.md)

## How conflict detection works

SSI detects two types of situations where a transaction may have acted on an outdated premise (source: chapter-07-transactions.md):

### 1. Detecting reads of stale MVCC object versions

When a transaction reads from a consistent snapshot, it ignores writes made by other transactions that had not yet committed. If those ignored writes subsequently commit before the reading transaction commits, the read was stale -- the premise on which the transaction based its decisions may no longer be true. (source: chapter-07-transactions.md)

The database tracks which writes were ignored due to MVCC visibility rules. At commit time, it checks whether any of those writes have now committed. If so, the transaction must abort.

SSI waits until commit time rather than aborting immediately on a stale read because: the transaction might be read-only (no risk of [[write-skew]]), and the other transaction might still abort. Avoiding unnecessary aborts preserves snapshot isolation's support for long-running reads. (source: chapter-07-transactions.md)

### 2. Detecting writes that affect prior reads

When a transaction writes to the database, SSI checks indexes for other transactions that recently read the affected data. Rather than blocking (as [[two-phase-locking]] would), it uses the index entry as a "tripwire" -- it notifies those transactions that their read may be stale. (source: chapter-07-transactions.md)

In the doctors-on-call example: when transaction 42 writes (removing Alice from on-call), it notifies transaction 43 that its earlier read of on-call doctors may be outdated, and vice versa. Transaction 42 commits first (successfully, since 43 hasn't committed yet). When transaction 43 tries to commit, the conflicting write from 42 has already committed, so 43 must abort. (source: chapter-07-transactions.md)

## Performance characteristics

Compared to [[two-phase-locking]] (source: chapter-07-transactions.md):

- **No blocking**: writers don't block readers and vice versa, making query latency more predictable
- **Read-only queries** run on a consistent snapshot without any locks -- appealing for read-heavy workloads

Compared to [[actual-serial-execution]] (source: chapter-07-transactions.md):

- **Not limited to a single CPU core**: FoundationDB distributes conflict detection across multiple machines, scaling to high throughput
- **Cross-partition transactions** are possible while maintaining serializable isolation

Trade-offs:

- The abort rate significantly affects performance. Transactions that read and write over a long period are more likely to encounter conflicts and abort.
- Read-write transactions should be fairly short, though long-running read-only transactions are fine.
- Granularity of tracking (fine-grained vs coarse-grained) is a design trade-off: more precise tracking means fewer unnecessary aborts but higher bookkeeping overhead. PostgreSQL uses theoretical results to reduce unnecessary aborts. (source: chapter-07-transactions.md)

## Related pages

- [[serializability]]
- [[snapshot-isolation]]
- [[mvcc]]
- [[two-phase-locking]]
- [[actual-serial-execution]]
- [[write-skew]]
- [[phantoms]]
- [[isolation-levels]]
- [[transactions]]
