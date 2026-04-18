# Testing at Scale

**Summary**: The dependency-closure problem that testing infrastructure has to solve at the size of Google's codebase. A small unit test has a small dependency list; a release test can depend transitively on every object in the repository. Practical test environments select **branch points** between versions and merges that resolve the maximum uncertainty for the minimum number of iterations.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The closure problem

> A small unit test might have a short list of dependencies: one source file, the testing library, the runtime libraries, the compiler, and the local hardware running the tests. A robust testing environment dictates that those dependencies each have their own test coverage, with tests that specifically address use cases that other parts of the environment expect. If the implementation of that unit test depends on a code path inside a runtime library that doesn't have test coverage, an unrelated change in the environment can lead the unit test to consistently pass testing, regardless of faults in the code under test. (source: chapter-17-testing-for-reliability.md)

The failure mode is insidious: the test passes, so the change looks safe, but the test passes for the *wrong reason* — a path it depended on in a shared library has behaviour changes that happen to make the green light come on regardless of the code under test.

The fix is recursive test coverage: every dependency needs its own coverage of the use cases that matter to it. Missing coverage is not localised — it leaks outward.

## The release-test closure explosion

> In contrast, a release test might depend on so many parts that it has a transitive dependency on every object in the code repository. If the test depends on a clean copy of the production environment, in principle, every small patch requires performing a full disaster recovery iteration. (source: chapter-17-testing-for-reliability.md)

Naïvely, every patch would trigger a full-system rebuild and re-run. That's computationally infeasible at Google scale (the book later derives a **~21,000-test baseline per service**, applied twice for before/after). The practical response:

> Practical testing environments try to select branch points among the versions and merges. Doing so resolves the maximum amount of dependent uncertainty for the minimum number of iterations. Of course, when an area of uncertainty resolves into a fault, you need to select additional branch points. (source: chapter-17-testing-for-reliability.md)

The testing system is making an **economic choice about which subset of the closure to actually exercise**. Build systems like [[blaze-bazel|Bazel]] make this selection possible by producing dependency graphs that expose exactly which tests a given file change affects.

## Footnote example of a shared-library hazard

The chapter's footnote on the dependency-path failure (source: chapter-17-testing-for-reliability.md):

> For example, code under test that wraps a nontrivial API to provide a simpler and backward-compatible abstraction. The API that used to be synchronous instead returns a future. Calling argument errors still deliver an exception, but not until the future is evaluated. The code under test passes the API result directly back to the caller. Many cases of argument misuse may not be caught.

The test's assertion logic is correct, but the observational window has moved: errors that used to surface synchronously now surface lazily, and the test's expectations haven't been updated.

## Cross-book connections

- [[blaze-bazel]] (Ch 8) — the build system whose dependency graphs enable selective test execution; Ch 17 explicitly credits Bazel's "only rebuild the part that depends on this file" feature
- [[hermetic-builds]] (Ch 8) — hermetic builds make the dependency graph trustworthy; without hermeticity, what the build tool *thinks* depends on what can diverge from what actually does
- [[simplicity-sre]] / [[minimal-apis]] (Ch 9) — smaller APIs have smaller transitive dependency closures; the simplicity discipline is a prerequisite for the dependency selection to produce manageable test sets

## Related pages

- [[testing-for-reliability]]
- [[blaze-bazel]]
- [[hermetic-builds]]
- [[test-flakiness-budget]]
- [[fake-backend-versions]]
