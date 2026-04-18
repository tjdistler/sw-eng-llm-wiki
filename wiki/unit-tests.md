# Unit Tests

**Summary**: The smallest and simplest form of software testing: a test that exercises a **separable unit** (class, function) for correctness, independent of the rest of the system. Unit tests double as a **specification** for what the unit is supposed to do and are the foundation that integration and system testing layer on top of.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> A unit test is the smallest and simplest form of software testing. These tests are employed to assess a separable unit of software, such as a class or function, for correctness independent of the larger software system that contains the unit. Unit tests are also employed as a form of specification to ensure that a function or module exactly performs the behavior required by the system. Unit tests are commonly used to introduce test-driven development concepts. (source: chapter-17-testing-for-reliability.md)

Two jobs in one: **verification** (does it work?) and **specification** (what is it supposed to do?). Test-driven development leans on the specification half.

## Where they sit

In the [[testing-for-reliability|Chapter 17 hierarchy]], unit tests are the base of the traditional-testing pyramid. [[integration-tests]] sit above them; [[system-tests]] (smoke, performance, regression) sit above those.

## Economics

> Unit tests are very cheap in both dimensions, as they can usually be completed in milliseconds on the resources available on a laptop. (source: chapter-17-testing-for-reliability.md)

Cheapness matters because testing cost directly gates feedback speed for developers. Unit tests run interactively; they're the class of test that meets the [[testing-deadlines|pre-context-switch deadline]] easily.

## What they cannot catch

Unit tests cannot verify interactions between units, framework-level operations, or end-to-end behaviour. Bugs that emerge only when components combine require [[integration-tests]]; bugs that emerge only with full-stack dependencies require [[system-tests]] or [[production-probes]].

## Cross-book connections

- [[unit-testing-topology-functions]] (Bellemare) — the EDM-specific application of this class: pure transform/map/filter/reduce functions in a streaming topology
- [[architecture-fitness-function]] (Richards & Ford) — unit tests are the atomic form of a fitness function
- [[test-and-treat]] (Ch 12) — the debugging-time analogue: an experiment that proves or disproves a hypothesis about a small unit of behaviour

## Related pages

- [[integration-tests]]
- [[system-tests]]
- [[testing-for-reliability]]
- [[unit-testing-topology-functions]]
- [[testing-deadlines]]
