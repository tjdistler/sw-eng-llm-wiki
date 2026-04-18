# Production Guide

**Summary**: Google's internal repository of documented production best practices for services, drawn from the experiences of both SRE and development teams. The Guide is the documentation layer of [[sre-alternative-support|SRE alternative support]] — teams that don't have direct SRE engagement can still implement its recommendations — and it also feeds the per-team [[prr-analysis-phase|PRR checklists]] used during Simple PRR reviews.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What's in the Guide

Chapter 32 describes the Production Guide as documentation of production best practices for services, "as determined by the experiences of SRE and development teams alike" (source: chapter-32-the-evolving-sre-engagement-model.md). Developers can implement the Guide's solutions and recommendations to improve their services directly, without requiring SRE engagement.

## Who uses it and when

Three primary consumers:

- **Development teams without direct SRE engagement.** The Guide is the structural substitute; teams that can't justify an SRE team read the Guide and implement what's relevant
- **SRE reviewers during Analysis.** The [[prr-analysis-phase|Analysis phase]] of a PRR uses the Guide as the substrate for its checklist. Each team's checklist is specific to its service portfolio but is generally based on domain expertise, experience with related systems, and Production Guide practices
- **SRE consultants.** Launch consultation and ad-hoc SRE advice commonly draw on the Guide as the reference source for recommendations

## Feedback loop

The [[prr-continuous-improvement|Continuous Improvement phase]] explicitly feeds the Guide: lessons from managing a service are contributed to best practices documented in the Guide and elsewhere (source: chapter-32-the-evolving-sre-engagement-model.md). This is how hard-won operational knowledge compounds — one service's post-incident learning becomes the next service's checklist item.

## Relationship to frameworks

The [[service-framework|framework]] model takes the Guide one step further: rather than documenting best practices for developers to implement, the framework implements them once in code. A team that builds on the framework gets the Guide's recommendations by construction. The Guide doesn't go away — not everything can be codified, and documentation still covers the parts that can't — but it shifts from the primary enforcement mechanism to a complement.

## Related pages

- [[sre-alternative-support]]
- [[prr-analysis-phase]]
- [[prr-continuous-improvement]]
- [[production-readiness-review]]
- [[service-framework]]
- [[frameworks-and-sre-platform]]
- [[site-reliability-engineering]]
