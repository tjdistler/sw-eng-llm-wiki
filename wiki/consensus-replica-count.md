# Consensus Replica Count

**Summary**: Chapter 23's operational argument for how many replicas a consensus group should have: 2f+1 tolerates f failures for non-Byzantine protocols (3f+1 for Byzantine), three is the practical minimum and five is what lets the system tolerate an unplanned failure **during** a planned-maintenance window. The count is a trade-off between reliability, maintenance frequency, risk tolerance, performance (more replicas = more lagging replicas the quorum can outrun), and cost.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The formulas

In general, a [[consensus]]-based system operates on **majority quorums** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

| Fault model | Replicas to tolerate f failures |
|---|---|
| Non-Byzantine | 2f + 1 |
| Byzantine (must survive replicas returning incorrect results) | 3f + 1 |

[[byzantine-faults]] are out of scope for most production consensus systems — they are expensive to handle, and correlate in practice with software bugs rather than adversarial actors inside your own infrastructure. Three replicas tolerating one failure is the non-Byzantine minimum.

## Three replicas is the practical floor

Two replicas mean **no tolerance for failure** of any process. Three replicas tolerate one failure. The operational question is: what's the failure budget under realistic conditions?

Chapter 23's answer leans on the fact that most system downtime is due to **planned maintenance** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Three replicas allow a system to operate normally when one replica is down for maintenance. But if an unplanned failure happens *during* that maintenance window, the system becomes unavailable.

## Five replicas is what most systems want

For non-Byzantine systems where unavailability of the consensus system is unacceptable: run **five replicas**, which lets the system operate with up to two simultaneous failures (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This covers the common worst case: one replica is in maintenance, one fails unexpectedly, the remaining three still have quorum.

Chapter 23's specific operational rule: "No intervention is necessarily required if four out of five replicas in a consensus system remain, but if three are left, an additional replica or two should be added."

## When quorum is lost

If a consensus system loses so many replicas it cannot form a quorum, it is **in theory in an unrecoverable state**: the durable logs of at least one missing replica cannot be accessed, and a decision seen only by those missing replicas may have been made (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Administrators may force a group-membership change and add new replicas that catch up from the survivors to proceed, but **the possibility of data loss always remains** — a situation to avoid if at all possible. In a disaster, the choice is between forcing reconfiguration and waiting for missing machines to return.

## The replicated log

Theoretical papers often say "consensus can be used to construct a replicated log" but don't discuss **replicas that miss decisions and later need to catch up**. In production systems the **replicated log** is a first-class concern — see [[replicated-state-machine]] on peer synchronisation via Kirsch-Amir sliding-window protocols.

Chapter 23 calls out Raft specifically for defining this explicitly: "Raft describes a method for managing the consistency of replicated logs, explicitly defining how any gaps in a replica's log are filled. If a five-instance Raft system loses all of its members except for its leader, the leader is still guaranteed to have full knowledge of all committed decisions." If the missing majority *included* the leader, no strong guarantees can be made (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## Replicas vs quorum performance

There is a subtle performance-related reason to run **more** replicas than the bare minimum: the quorum is a **majority**, not every replica. A minority of slower replicas may lag behind, letting the quorum of better-performing replicas run faster — as long as the leader performs well (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

If replica performance varies significantly, every failure slows the overall system because slow outliers get pulled into the quorum. The more failures or lagging replicas the system can tolerate, the better its steady-state performance.

## The trade-offs

Chapter 23's decision is a trade-off across (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- Reliability need (SLO)
- Frequency of planned maintenance
- Risk tolerance
- Performance
- Cost

Cost matters particularly for **highly sharded** consensus systems like Photon, where each shard is a full group. Adding one replica multiplies by the number of shards: in a system with 1,000 shards, moving from 5 to 6 replicas per shard adds 1,000 processes.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[consensus-replica-placement]]
- [[quorum-composition]]
- [[hierarchical-quorums]]
- [[byzantine-faults]]
- [[replicated-state-machine]]
- [[consensus-monitoring]]
- [[n-plus-2-redundancy]]
