# Safety and Liveness

**Summary**: Two categories of properties for distributed algorithms -- safety properties say "nothing bad happens" and must hold at all times, while liveness properties say "something good eventually happens" and are allowed to have caveats about fault conditions.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Definitions

Distributed algorithm properties fall into two categories (source: designing-data-intensive-applications, chapter 8):

### Safety properties

If a safety property is violated, you can point to a **specific point in time** at which it was broken. Once violated, the damage is done -- it cannot be undone. Informally: "nothing bad happens."

Examples: uniqueness (no two fencing token requests return the same value), monotonic sequence (tokens are issued in order). (source: designing-data-intensive-applications, chapter 8)

### Liveness properties

A liveness property may not hold at a given point in time, but there is always hope it will be satisfied **in the future**. Informally: "something good eventually happens." A giveaway is the word "eventually" in the definition.

Examples: availability (a request eventually receives a response), [[eventual-consistency]] (replicas eventually converge). (source: designing-data-intensive-applications, chapter 8)

## Why the distinction matters

The distinction helps deal with difficult [[system-models]] (source: designing-data-intensive-applications, chapter 8):

- **Safety properties must always hold**, in all possible situations of the system model -- even if all nodes crash or the entire network fails. The algorithm must never return a wrong result.
- **Liveness properties are allowed caveats**: for example, a request may only need to receive a response if a majority of nodes have not crashed, and only if the network eventually recovers from an outage.

The partially synchronous model requires that the system eventually returns to a synchronous state -- any period of network interruption lasts only a finite duration. This is what makes liveness properties achievable: the system can make progress once conditions improve, while safety is maintained throughout. (source: designing-data-intensive-applications, chapter 8)

## Application to consensus (SRE Chapter 23)

Laura Nolan applies the safety-vs-liveness distinction directly to the [[consensus]] problem as the operational explanation for how production systems sidestep the [[flp-impossibility|FLP impossibility result]]:

> The protocols guarantee safety, and adequate redundancy in the system encourages liveness.

(source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md)

So consensus algorithms are designed so that **safety is absolute** (no two values ever committed for the same proposal, regardless of how pathological the network) and **liveness is conditional** (progress requires enough healthy replicas and acceptable network connectivity, which is why deployments pick [[consensus-replica-count|5 replicas]] rather than the bare minimum of 3, and why [[multi-paxos|leader-election timeouts]] use randomised backoffs to avoid [[multi-paxos|dueling-proposers]] livelock).

## Related pages

- [[system-models]]
- [[eventual-consistency]]
- [[fencing-tokens]]
- [[fault-tolerance]]
- [[consensus]]
- [[flp-impossibility]]
- [[managing-critical-state]]
