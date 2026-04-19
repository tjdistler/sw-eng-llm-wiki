# Consumer-Driven Contracts

**Summary**: A test-based technique where the *consumer* of a microservice writes an executable specification of how the service is expected to behave; the producer runs those tests on every change. CDCs catch contract breakage from the consumer's point of view and reduce the need for cross-team end-to-end tests.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

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

## Hard Parts Ch 13: CDCs as the microservices default

Ford, Richards, Sadalage, and Dehghani's *Software Architecture: The Hard Parts* Chapter 13 promotes CDCs from "poorly underused practice" to **explicit microservices default** — the canonical resolution of the seeming contradiction between loose coupling and contract fidelity (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

### The push vs pull inversion

Most integration scenarios use a *push* model: the provider decides what to emit, and consumers adapt. CDCs invert this into a *pull* model:

> The consumer puts together a contract for the items they need from the provider, and passes the contract to the provider, who includes it in their build and keeps the contract test green at all times. (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md)

The provider runs every consumer's contract as part of CI/CD. Each consumer specifies its own contract at its own level of strictness. Structural deviations and semantic-behaviour changes both break the build.

### The architectural pitch: loose contract + CDC

Ch 13's recommended pairing for microservices (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

- Use name-value pairs (loose wire format) between services — for decoupling and evolvability.
- Use CDCs as an [[architecture-fitness-function|architecture fitness function]] — for contract fidelity.

The two interlocking mechanisms substitute for a single end-to-end schema tool and accept a small complexity cost for a large decoupling gain.

### Advantages named by Ch 13

Three (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Loosest possible coupling.** Name-value pairs mean implementation changes rarely break the integration point.
2. **Variability in strictness per consumer.** Each consumer can specify as much or as little rigour as it needs — including constraints that typical schemas can't express (e.g. numeric *ranges*, not just numeric types).
3. **Evolvability.** Loose coupling means integration points can evolve without rewriting the wire format, so long as the semantics are preserved.

### Disadvantages named by Ch 13

Two (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Requires engineering maturity.** Fitness functions only work when teams respect failing tests. If contract tests are routinely ignored or not run, the verification layer is theatre.
2. **Two interlocking mechanisms rather than one.** Architects often prefer one end-to-end tool to two composing primitives. The CDC+name-value pattern is explicitly the latter — two simple tools doing one rich job.

The summary: CDCs trade *schema-as-artifact* for *test-as-artifact*, and tests compose better across multiple consumers than any single schema can.

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
- [[contracts]]
- [[loose-contract]]
- [[strict-contract]]
- [[architecture-fitness-function]]
- [[data-contract]]
- [[software-architecture-the-hard-parts]]
