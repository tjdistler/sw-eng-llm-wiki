# Consensus

**Summary**: The fundamental problem of getting multiple nodes in a distributed system to agree on a value, despite node crashes and network faults -- equivalent to [[total-order-broadcast]], [[linearizability|linearizable compare-and-set]], and atomic commit, and solvable by algorithms such as Paxos, Raft, and Zab.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## The problem

Informally, consensus means getting several nodes to agree on something. This arises in many critical situations (source: designing-data-intensive-applications, chapter 9):

- **Leader election**: all nodes must agree which node is the leader to avoid split-brain in [[leader-based-replication]].
- **Atomic commit**: in a [[distributed-transactions|distributed transaction]], all nodes must agree whether to commit or abort.
- **Uniqueness constraints**: when concurrent requests try to claim the same resource, the system must decide a winner.
- **Lock acquisition**: only one client should hold a distributed lock at a time.

## Formal properties

A consensus algorithm must satisfy four properties (source: designing-data-intensive-applications, chapter 9):

1. **Uniform agreement**: no two nodes decide differently.
2. **Integrity**: no node decides twice.
3. **Validity**: if a node decides value v, then v was proposed by some node (ruling out trivial solutions like always deciding null).
4. **Termination**: every node that does not crash eventually decides some value (the liveness/fault-tolerance property).

The first three are safety properties (always hold, even during total failure). Termination is a liveness property that requires at least a **majority of nodes** to be functioning. (source: designing-data-intensive-applications, chapter 9)

## The FLP impossibility result

The FLP result (Fischer, Lynch, Paterson) proves that no deterministic algorithm can always reach consensus in an asynchronous system where nodes may crash. However, this result assumes no clocks or timeouts. In practice, consensus is achievable by using timeouts to detect suspected failures, or by using randomization. (source: designing-data-intensive-applications, chapter 9)

## Major algorithms

The best-known fault-tolerant consensus algorithms are (source: designing-data-intensive-applications, chapter 9):

- **Paxos** (and Multi-Paxos for sequences of values)
- **Raft** (used by etcd)
- **Zab** (used by [[zookeeper]])
- **Viewstamped Replication (VSR)**

In practice, these algorithms decide on a **sequence of values** rather than a single value, making them [[total-order-broadcast]] algorithms. Each round of consensus corresponds to one message delivery in the total order. (source: designing-data-intensive-applications, chapter 9)

## How consensus algorithms work: epoch numbering and quorums

All major consensus protocols use a leader internally, but with safeguards (source: designing-data-intensive-applications, chapter 9):

1. **Epoch numbers**: each leadership period has a unique, monotonically increasing epoch number (called ballot number in Paxos, view number in VSR, term number in Raft).
2. **Two rounds of voting**: one vote to elect a leader, another to vote on the leader's proposals.
3. **Quorum overlap**: the quorums for leader election and proposal voting must overlap, ensuring any proposal vote can detect if a newer leader has been elected.

Key differences from [[two-phase-commit]] (source: designing-data-intensive-applications, chapter 9):
- The coordinator/leader is elected, not fixed
- Only a majority vote is needed, not unanimity
- A recovery process ensures safety after leader changes

## Equivalence with other problems

A deep result: the following problems are all equivalent -- a solution to any one can be transformed into solutions for the others (source: designing-data-intensive-applications, chapter 9):

- Consensus
- [[total-order-broadcast]]
- [[linearizability|Linearizable compare-and-set]] registers
- Atomic transaction commit
- Locks and leases
- Membership/coordination services
- Uniqueness constraints

## Single-leader replication and consensus

[[leader-based-replication|Leader-based replication]] effectively implements total order broadcast (the replication log). But choosing and maintaining the leader requires consensus. If the leader is manually chosen by operators, the system does not satisfy the termination property (human intervention required). Automatic [[failover]] brings the system closer to fault-tolerant consensus, but correctly implementing leader election without split brain requires a consensus algorithm. (source: designing-data-intensive-applications, chapter 9)

## Limitations

Consensus is not free (source: designing-data-intensive-applications, chapter 9):

- **Performance**: proposal voting is essentially synchronous replication, adding latency.
- **Minimum nodes**: requires at least 3 nodes to tolerate 1 failure, or 5 to tolerate 2.
- **Network sensitivity**: during a partition, only the majority side can make progress. Frequent false leader elections due to network issues can degrade performance severely.
- **Fixed membership**: most algorithms assume a fixed set of voting nodes. Dynamic membership extensions exist but are less well understood.
- **Raft edge cases**: unreliable network links can cause continuous leadership bouncing between nodes.

In practice, systems outsource consensus to dedicated services like [[zookeeper]] or etcd rather than implementing it themselves. (source: designing-data-intensive-applications, chapter 9)

Burns is unusually blunt about this point in his applied container-level treatment: implementing Paxos or Raft yourself is "akin to implementing locks on top of assembly code compare-and-swap instructions. It's an interesting exercise for an undergraduate computer science course, but it is not something that is generally worth doing in practice." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md) His Chapter 9 builds the full [[ownership-election-pattern|ownership election pattern]] on etcd's compare-and-swap and TTL primitives alone, never touching the consensus layer itself.

## Consensus, uniqueness, and coordination avoidance

Chapter 12 expands on the relationship between consensus and uniqueness constraints. Enforcing strict uniqueness (usernames, seat bookings) requires consensus, typically via a single leader or partitioned log-based messaging. However, many applications can tolerate **loosely interpreted constraints**: allowing temporary violations and fixing them with compensating transactions (apologies, refunds). This [[coordination-avoidance]] approach achieves strong integrity without the performance and availability costs of consensus. Consensus and coordination remain necessary only for constraints where recovery from violation is impossible (source: chapter-12-the-future-of-data-systems.md).

## Scaling limitations

Most consensus algorithms are designed for situations where a single node's throughput can process the entire event stream. They do not provide a mechanism for multiple nodes to share the work of ordering events. Designing consensus algorithms that scale beyond a single node and work well in geographically distributed settings remains an open research problem (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[total-order-broadcast]]
- [[linearizability]]
- [[two-phase-commit]]
- [[distributed-transactions]]
- [[zookeeper]]
- [[leader-based-replication]]
- [[failover]]
- [[fault-tolerance]]
- [[cap-theorem]]
- [[coordination-avoidance]]
- [[data-integration]]
- [[unbundling-databases]]
- [[ownership-election-pattern]]
- [[distributed-locks-on-kv-stores]]
