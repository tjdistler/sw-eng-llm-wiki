# Atomic Broadcast

**Summary**: A distributed-systems primitive in which messages are received **reliably and in the same order** by all participants. Chandra and Toueg (1996) proved atomic broadcast is equivalent to [[consensus]]: any atomic broadcast implementation solves consensus and vice versa. The primitive underpins publish-subscribe messaging, coherent distributed caches, and — at Kleppmann's naming — [[total-order-broadcast]].

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Definition

Chapter 23's phrasing: "Atomic broadcast is a distributed systems primitive in which messages are received reliably and in the same order by all participants. This is an incredibly powerful distributed systems concept and very useful in designing practical systems" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The two requirements are:

1. **Reliability** — every correct participant eventually receives every broadcast message.
2. **Total order** — every participant sees the messages in the same order.

The primitive is identical to what Kleppmann's DDIA calls [[total-order-broadcast]].

## Equivalence to consensus

Chandra and Toueg showed that atomic broadcast and consensus are equivalent: you can build either from the other (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This is the theoretical underpinning that lets the wiki treat a [[replicated-state-machine]], a consensus-based queue, and a totally-ordered log as implementations of the same fundamental capability — and justifies why production systems like Kafka, Zab-based ZooKeeper, and Raft-based etcd all cluster into the same design-pattern family.

## Use cases

Chapter 23's catalogue (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Publish-subscribe messaging** — messages consumed by many clients subscribed to a topic or channel; messages stored as a persistent ordered list. Not all pub-sub systems provide atomic guarantees, but those that do are implementing atomic broadcast.
- **Coherent distributed caches** — pub-sub of invalidation messages lets every cache see updates in the same order, keeping caches coherent without per-read consensus.
- **Reliable distributed queuing** — see [[reliable-distributed-queue]]; the queue's ordering property is atomic broadcast in a different guise.

## Cross-book framing

- [[total-order-broadcast]] (Kleppmann) — the same primitive under a different name; the Kleppmann page has more on the consensus-equivalence proof and on where it shows up in database replication.
- [[log-based-message-brokers]] (Kleppmann) — Kafka's append-only partitioned log is atomic broadcast packaged as a broker; total ordering is per-partition.
- [[event-broker]] (Bellemare) — the EDM-world name for the atomic-broadcast substrate services are built on.
- [[state-machine-replication]] / [[replicated-state-machine]] — the RSM consumes atomic broadcast as its input, producing replicated state as its output.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[total-order-broadcast]]
- [[replicated-state-machine]]
- [[reliable-distributed-queue]]
- [[log-based-message-brokers]]
- [[event-broker]]
- [[state-machine-replication]]
