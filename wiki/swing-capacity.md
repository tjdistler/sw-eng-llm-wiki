# Swing Capacity

**Summary**: Chapter 33's telecom-industry preparedness pattern — a mobile, deployable reserve that can be moved to where load suddenly appears. The canonical example: the *switch on wheels* (SOW), a mobile telco office that can be rolled out for predictable surges (Olympics) or for unpredictable ones (natural disasters; the 2005 leaked celebrity phone number that produced DDoS-shaped traffic). Distinct from cloud-style elasticity because the capacity exists *physically reserved* and is moved into position rather than spun up on demand.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## The pattern

Chapter 33's framing (source: chapter-33-lessons-learned-from-other-industries.md):

> System utilization in the telecom industry can be highly unpredictable. Absolute capacity can be strained by unforeseeable events such as natural disasters, as well as large, predictable events like the Olympics. According to Gus Hartmann, the industry deals with these incidents by deploying swing capacity in the form of a SOW (switch on wheels), a mobile telco office. This excess capacity can be rolled out in an emergency or in anticipation of a known event that is likely to overload the system.

The structural property: capacity is **pre-built and reserved**, not provisioned at need. The optimisation isn't *speed of provisioning*; it's *physical mobility* — the capacity exists in a parking lot somewhere and gets driven to the place that needs it.

## The unexpected-load case

Chapter 33's worked unexpected example (source: chapter-33-lessons-learned-from-other-industries.md):

> When a celebrity's private phone number was leaked in 2005 and thousands of fans simultaneously attempted to call her, the telecom system exhibited symptoms similar to a DDoS or massive routing error.

The leaked-phone-number example matters because the load shape isn't *more total volume on the network* — it's *all the volume converging on a single endpoint*. Swing capacity addresses absolute throughput, not the routing-hot-spot variant; this is roughly the [[hot-spots|hot-spot]] problem applied to telecom infrastructure.

## Mapping onto SRE practice

SRE's analogous patterns aren't exact mirrors because Google's infrastructure is software-defined and the *roll a truck to the place that needs it* primitive doesn't apply directly. The closest analogues:

- **[[capacity-planning|Capacity planning]]** with explicit organic-and-inorganic surge headroom. The provisioned ceiling is set above the predicted peak by enough margin to absorb at least the surprises that have been seen before.
- **[[norad-tracks-santa|NORAD Tracks Santa]]'s 25× normal peak preparation** is a worked SRE case of the same problem: a known-date event with high uncertainty about absolute peak, addressed by overprovisioning across multiple datacenters.
- **[[gradual-rollout|Capacity buffers around launches]]** function as launch-time swing capacity — the infrastructure isn't on wheels, but the reserved-but-cold variant is what the buffer is.
- **[[handling-overload|Graceful degradation and load shedding]]** are the *opposite* response — when no swing capacity is available, the system serves a fraction of the traffic correctly rather than failing entirely. Both responses can coexist.

The Google telecom analogue would be reserving a fraction of cluster capacity that doesn't run the regular fleet at all and can be rapidly rebound to absorb a surge. Borg's preemption mechanics (high-priority jobs evicting batch jobs) provide a software version of *the truck arrives and the lower-priority load gets out of the way*.

## Why this matters

The Chapter 33 lesson is that **even highly automated infrastructure benefits from physically reserved spare capacity**, not just from elastic provisioning. Cloud rhetoric around *infinite scale* obscures the case where the absolute ceiling matters: the time it takes to provision new capacity is non-zero, and during that time, requests are being dropped. Swing capacity collapses that latency to zero by paying the cost of keeping unused capacity around all the time.

## Cross-book connections

- [[capacity-planning]] (SRE Ch 1, 18) — Google's explicit capacity-planning discipline with organic and inorganic demand forecasting
- [[norad-tracks-santa]] (SRE Ch 27) — the 25× normal peak case study; the surge-event launch realisation of swing-capacity discipline
- [[handling-overload]] (SRE Ch 21) — the alternative response when no swing capacity is available
- [[hot-spots]] (Kleppmann) — the routing-convergence load shape the leaked-celebrity-phone-number incident exhibited
- [[scaling-approaches]] (Kleppmann) — the manual / elastic / horizontal / vertical taxonomy in which swing capacity is *manual + horizontal + pre-reserved*
- [[lessons-from-other-industries]] / [[preparedness-and-disaster-testing]] — the Chapter 33 umbrella

## Related pages

- [[lessons-from-other-industries]]
- [[preparedness-and-disaster-testing]]
- [[capacity-planning]]
- [[norad-tracks-santa]]
- [[handling-overload]]
- [[hot-spots]]
