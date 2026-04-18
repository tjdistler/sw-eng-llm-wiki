# Performance Tests

**Summary**: A [[system-tests|system test]] that establishes acceptable performance *over the lifecycle* of a system. Written after smoke tests establish basic correctness, they catch the slow-drift failure mode where response times, memory footprints, or resource requirements grow incrementally release-over-release until the system is too slow or too expensive to run.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> Once basic correctness is established via a smoke test, a common next step is to write another variant of a system test to ensure that the performance of the system stays acceptable over the duration of its lifecycle. Because response times for dependencies or resource requirements may change dramatically during the course of development, a system needs to be tested to make sure that it doesn't become incrementally slower without anyone noticing (before it gets released to users). For example, a given program may evolve to need 32 GB of memory when it formerly only needed 8 GB, or a 10 ms response time might turn into 50 ms, and then into 100 ms. A performance test ensures that over time, a system doesn't degrade or become too expensive. (source: chapter-17-testing-for-reliability.md)

The failure mode is **frog-in-boiling-water**. No single release regresses performance visibly; the cumulative effect over a year is catastrophic.

## Where they sit

After [[smoke-tests]] in the [[system-tests|system-test]] hierarchy. Smoke proves the thing works at all; performance proves it still works *well enough*.

## Cross-book connections

- [[long-tail-latency]] (Ch 6) — the monitoring-side version: watch the tail, not the mean, because averages hide regressions
- [[monitoring-resolution]] (Ch 6) — the tooling for observing the performance characteristics performance tests are designed to freeze
- [[stress-tests]] — complementary production test: find where performance breaks down catastrophically under load

## Related pages

- [[system-tests]]
- [[smoke-tests]]
- [[regression-tests]]
- [[stress-tests]]
- [[testing-for-reliability]]
