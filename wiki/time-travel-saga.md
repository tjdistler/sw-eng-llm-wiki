# Time Travel Saga (sec)

**Summary**: [[saga]] pattern with **synchronous** communication, **eventual** consistency, **choreographed** coordination. Chapter 12 of *Software Architecture: The Hard Parts* names this the Time Travel Saga(sec) because each service owns its own transactional context and consistency becomes temporally gradual — state "time-travels" into consistency over time. Well-suited to fast one-way pipelines (Chain of Responsibility, Pipes and Filters); the on-ramp to the more scalable [[anthology-saga|Anthology Saga(aec)]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## Axes

| Axis | Value |
|---|---|
| Communication | Synchronous |
| Consistency | Eventual |
| Coordination | Choreographed |

Superscript notation: **sec**.

## Description

Each service accepts a request, performs its local transaction, and **synchronously forwards** the request to the next service. No orchestrator exists; workflow state lives in the chain itself (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md). The pattern implements the **Chain of Responsibility** design pattern or the **Pipes and Filters** architecture style at the distributed-workflow grain.

The name reflects that each service owns its transactional context independently — consistency is achieved over time through the design of inter-service communication, not atomically.

## When to use

- **Fire-and-forget** style workflows: electronic data ingestion, bulk transaction processing, log-shaped pipelines.
- Linear chains where every step is a transformation or enrichment.
- High throughput desired but full async complexity not yet justified.
- Error conditions are simple or infrequent.

## When to avoid

- Complex error handling or branching workflows — no orchestrator to coordinate recovery.
- Workflows requiring operational state visibility — there is no central place to ask "where is workflow X?"
- When even higher scale is required — move to [[anthology-saga]] by substituting async for sync.

## Trade-off ratings

Chapter 12's Table 12-5 ratings (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| Characteristic | Rating |
|---|---|
| Coupling | Medium (sync calls still couple participants in time, but no orchestrator and no atomicity) |
| Complexity | Low (absent transactionality and orchestration simplify the design) |
| Responsiveness / availability | Medium — high for purpose-built linear pipelines, low for complex error paths |
| Scale / elasticity | **High** — only [[anthology-saga|Anthology Saga(aec)]] exceeds it |

## Quasi-special-purpose

The book explicitly classifies this pattern as **quasi-special-purpose**: it fits one-way synchronous workflow chains very well, but is awkward for anything else. When a team finds themselves in Time Travel Saga(sec) territory, the usual decision is: stay here for simplicity, or migrate to [[anthology-saga|Anthology Saga(aec)]] for higher scale.

Chapter 12's framing: Time Travel Saga(sec) is the **on-ramp** to [[anthology-saga|Anthology Saga(aec)]] — it gets teams comfortable with choreographed workflows using the easier synchronous paradigm before adding async complexity.

## Related pages

- [[saga]]
- [[workflow-choreography]]
- [[eventual-consistency]]
- [[anthology-saga]] — same pattern but async (higher scale)
- [[fairy-tale-saga]] — same pattern but orchestrated
- [[phone-tag-saga]] — same pattern but atomic
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
