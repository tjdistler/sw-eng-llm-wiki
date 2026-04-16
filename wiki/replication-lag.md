# Replication Lag

**Summary**: The delay between a write being processed on the leader and being reflected on an asynchronous follower — small in healthy systems, but capable of growing to minutes under load, causing real consistency anomalies.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Last updated**: 2026-04-15

---

## What replication lag is

In [[leader-based-replication]] with asynchronous followers, writes go to the leader but reads can be served by any follower. If a follower is behind, a read from that follower returns stale data. This temporary inconsistency is called **eventual consistency** — the replicas will converge to the same value, but only eventually.

In normal operation, lag is a fraction of a second and unnoticeable. Under high load or network problems, it can grow to minutes. At that scale, the inconsistency is not theoretical — it causes real problems for users.

## Read-scaling architecture

The primary motivation for tolerating replication lag is **read scaling**: add more followers to serve more read requests without burdening the leader. This only works with asynchronous replication — synchronous replication to all followers would mean any single follower outage blocks all writes.

## The three anomalies

Replication lag produces three specific categories of observable inconsistency:

### 1. Stale reads after your own write

A user submits data, then immediately reads it back. If the read is served by a lagging follower, the user sees their own write missing — as if it was lost. This violates [[read-after-write-consistency]].

### 2. Time going backward

A user makes two reads in sequence from different replicas. The first replica is fresh, the second is lagging. The user sees data "disappear" — something visible in the first read is absent in the second. This violates [[monotonic-reads]].

### 3. Seeing effects before causes

In a sharded or multi-replica system, some writes may replicate faster than others. An observer may see a reply before the question it answers — a causal violation. This violates [[consistent-prefix-reads]].

## Why application-level workarounds are fragile

Applications *can* work around replication lag — routing certain reads to the leader, tracking timestamps, pinning users to replicas — but doing so is complex and error-prone. The right long-term answer is for the database to provide stronger guarantees ([[eventual-consistency]] → transactions). Single-node transactions have existed for decades; distributed transactions are harder and were widely abandoned in the NoSQL era, though this turned out to be an oversimplification.

## Monitoring replication lag

In [[leader-based-replication]], lag is measurable: subtract a follower's current log position from the leader's position. In [[leaderless-replication]], no fixed write order exists, making lag much harder to quantify. Without an anti-entropy process, a rarely-read value on a stale replica might be arbitrarily old.

## Related pages

- [[replication]]
- [[leader-based-replication]]
- [[read-after-write-consistency]]
- [[monotonic-reads]]
- [[consistent-prefix-reads]]
- [[eventual-consistency]]
- [[leaderless-replication]]
