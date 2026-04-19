# Conceptual, Logical, and Physical Data Models

**Summary**: The three-step continuum Reis & Housley use to describe moving from business abstraction to database implementation: **conceptual** (what the data means), **logical** (how it's structured with types and keys), **physical** (how it lives in a specific database).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The three levels

| Level | Describes | Artifacts |
|---|---|---|
| **Conceptual** | Business logic, rules, entities and their relationships | Entity-relationship (ER) diagram; schemas, tables, fields by name and broad type |
| **Logical** | How the conceptual model will be implemented: specific field types, primary and foreign keys, cardinalities | Annotated ER / schema definitions; normalized form |
| **Physical** | How the logical model actually lives in a database system: specific databases, schemas, tables, indexes, partitions, clustering, configuration | DDL; storage layout |

(source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md)

## Why the hierarchy exists

Every major batch modeling paradigm — [[inmon-model|Inmon]], [[kimball-model|Kimball]], [[data-vault]] — is really a prescription for how to walk this continuum. You don't start with `CREATE TABLE`. You start with "what does the business mean by *customer*?"

Reis & Housley insist that successful data modeling involves business stakeholders at the **inception** of the process. Engineers need to obtain definitions and business goals for the data. Modeling is "a full-contact sport" — not a DBA activity in isolation (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Grain

A closely related concept: the **grain** of the data — the resolution at which data is stored and queried. Grain is typically at the level of a primary key: customer ID, order ID, product ID, often accompanied by a date/timestamp for fidelity (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

**The grain rule:** model at the **lowest level of grain possible**. You can always aggregate fine-grained data upward; you cannot restore detail you already aggregated away. The chapter's worked example: an experienced engineer responding to a "daily customer order totals" report request by still modeling the full customer-order-line detail, so the next report (with a different aggregation) doesn't require starting over.

## Relationship to conceptual vs physical decisions

The grain decision is **conceptual** — it's a statement about what the business cares about tracking. It then constrains the **logical** model (primary keys must uniquely identify at the grain) and the **physical** model (clustering / partitioning strategies typically follow the grain).

## Cross-book connections

- [[domain-driven-design]] — the bounded context / ubiquitous language story from the application-architecture side is the same idea in microservices vocabulary: you define what terms mean before you define schemas.
- [[data-contract]] — the contract artifact lives at the conceptual-logical boundary.

## Related pages

- [[data-modeling]]
- [[inmon-model]]
- [[kimball-model]]
- [[data-vault]]
- [[normalization-levels]]
