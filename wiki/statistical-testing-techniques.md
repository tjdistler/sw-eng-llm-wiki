# Statistical Testing Techniques

**Summary**: Non-deterministic test techniques — **fuzzing** (Lemon), **chaos engineering** (Chaos Monkey), **distributed-state property testing** (Jepsen) — that exercise code paths a hand-written test suite would not find. They are not repeatable in the deterministic sense: rerunning after a fix doesn't definitively prove the fault is gone. But they are highly useful at discovering failures, estimating fix confidence, and suggesting suspicious regions of code.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The three representatives Chapter 17 names

- **Lemon** — fuzzing tool for application-layer testing.
- **Chaos Monkey** (Netflix) — randomly kills production instances to verify the service survives. The name and pattern are the origin of the **chaos engineering** industry movement.
- **Jepsen** — property-based testing of distributed systems under adversarial network partitions, frequently applied to databases and coordination services.

## The repeatability caveat

> Statistical techniques, such as Lemon for fuzzing, and Chaos Monkey and Jepsen for distributed state, aren't necessarily repeatable tests. Simply rerunning such tests after a code change doesn't definitively prove that the observed fault is fixed. (source: chapter-17-testing-for-reliability.md)

A footnote drives the point home (source: chapter-17-testing-for-reliability.md):

> Even if the test run is repeated with the same random seed so that the task kills are in the same order, there is no serialization between the kills and the fake user traffic. Therefore, there's no guarantee that the actual previously observed code path will now be exercised again.

Randomness plus concurrency means a green run after a fix is consistent with the bug being fixed, or with the path simply not being re-exercised this time.

## Why they're still useful

Chapter 17 lists four concrete payoffs (source: chapter-17-testing-for-reliability.md):

1. **Log of actions**. The run's randomly-selected actions can be recorded — often just by logging the random-number-generator seed. That's enough to reconstruct the test trajectory.
2. **Refactor as a release test**. If the log shows a failure, replaying it a few times before filing the bug tells you the failure rate, which tells you how hard it will be to later assert the fix worked.
3. **Suggestive localisation**. Variations in how the fault expresses itself across runs help identify suspicious code regions.
4. **Escalation signal**. Later runs may surface even more severe failure situations, which justify escalating the bug's priority.

In other words: the test's non-determinism is a feature for discovery, and its logs + repeated replays are the mechanism by which it yields to conventional (more deterministic) test techniques.

## Connection to the canary

[[canary-test|Canary tests]] are in some sense the production-side cousin of statistical tests: both expose code to unpredictable traffic, both rely on variance reports and probabilistic estimates rather than clean pass/fail. Chapter 17 positions statistical tests as a pre-production way to shake loose the same kinds of faults a canary would find, with the benefit that the blast radius is test-infrastructure compute rather than user traffic.

## Cross-book connections

- Chaos engineering (Netflix, industry practice) — Chapter 17's brief mention of Chaos Monkey is the book's only explicit gesture toward chaos engineering; the field has since grown into DiRT ([[operational-underload]]'s organisational version at Google), Gremlin, and similar products
- [[fault-tolerance]] (Kleppmann / Burns) — the property statistical techniques are trying to verify; Kleppmann's fault/failure framing is the model they operate against
- [[byzantine-faults]] (Kleppmann) — Jepsen's test regime often approaches Byzantine-like conditions (stale, conflicting, partitioned views)
- [[test-and-treat]] (Ch 12) — the debugging-time analogue of running non-deterministic experiments to localise a bug
- [[negative-results]] (Ch 12) — Bosetti's publish-your-failures sidebar is the cultural scaffolding that makes the "log the seed, re-run, report rate" workflow a normal thing to do

## Related pages

- [[testing-for-reliability]]
- [[canary-test]]
- [[testing-disaster-recovery]]
- [[learning-from-outages]]
