# Causal Consistency

**Summary**: A consistency model that preserves the ordering of causally related operations (cause always comes before effect) while allowing concurrent operations to be processed in any order -- weaker than [[linearizability]] but stronger than [[eventual-consistency]], and the strongest model that does not require coordination.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## What causality means in distributed systems

Two operations are causally related when one depends on or could have been influenced by the other. If operation A happened before operation B (B could have known about A), then they are causally ordered: A must be visible before B. If neither could have known about the other, they are concurrent and can be ordered arbitrarily. (source: designing-data-intensive-applications, chapter 9)

Examples of causal dependencies throughout the book (source: designing-data-intensive-applications, chapter 9):

- A question must exist before its answer ([[consistent-prefix-reads]])
- A row must be created before it can be updated
- In [[snapshot-isolation]], a snapshot must include causes of any effects it shows
- In [[write-skew]], the decision to go off-call depends on observing who is currently on call
- In [[linearizability]] violations, hearing Alice announce a result causally depends on the result being decided

## Causal order is a partial order

Unlike [[linearizability]], which imposes a **total order** (every pair of operations is ordered), causality imposes a **partial order**: some operations are ordered relative to each other (causally related), while others are incomparable (concurrent). (source: designing-data-intensive-applications, chapter 9)

This is analogous to version histories in Git: commits usually form a sequence, but branches represent concurrent work, and merges combine them. (source: designing-data-intensive-applications, chapter 9)

## Relationship to linearizability

[[Linearizability]] implies causal consistency: any linearizable system automatically preserves causality. But the converse is not true -- causal consistency is strictly weaker. (source: designing-data-intensive-applications, chapter 9)

The critical advantage of causal consistency: it is the **strongest possible consistency model that does not slow down due to network delays and remains available in the face of network failures**. The [[cap-theorem]] does not apply to causal consistency. Many systems that appear to require linearizability actually only need causal consistency, which can be implemented more efficiently. (source: designing-data-intensive-applications, chapter 9)

## Capturing causal dependencies

To maintain causal consistency, the system must know which operation happened before which. Techniques include (source: designing-data-intensive-applications, chapter 9):

- **[[version-vectors]]**: originally used for detecting concurrent writes to the same key in [[leaderless-replication]], but can be generalized to track causal dependencies across the entire database.
- **[[lamport-timestamps]]**: sequence numbers that provide a total order consistent with causality, though they cannot distinguish causally related from concurrent operations.
- **Passing version numbers with reads/writes**: the database tracks which version of data was read by a transaction, so it can determine causal order.

The approach used in [[serializable-snapshot-isolation]] is related: SSI detects causal dependencies between transactions by tracking which data each transaction has read. (source: designing-data-intensive-applications, chapter 9)

## Limitations

While causal consistency can determine which operations depend on which after the fact, it cannot solve problems that require real-time decisions about uniqueness or ordering. For example, enforcing a uniqueness constraint (like unique usernames) requires knowing at decision time that no other node is concurrently performing the same operation -- this needs [[total-order-broadcast]] or [[consensus]], not just causal ordering. (source: designing-data-intensive-applications, chapter 9)

## Current state

Researchers are actively exploring databases that preserve causality with performance and availability characteristics similar to [[eventual-consistency]]. As of writing, this research has not yet made its way into mainstream production systems, but it is a promising direction. (source: designing-data-intensive-applications, chapter 9)

## Capturing causality in practice

Chapter 12 revisits the problem of causal ordering when total order is infeasible. Subtle cross-system causal dependencies can arise -- for example, a social network user unfriends someone and then sends a message to remaining friends; if the unfriend and message events are stored in different systems, a notification service might process them out of order and deliver the message to the ex-friend (source: chapter-12-the-future-of-data-systems.md).

Starting points for handling such cross-system causality (source: chapter-12-the-future-of-data-systems.md):

- **[[lamport-timestamps]]** provide total ordering without coordination, but recipients must handle out-of-order events and additional metadata is required.
- **Logging the user's observed state** before a decision, with a unique identifier that later events can reference, explicitly records the causal dependency.
- **Conflict resolution algorithms** (see [[write-conflicts]]) help maintain state consistency, but cannot undo external side effects like sent notifications.

Efficient patterns for capturing causal dependencies without bottlenecking everything through [[total-order-broadcast]] remain an open area of research and development.

## Related pages

- [[linearizability]]
- [[eventual-consistency]]
- [[consistent-prefix-reads]]
- [[version-vectors]]
- [[lamport-timestamps]]
- [[total-order-broadcast]]
- [[snapshot-isolation]]
- [[write-skew]]
- [[cap-theorem]]
- [[data-integration]]
- [[write-conflicts]]
