# Read Skew

**Summary**: A concurrency anomaly (also called nonrepeatable read) where a [[transactions|transaction]] sees different parts of the database at different points in time, caused by another transaction's writes becoming visible partway through a read -- prevented by [[snapshot-isolation]].

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## The problem

Read skew occurs when a transaction reads data at different points in time and sees an inconsistent state. This is allowed under [[read-committed]] isolation because each individual read returns a committed value -- the inconsistency arises only when the reads are considered together. (source: chapter-07-transactions.md)

### Example

Alice has $1,000 split across two bank accounts ($500 each). A transfer of $100 from one account to the other is in progress. If Alice reads both account balances during the transfer, she might see one account before the transfer ($500) and the other after the transfer ($400), making it appear she only has $900. (source: chapter-07-transactions.md)

For a simple web page reload, this temporary inconsistency is tolerable. But for certain operations it is not acceptable:

- **Backups**: A multi-hour backup could capture some data at an older point in time and other data at a newer point. Restoring from such a backup makes the inconsistency permanent.
- **Analytic queries and integrity checks**: Large scans that observe different parts of the database at different times can return nonsensical results. (source: chapter-07-transactions.md)

## Solution: snapshot isolation

[[snapshot-isolation|Snapshot isolation]] solves read skew by having each transaction read from a consistent snapshot taken at the start of the transaction. Even if data changes during the transaction, the transaction sees only the data that was committed when the snapshot was taken. This is implemented using [[mvcc|multi-version concurrency control]]. (source: chapter-07-transactions.md)

## Related pages

- [[snapshot-isolation]]
- [[read-committed]]
- [[isolation-levels]]
- [[mvcc]]
- [[transactions]]
