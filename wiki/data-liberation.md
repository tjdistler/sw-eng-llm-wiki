# Data Liberation

**Summary**: Adam Bellemare's term for the process of identifying cross-domain data sets trapped inside legacy systems' implementation data stores and publishing them to event streams so they become available to the rest of the organization as the new single source of truth. Data liberation is the on-ramp for migrating toward [[event-driven-microservices]].

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`

**Last updated**: 2026-04-17

---

## Definition

Data liberation is the **identification and publication of cross-domain data sets to their corresponding event streams**, and is part of a migration strategy for event-driven architectures (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md). Cross-domain data sets include any data stored in one data store that is required by other external systems — product catalogs, prices, stock, payments, customer records, and so on.

Point-to-point dependencies between existing services and data stores are the telltale sign of cross-domain data that should be liberated: if three services all query the same legacy database directly, the data the three of them need is a candidate for liberation (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## What liberation enforces

Liberation delivers two primary features of event-driven architecture (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Single source of truth.** Liberated streams standardize how systems across the organization access the data — consumers couple on the [[data-contract]] of an event stream rather than on an underlying table or service.
- **Elimination of direct coupling.** Downstream systems no longer reach into the legacy data store. Reactive event-driven consumers can be built against the stream, and legacy systems can be migrated in due time.

See [[event-as-single-source-of-truth]] and [[coupling]].

## Compromise: unidirectional liberation

In the ideal, every service would **publish to the event broker first** and then materialize state back from the stream — including the service that produced the data in the first place (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md). That posture fully realizes the event as single source of truth.

This is often impractical for legacy systems. Bellemare names three reasons refactoring is frequently infeasible (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Limited developer support** for legacy systems; low-effort solutions are required.
- **Expense of refactoring** a complex MVC monolith into an event-driven consumer.
- **Legacy support risk** — the system's responsibilities may be unclear due to technical debt and undocumented point-to-point connections.

The compromise is **unidirectional** data liberation: the legacy system keeps its internal state, CDC mechanisms extract changes to the event stream, and the legacy system never reads back from the stream. The event stream is kept eventually consistent with the internal data set through strictly controlled publishing (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

A critical property: the liberated stream, if materialized, must produce an **exact replica** of the source table. This replica property is what lets downstream event-driven services rebuild their own state from the stream — see [[table-stream-duality]].

## Three liberation patterns

There are three main patterns for extracting data from an underlying store (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

| Pattern | How it works | Page |
|---|---|---|
| **Query-based** | Periodically query the data store; emit results to the event stream | [[query-based-cdc]] |
| **Log-based** | Follow the data store's append-only change log (binlog / WAL) | [[change-data-capture]] (log-based section) |
| **Table-based (outbox)** | Application writes to an outbox table inside the same transaction; a publisher drains the outbox | [[outbox-table-pattern]] |

Triggers are a fourth, older mechanism — see [[cdc-triggers]].

One commonality across all three: each should produce events in **sorted timestamp order**, using the source record's most recent `updated_at` time in the output event's header, not the wall-clock time of publishing. This keeps the stream timestamped by event occurrence for accurate downstream interleaving (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Liberated data is still event data

Liberated events are subject to the same schema discipline as any other events. They must have an explicitly defined, evolutionarily compatible schema registered in a [[schema-registry]], use the organization's standard event format, and respect the full suite of [[event-design-guidelines]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Failing to schematize liberated data is particularly damaging because consumers are forced to parse or interpret the producer's internal data, which breaks the single-source-of-truth property the liberation is supposed to deliver.

## Frameworks vs self-owned liberation

Two organizational stances are possible (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Centralized liberation frameworks** — Kafka Connect, Apache Gobblin, Apache NiFi. Convenient for teams with limited resources, but they tend to encourage an anti-pattern: exposing the producer's internal data model directly to downstream consumers. See [[data-liberation-framework]].
- **Teams own their own event production** — services themselves become event-driven producers (often using the [[outbox-table-pattern]]). More up-front work but eliminates cross-team connector dependencies and propagates an "event-first" culture.

Bellemare's warning: CDC tooling is **a bootstrap, not a final destination**. Organizations that become complacent once their monolith data is connected via CDC end up with the broker acting as glue between monoliths instead of as a first-class data communication layer (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Drawbacks and cost

Liberation is never free. Beyond the per-pattern costs catalogued in [[query-based-cdc]], [[outbox-table-pattern]], and [[cdc-triggers]], there are cross-cutting concerns:

- **Internal data-model exposure.** Query and log-based patterns both leak the producer's internal schema unless actively isolated (via database views or dedicated outbox denormalization). Exposing internal models to downstream consumers is an anti-pattern that increases [[coupling]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **DDL evolution under capture.** Valid alterations to the source data set may be invalid evolutions of the output event schema. See [[schema-evolution]] and the DDL-capture section below.
- **Ownership ambiguity.** A centralized framework team becomes a dependency of every team whose data it captures; decisions made by the data-owner team (new field, renamed column, logic change) can silently break the connector (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Capturing DDL changes

Data-definition changes (adding, dropping, renaming, retyping columns) are routine but can break the output event schema. Capture of DDL depends on the pattern (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Query pattern** — schema is inferred at query time; compatibility checks happen **after the fact**.
- **CDC log pattern** — DDL entries live in the log; support is limited (Debezium currently supports MySQL DDL only). Again, **after the fact**.
- **Change-data table / outbox pattern** — DDL is integrated with the source system's development cycle; the outbox schema acts as a bridge, and incompatible changes are caught **before release**.

The outbox's bridge role is one of the main reasons Bellemare recommends it over the more reactive CDC-framework approaches.

## Sequencing and the composition payoff (Chapter 17)

Bellemare's conclusion adds two pragmatic framings (source: chapter-17-conclusion.md):

- **Liberation is a lengthy process — prioritize by business value.** It will take time to get all necessary data into the broker. "Start by liberating the data that is most commonly used and most critical to your organization's next major goals." Don't try to liberate everything at once; pick the data that unblocks the highest-value next move.
- **Composition as the return on investment.** Once business-critical data is readily available as event streams, *a new service is built by subscribing to the streams of interest* rather than directly connecting to each system that provides the data. The broker absorbs the integration cost that used to be paid per-connection. This is the deferred payoff that justifies the up-front liberation work — see [[event-driven-microservices]]'s closing-framings section.

Treat liberation effort as investment in the [[communication-structures|data communication structure]]: every liberated stream reduces the cost of every future consumer that needs that data.

## Cultural shift

Liberation is ultimately a cultural project, not just a technical one. Data owners must accept that their event streams are products — with SLAs on schema, data model, ordering, latency, and correctness — and not just a side-effect of running a connector against their database. The quality of the data communication layer equals the quality of the data inside it (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## Related pages

- [[change-data-capture]]
- [[query-based-cdc]]
- [[outbox-table-pattern]]
- [[cdc-triggers]]
- [[data-liberation-framework]]
- [[event-sinking]]
- [[eventification]]
- [[event-driven-microservices]]
- [[event-as-single-source-of-truth]]
- [[event-broker]]
- [[event-streams]]
- [[data-contract]]
- [[schema-registry]]
- [[schema-evolution]]
- [[coupling]]
- [[communication-structures]]
- [[table-stream-duality]]
