# Testing Deadlines

**Summary**: Tests have an **informal deadline**: the point at which the engineer context-switches to the next task. Chapter 17 draws a hard line between tests that meet this deadline (interactive, self-contained, seconds on a laptop) and tests that cannot (batch, orchestrated, minutes to hours). Batch tests are saying "not ready for review" to the reviewer, not "don't close the tab" to the author.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The interactive / batch split

> Most tests are simple, in the sense that they run as a self-contained hermetic binary that fits in a small compute container for a few seconds. These tests give engineers interactive feedback about mistakes before the engineer switches context to the next bug or task. Tests that require orchestration across many binaries and/or across a fleet that has many containers tend to have startup times measured in seconds. Such tests are usually unable to offer interactive feedback, so they can be classified as batch tests. Instead of saying "don't close the editor tab" to the engineer, these test failures are saying "this code is not ready for review" to the code reviewer. (source: chapter-17-testing-for-reliability.md)

The observation is economic, not technical. A fast test can keep the author's attention; a slow test necessarily addresses a different audience (the reviewer, the CI dashboard, a batch report). Both are legitimate — they just serve different phases of the work.

## The engineer's context switch

> The informal deadline for the test is the point at which the engineer makes the next context switch. Test results are best given to the engineer before he or she switches context, because otherwise the next context may involve XKCD compiling. (source: chapter-17-testing-for-reliability.md)

The XKCD reference (303 — "Compiling") is to the classic comic of programmers treating slow builds as authorised downtime. Context switches are expensive cognitive overhead; tests that finish before the switch keep the engineer in-flow.

## The implication for test suite design

Fast tests dominate the pyramid because they meet the deadline. They dictate:

- **Unit-test counts in the thousands**, run per save or per commit.
- **Integration tests running selectively**, based on [[testing-at-scale|Bazel-style dependency closure]].
- **System and release tests running as batch**, on CI runners, with results surfaced on the CL for the reviewer.

A test suite dominated by batch tests — because the unit suite isn't comprehensive enough to be worth running, or because every test requires a multi-container fleet — produces the frustration the chapter alludes to: the engineer never gets feedback in time to act on it.

## Cross-book connections

- [[test-flakiness-budget]] — the reliability floor; a flaky batch test that fails an hour after the commit wastes even more attention than a flaky interactive test
- [[hermetic-builds]] / [[blaze-bazel]] (Ch 8) — the infrastructure that makes fast selective tests possible; without dependency graphs every patch triggers the slow suite
- [[build-system-discipline]] — the continuous-build notification loop is the batch-test-feedback channel; Ch 17 argues it must be as short as technically feasible

## Related pages

- [[testing-for-reliability]]
- [[testing-at-scale]]
- [[test-flakiness-budget]]
- [[build-system-discipline]]
