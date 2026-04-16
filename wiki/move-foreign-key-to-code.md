# Pattern: Move Foreign-Key Relationship to Code

**Summary**: When two tables joined by a foreign key end up in different services, the database can no longer enforce the relationship or perform the join. The join becomes an inter-service call; referential integrity becomes the application's problem.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The setup

Newman's example: a music shop where `Ledger` rows record sales by SKU and reference rows in the `Albums` table via a foreign key. Once `Catalog` and `Finance` are separate services, the FK can't span the database boundary. Two distinct problems arise (source: chapter-04-decomposing-the-database.md):

1. **Joins.** A best-sellers report needs the album titles for the top SKUs. With one schema, that was a single SQL `SELECT` with a join. Now it's a query against the `Ledger`, then a service call to `Catalog` to enrich each SKU.
2. **Consistency.** The database used to prevent deletion of an album row referenced by the ledger. Without the FK, nothing prevents that inconsistency.

## Moving the join

The join doesn't disappear; it moves up into the application. The Finance service queries its own `Ledger`, then calls the Catalog service for the album details, then merges the results in memory. (source: chapter-04-decomposing-the-database.md)

This is **strictly slower** than a database join. Mitigations Newman lists (source: chapter-04-decomposing-the-database.md):

- **Bulk lookups** — let `Catalog` accept a list of SKUs in a single call.
- **Caching** — cache album info locally in `Finance` (especially powerful when reports run monthly).
- **Distributed tracing** — Jaeger and similar tools help you measure the latency cost across service boundaries.

Whether the latency increase matters is context-dependent. Newman: "You need to have an understanding of acceptable latency for key operations, and be able to measure what the latency currently is." (source: chapter-04-decomposing-the-database.md)

## Handling consistency

With the FK gone, what stops `Albums` from deleting a row that `Ledger` still references? Newman walks through the options (source: chapter-04-decomposing-the-database.md):

### Check before deletion (avoid)

The `Catalog` service asks every consumer "are you using SKU X?" before deleting. Newman urges you not to do this:

- **Race conditions.** A new reference could appear during the check. To prevent that, you'd need distributed locks — all the pain of [[two-phase-commit]] for free.
- **Reverse dependency.** `Catalog` now depends on every consumer. Adding a new consumer means changing `Catalog`.

### Handle deletion gracefully (preferred)

Let `Finance` cope with the missing reference. If a SKU lookup fails, render `"Album Information Not Available"`. Use a meaningful HTTP status code: `410 Gone` rather than `404 Not Found`, to distinguish "deleted" from "never existed." This distinction matters when tracking down inconsistency bugs. (source: chapter-04-decomposing-the-database.md)

A more sophisticated variant: subscribe to deletion events from `Catalog` and copy the deleted album info into `Finance`'s local store. Useful for cascading-deletion or distributed state-machine cases.

### Don't allow deletion

If a true delete in `Catalog` is rare (the album just becomes "unavailable for sale"), implement a **soft delete** — a status column or a "graveyard" table. Lookups still work because the row is still there. (source: chapter-04-decomposing-the-database.md)

For richer historical reconstruction, [[event-sourcing]] becomes attractive (Newman flags this in a footnote).

### Newman's choice

For the album/ledger scenario, Newman would do *both*: don't allow deletion in `Catalog`, *and* have `Finance` handle a missing record gracefully. Defence in depth: even if a recovery from backup leaves `Catalog` without an album the ledger references, `Finance` doesn't fall over. (source: chapter-04-decomposing-the-database.md)

## When you might be splitting an aggregate

A warning sign: **before you break a foreign key, check that you aren't breaking an [[aggregate]]**. The `Order` ↔ `OrderLine` relationship looks like a parent-child FK, but order lines are part of the order itself — moving them into a separate service would shred a single domain entity. If the FK lives inside an aggregate, move both sides together as a unit. (source: chapter-04-decomposing-the-database.md)

> "Sometimes, by taking a bigger bite out of the monolithic schema, you may be able to move both sides of a foreign-key relationship with you, making your life much easier!"

## Related pages

- [[database-decomposition]]
- [[split-table-pattern]]
- [[aggregate]]
- [[bounded-context]]
- [[event-sourcing]]
- [[change-data-ownership]]
- [[transactions]]
- [[saga]]
- [[two-phase-commit]]
