# Safety and Liveness

**Summary**: Two categories of properties for distributed algorithms -- safety properties say "nothing bad happens" and must hold at all times, while liveness properties say "something good eventually happens" and are allowed to have caveats about fault conditions.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[system-models]]
- [[eventual-consistency]]
- [[fencing-tokens]]
- [[fault-tolerance]]
