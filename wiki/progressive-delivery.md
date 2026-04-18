# Progressive Delivery

**Summary**: Umbrella term coined by James Governor for techniques that control how software is rolled out to users in a nuanced way — allowing faster releases while validating efficacy and limiting blast radius. Includes [[parallel-run-pattern|parallel run]], canary release, dark launch, and feature toggles.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The idea

Releasing software is not a single binary event. Progressive delivery decomposes the release into a controlled sequence of exposure: deploy first, expose to a small population, observe, then expand (source: chapter-03-splitting-the-monolith.md). The umbrella term unifies several specific techniques that all share the goal of reducing the impact of bad releases while preserving release velocity.

The central enabler is the separation of [[deployment-vs-release|deployment from release]]: software in production is not necessarily software in use.

## The techniques

### Canary release

A subset of users is routed to the new code; the rest continue to use the old. If something is wrong, only the canary subset is affected and you roll back routing — not code. The selection mechanism can be by user ID, geography, account type, or random sampling at the proxy/load balancer (source: chapter-03-splitting-the-monolith.md).

### Dark launch

The new functionality is *deployed and exercised* but invisible to users — for example, the new code processes a copy of every request but no result is shown. Used to validate behaviour and load characteristics before flipping it on (source: chapter-03-splitting-the-monolith.md).

### Parallel run

A specific implementation of dark launching: both old and new run on every call, with results compared. The old is authoritative until the new earns trust. See [[parallel-run-pattern]] for the depth (source: chapter-03-splitting-the-monolith.md).

### Feature toggles

Configuration-driven switches that turn capability on or off at runtime, often per-user or per-segment. See [[feature-toggle]] (source: chapter-03-splitting-the-monolith.md).

## Implementation via ambassadors

At the container level, all three traffic-shaping techniques above — canary, dark launch, and parallel run — can be implemented by an ambassador container running in the application's pod. Burns's Chapter 3 [[request-splitting|10%-experiment nginx ambassador]] is a canary release; the same tool teeing both backends is a dark launch or parallel run (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). An ambassador-level implementation is language-agnostic and needs no cooperation from the application — a complement to in-process [[feature-toggle|feature toggles]] rather than a replacement. See [[ambassador-pattern]] and [[request-splitting]].

## Automated release remediation

Chapter 5 takes progressive delivery further: once you have measurable acceptance thresholds (95th-percentile latency, error rate), the rollout decision can be automated (source: chapter-05-growing-pains.md). If thresholds are met, the rollout continues; if not, automated rollback. Netflix's **Spinnaker** is the canonical example.

Newman frames this as part of the response to [[end-to-end-testing|end-to-end testing's diminishing returns]]:

> "I'm not saying you should consider automated release remediation instead of testing, just that you should think about where you get the best return on your effort. You may end up with a far more robust system by putting some work into catching problems if they do occur, rather than just focusing on stopping problems from happening in the first place." (source: chapter-05-growing-pains.md)

Even *manual* progressive delivery — without automated rollback — is a big step up from rolling out to all users at once.

## The SRE framing: 70% of outages come from change

Google SRE's Chapter 1 reaches the same recipe from a different starting point (source: raw/site-reliability-engineering/chapter-01-introduction.md):

> SRE has found that roughly 70% of outages are due to changes in a live system.

The response is a three-part automation trio that is essentially progressive delivery restated as change-management discipline:

1. **Progressive rollouts**.
2. **Quickly and accurately detecting problems**.
3. **Rolling back changes safely**.

Chapter 1 frames progressive rollouts and 1% experiments as ways to *free up* [[error-budget]]: if you can launch something without consuming much budget, you can launch more often. This closes the loop between [[change-management-sre|change management]] and velocity. See [[change-management-sre]] for the full SRE framing.

## The SRE Ch 27 elaboration: launches as the distinctive case

SRE Chapter 27 specialises the progressive-delivery recipe for product launches, at up to 70 per week at Google scale. Chapter 27's additions:

- [[gradual-rollout]] is the staged-rollout pattern, at three typical stages (subset in one datacenter → whole datacenter → global) with observation windows between. Client-fleet variants cover Android app rollouts to install fractions; invite systems are the sign-up-rate-limited variant.
- [[feature-flag-framework]] is infrastructure for running many small changes in parallel, each revertible independently — two styles (HTTP-payload rewriter for stateless UI, request routing for stateful business logic) that absorb the launch process for flag-gated changes.
- [[abusive-client-behavior]] names the dormant-functionality pattern: ship code inactive, activate server-side. The server-controlled client configuration makes emergency rollback possible without a client-binary update.
- [[launch-checklist]] and [[launch-checklist-themes]] encode the cross-cutting concerns (capacity, failure modes, client behaviour, external dependencies, rollout planning) into a single curated instrument that every launch crosses.

## Why it matters in microservice migration

Migration is exactly when bad releases are most likely: new code, new operational profile, new dependencies. Progressive delivery techniques let you take the migration step in production with the safety net of fast, reversible exposure (source: chapter-03-splitting-the-monolith.md). Both [[strangler-fig-pattern]] and [[branch-by-abstraction]] explicitly hand off to progressive delivery techniques at the cutover step.

## Related pages

- [[parallel-run-pattern]]
- [[feature-toggle]]
- [[deployment-vs-release]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[incremental-migration]]
- [[end-to-end-testing]]
- [[synthetic-transactions]]
- [[ambassador-pattern]]
- [[request-splitting]]
- [[service-mesh]]
- [[edm-deployment-patterns]]
- [[blue-green-deployment]]
- [[change-management-sre]]
- [[error-budget]]
- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
- [[launch-checklist]]
- [[gradual-rollout]]
- [[feature-flag-framework]]
- [[abusive-client-behavior]]
