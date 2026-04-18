# Regression Tests

**Summary**: A [[system-tests|system test]] (or integration test) that preserves a historically fixed bug as a recurring assertion. The test suite becomes a "gallery of rogue bugs" — engineers refactoring the codebase are protected against re-introducing failures the organisation has already paid to eliminate.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> Another type of system test involves preventing bugs from sneaking back into the codebase. Regression tests can be analogized to a gallery of rogue bugs that historically caused the system to fail or produce incorrect results. By documenting these bugs as tests at the system or integration level, engineers refactoring the codebase can be sure that they don't accidentally introduce bugs that they've already invested time and effort to eliminate. (source: chapter-17-testing-for-reliability.md)

Each bug fix has a dollar cost (debug time, repair time, production impact). A regression test preserves that investment. Without one, the same bug can return — sometimes when the engineer who fixed it has left the team.

## As bug-to-test conversion

Chapter 17 links regression tests to cultural practice:

> One way to establish a strong testing culture is to start documenting all reported bugs as test cases. If every bug is converted into a test, each test is supposed to initially fail because the bug hasn't yet been fixed. As engineers fix the bugs, the software passes testing and you're on the road to developing a comprehensive regression test suite. (source: chapter-17-testing-for-reliability.md)

The pattern is: bug filed → failing test written → bug fixed → test passes → test kept. The test suite grows in proportion to known failure modes.

## Limits at canary time

Chapter 17's [[canary-test|canary-test]] section qualifies the regression approach: **most bugs are of order one** (they scale linearly with user traffic) and can be mechanically converted to regression tests from logs of unusual responses. Higher-order bugs (request corrupts data for *future* requests; corrupted data is a valid identifier in a *past* request) cannot be captured this way — replaying the logged requests in isolation reproduces nothing. For those, you need the [[canary-test|canary mechanism]] itself (source: chapter-17-testing-for-reliability.md).

## Cross-book connections

- [[learning-from-outages]] (Ch 13) — postmortem follow-up items often include a regression test as the preventive action; Ch 17 is where the mechanism is named
- [[architecture-fitness-function]] (Richards & Ford) — each regression test is an objective automatable check; a corpus of regression tests is a de facto fitness-function suite for known failure modes

## Related pages

- [[system-tests]]
- [[testing-for-reliability]]
- [[canary-test]]
- [[learning-from-outages]]
