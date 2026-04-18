# Stable Leader

**Summary**: A consensus-system design choice in which a single replica holds the leader role for as long as conditions allow, so the consensus protocol skips leader election on each operation. Adopted by [[multi-paxos|Multi-Paxos]], Zab ([[zookeeper|ZooKeeper]]), and Raft. Chapter 23's operational warning: stable leaders buy the best common-case latency but introduce three structural liabilities (non-local client latency, leader outgoing bandwidth, leader-machine performance) and a fourth mode failure around [[multi-paxos|dueling proposers]] on re-election.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why stable leaders

Almost all distributed consensus systems designed with performance in mind use either the **stable leader** pattern or a system of **rotating leadership** in which each numbered consensus round is pre-assigned to a replica (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The motivation for stability:

- **Message count minimisation.** Multi-Paxos reduces to a single round trip from proposer to a quorum of acceptors once a view has been established; this is optimal.
- **Read optimisation.** A stable leader has the most up-to-date state, so it can serve [[linearizability|linearizable]] reads directly.
- **Batching.** A single proposer can batch multiple client operations into one proposal — a major throughput lever, per [[consensus-performance]].

## The three liabilities

Chapter 23 lists three specific problems with stable leaders (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. **All state-changing operations go via the leader.** Clients not near the leader pay network latency on every write.
2. **Leader's outgoing network bandwidth is a system bottleneck.** The leader's Accept message contains all the proposal data; replies are tiny acknowledgements. On outgoing bandwidth this is asymmetric.
3. **Leader-machine performance dominates the cluster.** A leader on a machine with problems throttles everyone.

## Dueling proposers and leader election tuning

When a leader is suspected down, multiple replicas may race to become the new leader and interrupt each other's Prepare phases — the [[multi-paxos|dueling proposers]] livelock. Chapter 23 frames this as the **timeout tuning trade-off**: "the leader election process must be tuned carefully to balance the system unavailability that occurs when no leader is present with the risk of dueling proposers. It's important to implement the right timeouts and backoff strategies" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

**Randomness is the best defence.** Raft's election timer uses randomised intervals per replica, which makes simultaneous candidacy unlikely. Chapter 23 singles out Raft as having "a well-thought-out method of approaching the leader election process."

## Geographic implications

Over a wide-area network with clients spread geographically and replicas near the clients, **rotating leadership** ([[mencius-epaxos|Mencius, EPaxos]]) leads to lower perceived latency than a single fixed leader, because each client's RTT to the *nearest* replica is, on average, smaller than its RTT to an arbitrary leader (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This is the scenario where the rotating-leader / leaderless alternatives gain over stable leaders.

## Read optimisations enabled by a stable leader

If the system has a stable leader, reads can be served either directly by the leader or by any replica granted a [[quorum-leases|quorum lease]]. The leader's always-up-to-date property means leader reads are linearizable without running a read-only consensus round. See [[consensus-read-optimisations]] for the full menu of read strategies.

## Monitoring implications

Because the stable-leader architecture is so common, [[consensus-monitoring|consensus monitoring]] specifically includes leader-existence and leader-change metrics:

- **Whether a leader exists** — no leader means the system is totally unavailable.
- **Number of leader changes (flap rate)** — rapid changes impair performance; too-rapid increases signal network connectivity issues.
- **View or term number** — always-increasing when healthy; a decrease signals a bug.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[multi-paxos]]
- [[paxos]]
- [[mencius-epaxos]]
- [[consensus-performance]]
- [[quorum-leases]]
- [[consensus-read-optimisations]]
- [[consensus-monitoring]]
- [[zookeeper]]
- [[chubby]]
