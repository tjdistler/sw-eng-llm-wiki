# Outbox Table Pattern

**Summary**: A [[data-liberation]] pattern in which every significant change to the application's internal tables is written to an **outbox table in the same transaction**. A separate publisher process drains the outbox and emits events to the [[event-broker]], then deletes the drained rows. The pattern gives the strongest consistency between internal state and the output event stream that a CDC mechanism can offer, at the cost of application-code changes.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## Mechanics

Whenever an INSERT, UPDATE, or DELETE touches a table marked for capture, the application also writes a corresponding row to an outbox table. **Both writes happen inside one transaction** — either both succeed or both fail. A separate thread or process polls the outbox, publishes each row as an event to the configured stream, and deletes the row once publication succeeds (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

The outbox leverages the durability of the source data store: it is a write-ahead log for events awaiting publication. Transactional atomicity prevents the outbox and the internal tables from diverging, which would be difficult to detect and repair.

## Required columns

Two columns are load-bearing (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Strict ordering identifier** — an autoincrementing ID assigned at insertion time. Necessary because the same primary key may be updated many times in quick succession. Without an ordering ID, the publisher would have to find and overwrite previous entries, which is slow and drops intermediate updates from the stream.
- **`created_at` timestamp** — the event time, which should be used in the output event's header instead of the publisher's wall clock. This enables accurate downstream interleaving when consumers merge multiple streams.

## Delivery guarantees

The outbox pattern provides **at-least-once delivery**. If the broker, publisher, or data store fails, the outbox still holds the event and re-publication will succeed eventually. Duplicate events must be handled by consumers (see [[idempotence]]), which is typically inexpensive for entity-event streams where updates are idempotent anyway (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Schema validation: before vs after the write

When the outbox is serialized matters a lot for consistency.

### Before-the-write serialization (strongly preferred)

The event is schematized and serialized **prior to committing the outbox row**. A serialization failure rolls back the transaction, keeping the internal tables and the outbox in sync and preventing an invalid event from ever being written (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Advantages:

- Data inconsistency between internal state and the output stream is eliminated by construction.
- Event data is treated as a first-class citizen — publishing a correctly-shaped event is as important as updating internal state.
- A **single shared outbox table** can be used for all entities, since the content is just pre-serialized bytes plus an `output_stream` routing key.

Drawback: serialization overhead is inline with the business transaction. For very hot paths, this can be nontrivial. Schema failures also block the underlying business process — a real cost in legacy systems.

### After-the-write serialization

Events are written to typed outboxes (one per entity) in their raw form, and serialized by the publisher before production (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Drawback: if the row does not match the current output schema, it has already been committed. Rolling back a completed transaction is at best expensive and at worst impossible. In practice, unserializable events accumulate, human intervention is required, and other events may have been published around the bad ones — producing order anomalies in the output stream.

Bellemare's guidance: **validate and serialize before writing to the outbox** wherever possible. This is "the strongest guarantee that a change-data capture solution can offer" (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Isolating the internal data model

An outbox does **not** need to map 1:1 to an internal table. Two ways to keep the internal model hidden from downstream consumers (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Denormalize on insert.** The application composes the final public-shaped event and writes that to the outbox. Costs storage and CPU, but the outbox directly reflects the public [[data-contract]].
- **[[eventification|Eventify]] downstream.** Keep a 1:1 mapping to private, internal-shaped streams, and run a dedicated downstream stream processor that joins and denormalizes them into the public stream.

Exposing the internal model directly is explicitly called out as an anti-pattern; downstream consumers must see only the public data contract defined in [[data-contract]].

## Benefits

- **Multilanguage support.** Any client or framework with transactional capability can implement the pattern (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Before-the-fact schema enforcement.** Serialization at write time prevents propagation of schema-incompatible events. See [[schema-evolution]].
- **Isolation of the internal data model.** The application chooses what fields to emit.
- **Denormalization.** Data can be joined and flattened before entering the outbox.
- **Delete tracking is built in.** DELETEs are regular events on the outbox; no soft-delete workaround needed.

## Drawbacks

- **Required application-code changes.** Outboxes require the application developers' attention and testing resources. This is a higher up-front cost than [[query-based-cdc]] or log-based [[change-data-capture]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Business-process performance impact.** Serialization, extra writes, and occasional rollbacks add latency to the transaction. Schema failures can block business operations.
- **Data-store performance impact.** Nontrivial extra write/read/delete load, especially at volume.

Bellemare frames the cost choice plainly: every cost saved on the producer side tends to show up amplified on the consumer side (schema cleanup, decoupling from internal models). An outbox pays the cost once, in one place, at the source (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Built-in change-data tables

Some databases (notably SQL Server) provide built-in change-data tables rather than change-data logs. A CDC framework like [[data-liberation-framework|Kafka Connect]] running Debezium can drain a change-data table using the query pattern — functionally close to an outbox but managed by the database itself (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Relationship to other patterns

- [[data-liberation]] — the outbox is one of three primary liberation patterns, and Bellemare's recommended approach when teams own their own event production.
- [[query-based-cdc]] — the mechanism typically used to drain the outbox (autoincrementing-id loading).
- [[cdc-triggers]] — an older alternative that also writes to an audit table, but from within the database rather than the application.
- [[change-data-capture]] — the log-based alternative; requires no application-code change but exposes the internal model and cannot validate schemas before the fact.
- [[eventification]] — the downstream denormalization step when an outbox keeps private 1:1 streams.

## Related pages

- [[data-liberation]]
- [[change-data-capture]]
- [[query-based-cdc]]
- [[cdc-triggers]]
- [[eventification]]
- [[data-contract]]
- [[schema-registry]]
- [[schema-evolution]]
- [[event-broker]]
- [[event-as-single-source-of-truth]]
- [[idempotence]]
- [[coupling]]
