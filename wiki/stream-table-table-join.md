# Stream-Table-Table Join

**Summary**: A compound enrichment pattern — materialize an entity stream into a table, aggregate a second input stream into a second table, and join the two tables on a shared key — used when a microservice needs to enrich business aggregates with relational context. Chapter 12 presents it as the canonical worked example of [[lightweight-framework-microservice|lightweight-framework]] expressiveness in Kafka Streams, combining [[repartitioning]], `groupByKey` + `aggregate`, and a full-outer table-table join in a short topology (source: chapter-12-lightweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-12-lightweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## The scenario

An advertising company produces a session-windowed stream of user actions (views and clicks, keyed by `<windowId, userId>`). A downstream service wants to bill advertisers based on completed view-to-click conversions, broken out per advertisement, enriched with the advertisement's name and owner (source: chapter-12-lightweight-framework-microservices.md).

Three inputs:

- **Advertisement-Sessions stream** — session-windowed user actions.
- **Advertisement-Conversions stream** — derived: one event per view-click pair, keyed by `advertisementId`.
- **Advertisement entity stream** — entity events keyed by `advertisementId` carrying `name`, `address`, owning customer, etc.

One output:

- **Enriched-Advertising-Engagements stream** — one event per advertisement, value = `{sum, name, type, ...}`.

## Topology

```
KStream<WindowKey, Actions> userSessions = ...

// stage 1/2: transform sessions into conversion events, rekey on advertisementId
KTable<AdvertisementId, Long> conversions = userSessions
    .transform(...)                // sessions -> conversions
    .groupByKey()
    .aggregate(...);               // sum per advertisementId -> KTable

// materialize the advertisement entity stream as a KTable
KTable<AdvertisementId, Advertisement> advertisements = ...

// full-outer table-table join; automatic copartitioning
conversions
    .join(advertisements, joinFunc)
    .to("AdvertisementEngagements");
```

(adapted from source: chapter-12-lightweight-framework-microservices.md)

## Stage-by-stage

1. **Repartition the Advertisement entity stream** from its original partition count up to 12 so it copartitions with the conversions stream. An internal repartitioning topic (see [[broker-as-shuffle-service]]) carries the advertisement events. Both tables are now copartitioned by `advertisementId` across 12 partitions — the copartitioning is established implicitly by the join operation in the topology (source: chapter-12-lightweight-framework-microservices.md).
2. **Produce conversion events** from sessions. Each session event can produce zero or more conversion events (one per view-click pair). Events are keyed by `advertisementId`.
3. **Aggregate** conversions into a KTable `<advertisementId, conversionSum>` — a simple running sum. The aggregation is stored in a [[internal-state-store|state store]] backed by a [[changelog-stream]].
4. **Join** the conversion-sum KTable with the advertisement-entity KTable. The join function decides the output shape (enrichment columns, tombstone semantics), much like a SQL `SELECT` clause.

The equivalent SQL is a plain full-outer join (source: chapter-12-lightweight-framework-microservices.md):

```sql
SELECT adConversionSumTable.sum, adTable.name, adTable.type
FROM adConversionSumTable
FULL OUTER JOIN adTable ON adConversionSumTable.id = adTable.id
```

## Parallelism

- The service can spin up between 1 and 12 instances. Input-partition count sets the upper bound on useful parallelism.
- Off-peak hours may run with 1–2 instances; peak hours scale up to 12.
- Because the entity stream's partition count was 3 (not 12), it had to be repartitioned through an internal 12-partition topic before the join could be copartitioned.

This is the lightweight framework leveraging the broker both as a shuffle medium (for the repartition) and as a state-durability medium (for the aggregation's changelog) — see [[broker-as-shuffle-service]] and [[changelog-stream]].

## Tombstones and full-outer joins

The join function receives `(sum, advertisement)` pairs where either side may be null (source: chapter-12-lightweight-framework-microservices.md):

```java
public EnrichedAd joinFunction(Long sum, Advertisement ad) {
    if (sum != null || ad != null)
        return new EnrichedAd(sum, ad.name, ad.type);
    else
        // Both sides null — upstream deletion on both sides; emit tombstone.
        return null;
}
```

Most frameworks differentiate inner, left, right, outer, and foreign-key joins and handle [[tombstone|tombstone]] propagation for you — but the example demonstrates the underlying semantics explicitly. Kafka Streams in particular supports foreign-key table-table joins, which are useful when the business key on one side is not the table's own primary key.

## Why this is the lightweight-framework worked example

The pattern showcases features that lightweight frameworks (Kafka Streams, Samza embedded) provide out of the box and that BPC services and FaaS handlers have to build by hand (source: chapter-12-lightweight-framework-microservices.md):

- Indefinitely retained materialized KTables.
- Automatic copartitioning triggered by join operators in the topology.
- Changelog-backed aggregation state.
- A SQL-like join surface.

It also leans on every broker-as-infrastructure affordance the lightweight model provides: internal topics as shuffles, changelogs as durability, consumer-group membership as parallelism. The example fits on a page; the equivalent BPC implementation would not.

## Related pages

- [[lightweight-framework-microservice]]
- [[stream-joins]]
- [[repartitioning]]
- [[copartitioning]]
- [[changelog-stream]]
- [[internal-state-store]]
- [[broker-as-shuffle-service]]
- [[table-stream-duality]]
- [[materialized-state]]
- [[tombstone]]
- [[windowing]]
