# Simple PRR Model

**Summary**: The classical [[sre-engagement-model|SRE engagement]] pattern for already-launched services. SRE runs a [[production-readiness-review|Production Readiness Review]] on an existing service, drives improvements, trains the receiving SRE team, and then takes over production responsibility. Six phases run like a development lifecycle: [[prr-engagement-phase|Engagement]] → [[prr-analysis-phase|Analysis]] → [[prr-improvements-and-refactoring|Improvements and Refactoring]] → [[prr-training-phase|Training]] → [[prr-onboarding-phase|Onboarding]] → [[prr-continuous-improvement|Continuous Improvement]].

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## When Simple PRR applies

Chapter 32 calls the Simple PRR Model "the most typical initial step of SRE engagement" (source: chapter-32-the-evolving-sre-engagement-model.md). It targets services that are already launched and serving production traffic, and whose development teams are requesting SRE takeover.

The model begins once SRE leadership decides the service merits support and that SRE and the development organisation agree on the staffing level required to sustain it (source: chapter-32-the-evolving-sre-engagement-model.md).

## Objectives

The PRR has two explicit objectives (source: chapter-32-the-evolving-sre-engagement-model.md):

- Verify the service meets accepted standards of production setup and operational readiness, and that service owners are prepared to take advantage of SRE expertise
- Improve the reliability of the service and minimise the number and severity of expected incidents

The six phases (covered on their own pages) sequence the review, reshape the service, train the receiving team, and institute long-term operational partnership:

1. **[[prr-engagement-phase|Engagement]]** — SRE leadership assigns 1-3 reviewers; they kick off discussion with the development team on [[service-level-objective|SLO]]/[[service-level-agreement|SLA]], disruptive design changes, and planning
2. **[[prr-analysis-phase|Analysis]]** — SRE reviewers learn the service, run it through the PRR checklist, review recent incidents and postmortems
3. **[[prr-improvements-and-refactoring|Improvements and Refactoring]]** — jointly prioritise and execute the identified gaps; usually the longest and most variable phase
4. **[[prr-training-phase|Training]]** — PRR leaders train the full SRE team via design overviews, request-flow deep dives, production walkthroughs, and hands-on exercises
5. **[[prr-onboarding-phase|Onboarding]]** — progressive transfer of operations, change management, and access rights
6. **[[prr-continuous-improvement|Continuous Improvement]]** — ongoing partnership; SRE maintains reliability as the service evolves and contributes lessons back to the [[production-guide|Production Guide]]

## Shakespeare, worked

Chapter 32 closes with the [[shakespeare-example-prr|Shakespeare service]] running through the Simple PRR Model: dashboards weren't covering some SLO-defined metrics, those were fixed, SRE took over the pager with two developers still in the rotation, weekly on-call meetings became the coordination venue, and future launches are now pre-reviewed with SRE (source: chapter-32-the-evolving-sre-engagement-model.md).

## Limitations

The Simple PRR Model is late in the lifecycle — the service is already launched and serving at scale. Chapter 32 names the costs (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Process overhead.** Additional communication between teams increases cognitive burden on SRE reviewers
- **Availability constraints.** The right SRE reviewers must be available and able to prioritise a new engagement against existing ones
- **Visibility needs.** SRE work must be highly visible and sufficiently reviewed by developers for knowledge to transfer — SREs must act as part of the development team, not as an external audit function
- **Late remediation cost.** Design fixes that would have been trivial pre-launch are expensive or impossible once the service is serving real traffic at scale

These limitations are the motivation for the [[early-engagement-model|Early Engagement Model]], which shifts SRE engagement to the Design phase.

## Related pages

- [[sre-engagement-model]]
- [[production-readiness-review]]
- [[prr-engagement-phase]]
- [[prr-analysis-phase]]
- [[prr-improvements-and-refactoring]]
- [[prr-training-phase]]
- [[prr-onboarding-phase]]
- [[prr-continuous-improvement]]
- [[early-engagement-model]]
- [[shakespeare-example-prr]]
- [[site-reliability-engineering]]
