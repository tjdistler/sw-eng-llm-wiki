# Incident Planning Lead

**Summary**: The longer-horizon support role in Chapter 14's [[incident-management-framework]]. Planning takes care of the items that would otherwise drop on the floor while [[incident-ops-lead|Ops]] is fixing the system: filing bugs, ordering dinner, arranging handoffs, and tracking how the system has diverged from the norm so it can be reverted once the incident is resolved.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## What the planning lead does

> The planning role supports Ops by dealing with longer-term issues, such as filing bugs, ordering dinner, arranging handoffs, and tracking how the system has diverged from the norm so it can be reverted once the incident is resolved. (source: chapter-14-managing-incidents.md)

Chapter 14 lists these in the same breath, which is informative — the role spans serious continuity work (arranging handoffs, tracking system divergence) alongside humble logistics (dinner). The unifying property is that none of it is the immediate technical fix, and all of it would otherwise interrupt Ops if Ops had to do it.

## Tracking system divergence

The "tracking how the system has diverged from the norm" duty is the important one to call out separately. During an incident, the response team may:

- Disable subsystems to lighten load
- Drop traffic
- Remove load-balancer entries
- Push an emergency configuration
- Manually disable an alert that's flapping while the underlying issue is being fixed
- Skip a scheduled rollout

Each of these is a deliberate, temporary deviation from the steady-state configuration. Without somebody tracking them, **they will not all be reverted** when the incident resolves — and the leftover state becomes the seed of the next incident. (Chapter 13's [[automation-gone-wrong|Diskerase]] response left automation frozen for a recovery window; *unfreezing it* was a separate planned action.)

The planning lead's tracking is the bridge between the response and the postmortem follow-up. Many postmortem action items fall out of "things we did during the incident that we now need to formally undo or codify".

## Allocating new staff

Planning is also the role that responds when another role is overloaded and asks for more people (source: chapter-14-managing-incidents.md, Recursive Separation of Responsibilities section). Planning sources the staff and arranges their integration into the response. The role is the natural owner of "who's doing what right now" because it's already tracking schedules and handoffs.

## Why dinner is on the list

Sustaining a multi-shift incident response means sustaining the people running it. Skipping meals, working from home without a break, missing a partner pickup — these are the ways the response degrades silently. Naming "order dinner" as a planning responsibility is Chapter 14's terse acknowledgment that **physical maintenance of the responders is part of the work**.

## Cross-book connection

- The "track divergence so it can be reverted" duty is the operational form of [[architecture-decision-record|ADR consequences]] applied to ephemeral incident decisions: each temporary deviation is a tiny decision whose consequences someone has to track.
- Sustaining responders over a long incident is the same problem as sustaining engineers over a long on-call rotation — see [[balanced-on-call]] and [[on-call-compensation]].

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[recursive-separation-of-responsibilities]]
- [[blameless-postmortem]]
- [[incident-handoff]]
