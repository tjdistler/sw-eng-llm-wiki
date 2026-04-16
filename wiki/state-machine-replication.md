# State Machine Replication

**Summary**: A principle stating that if every replica processes the same sequence of deterministic operations in the same order, all replicas will remain consistent -- the theoretical foundation for [[total-order-broadcast]] and database replication.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-15

---

## The principle

If you model each replica as a deterministic state machine (given the same input, it always produces the same output), then feeding every replica the same sequence of inputs in the same order guarantees they remain in identical states. (source: designing-data-intensive-applications, chapter 9)

This is exactly what [[total-order-broadcast]] provides: every message (representing a write or deterministic transaction) is delivered to every node in the same order. (source: designing-data-intensive-applications, chapter 9)

## Applications

**Database replication**: the replication log in [[leader-based-replication]] is an instance of state machine replication. The leader determines the order; followers apply writes in that order and converge to the same state. (source: designing-data-intensive-applications, chapter 9)

**Serializable transactions**: if each message represents a deterministic stored procedure, and every node processes them in the same total order, partitions and replicas stay consistent. This connects state machine replication to [[serializability]] via [[actual-serial-execution]]. (source: designing-data-intensive-applications, chapter 9)

**Consensus-based systems**: [[zookeeper]], etcd, and other [[consensus]]-based coordination services use state machine replication internally. The consensus algorithm ensures all nodes agree on the sequence of operations. (source: designing-data-intensive-applications, chapter 9)

## Requirements

For state machine replication to work, operations must be **deterministic**: the same operation applied to the same state must always produce the same result. Non-deterministic operations (using current time, random numbers, external calls) must be handled specially -- typically by having the leader determine the result and replicating that result rather than the operation itself. (source: designing-data-intensive-applications, chapter 9)

## Connection to event streams

Chapter 11 reinforces that state machine replication is just another case of event streams. A [[replication]] log is a stream of database write events; if every replica processes the same events in the same order, they converge to the same state. This principle underlies both [[change-data-capture]] (where the source database is the leader and derived systems are followers processing its change stream) and [[event-sourcing]] (where the application explicitly writes to an append-only event log and derives state by replaying it) (source: chapter-11-stream-processing.md).

## Related pages

- [[total-order-broadcast]]
- [[consensus]]
- [[leader-based-replication]]
- [[replication]]
- [[serializability]]
- [[zookeeper]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[stream-processing]]
