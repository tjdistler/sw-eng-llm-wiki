# Source System Considerations

**Summary**: The practical checklist a data engineer should run through before connecting to any new [[source-systems|source system]]. Chapter 5 of *Fundamentals of Data Engineering* expands the evaluation questions from Chapter 2 into a full set of concerns spanning data shape, volume, cadence, reliability, ownership, and the six [[data-engineering-lifecycle|lifecycle undercurrents]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## Why the checklist matters

Source systems are **outside the data engineer's control**, so most of the engineer's leverage is in *understanding* them deeply before writing any code. Reis and Housley's advice: read the source system's documentation, learn how it operates (writes, commits, queries), and know its patterns and quirks before building an ingestion path on top (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). The questions below are the starting point.

## Database characteristics

For any database-backed source (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **DBMS components.** Storage engine, query optimizer, disaster recovery, replication — know what the vendor ships.
- **Lookups.** How does the database find rows? What [[indexes]] exist (B-tree, [[sstables-and-lsm-trees|LSM]])? What are the efficient extraction patterns?
- **Query optimizer.** Present? What are its characteristics?
- **Scaling strategy.** Horizontal (more nodes) or vertical (bigger box)?
- **Modeling patterns.** Normalized or wide-table? See [[data-modeling]].
- **CRUD handling.** See [[crud]] — every database implements create/read/update/delete differently.
- **Consistency model.** Fully consistent, [[eventual-consistency|eventually consistent]], or configurable per read/write? Understanding the consistency model "helps you prevent disasters" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Data shape and volume

- **Structure.** Structured (RDBMS, Parquet), semi-structured (JSON, XML), unstructured (plain text, blobs).
- **Schema.** Fixed (schema-on-write) or flexible (schema-on-read)? See [[schema-on-read-vs-write]].
- **Volume.** Bytes per day, rows per hour, peak multipliers.
- **Cardinality.** How many distinct keys, partitions, devices?
- **Partitioning.** How does the source partition its own data? Shape must be preserved or re-shaped downstream.

## Cadence and delivery

- **Generation rate.** Events per second, gigabytes per hour.
- **Read cadence.** Batch (daily, hourly, sub-hourly) or continuous?
- **Push vs pull.** Who initiates — the source or the ingestion system? See [[data-ingestion]].
- **Stateful handling.** For state-bearing sources, periodic snapshots or [[change-data-capture|CDC]]? How are changes tracked internally?

## Reliability and quality

- **Uptime.** What SLA can the source commit to?
- **Error frequency.** Duplicates, nulls, late arrivals, corrupt rows — what's the rate, and what's the remediation path?
- **Provenance.** Which team or process is the transmitting authority? Is there an upstream chain whose problems propagate?
- **Trust.** Is the source legitimate? Reis and Housley: "trust but verify" — don't ingest data from a malicious actor (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Impact on the source

- **Load coupling.** Will your read traffic hurt the source's performance? OLTP sources are especially sensitive to full scans.
- **Minimally-invasive extraction.** Prefer log-based [[change-data-capture|CDC]], replica reads, or dedicated read-only replicas over live-table scans when possible.

## Ownership and contracts

Two classes of stakeholders to identify and maintain relationships with (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Systems stakeholders.** Software engineers, application developers, third parties — the people who build and maintain the source system.
- **Data stakeholders.** IT, data governance, third parties — the people who own and control access to the data itself.

A [[data-contract]] with these stakeholders should state what data is extracted, via what method (full, incremental), how often, and who the contacts are on both sides. Pair it with an [[service-level-agreement|SLA]] and [[service-level-objective|SLO]] for uptime and quality expectations.

## Undercurrents checklist

Source systems touch every one of the six [[data-engineering-lifecycle|lifecycle undercurrents]]. Chapter 5 names concrete questions per undercurrent (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

| Undercurrent | Source-system concern |
|---|---|
| [[data-security|Security]] | Encryption at rest and in flight; public internet vs VPN; secret-store hygiene for credentials; trust verification |
| [[data-management]] | Governance, quality, schema change, MDM, privacy/ethics, regulatory fit |
| [[dataops]] | Automation coupling, observability of uptime and quality, incident response |
| [[data-architecture]] | Reliability, durability, availability; who owns architectural decisions upstream |
| [[orchestration]] | Cadence, frequency, common frameworks (Kubernetes, Airflow integration) |
| [[software-engineering-for-data]] | Network access, authn/authz, access patterns, retries/timeouts, deployment |

## Cross-book connections

- The Chapter 2 version of this list lives on [[source-systems]]. Chapter 5 expands it rather than replacing it; read both together.
- Bellemare's [[data-liberation]] and [[outbox-table-pattern]] are what the "ideal" end-state looks like — the source team publishes a first-class event stream so none of these questions have to be answered under duress by the data engineer.

## Related pages

- [[source-systems]]
- [[data-engineering-lifecycle]]
- [[data-ingestion]]
- [[change-data-capture]]
- [[data-contract]]
- [[data-engineer-stakeholders]]
- [[schema-on-read-vs-write]]
- [[crud]]
- [[nosql]]
