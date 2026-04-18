# Consensus Replica Placement

**Summary**: Chapter 23's framing of where to put consensus replicas, as a trade-off between **failure domains** a single failure can take out and **latency** between replicas. As geographic distance between replicas increases, both the failure size the system survives *and* the latency of operations increase. The right answer is workload-dependent and bounded by the location of the clients — there is no value in surviving a disaster that takes out all your clients too.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Failure domains

A **failure domain** is the set of components that can become unavailable as a result of a single failure. Chapter 23's examples, ordered by size (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- A physical machine
- A rack in a datacenter served by a single power supply
- Several racks served by one piece of networking equipment
- A datacenter that could be rendered unavailable by a fibre cut
- A set of datacenters in a single geographic area that could all be affected by a natural disaster

Spreading replicas across larger failure domains lets the system survive larger outages, at the cost of higher RTT between replicas and therefore higher consensus-operation latency.

## The latency-vs-failure-size trade-off

For most consensus systems, increasing RTT between replicas increases operation latency. The extent to which latency matters is workload-dependent:

- **A consensus system that provides group membership and leader election for another service** probably isn't heavily loaded. If the consensus transaction time is only a fraction of the leader-lease time, its performance isn't critical (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).
- **Batch-oriented systems** can increase batch size to increase throughput at the cost of latency — so latency matters less.
- **Latency-sensitive online workloads** need careful placement; every replica hop is on the critical path.

## The upper bound on geographic spread

Chapter 23 makes a pointed observation about how *not* to over-engineer placement:

> It doesn't always make sense to continually increase the size of the failure domain whose loss the system can withstand. For instance, if all of the clients using a consensus system are running within a particular failure domain (say, the New York area) and deploying a distributed consensus–based system across a wider geographical area would allow it to remain serving during outages in that failure domain (say, Hurricane Sandy), is it worth it? Probably not, because the system's clients will be down as well so the system will see no traffic.

(source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md)

The rule: a consensus system should not be more geographically robust than its clients need it to be. Extra cost in latency, throughput, and computing resources with no benefit.

## Disaster recovery and backups

Chapter 23 points out two failure domains you can **never escape** regardless of replica placement (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **The software itself** — bugs can emerge under unusual circumstances and cause data loss.
- **Human error** on the part of administrators — misconfiguration, sabotage, and ordinary mistakes.

This is why **regular snapshot backups** are critical even for solid consensus-based systems deployed across diverse failure domains. The consensus replicas are essentially online copies; backups are what protect against the two unescapable failure modes.

## Client-perceived latency as the metric

Chapter 23's summary rule: "the most important measure of performance is client perception: ideally, the network round-trip time from the clients to the consensus system's replicas should be minimized" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Over wide-area networks with clients spread geographically and replicas near them, [[mencius-epaxos|leaderless protocols]] like Mencius or Egalitarian Paxos may have a performance edge — particularly if application consistency constraints permit read-only operations on any replica without a consensus round.

## Cross-book framing

- [[google-datacenter-topology]] — the machine/rack/row/cluster/building/campus hierarchy gives names to Chapter 23's failure-domain levels
- [[anycast-dns]] — geographic replica placement's analogue at the DNS layer; same principle, different layer
- [[edm-deployment-patterns]] (Bellemare) — similar trade-offs for event-driven-microservice deployments
- [[cross-cluster-replication]] (Bellemare) — Kafka MirrorMaker between regions is the event-log analogue of cross-datacenter consensus-replica placement

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[consensus-replica-count]]
- [[quorum-composition]]
- [[hierarchical-quorums]]
- [[consensus-performance]]
- [[mencius-epaxos]]
