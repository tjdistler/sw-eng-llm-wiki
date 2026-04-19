# Data Domain

**Summary**: In *Software Architecture: The Hard Parts*, a **data domain** is a collection of coupled database artifacts — tables, views, foreign keys, triggers, stored procedures — that belong to the same bounded functional scope and are frequently used together. Data domains are the unit of [[database-decomposition]]: a monolithic database is broken apart one data domain at a time.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The concept

> A data domain is a collection of coupled database artifacts — tables, views, foreign keys, and triggers — that are all related to a particular domain and frequently used together within a limited functional scope. (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md)

Where an application architect identifies [[components]] and rolls them up into [[bounded-context|bounded contexts]], a data architect identifies *tables* and rolls them up into **data domains**. The two hierarchies ideally align — one bounded context per data domain — and the alignment is what makes per-service [[data-sovereignty|data sovereignty]] possible.

The Sysops Squad example the book uses has six data domains:

| Data domain | Example tables |
|---|---|
| Customer | customer, customer_contact |
| Survey | survey, question, response |
| Payment | billing, contract, payment_method |
| Profile | sysops_user, skill |
| Knowledge base | article, tag |
| Ticketing | ticket, ticket_type, ticket_history |

Each domain's internal references (FKs, views, triggers) stay inside the domain. Cross-domain references become **coupling points** that must eventually move to the service layer.

## The soccer-ball mental model

The book's visual: the database is a soccer ball, and each **white hexagon** is a data domain. Inside a hexagon, relationships are dense and preserved. Between hexagons, the few existing dependencies are the ones that must be broken — cross-hexagon FKs, cross-hexagon views, cross-hexagon stored procedures (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

This visualisation makes it obvious that **the cost of decomposition is localised to inter-hexagon dependencies**, not the whole schema. Most of the schema's complexity — the intra-hexagon FK web — survives the split intact.

## Data domain vs database schema

The book is explicit about the relationship (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- A **data domain** is an **architectural concept** — a logical grouping of related data.
- A **schema** is a **database construct** — a namespace in the DB engine that owns tables, views, functions.

Usually the mapping is 1:1 — one data domain per schema. But when two data domains are tightly coupled through data relationships the team can't (yet) break, the two domains may merge into a single broader bounded context, mapped to one or two schemas. The book uses "data domain" and "schema" interchangeably in later chapters for this reason.

## Cross-domain artifacts

When a data domain is extracted, every coupling artifact that crosses the domain boundary must go somewhere:

- **Foreign keys** — drop the constraint; move the integrity check into the service layer (see [[move-foreign-key-to-code]]).
- **Views** — rewrite without the cross-domain joins, OR move the join into the service that queries both domains.
- **Triggers / stored procedures** — move into service-layer orchestration code.
- **Synonyms** — a stepping-stone: create a DB-level synonym for the cross-schema table, use it to find and refactor callers, then remove it.

The book's Payment/Customer example: a `v_customer_contract` view in the Payment schema joined a Customer table. After extraction, the view drops the join and the Payment service must call the Customer service to get the customer name it used to get from the view.

## The synonym stepping-stone

In the middle of decomposition, a database team can create a **synonym** — a DB alias for a table in another schema. Queries keep working through the synonym, but the cross-schema query is now *visible* and *grepable*, making it easy to find and refactor (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

```sql
CREATE SYNONYM ticketing.sysops_user
FOR profile.sysops_user;
```

The query in the Ticketing schema can then use `ticket.sysops_user` instead of `profile.sysops_user`. This doesn't eliminate the cross-schema coupling — it just makes it a coupling point the team can systematically chase down. The synonym is removed when the caller is refactored to use a service call instead.

## Combining data domains

When two domains are so tightly coupled (e.g., a problem-ticket table and its ticket-status table with bidirectional FKs and shared triggers) that decomposing them would cost more than it's worth, the book recommends **combining** them into a broader bounded context. A single service ends up owning both tables and the composite domain. This is discussed in Chapter 9's data-ownership treatment.

## Data domain as a joint-ownership technique (Ch 9)

Chapter 9 re-uses the data-domain concept as one of the four [[joint-ownership-techniques]] for resolving the case where two services both write to the same table. The technique: instead of splitting or picking a delegate, put the shared tables into a shared schema — a data domain — and accept that the **broader bounded context** crosses both services (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

This trades the tight per-service bounded context (microservices' usual default) for performance, availability, and data consistency. The chapter warns that schema changes now require multi-service coordination, and that "which service can write which columns" governance must move to application-layer policy because the DB no longer enforces it via access control.

Usually a sign the question *"why are these still two services?"* deserves a second look — see [[joint-ownership-techniques]] for the comparison with service consolidation.

## Data domain as a read-access pattern (Ch 10)

Chapter 10 applies the same move to the **read** side — see [[data-domain-pattern]]. When one service owns a table and another needs to read it, and none of [[interservice-communication-pattern]], [[column-schema-replication-pattern]], or [[replicated-caching-pattern]] fit, putting the table in a shared data domain gives the reader local SQL access with perfect data currency (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md). The mechanics are identical; only the motivating scenario differs (shared reads vs shared writes). In both uses, the table schema becomes the cross-service contract and the bounded context widens to cover both services.

## Where data domains fit in the workflow

Data domains are the unit produced by **Step 1** of the five-step [[database-decomposition]] pattern (analyze the database and create data domains), and the unit Steps 2–5 operate on (assign tables, split connections, move schemas, separate servers). Without a clean domain decomposition, the later steps have nothing to move.

## Related pages

- [[database-decomposition]]
- [[data-decomposition-drivers-and-integrators]]
- [[bounded-context]]
- [[data-sovereignty]]
- [[architectural-quantum]]
- [[move-foreign-key-to-code]]
- [[database-per-bounded-context]]
- [[shared-database-antipattern]]
- [[polyglot-persistence]]
- [[software-architecture-the-hard-parts]]
- [[data-ownership]]
- [[joint-ownership-techniques]]
- [[data-domain-pattern]]
- [[distributed-data-access]]
