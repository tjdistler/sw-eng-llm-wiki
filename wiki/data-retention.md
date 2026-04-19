# Data Retention

**Summary**: Data retention answers the question "**how long should we keep this?**" — weighing business value against storage cost, privacy regulation, and the technical realities of tiered storage. Retention is the sibling concept of [[data-temperature|hot/warm/cold]] tiering: one decides *where* data lives, the other decides *whether it stays at all*.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The death of "keep everything"

Chapter 6 opens with a historical contrast (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> Back in the early days of "big data," there was a tendency to err on the side of accumulating every piece of data possible, regardless of its usefulness. The expectation was, "we might need this data in the future." This data hoarding inevitably became unwieldy and dirty, giving rise to data swamps, and regulatory crackdowns on data retention, among other consequences and nightmares.

Three forces ended the "keep everything" era:

1. **Cloud pay-as-you-go economics.** Storage is no longer a sunk hardware cost; every byte shows up on a monthly bill.
2. **Privacy regulation.** GDPR, CCPA, and others require deletion of user data on request and enforce upper-bound retention for certain categories.
3. **Data swamps.** Ungoverned accumulation destroys value: if nobody can find or trust the data, it is actively harmful.

## The four questions

Chapter 6 frames retention as balancing four inputs (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

### 1. Value

Is the data worth retaining?

- Can it be **re-created** by re-running a pipeline from an upstream source? If yes, retention can be shorter.
- Is there a **real downstream consumer** depending on it, or is it aspirational "maybe someone will need this"?
- How **impossible to regenerate** is it? Source-system events usually can't be replayed after the source system evicts them.

Value is subjective. Chapter 6 is explicit that it depends on the immediate use case and the broader organisational context. The engineer should know it before committing to a retention policy.

### 2. Time

Value **decays with age** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md): newer data is typically more valuable and more frequently queried. This is the same insight behind [[data-temperature|temperature tiering]].

Technical limits also bind retention to time:

- **Hot storage has limits.** RAM/cache-tier data cannot be retained forever — you need **TTLs** to expire entries.
- **Disk space is finite.** Eventually warm data has to be tiered down or deleted.

### 3. Compliance

Two directions, both mandatory:

- **Minimum retention.** HIPAA, PCI, and financial-records regulations require data be retained for specified periods, accessible on request. Chapter 6: "the data simply needs to be accessible upon request, even if the likelihood of an access request is low" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).
- **Maximum retention.** GDPR/CCPA require deletion of personal data on request or past a defined period. The engineer must be able to **find and delete specific records** reliably.

These pull in opposite directions. The storage architecture must support both: cold long-term archives that are cheap to retain *and* lineage that makes targeted deletion feasible.

### 4. Cost

Data has an ROI. Chapter 6 recommends automating data lifecycle management to match retention policy to cost (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- Move data to cold/archival tiers past the "frequently accessed" window.
- Delete data that is past its useful life and not required by compliance.
- Model retrieval costs — moving cold data back out is often the expensive part.

## How retention shows up in storage systems

| System | Retention mechanism |
|---|---|
| [[object-storage]] | Lifecycle policies: auto-tier to cold classes; auto-delete past N days. |
| [[data-warehousing|Cloud data warehouse]] | SQL `DELETE` with `WHERE`; table-level TTL on some platforms. |
| [[data-lake]] (classic) | Append-only; deletion requires rewriting partitions or entire files. |
| [[data-lakehouse]] / [[lakehouse-table-formats]] | `DELETE` statements backed by [[mvcc|MVCC]] and [[tombstone|tombstones]]; VACUUM removes old versions. |
| [[streaming-storage]] | Topic-level retention (days / weeks / indefinite); tiered storage offloads old partitions to object storage. |
| [[cache-memory-storage]] | TTL per key; LRU eviction when memory is full. |

The engineer picks a policy at each layer and verifies they compose — a warehouse-level deletion is worthless if the raw data still lives in an append-only lake file with the same PII.

## The connection to temperature

Retention and [[data-temperature|temperature]] are two dimensions of the same problem:

- **Temperature** — "how fast does this need to be accessible?" → choice of storage *tier*.
- **Retention** — "for how long?" → choice of storage *duration*.

A complete storage policy specifies both: *keep transaction events in hot storage for 30 days, warm for 1 year, cold for 7 years, then delete*. Cloud lifecycle policies automate this transition.

## Related pages

- [[data-lifecycle-management]]
- [[data-temperature]]
- [[data-storage-stage]]
- [[data-lake]]
- [[object-storage]]
- [[lakehouse-table-formats]]
- [[streaming-storage]]
- [[data-ethics]]
- [[data-governance]]
- [[backups-vs-archives]]
