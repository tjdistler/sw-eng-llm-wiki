# Two-Phase Locking (2PL)

**Summary**: A pessimistic concurrency control algorithm for [[serializability]] where [[transactions]] acquire shared or exclusive locks on objects, with the critical property that writers block readers and readers block writers -- the standard approach to serializable isolation for roughly 30 years.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## 2PL is not 2PC

Two-phase locking (2PL) is unrelated to two-phase commit (2PC). They are completely different algorithms despite the similar names. (source: chapter-07-transactions.md)

## Core principle

In 2PL, writers block readers and readers block writers. This is the key difference from [[snapshot-isolation]], which has the mantra "readers never block writers, and writers never block readers." (source: chapter-07-transactions.md)

Specifically:

- If transaction A has **read** an object and transaction B wants to **write** it, B must wait until A commits or aborts.
- If transaction A has **written** an object and transaction B wants to **read** it, B must wait until A commits or aborts. Reading an old version (as in snapshot isolation) is not allowed under 2PL. (source: chapter-07-transactions.md)

## Lock modes

Each object in the database has a lock with two modes (source: chapter-07-transactions.md):

- **Shared mode**: Required for reading. Multiple transactions can hold shared locks simultaneously, but they must wait if another transaction holds an exclusive lock.
- **Exclusive mode**: Required for writing. No other transaction may hold any lock (shared or exclusive) on the object.

A transaction that first reads and then writes an object upgrades its shared lock to an exclusive lock. The name "two-phase" comes from the two phases of lock usage: the **growing phase** (locks are acquired during execution) and the **shrinking phase** (all locks are released at transaction end -- commit or abort). (source: chapter-07-transactions.md)

## Implementations

Used by the serializable isolation level in MySQL (InnoDB) and SQL Server, and the repeatable read isolation level in IBM DB2. (source: chapter-07-transactions.md)

## Deadlocks

Because many locks are held simultaneously, deadlocks occur easily: transaction A waits for B's lock while B waits for A's lock. The database detects deadlocks automatically and aborts one transaction so the others can proceed. The aborted transaction must be retried by the application. (source: chapter-07-transactions.md)

Deadlocks occur more frequently under 2PL than under [[read-committed]] with locks, and frequent deadlocks waste significant effort due to retries. (source: chapter-07-transactions.md)

## Performance

The major downside of 2PL (source: chapter-07-transactions.md):

- **Reduced concurrency**: Any potential race condition causes blocking, significantly hurting throughput.
- **Unstable latencies**: A single slow transaction or one that acquires many locks can cause the rest of the system to grind to a halt. Latencies at high percentiles can be very poor.
- **Deadlock overhead**: Aborted-and-retried transactions waste work.

This is why 2PL is not universally adopted despite providing true serializability.

## Preventing phantoms

### Predicate locks

A predicate lock covers all objects matching a search condition, including objects that do not yet exist. This prevents [[phantoms]] completely. However, checking many predicate locks against each other is expensive. (source: chapter-07-transactions.md)

### Index-range locks (next-key locking)

A practical approximation of predicate locks. The lock is attached to an index entry covering a broader range than the exact predicate. For example, instead of locking "bookings for room 123 between noon and 1pm," the database might lock all bookings for room 123 (any time) or all bookings in the noon-to-1pm range (any room). (source: chapter-07-transactions.md)

Less precise than predicate locks but much faster. If no suitable index exists, the database falls back to a shared lock on the entire table (safe but slow). (source: chapter-07-transactions.md)

## Related pages

- [[serializability]]
- [[phantoms]]
- [[snapshot-isolation]]
- [[serializable-snapshot-isolation]]
- [[isolation-levels]]
- [[transactions]]
