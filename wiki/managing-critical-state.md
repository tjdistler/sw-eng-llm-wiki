# Managing Critical State

**Summary**: Laura Nolan's Chapter 23 framing of distributed [[consensus]] as the structural answer to a whole family of problems ad-hoc solutions (heartbeats, gossip, timeouts, manual failover) get wrong: leader election, group membership, distributed locks and leases, reliable queuing, and any critical shared state. The chapter's operational thesis: whenever you see leader election, critical shared state, or distributed locking, use a formally-proven consensus system or accept that you are building "a ticking bomb waiting to explode."

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why this chapter exists

Processes crash, hard drives fail, natural disasters take out whole regions. Running services across multiple sites is the only way to survive these realities, and distributing a system is the easy half — maintaining a **consistent view of system state** across that distribution is the hard half (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

A group of processes reliably agreeing on things — *which process is the leader, what is the membership of the group, has a message been committed, does this process hold a lease, what is the value for this key* — is exactly the [[consensus|distributed consensus problem]]. Chapter 23 argues this machinery underpins virtually every service Google offers, and that informal approaches lead to outages and (worse) subtle data consistency problems that prolong outages unnecessarily.

## The three case studies

Chapter 23 opens with three short case studies of what happens when you try to solve agreement problems without a real consensus algorithm. Each is catalogued on [[consensus-coordination-failures]]:

- **Split-brain via STONITH**: two file servers with heartbeats and a "shoot the other node in the head" protocol end up either both active or both down under a slow network
- **Failover requires human intervention**: a highly-sharded DB promotes secondaries based on external health checks, but a primary that can't reach its secondary escalates to a human — operational load that doesn't scale, imposed during infrastructure-wide incidents when humans are already overloaded
- **Faulty group membership via gossip**: a cluster discovers itself via gossip and elects a leader, but a partition produces two leaders and data corruption

The lesson is the same each time: leader election, group membership, distributed locks and leases, reliable queuing, and any maintenance of critical shared state are all instances of distributed consensus. Ad-hoc solutions (heartbeats, timeouts, gossip) always have reliability problems.

## The chapter's structure

Chapter 23 works outward from the core problem to deployment:

1. **The problem and its framing** — [[cap-theorem]] reframed, BASE vs ACID, the need for correctness on critical state.
2. **How consensus works** — asynchronous vs synchronous, crash-fail vs crash-recover, Byzantine vs non-Byzantine; the [[flp-impossibility|FLP impossibility result]]; [[paxos|Paxos]] as the original protocol; [[safety-and-liveness|safety and liveness]] framing.
3. **System architecture patterns** — consensus algorithms are primitive and low-level; real systems use higher-level abstractions. Five patterns: [[replicated-state-machine|reliable replicated state machines]], [[reliable-replicated-datastore|reliable replicated datastores]], leader election for highly available processing, [[distributed-barrier|barriers]] / locks / coordination, [[reliable-distributed-queue|reliable distributed queuing]].
4. **Performance** — [[multi-paxos|Multi-Paxos]] message flow; [[fast-paxos|Fast Paxos]] and when it's slower; [[stable-leader|stable leaders]]; [[quorum-leases|quorum leases]] for scaling reads; batching; pipelining; [[consensus-disk-access|disk access]] as the under-appreciated bottleneck; the [[mencius-epaxos|rotating-leader protocols]] (Mencius, EPaxos).
5. **Deployment** — [[consensus-replica-count|number of replicas]]; [[consensus-replica-placement|location of replicas]]; capacity and load balancing; [[quorum-composition|quorum composition]] across regions; [[hierarchical-quorums|hierarchical quorums]] as a weakness-of-simple-majority-quorum mitigation.
6. **Monitoring** — what to alert on in a consensus cluster: see [[consensus-monitoring]].

## What the chapter deliberately avoids

Chapter 23 is pointedly not a tutorial on a specific algorithm or implementation. Nolan's rationale: "distributed coordination systems and the technologies underlying them are evolving quickly, and this information would rapidly become out of date, unlike the fundamentals" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The chapter trades depth on any one algorithm for a stable map of the problem space and its operational shape.

## Related pages

- [[consensus]]
- [[consensus-coordination-failures]]
- [[paxos]]
- [[multi-paxos]]
- [[fast-paxos]]
- [[flp-impossibility]]
- [[replicated-state-machine]]
- [[reliable-replicated-datastore]]
- [[distributed-barrier]]
- [[atomic-broadcast]]
- [[reliable-distributed-queue]]
- [[consensus-performance]]
- [[quorum-leases]]
- [[stable-leader]]
- [[mencius-epaxos]]
- [[consensus-disk-access]]
- [[consensus-replica-count]]
- [[consensus-replica-placement]]
- [[quorum-composition]]
- [[hierarchical-quorums]]
- [[consensus-monitoring]]
- [[zookeeper]]
- [[chubby]]
- [[cap-theorem]]
- [[safety-and-liveness]]
- [[site-reliability-engineering]]
