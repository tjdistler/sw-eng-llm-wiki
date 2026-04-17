# Architecture Governance

**Summary**: The practice of steering a software project so that its architectural decisions, characteristics, and design principles are actually upheld in the code base. Richards and Ford's Chapter 6 treatment — the modern form of architecture governance is automated: declared properties are enforced by [[architecture-fitness-function|fitness functions]] that run in the continuous-integration pipeline.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`

**Last updated**: 2026-04-16

---

## What governance means here

The word **governance** derives from the Greek *kubernan* ("to steer") (source: chapter-06-measuring-and-governing-architecture-characteristics.md). In software it covers any aspect of the development process that an architect (or enterprise architect, or architecture review board) wants to exert influence over: quality, security, modularity, layer discipline, dependency rules, deprecation timelines, licence compliance, performance budgets, anything the team has agreed should not drift.

Governance is distinct from coding: developers write features; governance ensures those features do not silently break the system's architectural invariants. Richards and Ford cite modularity as the canonical example — important but rarely urgent, so it loses to any feature deadline unless the architect has an automated check enforcing it (source: chapter-06-measuring-and-governing-architecture-characteristics.md).

Governance is also distinct from [[architecture-decisions-vs-design-principles|architecture decisions]]: decisions say *what the rule is*; governance is *how you make sure the rule holds*.

## The historical pattern

The chapter frames governance through an incrementalist lens (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

1. **Extreme Programming** pushed for continuous automation of unit tests.
2. **Continuous integration** extended that automation to build + integration on every commit.
3. **DevOps** extended automation further into deployment and operations.
4. **Architecture governance** is the latest layer — automate the checks that preserve architectural properties.

Each layer shortens the feedback loop between intent and violation. Code reviews catch problems days later; CI catches them minutes later; production monitors catch them seconds later. The book's thesis is that the same shift-left pattern applies to architectural invariants.

## Mechanisms

The load-bearing mechanism for automated governance is the [[architecture-fitness-function|architecture fitness function]]: an objective, automatable check attached to a named architecture characteristic (source: chapter-06-measuring-and-governing-architecture-characteristics.md). See that page for the full taxonomy of fitness-function types (atomic vs holistic, triggered vs continual, static vs dynamic, etc.) and for the concrete tool examples (JDepend, ArchUnit, NetArchTest, Netflix's Simian Army).

Other governance mechanisms that cooperate with fitness functions:

- **Architecture Decision Records (ADRs)** — capture the *why* behind a rule so the fitness function isn't an inscrutable failure (see [[architecture-decisions-vs-design-principles]]).
- **Architecture Review Boards (ARBs)** — for variance and exception handling when a rule must be relaxed.
- **Code reviews** — useful but too slow for frequent rules; reserve for judgement-heavy decisions.
- **Runtime monitors** — fitness functions that live in production rather than CI; appropriate for performance and availability.
- **[[monitoring-and-observability|Observability]]** — the substrate for runtime fitness functions.

## Why automate

Code reviews catch problems late. Richards and Ford's worked example: a team without a cyclic-dependency check lets developers auto-import classes across modules for a week; by the time code review happens, the damage is done and unwinding it is expensive (source: chapter-06-measuring-and-governing-architecture-characteristics.md). Automated governance prevents the cycle from being introduced in the first place.

The deeper argument: developers juggle dozens or hundreds of priorities. Governance concerns (modularity, security, layer discipline) are important but rarely urgent, so they lose attention. Automation converts important-but-not-urgent concerns into hard CI failures that developers cannot defer without explicit action.

## The Checklist Manifesto framing

Richards and Ford reach for Atul Gawande's *The Checklist Manifesto* as an analogy (source: chapter-06-measuring-and-governing-architecture-characteristics.md). Airline pilots and surgeons use checklists not because they don't know their jobs, but because high-repetition expert work makes details easy to miss. A succinct checklist is a reminder that doesn't depend on vigilance.

> This is the correct perspective on fitness functions — rather than a heavyweight governance mechanism, fitness functions provide a mechanism for architects to express important architectural principles and automatically verify them. (source: chapter-06-measuring-and-governing-architecture-characteristics.md)

The framing matters for how governance is sold to teams. It's not surveillance; it's the same discipline that keeps surgeons from leaving tools inside patients.

## Common governance checks

The chapter and the wiki's surrounding pages suggest a starter set:

- **Cyclic dependency detection** — JDepend-style package-graph check; no module may participate in a cycle.
- **Layer-discipline rules** — ArchUnit or NetArchTest: presentation may not depend on persistence, services may not depend on controllers, etc.
- **[[cyclomatic-complexity|Cyclomatic-complexity]] thresholds** — fail CI for any method above an agreed ceiling.
- **Distance-from-the-main-sequence** — JDepend check that no package drifts into the zone of pain or uselessness (see [[coupling-metrics]]).
- **Security scans** — Dependabot-style CVE detection, OWASP-style lint.
- **Deprecation countdown timers** — fitness functions that fail once a deprecation grace period elapses.
- **Performance budgets** — CI-level p95 latency checks, K-weight budgets for frontend bundles.
- **Chaos experiments** — holistic runtime fitness functions verifying fault tolerance (see [[fault-tolerance]]).

Each item on the list is a fitness function attached to a named characteristic. The act of writing the check documents the invariant.

## Collaboration, not imposition

The chapter is explicit that fitness functions must not be handed down from an ivory tower (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

> The intent is not for a group of architects to ascend to an ivory tower and develop esoteric fitness functions that developers cannot understand. Architects must ensure that developers understand the purpose of the fitness function before imposing it on them.

The "distance from the main sequence" check is the test case: the metric is esoteric and useless if the developers whose code it gates cannot read it. Governance that developers cannot interpret is governance that will be worked around.

## Relation to other wiki concepts

- [[architecture-fitness-function]] — the mechanism. This page is the umbrella; the fitness-function page is the deep dive.
- [[architecture-vitality]] — governance prevents structural decay.
- [[evolutionary-architecture]] — fitness-function-driven governance is what makes evolution safe.
- [[architecture-decisions-vs-design-principles]] — decisions produce hard pass/fail fitness functions; principles produce monitors.
- [[architect-expectations]] — expectation #4 (ensure compliance) is largely this page in automated form.
- [[measuring-architecture-characteristics]] — governance presupposes objective measurement.
- [[desired-state-management]] — operational analogue of the same pattern: declare the property, let automation maintain it.

## Related pages

- [[architecture-fitness-function]]
- [[measuring-architecture-characteristics]]
- [[cyclomatic-complexity]]
- [[architecture-characteristics]]
- [[architecture-decisions-vs-design-principles]]
- [[architecture-vitality]]
- [[evolutionary-architecture]]
- [[architect-expectations]]
- [[coupling-metrics]]
- [[fault-tolerance]]
- [[fundamentals-of-software-architecture]]
