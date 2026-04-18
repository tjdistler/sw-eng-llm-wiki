# Test Flakiness Budget

**Summary**: When 21,000 tests are run twice (once before and once after a patch) to validate a single CL, and users tolerate roughly 1 incorrect patch rejection in 100, individual tests must pass correctly **over 99.9999% of the time**. The chapter's derivation is a startling concrete illustration of how much the per-test flakiness floor tightens as test counts grow, and of why even "rarely flaky" tests are an unaffordable luxury at scale.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The derivation

Chapter 17's scenario (source: chapter-17-testing-for-reliability.md): an engineer works on a service with 21,000 simple tests and occasionally proposes a patch. To validate, you compare the pass/fail vector **before** the patch with the pass/fail vector **after** — that's 42,000 test outcomes per CL. A favourable comparison provisionally qualifies the codebase as releasable.

User tolerance:

> It seems likely that users would vehemently complain if 1 in 10 patches is rejected. But a rejection of 1 patch among 100 perfect patches might go without comment. (source: chapter-17-testing-for-reliability.md)

So the system's incorrect-rejection rate per patch is 0.01 (one in a hundred). The chapter then computes the required per-test reliability:

> This means you're interested in the 42,000th root of 0.99. This calculation ... suggests that those individual tests must run correctly over 99.9999% of the time. (source: chapter-17-testing-for-reliability.md)

Six nines per test. The chapter's deadpan "Hmm." lands after the calculation.

## The implication

Most tests are not 99.9999% reliable. A test that's 99% reliable is unacceptable — in a 42,000-outcome run it would produce hundreds of false negatives and reject nearly every CL. Even 99.99% reliability only gets you part of the way: `0.9999^42000 ≈ 0.015`, still a 98.5% rejection rate on good patches.

The consequences for test design:

- **Hermeticity is not optional.** A test that sometimes depends on network or shared state fails more than once in a million runs.
- **Determinism is not optional.** Order-dependent tests, wall-clock-sensitive tests, and tests that race with their fixtures are all forms of flake.
- **Flaky tests must be removed aggressively.** One flake-per-week test among 42,000 is enough to degrade the CL validation experience materially.

## Blame allocation

> Engineers who use the testing infrastructure want to know if their code — usually a tiny fraction of all the source behind a given test run — is broken. Often, not being broken implies that any observed failures can be blamed on someone else's code. In other words, the engineer wants to know if their code has an unanticipated race condition that makes the test flaky (or more flaky than the test already was due to other factors). (source: chapter-17-testing-for-reliability.md)

Test-flakiness attribution is itself a statistical problem. The test infrastructure has to estimate, across 42,000 outcomes affected by many concurrent scenarios, which failures are "the engineer's fault" vs background noise. Chapter 17 flags this as one of the harder operational challenges of running a large shared test service.

## Cross-book connections

- [[testing-at-scale]] — the dependency-closure problem that produces the 21,000-test count in the first place
- [[testing-deadlines]] — flakiness interacts badly with deadlines: a flaky test that fails within the interactive window forces a rerun which misses the deadline
- [[architecture-fitness-function]] (Richards & Ford) — the six-nines floor is the reliability budget for individual fitness functions in a service with thousands of them; a weakly-reliable fitness function becomes net noise

## Related pages

- [[testing-for-reliability]]
- [[testing-at-scale]]
- [[testing-deadlines]]
- [[statistical-testing-techniques]]
