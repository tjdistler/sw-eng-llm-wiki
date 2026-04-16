# Linearizability

**Summary**: The strongest single-object consistency model, making a distributed system appear as if there is only one copy of the data and all operations on it are atomic -- also known as atomic consistency, strong consistency, immediate consistency, or external consistency.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## The core idea

Linearizability is a recency guarantee: once a write has completed successfully, all subsequent reads (from any client) must return that value or a later one. The system behaves as though there is a single copy of the data, and every operation takes effect atomically at some point between its invocation and its response. (source: designing-data-intensive-applications, chapter 9)

In a linearizable system, as soon as one client successfully completes a write, all clients reading from the database must be able to see the value just written. There is no stale data visible after a write completes. (source: designing-data-intensive-applications, chapter 9)

## Formal definition

Operations in a linearizable system can be modeled on a timeline. For any two operations:

- If operation A completes before operation B starts, then B must see A's effect.
- If A and B are concurrent (overlapping in time), B may or may not see A's effect -- but once any read returns the new value, all subsequent reads must also return the new value. (source: designing-data-intensive-applications, chapter 9)

The key constraint: there must be a point in time (between invocation and response) at which each operation appears to take effect atomically. These points must form a valid sequential order that moves forward in time, never backward. (source: designing-data-intensive-applications, chapter 9)

## Linearizability vs serializability

These are often confused but are fundamentally different guarantees (source: designing-data-intensive-applications, chapter 9):

| Property | [[serializability]] | Linearizability |
|---|---|---|
| Scope | Multi-object transactions | Single object (register) |
| Guarantee | Transactions behave as if serial | Reads reflect most recent write |
| Type | Isolation property | Consistency (recency) property |

A database can provide both: this combination is called **strict serializability** (or strong one-copy serializability). [[two-phase-locking]] and [[actual-serial-execution]] are typically linearizable. [[serializable-snapshot-isolation]] is NOT linearizable because it reads from a consistent snapshot that intentionally excludes recent writes. (source: designing-data-intensive-applications, chapter 9)

## When linearizability is needed

**Locking and leader election**: Systems using [[leader-based-replication]] need all nodes to agree on who holds the lock or leadership. Coordination services like [[zookeeper]] use [[consensus]] algorithms to provide linearizable operations for this purpose. (source: designing-data-intensive-applications, chapter 9)

**Uniqueness constraints**: Enforcing that a username, filename, or other identifier is unique requires linearizability -- it is equivalent to acquiring a lock or performing an atomic compare-and-set. (source: designing-data-intensive-applications, chapter 9)

**Cross-channel timing dependencies**: When a system has multiple communication channels (e.g., a file store and a message queue), linearizability prevents race conditions between them. Without it, a message about a file could be processed before the file is visible on all replicas. (source: designing-data-intensive-applications, chapter 9)

## Implementing linearizable systems

The achievability of linearizability depends on the replication architecture (source: designing-data-intensive-applications, chapter 9):

| Architecture | Linearizable? | Notes |
|---|---|---|
| [[leader-based-replication]] | Potentially | Only if reads go to the leader or synchronous followers; violated by snapshot isolation or concurrency bugs |
| [[consensus]] algorithms | Yes | ZooKeeper, etcd use consensus for safe linearizable storage |
| [[multi-leader-replication]] | No | Concurrent writes on multiple nodes with async replication |
| [[leaderless-replication]] | Probably not | Even strict [[quorums]] can be nonlinearizable due to race conditions |

For leaderless systems: although strict quorums (w + r > n) seem like they should guarantee linearizability, variable network delays allow race conditions where one client reads the new value while a concurrent client reads the old value. Making quorums linearizable requires synchronous read repair before returning results, plus the writer reading quorum state before writing -- and even then, compare-and-set requires [[consensus]]. (source: designing-data-intensive-applications, chapter 9)

## The cost of linearizability

The [[cap-theorem]] captures a fundamental trade-off: when a network partition occurs, a system must choose between linearizability (consistency) and availability. If some replicas are disconnected, linearizable systems must make those replicas unavailable; non-linearizable systems can keep serving requests from disconnected replicas. (source: designing-data-intensive-applications, chapter 9)

However, the real reason most systems forgo linearizability is **performance**, not fault tolerance. Even modern multi-core CPUs do not provide linearizable memory access by default (each core has its own cache). Attiya and Welch proved that linearizable read/write response times must be at least proportional to network delay uncertainty. Weaker consistency models can be much faster. (source: designing-data-intensive-applications, chapter 9)

## Relationship to causality

Linearizability implies [[causal-consistency]]: a linearizable system automatically preserves causality because it imposes a total order on all operations. However, linearizability is stronger than necessary for preserving causality. [[causal-consistency]] is the strongest consistency model that does not require coordination (and thus does not suffer the performance penalties or availability limits of linearizability). (source: designing-data-intensive-applications, chapter 9)

## Linearizability as timeliness

Chapter 12 reframes linearizability as a **[[timeliness-and-integrity|timeliness]]** guarantee: it ensures users observe up-to-date state. This is distinct from **integrity** (absence of corruption). ACID transactions bundle both, but event-based dataflow systems can provide integrity without linearizability, achieving better performance and fault tolerance. Many applications that seem to require linearizability actually only need integrity -- they can tolerate temporary staleness and enforce constraints asynchronously via [[coordination-avoidance]] (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[causal-consistency]]
- [[cap-theorem]]
- [[consensus]]
- [[total-order-broadcast]]
- [[serializability]]
- [[eventual-consistency]]
- [[quorums]]
- [[leader-based-replication]]
- [[zookeeper]]
- [[two-phase-commit]]
- [[timeliness-and-integrity]]
- [[coordination-avoidance]]
