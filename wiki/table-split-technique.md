# Table Split Technique

**Summary**: A [[joint-ownership-techniques|joint-ownership]] resolution: break one table shared by two services into two tables, each owned solely by one service, and synchronise across the boundary. Described in *Software Architecture: The Hard Parts* Ch 9 (and earlier in Ambler & Sadalage's *Refactoring Databases*).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The refactor

Chapter 9's worked example: a `Product` table written by both the Catalog Service (static product info) and the Inventory Service (current stock count). The split:

1. Create a new `Inventory` table keyed by `product_id` with the inventory columns.
2. Copy current values out of `Product` into `Inventory`.
3. Drop the inventory columns from `Product`.

```sql
CREATE TABLE Inventory (
    product_id  VARCHAR(10),
    inv_cnt     INT
);

INSERT INTO Inventory (product_id, inv_cnt)
    AS SELECT product_id, inv_cnt FROM Product;
COMMIT;

ALTER TABLE Product DROP COLUMN inv_cnt;
```

(source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md)

After the split: Catalog Service solely owns `Product`, Inventory Service solely owns `Inventory`. Joint ownership has become two [[data-ownership|sole-ownership]] cases.

## The synchronisation problem it creates

Splitting the columns doesn't eliminate the coupling — it moves the coupling from the DB schema to the service layer. Whenever a product is created or removed, both tables must change in lock-step:

- Catalog Service inserts into `Product` → must tell Inventory Service to insert into `Inventory`.
- Catalog Service deletes from `Product` → must tell Inventory Service to delete from `Inventory`.

This is a two-service write that used to be a one-service write. Every write decision that was previously implicit (one table, one transaction) is now explicit.

## The CAP trade-off is now visible

The chapter makes the CAP trade-off explicit on this pattern (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

- **Availability choice** — Catalog Service always succeeds in adding/removing a product, even if Inventory Service is unavailable. Consequence: the `Inventory` row may not get created/deleted promptly; the tables can be inconsistent.
- **Consistency choice** — Product changes only succeed if Inventory Service is reachable and the corresponding Inventory row is updated. Consequence: Catalog Service's availability now depends on Inventory Service's availability.

The choice is forced by [[cap-theorem]] and the inevitability of network partitions; one side must be sacrificed.

## Sync vs async communication

Also forced:

- **Synchronous call** (HTTP/gRPC) — Catalog waits for Inventory to confirm. Better consistency, worse performance, stronger availability coupling.
- **Asynchronous call** (message/queue) — Catalog fires and continues. Better performance, [[eventual-consistency|eventually consistent]], potential for lost updates on errors.

Neither gets you full atomic update across the split. That would need a [[distributed-transactions|distributed transaction]] (which the chapter talks architects out of). The sync/async choice is just how much inconsistency and latency you accept.

## Trade-off summary

| | For | Against |
|---|---|---|
| **Table split** | Clear sole ownership restored; simpler mental model per service; schemas are smaller | Requires cross-service synchronisation on every product create/delete; availability vs consistency now explicit; failure modes on async comms (lost updates, retries, dead letters) |

## When it's a good fit

The technique works best when the shared table has **distinct column-groups** with naturally distinct owners. Product (static data) and Inventory count (frequently mutating transactional data) are a textbook case: different volatility, different access patterns, different operational requirements — the split aligns the schema with the service boundary.

It works poorly when columns are deeply interdependent (FKs within the "row," cross-column invariants the DB used to enforce) — splitting those forces the integrity rules into application code, often across two codebases.

## Relationship to other techniques

- The **[[data-domain]] technique** leaves the table shared rather than split — avoids the sync problem at the cost of a broader bounded context.
- The **[[delegate-technique]]** keeps one table, picks a sole owner, and routes the other service's writes through the owner — similar coordination cost, different shape.
- **Service consolidation** (see [[joint-ownership-techniques]]) merges the services — eliminates joint ownership entirely.

Chapter 9 recommends picking whichever technique's trade-offs match the architecture characteristics the services were split to preserve.

## Related pages

- [[joint-ownership-techniques]]
- [[data-ownership]]
- [[delegate-technique]]
- [[data-domain]]
- [[split-table-pattern]]
- [[cap-theorem]]
- [[eventual-consistency]]
- [[distributed-transactions]]
- [[database-decomposition]]
- [[software-architecture-the-hard-parts]]
