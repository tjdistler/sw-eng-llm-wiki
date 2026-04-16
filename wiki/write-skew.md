# Write Skew

**Summary**: A concurrency anomaly where two [[transactions]] read the same data, make decisions based on what they saw, and then write to different objects -- violating an invariant that neither transaction alone would have broken -- preventable only by [[serializability|serializable isolation]].

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## The problem

Write skew occurs when two transactions read the same set of objects, each makes a decision based on what it read, and each writes to a different object. Because the transactions update different rows, neither dirty write detection nor lost update detection catches the conflict. The invariant that both transactions assumed was true is violated after both commit. (source: chapter-07-transactions.md)

Write skew is a generalization of the [[lost-updates]] problem. Lost updates are the special case where both transactions update the **same** object; write skew is the general case where they update **different** objects after reading the same data. (source: chapter-07-transactions.md)

### Classic example: doctors on call

A hospital requires at least one doctor on call per shift. Alice and Bob are both on call and both request leave simultaneously. Each transaction checks that two doctors are on call (true), then removes itself. Both commit successfully, leaving zero doctors on call. Under [[snapshot-isolation]], both transactions see the same snapshot where two doctors are on call. (source: chapter-07-transactions.md)

## More examples

- **Meeting room double-booking**: Two transactions check that a room is available for a time slot, find no conflicts, and both insert a booking.
- **Username claiming**: Two users try to register the same username concurrently; both check and find it available, both insert.
- **Multiplayer game**: Two players move different pieces to the same position; both check the position is empty, both write.
- **Double-spending**: Two spending transactions both check sufficient balance, both deduct, and total spending exceeds the balance. (source: chapter-07-transactions.md)

## Why weaker isolation levels fail

- **Atomic single-object operations** do not help because multiple objects are involved.
- **Automatic lost update detection** in [[snapshot-isolation]] does not catch write skew (confirmed for PostgreSQL, MySQL/InnoDB, Oracle, SQL Server).
- **Database constraints** (unique, foreign key) can help in some cases (e.g., username uniqueness) but most databases cannot express multi-object invariants. (source: chapter-07-transactions.md)

## Prevention strategies

### Serializable isolation

The only complete solution. See [[serializability]], [[two-phase-locking]], [[actual-serial-execution]], and [[serializable-snapshot-isolation]]. (source: chapter-07-transactions.md)

### Explicit locking (workaround)

When serializable isolation is unavailable, you can use `SELECT FOR UPDATE` to lock the rows the transaction depends on:

```sql
BEGIN TRANSACTION;
SELECT * FROM doctors WHERE on_call = true AND shift_id = 1234 FOR UPDATE;
UPDATE doctors SET on_call = false WHERE name = 'Alice' AND shift_id = 1234;
COMMIT;
```

This forces concurrent transactions to wait, effectively serializing access to those rows. (source: chapter-07-transactions.md)

### Materializing conflicts

When the problem involves [[phantoms]] (no existing row to lock), you can create a table of lock objects. For example, pre-populate a table of room-timeslot combinations and lock relevant rows with `SELECT FOR UPDATE` before inserting a booking. This turns a phantom into a concrete lock conflict. (source: chapter-07-transactions.md)

Materializing conflicts is a last resort -- it is error-prone and leaks concurrency control into the application data model. Serializable isolation is preferable. (source: chapter-07-transactions.md)

## Related pages

- [[phantoms]]
- [[lost-updates]]
- [[snapshot-isolation]]
- [[serializability]]
- [[isolation-levels]]
- [[transactions]]
