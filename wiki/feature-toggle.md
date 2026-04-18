# Feature Toggle

**Summary**: A configuration-driven switch that selects between alternative code paths at runtime. In a microservice migration, toggles let you flip between old and new implementations without redeploying — making rollback fast and explicit. Pair with [[branch-by-abstraction]] and [[strangler-fig-pattern]] to control cutover.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## What it is

A feature toggle (or feature flag) is configuration that decides which code path runs. In a migration context, the toggle picks between the in-monolith implementation and the new microservice implementation of the same functionality (source: chapter-03-splitting-the-monolith.md). Pete Hodgson's [feature toggles article](https://martinfowler.com/articles/feature-toggles.html) is Newman's recommended deeper reference.

## Why use them in migration

Toggles support the central discipline of incremental migration: each step should be reversible (source: chapter-03-splitting-the-monolith.md). Specifically:

- **Fast rollback** if the new implementation misbehaves — flip a config value, no redeploy.
- **Explicit configuration state** — the desired routing is visible in one place rather than implicit in code.
- **Decouple deployment from release** — deploy the new code with toggle off, validate in production, then toggle on (see [[deployment-vs-release]]).
- **Coordinate with other migration patterns** — branch by abstraction's switch step is a natural toggle home; strangler fig redirection rules can be expressed as toggles in the proxy.

## Toggle hygiene

Newman's standing warning: **clean up dead toggles** (source: chapter-03-splitting-the-monolith.md). The classic pathology of feature flags is leaving them in place after the migration completes — flag combinatorics quickly become a maintenance problem and a source of bugs.

When the migration is done:

1. Remove the old code path.
2. Remove the toggle.
3. Optionally remove the abstraction the toggle switched on, if it was created purely for migration.

## Why Agile makes this pattern practical

Richards and Ford name feature toggles — alongside the [[strangler-fig-pattern|strangler pattern]] — as a restructuring technique that Agile methodologies enable (source: chapter-01-introduction.md). The tight feedback loop of an iterative process is what lets a toggle be deployed, exercised in production, and flipped on with confidence. On planning-heavy processes without frequent integration, the rollback advantage of a toggle cannot be cashed in because cutovers happen too rarely for toggle infrastructure to be worth the investment.

## The SRE Ch 27 framework framing

SRE Chapter 27 extends the feature-toggle concept to [[feature-flag-framework|feature flag *frameworks*]] — infrastructure that lets hundreds of small changes roll out in parallel, each to a few servers/users/entities, independently revertible. Two classes:

- HTTP-payload rewriter at the frontend (for stateless UI changes)
- Request routing to different servers (for stateful or business-logic changes)

The framework framing matters because it collapses per-toggle launch overhead: the framework is hardened once, and subsequent changes inherit its mechanics rather than each re-inventing small rollout/revert machinery. This is an organisation-scale answer to the "clean up dead toggles" hygiene problem — with a standardised framework, toggles live in managed infrastructure, not scattered across service repos.

Chapter 27 also introduces the **dormant-functionality** pattern ([[abusive-client-behavior]]): client-side code for a new feature is shipped inactive ahead of the server-side activation. Aborting the launch becomes a config flip rather than a client binary rollback.

## Related pages

- [[branch-by-abstraction]]
- [[strangler-fig-pattern]]
- [[parallel-run-pattern]]
- [[deployment-vs-release]]
- [[progressive-delivery]]
- [[incremental-migration]]
- [[feature-flag-framework]]
- [[abusive-client-behavior]]
- [[reliable-product-launches]]
