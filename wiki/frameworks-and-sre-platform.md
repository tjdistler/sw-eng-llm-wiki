# Frameworks and SRE Platform

**Summary**: The structural evolution of [[sre-engagement-model|SRE engagement]] past per-service review. Rather than retrofit each service to SRE standards via a [[production-readiness-review|PRR]], Google builds [[service-framework|language-specific service frameworks]] that codify production best practices into code. Services built on the frameworks inherit reliability by construction, PRR becomes faster and cheaper, and SRE gains a common platform with uniform observability, configuration, and control surface.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The problems this model solves

Chapter 32 diagnoses the costs of the [[simple-prr-model|Simple PRR Model]] and [[early-engagement-model|Early Engagement Model]] that framework-based engagement is designed to attack (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Serialised onboardings.** Each PRR took 2-3 SREs over 2-3 quarters; insufficient SRE staffing forced strict prioritisation and long lead times
- **Reimplementation waste.** Production features (logging, load management, instrumentation) were implemented differently across services because of differing software practices. The same logging framework, for example, was re-written in the same language repeatedly because different services didn't share code structure
- **No easy replication of fixes.** Common failure modes (overload, hot-spotting) produced locally tailored fixes that didn't transfer between services
- **Local SRE contributions.** SRE-written software was usually service-specific, so new lessons couldn't be deployed across previously-onboarded services without revisiting each one

Plus external pressure (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Microservices trend.** More requests for SRE support, more services to support, and an expectation of lower deployment lead time that the months-long PRR model couldn't meet
- **Hiring constraints.** SRE hiring is slow and the training is lengthy
- **Non-SRE services.** The majority of Google services cannot justify direct SRE support but still need production-quality infrastructure

## The design principles

Chapter 32 lists four principles that the framework-based model satisfies (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Codified best practices.** Commit what works in production to code so services become "production-ready by design" by using it
- **Reusable solutions.** Common implementations of techniques for scalability and reliability that are easily shareable
- **Common production platform with a common control surface.** Uniform interfaces to production facilities, uniform operational controls, uniform monitoring, logging, and configuration
- **Easier automation and smarter systems.** A common control surface enables automation (e.g. a single view of outage-relevant information rather than hand-collected raw data)

## How frameworks decompose a service

An application is split into two parts (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Business logic** — the application-specific value
- **Infrastructure** — what SRE cares about; encapsulated in framework modules

Each framework module provides a cohesive solution for a problem domain or infrastructure dependency. Example module concerns:

- Instrumentation and metrics
- Request logging
- Control systems involving traffic and load management

A framework is prescriptive: it tells developers how a set of software components should be assembled and exposes cohesive controls over them. Chapter 32's example feature set (source: chapter-32-the-evolving-sre-engagement-model.md):

- Business logic organised as well-defined semantic components that can be referenced by standard names
- Standard dimensions for monitoring instrumentation
- Standard format for request-debugging logs
- Standard configuration format for managing [[load-shedding|load shedding]]
- A semantically consistent measure of per-server capacity and "overload" that feeds various control systems

## Multi-language frameworks with identical semantics

Google supports several application languages (Java, C++, Go in Chapter 32's list). Each has its own framework implementation. Though the implementations don't share code, the goal is for all of them to expose the same API, behaviour, configuration, and controls for identical functionality (source: chapter-32-the-evolving-sre-engagement-model.md). Development teams pick the language that fits their need; SRE gets the same familiar behaviour regardless of which one was chosen.

## Benefits

Chapter 32 enumerates the payoffs (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Significantly lower operational overhead.** Strong conformance tests for coding structure, dependencies, and style. Built-in service deployment, monitoring, and automation. Easier management of large numbers of services (including microservices). Idea-to-production-quality deployment in days
- **Universal support by design.** Services that can't justify full SRE engagement still use SRE-developed production features; framework users benefit from improvements made over time to framework modules. This breaks the SRE staffing barrier
- **Faster, lower-overhead engagements.** PRR execution gets faster — built-in features, faster service onboarding (typically a single SRE in one quarter), and less cognitive burden for the SRE team managing framework-based services
- **Shared-responsibility engagement model.** See [[shared-responsibility-engagement]]: SRE supports the platform infrastructure, development teams support application-specific bugs. A structural departure from the previous "full SRE or nothing" binary

## How this changes the PRR

A framework-based service doesn't eliminate the PRR; it cuts the effort. Chapter 32 describes a typical framework-era PRR as one SRE in one quarter with less cognitive burden on the SRE team (source: chapter-32-the-evolving-sre-engagement-model.md). The assessment and qualification effort drops because framework-built services start from a known-good baseline. The production-quality bar stays high.

## Related pages

- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[early-engagement-model]]
- [[production-readiness-review]]
- [[service-framework]]
- [[shared-responsibility-engagement]]
- [[sre-alternative-support]]
- [[site-reliability-engineering]]
