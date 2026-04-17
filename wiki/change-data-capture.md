# Change Data Capture

**Summary**: Change data capture (CDC) is the process of observing all data changes written to a database and extracting them as a stream that can be replicated to other systems -- making one database the leader and turning derived systems (search indexes, caches, warehouses) into followers.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`, `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## The problem: keeping systems in sync

Most nontrivial applications use multiple data systems: an OLTP database for serving requests, a cache for speed, a full-text index for search, and a data warehouse for analytics. Each stores its own copy of the data, optimized for its purpose. These copies must be kept in sync (source: chapter-11-stream-processing.md).

### Why dual writes fail

A common but flawed approach is **dual writes**: the application explicitly writes to each system when data changes (e.g., write to the database, then update the search index, then invalidate the cache). Dual writes have two serious problems (source: chapter-11-stream-processing.md):

1. **Race conditions**: Two concurrent clients updating the same item can interleave their writes to different systems, leaving them permanently inconsistent. For example, the database ends up with value B while the search index ends up with value A, with no error reported. Without a concurrency detection mechanism like [[version-vectors]], this goes unnoticed.

2. **Partial failure**: One write may succeed while another fails, again leaving systems inconsistent. Ensuring both succeed or both fail is the [[two-phase-commit|atomic commit problem]], which is expensive to solve.

The root cause is the lack of a single leader determining write order. If the database has a leader and the search index has a separate leader, neither follows the other, and conflicts arise (see [[multi-leader-replication]]).

## How CDC works

CDC solves the sync problem by making the database the single source of truth and treating all other systems as derived views. Changes are extracted from the database's internal log (replication log, write-ahead log, binlog, oplog) and applied to derived systems in the same order (source: chapter-11-stream-processing.md).

A [[log-based-message-brokers|log-based message broker]] is well suited for transporting change events because it preserves message ordering (source: chapter-11-stream-processing.md).

### Implementation approaches

| Approach | Examples | Notes |
|---|---|---|
| Parse replication log | Maxwell, Debezium (MySQL binlog), Bottled Water (PostgreSQL WAL), GoldenGate (Oracle) | More robust than triggers but must handle schema changes |
| Database triggers | Generic approach | Fragile, significant performance overhead |
| MongoDB oplog | Mongoriver | Reads the internal operation log |
| Large-scale systems | LinkedIn Databus, Facebook Wormhole, Yahoo! Sherpa | Custom CDC at scale |

(source: chapter-11-stream-processing.md)

### CDC is asynchronous

Like [[message-brokers]], CDC is usually asynchronous: the source database does not wait for consumers to apply the change before committing. This means adding a slow consumer does not affect the source, but all issues of [[replication-lag]] apply (source: chapter-11-stream-processing.md).

## Initial snapshot

If you don't have the complete log history (which would require too much disk space to retain forever), new derived systems need a **consistent snapshot** of the database as a starting point, corresponding to a known offset in the change log. After processing the snapshot, the consumer applies changes from that offset forward. Some CDC tools integrate this; others require manual snapshots (source: chapter-11-stream-processing.md).

## Log compaction

An alternative to periodic snapshots: [[log-based-message-brokers|log compaction]] retains only the most recent update for each primary key. A new consumer can start from offset 0 of the compacted topic and obtain a full copy of the database without a separate snapshot. Apache Kafka supports this natively (source: chapter-11-stream-processing.md).

CDC log compaction works because each event typically contains the entire new version of the record, so the latest event for a primary key fully determines the current value. (This differs from [[event-sourcing]], where events express intent rather than state, and log compaction is not applicable in the same way.) (source: chapter-11-stream-processing.md)

## API support for change streams

Databases are increasingly providing change streams as a first-class interface rather than requiring reverse-engineering of internal logs (source: chapter-11-stream-processing.md):

- **RethinkDB** -- queries subscribe to result change notifications
- **Firebase and CouchDB** -- data synchronization via change feeds
- **Meteor** -- subscribes to MongoDB oplog for UI updates
- **VoltDB** -- exports data as a stream via a special table that committed transactions write to
- **Kafka Connect** -- integrates CDC tools for many database systems with Kafka

## Relationship to replication

CDC is conceptually the same as [[replication]]: the source database is the leader, and derived systems are followers that apply the leader's change stream. The key difference is that CDC replicates across heterogeneous systems (database to search index, database to cache) rather than between identical database replicas (source: chapter-11-stream-processing.md).

This connects to the [[state-machine-replication]] principle: if every replica processes the same events in the same order, they converge to the same state.

## CDC as a microservice migration pattern

Newman lists CDC as a fallback migration pattern for situations where you need to react to a change inside the [[monolith]] but cannot intercept it via the monolith's API perimeter, cannot change the monolith's source code, and cannot use a [[decorating-collaborator-pattern]] because the inbound request and response don't carry the information you need (source: chapter-03-splitting-the-monolith.md).

### Example: loyalty cards

When a customer is enrolled, the monolith returns only "success". To print a loyalty card, a new service needs more customer details. Rather than hacking that data out of the monolith's response, you watch for inserts into the `LoyaltyAccount` table and fire a `Loyalty Account Created` event into a message broker. A printing service consumes the event and batches print jobs (source: chapter-03-splitting-the-monolith.md).

### Implementation options Newman highlights

| Approach | Trade-off |
|---|---|
| **Database triggers** | "Having one or two triggers isn't terrible. Building a whole system off them is a terrible idea." (Randy Shoup, quoted by Newman) Tooling and change management are weak; the system becomes baroque. (source: chapter-03-splitting-the-monolith.md) |
| **Transaction log pollers** | Most sophisticated; runs as a separate process reading the binlog/WAL. Only sees committed transactions. Newman calls this the neatest implementation. (source: chapter-03-splitting-the-monolith.md) |
| **Batch delta copier** | Periodic scan for changed rows. Simple but works only when the schema or metadata can tell you what changed; otherwise considerable bookkeeping. (source: chapter-03-splitting-the-monolith.md) |

### When to use it for migration

Newman recommends keeping CDC use to a minimum during migration because of the implementation complexity (source: chapter-03-splitting-the-monolith.md). It's a useful tool when other patterns don't fit — particularly when the data change *is* the event the new service cares about.

The pattern unavoidably couples the new system to the monolith's *datastore*, not just its API. That's a real cost worth weighing against the benefit of not having to change the monolith. See [[migration-pattern-selection]] for the broader picture.

## CDC in Bellemare's three-pattern taxonomy

Bellemare decomposes change-data capture into **three patterns for extracting data from an underlying store** as part of [[data-liberation]] — the broader umbrella under which CDC sits in the event-driven microservices story (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

| Pattern | Page | Core idea |
|---|---|---|
| Query-based | [[query-based-cdc]] | Periodic SELECT against the source store, filtered by `updated_at` or autoincrementing id |
| Log-based | this page | Parse the binlog / WAL / oplog directly |
| Outbox / table-based | [[outbox-table-pattern]] | Application writes to an outbox inside the business transaction; publisher drains it |

Triggers are a fourth, older mechanism — see [[cdc-triggers]]. The log-based option is what the DDIA and Newman sections above describe.

### Benefits of log-based CDC (Bellemare's framing)

- **Hard-delete tracking.** Binlogs contain deletes; no soft-delete workaround needed, unlike [[query-based-cdc]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Minimal performance impact on the source.** Log-based capture reads the change log, not the live tables. Change-data-table systems (e.g., SQL Server) scale with volume instead.
- **Low latency.** Updates propagate as soon as the write lands in the log.

### Drawbacks of log-based CDC

- **Internal-data-model exposure.** The log contains the internal schema, and there is no view-layer equivalent to hide it. Isolation must be managed carefully and selectively — or compensated downstream with [[eventification]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Denormalization happens outside the data store.** Logs emit single-table entries, so highly normalized sources produce highly normalized event streams. Downstream consumers (or a dedicated eventifier) must handle foreign-key joins.
- **Brittle schema coupling.** Like query-based CDC, the capture mechanism lives outside the source application's codebase. A valid DDL change can be an invalid schema evolution for the output event. DDL handling is pattern-specific — see the DDL section in [[data-liberation]].

### Bootstrapping

The log is not retained back to the beginning of time. A new log-based CDC pipeline must start with a **snapshot query** of the source table (a performance-impacting bulk read), with overlap guaranteed against the log's start to avoid missing records (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md). Progress is then checkpointed; a failure can restore from the last checkpoint and re-read from the log. This gives **at-least-once** production semantics, which is usually fine for entity data because updates are idempotent.

### Tooling

- **Debezium** is the most widely used log-based CDC reader. It handles most common relational databases and writes to Kafka or Pulsar. See also [[data-liberation-framework]].
- **Maxwell** is MySQL-only, Kafka-only, and lighter.
- Modern NoSQL stores often expose change logs as a first-class API — MongoDB Change Streams, Couchbase replication, etc.

### Log-based CDC as a bootstrap, not a destination

Bellemare is explicit that CDC tooling is **"primarily meant to help bootstrap the process"** of moving to EDM, not its final form. Organizations that rely on centralized connectors permanently tend to institutionalize two anti-patterns: exposing internal data models, and leaving source teams passive about event production. For actively developed systems, migrate from log-based CDC to the [[outbox-table-pattern]] as the source team matures (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## CDC's role in database decomposition

Newman returns to CDC repeatedly in his database-decomposition chapter. Beyond the migration-pattern use above, it appears as the recommended mechanism for several other patterns (source: chapter-04-decomposing-the-database.md):

- **Mapping engine for the [[database-as-a-service-interface]] pattern** — Debezium and similar tools are Newman's preferred way to keep an externally-exposed read-only database in sync with the service's internal database. He prefers CDC to batch copies because batches lag, fail silently, and don't fit the modern "data faster" expectation.
- **Bringing the new database in sync after a bulk import** — in the [[synchronize-data-in-application]] pattern, after the initial batch copy completes, a CDC process catches up the changes that happened *during* the import. This is how Trifork bridged the snapshot-to-live gap when migrating Danish medical records to Riak.
- **Synchronising sources of truth in [[tracer-write]]** — CDC is one of the three options for keeping the old and new sources in sync during a phased migration; the windows of inconsistency it produces are typically measured in seconds.

The recurring theme: CDC turns the monolith's database into a source of events for everyone else, without requiring the monolith to know it's happening.

## Related pages

- [[stream-processing]]
- [[event-streams]]
- [[log-based-message-brokers]]
- [[event-sourcing]]
- [[replication]]
- [[replication-lag]]
- [[state-machine-replication]]
- [[two-phase-commit]]
- [[multi-leader-replication]]
- [[version-vectors]]
- [[data-warehousing]]
- [[decorating-collaborator-pattern]]
- [[migration-pattern-selection]]
- [[strangler-fig-pattern]]
- [[database-decomposition]]
- [[database-as-a-service-interface]]
- [[synchronize-data-in-application]]
- [[tracer-write]]
- [[data-liberation]]
- [[query-based-cdc]]
- [[outbox-table-pattern]]
- [[cdc-triggers]]
- [[data-liberation-framework]]
- [[event-sinking]]
- [[eventification]]
