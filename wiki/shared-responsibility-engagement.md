# Shared Responsibility Engagement

**Summary**: The engagement model that becomes possible once services are built on [[service-framework|SRE-supported frameworks]]. SRE provides on-call support for the platform infrastructure (load shedding, overload handling, automation, traffic management, logging, monitoring); development teams carry the pager for functional bugs in the application code. A structural departure from the "full SRE support or approximately no SRE engagement" binary of the earlier engagement models.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The binary that preceded it

Under the [[simple-prr-model|Simple PRR Model]] and [[early-engagement-model|Early Engagement Model]], a service got one of two treatments (source: chapter-32-the-evolving-sre-engagement-model.md):

- Full SRE support — an SRE team takes production ownership after a PRR
- Approximately no SRE engagement — occasional best-effort consulting only, via docs and [[launch-coordination-engineering|LCE]]

Chapter 32 calls this out explicitly (source: chapter-32-the-evolving-sre-engagement-model.md):

> The original SRE engagement model presented only two options: either full SRE support, or approximately no SRE engagement.

The framework-based platform breaks the binary by making it possible to split responsibilities coherently.

## How the split works

With a common service structure, conventions, and software infrastructure (source: chapter-32-the-evolving-sre-engagement-model.md):

- **SRE supports the "platform" infrastructure.** SRE assumes responsibility for the development and maintenance of large parts of service software infrastructure — control systems such as load shedding, overload handling, automation, traffic management, logging, and monitoring
- **Development teams provide on-call support for functional issues.** Bugs in application code stay with the team that wrote it

The division is clean because the framework draws a hard line between infrastructure (uniform, SRE-supported) and business logic (service-specific, dev-supported).

## What this changes about staffing

Chapter 32's footnote makes the staffing consequence explicit (source: chapter-32-the-evolving-sre-engagement-model.md):

> The new model of service management changes the SRE staffing model in two ways: (1) because a lot of service technology is common, it reduces the number of required SREs per service; (2) it enables the creation of production platforms with separation of concerns between production platform support (done by SREs) and service-specific business-logic support, which remains with the development team. These platforms teams are staffed based upon the need to maintain the platform rather than upon service count, and can be shared across products.

Two payoffs follow:

- **Fewer SREs per service.** Because common infrastructure is supported once, not per service
- **Platform teams that scale by platform size, not service count.** An SRE platform team can support hundreds of services because the support surface is the platform, not each consumer

## Why this is a new relationship model

The shared-responsibility model changes the SRE-dev interaction in ways the earlier models couldn't. Under full SRE support, the development team essentially outsources production responsibility to SRE after onboarding. Under shared responsibility, both sides stay on the pager — SRE for the infrastructure layer, dev for the application layer — and the collaboration is continuous rather than hand-off-shaped. The [[production-meetings|weekly production meeting]] and [[sre-dev-collaboration|SRE-dev collaboration]] patterns from Chapter 31 have an even tighter version under this model because dev never leaves the operational loop.

## Related pages

- [[frameworks-and-sre-platform]]
- [[service-framework]]
- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[early-engagement-model]]
- [[sre-alternative-support]]
- [[sre-dev-collaboration]]
- [[production-meetings]]
- [[site-reliability-engineering]]
