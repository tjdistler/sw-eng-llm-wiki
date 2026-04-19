# Anthology Saga (aec)

**Summary**: [[saga]] pattern with **asynchronous** communication, **eventual** consistency, **choreographed** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Anthology Saga(aec); it is the **exact opposite** of [[epic-saga|Epic Saga(sao)]] — the least coupled of the eight patterns and the natural default for [[event-driven-architecture|event-driven architectures]] / the [[broker-topology]]. Best-in-class scale and responsiveness; correspondingly hard for complex workflows.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Asynchronous |
| Consistency | Eventual |
| Coordination | Choreographed |

Superscript notation: **aec**.

## Description

Services communicate via **asynchronous message queues** without an orchestrator. Each service owns its local transaction boundary; workflow state is implicit in the event chain. Error handling and cross-service coordination are the responsibility of the participating services themselves (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

The name *Anthology* reflects the pattern's fit for short-story-shaped workflows — linear, self-contained, high-throughput. A Pipes-and-Filters architecture matches this pattern exactly.

## When to use

- **Simple, mostly linear workflows** where high throughput and scale are first-order requirements.
- Workflows with **rare or easy** error scenarios.
- Event-driven architectures / broker-topology systems — this is their native saga pattern.
- Fire-and-forget pipelines, log ingestion, analytical event chains.

## When to avoid

- Complex workflows with rich compensation semantics — no orchestrator home for the logic; each service accretes workflow knowledge.
- Critical workflows where data-consistency errors must be actively resolved — compensation in choreography with async + eventual is the hardest of all error-recovery regimes.
- Workflows requiring operational state visibility without a [[correlation-ids|correlation ID]] + state-projection service.

## Trade-off ratings

Chapter 12's Table 12-9 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | **Lowest of all patterns** — no coordinator, no atomicity, no sync |
| Complexity | High for non-trivial workflows — no orchestrator means each service must carry more workflow knowledge |
| Responsiveness / availability | **Highest** — no speed governors |
| Scale / elasticity | **Highest** — maximum parallelism, no choke points |

## Stamp coupling as an alternative to an orchestrator

As in [[phone-tag-saga|Phone Tag Saga(sac)]], workflow state can ride inside the messages themselves — [[stamp-coupling]] — letting participants propagate partial workflow state without a mediator. The trade-off recapitulates the usual: larger messages, shared contract shape, no single place to query.

## Relation to the broker topology and EDA

The Anthology Saga(aec) is the saga-level instantiation of the [[broker-topology|broker-topology]] from Richards and Ford's *Fundamentals of Software Architecture* Chapter 14, and the natural saga pattern for any system built on [[event-driven-architecture|event-driven architecture]]. If the architecture style is broker-topology EDA, its sagas are choreographed + async by default; adding atomicity turns them into [[horror-story-saga|Horror Story(aac)]] territory, which the book explicitly warns against.

## Related pages

- [[saga]]
- [[workflow-choreography]]
- [[event-based-consistency-pattern]]
- [[broker-topology]]
- [[event-driven-architecture]]
- [[eventual-consistency]]
- [[parallel-saga]] — same pattern but orchestrated
- [[time-travel-saga]] — same pattern but sync
- [[horror-story-saga]] — same pattern but atomic (cautionary)
- [[epic-saga]] — the exact opposite pattern
- [[stamp-coupling]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
