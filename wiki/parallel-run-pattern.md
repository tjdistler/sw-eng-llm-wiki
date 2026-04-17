# Parallel Run Pattern

**Summary**: A migration verification pattern where both the old and new implementations execute on every request and their results are compared. One implementation remains the source of truth (typically the old one) until the new one has earned trust. Useful when correctness or non-functional behaviour of the new service is high-risk.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`

**Last updated**: 2026-04-16

---

## The idea

Both [[strangler-fig-pattern]] and [[branch-by-abstraction]] let old and new implementations coexist in production but only execute *one* per call. A parallel run **calls both** and compares the results, treating one as authoritative (source: chapter-03-splitting-the-monolith.md).

This verifies more than functional equivalence:

- **Functional equivalence**: same inputs → same outputs.
- **Non-functional behaviour**: latency, time-out rate, failure rate of the new service in real production traffic.

## Example: credit derivative pricing

Newman recounts replacing a bank's credit derivative pricing system. Pricing events were duplicated to both old and new systems. Each morning a batch reconciliation surfaced any discrepancies in an Excel spreadsheet, which engineers walked through with bank analysts. The exercise found bugs in *both* systems — many of the discrepancies were the new system being correct against a buggy original. After roughly a month, the new system became authoritative (source: chapter-03-splitting-the-monolith.md).

## Example: Homegate listings

Homegate ran their FTP-based listing import alongside the new microservice that processed REST equivalents. A single FTP upload triggered both. Once the team confirmed equivalent behaviour, the old FTP path in the monolith was switched off (source: chapter-03-splitting-the-monolith.md). See also [[strangler-fig-pattern]].

## Spies for side-effecting code

If the operation has external side effects (sending an email, charging a card), running both implementations would double-fire the side effect. The pattern from unit testing applies: a **Spy** stands in for the side-effecting call and records that it was invoked rather than performing it. In a parallel run for a notification service, the Spy replaces the actual email-sending code while the rest of the new service runs as normal (source: chapter-03-splitting-the-monolith.md).

Spies running in a separate process complicate verification timing — typically you record interactions for offline reconciliation rather than in-band verification.

## GitHub Scientist

GitHub's open-source [Scientist](https://github.com/github/scientist) Ruby library implements the pattern at code level: declare a `science` block with old and new candidates, and the library handles execution, comparison, and metrics. Ports exist for Java, .NET, Python, Node.js and others (source: chapter-03-splitting-the-monolith.md).

## Teeing at the ambassador / proxy layer

An alternative to in-process libraries is to do the teeing *outside* the application. Burns's Chapter 3 [[request-splitting|request-splitting ambassador]] describes exactly this: an ambassador container proxies requests to both the production system and a newer undeployed version, returns the production response to the user, and discards or logs the experimental response (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). That is a parallel run implemented at the transport layer, with no application-side code. Compared to Scientist-style in-process libraries it is language-agnostic and does not require each application to adopt the library; compared to Scientist it has less access to application-level semantic comparison, so the comparison logic tends to be coarser (e.g. byte-equality or HTTP-status-code equality).

## N-version programming: a relative

Safety-critical control systems (fly-by-wire avionics) deploy multiple independent implementations of the same subsystem, send each input to all of them, and pick the answer agreed by a quorum. The goal is fault tolerance during operation rather than migration verification — but the structural pattern is the same (source: chapter-03-splitting-the-monolith.md).

## Parallel run vs canary vs dark launch

These three are all part of [[progressive-delivery]] and are often confused (source: chapter-03-splitting-the-monolith.md):

- **Canary release**: a *fraction* of real users hit the new code; the rest hit the old.
- **Dark launch**: the new functionality is deployed and exercised but invisible to users.
- **Parallel run**: *both* implementations run on *every* call; results are compared.

Parallel run is one way to implement dark launching.

## When to use it

Parallel runs are non-trivial to implement. Newman has used the pattern only "once or twice" but found it hugely useful in those cases (source: chapter-03-splitting-the-monolith.md). Reserve it for high-risk migrations where:

- Incorrect output has significant business or safety consequences (financial pricing, medical records).
- The new implementation differs enough from the old that bugs are plausible.
- You can capture the behaviour for offline comparison.

## Related pages

- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[progressive-delivery]]
- [[deployment-vs-release]]
- [[feature-toggle]]
- [[migration-pattern-selection]]
- [[request-splitting]]
- [[ambassador-pattern]]
