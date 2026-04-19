# One Big Table

**Summary**: The "don't model at all" extreme — query sources directly, or load everything into one enormous [[wide-denormalized-table|wide denormalized table]] without the discipline of [[kimball-model|Kimball]], [[inmon-model|Inmon]], or [[data-vault]]. Fast to start, hard to trust.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The stance

You have the option of not modeling your data at all. Query sources directly; or dump everything into one wide table and build reports off it. Used especially when companies are just getting started and want quick insights (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## The questions Reis & Housley want you to answer first

Before committing to OBT, ask (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **How do I know my query results are consistent** if I don't model my data?
- **Do I have proper definitions of business logic in the source system**, and will my query produce truthful answers against those definitions?
- **What query load am I putting on source systems**, and how does that impact users of those systems?

The first two are the killers. Without modeling, business semantics live inside each query. Analysts independently implement "active customer" six different ways; reports disagree; trust erodes.

## The predictable trajectory

Chapter 8 is direct: "At some point, you'll probably gravitate toward a stricter batch data model paradigm and a dedicated data architecture that doesn't rely on the source systems for the heavy lifting."

OBT is a waypoint, not a destination — it gets you to insight quickly and at low engineering cost, but most successful data organizations move past it as the business logic burden in queries becomes unmanageable.

## When OBT is defensible

- **Early-stage companies** that need analytics fast and don't yet know what the business questions are.
- **Exploratory analysis** over datasets of unknown shape.
- **Streaming-first stacks** where flexible schemas are already the rule (see [[streaming-data-modeling]]).
- **Situations where a [[metrics-layer]] or [[dbt]] sits on top of OBT** — the modeling moves from the table layer to a semantic layer, preserving consistency without rigid schemas.

## Related pages

- [[wide-denormalized-table]]
- [[streaming-data-modeling]]
- [[data-modeling]]
- [[metrics-layer]]
- [[dbt]]
