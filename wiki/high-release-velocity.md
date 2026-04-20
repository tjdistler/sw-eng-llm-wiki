# High Release Velocity

**Summary**: The second of the four [[release-engineering-principles]]. User-facing software is rebuilt frequently because **frequent releases mean fewer changes between versions**, which makes testing and troubleshooting easier. Some Google teams build hourly and select the best build to deploy; others adopt [[push-on-green]] and deploy every build that passes tests.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`, `raw/site-reliability-engineering/chapter-09-simplicity.md`

**Last updated**: 2026-04-17

---

## The principle

> We have embraced the philosophy that frequent releases result in fewer changes between versions. This approach makes testing and troubleshooting easier. (source: chapter-08-release-engineering.md)

The logic chain:

1. Fewer changes per release → smaller blast radius if something breaks.
2. Smaller blast radius → faster triage.
3. Faster triage → higher confidence in releasing often.

Velocity reinforces itself.

## Two release cadences

The chapter describes two patterns Google teams use (source: chapter-08-release-engineering.md):

### Hourly builds with selective deployment

- Build every hour.
- A pool of candidate builds accumulates.
- Pick one to deploy based on test results and which features it contains.

This decouples build cadence from deploy cadence — teams can cut a release whenever a build with the right feature set is green.

### Push on green

- Every build that passes all tests is deployed.
- No human picks.

See [[push-on-green]] for the full pattern, the prerequisites that make it safe, and its dependence on [[change-management-sre|progressive rollouts]] and [[error-budget|error budgets]] to tolerate the occasional regression.

## Why it works at Google specifically

High velocity of this kind is not a configuration setting — it is a consequence of everything else in the chapter:

- [[hermetic-builds]] so that each build is a known quantity
- [[rapid-release-system|Rapid]] plus a hermetic build tool and content-addressed package manager so that "build hourly" is cheap
- Continuous testing on the mainline so builds are already tested before release selection
- [[self-service-release-model]] so that teams don't have to queue at a central release team
- [[change-management-sre]] automation (progressive rollout + detection + rollback) so that a bad build doesn't mean a big outage

## Cross-book connections

- [[progressive-delivery]] — high velocity only makes sense if the *safety* of each release is decoupled from the *frequency*; progressive delivery is what decouples them
- [[error-budget]] — velocity is paid for with error budget; Chapter 1 framed 1%-experiments and progressive rollouts explicitly as ways to *free up* budget so you can release more often
- [[continuous-integration-delivery-deployment]] (Bellemare) — the "continuous deployment" tier is the same idea applied per-service

## The Chapter 9 restatement

Chapter 9 makes the same argument from a different direction under the heading **Release Simplicity** (source: chapter-09-simplicity.md):

> Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously.

Luebbe compares the resulting cadence to gradient descent: many small steps, each evaluated for improvement or regression. Chapter 8's starting point is engineering efficiency ("fewer changes per release means easier testing"); Chapter 9's starting point is simplicity as a virtue ("one change is easier to reason about than ten"); both converge on the same pattern. See [[release-simplicity]] for the Chapter 9 framing and [[simplicity-sre]] for the surrounding argument.

## Related pages

- [[release-engineering]]
- [[release-engineering-principles]]
- [[push-on-green]]
- [[hermetic-builds]]
- [[change-management-sre]]
- [[error-budget]]
- [[progressive-delivery]]
- [[release-simplicity]]
- [[simplicity-sre]]
