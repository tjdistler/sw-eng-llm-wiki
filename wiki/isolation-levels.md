# Isolation Levels

**Summary**: A spectrum of guarantees that databases provide to protect concurrent [[transactions]] from interfering with each other, ranging from weak levels like [[read-committed]] to the strongest level, [[serializability]] -- with weaker levels trading safety for performance.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Why weak isolation exists

Serializable isolation guarantees that concurrent transactions behave as if they ran serially. However, it carries a performance cost, so most databases default to weaker levels that protect against some but not all race conditions. (source: chapter-07-transactions.md)

Concurrency bugs caused by weak isolation are not just theoretical -- they have caused financial losses, triggered auditor investigations, and corrupted customer data. The advice "use an ACID database" is insufficient because many ACID databases use weak isolation by default. (source: chapter-07-transactions.md)

## Hierarchy of isolation levels

From weakest to strongest:

| Level | Prevents | Does not prevent |
|---|---|---|
| **Read uncommitted** | [[dirty-reads-and-dirty-writes\|Dirty writes]] | Dirty reads, everything else |
| **[[read-committed]]** | Dirty reads, dirty writes | [[read-skew]], [[lost-updates]], [[write-skew]], [[phantoms]] |
| **[[snapshot-isolation]]** | Dirty reads, dirty writes, read skew | Lost updates (in some implementations), write skew, phantoms in write contexts |
| **[[serializability]]** | All race conditions | Nothing -- this is the strongest level |

## Naming confusion

The SQL standard's definition of isolation levels is flawed -- ambiguous, imprecise, and not implementation-independent. Key confusions (source: chapter-07-transactions.md):

- **Snapshot isolation** is not in the SQL standard (it was invented after the standard was written). PostgreSQL and MySQL call it "repeatable read." Oracle calls it "serializable." IBM DB2 uses "repeatable read" to mean actual serializability.
- Even databases that claim the same isolation level name may provide very different guarantees in practice.

## Race conditions at each level

Each isolation level protects against specific race conditions:

- **[[dirty-reads-and-dirty-writes]]** -- prevented by read committed and above
- **[[read-skew]]** (nonrepeatable reads) -- prevented by snapshot isolation and above
- **[[lost-updates]]** -- some snapshot isolation implementations detect and prevent automatically; others require explicit locking
- **[[write-skew]]** -- only prevented by serializable isolation
- **[[phantoms]]** -- snapshot isolation prevents phantom reads in read-only queries, but phantoms causing write skew require serializable isolation or special techniques like index-range locks

## Choosing an isolation level

There are no good tools to detect race conditions from application code. Testing for concurrency issues is hard because they are nondeterministic. The safest approach is to use [[serializability]], but if performance requirements preclude it, developers must understand exactly which race conditions their chosen level allows. (source: chapter-07-transactions.md)

## Related pages

- [[transactions]]
- [[acid]]
- [[read-committed]]
- [[snapshot-isolation]]
- [[serializability]]
- [[dirty-reads-and-dirty-writes]]
- [[read-skew]]
- [[lost-updates]]
- [[write-skew]]
- [[phantoms]]
