# Configuration Test

**Summary**: A production test that compares a checked-in configuration file against how the binary is **actually configured in production** and reports the diff. Configuration tests are inherently non-hermetic — they run outside the test sandbox against the live system — and the pattern of passes/fails across a fleet is itself a useful signal for a distributed monitoring system.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> At Google, web service configurations are described in files that are stored in our version control system. For each configuration file, a separate configuration test examines production to see how a particular binary is actually configured and reports discrepancies against that file. Such tests are inherently not hermetic, as they operate outside the test infrastructure sandbox. (source: chapter-17-testing-for-reliability.md)

Two facts about Google production environments make configuration tests necessary:

1. Rollout cadences make live changes to production in small, well-understood chunks — production is intentionally not representative of any single revision in source control (source: chapter-17-testing-for-reliability.md).
2. Source control can hold multiple versions of a binary and configuration file waiting to go live simultaneously.

The result: at any given moment, production is a mixed blend of revisions. A configuration test asks a specific question — "what version of this config is *actually* running in production right now?" — and compares the answer against the version in the repository.

## As a release-progress indicator

> Comparing which version of the test is passing in relation to the goal version for automation implicitly indicates how far actual production currently lags behind ongoing engineering work. (source: chapter-17-testing-for-reliability.md)

The test's pass/fail state is a binary signal with a useful interpretation: green means production matches repository; red means the push hasn't propagated yet. The ratio of green-to-red across the fleet is a push-progress gauge.

## As monitoring input

Because configuration tests run continuously against production, their pattern of passes and fails can feed the monitoring system (source: chapter-17-testing-for-reliability.md):

> These nonhermetic configuration tests tend to be especially valuable as part of a distributed monitoring solution since the pattern of passes/fails across production can identify paths through the service stack that don't have sensible combinations of the local configurations. The monitoring solution's rules try to match paths of actual user requests (from the trace logs) against that set of undesirable paths. Any matches found by the rules become alerts that ongoing releases and/or pushes are not proceeding safely and remedial action is needed.

The cross-cut is powerful: a user request traversing a path through the service stack where the configuration tests *would* fail is evidence that the rollout is entering unsafe territory.

## Implementation complexity

The simple case — production uses the file verbatim and offers a real-time query to retrieve its current content — reduces to a diff. The test is a few lines of code.

Complexity grows when (source: chapter-17-testing-for-reliability.md):

- Defaults are baked into the binary (tests must be versioned against the binary too).
- Configuration passes through a preprocessor (bash, template engine) into command-line flags (tests must account for expansion rules).
- Configuration specifies behavioural context for a shared runtime (tests now depend on the runtime's release schedule, not just the config file's).

Each complication moves the test closer to the runtime and further from a mechanical diff.

## Cross-book connections

- [[configuration-management-sre]] (Ch 8) — the four distribution models this test validates; configuration tests are what make the "config in repo + strict code review" rule enforceable end-to-end
- [[prodtest]] (Ch 7) — the forerunner: Python unit tests extended to check real services; configuration tests are a specialisation of the same idea
- [[architecture-fitness-function]] (Richards & Ford) — "the running configuration matches the declared configuration" is an objective automatable integrity assessment of release hygiene

## Related pages

- [[testing-for-reliability]]
- [[configuration-management-sre]]
- [[configuration-integration-testing]]
- [[prodtest]]
- [[production-probes]]
