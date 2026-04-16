# Progressive Delivery

**Summary**: Umbrella term coined by James Governor for techniques that control how software is rolled out to users in a nuanced way — allowing faster releases while validating efficacy and limiting blast radius. Includes [[parallel-run-pattern|parallel run]], canary release, dark launch, and feature toggles.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

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

## Automated release remediation

Chapter 5 takes progressive delivery further: once you have measurable acceptance thresholds (95th-percentile latency, error rate), the rollout decision can be automated (source: chapter-05-growing-pains.md). If thresholds are met, the rollout continues; if not, automated rollback. Netflix's **Spinnaker** is the canonical example.

Newman frames this as part of the response to [[end-to-end-testing|end-to-end testing's diminishing returns]]:

> "I'm not saying you should consider automated release remediation instead of testing, just that you should think about where you get the best return on your effort. You may end up with a far more robust system by putting some work into catching problems if they do occur, rather than just focusing on stopping problems from happening in the first place." (source: chapter-05-growing-pains.md)

Even *manual* progressive delivery — without automated rollback — is a big step up from rolling out to all users at once.

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
