# Joint Ownership Techniques

**Summary**: When multiple services within the same domain legitimately need to write to the same table, *Software Architecture: The Hard Parts* Chapter 9 names four resolution techniques: **table split**, **data domain**, **delegate**, and **service consolidation**. None is universally correct; pick by trade-off.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The problem

Joint ownership occurs when **only a few services within the same domain** write to the same table — not the every-service free-for-all of [[data-ownership|common ownership]]. The book's canonical example: a `Product` table written by the **Catalog Service** (creates, deletes, updates static product info) and the **Inventory Service** (reads and updates on-hand counts). Both have a legitimate write claim (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

The four techniques below are the book's resolutions.

## 1. Table split technique

Break the one table into two. Each service owns a part.

For the Product example: extract `inv_cnt` into a new `Inventory` table keyed by `product_id`; remove the column from `Product`. Now the Catalog Service solely owns `Product`; the Inventory Service solely owns `Inventory`. Joint ownership has become two single ownerships.

Cost: the two services must now **communicate** when a product is created or removed so the second table stays in step — a cross-service call every time `Product` is mutated. The availability-vs-consistency trade-off ([[cap-theorem|CAP]]) surfaces explicitly: should `Catalog.addProduct` fail if `Inventory` is unreachable, or succeed and risk inconsistency?

See [[table-split-technique]] for the full trade-off analysis and the DDL snippet.

## 2. Data domain technique

Stop pretending only one service should own the table. Put the shared tables into a shared schema or database — a [[data-domain]] — and accept that both services have write access within a **broader bounded context** (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

What it buys:
- **No interservice communication** for the shared data. Both services talk to the database directly.
- Best performance, availability, consistency inside the shared data.

What it costs:
- **Broader bounded context.** Schema changes must be coordinated across both services. Increased test scope and deployment risk.
- **Write governance weakens.** If you care *which* service can update *which* columns, you must add policy enforcement outside the database.
- The book asks you to re-evaluate: *why are these still two services?* If they share so much data that a shared domain is the best answer, maybe service consolidation (below) is the real answer.

The trade-off list gives the data-domain technique the ironic status of being **more tightly coupled** at the data layer than a plain microservices split, but the data coupling is explicit, bounded, and usually cheaper than the alternatives when the services really do share a data concern.

## 3. Delegate technique

Assign single ownership to **one** of the services — the **delegate** — and have the other service send write requests to it.

Two rules for picking the delegate (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

- **Primary domain priority** — pick the service that does most of the primary-entity CRUD. For Product, that's usually the Catalog Service (create/update/delete the product record itself). Inventory updates are then done via a call from Inventory Service → Catalog Service.
- **Operational characteristics priority** — pick the service with the highest operational demands (performance, scalability, throughput). For Product, that would be Inventory — inventory updates are far more frequent than product-metadata edits. Making Inventory the owner means its high-volume writes are direct DB calls.

The book's preference is **primary domain priority**: it keeps domain boundaries clean. Address the operational-characteristics concern with caching (replicated in-memory or distributed cache) instead of reversing the domain model.

Disadvantages (structural, not fixable by picking the right delegate):

- **Service coupling** — every non-delegate write is a remote call.
- **No atomic transaction** across the boundary.
- **Performance** — network + processing latency per write.
- **Fault tolerance** — if the delegate is down, non-delegate writes fail or queue.

The delegate technique is suitable only when write scenarios **do not require atomic transactions** and can **tolerate eventual consistency** over async comms. See [[delegate-technique]] for the full treatment.

## 4. Service consolidation

Merge the two services into one. Joint ownership becomes single ownership of the now-one-service.

This is the right answer when the two services' data is so intertwined that the boundary was wrong to begin with — a common finding in early decomposition. [[service-granularity]] frames this as the granularity [[granularity-integrators|integrator]] winning over the [[granularity-disintegrators|disintegrator]] that originally pulled them apart.

Trade-offs:
- **Coarser service** — bigger test scope, bigger deployment unit, bigger deployment risk.
- **Failure coupling** — both functional areas now fail together.
- **Scalability waste** — catalog-maintenance scales to match inventory-update traffic because they share a deployable.

The book's framing: service consolidation is the least glamorous of the four techniques but often the correct one when joint ownership keeps re-appearing. The question *"why are these two services?"* must have a good answer; if the only answer is "they were split at the start and we haven't fixed it," the fix is consolidation.

## Which technique to pick

Chapter 9's stance is explicitly trade-off-driven; no technique is a default. Rough heuristic from the chapter's worked examples:

| Technique | Use when |
|---|---|
| Table split | The shared table actually has two column-groups with distinct owners (Product vs. Inventory count). |
| Data domain | Tables are genuinely shared and the broader bounded context is acceptable. |
| Delegate | One service has clear domain primacy and the other's write traffic is modest. |
| Service consolidation | The services keep needing to coordinate; the original split was probably wrong. |

## Related pages

- [[data-ownership]]
- [[table-split-technique]]
- [[delegate-technique]]
- [[data-domain]]
- [[bounded-context]]
- [[service-granularity]]
- [[granularity-integrators]]
- [[granularity-disintegrators]]
- [[cap-theorem]]
- [[eventual-consistency]]
- [[database-decomposition]]
- [[software-architecture-the-hard-parts]]
