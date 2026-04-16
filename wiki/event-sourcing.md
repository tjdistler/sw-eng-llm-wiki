# Event Sourcing

**Summary**: Event sourcing stores all changes to application state as an immutable, append-only log of events that express user intent at the application level -- in contrast to [[change-data-capture]], which extracts low-level state changes from a database's internal log.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## Core idea

Event sourcing, developed in the domain-driven design (DDD) community, involves storing every change to application state as an immutable event in an append-only log. Updates and deletes are discouraged or prohibited -- instead, new events represent changes (e.g., a cancellation event rather than a row deletion) (source: chapter-11-stream-processing.md).

## Event sourcing vs change data capture

Both store a log of changes, but they operate at different levels of abstraction (source: chapter-11-stream-processing.md):

| Aspect | [[change-data-capture]] | Event sourcing |
|---|---|---|
| Abstraction level | Low-level database changes (row inserts, updates, deletes) | Application-level user intent |
| Database usage | Application uses the database mutably; CDC extracts the change log transparently | Application writes directly to an append-only event log |
| Application awareness | Application doesn't need to know CDC is occurring | Application logic is explicitly built around immutable events |
| Log compaction | Works -- latest event per key determines current state | Does not work the same way -- later events don't override earlier ones; full history is needed |
| Example event | "Row 42 in enrollments table was deleted" | "Student cancelled their course enrollment" |

The event sourcing approach captures more meaningful information: "student cancelled their course enrollment" expresses intent, while "row deleted from enrollments, row added to feedback" embeds assumptions about how data will be used. If a new feature is added (e.g., offering the place to the next person on the waiting list), the event sourcing approach allows it to be chained off the existing event (source: chapter-11-stream-processing.md).

## Deriving current state from events

An event log by itself is not directly useful to users -- they want to see current state (the contents of their cart, not the full history of changes). Applications using event sourcing must transform the event log into application state suitable for reading. This transformation should be deterministic so it can be replayed to reconstruct state (source: chapter-11-stream-processing.md).

Because event sourcing events express intent rather than state updates, **log compaction cannot discard old events** the way it can with [[change-data-capture]]. The full event history is needed to reconstruct the final state. Applications typically store **snapshots** of current state as a performance optimization for reads and crash recovery, but the system should be capable of reprocessing the full event log from scratch (source: chapter-11-stream-processing.md).

Event sourcing is similar to the chronicle data model and shares similarities with fact tables in a [[data-warehousing|star schema]]. Specialized databases like Event Store support event sourcing, but the approach is independent of any particular tool -- a conventional database or [[log-based-message-brokers|log-based message broker]] works too (source: chapter-11-stream-processing.md).

## Commands vs events

Event sourcing carefully distinguishes the two (source: chapter-11-stream-processing.md):

- A **command** is an incoming user request that may still fail (e.g., "register username X" -- it might already be taken).
- An **event** is a command that has been validated and accepted. It is durable, immutable, and represents a fact.

Validation must happen **synchronously**, before a command becomes an event. Options include:
- A serializable transaction that atomically validates the command and publishes the event
- A two-step approach: publish a tentative reservation event, then a separate confirmation event after async validation

Once an event is generated, consumers of the event stream cannot reject it -- it is already an immutable part of the log that other consumers may have seen (source: chapter-11-stream-processing.md).

## State, streams, and immutability

Mutable state and an immutable event log are two sides of the same coin. The application state is the result of integrating the event stream over time; the event stream is the derivative of state over time. Pat Helland's insight: "The truth is the log. The database is a cache of a subset of the log" (source: chapter-11-stream-processing.md).

### Advantages of immutability

- **Auditability**: Like financial bookkeeping, mistakes are corrected with compensating entries, not erasure. The original record remains.
- **Bug recovery**: If buggy code writes bad data, an immutable log makes diagnosis and recovery much easier than destructive overwrites.
- **Richer analytics**: A customer adding then removing an item from their cart generates useful intent data that a mutable database would lose.
- **Multiple views**: The same event log can feed different read-optimized representations (search indexes, analytics, caches). See CQRS below.

(source: chapter-11-stream-processing.md)

## Command Query Responsibility Segregation (CQRS)

By separating the write format (append-only event log) from the read format (derived views), you gain flexibility (source: chapter-11-stream-processing.md):

- Multiple read-optimized views can be derived from the same event log
- New features can create new views by replaying the event log, running side by side with existing systems
- Debates about [[normalization]] and denormalization become less relevant -- you can denormalize in read views because the event log keeps them consistent
- Evolving the application is easier: build a new view, run it alongside the old system, then retire the old one

This is the idea behind CQRS: separating the form in which data is written from the form in which it is read.

## Concurrency control

The main downside of event sourcing (and [[change-data-capture]]) is that consumers are usually asynchronous, so a user may write an event and then read from a derived view before the view has been updated. This is the same problem as [[read-after-write-consistency]] (source: chapter-11-stream-processing.md).

On the other hand, event sourcing simplifies some concurrency problems: a user action can be captured as a single atomic append to the event log, reducing the need for [[transactions|multi-object transactions]]. If the event log and application state are partitioned the same way, a single-threaded log consumer needs no concurrency control for writes (source: chapter-11-stream-processing.md).

## Event sourcing as an alternative to soft deletes

Newman flags event sourcing as an alternative to soft-delete strategies when a service needs to preserve historical state across what would otherwise be hard deletes. In the [[move-foreign-key-to-code]] discussion, when the `Catalog` service stops "deleting" albums to preserve referential integrity for the `Finance` service, Newman notes (in a footnote) that maintaining historical data in a relational database can get complicated — particularly if you need to reconstitute earlier versions of entities — and that **event sourcing is a worthwhile alternative way to maintain state** in such situations (source: chapter-04-decomposing-the-database.md).

The fit is natural: event sourcing keeps every state change as a fact, so reconstituting old states or providing audit trails is straightforward. Soft delete is a partial solution to the same problem; event sourcing is the more general answer.

## Limitations of immutability

Keeping an immutable history forever is feasible when data is mostly appended and rarely updated. For workloads with high update/delete rates, the immutable history may grow prohibitively large and compaction/garbage collection performance becomes critical (source: chapter-11-stream-processing.md).

Some situations require true deletion (not just a "deleted" event): privacy regulations, data protection laws, accidental sensitive data leaks. Datomic calls this **excision**; Fossil calls it **shunning**. True deletion is surprisingly hard because copies may live in storage engines, filesystems, SSDs, and backups (source: chapter-11-stream-processing.md).

## Related pages

- [[stream-processing]]
- [[event-streams]]
- [[change-data-capture]]
- [[log-based-message-brokers]]
- [[data-warehousing]]
- [[normalization]]
- [[read-after-write-consistency]]
- [[transactions]]
- [[state-machine-replication]]
- [[replication]]
- [[move-foreign-key-to-code]]
- [[database-decomposition]]
