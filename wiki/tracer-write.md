# Pattern: Tracer Write

**Summary**: Migrate the source of truth for a piece of data incrementally by tolerating two sources of truth during the migration. New writes go to both old and new stores; consumers move over piece by piece; eventually the old source retires. A variant of [[synchronize-data-in-application]] tuned for microservice extractions.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

Identify a new service that will host the relocated data. The current system continues to maintain its own copy, but every change is also written to the new service via its API. Code is migrated to read from the new service; once everyone has moved, the old source retires. (source: chapter-04-decomposing-the-database.md)

The name comes from the idea that you can start with a *small set* of data being synchronised — a "tracer" — and grow it over time, increasing the number of fields synced and the number of consumers using the new source. (source: chapter-04-decomposing-the-database.md)

## Why two sources of truth, on purpose?

Wanting a single source of truth is rational, but if you insist on it, the migration has to be a *big bang*: before the release the monolith is the source; after the release the new service is. Lots of things can go wrong in that switchover. Tracer write trades the conceptual simplicity of one source of truth for a phased switchover with much smaller per-release risk. (source: chapter-04-decomposing-the-database.md)

## Three ways to keep the sources in sync

Newman lists three options and the trade-offs (source: chapter-04-decomposing-the-database.md):

| Option | How it works | Trade-off |
|---|---|---|
| **Write to one source, sync to the other** | Writes go to one, and a background process replicates to the other ([[change-data-capture]] is the obvious mechanism) | Window of inconsistency = sync lag; one-way is much simpler |
| **Send writes to both sources** | Upstream clients (or an intermediary) call both stores | Caller must handle partial failures |
| **Seed writes to either source** | Either side can take a write, with two-way sync behind the scenes | Avoid this — two-way sync is hard |

In all three you get [[eventual-consistency]]: both sources will agree, eventually. The window of inconsistency is shorter with streaming sync, longer with nightly batch.

Newman emphasises **reconciliation**: don't rely on hope. Run SQL queries against both sources to verify they agree. Run the new source for a period with no consumers until you trust it. (source: chapter-04-decomposing-the-database.md)

## Square's Fulfillments service

Square used this pattern to untangle their `Order` concept, which had bundled three different workflows (customer ordering, restaurant preparing, driver delivering) into a single object. Different teams contended for the same code. (source: chapter-04-decomposing-the-database.md)

The migration:

1. Created a new `Fulfillments` service for the restaurant- and driver-related parts of an order.
2. Ran a background worker that called the `Fulfillments` API to copy existing data over (controlled by a feature flag for easy off-switch).
3. Once trusted, code that updated restaurant- or driver-related order data was changed to write to *both* the old system and the new `Fulfillments` service via two API calls.
4. Migrated consumers one at a time to read from the new service.
5. Each consumer migration was, in Derek Hammer's words, "pretty much a non-event."

These dual writes were not atomic — there was a brief window where one system reflected the change and the other didn't. For Square's use case, this [[eventual-consistency]] was acceptable. (source: chapter-04-decomposing-the-database.md)

Newman notes that an event-driven architecture would have made this cleaner: a single `Order Updated` event could be consumed by both stores via pub/sub. Retrofitting an event bus *just* for this would be too much work, but if you already have one, lean on it. (source: chapter-04-decomposing-the-database.md)

Square chose to keep the duplicated data permanently in this case — losing the new service's availability would still leave a fallback view in the old system. The cost is keeping the synchronisation in place. (source: chapter-04-decomposing-the-database.md)

## Where to use it

- When data ownership is moving between services and you want a phased cutover.
- When you can tolerate brief inconsistency between the two stores ([[eventual-consistency]]).
- When you have an event-driven system or [[change-data-capture]] pipeline already, much of the synchronisation infrastructure is in place.
- Avoid two-way sync if you can. The shorter the inconsistency window you need, the harder this gets. (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[synchronize-data-in-application]]
- [[change-data-ownership]]
- [[change-data-capture]]
- [[strangler-fig-pattern]]
- [[eventual-consistency]]
- [[message-brokers]]
