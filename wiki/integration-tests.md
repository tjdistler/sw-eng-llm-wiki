# Integration Tests

**Summary**: Tests run on **assembled components** — software that has passed individual [[unit-tests]] composed into larger units and verified for correct interaction. Dependency injection (Dagger, etc.) is the key technique: replace stateful dependencies with lightweight mocks that have precisely specified behaviour, then exercise the assembled component.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> Software components that pass individual unit tests are assembled into larger components. Engineers then run an integration test on an assembled component to verify that it functions correctly. Dependency injection, which is performed with tools such as Dagger, is an extremely powerful technique for creating mocks of complex dependencies so that an engineer can cleanly test a component. A common example of a dependency injection is to replace a stateful database with a lightweight mock that has precisely specified behavior. (source: chapter-17-testing-for-reliability.md)

The defining discipline is **controlled assembly**: real units, faked dependencies. The mock's behaviour is part of the test specification — the test asserts not only on outputs but on how the component interacts with the mock.

## Where they sit

In the [[testing-for-reliability|Chapter 17 hierarchy]]: above [[unit-tests]], below [[system-tests]]. They exercise interactions that unit tests cannot reach, without paying the cost of full-system assembly.

## Cross-book connections

- [[local-integration-testing]] (Bellemare) — the EDM-specific realisation: run broker, schema registry, state stores, and the microservice together locally under programmatic control
- [[remote-integration-testing]] (Bellemare) — the shared-environment extension when local assembly is not enough
- [[consumer-driven-contracts]] (Newman) — a style of integration check where the consumer writes an executable spec and the producer runs it, avoiding cross-service test environments
- [[architecture-fitness-function]] (Richards & Ford) — integration tests are fitness functions at the component-interaction layer

## Related pages

- [[unit-tests]]
- [[system-tests]]
- [[testing-for-reliability]]
- [[local-integration-testing]]
- [[remote-integration-testing]]
- [[configuration-integration-testing]]
