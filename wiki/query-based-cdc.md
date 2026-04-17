# Query-Based CDC

**Summary**: The [[data-liberation]] pattern in which a client periodically queries the source data store and emits selected results to an event stream. Works against any data store but requires an `updated_at` (or autoincrementing id) column, cannot see hard deletes, and exposes the internal data model unless isolated with database views.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## Mechanics

A client uses the data store's API (SQL or otherwise) to request a specific data set. An initial **bulk load** queries and publishes all existing rows; thereafter, an **incremental update** polls for changes and emits only rows that have been added or modified (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Four query shapes are common:

| Query shape | When to use |
|---|---|
| **Bulk loading** | Small tables where the whole set fits cheaply; also required as the one-time seed for every incremental approach |
| **Incremental timestamp loading** | Filter by `updated_at > last_seen_time` — the default for mutable tables |
| **Autoincrementing ID loading** | Filter by `id > last_seen_id` — for immutable rows (e.g. an [[outbox-table-pattern|outbox table]]) |
| **Custom querying** | Denormalize across joined tables, filter by partner, or otherwise hide the internal data model |

(source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md)

## Choosing the poll interval

Three interacting dials (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Frequency vs load.** Higher polling frequency means lower propagation latency but more load on the source store.
- **Interval vs query duration.** If a poll starts before the previous one finishes, the two queries can race and older data can overwrite newer data in the output stream.
- **Initial bulk load first.** Every incremental pipeline must begin with a full bulk load; otherwise pre-existing rows never appear in the stream.

## Benefits

- **Customizability.** Any data store can be queried, with the full range of client query options available (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Independent polling periods.** Different queries can run at different frequencies to meet different SLAs.
- **Isolation of the internal data model.** Relational databases can expose read-only or materialized views to the CDC client so that the internal schema is hidden. Bellemare singles this out as a significant advantage over [[change-data-capture|log-based CDC]], which leaks the internal model by construction (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Drawbacks

- **Requires `updated_at` (or autoincrementing id).** Tables lacking a last-modified column must be altered to add one, or query-based CDC is not possible (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Untraceable hard deletes.** A DELETE leaves no trace in the query results. Deletions can only be captured via **soft deletes** (an `is_deleted` boolean or similar).
- **Brittle dependency between source schema and output event schema.** The CDC client lives outside the application codebase; valid data-set changes can break the output schema. Compatibility is detected only after the fact.
- **Intermittent capture.** Multiple in-between updates to the same row collapse into a single event at poll time. If you need every transition, query-based CDC will not give them to you.
- **Production resource consumption.** Each query competes with the application for the source store's resources. A read replica mitigates this at additional cost and complexity.
- **Variable query performance.** The worst case is that the whole data set changed between polls; the query is then as expensive as a bulk load and may race the next poll.

See [[coupling]] for the general concern about leaking source schemas.

## When Bellemare recommends it

Query-based CDC is the most broadly applicable pattern because it works on any data store. It is particularly well suited to (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- Sources that already have disciplined `updated_at` conventions.
- Small or medium data sets where bulk re-reads are cheap.
- Situations where a database view can be placed between the store and the CDC client to isolate the internal data model.
- Immutable, append-only tables — in particular, an [[outbox-table-pattern|outbox]] being drained by autoincrementing-id loading.

For mutable high-volume relational sources where hard deletes must be tracked, log-based CDC or the outbox pattern are usually better fits.

## Relationship to other patterns

- [[change-data-capture]] — the Kleppmann/Newman-level framing; query-based is one of three patterns under the same umbrella in Bellemare's Chapter 4 decomposition.
- [[outbox-table-pattern]] — often drained by a query-based client using autoincrementing-id loading.
- [[cdc-triggers]] — a precursor mechanism; triggers write to an audit table that is then drained by a query.
- [[data-liberation-framework]] — Kafka Connect and Apache Gobblin ship with query-based connectors for many relational sources.

## Related pages

- [[data-liberation]]
- [[change-data-capture]]
- [[outbox-table-pattern]]
- [[cdc-triggers]]
- [[data-liberation-framework]]
- [[schema-evolution]]
- [[database-view-pattern]]
- [[coupling]]
- [[event-streams]]
- [[schema-registry]]
