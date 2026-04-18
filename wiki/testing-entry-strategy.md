# Testing Entry Strategy

**Summary**: Chapter 17's advice for SREs joining a developer team whose project is already underway — prototype-grade, low or zero coverage. Rather than aspiring to comprehensive unit coverage (overwhelming), start with tests that deliver the **most impact with the least effort**: [[smoke-tests]] on mission-critical paths, bug-to-test conversion for every reported issue, and tests on APIs other teams integrate against.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The framing

> While it's wonderful to think about these types of tests and failure scenarios on day one of a project, frequently SREs join a developer team when a project is already well underway ... The team's codebase is still a prototype and comprehensive testing hasn't yet been designed or deployed. In such situations, where should your testing efforts begin? Conducting unit tests for every key function and class is a completely overwhelming prospect if the current test coverage is low or nonexistent. Instead, start with testing that delivers the most impact with the least effort. (source: chapter-17-testing-for-reliability.md)

The realistic starting point acknowledges that "unit tests for everything" is a multi-quarter project that produces no signal for weeks. SRE needs something that produces a coverage delta within days.

## The prioritisation questions

Chapter 17's starting prompts (source: chapter-17-testing-for-reliability.md):

- **Can you prioritize the codebase in any way?** If every task is high priority, none are. Stack-rank the components by some measure of importance.
- **Are there mission-critical or business-critical functions or classes?** Code involving billing is a common example; it is usually cleanly separable.
- **Which APIs are other teams integrating against?** Breakage that never reaches users can still be extremely harmful if it misleads other developers into writing bad clients against the broken API. Shipping obviously-broken software is among the cardinal sins of a developer.

The triage produces a short list of the first places to test.

## Smoke tests first

> It takes little effort to create a series of smoke tests to run for every release. This type of low-effort, high-impact first step can lead to highly tested, reliable software. (source: chapter-17-testing-for-reliability.md)

[[smoke-tests]] are the minimum viable test investment. A dozen smoke tests on critical paths catch the "the main thing doesn't work" class of bug with very little engineering cost.

## Bug-to-test conversion

> One way to establish a strong testing culture is to start documenting all reported bugs as test cases. If every bug is converted into a test, each test is supposed to initially fail because the bug hasn't yet been fixed. As engineers fix the bugs, the software passes testing and you're on the road to developing a comprehensive regression test suite. (source: chapter-17-testing-for-reliability.md)

The virtue of bug-to-test: every filed bug is already localised to a real failure. Converting it to a test produces a coverage unit that corresponds to a known failure mode. Over time the suite becomes a map of the system's empirical failure surface.

See [[regression-tests]] for the generalised pattern.

## Build infrastructure alongside

> Another key task for creating well-tested software is to set up a testing infrastructure. (source: chapter-17-testing-for-reliability.md)

Chapter 17 argues infrastructure investment happens in parallel with the first tests, not before and not after. See [[build-system-discipline]] for the foundation layer.

## Cross-book connections

- [[toil-and-engineering-balance]] / [[engineering-work-categories]] (Ch 5) — setting up testing infrastructure is the "systems engineering" category of the engineering-work taxonomy; these are the engineering-half activities that replace toil permanently
- [[simplicity-sre]] (Ch 9) — testing a simple codebase is cheaper than testing a complex one; the entry strategy benefits enormously from the simplicity discipline being in place before SRE joins

## Related pages

- [[testing-for-reliability]]
- [[smoke-tests]]
- [[regression-tests]]
- [[build-system-discipline]]
- [[architecture-fitness-function]]
