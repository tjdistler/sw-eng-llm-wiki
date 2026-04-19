# Horror Story Saga (aac)

**Summary**: [[saga]] pattern with **asynchronous** communication, **atomic** consistency, **choreographed** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Horror Story(aac) pattern and explicitly calls it the **worst combination** — it pairs the most demanding consistency constraint (atomic) with the two loosest coordination choices (async + choreographed). Usually avoidable; the book's recommended replacement is [[anthology-saga|Anthology Saga(aec)]] (drop atomicity).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Asynchronous |
| Consistency | Atomic |
| Coordination | Choreographed |

Superscript notation: **aac**.

## Description

No mediator exists to coordinate atomic commitment across the workflow, yet atomic consistency is the architectural goal. Each domain service must track **undo information** about every in-flight transaction it participates in — potentially out-of-order because of asynchronicity — and coordinate compensations with peers on error conditions (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

Chapter 12's worked example: while transaction Alpha is pending, transaction Beta starts. One of Alpha's async calls fails. The choreographed services must now reverse the firing order of Alpha's partial commits — possibly out of order — while Beta continues in parallel. The state space of "what could go wrong" grows combinatorially.

## When to use

- **Avoid if at all possible.** If architects reach this combination, almost certainly an axis needs to be reconsidered.

## When to avoid

- Always, unless the atomic requirement is absolutely fixed *and* neither orchestration nor synchronous communication are tolerable. In practice this set is empty for most real systems. The recommended substitute is [[anthology-saga|Anthology Saga(aec)]] — drop atomicity.

## Trade-off ratings

Chapter 12's Table 12-7 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | High (but interestingly **not** the worst — that's [[epic-saga|Epic Saga(sao)]]; no mediator and async relieve two of the axes) |
| Complexity | **Highest of all patterns** — the most demanding consistency requirement with the most difficult coordination combination |
| Responsiveness / availability | Low — async chatter for atomic coordination across services is expensive |
| Scale / elasticity | Better than orchestrated patterns (no orchestrator bottleneck; async allows parallelism) |

## How architects end up here

Chapter 12's diagnostic: a well-meaning architect starts with [[epic-saga|Epic Saga(sao)]], notices it's slow, and reaches for performance fixes they understand in isolation:

1. "Async will make it faster" — switch sync to async.
2. "Choreography will remove the orchestrator bottleneck" — remove the mediator.

Both are individually correct statements. Applied together while maintaining atomic consistency, they produce Horror Story(aac). The book's lesson: architectural forces are **entangled**, not independent. You cannot change one axis in isolation and expect the others to stay put.

## Coupling paradox

Horror Story(aac)'s coupling rating is high but not the absolute worst. [[epic-saga|Epic Saga(sao)]] is more coupled because its sync + orchestrated + atomic combination produces *three* maximally-coupled axes, not two. Horror Story(aac) is worse on **complexity** because transactional consistency with the loosest two coordination axes forces each service to carry enormous workflow knowledge — but the coupling itself is lower. This is the pattern used to demonstrate that **coupling and complexity are not the same metric**; a less coupled pattern can be more complex.

## Related pages

- [[saga]]
- [[anthology-saga]] — the recommended substitute (drop atomicity)
- [[phone-tag-saga]] — the sync cousin
- [[fantasy-fiction-saga]] — the orchestrated cousin
- [[epic-saga]] — the strictly-opposite pattern
- [[dynamic-coupling]]
- [[compensating-update]]
- [[software-architecture-the-hard-parts]]
