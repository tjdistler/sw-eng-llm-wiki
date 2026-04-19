# Phone Tag Saga (sac)

**Summary**: [[saga]] pattern with **synchronous** communication, **atomic** consistency, **choreographed** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Phone Tag Saga(sac) after the children's game: each service whispers to the next, and on error must unwind the chain via compensating calls. Rare combination; usually a worse choice than the [[epic-saga|Epic Saga(sao)]] once error scenarios are more than trivial.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Synchronous |
| Consistency | Atomic |
| Coordination | Choreographed |

Superscript notation: **sac**.

## Description

A front-controller service (typically the first service in the chain) accepts the request and begins the workflow; each subsequent service performs its local transaction and synchronously calls the next (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md). On error, each participating service must carry **workflow and compensation logic** to send [[compensating-update|compensating calls]] back along the chain.

Because the architectural goal is atomic consistency but no orchestrator exists, the coordination burden is distributed across all domain services. For any non-trivial workflow, the front controller ends up as complex as a mediator — at which point architects usually wish they had just chosen the [[epic-saga|Epic Saga(sao)]].

## When to use

- **Simple linear workflows** where error scenarios are rare or easily retried.
- Each domain service can be made **idempotent** so retries are safe.
- You want slightly better scale than [[epic-saga|Epic Saga(sao)]] and can accept the complexity cost.

## When to avoid

- Complex error handling or many branching paths — the per-service compensation logic compounds quickly.
- Teams that cannot coordinate a rich shared workflow contract.
- Anywhere [[fairy-tale-saga]] or [[parallel-saga]] can replace atomicity with eventual consistency — they dominate this pattern on almost every axis.

## Trade-off ratings

Chapter 12's Table 12-3 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | High (slightly less than Epic Saga(sao) — choreography relaxes one axis) |
| Complexity | **Very high** — grows linearly with workflow semantic complexity because each service must know more about the workflow |
| Responsiveness / availability | Medium (better happy path than Epic Saga(sao); worse error path) |
| Scale / elasticity | Slight improvement over Epic Saga(sao) (no orchestrator bottleneck) |

## Why the combination is rare

Architects who choose choreography usually also choose asynchronicity. Choreography + synchronicity is unusual because the two decisions typically travel together. The book notes one legitimate use case: synchronous calls ensure each service finishes its part before the next begins, eliminating race conditions — but only for simple workflows where the costs of distributing workflow logic across services stay manageable.

Alternatively, workflow state can ride in the message body as [[stamp-coupling]] to propagate context — at the cost of every service coupling to the message's shared shape.

## Failure modes

- **Chain unwind complexity** — error paths require each service to compensate the next-upstream service. With N participants, an error at step N triggers N-1 compensating messages.
- **Front controller creep** — as workflow complexity grows, the front controller accretes the responsibilities of an orchestrator without the name.
- **Partial unwind on compensation failure** — a compensating call that fails leaves the chain in an inconsistent state, with no central authority to reconcile.

## Related pages

- [[saga]]
- [[epic-saga]] — the orchestrated cousin (usually preferred at this complexity level)
- [[horror-story-saga]] — the async cousin (strictly worse)
- [[workflow-choreography]]
- [[compensating-update]]
- [[stamp-coupling]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
