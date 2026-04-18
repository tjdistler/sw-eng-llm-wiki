# Consensus Coordination Failures

**Summary**: Chapter 23's three opening case studies in what happens when you try to solve a distributed agreement problem with ad-hoc mechanisms — heartbeats, timeouts, gossip, human escalation — instead of a real [[consensus]] algorithm. Each case is a real-world pathology that a proven consensus system would have prevented.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Case study 1: The split-brain problem

A content-repository service uses pairs of replicated file servers in different racks. Each pair has one leader and one follower, monitored by heartbeats. If a server can't reach its partner, it sends a **STONITH** command (*Shoot The Other Node in the Head*) to its partner, shuts it down, and takes mastership (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

STONITH is the industry-standard response to split-brain. Nolan's objection is that it is **conceptually unsound** when used with heartbeats alone.

**What goes wrong under a slow or lossy network:**

1. Heartbeats exceed their timeouts on both sides.
2. Both servers send STONITH commands to their partners and try to take mastership.
3. Some STONITH commands are dropped or delayed.
4. The pair ends in either of two bad states:
   - Both are active for the same resource (data corruption — the [[failover|split-brain]] failure mode).
   - Both are down because both received STONITH commands before sending their own succeeded.

The root cause: "the system is trying to solve a leader election problem using simple timeouts. Leader election is a reformulation of the distributed asynchronous consensus problem, which cannot be solved correctly by using heartbeats" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is why [[failover]] remains dangerous in practice and why automatic leader election belongs in a [[consensus]] protocol, not in bespoke heartbeat code.

## Case study 2: Failover requires human intervention

A sharded database replicates each primary synchronously to a secondary in another datacenter. An external health-checker promotes a secondary when a primary is unhealthy. If the primary loses contact with its secondary, rather than risk split-brain, it **makes itself unavailable and pages a human** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This avoids data loss but has its own structural problems:

- **Availability loss**: the whole shard is offline until a human responds.
- **Operational load that doesn't scale**: every primary-secondary partition pages someone.
- **Worst-case timing**: these events correlate with larger infrastructure problems — exactly when responders are already swamped.
- **The human is no better positioned than an algorithm** if the network really is partitioned, no one has enough information to make the call safely.

The implicit claim — "a human will make a better decision here" — is usually false under the conditions that trigger the escalation. A consensus-based leader election would handle the decision automatically with safety properties the human cannot match.

## Case study 3: Faulty group-membership algorithms

An indexing/search cluster uses a **gossip protocol** for discovery and membership, then elects a leader for coordination. Under a network partition, each side independently elects a master, accepts writes and deletions, and ends up with data corruption when the partition heals (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Determining a consistent view of group membership across a group of processes is itself a distributed consensus problem. So is master election. Gossip converges eventually but provides no safety property that would prevent two sides from independently electing masters during a partition.

## The unifying lesson

Nolan's chapter uses these three cases to establish a rule the rest of the chapter elaborates on (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

> Many distributed systems problems turn out to be different versions of distributed consensus, including master election, group membership, all kinds of distributed locking and leasing, reliable distributed queuing and messaging, and maintenance of any kind of critical shared state that must be viewed consistently across a group of processes. All of these problems should be solved only using distributed consensus algorithms that have been proven formally correct, and whose implementations have been tested extensively. Ad hoc means of solving these sorts of problems (such as heartbeats and gossip protocols) will always have reliability problems in practice.

## Connections to the rest of the wiki

- [[failover]] — the Kleppmann framing of split-brain and the many ways automatic failover goes wrong is the theoretical substrate for case study 1
- [[truth-and-leadership-in-distributed-systems]] — a node can never trust its own judgment about whether it is still the leader; heartbeats and STONITH both violate this
- [[timeouts]] — the fundamental limit: timeouts are the only sure fault detection mechanism, but they cannot distinguish "partner dead" from "partner slow"
- [[byzantine-faults]] — all three cases are non-Byzantine but still unsolvable by ad-hoc means
- [[consensus]] — the right tool; see [[paxos]], [[multi-paxos]], Raft, Zab
- [[zookeeper]] / [[chubby]] — the typical deployment shape for outsourcing consensus

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[failover]]
- [[truth-and-leadership-in-distributed-systems]]
- [[timeouts]]
- [[fencing-tokens]]
- [[byzantine-faults]]
- [[zookeeper]]
- [[chubby]]
