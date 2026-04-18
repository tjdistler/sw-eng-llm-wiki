# Unmanaged Incident Anti-Patterns

**Summary**: Chapter 14's three named failure modes when an incident is handled without a structured framework. They are cataloguing failures of *coordination* — every individual is doing their job correctly; the response fails because the individual jobs are not composed. The [[incident-management-framework]] is the structural fix.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## The opening case study

Chapter 14 opens with Mary, the Friday-afternoon on-call engineer for "The Firm". A datacentre stops serving; then a second; then a third. The remaining datacentres overload. Mary's colleague Josephine (the developer who wrote most of the code, in another time zone) is woken up. Other colleagues poke around independently. A VP demands an ETA. Josephine recruits Malcolm, who has a brainwave about CPU affinity and pushes a one-line change directly to production. The remaining servers restart and die.

> Note that everybody in the preceding scenario was doing their job, as they saw it. How could things go so wrong? (source: chapter-14-managing-incidents.md)

The chapter names three structural causes.

## 1. Sharp focus on the technical problem

> We tend to hire people like Mary for their technical prowess. So it's not surprising that she was busy making operational changes to the system, trying valiantly to solve the problem. She wasn't in a position to think about the bigger picture of how to mitigate the problem because the technical task at hand was overwhelming. (source: chapter-14-managing-incidents.md)

The on-call engineer's cognitive budget is fully consumed by the technical work, which means there's no budget left for:

- Communications with stakeholders
- Coordinating volunteers who want to help
- Strategic re-evaluation ("is this approach actually working?")
- Considering [[triage-sre|emergency mitigations]] like traffic diversion

The framework's fix is the [[incident-commander]] role — a person whose explicit job is to hold the bigger picture, freeing the technical lead to stay focused.

## 2. Poor communication

> For the same reason, Mary was far too busy to communicate clearly. Nobody knew what actions their coworkers were taking. Business leaders were angry, customers were frustrated, and other engineers who could have lent a hand in debugging or fixing the issue weren't used effectively. (source: chapter-14-managing-incidents.md)

Two failures cascade from the lack of communication:

- **Stakeholders' anxiety amplifies pressure on the response team** — the angry boss phone call, the VP demanding ETAs, the irrelevant-but-hard-to-refute engineering suggestions ("Increase the page size!"). Each interruption further depletes the on-call engineer's cognitive budget.
- **Available help is wasted** — the colleagues who could have been useful didn't know what was being tried, what was needed, or who to ask.

The framework's fix is twofold: the [[incident-communications-lead|comms lead]] role plus the [[recognized-command-post|recognised command post]] (chat / war room / email thread). Stakeholders learn there is one place to look; the response team learns where to coordinate.

## 3. Freelancing

> Malcolm was making changes to the system with the best of intentions. However, he didn't coordinate with his coworkers — not even Mary, who was technically in charge of troubleshooting. His changes made a bad situation far worse. (source: chapter-14-managing-incidents.md)

This is the most insidious of the three because the freelancer is *helping*, by their lights. Malcolm's CPU-affinity change was a real engineering insight; under other circumstances it might have been the fix. The failure was the uncoordinated application of it during a response in which the on-call engineer was already trying multiple changes and trying to reason about cause and effect.

The framework's fix is the **operations-team-only** rule (see [[incident-ops-lead]]): during an incident, only the designated ops team modifies the system. Volunteers who want to help route through the IC, who decides whether to incorporate them into the response.

## Why the failure is structural

The chapter's emphasis is that **the people in the unmanaged scenario are not at fault**. They are good engineers responding to a crisis with the tools and instincts available to them. The failure is the absence of a framework that channels those instincts into a coordinated response.

This is the SRE-book pattern of attributing outcomes to systems rather than individuals — it's the same cultural commitment that produces [[blameless-postmortem|blameless postmortems]]. Chapter 14 is doing the proactive form: rather than blaming individuals after the failure, build the system that lets individuals succeed.

## Cross-book connection

- The "everyone doing their job" framing is the operational analogue of Newman's distributed-system [[fallacies-of-distributed-computing|fallacies]]: well-intentioned local correctness does not compose into global correctness without explicit structure.
- The freelancing anti-pattern is the human form of the [[change-management-sre|uncoordinated change]] failure mode that automation discipline is designed to prevent.

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[recognized-command-post]]
- [[recursive-separation-of-responsibilities]]
- [[declaring-an-incident]]
- [[blameless-postmortem]]
