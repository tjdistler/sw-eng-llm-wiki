# Zero MTTR Testing

**Summary**: A system-level test applied to a subsystem such that the test detects the exact problem monitoring would detect in production — but catches it at push time. Repairing a bug found this way takes **zero production MTTR**: the push is blocked, the user never sees the failure. The concept reframes testing as the most effective [[mttr-and-mttf|MTTR]] lever available to SRE.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> It's possible for a testing system to identify a bug with zero MTTR. Zero MTTR occurs when a system-level test is applied to a subsystem, and that test detects the exact same problem that monitoring would detect. Such a test enables the push to be blocked so the bug never reaches production (though it still needs to be repaired in the source code). (source: chapter-17-testing-for-reliability.md)

The word **zero** is precise: zero time elapses between the bug's detection and the production service being "repaired" against it, because the bug is blocked from reaching production at all. The source code still has the defect — that repair time is engineering work, not operational MTTR.

## Why the framing matters

Passing tests do not prove reliability; failing tests prove absence of reliability (source: chapter-17-testing-for-reliability.md). A monitoring system can find bugs too — but only as fast as the reporting pipeline reacts, which is longer than zero. The test that catches the same problem monitoring would catch, but at the release gate, strictly dominates monitoring on MTTR.

The implication for [[mttr-and-mttf|MTBF]]:

> The more bugs you can find with zero MTTR, the higher the Mean Time Between Failures (MTBF) experienced by your users. As MTBF increases in response to better testing, developers are encouraged to release features faster. (source: chapter-17-testing-for-reliability.md)

User-experienced reliability rises because user-visible failures become rarer. The velocity feedback loop follows naturally — better testing enables more frequent releases, each of which further exercises the testing pipeline.

## Which tests achieve zero MTTR

Not every test does. The requirement is that the test **detects the same problem monitoring would detect**. That usually means a system-level test of some size — a [[smoke-tests|smoke test]], an [[integration-tests|integration test]] with realistic inputs, or a release test that replays known-good and known-bad requests (see [[production-probes]]).

A unit test that catches a function-level bug before it composes into a user-visible symptom is earlier-than-zero-MTTR: it prevents the bug from ever manifesting in aggregate. But the chapter's concept specifically captures the class of bug that *would* have shown up in production monitoring if unblocked — tests that pre-empt the alert.

## Connection to the error budget

Zero-MTTR bugs cost no [[error-budget]]. Bugs that escape to production and are detected by monitoring consume budget during their repair window. Shifting bug detection leftward moves it out of the budget entirely, which is why [[change-management-sre|progressive rollouts]] and testing together are the two levers SRE emphasises.

## Related pages

- [[mttr-and-mttf]]
- [[testing-for-reliability]]
- [[system-tests]]
- [[production-probes]]
- [[error-budget]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
