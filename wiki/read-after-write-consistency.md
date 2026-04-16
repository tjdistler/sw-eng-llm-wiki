# Read-After-Write Consistency

**Summary**: A guarantee that after a user submits data, any subsequent read by *that same user* will reflect their write — even on a system with asynchronous replication lag.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Last updated**: 2026-04-15

---

## The problem

In a [[leader-based-replication]] system with asynchronous followers, writes go to the leader but reads can come from any follower. If a user writes something and then immediately reads it back from a lagging follower, their own write appears missing — as though it was silently discarded. This is one of the three anomalies caused by [[replication-lag]].

Read-after-write consistency (also called *read-your-writes* consistency) ensures this doesn't happen. It makes no promise about what *other* users' writes are visible; only that your own writes are.

## Implementation strategies

**Route reads to the leader for user-owned data**: if only the owner can modify a piece of data (e.g., a user's own profile), always read it from the leader. This is simple but only works for a small subset of data.

**Time-based routing**: for a configurable window after a write (e.g., one minute), route all reads for that user to the leader or to replicas confirmed to be within one minute of lag. Requires monitoring replication lag.

**Client-tracked timestamps**: the client records the logical timestamp (or log sequence number) of its most recent write. On each read, the system routes to a replica that has caught up to at least that timestamp. If no such replica is available, the read waits or falls back to the leader.

## Cross-device complexity

When the same user accesses from multiple devices (desktop + mobile), the guarantees become harder to provide:

- The timestamp tracking must be centralized, because each device doesn't know what the others have written.
- If replicas are distributed across datacenters, there's no guarantee that two devices will be routed to the same datacenter — yet both need to see the same up-to-date view. Routing all of a user's traffic to a single datacenter may be required.

## Related pages

- [[replication-lag]]
- [[replication]]
- [[monotonic-reads]]
- [[consistent-prefix-reads]]
- [[eventual-consistency]]
