# Fantasy Fiction Saga (aao)

**Summary**: [[saga]] pattern with **asynchronous** communication, **atomic** consistency, **orchestrated** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Fantasy Fiction Saga(aao) because the combination is mostly implausible — maintaining atomic transactions across asynchronous calls requires the orchestrator to track pending transactional state across concurrent workflows, with all the deadlock, race-condition, and ordering headaches that implies. Usually a misguided attempt to speed up an [[epic-saga|Epic Saga(sao)]]; the better answer is almost always [[parallel-saga|Parallel Saga(aeo)]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Asynchronous |
| Consistency | Atomic |
| Coordination | Orchestrated |

Superscript notation: **aao**.

## Description

Structurally identical to [[epic-saga|Epic Saga(sao)]] except the orchestrator uses **asynchronous** messaging to participants (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md). The intent is usually to gain parallelism and responsiveness — but retaining atomic consistency means the orchestrator must:

- Track the pending state of every in-flight transaction.
- Handle new transactions that depend on the outcome of still-pending ones.
- Detect deadlocks between workflows.
- Resolve race conditions when compensations are emitted against a still-acknowledging service.

Chapter 12's verdict: asynchronicity is not a simple substitution. It interacts poorly with atomicity.

## When to use

- **Very rarely.** Possibly when there's an orchestration framework that specifically handles async + atomic (unusual) and a business requirement forces both.
- Usually a sign the architect should revisit the atomicity requirement.

## When to avoid

- Almost always. The near-universal replacement is [[parallel-saga|Parallel Saga(aeo)]] — relax atomicity to eventual.

## Trade-off ratings

Chapter 12's Table 12-6 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | **Very high** (orchestrator + atomicity; async adds coordination complexity, not decoupling) |
| Complexity | **Very high** (design, debugging, and operational complexity all compound) |
| Responsiveness / availability | Low (atomic coordination bottlenecks + any unavailable participant blocks the workflow) |
| Scale / elasticity | Poor for a transactional system, even with async |

## Why the combination is dangerous

Architects reach for this pattern when:

1. An [[epic-saga|Epic Saga(sao)]] is too slow because sync calls serialise everything.
2. Async seems like a targeted fix.
3. The transactional requirement feels mandatory and is not re-examined.

The book's correction: if the performance of Epic Saga(sao) is the problem, the usually-better trade is to relax **atomicity** (moving to [[fairy-tale-saga|Fairy Tale(seo)]] or [[parallel-saga|Parallel(aeo)]]), not communication synchronicity.

## Related pages

- [[saga]]
- [[parallel-saga]] — the recommended substitute (relax atomicity)
- [[epic-saga]] — the sync cousin
- [[horror-story-saga]] — the choreographed cousin (strictly worse)
- [[workflow-orchestration]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
