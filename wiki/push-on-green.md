# Push on Green

**Summary**: A release model in which **every build that passes all tests is automatically deployed to production** — no human decision between "green" and "live." Some Google teams adopt push-on-green for user-facing software; it is the logical limit of [[high-release-velocity]] and rests on [[hermetic-builds]], continuous testing, [[change-management-sre|automated progressive rollout and rollback]], and an [[error-budget]] that tolerates occasional regressions.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-08-release-engineering.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The model

Chapter 8 names the pattern directly:

> Other teams have adopted a "Push on Green" release model and deploy every build that passes all tests. (source: chapter-08-release-engineering.md)

Chapter 2 had already mentioned push-on-green as the end state of the [[google-monorepo|monorepo]] workflow — continuous testing on each CL plus an automatic promotion step for projects that opt in (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Why the model is viable

Push-on-green collapses the human review step between "tests pass" and "production deploy." Several preconditions have to be in place for this to be safe:

- **[[hermetic-builds]]** — the thing tested is byte-identical to the thing deployed.
- **High test coverage on mainline** — tests are the gate, so they have to be trustworthy.
- **[[release-branching-and-cherry-picking|Build from continuous-test revisions]]** — the chapter recommends creating releases at the revision of the last continuous test build that successfully completed all tests, which is the push-on-green-compatible shape.
- **[[change-management-sre|Automation trio]]** — progressive rollout + fast detection + safe rollback, because some regressions will escape tests.
- **[[error-budget]]** — the model presumes the [[service-level-objective|SLO]] leaves room for occasional regressions that get caught in rollout.
- **[[rapid-release-system|Rapid]] + [[sisyphus]]** — the orchestration that actually performs the push.

Without these, push-on-green is not velocity — it is hope.

## The velocity argument

Why adopt it? Because it is the endpoint of the [[high-release-velocity]] logic chain:

1. Frequent releases → fewer changes per release → smaller blast radius.
2. Smaller blast radius → higher tolerance for releasing more often.
3. Human decisions in the middle of that loop are the bottleneck.

Remove the human and the loop runs as fast as the tooling allows.

## The test-reliability floor (Chapter 17)

Push-on-green puts the tests in the release-gate position. That makes the per-test reliability floor the whole-service's reliability floor. Chapter 17 derives the number: with ~21,000 tests run twice per patch (before and after) and a user tolerance of ~1% incorrect patch rejections, **each test must pass correctly over 99.9999% of the time** (source: chapter-17-testing-for-reliability.md). See [[test-flakiness-budget]].

The implication for push-on-green: before going live with the model, the team must deal with test flakiness aggressively. A push-on-green pipeline with 99% per-test reliability would reject nearly every patch; a human-gated pipeline can tolerate it.

## Connection to the error budget

Chapter 1 framed 1%-experiments and progressive rollouts as ways to **free up error budget**: each low-risk release consumes little budget, which lets you release more often. Push-on-green is the operational discipline that actually does release more often — it is what the error-budget framing enables at the top end.

## Cross-book connections

- [[continuous-integration-delivery-deployment]] (Bellemare) — push-on-green is Bellemare's "continuous deployment" tier; his warning that stateful services make continuous deployment hard is the caveat for why not every Google service does push-on-green
- [[progressive-delivery]] (Newman / Burns) — push-on-green relies entirely on progressive-delivery techniques to be safe; without them it would be "push every build to everyone."
- [[change-management-sre]] — push-on-green is the regime in which change management stops being a phase and becomes a continuous system property

## Related pages

- [[release-engineering]]
- [[high-release-velocity]]
- [[hermetic-builds]]
- [[rapid-release-system]]
- [[sisyphus]]
- [[change-management-sre]]
- [[error-budget]]
- [[progressive-delivery]]
- [[continuous-integration-delivery-deployment]]
- [[google-monorepo]]
- [[testing-for-reliability]]
- [[test-flakiness-budget]]
- [[zero-mttr-testing]]
