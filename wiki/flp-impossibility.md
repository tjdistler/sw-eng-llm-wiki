# FLP Impossibility Result

**Summary**: The Fischer-Lynch-Paterson (1985) theorem that no deterministic asynchronous distributed [[consensus]] algorithm can guarantee progress in the presence of an unreliable network. Chapter 23's operational reading: you don't escape FLP by cleverness, you escape it by arranging the deployment so that "sufficient healthy replicas and network connectivity" exist to make progress most of the time, and by using randomised backoffs so retries don't cause cascades.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-17

---

## The result

Technically, solving asynchronous distributed [[consensus]] in bounded time is impossible (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The Dijkstra-Prize-winning FLP proof shows there is no deterministic algorithm that can guarantee *termination* (the liveness property) of consensus under arbitrarily-adversarial message scheduling.

This result assumes no clocks and no timeouts. It is a result about the purely asynchronous model — where messages may take arbitrarily long.

## The operational workaround

Chapter 23's framing of how production systems sidestep FLP:

> In practice, we approach the distributed consensus problem in bounded time by ensuring that the system will have sufficient healthy replicas and network connectivity to make progress reliably most of the time. In addition, the system should have backoffs with randomized delays. This setup both prevents retries from causing cascade effects and avoids the dueling proposers problem described later in this chapter.

(source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md)

Two operational disciplines fall out of this:

1. **Adequate redundancy to make progress likely.** Translated into [[consensus-replica-count|replica-count]] choices: 3 replicas tolerate 1 failure, 5 tolerate 2. Under realistic maintenance windows, 5 is what lets you keep making progress when a maintenance window overlaps an unplanned failure.
2. **Randomised backoffs on retries.** This both prevents [[cascading-failure|cascade effects]] and avoids the [[multi-paxos|dueling-proposers]] synchronisation anti-pattern.

## Safety vs liveness

The FLP result is fundamentally about liveness. The operational workaround is to sacrifice liveness-in-the-worst-case, not safety. As Chapter 23 puts it: "the protocols guarantee safety, and adequate redundancy in the system encourages liveness" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is the [[safety-and-liveness|safety-and-liveness framing]] applied to consensus: safety properties must always hold (never two different values committed for the same proposal), while liveness properties (eventual termination) may not hold during pathological network conditions.

## Cross-book framing

- [[consensus]] — the DDIA treatment of consensus reaches the same operational conclusion: "consensus is achievable by using timeouts to detect suspected failures, or by using randomization."
- [[safety-and-liveness]] — the abstract framing that FLP specifically isolates as a liveness-vs-safety trade-off.
- [[system-models]] — FLP is a result about the purely asynchronous model. Partially synchronous models (Chandra-Toueg) are how real implementations dodge it.
- [[timeouts]] — Kleppmann's DDIA Chapter 8 framing: timeouts are the only sure fault detection mechanism, and they are exactly what pure asynchrony forbids.
- [[unreliable-networks]] — the messaging model FLP assumes.
- [[process-pauses]] / [[unreliable-clocks]] — the practical sources of "unbounded delay" that make the FLP model real, not theoretical.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[safety-and-liveness]]
- [[system-models]]
- [[timeouts]]
- [[unreliable-networks]]
- [[paxos]]
- [[multi-paxos]]
- [[cascading-failure]]
