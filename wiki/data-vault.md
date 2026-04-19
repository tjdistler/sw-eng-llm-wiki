# Data Vault

**Summary**: Dan Linstedt's 1990s alternative to [[inmon-model|Inmon]] and [[kimball-model|Kimball]]: separate structural aspects of source data from its attributes using three table types — **hubs** (business keys), **links** (relationships between keys), and **satellites** (descriptive attributes). Insert-only, flexible, agile under source-system change. Often used as a landing zone feeding a downstream star schema.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Design philosophy

Kimball and Inmon encode business logic **in the model itself** — which dimensions, which facts, which normalization level. Data Vault takes a different stance: **load data from sources as-is into purpose-built tables, and interpret business logic only at query time** (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

The motivation is agility. Data moves fast. Source systems change. Business rules evolve. A model that bakes business logic into the schema requires schema changes every time the business changes. Data Vault keeps the schema stable — all change lands as new links and satellites, never as ETL rewrites.

There's no notion of "good, bad, or conformed" data in a data vault. Source truth is preserved.

## The three table types

### Hubs

A hub stores the **business keys** for an entity — customers, products, orders. One hub per entity type.

Required columns:

- **Hash key** — an MD5 (or similar) of the business key, used as the primary join key. Stable even if the source renames things.
- **Load date** — when this record was loaded.
- **Record source** — which source system it came from.
- **Business key(s)** — the natural key from the source system.

Hubs are **insert-only**. Data once loaded is never altered.

### Links

A link table tracks **relationships between business keys** in two or more hubs. Link tables connect hubs, ideally at the lowest grain.

Because a link connects multiple hubs, the relationship cardinality is modelled as many-to-many by default. New relationships between existing entities are added by inserting into a link — no schema change.

Example: `LinkOrderProduct` joining the order hub to the product hub.

### Satellites

Satellites attach **descriptive attributes** (context, measures, properties) to hubs and links. The only required columns are a primary key (business key of the parent hub / link plus load date) and the attributes themselves.

A hub can have many satellites — each one carrying a different set of attributes, possibly from different source systems.

## Why insert-only matters

Every table is append-only. To know the current state of an entity, queries filter for the latest load date per business key. To trace history, scan the insert log. This is structurally identical to [[event-sourcing]] and the [[changelog-stream]] pattern for streams — the data vault is, in effect, an immutable log of every source-system observation (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Typical use

Data Vault is often the **landing zone**: raw data lands into hubs/links/satellites insert-only, then a downstream transformation projects it into a [[kimball-model|Kimball star schema]] (or [[wide-denormalized-table|wide denormalized tables]]) for analytics consumption. This gives you the agility of Data Vault on the write side and the usability of a star on the read side.

Reis & Housley note that the Data Vault model adapts to NoSQL and streaming sources better than Inmon or Kimball — its insert-only, schema-flexible design aligns well with event-driven and [[change-data-capture|CDC]] ingestion (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Other tables

Data Vault defines more table types beyond the core three — **point-in-time (PIT)** tables and **bridge tables** — but Reis & Housley don't cover them; they exist to speed up common query patterns over the hub/link/satellite graph.

## Canonical reference

- Linstedt & Olschimke, *Building a Scalable Data Warehouse with Data Vault 2.0* (Morgan Kaufmann).

## Related pages

- [[inmon-model]]
- [[kimball-model]]
- [[data-warehousing]]
- [[insert-only]]
- [[event-sourcing]]
- [[change-data-capture]]
- [[streaming-data-modeling]]
