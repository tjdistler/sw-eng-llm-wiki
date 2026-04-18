# PRR Engagement Phase

**Summary**: The first phase of the [[simple-prr-model|Simple PRR Model]]. SRE leadership identifies an SRE team to take over the service, one to three SREs are selected or self-nominate as reviewers, and those reviewers open discussion with the development team on SLOs, disruptive design changes, and planning.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What happens in this phase

Chapter 32's Engagement phase (source: chapter-32-the-evolving-sre-engagement-model.md):

- **SRE leadership picks a team.** A good-fit SRE team is selected to take over the service
- **Reviewers form.** Usually one to three SREs are selected or self-nominate to conduct the PRR process
- **Discussion opens with the development team.** The topics (source: chapter-32-the-evolving-sre-engagement-model.md):
  - Establishing a [[service-level-objective|SLO]] / [[service-level-agreement|SLA]] for the service
  - Planning for potentially disruptive design changes required to improve reliability
  - Planning and training schedules

The output of the phase is a common agreement about the process, end goals, and outcomes required for the SRE team to engage with the development team and the service.

## Why the SLO discussion comes first

Chapter 32 calls establishing the SLO a first-order Engagement-phase task. Without it, the subsequent phases lack an objective reliability target against which the [[prr-analysis-phase|Analysis phase]] can gauge maturity and the [[prr-improvements-and-refactoring|Improvements phase]] can prioritise work. The SLO is also what the development team and SRE will use to resolve the tension between velocity and reliability once SRE takes over (the [[error-budget|error budget]] framing from Chapter 3).

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-analysis-phase]]
- [[service-level-objective]]
- [[service-level-agreement]]
- [[sre-engagement-model]]
- [[site-reliability-engineering]]
