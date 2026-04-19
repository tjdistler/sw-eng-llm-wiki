# Data Domain Pattern (Access)

**Summary**: A [[distributed-data-access]] pattern that resolves cross-service reads by putting the relevant tables into a **shared schema** (a [[data-domain]]) that both the owner and the reader access directly. The Wishlist and Product tables move into the same schema; the Wishlist Service's read becomes a local SQL join. Decouples services, preserves integrity, and is the fastest and most consistent option — but widens the bounded context across both services and turns the table schema into the cross-service contract.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md`

**Last updated**: 2026-04-19

---

## The mechanics

The data-domain access pattern is the Chapter 9 [[joint-ownership-techniques|joint-ownership data-domain technique]] applied to the **read** side. Instead of one service owning a table and others reading via remote call, replication, or cache, the tables themselves are moved into a shared schema accessible to every service in the domain (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

In the Wishlist/Catalog example: the `Wishlist` and `Product` tables are both placed into a single schema owned by neither service but shared between them. The Wishlist Service reads product descriptions with a plain SQL join.

Conceptually: no data is transferred, replicated, or synchronised — because there's only one copy.

## What you get

Chapter 10 rates this pattern the best on almost every quality attribute (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md):

- **Decoupling** — no runtime call between services, no availability dependency, no scaling dependency.
- **Responsiveness** — a regular SQL join.
- **Data consistency and integrity** — one physical copy, so no sync lag. Foreign keys, views, stored procedures, and triggers can enforce integrity the way they used to in the monolith.
- **No contract transfer** — the table schema *is* the contract; no DTOs or API versions to ship.

Preserving DB-level integrity (FKs, views, stored procedures) is itself a reason to choose this pattern — some shops want the DB to enforce invariants rather than the application.

## What you give up

The chapter is careful about the costs:

### Broader bounded context

Two services now share a **common, broader bounded context**. A change to any table in the shared schema potentially impacts **both** services. Interservice communication and replicated cache patterns form an **abstraction layer** (API contract, cache DTO) over the table shape, letting tables evolve privately. The data domain pattern removes that abstraction, so table changes become multi-service change-management events (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

### Security and access governance

Each service accessing the data domain has **full access** to every table in the shared schema. In the Wishlist/Catalog example this is fine; in scenarios with PII or tiered access, a tighter per-service bounded context (with contracts) can enforce "this caller can see descriptions but not cost" — the data-domain pattern cannot. DB access control helps only at the role-per-schema granularity.

### Loss of data-sovereignty purity

[[data-sovereignty]] — one service, one schema — is the microservices ideal the book starts with. This pattern explicitly breaks it. The chapter's defence is that sometimes every other pattern's trade-offs are worse, and a broader bounded context is the least-worst choice.

## Trade-offs summary (Table 10-4)

| Dimension | Rating |
|---|---|
| Service dependency | **None** — no runtime call |
| Response time | **Excellent** — local SQL join |
| Data currency | **Excellent** — one copy, no sync |
| Fault tolerance | Good — depends on the shared DB |
| Data volume | Any |
| Scalability | Independent of each other; shared-DB scaling applies |
| Complexity | **Low** at runtime; high at schema-change time |
| Contract versioning | **Table = contract; broader bounded context** |

(source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md, Table 10-4)

## When to use it

Chapter 10 frames this as the **last-resort pattern that has the most benefits**. Reach for it when the other three are disqualified:

- [[interservice-communication-pattern]] — ruled out by latency or fault-tolerance.
- [[column-schema-replication-pattern]] — ruled out by consistency requirements.
- [[replicated-caching-pattern]] — ruled out by data volume or volatility.

Also the right choice when DB-level integrity (FKs, views, triggers) is a hard requirement the application can't replace.

## Relation to Chapter 9

Ch 9 introduced [[data-domain]] as a **joint-ownership technique** for tables multiple services **write**. Ch 10 reuses the same structural move for tables one service writes but several **read**. The mechanism is identical — a shared schema, a broader bounded context, table-as-contract — only the motivating scenario differs.

## Related pages

- [[distributed-data-access]]
- [[data-domain]]
- [[joint-ownership-techniques]]
- [[data-ownership]]
- [[interservice-communication-pattern]]
- [[column-schema-replication-pattern]]
- [[replicated-caching-pattern]]
- [[bounded-context]]
- [[data-sovereignty]]
- [[shared-database-antipattern]]
- [[database-view-pattern]]
- [[software-architecture-the-hard-parts]]
