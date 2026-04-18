# Quorum Composition

**Summary**: Chapter 23's framing of how replica *placement* affects quorum latency once you accept the [[consensus-replica-placement|replica-placement]] trade-offs. Spreading replicas evenly with similar inter-replica RTTs produces consistent regional performance; geography (intra-continental vs transatlantic) can make that impossible, motivating placements where one replica acts as a **linchpin** bridging two possible quorums. Loss of the linchpin replica can cause a drastic latency jump.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The even-placement ideal

One approach is to spread replicas as evenly as possible, with similar RTTs between all replicas. All other factors equal, this produces fairly consistent performance regardless of where the group leader happens to be (or, for a leaderless protocol, for each replica of the consensus group) (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## Why geography makes this impossible

"Geography can greatly complicate this approach. This is particularly true for intracontinental versus transpacific and transatlantic traffic" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

A system spanning North America and Europe cannot place replicas equidistantly: transatlantic RTT is always higher than intracontinental RTT. Some transactions will always require a transatlantic round trip to reach consensus.

## The linchpin placement

Chapter 23's example (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md): place **five replicas** as follows:

- Two replicas roughly centrally in the US
- One replica on the east coast
- Two replicas in Europe

Average-case result:

- Consensus in North America can be achieved without waiting for Europe (the 3-replica US majority forms locally).
- Consensus from Europe can be achieved by exchanging messages only with the east-coast replica (2 EU + 1 east-coast = majority).

The east-coast replica is a **linchpin** — two possible quorums overlap in it.

## The linchpin's failure mode

Loss of the linchpin replica causes a drastic latency change. Consensus now requires the slower central-US-to-EU RTT, which is ~50% higher than the EU-to-east-coast RTT. The geographic distance between the nearest possible quorum increases enormously (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is the key weakness of a simple-majority quorum applied to groups of replicas with very different inter-replica RTTs.

## The hierarchical-quorum alternative

When the flat-majority quorum is fragile against linchpin loss, a **hierarchical** scheme helps — see [[hierarchical-quorums]]. Nine replicas in three groups of three, where a quorum is formed by a majority of groups and a group counts when a majority of its members are available. The central group can lose one replica without a significant latency hit.

The cost is more replicas in the system. In a highly-sharded, read-heavy system, this can be offset by using fewer consensus groups so the total process count is unchanged.

## Monitoring consequences

Linchpin placements make [[consensus-monitoring|monitoring]] more important: the health of the linchpin replica has outsized impact on observable latency, and loss of that specific replica should trigger specific investigation rather than a generic replica-down alert.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[consensus-replica-placement]]
- [[consensus-replica-count]]
- [[hierarchical-quorums]]
- [[consensus-monitoring]]
- [[consensus-performance]]
