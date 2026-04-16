# Lost Updates

**Summary**: A race condition where two [[transactions]] concurrently perform a read-modify-write cycle on the same data, and one transaction's modification is silently lost because the second write does not incorporate the first transaction's change.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## The problem

The lost update problem occurs when an application reads a value, modifies it, and writes it back (a read-modify-write cycle). If two transactions do this concurrently, the later write clobbers the earlier write without incorporating its changes. (source: chapter-07-transactions.md)

Common scenarios where this arises:

- Incrementing a counter or updating an account balance
- Adding an element to a list within a JSON document
- Two users editing a wiki page simultaneously, each sending the full page contents to the server (source: chapter-07-transactions.md)

## Prevention strategies

### Atomic write operations

Many databases provide built-in atomic update operations that avoid the need for a read-modify-write cycle in application code:

```sql
UPDATE counters SET value = value + 1 WHERE key = 'foo';
```

These are usually implemented by taking an exclusive lock on the object when it is read (cursor stability) or by forcing all atomic operations onto a single thread. Atomic operations are the best choice when the update can be expressed this way. (source: chapter-07-transactions.md)

ORM frameworks can make it easy to accidentally write unsafe read-modify-write cycles instead of using database-provided atomic operations. (source: chapter-07-transactions.md)

### Explicit locking (SELECT FOR UPDATE)

When atomic operations are insufficient (e.g., the update requires application logic like game rule validation), the application can explicitly lock the relevant rows:

```sql
BEGIN TRANSACTION;
SELECT * FROM figures WHERE name = 'robot' AND game_id = 222 FOR UPDATE;
-- Check move validity, then update
UPDATE figures SET position = 'c4' WHERE id = 1234;
COMMIT;
```

The `FOR UPDATE` clause locks all rows returned by the query. This forces concurrent read-modify-write cycles to execute sequentially. The risk is forgetting to add the lock somewhere in the code. (source: chapter-07-transactions.md)

### Automatic detection

Some [[snapshot-isolation]] implementations automatically detect lost updates and abort the offending transaction, forcing a retry. This is supported by PostgreSQL's repeatable read, Oracle's serializable, and SQL Server's snapshot isolation. MySQL/InnoDB's repeatable read does **not** detect lost updates. (source: chapter-07-transactions.md)

Automatic detection is less error-prone than manual locking since it does not require special application code.

### Compare-and-set

In databases without full transaction support, a compare-and-set operation allows a write only if the value has not changed since the last read:

```sql
UPDATE wiki_pages SET content = 'new content'
WHERE id = 1234 AND content = 'old content';
```

This is not always safe -- if the WHERE clause reads from an old snapshot, the condition may evaluate to true even though a concurrent write is in progress. Check whether your database's compare-and-set is safe before relying on it. (source: chapter-07-transactions.md)

### Conflict resolution in replicated databases

In [[multi-leader-replication]] or [[leaderless-replication]], locks and compare-and-set do not apply because there is no single up-to-date copy of the data. Instead, concurrent writes create conflicting versions (siblings) that must be resolved after the fact. (source: chapter-07-transactions.md)

Commutative atomic operations (e.g., incrementing a counter, adding to a set) work well in replicated contexts because they produce the same result regardless of application order. The last-write-wins (LWW) strategy, by contrast, is prone to lost updates. (source: chapter-07-transactions.md)

## Related pages

- [[isolation-levels]]
- [[snapshot-isolation]]
- [[read-committed]]
- [[write-skew]]
- [[write-conflicts]]
- [[transactions]]
- [[multi-leader-replication]]
- [[leaderless-replication]]
