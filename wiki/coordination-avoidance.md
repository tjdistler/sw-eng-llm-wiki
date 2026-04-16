# Coordination Avoidance

**Summary**: A design approach for data systems that maintains strong integrity guarantees without requiring synchronous cross-partition coordination (linearizability, distributed transactions), by combining asynchronous event processing with loosely interpreted constraints and compensating transactions.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## Two key observations

The case for coordination avoidance rests on two insights (source: chapter-12-the-future-of-data-systems.md):

1. **Dataflow systems can maintain integrity without atomic commit, [[linearizability]], or synchronous cross-partition coordination.** Using end-to-end operation IDs, deterministic derivation, and [[exactly-once-semantics|idempotent processing]], [[derived-data|derived data]] stays correct even with asynchronous processing.

2. **Many applications tolerate loose constraints.** Strict uniqueness requires [[timeliness-and-integrity|timeliness]] and coordination, but many real-world business processes accept temporary violations followed by compensating transactions (apologies, refunds, reordering stock).

## What coordination avoidance enables

Coordination-avoiding data systems achieve better performance and [[fault-tolerance]] than systems requiring synchronous coordination (source: chapter-12-the-future-of-data-systems.md):

- **Multi-datacenter operation** in a [[multi-leader-replication|multi-leader]] configuration with asynchronous cross-region replication.
- **Each datacenter operates independently** -- no synchronous cross-region coordination required.
- **Weak timeliness guarantees** (not linearizable), but **strong integrity guarantees** (no data loss or corruption).

## Where coordination is still needed

Synchronous coordination can be introduced selectively for strict constraints where recovery from a violation is not possible (e.g., ensuring a financial settlement is irreversible). But most of the application need not pay the cost of coordination. Serializable [[transactions]] remain useful for maintaining [[derived-data|derived state]] at a small scope (source: chapter-12-the-future-of-data-systems.md).

Heterogeneous [[distributed-transactions]] (XA) are not required. Within a single storage or [[stream-processing]] system, transactions work well. Across system boundaries, asynchronous event logs with [[exactly-once-semantics|idempotent consumers]] are more robust (source: chapter-12-the-future-of-data-systems.md).

## Uniqueness via log-based messaging

Where uniqueness constraints are needed, they can be enforced through log-based messaging without distributed transactions (source: chapter-12-the-future-of-data-systems.md):

1. Partition the log by the value that must be unique (e.g., hash of username).
2. A stream processor reads requests sequentially on a single thread per partition.
3. It maintains a local database of claimed values and emits success or rejection messages.
4. The client watches the output stream for its result.

This is essentially the algorithm for [[linearizability|implementing linearizable storage]] using [[total-order-broadcast]], and scales by increasing the number of partitions (source: chapter-12-the-future-of-data-systems.md).

## The trade-off

Coordination reduces apologies for inconsistencies but may increase apologies for outages. The goal is the sweet spot: neither too many inconsistencies nor too many availability problems (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[timeliness-and-integrity]]
- [[exactly-once-semantics]]
- [[end-to-end-argument]]
- [[derived-data]]
- [[linearizability]]
- [[distributed-transactions]]
- [[total-order-broadcast]]
- [[consensus]]
- [[fault-tolerance]]
- [[multi-leader-replication]]
- [[event-sourcing]]
