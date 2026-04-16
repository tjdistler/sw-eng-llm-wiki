# End-to-End Testing

**Summary**: Tests that exercise multiple services together to verify a user journey. In a microservice architecture they become slow, flaky, expensive, and ambiguous in their failure modes. Newman's prescription: keep their scope tight, push verification to consumer-driven contracts and progressive delivery, and continuously refine the feedback cycle.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The squeeze

Test scope is a balancing act: more functionality covered means more confidence, but also longer test runs and harder failure diagnosis. End-to-end tests sit at the wide end of that scale (source: chapter-05-growing-pains.md).

A monolith can host end-to-end tests reasonably: one process, one database, one CI run. A microservice architecture pushes the same tests across multiple services that all need to be deployed and configured for the test scenario. False negatives multiply — a service instance dies, a network times out, a deployment partially fails, the test fails for reasons unrelated to the code under test (source: chapter-05-growing-pains.md).

> "I'd argue that we are much more vulnerable to issues outside of our control when running end-to-end tests against a microservice architecture than we are with a standard monolithic architecture."

## Symptoms

(source: chapter-05-growing-pains.md)

- The end-to-end suite grows because multiple teams add scenarios "just in case", unsure which ones are already covered.
- Failures in the suite often *don't* indicate a real bug. Developers re-run the suite hoping it passes — a bad cultural signal.
- Test runtime grows. Pressure mounts to add testers, even a separate test team.

This pattern emerges most sharply when **multiple teams** own different parts of a user journey — each team can manage its own tests well, but cross-team flows become nobody's well-defined problem.

## Newman's four-part response

A summary of his prescription, drawn from a much fuller treatment in *Building Microservices* Chapter 9 (source: chapter-05-growing-pains.md).

### 1. Limit scope of functional automated tests

Keep tests inside the team that owns the services they cover. Tests crossing team boundaries quickly become orphaned in a Conway's-law sense — no one is sure what they cover, no one runs them on local changes, no one fixes them when they fail.

### 2. Use [[consumer-driven-contracts]]

CDCs replace many cross-service test cases. The consumer of a service writes an executable specification of what they expect; the producer runs it on every change. This catches contract breakage from the consumer's perspective without needing both services in a single integration environment.

> "It remains a poorly underused practice for solving a really difficult problem." (Newman on CDCs)

### 3. Use automated release remediation and progressive delivery

Reduce the *cost* of production issues, since you can't reduce their probability to zero. [[progressive-delivery]] — canary, dark launch, [[parallel-run-pattern|parallel run]], [[feature-toggle|feature toggles]] — exposes new releases to a small slice of users with measurable acceptance thresholds. If error rates or p95 latency cross the threshold, automatic rollback (source: chapter-05-growing-pains.md).

Netflix's Spinnaker is the canonical example of this approach in production. Newman's framing:

> "I'm not saying you should consider automated release remediation instead of testing, just that you should think about where you get the best return on your effort."

Even *manual* progressive delivery (without automated rollback) is a big step up from rolling out to all users at once.

### 4. Continually refine your quality feedback cycles

> "It's about balancing the need for fast feedback with safety. You need to be just as willing to identify, and remove or replace, the wrong test as you are to add a new test." (source: chapter-05-growing-pains.md)

Test suites tend to grow monotonically because adding a test feels safer than removing one. Someone — preferably with cross-cutting context — needs the authority and the willingness to delete tests that no longer pull their weight, and to add tests where production defects are escaping.

## Where end-to-end tests still live

Newman doesn't argue for zero end-to-end tests. He argues for keeping their scope tight, their ownership clear, their count small, and their role complemented by [[synthetic-transactions]] in production and [[progressive-delivery]] at the cutover. The shift is from "end-to-end tests as primary safety net" to "end-to-end tests as one technique among many".

## Related pages

- [[consumer-driven-contracts]]
- [[progressive-delivery]]
- [[parallel-run-pattern]]
- [[feature-toggle]]
- [[synthetic-transactions]]
- [[breaking-changes]]
- [[independent-deployability]]
