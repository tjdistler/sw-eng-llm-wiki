# Write Conflicts

**Summary**: When two nodes in a [[multi-leader-replication]] or [[leaderless-replication]] system concurrently accept writes to the same data, a conflict arises that the system must resolve — usually in a way that risks data loss if not handled carefully.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Last updated**: 2026-04-15

---

## Why conflicts happen

In [[leader-based-replication]], the single leader serializes all writes: the second writer blocks or retries. In multi-leader and leaderless systems, two writers succeed locally and the conflict is only discovered asynchronously, when the writes are exchanged. At that point, it may be too late to ask users to arbitrate.

You could make conflict detection synchronous — waiting for all replicas to confirm before reporting success — but that negates the availability advantage of multi-leader replication. If you want synchronous conflict detection, you might as well use single-leader.

## Conflict avoidance

The simplest strategy: ensure all writes for a particular record always route through the same leader. If a user always writes their data to the same datacenter's leader, conflicts can't occur for that user's data. This works until the designated leader changes (failover, user relocation), at which point conflicts become possible again.

## Resolution strategies

### Last write wins (LWW)

Attach a timestamp to each write. The write with the highest timestamp wins; others are discarded.

- Simple to implement; the only conflict resolution in Cassandra, optional in Riak.
- **Dangerous**: silently discards data. Concurrent writes that were all acknowledged to the client may be lost. Even non-concurrent writes can be dropped due to clock skew.
- Safe only when keys are written once and treated as immutable thereafter (e.g., using UUIDs as keys in Cassandra).

### Replica ID ordering

Give each replica a unique ID and let writes from higher-numbered replicas always win. Also implies data loss.

### Value merging

Rather than picking a winner, merge the conflicting values — e.g., take the union of two sets, or concatenate strings. Requires the data to be merge-friendly. For sets, this works cleanly; for scalar values, it typically produces garbage.

**Tombstones**: a deletion cannot simply be modeled as "remove the item" because merging a version that removed the item with a version that kept it would resurrect it. Instead, deletions are marked with a *tombstone* — a marker that survives merges, indicating the item was intentionally removed.

### Custom conflict resolution logic

Application-provided code runs automatically when a conflict is detected:

- **On write**: the database calls the conflict handler as soon as a conflict appears in the replication log. Must run quickly; cannot prompt the user. Example: Bucardo (Postgres) allows a Perl snippet.
- **On read**: all conflicting versions are stored and returned to the application on the next read. The application resolves the conflict and writes the result back. Example: CouchDB.

Conflict resolution applies at the granularity of a single row or document, not an entire transaction.

## Automatic conflict resolution approaches

Three research-backed approaches that can reduce or eliminate the need for manual resolution:

**CRDTs (Conflict-free Replicated Data Types)**: data structures (sets, maps, counters, ordered lists) designed so that concurrent modifications can always be merged automatically and sensibly. No data loss. Used in Riak 2.0. Appropriate when the data structure maps to a CRDT type.

**Mergeable persistent data structures**: track full history (like git) and use three-way merges instead of two-way merges.

**Operational transformation**: the algorithm behind collaborative text editors (Google Docs, Etherpad). Designed for concurrent edits to ordered lists of characters, transforming operations so they commute correctly regardless of arrival order.

## What counts as a conflict?

Obvious conflicts: two writers simultaneously update the same field to different values. Subtle conflicts: a meeting room booking system where two bookings for the same room at the same time are inserted on different leaders — neither write touches the other's data, but together they violate a constraint. These application-level conflicts require application-level awareness.

## Related pages

- [[multi-leader-replication]]
- [[leaderless-replication]]
- [[version-vectors]]
- [[replication]]
- [[eventual-consistency]]
