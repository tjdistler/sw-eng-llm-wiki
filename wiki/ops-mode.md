# Ops Mode

**Summary**: The structural failure mode where a team meets growth in service load by adding human labour rather than by writing software. The SRE model's explicit goal is the opposite: the number of people required to run a service should not increase as a function of service load. Chapter 30 names *ops mode versus nonlinear scaling* as the single framing the visiting SRE uses to diagnose and explain team drift.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## Definition

*The term ops mode refers to a certain method of keeping a service running. Various work items increase with the size of the service. For example, a service needs a way to increase the number of configured virtual machines (VMs) as it grows. A team in ops mode responds by having a greater number of administrators managing those VMs* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

The contrast: **SRE focuses on writing software or eliminating scalability concerns so that the number of people required to run a service doesn't increase as a function of load on the service.**

Ops mode is therefore not about laziness or poor engineering — it's about which dimension you grow along as the service grows. Ops mode scales humans linearly with load; SRE scales software complexity with load and keeps humans flat (or sublinear). See [[sre-discipline]] for the sublinear-scaling argument.

## How a team slides into ops mode

The chapter's observation: *SRE teams sometimes fall into ops mode because they focus on how to quickly address emergencies instead of how to reduce the number of emergencies* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). A default to ops mode usually happens in response to **overwhelming pressure, real or imagined**. The team's attention is consumed by today's queue, and the work that would prevent tomorrow's queue never gets done. This is the structural feedback loop that produces [[operational-overload]].

## Diagnostic: more tickets should not require more SREs

Chapter 30's one-line test for ops mode: *remind the team that more tickets should not require more SREs: the goal of the SRE model is to only introduce more humans as more complexity is added to the system* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). If the team's response to rising ticket volume is "we need more headcount", they are in ops mode. The correct SRE response to rising ticket volume is "what automation or redesign reduces the volume?"

Complexity growth *does* justify adding SREs — a genuinely richer system needs more heads to understand it. Load growth does not.

## The "my service is tiny" defence

One failure mode: a team in ops mode convinces itself that scale doesn't apply — *"my service is tiny"*. Chapter 30 is explicit that this deserves verification rather than acceptance (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

- Shadow an on-call session to confirm whether the assessment is true. Scale affects strategy.
- If the service is genuinely small but business-critical, focus on how the team's current approach prevents them from improving reliability. *Remember that your job is to make the service work, not to shield the development team from alerts.*
- If the service is in early growth, focus on preparing the team for explosive growth. *A 100 request/second service can turn into a 10k request/second service in a year.*

The small-service rationalisation is dangerous because it treats the 100× scaling horizon as someone else's problem. In practice it is the current team's problem, just delayed.

## Why healthy work habits matter as much as automation

Chapter 30 flags an easily-missed point: when embedded, the visiting SRE should draw attention to *how healthy work habits reduce the time spent on tickets*, and that doing so is *as important as pointing out missed opportunities for automation or simplification of the service* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

Ops mode has a cultural dimension as well as a technical one. A team that writes good postmortems, sorts fires into toil-vs-not-toil, and defends project time is a team that generates less ops work per engineer even before any automation ships. The opposite — a team that firefights each ticket in isolation without a follow-up discipline — will generate the same ops work per engineer even after automation ships, because the next batch of fires appears at the same rate.

## Relationship to the 50% cap

The [[toil-and-engineering-balance|50% cap]] is the structural defence against ops mode. Chapter 1 introduces the cap and the safety valve; Chapter 5 sharpens the toil definition; Chapter 11 puts concrete numbers on [[operational-overload|overload]] symptoms; Chapter 30 is what happens when the cap has already been breached for months. Ops mode is the name for the shape of the breach.

## Relationship to the sysadmin approach

Ops mode is the same phenomenon as the [[sysadmin-approach|sysadmin approach]], seen from the inside of an SRE org. A team in ops mode *with SRE in its name* is structurally the same as a sysadmin team — the job title doesn't rescue the trajectory. Chapter 30's rescue pattern ([[embedding-sre]]) is the organisational intervention for pulling a team back across the line.

## Related pages

- [[embedding-sre]]
- [[toil-and-engineering-balance]]
- [[operational-overload]]
- [[sre-discipline]]
- [[sysadmin-approach]]
- [[identifying-kindling]]
- [[dealing-with-interrupts]]
- [[sre-tenets]]
