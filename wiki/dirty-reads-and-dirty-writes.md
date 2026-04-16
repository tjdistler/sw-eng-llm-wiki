# Dirty Reads and Dirty Writes

**Summary**: Two fundamental race conditions in concurrent [[transactions]] -- a dirty read occurs when a transaction sees another transaction's uncommitted writes, and a dirty write occurs when a transaction overwrites another's uncommitted value -- both prevented by [[read-committed]] isolation and above.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Dirty reads

A dirty read happens when a transaction reads data that another transaction has written but not yet committed. (source: chapter-07-transactions.md)

Why this is a problem:

- **Partial updates visible**: If a transaction updates multiple objects, a dirty read can expose a state where only some updates have been applied. For example, a new email arrives but the unread counter has not yet been incremented.
- **Reading rolled-back data**: If a transaction aborts, its writes are rolled back. A dirty read could have exposed data that was never actually committed to the database. (source: chapter-07-transactions.md)

### Prevention

Most databases prevent dirty reads by remembering both the old committed value and the new uncommitted value for each object being written. Other transactions reading that object are given the old value until the writing transaction commits. This avoids the need for read locks, which would cause long-running writes to block all readers. (source: chapter-07-transactions.md)

## Dirty writes

A dirty write happens when a transaction overwrites a value that was written by another transaction that has not yet committed. (source: chapter-07-transactions.md)

Why this is a problem:

- **Mixed-up updates across objects**: Two concurrent transactions updating multiple related objects can end up with a mix of values from both transactions. The classic example is two people simultaneously buying the same car -- one wins the listing update, the other wins the invoice update. (source: chapter-07-transactions.md)

### Prevention

Databases prevent dirty writes using row-level locks. A transaction must acquire a lock on an object before modifying it, and holds the lock until commit or abort. If another transaction wants to write to the same object, it must wait. (source: chapter-07-transactions.md)

## What dirty write prevention does NOT cover

Read committed prevents dirty writes but does **not** prevent concurrent read-modify-write cycles from causing [[lost-updates]]. In the lost update scenario, the second write happens after the first transaction has committed, so it is not a dirty write -- but the result is still incorrect. (source: chapter-07-transactions.md)

## Related pages

- [[read-committed]]
- [[isolation-levels]]
- [[transactions]]
- [[lost-updates]]
