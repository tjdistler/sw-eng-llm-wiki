# Production Readiness Review (PRR)

**Summary**: The formal review SRE conducts before accepting production responsibility for a service. A PRR identifies the reliability needs of the service, applies accumulated SRE expertise to ensure it can operate in production, and drives improvements until the service is judged ready for SRE support. A PRR is a prerequisite for an SRE team to accept production responsibility.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What a PRR is

A Production Readiness Review is SRE's gate on production responsibility: before an SRE team will own the pager for a service, the service must pass a review that verifies (source: chapter-32-the-evolving-sre-engagement-model.md):

- The service meets accepted standards of production setup and operational readiness
- Service owners are prepared to work with SRE and take advantage of SRE expertise
- Expected incident frequency and severity have been driven down to a tolerable level

A PRR targets every aspect of "production" SRE cares about — architecture and dependencies, instrumentation and monitoring, emergency response, capacity planning, change management, and performance (source: chapter-32-the-evolving-sre-engagement-model.md). See [[sre-engagement-model]] for the full list.

## Three models that use the PRR

Chapter 32 describes the PRR under three engagement models (source: chapter-32-the-evolving-sre-engagement-model.md):

- **[[simple-prr-model|Simple PRR Model]]** — the classical shape; run on an already-launched service when the development team asks SRE to take over
- **[[early-engagement-model|Early Engagement Model]]** — the PRR process begins in the Design phase of the service lifecycle, not after launch, so the "review" becomes a continuous collaboration
- **[[frameworks-and-sre-platform|Frameworks and SRE Platform]]** — when a service is built on SRE-supported frameworks, the PRR is largely satisfied by construction; review effort drops because the service reuses blessed infrastructure

The Simple PRR Model's six-phase structure (Engagement, Analysis, Improvements and Refactoring, Training, Onboarding, Continuous Improvement) is the canonical form; the other two models vary when and how the phases apply.

## PRR lead times

The PRR is proportionally expensive. Chapter 32's own retrospective documents the costs of the Simple PRR Model (source: chapter-32-the-evolving-sre-engagement-model.md):

- Two or three SREs per service
- Two or three quarters per engagement
- Lead times measured in quarters
- Insufficient SRE staffing forces serialization and strict prioritization

These numbers are what the framework-based model was designed to attack: framework-built services complete a PRR with one SRE in one quarter, because the heavy lifting already happened once — in the framework itself.

## What the Analysis phase checks

The [[prr-analysis-phase|Analysis phase]] runs the service against a PRR checklist maintained by the SRE team. See that page for the full list; representative checks from Chapter 32 (source: chapter-32-the-evolving-sre-engagement-model.md):

- Do updates impact an unreasonably large percentage of the system at once?
- Does the service connect to the appropriate serving instance of its dependencies (e.g. user-facing requests not landing on batch-processing backends)?
- Does the service request a high enough network quality-of-service when talking to critical remote services?
- Does the service report errors to central logging systems and instrument user-visible failures with suitable alerting?

The checklist also encodes SRE team-specific "gold standards" — a perfectly functional service whose configuration doesn't match the team's scalable-configuration patterns may still be refactored as part of the PRR, because otherwise the ongoing operational cost would be higher.

## Outcome

If the Analysis phase identifies serious shortcomings, the [[prr-improvements-and-refactoring|Improvements and Refactoring phase]] negotiates and executes a plan with the development team. Once the service is deemed ready, SRE moves through [[prr-training-phase|Training]] and [[prr-onboarding-phase|Onboarding]] and assumes production responsibility.

Not every engagement ends in takeover. Under the Early Engagement Model, [[disengaging-from-a-service|SRE may disengage]] if the service turns out to be sufficiently reliable and low-maintenance that it can stay with the development team, or if it fails to grow into the use case that justified SRE attention (source: chapter-32-the-evolving-sre-engagement-model.md).

## Related pages

- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[prr-engagement-phase]]
- [[prr-analysis-phase]]
- [[prr-improvements-and-refactoring]]
- [[prr-training-phase]]
- [[prr-onboarding-phase]]
- [[prr-continuous-improvement]]
- [[early-engagement-model]]
- [[frameworks-and-sre-platform]]
- [[disengaging-from-a-service]]
- [[launch-coordination-engineering]]
- [[site-reliability-engineering]]
