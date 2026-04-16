# Phantoms

**Summary**: A concurrency phenomenon where a write in one [[transactions|transaction]] changes the result of a search query in another transaction -- particularly dangerous when combined with [[write-skew]], because there are no existing rows to lock against.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## The problem

A phantom occurs when a write in one transaction changes the set of rows that match another transaction's search condition. [[snapshot-isolation|Snapshot isolation]] prevents phantoms in read-only queries (the reader sees a consistent snapshot), but in read-write transactions, phantoms can cause [[write-skew]]. (source: chapter-07-transactions.md)

## The pattern

Phantom-related write skew follows a consistent pattern (source: chapter-07-transactions.md):

1. A `SELECT` query checks whether some requirement is satisfied (e.g., no conflicting bookings exist, a username is not taken, sufficient balance remains).
2. The application decides to proceed based on the query result.
3. The application writes (`INSERT`, `UPDATE`, or `DELETE`), and the write changes the precondition that was checked in step 1.

The problem: in step 1, the transaction checks for the **absence** of matching rows. If two transactions run this pattern concurrently, both may find no conflicts and both proceed to write, violating the constraint.

Because there are no existing rows matching the condition, `SELECT FOR UPDATE` has nothing to lock.

## Solutions

### Materializing conflicts

Create a table of lock objects representing all possible conditions. For example, for a meeting room booking system, pre-populate a table with rows for every room-timeslot combination. A transaction locks the relevant rows (`SELECT FOR UPDATE`) before checking and inserting. This turns the phantom into a concrete lock conflict on existing rows. (source: chapter-07-transactions.md)

Drawbacks: hard to figure out how to materialize conflicts correctly, error-prone, and it leaks concurrency control concerns into the application data model. This should be a last resort. (source: chapter-07-transactions.md)

### Predicate locks

A predicate lock belongs to all objects matching a search condition (including objects that do not yet exist). If transaction A holds a predicate lock on "bookings for room 123 from noon to 1pm," transaction B cannot insert a booking matching those conditions until A completes. Predicate locks prevent phantoms completely, but they are expensive to check -- if many locks are active, matching them against each other becomes slow. (source: chapter-07-transactions.md)

### Index-range locks (next-key locking)

A practical approximation of predicate locks used by most databases implementing [[two-phase-locking]]. Instead of locking the exact predicate, the lock is attached to an index entry that covers a broader range. For example, locking all bookings for room 123 (any time), or all bookings in a time range (any room). (source: chapter-07-transactions.md)

This is less precise than predicate locks (it may lock more than strictly necessary) but has much lower overhead. If no suitable index exists, the database can fall back to a shared lock on the entire table. (source: chapter-07-transactions.md)

### Serializable snapshot isolation

[[serializable-snapshot-isolation|SSI]] uses a similar technique to index-range locks but as "tripwires" rather than blocking locks. When a transaction writes to an indexed range, it notifies other transactions that read from that range that their data may be stale. Conflicts are checked at commit time. (source: chapter-07-transactions.md)

## Related pages

- [[write-skew]]
- [[two-phase-locking]]
- [[serializable-snapshot-isolation]]
- [[serializability]]
- [[isolation-levels]]
- [[transactions]]
