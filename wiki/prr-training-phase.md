# PRR Training Phase

**Summary**: The phase of the [[simple-prr-model|Simple PRR Model]] in which the PRR reviewers teach the receiving SRE team everything required to take over production responsibility. Instruction covers design, request flows, production setup, and hands-on operational exercises, typically conducted jointly with the development team.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Why the PRR reviewers run training

Production responsibility is assumed by an entire SRE team, not by the handful of engineers who conducted the review. The PRR reviewers take ownership of preparing the whole team — including the documentation necessary to support the service — because they have the deepest context (source: chapter-32-the-evolving-sre-engagement-model.md).

## What the training covers

Chapter 32 lists four instructional formats (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Design overviews.** The architecture at the level SRE needs
- **Request-flow deep dives.** Tracing individual operations through the system
- **Production setup.** Deployment layout, configuration, release machinery
- **Hands-on exercises.** Operational tasks run against the service to build muscle memory

The development team typically participates — sometimes leading sessions for areas SRE is less familiar with — because they still hold knowledge SRE needs and this is the phase to transfer it.

## Connection to the broader onboarding discipline

Training in the PRR sense is the service-specific counterpart to [[sre-onboarding|SRE onboarding]] for individuals. Where Ch 28 covers the structural curriculum that makes a new SRE productive on any service, the PRR Training phase covers the specific knowledge required for a specific service. Both lean on the same tools — the [[on-call-learning-checklist|learning checklist]], [[disaster-role-playing|Wheel of Misfortune]]–style exercises, and [[documentation-as-apprenticeship|documentation authorship]] as a learning lever.

## Output

At the end of training, the SRE team is prepared to manage the service. That readiness unlocks the [[prr-onboarding-phase|Onboarding phase]], in which actual production responsibility is progressively handed over.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-improvements-and-refactoring]]
- [[prr-onboarding-phase]]
- [[sre-onboarding]]
- [[on-call-learning-checklist]]
- [[disaster-role-playing]]
- [[site-reliability-engineering]]
