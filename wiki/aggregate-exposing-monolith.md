# Pattern: Aggregate Exposing Monolith

**Summary**: When a newly extracted service needs data still owned by the [[monolith]], expose it from the monolith as a proper service endpoint (API or event stream) — not as a database view, and certainly not as direct schema access. The monolith retains ownership of the [[aggregate]]'s state machine; the new service consumes it through a real interface.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

Newman's example: a new `Invoice` service needs `Employee` data (for approval workflows) that is still managed by the monolith. Rather than reaching into the monolith's database, the monolith exposes an `Employee`-related endpoint and the `Invoice` service calls it. (source: chapter-04-decomposing-the-database.md)

The point is not just to share data — it is to expose the **operations** that allow callers to query state and request state transitions on an aggregate that the monolith continues to own. The monolith is still the authority on what state changes are allowed. (source: chapter-04-decomposing-the-database.md)

This is [[information-hiding]] applied to the monolith itself.

## A pathway to more services

By defining the needs of the new service through this interface, you've already done a lot of the work to discover the *next* service boundary. The `Employee` API makes the eventual `Employee` service obvious. (source: chapter-04-decomposing-the-database.md)

The aggregate-exposing endpoint becomes a seam (see [[seams-and-legacy-code]]) along which the next extraction can happen. The monolith, after that extraction, would need to be changed to call the new `Employee` service — but the consumers of the monolith's `Employee` endpoint don't.

## Where to use it

When the data you need is still owned by the monolith and you want to keep it that way for now. Newman: "Having the new service call back to the monolith to access the data it needs is likely little more work than directly accessing the database of the monolith — but in the long term is a much better idea." (source: chapter-04-decomposing-the-database.md)

## When the monolith can't be changed

If you cannot add an endpoint to the monolith (closed-source, hostile codebase, no team capacity), Newman ranks the fallbacks (source: chapter-04-decomposing-the-database.md):

1. [[change-data-capture]] — react to data changes in the monolith's database
2. [[database-view-pattern]] — read-only projection of the monolith's schema
3. [[database-wrapping-service]] — wrap the monolith's schema in a thin service

All of these are worse than a real endpoint, but better than direct schema access.

## Contrast with change-data-ownership

This pattern *keeps* the data in the monolith. The opposite move — the monolith calls back into a new service that now owns the data — is [[change-data-ownership]]. The two often appear together: some data moves to the new service; some stays with the monolith and gets exposed properly.

## Related pages

- [[database-decomposition]]
- [[change-data-ownership]]
- [[aggregate]]
- [[bounded-context]]
- [[information-hiding]]
- [[change-data-capture]]
- [[database-view-pattern]]
- [[database-wrapping-service]]
- [[seams-and-legacy-code]]
