# Data Ownership

**Summary**: Once a database has been pulled apart into [[data-domain|data domains]], each table must be assigned to an owning service. The primary rule of *Software Architecture: The Hard Parts* Chapter 9: **the service that writes to a table owns it**. Readers don't own. The complications arrive when multiple services write to the same table.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The writer-owns rule

> The general rule of thumb for data ownership is that the service that performs write operations to a table is the owner of that table. (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md)

The rule is intentionally simple. Reads don't confer ownership — any number of services can be read-only clients of a table without changing its owner. Writes do, because writes are where integrity, invariants, and business rules live. Assigning ownership to the writer aligns the table with the service's [[bounded-context]] and keeps write logic in one place.

The simple rule breaks down in two ways:

- **Common ownership** — many services want to write the same table.
- **Joint ownership** — a few related services legitimately write the same table.

Most of Chapter 9 is about resolving these cases.

## The three scenarios

The chapter enumerates three ownership scenarios an architect encounters after [[database-decomposition]] (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

| Scenario | Definition | Typical resolution |
|---|---|---|
| **Single (sole) ownership** | Exactly one service writes to a table | Assign ownership to that service. Done. |
| **Common ownership** | Most or all services write the same table (classic: `Audit` table) | Create a dedicated owning service; other services send write requests to it (async fire-and-forget queue is the common shape) |
| **Joint ownership** | A few related services within a domain write the same table (classic: `Product` table shared by Catalog and Inventory) | Pick one of four techniques — see [[joint-ownership-techniques]] |

The book's worked example has all three in one diagram: a `Wishlist` table (single owner — Wishlist Service), an `Audit` table (every service writes — common), and a `Product` table (Catalog + Inventory both write — joint).

## Do single ownership first

Chapter 9's practical advice: resolve the **single-ownership** tables first. They are cheap decisions and they clear the diagram so the remaining complexity stands out. Don't get stuck agonising about the `Product` table when the `Wishlist` table can be assigned in thirty seconds.

## Common ownership: the dedicated-service fix

Common ownership looks like a shared table is fine — *every* service is writing to it, so nobody can get in the way. In fact it is the worst of the three scenarios because it resurrects every [[shared-database-antipattern|shared-database problem]] — change control, connection starvation, scalability, fault tolerance (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

The fix is to make a new **dedicated owner service** for the table. Other services send it write requests:

- **Fire-and-forget async** over a persistent queue when no return value is needed (the Audit-table case).
- **Synchronous call** (REST, gRPC, request-reply messaging) when the caller needs a confirmation or ID back.

Persistent queues give guaranteed delivery across broker/service failures without blocking callers. This is the book's recommended default for audit-style common-ownership cases.

## Joint ownership: four techniques

Joint ownership is the genuinely hard case. Chapter 9 names four techniques — see [[joint-ownership-techniques]] for the full comparison. Summary:

1. **[[table-split-technique]]** — split the shared table into two tables, one per owning service, and synchronise across the boundary.
2. **[[data-domain]] technique** — accept that the table is shared, put it in a data domain that both services access, and live with the broader bounded context.
3. **[[delegate-technique]]** — assign single ownership to one service; the other sends write requests to it.
4. **Service consolidation** — merge the two services into one. If the data wants to live together, maybe the services should too — see [[service-granularity]].

Each technique has trade-offs. The book's framing: no technique is "right"; pick by matching trade-offs to the architecture characteristics the service boundary was designed to optimise for.

## Readers cause friction too

A service that doesn't own a table can still need to read it, and read access creates its own class of coupling problems — [[distributed-transactions|consistency across services]], synchronisation latency, cache coherency. Chapter 10 of *The Hard Parts* covers the read-access side in depth: see [[distributed-data-access]] and the four patterns — [[interservice-communication-pattern]], [[column-schema-replication-pattern]], [[replicated-caching-pattern]], [[data-domain-pattern]].

Chapter 9's focus is the write side; its reminder is that *ownership disputes are about writes*, but *reads still have costs*, and the architect must address both.

## Validate ownership against business workflows

The chapter closes with a note worth carrying forward: once table ownership is assigned, **analyse the end-to-end business workflows** that cross those boundaries. An ownership assignment that looks clean on a diagram may turn pathological under a workflow that needs to atomically update three services. That analysis is what motivates the rest of the chapter — [[distributed-transactions]], [[eventual-consistency]] patterns, and ultimately the [[saga]] work in Chapter 12.

## Related pages

- [[joint-ownership-techniques]]
- [[table-split-technique]]
- [[delegate-technique]]
- [[data-domain]]
- [[database-decomposition]]
- [[bounded-context]]
- [[shared-database-antipattern]]
- [[distributed-transactions]]
- [[eventual-consistency]]
- [[base-properties]]
- [[saga]]
- [[change-data-ownership]]
- [[service-granularity]]
- [[distributed-data-access]]
- [[software-architecture-the-hard-parts]]
