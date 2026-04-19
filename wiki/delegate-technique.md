# Delegate Technique

**Summary**: A [[joint-ownership-techniques|joint-ownership]] resolution from *Software Architecture: The Hard Parts* Chapter 9: pick one service as the **delegate** (sole owner of the shared table); all other services that need to write go through it. Trades atomicity for single-writer clarity.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The shape

Given a table written by services A and B, pick A as the delegate. A now solely owns the table, exactly as in the [[data-ownership|single-ownership]] case. B no longer writes the table directly — it **sends write requests** to A over the network (REST, gRPC, request-reply messaging, or async messaging) and A performs the write on B's behalf (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

This resembles the fix the chapter applies to [[data-ownership|common ownership]] (dedicated service owner + remote writes), but at smaller scale: only a couple of services are involved and one of them already has a legitimate claim on the table.

## Who to pick as the delegate

Chapter 9 names two rules (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

### Primary domain priority

Pick the service that does most of the **primary-entity CRUD**. For the Product example, the Catalog Service creates, updates, and removes products — static-data operations on the entity itself. It is the natural owner. The Inventory Service, responsible for `inv_cnt` mutations, sends update requests to Catalog.

Pros:
- Domain alignment. The service that "is about" products owns the product data.
- Error handling for product CRUD lives in one place.

Cons:
- The high-volume writer (Inventory, in this example) pays the remote-call tax on every update.

### Operational characteristics priority

Pick the service with the higher operational demand — performance, scalability, throughput, availability. For the Product example, that's Inventory Service: inventory updates are far more frequent than product-metadata edits. Making Inventory the delegate means the hot path uses direct DB calls.

Pros:
- Fast path matches actual load profile.
- Most volatile data (inventory count) is highly consistent.

Cons:
- **Domain responsibility mismatch.** Inventory Service is not "about" product records, yet it's now responsible for product CRUD and the corresponding error handling.
- The chapter's critique: the code gets weirder to navigate — inventory code coexisting with catalog-maintenance code.

### The book's preference

The chapter prefers **primary domain priority** and recommends addressing performance/fault-tolerance pressure on the non-delegate with **caching** (replicated in-memory cache or distributed cache) rather than reversing the ownership call (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

## What the delegate technique costs you

The structural costs hold no matter which delegate you pick (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

- **Service coupling.** The non-delegate is now a client of the delegate for every write. Schema or API changes propagate across the boundary.
- **No atomic transaction.** A multi-table business operation that touches both a non-delegate-owned table and the delegated table cannot be wrapped in one ACID transaction.
- **Performance.** Every non-delegate write crosses a network.
- **Fault tolerance.** Delegate unavailability means non-delegate writes fail or queue.

Because of the atomicity loss, the delegate technique is **suitable only for writes that do not require cross-boundary atomicity** and can tolerate [[eventual-consistency]] via async comms. If you need atomic updates across both sides, you are in [[distributed-transactions]] territory — and the chapter's answer is [[saga|sagas]], not 2PC.

## Sync vs async

The write-request channel can be either:

- **Sync** (HTTP/gRPC, request-reply messaging) — non-delegate waits for confirmation. Stronger consistency; worse performance; availability of non-delegate coupled to delegate.
- **Async** (fire-and-forget over a queue) — non-delegate doesn't wait. Eventually consistent; faster; non-delegate can keep working when delegate is down; but errors in the delegate can silently drop the write.

The chapter emphasises: async eliminates the waiting-time penalty but *loses the ability to confirm the write landed* unless you add explicit ack / retry / dead-letter machinery.

## Trade-off summary

| | For | Against |
|---|---|---|
| **Delegate technique** | Restores sole ownership of the table; clear domain home; cacheable hot paths; works for "one service really does own this" cases | Cross-boundary atomicity gone; network-hop per non-delegate write; delegate becomes bottleneck/SPOF; error handling for remote writes is complex |

## Relationship to other techniques

- **[[table-split-technique]]** — splits the schema so each service has its own table; delegate keeps one table and picks a winner.
- **[[data-domain]] technique** — both services still write, inside a broader bounded context; delegate restricts writes to one service.
- **Service consolidation** — merges the services entirely (see [[joint-ownership-techniques]]); delegate keeps them separate but makes one subordinate for this data.

## Related pages

- [[joint-ownership-techniques]]
- [[data-ownership]]
- [[table-split-technique]]
- [[data-domain]]
- [[distributed-transactions]]
- [[eventual-consistency]]
- [[saga]]
- [[saga|compensating actions]]
- [[cap-theorem]]
- [[software-architecture-the-hard-parts]]
