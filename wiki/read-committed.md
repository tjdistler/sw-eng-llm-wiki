# Read Committed

**Summary**: The most basic useful [[isolation-levels|isolation level]] for [[transactions]], providing two guarantees: no [[dirty-reads-and-dirty-writes|dirty reads]] (you only see committed data) and no dirty writes (you only overwrite committed data).

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Guarantees

Read committed provides two guarantees (source: chapter-07-transactions.md):

1. **No dirty reads**: When reading from the database, you only see data that has been committed. A transaction's writes become visible to others only when that transaction commits (and then all writes become visible at once).
2. **No dirty writes**: When writing to the database, you only overwrite data that has been committed. The second write waits until the first write's transaction has committed or aborted.

## Why prevent dirty reads

- A transaction updating multiple objects could be seen in a partially updated state, causing confusion or incorrect decisions by other transactions.
- If a transaction aborts, its writes are rolled back. Dirty reads would expose data that was never actually committed. (source: chapter-07-transactions.md)

## Why prevent dirty writes

Dirty writes can cause different transactions' updates to get mixed up across objects. The classic example: two people simultaneously buying the same car. Without dirty write prevention, one buyer could win the listing update while the other wins the invoice update, creating an inconsistent outcome. (source: chapter-07-transactions.md)

However, read committed does **not** prevent the race condition where two transactions do concurrent read-modify-write cycles on the same object (the [[lost-updates]] problem). (source: chapter-07-transactions.md)

## Implementation

Read committed is the default isolation level in Oracle 11g, PostgreSQL, SQL Server 2012, MemSQL, and many other databases. (source: chapter-07-transactions.md)

**Preventing dirty writes**: Databases use row-level locks. A transaction must acquire a lock on an object before modifying it, and holds the lock until commit or abort. Only one transaction can hold the write lock at a time. (source: chapter-07-transactions.md)

**Preventing dirty reads**: Rather than using read locks (which would cause long-running writes to block all reads), most databases remember both the old committed value and the new uncommitted value for each written object. Other transactions reading that object are given the old value until the writing transaction commits. (source: chapter-07-transactions.md)

## Limitations

Read committed does not prevent:

- **[[read-skew]]** (nonrepeatable reads) -- reading different parts of the database at different points in time
- **[[lost-updates]]** -- concurrent read-modify-write cycles
- **[[write-skew]]** -- decisions based on stale premises across multiple objects
- **[[phantoms]]** -- writes affecting another transaction's search query results

For protection against read skew, [[snapshot-isolation]] is needed.

## Related pages

- [[isolation-levels]]
- [[transactions]]
- [[dirty-reads-and-dirty-writes]]
- [[snapshot-isolation]]
- [[lost-updates]]
