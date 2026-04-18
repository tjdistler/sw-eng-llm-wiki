# Reliable Distributed Queue

**Summary**: A distributed queue implemented as a [[replicated-state-machine]] over a [[consensus]] algorithm, so the queue itself tolerates failure of individual nodes. Chapter 23's core point: naive queue implementations have the queue as a single point of failure; implementing the queue as an RSM makes the whole system robust. Closely related to [[atomic-broadcast]] (Chandra-Toueg equivalence) and natively supported by systems like Kafka.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The problem

Queues are a common structure for distributing tasks between worker processes. Queuing-based systems tolerate worker failure naturally — another worker picks up what a failed worker didn't complete. But the queue itself is structurally the single point of failure: "loss of the queue prevents the entire system from operating" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## The RSM answer

Implementing the queue as an RSM "can minimize the risk, and make the entire system far more robust" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Every enqueue and dequeue goes through the consensus protocol; the queue state is replicated across participants; individual node failures don't take the queue down.

## Leases, not removals

Chapter 23's operational guidance: the system must ensure claimed tasks are **successfully processed**. For that, use a **lease system** (as with distributed locks) rather than outright removal from the queue. If the worker holding the lease crashes, the lease expires and another worker can claim the task (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is the same pattern as [[renewable-leases]] in Burns's ownership-election terminology and [[distributed-locks-on-kv-stores]] in his applied treatment: TTL plus compare-and-swap plus a version / fencing token.

## Two usage shapes

Chapter 23 distinguishes two common shapes (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Queue as work distribution** — point-to-point. A pool of workers consumes tasks from a shared queue. This is a load-balancing device as much as a queue, and is the shape Burns documents as the [[work-queue-pattern]].
- **Publish-subscribe** — one-to-many. Messages consumed by many clients subscribed to a channel or topic; messages stored as a persistent ordered list. See [[atomic-broadcast]] and [[log-based-message-brokers]].

## Performance considerations

Queuing and messaging systems typically need excellent throughput but don't need extremely low latency (not usually directly user-facing). But "very high latencies in a system like the one just described, which has multiple workers claiming tasks from a queue, could become a problem if the percentage of processing time for each task grew significantly" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The batching and pipelining techniques on [[consensus-performance]] apply.

## Cross-book framing

The reliable distributed queue is the consensus-backed ancestor of every modern message broker. The wiki has extensive lower-level coverage:

- [[log-based-message-brokers]] (Kleppmann) — Kafka as the partitioned-append-only-log realisation; total ordering is per-partition
- [[event-broker]] (Bellemare) — the EDM-world name; Kafka and Pulsar are the concrete products
- [[message-brokers]] (Kleppmann) — the general message-broker treatment
- [[work-queue-pattern]] (Burns) — the container-level pattern built on top of a reliable queue
- [[atomic-broadcast]] — the theoretical equivalence; a reliable distributed queue is atomic broadcast with a particular API shape

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[replicated-state-machine]]
- [[atomic-broadcast]]
- [[log-based-message-brokers]]
- [[event-broker]]
- [[work-queue-pattern]]
- [[renewable-leases]]
- [[distributed-locks-on-kv-stores]]
