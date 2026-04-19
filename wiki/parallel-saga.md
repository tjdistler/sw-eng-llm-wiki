# Parallel Saga (aeo)

**Summary**: [[saga]] pattern with **asynchronous** communication, **eventual** consistency, **orchestrated** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Parallel Saga(aeo); it is the [[epic-saga|Epic Saga(sao)]] with the two hardest constraints relaxed. A strong default for complex workflows that need scale — keeps the orchestrator (for workflow state and error handling) but gains async parallelism and per-service transactionality.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Asynchronous |
| Consistency | Eventual |
| Coordination | Orchestrated |

Superscript notation: **aeo**.

## Description

An orchestrator directs the workflow across participating services using **asynchronous** messaging. Each service owns its own transaction boundary; the overall workflow is **eventually consistent** (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md). When errors occur, the orchestrator sends asynchronous compensating messages to the already-committed services, possibly driving retries or cross-service data synchronisation.

The pattern keeps the two things [[fairy-tale-saga|Fairy Tale(seo)]] keeps (orchestrated workflow ownership + eventual consistency) and trades synchronous communication for asynchronous — gaining parallelism and responsiveness in exchange for the usual async headaches (race conditions, queue reliability, ordering).

## When to use

- **Complex workflows that need scale.** The orchestrator provides the error-handling and state-management home; async communication allows parallel execution and decouples participant performance footprints.
- Services have **highly variable performance footprints** — public-facing services scaling differently from back-office services. Per-service transactionality + async lets each scale independently.
- Error handling requires a central home but atomicity is not mandatory.

## When to avoid

- Extremely simple linear workflows — orchestration overhead isn't paying for itself; prefer [[anthology-saga]].
- Workflows requiring genuine atomic consistency — no option on this axis is good; rarely go to [[epic-saga]].

## Trade-off ratings

Chapter 12's Table 12-8 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | **Low** (transactionality isolated to each service; async decouples wait states) |
| Complexity | Low — relatively easy to reason about given its axes |
| Responsiveness / availability | **High** (no atomic coordination; async parallelism) |
| Scale / elasticity | **High** — per-service transactional boundaries let architects scale each service independently |

## Why it's a strong default

Three design pressures align:

1. **Asynchronous communication** removes sync timing bottlenecks and allows parallel participant work.
2. **Eventual consistency** frees each service to commit locally without cross-service coordination.
3. **Orchestrator** keeps workflow state visible and gives errors a home.

The combination delivers most of [[epic-saga|Epic Saga(sao)]]'s orchestration benefits while removing its two biggest costs. For complex-workflow + scale-needed scenarios, this is the book's go-to orchestrated pattern.

## Contrast with neighbours

- **[[fantasy-fiction-saga|Fantasy Fiction(aao)]]** — same axes except atomic. Parallel Saga(aeo) is what Fantasy Fiction should usually become by relaxing atomicity.
- **[[fairy-tale-saga|Fairy Tale(seo)]]** — same axes except sync. Prefer Fairy Tale when the team wants easier debugging; prefer Parallel when throughput matters.
- **[[anthology-saga|Anthology(aec)]]** — same axes except choreographed. Prefer Anthology when the workflow is simple and linear; prefer Parallel when it's complex.

## Related pages

- [[saga]]
- [[workflow-orchestration]]
- [[eventual-consistency]]
- [[fairy-tale-saga]] — same pattern but sync
- [[fantasy-fiction-saga]] — same pattern but atomic
- [[anthology-saga]] — same pattern but choreographed
- [[epic-saga]] — the opposite trade-off
- [[event-based-consistency-pattern]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
