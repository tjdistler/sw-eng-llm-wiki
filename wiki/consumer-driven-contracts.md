# Consumer-Driven Contracts

**Summary**: A test-based technique where the *consumer* of a microservice writes an executable specification of how the service is expected to behave; the producer runs those tests on every change. CDCs catch contract breakage from the consumer's point of view and reduce the need for cross-team end-to-end tests.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The idea

With consumer-driven contracts, each consumer of a microservice defines its expectations of the service's behaviour as an executable specification — a test (source: chapter-05-growing-pains.md). When the producer changes the service, it runs those consumer-supplied tests. If they fail, the producer knows it's about to break a real consumer.

Two important properties:

1. **The tests are written from the consumer's point of view.** This catches accidental contract breakage that schema-only checks miss — including semantic regressions, not just structural ones.
2. **Different consumers can have different expectations.** The producer sees, in a structured way, what each consumer actually relies on. That's information the producer otherwise has to guess at.

## Why CDCs help with two Chapter 5 pain points

### [[breaking-changes]]

CDCs are Newman's recommended way to catch contract breakage early (source: chapter-05-growing-pains.md). Schemas catch *structural* breakage; CDCs catch *semantic* breakage and reveal which behaviours actual consumers depend on.

### [[end-to-end-testing]]

CDCs replace some cross-service test cases. Instead of standing up multiple services in an integration environment to verify a flow, the producer runs the consumer's contract test against an isolated instance. Faster, more reliable, no cross-team test ownership problem (source: chapter-05-growing-pains.md).

## Tooling: Pact

Newman's recommended tool is **Pact** (source: chapter-05-growing-pains.md). You can implement CDCs with a plain test-development workflow, but Pact is purpose-built — it handles contract publication, version matching, and the producer-side verification step.

## A poorly underused practice

Newman is candid that adoption is uneven (source: chapter-05-growing-pains.md):

> "I've seen some teams have huge success with this approach, but it's been difficult for others to adopt. The idea is sound, and I know it can work well, but I haven't yet fully understood the challenges that some people have had in adopting this technique. It remains a poorly underused practice for solving a really difficult problem."

His advice is still to try it. The problem CDCs solve — verifying contracts without huge cross-team test environments — gets harder, not easier, as the architecture grows.

## Where CDCs sit relative to other testing

A rough mental model:

- **Unit tests** — fast, isolated, lots of them.
- **Service-level tests** — exercise one service end-to-end inside its boundary.
- **Consumer-driven contract tests** — verify the producer keeps each consumer's specific expectations.
- **End-to-end tests** — span multiple services. Newman recommends limiting these aggressively; see [[end-to-end-testing]].
- **Synthetic transactions in production** — the ongoing equivalent of end-to-end tests, run against the real system; see [[synthetic-transactions]].

## Related pages

- [[breaking-changes]]
- [[end-to-end-testing]]
- [[independent-deployability]]
- [[information-hiding]]
- [[progressive-delivery]]
