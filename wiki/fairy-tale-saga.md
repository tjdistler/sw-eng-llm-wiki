# Fairy Tale Saga (seo)

**Summary**: [[saga]] pattern with **synchronous** communication, **eventual** consistency, **orchestrated** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Fairy Tale Saga(seo) because it reads like a fairy tale — easy story, happy ending. Very common real-world choice: orchestrator + sync calls + per-service-owned transactionality produces a good trade-off for most microservice workflows.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Synchronous |
| Consistency | Eventual |
| Coordination | Orchestrated |

Superscript notation: **seo**.

## Description

An orchestrator drives the workflow synchronously across participants, but **each domain service owns its own transaction boundary** — there is no cross-service atomicity requirement. The orchestrator can still issue [[compensating-update|compensating calls]] on failure, but without the pressure of completing them inside an active transaction (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

The pattern relaxes the hardest dimension of the [[epic-saga|Epic Saga(sao)]] — atomicity — while keeping the two dimensions architects find easiest to reason about: synchronous calls and a single coordinating mediator. If the Survey Service is temporarily down, the orchestrator can cache the intent and retry; it does not need to roll back the ticket update.

## When to use

- **Default choice for most orchestrated microservice workflows** where eventual consistency is acceptable.
- Workflow has complex error handling but atomicity is not a hard business requirement.
- Operational dashboards or "where is my order?" queries need a clear state-tracking home.
- The team values debuggability and a central place for the workflow logic to live.

## When to avoid

- Atomicity is a real business requirement (rare but possible — then see [[epic-saga]]).
- Extreme scale / throughput needs — prefer [[parallel-saga]] (async) or [[anthology-saga]] (choreographed + async).

## Trade-off ratings

Chapter 12's Table 12-4 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | High (two of three axes coupled: sync + orchestrated) — but the **worst coupling force** (transactionality) is gone |
| Complexity | **Low** — most convenient options combined with the loosest consistency restriction |
| Responsiveness / availability | Good (mediator holds less time-sensitive transaction state; better load balancing) |
| Scale / elasticity | Better than Epic Saga(sao); worse than async alternatives |

## Worked example (Sysops Squad)

Chapter 12's illustration (Figure 12-20): ticket completion sets survey status to `NO_SURVEY` if the Survey Service is unavailable, returns success to the expert, and leaves the Ticket Orchestrator to asynchronously retry or escalate. The end user is not blocked on the error; responsiveness is preserved. This is the canonical example of Fairy Tale Saga(seo) leveraging saga state machines instead of compensating updates (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

## Why it's so popular

Three forces align:

1. **Orchestrator** gives workflow state a natural home.
2. **Synchronous calls** are easier to reason about, implement, and debug than async.
3. **Eventual consistency** removes the hardest constraint of distributed systems.

The book's position: if an architect can tolerate eventual consistency, this pattern is usually the right starting point among the orchestrated options.

## Related pages

- [[saga]]
- [[workflow-orchestration]]
- [[eventual-consistency]]
- [[compensating-update]]
- [[dynamic-coupling]]
- [[epic-saga]] — same axes except consistency
- [[parallel-saga]] — same pattern but async (higher scale)
- [[time-travel-saga]] — same pattern but choreographed
- [[orchestrated-request-based-pattern]]
- [[software-architecture-the-hard-parts]]
