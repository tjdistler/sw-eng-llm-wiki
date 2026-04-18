# SRE Engagement Model

**Summary**: How an SRE team takes on responsibility for a service. Chapter 32 describes three successive engagement models — the [[simple-prr-model|Simple PRR Model]], the [[early-engagement-model|Early Engagement Model]], and the [[frameworks-and-sre-platform|Frameworks and SRE Platform]] structure — each scaling SRE's impact further by applying expertise earlier in the service lifecycle and codifying it into reusable infrastructure.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What SRE engagement means

SRE seeks production responsibility for important services where it can make concrete contributions to reliability. "Production" in Chapter 32 is the collection of aspects SRE cares about (source: chapter-32-the-evolving-sre-engagement-model.md):

- System architecture and interservice dependencies
- Instrumentation, metrics, and monitoring
- Emergency response
- Capacity planning
- Change management
- Performance: availability, latency, efficiency

When SRE engages a service, the team aims to improve it along all of these axes so that managing it in production becomes tractable (source: chapter-32-the-evolving-sre-engagement-model.md). This set of concerns is what every engagement model — simple, early, or framework-based — is pointed at.

## The three models

Chapter 32 documents the evolution of SRE engagement as the organisation scaled:

1. **[[simple-prr-model|Simple PRR Model]]** — the classical pattern. SRE runs a [[production-readiness-review|Production Readiness Review]] on an already-launched service, drives improvements, trains the team, and takes over production responsibility. Still the most typical initial step of SRE engagement (source: chapter-32-the-evolving-sre-engagement-model.md).
2. **[[early-engagement-model|Early Engagement Model]]** — SRE joins during the Design phase rather than after launch. "The best production incidents are those that never happen." SRE's design-time influence is higher, onboarding is faster, and post-launch operational burden is lower (source: chapter-32-the-evolving-sre-engagement-model.md).
3. **[[frameworks-and-sre-platform|Frameworks and SRE Platform]]** — rather than retrofit each service to SRE standards, development teams build on an SRE-validated platform and language-specific service frameworks that bake production best practices into the code. Turns onboarding into configuration and breaks the SRE-staffing barrier for services that don't warrant full-team engagement (source: chapter-32-the-evolving-sre-engagement-model.md).

All three are still practiced at Google simultaneously; frameworks are becoming the prominent model but do not replace the others (source: chapter-32-the-evolving-sre-engagement-model.md).

## Why engagement has to be selective

The number of development teams requesting SRE support exceeds SRE bandwidth by design (source: chapter-32-the-evolving-sre-engagement-model.md). Not every service needs high reliability, and [[sre-discipline|SRE hiring]] is intentionally slower than product-development hiring. The two fallback modes for services that cannot justify full SRE engagement:

- **[[sre-alternative-support|Alternative support]]** — documentation (the Production Guide) and consultation (launch advice, [[launch-coordination-engineering|LCE]]) without production ownership.
- **[[shared-responsibility-engagement|Shared responsibility]]** — the framework-era middle ground: SRE supports the platform infrastructure, development teams carry the pager for application-specific bugs.

## Decision to engage

When a development team requests SRE take over a service (the Simple PRR Model entry condition), SRE leadership gauges two things (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Service importance.** Does this service warrant SRE support?
- **SRE availability.** Can the organisation commit staffing for this engagement?

If both check out, a PRR is initiated and the small group of reviewers (usually one to three SREs) begins the [[prr-engagement-phase|Engagement phase]].

The Early Engagement Model adds earlier decision points. [[early-engagement-candidates|Candidates for Early Engagement]] are services where importance can be judged in advance: significant new functionality within an SRE-managed system, significant rewrites of SRE-managed services, or teams that proactively approached SRE (source: chapter-32-the-evolving-sre-engagement-model.md).

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-engagement-phase]]
- [[prr-analysis-phase]]
- [[prr-improvements-and-refactoring]]
- [[prr-training-phase]]
- [[prr-onboarding-phase]]
- [[prr-continuous-improvement]]
- [[early-engagement-model]]
- [[early-engagement-candidates]]
- [[frameworks-and-sre-platform]]
- [[service-framework]]
- [[shared-responsibility-engagement]]
- [[sre-alternative-support]]
- [[sre-discipline]]
- [[launch-coordination-engineering]]
- [[site-reliability-engineering]]
