# Cross-Service Analytics

**Summary**: Splitting a monolithic database breaks the assumption — held by analytics tools and stakeholders — that all data is queryable from one schema with SQL. Newman's pattern: keep presenting a single database for analytics, and have microservices push data into it. The same idea Chapter 4 generalised as [[database-as-a-service-interface]].

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The problem

A monolithic system typically has a monolithic database. Stakeholders who need to analyse all of the system's data — often via large joins — point their analytics tools (or a read replica) directly at the monolith schema (source: chapter-05-growing-pains.md).

Splitting into microservices breaks this. Data is now scattered across multiple logically-isolated schemas. The analytics need hasn't gone away — it has just become much harder. Newman has seen more than one project realise *halfway through* that the architecture direction was about to make life miserable for downstream analytics users (source: chapter-05-growing-pains.md).

The structural cause is "out of sight, out of mind": cross-system analytics happens outside the realm of normal software development, so its needs are rarely considered early enough.

## The pattern

If your stakeholders' analytics tools expect direct SQL access — and there is tooling and process invested in that assumption — you need to keep presenting them a single database. So:

1. **Separate the analytics database from the operational databases of each microservice** (source: chapter-05-growing-pains.md). This decouples the analytics schema's shape and evolution from each service's storage needs.
2. **Have the microservices push data into the analytics schema.** Mechanisms include:
   - **[[change-data-capture]]** — react to source-of-truth changes inside each service's database. Newman's "obvious" candidate.
   - **Database views** — project the analytics schema from views onto multiple service schemas.
   - **In-application code** — services explicitly write to the analytics database when they update their own state.
   - **Event-driven intermediaries** — listen to upstream service events and populate the analytics database from them.
3. **Design the analytics schema for analytics users** — not as a copy of the historical monolith schema, unless preserving that shape is the path of least resistance for existing tooling.

## Sidestepping the problem

If the monolith already pushes data to a dedicated analytics destination — a data warehouse or data lake — you may sidestep the migration pain entirely. All you have to do is make sure each microservice copies the appropriate data to the existing destination (source: chapter-05-growing-pains.md).

## Relationship to Chapter 4

This pattern is the Chapter 5 retelling of [[database-as-a-service-interface]] (source: chapter-04-decomposing-the-database.md), itself a generalisation of Martin Fowler's "reporting database" pattern. Chapter 4 framed it as a deliberate seam in database decomposition; Chapter 5 frames it as a pain point you will hit if you did not think about analytics users when planning the migration. Same mechanism, different motivation.

The full treatment is in Chapter 5 of *Building Microservices* (Newman, 2015) — confusingly the same chapter number as Chapter 5 of this book.

## Related pages

- [[database-as-a-service-interface]]
- [[database-decomposition]]
- [[change-data-capture]]
- [[database-view-pattern]]
- [[oltp-vs-olap]]
- [[data-warehousing]]
- [[derived-data]]
