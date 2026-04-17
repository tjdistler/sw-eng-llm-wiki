# Multi-Leader Replication

**Summary**: A replication architecture where multiple nodes each accept writes; also called master–master or active/active replication. Increases write availability and is natural for multi-datacenter and offline-first scenarios, at the cost of mandatory [[write-conflicts]] resolution.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## The basic idea

[[leader-based-replication|Leader-based replication]] has one bottleneck: there is a single leader, and all writes must reach it. Multi-leader replication allows any of several nodes to accept writes, with each leader replicating its changes to all other leaders and followers.

Within a datacenter, multi-leader rarely makes sense — the added complexity outweighs the benefits. The payoff comes at larger scales.

## Use cases

### Multi-datacenter operation

With a single leader, all writes must traverse the network to whichever datacenter hosts the leader. In a multi-leader setup, each datacenter has its own leader. Writes are processed locally, then replicated asynchronously to other datacenters.

Comparison for multi-datacenter:

| Property | Single-leader | Multi-leader |
|---|---|---|
| Write latency | Network round-trip to leader datacenter | Local — fast |
| Datacenter outage tolerance | Failover required | Other datacenters keep working |
| Network interruption tolerance | Writes blocked if leader unreachable | Local writes continue |

### Offline-first / clients with offline operation

A calendar app that works offline is architecturally equivalent to multi-leader replication: each device is a "datacenter" with its own local leader, and sync happens when connectivity is restored. Replication lag can be hours or days. CouchDB is designed for this pattern.

### Collaborative editing

Real-time collaborative editing (Google Docs, Etherpad) applies the same pattern. If the unit of change is large (a paragraph), you can serialize with a lock — equivalent to single-leader. For keystroke-level collaboration, you need multi-leader with conflict resolution, which is exactly what [[write-conflicts]] resolution algorithms (including operational transformation) address.

## The fundamental problem: write conflicts

The major downside of multi-leader replication is that the same data can be concurrently modified in two different leaders, producing a conflict that must be resolved. See [[write-conflicts]] for resolution strategies.

Multi-leader is described as "dangerous territory" in many databases — it's often a retrofitted feature with subtle interactions with autoincrement keys, triggers, and integrity constraints. Implementations include Tungsten Replicator (MySQL), BDR (PostgreSQL), and GoldenGate (Oracle).

## Replication topologies

A **replication topology** is the communication graph along which writes propagate between leaders.

**All-to-all**: every leader sends its writes to every other leader. Most fault-tolerant; if one link is slow, writes can route around it. But causality can be violated if some messages overtake others (see [[consistent-prefix-reads]]).

**Circular**: each node forwards writes to exactly one other node, forming a ring. A single node failure breaks the ring.

**Star**: one root node forwards writes to all others. Also vulnerable to single-node failure at the root.

In circular and star topologies, each write is tagged with the IDs of all nodes it has passed through to prevent infinite replication loops.

Even in all-to-all topologies, causality violations can occur: if link speeds vary, an update on node 3 may arrive at node 2 before the insert that created the row being updated. [[version-vectors]] can detect this; however, many multi-leader systems implement causal ordering poorly or not at all.

## Not linearizable

Multi-leader replication is **not linearizable**: writes are processed concurrently on multiple nodes and replicated asynchronously, producing conflicts that require resolution. This is an inherent artifact of having no single copy of the data. (source: designing-data-intensive-applications, chapter 9)

The claim is categorical rather than hedged: concurrent writes accepted at different leaders are, by definition, not linearizable unless they are serialised through a single point — and serialising through a single point is just single-leader replication. There is no "sometimes linearizable" multi-leader configuration. This is why the claim here is stronger than the "*probably* not linearizable" framing on [[leaderless-replication]]: a leaderless system with strict quorums at least *appears* linearizable until you examine the race conditions, whereas multi-leader is non-linearizable by construction.

However, multi-leader systems gain a significant advantage in the [[cap-theorem]] trade-off: during a network partition between datacenters, each datacenter can continue operating normally because writes are asynchronously queued and exchanged when connectivity is restored. A single-leader system would make the follower datacenter unavailable for writes and linearizable reads during the same partition. (source: designing-data-intensive-applications, chapter 9)

Multi-leader and leaderless systems do not use global [[consensus]]. The conflicts that arise are a consequence of this design choice -- but for many use cases, the availability and performance benefits outweigh the consistency trade-off. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[replication]]
- [[leader-based-replication]]
- [[write-conflicts]]
- [[leaderless-replication]]
- [[consistent-prefix-reads]]
- [[version-vectors]]
- [[eventual-consistency]]
- [[linearizability]]
- [[cap-theorem]]
- [[consensus]]
