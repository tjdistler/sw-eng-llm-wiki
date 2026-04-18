# Testing for Reliability

**Summary**: Chapter 17 hub. Testing is the **mechanism by which SREs quantify confidence** that the system will stay reliable through change; each passing test reduces uncertainty that must otherwise be paid for with post-deploy monitoring. The chapter develops a two-axis taxonomy — **traditional vs production** tests — spells out the economics of test coverage at scale, and treats the testing infrastructure as an SRE-owned service in its own right.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Chapter thesis

> One key responsibility of Site Reliability Engineers is to quantify confidence in the systems they maintain. (source: chapter-17-testing-for-reliability.md)

Confidence has two halves: past reliability (from monitoring data) and future reliability (predicted from past behaviour plus the deltas introduced by change). Predictions about the future only hold under one of two conditions (source: chapter-17-testing-for-reliability.md):

- The site is unchanging (no releases, no fleet changes).
- Every change is describable with enough fidelity that analysis can allow for the uncertainty it introduces.

**Testing is the mechanism that demonstrates equivalence when changes occur.** A test that passes both before and after a change reduces the uncertainty the analysis must budget for. The more coverage, the more change you can safely ship before predicted reliability falls below the [[service-level-objective|SLO]].

## Two coverage axes

The chapter's central taxonomy:

| Axis | Category | Pages |
|---|---|---|
| Offline, hermetic | Traditional | [[unit-tests]], [[integration-tests]], [[system-tests]] (with [[smoke-tests]], [[performance-tests]], [[regression-tests]]) |
| Against live production | Production | [[configuration-test]], [[stress-tests]], [[canary-test]] |

Both are necessary. Traditional tests verify correctness of undeployed software; production tests verify that *the deployed system in its actual environment* is working.

## Zero MTTR testing

The bridge between testing and reliability that the chapter makes explicit:

> It's possible for a testing system to identify a bug with zero MTTR. Zero MTTR occurs when a system-level test is applied to a subsystem, and that test detects the exact same problem that monitoring would detect. Such a test enables the push to be blocked so the bug never reaches production. (source: chapter-17-testing-for-reliability.md)

Every bug caught this way never affects a user. **The more bugs testing catches with zero MTTR, the higher the effective [[mttr-and-mttf|MTBF]] experienced by users** — and the more aggressively the team can then release features. See [[zero-mttr-testing]].

## Testing the infrastructure itself

Because tests consume computational resources and produce per-test pass/fail indications that have their own statistical behaviour, the testing system is itself an SRE-supported service with its own reliability concerns:

- [[testing-at-scale]] — dependency closure; branch-and-merge test selection
- [[testing-scalable-tools]] — SRE-developed automation and disaster tools need their own tests
- [[testing-disaster-recovery]] — offline-checkpoint-style tools vs online repair tools
- [[statistical-testing-techniques]] — fuzzing, Chaos Monkey, Jepsen as non-repeatable but useful
- [[test-flakiness-budget]] — the 99.9999% per-test reliability floor derived from 21,000 tests × 1% rejection tolerance
- [[testing-deadlines]] — interactive (seconds) vs batch (minutes) tests; the engineer's context-switch deadline

## From build system to production

The chapter walks through the pipeline as a series of stages:

- [[build-system-discipline]] — source control + continuous build + fix-the-build-first culture; stability as an enabler of agility
- [[testing-entry-strategy]] — where to start when joining an untested project mid-stream
- [[hermetic-builds]] (Ch 8) — builds insensitive to machine; the property Bazel's dependency graphs enable
- [[fake-backend-versions]] — release tests need backend fakes; versioned and release-aligned
- [[production-probes]] — known-good and known-bad requests replayed as monitoring probes to catch frontend/backend release skew
- [[break-glass-push]] — emergency override with non-silenced tests and boosted priority

## Configuration as a first-class test target

The chapter spends unusual weight on configuration because the MTBF of a config file is often much shorter than the binary it configures, and because config can bypass the application release gate entirely:

- [[configuration-test]] — production test comparing checked-in config with actual running config; inherently non-hermetic
- [[configuration-integration-testing]] — treating config content as hostile input; protocol buffers beat YAML beats interpreted-language config for bounded-runtime load
- [[configuration-management-sre]] (Ch 8) — the four distribution models this chapter's tests protect

## Barrier defenses for risky tools

When SRE-developed software has to bypass the normal API (batch updates that disable transactions for speed, online repair tools, etc.), the chapter prescribes a structural defence against havoc:

- [[barrier-defenses]] — place a barrier so replicas fail health checks; the risky software only accesses unhealthy replicas; a tested tool removes the barrier on completion.
- [[testing-automation-tools]] — automation's "side effect is an invisible discontinuity to another API client" characteristic; testing the other layer before and after the change

## Cross-book connections

- [[end-to-end-testing]] (Newman / Bellemare) — Chapter 17's traditional-vs-production axis pairs naturally with Newman's test-pyramid narrowing: the wider the test, the more value pushing it to production (probes, canary) rather than hermetic pre-deploy captures
- [[unit-testing-topology-functions]] / [[topology-testing]] / [[local-integration-testing]] / [[remote-integration-testing]] (Bellemare) — the EDM-specific realisations of unit / integration / system testing; Bellemare's pyramid is Ch 17's traditional column applied to event-driven services
- [[architecture-fitness-function]] (Richards & Ford) — every test in this chapter, from a unit test to a production probe, is an objective automatable integrity assessment; Ch 17 is the reliability-specific catalog of fitness-function implementations
- [[progressive-delivery]] (Newman / Burns) — canary tests are the named progressive-delivery mechanism; Chapter 17 adds the mathematical framing (exponential rollout; order-of-fault estimate)
- Chaos engineering (industry practice, Netflix) — Chapter 17 cites [[statistical-testing-techniques|Chaos Monkey]] explicitly; the chapter's statistical-testing section is the SRE-book's earliest treatment of the family
- [[synthetic-transactions]] (Newman) / [[prober]] — production probes in Ch 17 are the test-originated synthetic transaction; Prober is the monitoring tool that runs them continuously

## Related pages

- [[zero-mttr-testing]]
- [[unit-tests]]
- [[integration-tests]]
- [[system-tests]]
- [[smoke-tests]]
- [[performance-tests]]
- [[regression-tests]]
- [[configuration-test]]
- [[stress-tests]]
- [[canary-test]]
- [[testing-at-scale]]
- [[testing-scalable-tools]]
- [[testing-automation-tools]]
- [[testing-disaster-recovery]]
- [[statistical-testing-techniques]]
- [[test-flakiness-budget]]
- [[testing-deadlines]]
- [[break-glass-push]]
- [[build-system-discipline]]
- [[testing-entry-strategy]]
- [[barrier-defenses]]
- [[production-probes]]
- [[fake-backend-versions]]
- [[configuration-integration-testing]]
- [[mttr-and-mttf]]
- [[change-management-sre]]
- [[hermetic-builds]]
- [[site-reliability-engineering]]
