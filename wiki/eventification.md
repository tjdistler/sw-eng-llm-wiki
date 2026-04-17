# Eventification

**Summary**: Adam Bellemare's name for the process of **joining and denormalizing highly normalized relational data into easy-to-consume, single-event updates** — done downstream of an [[outbox-table-pattern|outbox]] that preserves 1:1 internal streams, so that the public event stream reflects the public [[data-contract]] rather than the producer's internal data model.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## The problem eventification solves

A well-factored relational domain often spans many small normalized tables. A `User` might have foreign keys to `Location` and `Employer`; a downstream consumer rarely wants those as three separate event streams — it wants a `User` event that already contains everything (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Two ways to present a single public `User` event:

- **Denormalize on insert.** The application joins at write time and writes a single denormalized row to the outbox. Costs storage and CPU in the source service.
- **Eventify downstream.** The application keeps writing normalized 1:1 outboxes; a dedicated downstream stream processor materializes `User`, `Location`, and `Employer` into local tables, joins them, and emits a denormalized `User` event to the public stream.

Eventification moves the join cost out of the source application and into a dedicated consumer, preserving the source's performance budget.

## Public and private namespaces

The raw normalized streams live in a **private namespace** visible only to the eventification service. Downstream consumers are not allowed to see them — exposing the normalized streams would re-expose the internal data model, which is the anti-pattern the outbox was meant to prevent. Only the public, denormalized stream lives in the public namespace (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

See [[data-contract]] and [[event-as-single-source-of-truth]] for the guiding principles.

## Mechanics

The eventification service holds materialized tables of each input entity (`User`, `Location`, `Employer`). An update to any of them re-exercises the join logic and emits an updated `User` event to the public stream. This is a standard stream-processing table-table join pattern — see [[table-stream-duality]] and [[stream-joins]].

Because every input is an entity stream keyed by primary key, the latest event per key describes the current state, and the join can be maintained incrementally without external lookups.

## Trade-offs

Bellemare's framing is that eventification is the **external** variant of the denormalize-on-insert pattern (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

| Location | Cost | Benefit |
|---|---|---|
| In the source app | Extra writes and joins inline with business transactions | Public outbox directly matches the data contract; fewer moving parts |
| In a downstream service (eventification) | Dedicated service and materialized tables to maintain; more moving parts | Source app stays lean; join logic isolated and evolvable independently |

Neither is universally correct; the choice depends on the hot-path sensitivity of the source, the number of downstream consumers, and the stability of the public data contract.

## Related pages

- [[outbox-table-pattern]]
- [[data-liberation]]
- [[data-contract]]
- [[event-as-single-source-of-truth]]
- [[entity-event]]
- [[table-stream-duality]]
- [[stream-joins]]
- [[event-streams]]
- [[coupling]]
