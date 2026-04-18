# Test-Induced Emergency

**Summary**: Chapter 13's first case study: a proactive dependency test on a distributed MySQL database blocked access to one database out of a hundred and unexpectedly took down numerous internal and external services. The incident illustrates that disaster testing is how hidden dependencies surface, that assumptions about scope are frequently wrong, and that rollback procedures themselves need to be tested before the large-scale test that relies on them.

**Sources**: `raw/site-reliability-engineering/chapter-13-emergency-response.md`

**Last updated**: 2026-04-17

---

## The test

Google has adopted a proactive approach to disaster and emergency testing (source: chapter-13-emergency-response.md). SREs deliberately break production systems, watch how they fail, and use what they learn to eliminate failure modes and hidden dependencies. Most tests go as planned and surface small weaknesses. This one did not.

The plan: flush out hidden dependencies on a test database inside a larger distributed MySQL deployment by **blocking access to just one database out of a hundred**. The expected blast radius was narrow.

## What went wrong

Within minutes of starting the test, dependent services reported that external and internal users could not reach key systems. Some systems were intermittently or only partially accessible — the fingerprint of a dependency everyone assumed was decoupled but in fact was not.

Assuming the test was responsible (correctly), SRE **immediately aborted the exercise**. They tried to roll back the permissions change — and the rollback itself failed. The rollback procedure had never been tested.

## The response

Rather than panic, the team **brainstormed an alternative recovery path**: restore permissions to the replicas and failovers using a different, already-tested approach. In parallel, key developers were pulled in to fix the flaw in the database application-layer library. Some dependent teams bypassed the problem by reconfiguring their systems away from the test database. Within an hour of the first report, access was fully restored.

## What went well

- Affected services escalated quickly inside the company.
- The SRE team correctly inferred "the controlled experiment has gotten out of hand" and aborted within minutes.
- An **alternative recovery path** — restoring permissions to replicas and failovers — worked because it had been previously exercised.
- Parallel team efforts (reconfiguring around the test database) compressed the outage timeline.
- Follow-up actions were resolved and a **periodic retesting schedule** was instituted to prevent the same flaw from re-entering the system.

## What was learned

- **The test scope was wrong.** Although thoroughly reviewed, reality revealed an insufficient understanding of the dependencies around this test database. This is the recurring lesson of disaster testing: you find out what the actual dependency graph is, which often differs from what the design diagram claims.
- **The incident-response process wasn't followed.** A formal process had been instituted only a few weeks before and hadn't been widely disseminated. Following it would have notified all services and customers about the outage up front.
- **Rollback procedures had not been tested** in a test environment before being relied on in production. Chapter 13 draws the explicit follow-up rule: **thoroughly test rollback procedures before large-scale tests**.

## Why it's in the chapter

The case is the book's canonical example of how proactive testing can itself cause the outage it was designed to find. Chapter 13's conclusion doesn't soften that: testing is still the right policy. You just have to run the drill on the drill before you run it on production — including the rollback path.

## Connections

- [[emergency-response]] — Chapter 13's first of three case studies. The response pattern (abort, don't panic, recover via an alternative route, pull in developers) matches the chapter's summary advice.
- [[change-management-sre]] — the **safe rollback** half of the automation trio failed here because rollback was never rehearsed. The incident is evidence that the trio's third leg requires testing as much as the first two.
- [[automation-gone-wrong]] — same broad lesson (automation needs guardrails), viewed from the test-exercise angle rather than the destructive-workflow angle.
- [[blameless-postmortem]] — the write-up is what produced the action items (periodic retesting, rollback testing rule, process dissemination).
- [[learning-from-outages]] — Chapter 13's closing section argues that the value of tests like this is precisely the action items they produce.
- [[operational-underload]] — the deeper motivation for disaster testing: quiet systems hide dependencies that only reveal themselves under failure.

## Cross-book connection

- Chaos engineering (Netflix Chaos Monkey and similar) — the general discipline this Google practice belongs to. The industry form and Google's disaster testing share the premise that the way to find hidden dependencies is to break things on purpose.
- [[progressive-delivery]] (Newman / Burns) — the rollback-must-be-tested lesson applies symmetrically to progressive-delivery rollbacks.

## Related pages

- [[emergency-response]]
- [[change-induced-emergency]]
- [[process-induced-emergency]]
- [[learning-from-outages]]
- [[change-management-sre]]
- [[automation-gone-wrong]]
- [[blameless-postmortem]]
- [[operational-underload]]
