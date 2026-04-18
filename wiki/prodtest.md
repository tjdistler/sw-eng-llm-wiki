# Prodtest

**Summary**: Chapter 7's name for the Production Test framework — Python unit tests extended to validate real-world services in a cluster. Prodtest answered "is this service correctly configured here?" via a dependency-aware chain of tests, later paired with idempotent fix scripts that remediated the misconfigurations the tests found.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`

**Last updated**: 2026-04-17

---

## The problem Prodtest solved

As Google's cluster count grew, some clusters required hand-tuned flags and settings and teams wasted increasing time chasing misconfigurations (source: chapter-07-the-evolution-of-automation-at-google.md). A representative failure mode: a flag that made [[colossus|GFS]] more responsive to log processing leaked into default templates, causing cells with many files to run out of memory under load.

The hand-rolled shell scripts used to configure clusters couldn't scale with the number of people wanting to make changes or the permutations of cluster configurations. They also couldn't answer three questions before declaring a service ready for traffic:

- Are all of the service's dependencies available and correctly configured?
- Are all configurations and packages consistent with other deployments?
- Are all configuration exceptions intentional?

## The design

Prodtest extended the Python unit-test framework to test real-world services (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Tests have dependencies.** A chain of tests runs in order; a failure in one test aborts the chain.
- **Parameterised by cluster name.** Given the name of a cluster, a team's Prodtest validates that team's services in that cluster.
- **Graph visualisation.** A dependency graph of unit tests and their states lets an engineer see which step failed in which cluster, with verbose Python-unit-test-style error messages.
- **Filed extensions.** Whenever a team hit a delay due to another team's misconfiguration, they could file a bug to extend the upstream team's Prodtest. The bug captures the lesson — the same problem is caught earlier next time.

The first visible payoff (Figure 7-1 in the chapter): a DNS-service Prodtest that aborted the downstream chain on a failed configuration check.

## Pairing tests with fixes

Prodtest as a pure test framework hit its limit when senior management asked for "five new clusters turned up on the same day, ready in one week" (source: chapter-07-the-evolution-of-automation-at-google.md). The team had tens of thousands of lines of shell script across dozens of teams; filing hundreds of bugs and waiting for fixes wasn't viable.

The evolution (Figure 7-2 in the chapter): **for each failing test, write a paired fix function, and require the fix to be idempotent.**

- If `TestDnsMonitoringConfigExists` fails, call `FixDnsMonitoringCreateConfig`, which scrapes configuration from a database and checks a skeleton file into revision control.
- On retry, `TestDnsMonitoringConfigExists` passes, and the next test (`TestDnsMonitoringConfigPushed`) runs.
- If the downstream test fails, `FixDnsMonitoringPushConfig` runs.
- If a fix fails multiple times, the loop stops and notifies a human.

Two properties made this viable:

- **Idempotence.** Teams could run the fix script every 15 minutes without corrupting the cluster — see [[idempotence]].
- **Dependency-aware waiting.** If the DNS team's test was blocked on a Machine Database entry, the DNS tests and fixes would start succeeding as soon as the upstream entry appeared.

With this apparatus, a small group of engineers could drive a cluster from "network works, machines listed in database" to "serving 1% of web-search and ads traffic" in a week or two.

## The retrospective critique

Chapter 7 is explicit that the test-and-fix design was deeply flawed despite its short-term success (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Test-fix-retest latency** introduced flaky tests that sometimes worked and sometimes didn't.
- **Not all fixes were naturally idempotent.** A flaky test followed by a partial fix could leave the system in an inconsistent state.
- **The incentive structure** that emerged (a dedicated turnup team running everyone's Prodtest) eroded the domain expertise needed to keep tests and fixes relevant and competent. See [[cluster-turnup-automation]] for the full specialisation-trap story.

Prodtest was a step, not an endpoint. The next generation reframed turnup as a Service-Oriented Architecture problem with per-service Admin Server RPCs — where each team's competence was aligned with ownership of its own automation.

## What Prodtest got right

Even viewed through the chapter's retrospective lens, Prodtest anchored several ideas that outlasted it:

- **Predictability through measurement.** Before Prodtest, "why does a cluster take six weeks" had no answer. After, it had a dependency graph.
- **Reusing the unit-test abstraction at a higher level.** Unit tests had a shared mental model (dependencies, assertions, pass/fail, failure messages) that dropped cleanly onto service validation.
- **The bug-as-Prodtest-extension habit.** Each missed issue became a regression test for the whole fleet.
- **Separating detection from remediation.** Test-then-fix is a decomposition that survived the next generation; modern Kubernetes operators, infrastructure-as-code plans, and drift-detection tools all use the same shape.

## Cross-book connections

- [[idempotence]] — the property that makes the fix loop safe to retry; Prodtest is the named example of idempotent fixes as an operational pattern.
- [[architecture-fitness-function]] (Richards & Ford) — Prodtest is essentially a fleet-wide continuous fitness function: an objective automatable integrity check of service configuration.
- [[operator-pattern]] (Burns) — a modern Kubernetes operator's reconciliation loop (observe state, compute diff, apply idempotent fixes) is the direct descendant of the Prodtest test-fix-retest model, embedded in the orchestrator instead of a cluster-bringup tool.

## Related pages

- [[cluster-turnup-automation]]
- [[automation-at-google]]
- [[hierarchy-of-automation-classes]]
- [[automation-gone-wrong]]
- [[idempotence]]
