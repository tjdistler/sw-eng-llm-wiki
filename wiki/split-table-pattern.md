# Pattern: Split Table

**Summary**: When a single table holds data belonging to two future service boundaries, separate it into two tables — typically column-by-column. Easy when columns clearly belong to one context; harder when multiple parts of the codebase update the same column.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

Sometimes the same table holds data for two different bounded contexts. Newman's first example: an `Item` table that stores both *catalog* information (name, description, SKU) and *warehouse* information (stock level). Catalog and warehouse are different services-to-be; the table needs to split. (source: chapter-04-decomposing-the-database.md)

In the spirit of [[incremental-migration]], split the tables apart **inside the existing schema first**, then split the schemas. Don't try to do both moves at the same time. (source: chapter-04-decomposing-the-database.md)

## When a column is updated by both contexts

The harder case is when a single column is touched by code from multiple contexts. Newman's example: a `Customer.Status` column. (source: chapter-04-decomposing-the-database.md)

- Customer-management code transitions the status from `NOT_VERIFIED` → `VERIFIED` during sign-up.
- Finance code transitions it to `SUSPENDED` when bills go unpaid.

Two services, one column. The judgement call: **which service owns the entity's state machine?** Newman argues `Status` is part of the customer's life cycle, so it belongs with the soon-to-be-created `Customer` service. The new `Finance` service must call the `Customer` service to request a suspension instead of writing to the column directly. (source: chapter-04-decomposing-the-database.md)

This is [[information-hiding]] applied to state transitions — keep the state machine for an [[aggregate]] inside one service.

## What you lose

Once a logical operation crosses two tables in different services, you lose the ACID transaction that used to wrap it. This is one of the big consequences of database decomposition; see [[transactions]] and [[saga]]. (source: chapter-04-decomposing-the-database.md)

## Where to use it

When a table is owned by two or more bounded contexts in your monolith, you need to split it along those lines. For columns updated by multiple parts of the codebase, you have to make a judgement about ownership: which existing domain concept does it belong to? (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[move-foreign-key-to-code]]
- [[aggregate]]
- [[bounded-context]]
- [[information-hiding]]
- [[saga]]
- [[transactions]]
