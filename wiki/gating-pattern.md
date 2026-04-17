# Gating Pattern

**Summary**: A stateful EDM pattern in which a service waits for a **known set of prerequisite events** — arriving in any order across multiple input streams — before emitting a downstream outcome event. Order doesn't matter; *completeness* does. Gating is the canonical stateful workload for a [[basic-producer-consumer-microservice|BPC]], because it needs state but doesn't need the deterministic cross-stream scheduling a full framework provides.

**Sources**: `raw/building-event-driven-microservices/chapter-10-basic-producer-and-consumer-microservices.md`

**Last updated**: 2026-04-17

---

## Shape

Each incoming event on any of the gated input streams is:

1. **Materialized** into its own per-stream table, keyed by the business entity (e.g. ISBN).
2. **Cross-checked** against the other tables. If the entity now has an entry in *every* required table, the gate opens: emit the aggregate event to the output stream.
3. Otherwise, the entity remains in a partial state, waiting for the rest of its prerequisites to show up.

This is a natural fit for a BPC with an [[external-state-store]]: the per-stream tables are just keyed rows in the store; every ingress is an upsert plus a few lookups (source: chapter-10-basic-producer-and-consumer-microservices.md).

## Worked example: book publishing

Bellemare's example: a publisher cannot send a book to the printer until three things have happened, in any order (source: chapter-10-basic-producer-and-consumer-microservices.md):

- **Contents** — the book has been written.
- **Cover art** — the cover has been designed.
- **Pricing** — prices are set for each region and format.

Three input streams, one per prerequisite, keyed by ISBN. A BPC consumes all three, materializes each into its own table, and on every new event checks whether the other two tables contain the same ISBN. When all three rows exist, it emits a `book-ready-for-printing` event.

In the chapter's illustration, ISBN 0010 has already been emitted (all three prerequisites present); ISBN 0011 is still waiting on cover art.

## Why BPC, not a framework?

Gating doesn't need deterministic [[event-scheduling]] or [[watermarks]]. Late and out-of-order events are fine — the gate opens when completeness is reached, regardless of time. That removes most of what a full stream-processing framework gives you. What's left — a few tables, key-by-key lookups, idempotent upserts — is comfortably within what a BPC over an [[external-state-store]] can do (source: chapter-10-basic-producer-and-consumer-microservices.md).

## The approval variant

A variant Bellemare flags as related is the **approval pattern**, where one of the gating prerequisites is *explicit human sign-off* rather than another system's event. The shape is identical — a table of approvals keyed by entity — but the upstream producer is a UI that writes an approval event when a human clicks a button. The newspaper-publishing workflow later in the book is the worked example.

## Relationship to compensating workflows

Gating is forward-only: the gate either opens or stays closed. It is **not** a [[saga]] or a [[compensation-workflow]]; there are no reverse actions. If a prerequisite is *invalidated* (e.g. the cover art is rejected after pricing has arrived), that is modeled as a new event on the same stream that retracts the existing row — the table's [[table-stream-duality|stream-table duality]] handles the update naturally, and the gate simply stops being open until a replacement arrives.

## Related pages

- [[basic-producer-consumer-microservice]]
- [[stateful-stream-processing]]
- [[materialized-state]]
- [[external-state-store]]
- [[table-stream-duality]]
- [[event-scheduling]]
- [[workflows-in-edm]]
