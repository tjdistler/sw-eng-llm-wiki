# Application Database as a Source

**Summary**: An application database — typically an [[oltp-vs-olap|OLTP]] system that stores application state — is the canonical first [[source-systems|source system]] a data engineer encounters. The tricky part is that the database is doing its *real* job (serving the application) while the engineer needs to extract from it without degrading that job. Reis and Housley's Chapter 5 treats this producer-consumer tension as a defining challenge of the generation stage.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## What an application database is

An application database "stores the state of an application" — the canonical example is the database that holds bank-account balances and updates them as transactions and payments flow through (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). It is typically an [[oltp-vs-olap|OLTP]] system: low latency, high concurrency, millisecond-scale row reads and updates, thousands of reads and writes per second.

The database may be:

- A [[relational-model|relational]] RDBMS — the traditional default.
- A [[document-model|document]] store — higher commit rates at the expense of consistency.
- A [[graph-data-models|graph]] database — when the application is relationship-heavy.

These shapes are common across application backends and "work well when thousands or even millions of users might be interacting with the application simultaneously" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Why the source-vs-backend tension matters

An application database is doing two jobs at once if a data engineer starts pulling from it:

1. **Primary job.** Serve the application — low latency, high concurrency, predictable performance.
2. **Incidental job.** Supply rows to an analytics pipeline — potentially large scans, joins across many tables, unpredictable query shapes.

Small companies routinely run analytics directly on the OLTP database. Reis and Housley are explicit: **this works in the short term but is ultimately not scalable** (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). Eventually either the structural limits of OLTP storage or simple resource contention with the transactional workload will bite. The engineer's job is to "set up appropriate integrations with analytics systems without degrading production application performance."

## Extraction patterns

Three approaches commonly used to pull data out without harming the live application:

| Pattern | Load on source | Latency | Notes |
|---|---|---|---|
| **Full scan / snapshot** | High — potentially table-locking | High (batch) | Works for small or slowly-changing data; cost grows linearly with table size |
| **Query-based [[change-data-capture|CDC]]** | Medium — scoped scans by `updated_at` | Minutes-to-hours | See [[query-based-cdc]] |
| **Log-based [[change-data-capture|CDC]]** | Very low — reads binlog/WAL | Near-real-time | Preferred for busy sources; doesn't touch live tables |
| **Read replica** | Zero on primary | Replication-lag bound | Offload scans to a replica configured for reporting |
| **[[outbox-table-pattern|Outbox]]** | Zero extra on scan side | Transactional with the write | Source team writes events alongside state changes |

The [[change-data-capture|log-based CDC]] and [[outbox-table-pattern|outbox]] approaches are what [[data-liberation|data liberation]] advocates for: the source ships a proper event stream rather than being reverse-queried.

## ACID and what it buys

Most RDBMS-backed application DBs offer [[acid|ACID]] guarantees: [[transactions|atomicity]], consistency, isolation ([[isolation-levels]]), and durability. Reis and Housley note this is "not required to support application backends, and relaxing these constraints can be a considerable boon to performance and scale" — but relaxed consistency (for example [[eventual-consistency]]) "dramatically simplifies the app developer's task" is lost (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). The engineer must know what consistency model the source provides, because it shapes how the extracted data behaves downstream.

Relaxed-consistency NoSQL sources are not ACID and often have to be analyzed via **full scan** or **CDC** strategies rather than transactional reads; this has performance and cost implications, particularly in serverless cloud variants that charge per-scan (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Data applications: hybrid backends

Reis and Housley coin the term **data application** for the emerging class of applications that "hybridize transactional and analytics workloads" — SaaS products that offer embedded analytics on live data (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). These blur the OLTP/OLAP line and create new challenges for data engineers: quick updates *combined with* analytics capabilities, with no clean boundary between the two. See [[analytics]] for the embedded-analytics framing.

## What changes when the source is CRUD

A [[crud|CRUD]]-pattern table lets the application overwrite fields in place, so **history is lost at the source** unless captured. Two options for keeping history:

- **[[change-data-capture|CDC]]** — capture every change event as it happens and ship it to a downstream stream or warehouse.
- **[[insert-only|Insert-only]] pattern** at the source — the application never updates or deletes; it appends new rows with timestamps.

Without one of these, "snapshot-based extraction" gives only the current state — you can see *what* is true now but not *what used to be true* or *when it changed* (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Cross-book connections

- [[source-systems]] — the Chapter 2 overview of which an application DB is one example.
- [[source-system-considerations]] — the Chapter 5 checklist applied to any source, including this one.
- [[change-data-capture]] — the most common pattern for extracting from a live application DB without query load.
- [[data-liberation]] (Bellemare) — the maturity path: move from extracting-from-the-DB to the-DB-publishes-events-first.
- [[outbox-table-pattern]] (Bellemare) — the best-in-class technique when the source team is cooperative.
- [[oltp-vs-olap]] — the DDIA treatment of the access-pattern difference this page depends on.

## Related pages

- [[source-systems]]
- [[source-system-considerations]]
- [[oltp-vs-olap]]
- [[change-data-capture]]
- [[crud]]
- [[insert-only]]
- [[outbox-table-pattern]]
- [[data-liberation]]
- [[acid]]
- [[relational-model]]
- [[document-model]]
- [[analytics]]
