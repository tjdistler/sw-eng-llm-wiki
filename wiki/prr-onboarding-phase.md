# PRR Onboarding Phase

**Summary**: The phase of the [[simple-prr-model|Simple PRR Model]] in which production responsibility progressively transfers from the development team to the SRE team. Operations, the change-management process, access rights, and other production aspects move over in stages; the development team stays available to back up and advise the SRE team as it settles into the role.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What transfers

Chapter 32 describes Onboarding as a "progressive transfer of responsibilities and ownership of various production aspects of the service" (source: chapter-32-the-evolving-sre-engagement-model.md):

- Operations responsibilities
- The change-management process
- Access rights
- The other production aspects SRE cares about (see [[sre-engagement-model]])

Transfer is progressive, not a single cutover. The SRE team takes on areas one by one, confirming it can handle each before moving to the next.

## The development team stays in the loop

Chapter 32 makes this explicit (source: chapter-32-the-evolving-sre-engagement-model.md):

> To complete the transition, the development team must be available to back up and advise the SRE team for a period of time as it settles in managing production for the service. This relationship becomes the basis for the ongoing work between the teams.

The development team is not released when onboarding starts — it becomes the escalation channel and advisor while the SRE team learns to manage the service in production. That relationship then carries forward as the long-term SRE-dev collaboration (see [[sre-dev-collaboration]] and [[production-meetings]]).

## When onboarding ends

Chapter 32 doesn't set a strict duration. Onboarding is complete when the SRE team is operationally self-sufficient on the service, at which point the relationship transitions into [[prr-continuous-improvement|Continuous Improvement]] as the ongoing steady state.

## Shakespeare worked example

In Chapter 32's Shakespeare case study, the handoff is partial by design (source: chapter-32-the-evolving-sre-engagement-model.md):

> SRE took over the pager for the service, though two developers were in the on-call rotation as well.

A mixed rotation during onboarding is a useful pattern: developers carry the pager at reduced load while SRE ramps up, providing both a safety net and ongoing knowledge transfer.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-training-phase]]
- [[prr-continuous-improvement]]
- [[sre-dev-collaboration]]
- [[production-meetings]]
- [[sre-engagement-model]]
- [[shakespeare-example-prr]]
- [[site-reliability-engineering]]
