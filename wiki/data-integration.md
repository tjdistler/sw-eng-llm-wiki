# Data Integration

**Summary**: The challenge of making data available in the right form across all the different systems that need it, by combining specialized tools through batch and stream processing rather than relying on a single general-purpose database.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## The problem

No single tool can efficiently serve all possible use cases. Applications inevitably combine several different pieces of software (OLTP databases, search indexes, caches, analytics systems, ML models) to provide their functionality. The challenge is keeping all of these systems in sync as data changes (source: chapter-12-the-future-of-data-systems.md).

Data integration is often invisible when you look at a single team or service, but becomes apparent when you zoom out and consider dataflows across an entire organization (source: chapter-12-the-future-of-data-systems.md).

## Reasoning about dataflows

When the same data must live in several storage systems to satisfy different access patterns, clarity about inputs and outputs is essential (source: chapter-12-the-future-of-data-systems.md):

- **Where is data written first?** Identify the system of record.
- **Which representations are derived from which sources?** For example, a search index derived from a database via [[change-data-capture]].
- **How does data flow into all the right places, in the right formats?**

If you funnel all user input through a single system that decides on an ordering for all writes, it becomes much easier to derive other representations by processing writes in the same order. This is an application of [[state-machine-replication]] and [[total-order-broadcast]] (source: chapter-12-the-future-of-data-systems.md).

## Derived data vs distributed transactions

Two approaches to keeping different data systems consistent (source: chapter-12-the-future-of-data-systems.md):

| Approach | Ordering mechanism | Atomicity mechanism | Timeliness |
|---|---|---|---|
| [[distributed-transactions]] | Locks for mutual exclusion | Atomic commit (2PC) | [[linearizability]] (synchronous) |
| Log-based [[derived-data]] | Event log ordering | Deterministic retry + idempotence | Asynchronous (eventual) |

Distributed transactions (especially [[two-phase-commit|XA]]) have poor fault tolerance and performance. Log-based derived data is more promising for integrating heterogeneous systems, though it sacrifices immediate consistency. See [[timeliness-and-integrity]] for how to reason about this trade-off (source: chapter-12-the-future-of-data-systems.md).

## Limits of total ordering

Constructing a [[total-order-broadcast|totally ordered event log]] is feasible for small systems but hits limits at scale (source: chapter-12-the-future-of-data-systems.md):

- **Throughput**: a single leader node deciding order cannot handle unlimited event throughput; partitioning introduces ambiguous cross-partition ordering.
- **Geographic distribution**: separate leaders per datacenter mean undefined ordering between datacenters.
- **Microservices**: independent services with no shared durable state have no defined cross-service ordering.
- **Offline-capable clients**: clients and servers see events in different orders.

Designing [[consensus]] algorithms that scale beyond a single node's throughput and work across geographic distances remains an open research problem (source: chapter-12-the-future-of-data-systems.md).

## Capturing causality without total order

When there is no causal link between events, lack of total order is fine -- concurrent events can be ordered arbitrarily. But causal dependencies sometimes arise subtly across different subsystems. Approaches include (source: chapter-12-the-future-of-data-systems.md):

- **[[lamport-timestamps]]** for total ordering without coordination (but recipients must handle out-of-order delivery).
- **Logging the state the user saw** before making a decision, so later events can reference that observation via a unique identifier.
- **Conflict resolution algorithms** (see [[write-conflicts]]) for maintaining state, though they don't help with external side effects.

See [[causal-consistency]] for the underlying theory.

## Batch and stream as integration tools

[[batch-processing|Batch]] and [[stream-processing]] are the primary tools for data integration. Their outputs are [[derived-data|derived datasets]]: search indexes, materialized views, ML models, aggregate metrics. The two are converging -- Spark performs stream processing via microbatching, while Flink performs batch on top of a stream engine (source: chapter-12-the-future-of-data-systems.md).

See [[lambda-architecture]] for a historical approach to combining batch and stream, and its successor: unified batch/stream processing.

## Related pages

- [[derived-data]]
- [[unbundling-databases]]
- [[lambda-architecture]]
- [[total-order-broadcast]]
- [[consensus]]
- [[distributed-transactions]]
- [[batch-processing]]
- [[stream-processing]]
- [[causal-consistency]]
- [[change-data-capture]]
- [[state-machine-replication]]
