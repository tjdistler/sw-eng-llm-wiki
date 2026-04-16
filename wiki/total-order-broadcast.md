# Total Order Broadcast

**Summary**: A protocol for exchanging messages between nodes that guarantees reliable delivery (no messages lost) and totally ordered delivery (all nodes receive messages in the same order) -- equivalent to [[consensus]] and the foundation for database replication, serializable transactions, and linearizable storage.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## Definition

Total order broadcast (also called atomic broadcast) is a protocol with two safety properties that must always be satisfied, even under faults (source: designing-data-intensive-applications, chapter 9):

1. **Reliable delivery**: if a message is delivered to one node, it is delivered to all nodes.
2. **Totally ordered delivery**: messages are delivered to every node in the same order.

The order is fixed at delivery time -- a node cannot retroactively insert a message into an earlier position if subsequent messages have already been delivered. This makes total order broadcast stronger than [[lamport-timestamps]], which only provide an after-the-fact ordering. (source: designing-data-intensive-applications, chapter 9)

Note: "atomic broadcast" has nothing to do with atomicity in [[acid]] transactions. It is also called total order multicast. (source: designing-data-intensive-applications, chapter 9)

## Scope of ordering

Partitioned databases with a single leader per partition often maintain ordering only per partition. Total ordering across all partitions is possible but requires additional coordination. (source: designing-data-intensive-applications, chapter 9)

## Uses

**Database replication ([[state-machine-replication]])**: if every message represents a write, and every replica processes writes in the same order, replicas stay consistent. This is exactly what [[leader-based-replication]] logs provide. (source: designing-data-intensive-applications, chapter 9)

**Serializable transactions**: if every message is a deterministic transaction (stored procedure), processing them in the same order on all nodes keeps partitions and replicas consistent. (source: designing-data-intensive-applications, chapter 9)

**Log-based systems**: total order broadcast is equivalent to creating a log (replication log, transaction log, or write-ahead log). Delivering a message is like appending to the log. All nodes see the same sequence. (source: designing-data-intensive-applications, chapter 9)

**Fencing tokens**: a lock service can use total order broadcast to assign monotonically increasing sequence numbers as fencing tokens. In [[zookeeper]], this is the zxid. (source: designing-data-intensive-applications, chapter 9)

## Building linearizable storage from total order broadcast

Total order broadcast is asynchronous (no guarantee about when a message arrives), while [[linearizability]] is a recency guarantee. They are not the same, but total order broadcast can be used to implement linearizable storage. (source: designing-data-intensive-applications, chapter 9)

Algorithm for a linearizable compare-and-set (e.g., unique username):

1. Append a message to the log, tentatively claiming the username.
2. Read the log and wait for your message to be delivered back.
3. If your message is the first claim for that username, the operation succeeds. Otherwise, abort.

This provides linearizable writes. For linearizable reads, three options (source: designing-data-intensive-applications, chapter 9):

- **Sequence reads through the log**: append a read message, wait for it to be delivered, then read. The message position defines the read's point in time (etcd quorum reads work this way).
- **Query the latest log position**: fetch the position in a linearizable way, wait for all entries up to that position, then read (ZooKeeper's sync() operation).
- **Read from a synchronously updated replica**: guaranteed to be up to date (chain replication).

Without these measures, reading from an asynchronously updated store provides only **sequential consistency** (also called timeline consistency), which is slightly weaker than linearizability. (source: designing-data-intensive-applications, chapter 9)

## Building total order broadcast from linearizable storage

The reverse construction also works: if you have a linearizable register with an atomic increment-and-get operation, you can build total order broadcast by assigning each message a sequence number from the register and delivering messages consecutively. (source: designing-data-intensive-applications, chapter 9)

Unlike [[lamport-timestamps]], these sequence numbers have **no gaps**: if a node has delivered message 4 and receives message 6, it knows it must wait for message 5. This gap-free property is what distinguishes total order broadcast from simple timestamp ordering. (source: designing-data-intensive-applications, chapter 9)

## Equivalence with consensus

Total order broadcast and [[consensus]] are formally equivalent: a solution to one can be transformed into a solution for the other. Similarly, a linearizable compare-and-set register is equivalent to consensus. This deep result means that all three problems -- consensus, total order broadcast, and linearizable compare-and-set -- are fundamentally the same problem. (source: designing-data-intensive-applications, chapter 9)

## Limits of total ordering at scale

Constructing a totally ordered log is feasible for small systems (as demonstrated by the popularity of [[leader-based-replication]]), but hits limits as systems grow (source: chapter-12-the-future-of-data-systems.md):

- **Throughput ceiling**: all events must pass through a single leader that decides ordering. If throughput exceeds one machine's capacity, the log must be partitioned, making cross-partition ordering ambiguous.
- **Geographic distribution**: separate leaders per datacenter mean undefined ordering between datacenters (see [[multi-leader-replication]]).
- **Microservices**: independent services with separate durable state have no defined cross-service ordering.
- **Offline clients**: client-side state updated without server confirmation creates divergent orderings.

Designing consensus algorithms that scale beyond a single node's throughput and work well across geographic distances remains an open research problem (source: chapter-12-the-future-of-data-systems.md).

## Enforcing uniqueness via log-based messaging

In [[unbundling-databases|unbundled database]] architectures, total order broadcast can enforce uniqueness constraints without [[distributed-transactions]]. The approach: partition the log by the value that must be unique, have a stream processor read requests sequentially per partition, and emit success/rejection messages. This is the same algorithm as building [[linearizability|linearizable storage]] from total order broadcast, and scales by adding partitions (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[consensus]]
- [[linearizability]]
- [[lamport-timestamps]]
- [[state-machine-replication]]
- [[leader-based-replication]]
- [[zookeeper]]
- [[causal-consistency]]
- [[data-integration]]
- [[unbundling-databases]]
- [[coordination-avoidance]]
- [[multi-leader-replication]]
