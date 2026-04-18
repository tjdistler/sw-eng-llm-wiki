# System Tests

**Summary**: The largest-scale test run against an **undeployed** system: all modules of a component are assembled and end-to-end functionality is exercised. Chapter 17 names three flavours — [[smoke-tests]] (simplest critical behaviours), [[performance-tests]] (guarding against degradation over time), and [[regression-tests]] (preventing previously fixed bugs from returning).

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> A system test is the largest scale test that engineers run for an undeployed system. All modules belonging to a specific component, such as a server that passed integration tests, are assembled into the system. Then the engineer tests the end-to-end functionality of the system. (source: chapter-17-testing-for-reliability.md)

"Undeployed" is the key word. System tests run in a hermetic testing environment against a fully-assembled component, not against live production. Once the same requests are replayed against production, they become part of the [[production-probes]] / black-box family.

## The three flavours

### [[smoke-tests]]

Test very simple but critical behaviour. Serve to short-circuit additional and more expensive testing (source: chapter-17-testing-for-reliability.md). Also known as sanity testing.

### [[performance-tests]]

Ensure performance stays acceptable over the lifecycle of a system. Guard against memory footprints growing from 8 GB to 32 GB unnoticed, or response times drifting from 10 ms to 50 ms to 100 ms over successive releases (source: chapter-17-testing-for-reliability.md).

### [[regression-tests]]

Prevent bugs from sneaking back into the codebase. A gallery of rogue bugs that historically caused failures, documented as tests at the system or integration level (source: chapter-17-testing-for-reliability.md).

## Economics

> At the other end of the spectrum, bringing up a complete server with required dependencies (or mock equivalents) to run related tests can take significantly more time — from several minutes to multiple hours — and possibly require dedicated computing resources. Mindfulness of these costs is essential to developer productivity, and also encourages more efficient use of testing resources. (source: chapter-17-testing-for-reliability.md)

System tests are the expensive tier. They fail the interactive [[testing-deadlines|deadline]] and must be treated as batch work whose feedback is for the code reviewer, not the author.

## Cross-book connections

- [[end-to-end-testing]] (Newman / Bellemare) — the microservice-era framing of the same class; Newman's argument is that end-to-end tests become unsustainable past a certain number of services and must be supplemented by CDCs and progressive delivery
- [[topology-testing]] (Bellemare) — the EDM-specific analogue: exercise the whole topology under a test driver without standing up a broker

## Related pages

- [[smoke-tests]]
- [[performance-tests]]
- [[regression-tests]]
- [[unit-tests]]
- [[integration-tests]]
- [[testing-for-reliability]]
- [[end-to-end-testing]]
