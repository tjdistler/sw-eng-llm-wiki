# Epic Saga (sao)

**Summary**: The "traditional" [[saga]] pattern — **synchronous** communication, **atomic** consistency, **orchestrated** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this combination the Epic Saga(sao) and flags it as the most tightly coupled of the eight saga patterns. It mimics monolithic-transaction behaviour at the cost of every operational characteristic that motivated distribution in the first place.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Synchronous |
| Consistency | Atomic |
| Coordination | Orchestrated |

Superscript notation: **sao** (synchronous, atomic, orchestrated — alphabetical by axis name).

## Description

An orchestrator service drives a workflow across participating services expected to commit or abort **transactionally** — either all succeed or none do. When a call fails, the orchestrator issues [[compensating-update|compensating updates]] to services that already committed, attempting to return the overall state to its pre-transaction starting point (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

The pattern mimics monolithic-system transaction behaviour — if a monolith were plotted on the 3-axis [[dynamic-coupling]] diagram, it would sit at the origin, and Epic Saga(sao) is the closest point to the origin in the distributed space. This familiarity is why the pattern keeps getting chosen.

## When to use

- Stakeholders **require** cross-service atomic consistency and there is no domain-level way to relax it.
- The workflow is short and each step's [[compensating-update|compensation]] is well-understood.
- Scale and responsiveness constraints are modest.

## When to avoid

- Almost any other time. The book's position: *distributed transactions present a host of difficulties and are best avoided if possible.* When the stakeholder demand is really about "the user should see consistent state," a [[fairy-tale-saga]] (eventual consistency + orchestration) usually delivers the same perceived behaviour with far less pain.

## Trade-off ratings

Chapter 12's Table 12-2 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | **Very high** (all three axes maximally coupled — the most coupled pattern in the catalogue) |
| Complexity | High (atomicity + orchestration + error handling) |
| Responsiveness / availability | Low (orchestrator sequences sync calls; any unavailable participant fails the transaction) |
| Scale / elasticity | Low (orchestration bottleneck + transaction coordination) |

## Why architects default here anyway

The Epic Saga(sao) keeps getting chosen despite its reputation because:

1. It models the transaction semantics developers already know from monoliths.
2. Stakeholders frequently mandate "state changes must synchronize" without understanding the distributed-systems cost.
3. The pattern has a name, a Wikipedia entry, and tutorials — naive architects treat "pattern exists" as "problem is solved."

Chapter 12's corrective: *the pattern is recognition of only commonality, not solvability.*

## Failure modes

- **Orchestrator bottleneck** — every call funnels through one service; throughput caps there.
- **Synchronous timing constraints** — any slow participant slows the whole transaction.
- **Compensation failure** — a compensating update itself fails and leaves the system in a state neither the original nor the compensated one can describe. Chapter 9 flagged this as often requiring human intervention; see [[compensating-update]].
- **Participant unavailability** — the entire transaction fails if any participant is down.

## Related pages

- [[saga]]
- [[distributed-transactions]]
- [[compensating-update]]
- [[workflow-orchestration]]
- [[dynamic-coupling]]
- [[fairy-tale-saga]] — the usually-better alternative (relax atomicity to eventual)
- [[fantasy-fiction-saga]] — Epic Saga(sao) with async communication substituted
- [[phone-tag-saga]] — Epic Saga(sao) with choreography substituted
- [[two-phase-commit]]
- [[orchestrated-request-based-pattern]]
- [[software-architecture-the-hard-parts]]
