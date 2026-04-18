# System Prevalence Pattern

**Summary**: A storage technique in which application state is **held in RAM for fast access** and **mutations are synchronously journaled to persistent disk** for durability. The application is restored on restart by replaying the journal from a snapshot. Chapter 25 names system prevalence as the technique [[task-master|Task Master]] uses to combine the speed of in-memory state with the durability of a database; the pattern predates modern naming (Redis AOF, [[event-sourcing|event-sourcing]]) but is conceptually identical.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What it is

The chapter's specific reference (source: chapter-25-data-processing-pipelines.md):

> The Task Master uses the system prevalence pattern to hold all job states in memory for fast availability while synchronously journaling mutations to persistent disk.

The system prevalence pattern (the term originates from the Smalltalk / Prevayler community) has three components:

1. **The in-memory model** — the live state of the application, held in regular language data structures, mutated by regular code.
2. **The command journal** — a persistent log of every mutation applied to the model, written synchronously before the mutation takes effect in memory.
3. **Periodic snapshots** — full serialised dumps of the in-memory model, written occasionally to bound recovery time.

Recovery is: load the latest snapshot into memory, then replay the journal entries since the snapshot.

## Why it works for Workflow

The pattern fits [[google-workflow|Workflow]]'s [[task-master|Task Master]] for several reasons:

- **Read latency is critical.** Workers acquire leases, commit work, read configuration — all in the request path of every pipeline operation. In-memory state means every read is a memory access, not a database round-trip.
- **Write throughput is moderate.** Lease acquisitions and commits happen frequently but not at the rate of bulk-data operations (which go to the [[distributed-filesystems|distributed filesystem]] directly). The synchronous journal can keep up.
- **Recovery time is bounded by snapshot frequency.** A daily snapshot plus a day's worth of journal entries is a few minutes of recovery; a more frequent snapshot reduces this further at the cost of snapshot I/O.
- **All state fits in RAM.** Because the Task Master holds only pointers to work (not the bulk data itself), the in-memory state of even a large pipeline fits comfortably in a single machine's RAM.

## What it gives up vs a general database

The pattern is not a free lunch:

- **Single-writer.** The in-memory model is owned by one process; you cannot have multiple instances mutating it concurrently. For Workflow this is fine because the Task Master is the single coordinator.
- **No ad-hoc query layer.** The model is whatever data structures the application defines; there is no SQL surface for unforeseen queries. Workflow doesn't need one — its access pattern is fully known at design time.
- **Schema evolution is the application's problem.** Changing the in-memory model means versioning the journal entries and writing replay code that handles old entries. Less convenient than ALTER TABLE.
- **Replication / HA is not built in.** Standalone system prevalence runs on one machine. To survive machine loss you need additional machinery — for Workflow this is the [[workflow-business-continuity|business-continuity layer]] that journals to [[spanner|Spanner]].

For Workflow's Task Master these are acceptable trade-offs because the access pattern is uniform, schema evolution is rare, and HA is solved at a different layer.

## Modern descendants

The pattern is conceptually identical to several systems that emerged later:

- **[[redis|Redis]] AOF persistence** — in-memory key-value store with append-only file journaling and periodic RDB snapshots.
- **[[event-sourcing|Event-sourced]] applications** — Kleppmann's name for the same shape applied at the application architecture level: state is derived by folding over an immutable command/event log.
- **In-memory databases with WAL** — VoltDB, MemSQL, Hekaton; commercial packagings of the same idea with SQL surfaces.
- **[[actual-serial-execution|Single-threaded transaction execution]]** (DDIA) — Kleppmann's discussion of VoltDB-style serial execution depends on the same in-memory + WAL substrate.

The Workflow chapter notes the pattern by reference rather than developing it in detail, treating it as a known technique to apply.

## Cross-references

- [[task-master]] — the specific Workflow component that uses this pattern
- [[google-workflow]] — the system the pattern enables
- [[event-sourcing]] (Kleppmann) — the modern packaging of the same idea at the application level
- [[actual-serial-execution]] (Kleppmann) — VoltDB-style serial execution, which depends on the same in-memory + journal substrate
- [[redis|Redis]] — the canonical open-source instance (named in the wiki's caching-layer page); AOF persistence is system prevalence by another name
- [[mvcc]] (Kleppmann) — the alternative pattern: keep multiple versions in a database, allow concurrent reads. System prevalence chooses single-writer + RAM speed over MVCC's multi-version concurrency

## Related pages

- [[task-master]]
- [[google-workflow]]
- [[workflow-correctness-guarantees]]
- [[event-sourcing]]
- [[actual-serial-execution]]
- [[data-processing-pipelines]]
