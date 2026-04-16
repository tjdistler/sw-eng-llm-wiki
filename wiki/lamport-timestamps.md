# Lamport Timestamps

**Summary**: A simple algorithm for generating sequence numbers that provide a total ordering of operations consistent with causality, proposed by Leslie Lamport in 1978 -- one of the most-cited papers in distributed systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## How they work

A Lamport timestamp is a pair of (counter, node ID). Each node maintains its own counter, incrementing it for every operation. The node ID breaks ties when two nodes have the same counter value, ensuring every timestamp is globally unique. (source: designing-data-intensive-applications, chapter 9)

Ordering rule: compare counter values first; the larger counter is the later operation. If counters are equal, the larger node ID wins. (source: designing-data-intensive-applications, chapter 9)

## The key mechanism

What makes Lamport timestamps consistent with causality (unlike naive per-node counters): every node and every client keeps track of the **maximum counter value** it has seen so far, and includes that maximum on every request. When a node receives a request or response with a counter value greater than its own, it immediately advances its own counter to that maximum. (source: designing-data-intensive-applications, chapter 9)

This ensures that every causal dependency results in an increased timestamp: if operation A causally precedes B, then A's timestamp is always lower than B's. (source: designing-data-intensive-applications, chapter 9)

## Why naive alternatives fail

Without the piggyback-the-maximum mechanism, several simpler approaches fail to preserve causality (source: designing-data-intensive-applications, chapter 9):

- **Per-node counters (odd/even)**: nodes process operations at different rates, so the counters diverge and ordering is inconsistent with causality.
- **Physical clock timestamps**: subject to clock skew; a causally later event can receive a lower timestamp.
- **Block-allocated sequence numbers**: a causally later operation can receive a number from a lower block than an earlier operation.

## Lamport timestamps vs version vectors

Lamport timestamps and [[version-vectors]] serve different purposes despite surface similarities (source: designing-data-intensive-applications, chapter 9):

| Property | Lamport timestamps | [[version-vectors]] |
|---|---|---|
| Provides | Total order | Partial order |
| Can detect concurrency | No | Yes |
| Size | Compact (counter + node ID) | One counter per replica |

Version vectors can distinguish whether two operations are concurrent or causally dependent. Lamport timestamps impose a total order but cannot tell you whether two operations were concurrent -- they may just happen to have adjacent timestamps.

## Limitations: total order is not enough

Lamport timestamps provide a total order consistent with causality, but this is insufficient for many practical problems. The ordering only becomes apparent **after the fact** -- when you have collected all operations and can compare their timestamps. (source: designing-data-intensive-applications, chapter 9)

For a problem like enforcing username uniqueness: when a node receives a registration request, it cannot know in real time whether another node is concurrently processing a registration for the same username with a lower timestamp. You would need to check with every other node, and if any node is unreachable, the system stalls. (source: designing-data-intensive-applications, chapter 9)

This limitation is what motivates [[total-order-broadcast]]: you need to know not just the order, but **when the order is finalized**. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[causal-consistency]]
- [[total-order-broadcast]]
- [[version-vectors]]
- [[consensus]]
- [[linearizability]]
