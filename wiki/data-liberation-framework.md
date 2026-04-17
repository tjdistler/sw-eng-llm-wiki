# Data Liberation Framework

**Summary**: A centralized system — Kafka Connect, Apache Gobblin, Apache NiFi, Debezium running under Kafka Connect — that extracts data from source stores into event streams on behalf of many teams. Convenient as a bootstrap for [[data-liberation]], but Bellemare warns it tends to institutionalize two anti-patterns: exposing internal data models to downstream consumers, and making teams passive about producing their own events.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## What a liberation framework does

A dedicated framework runs configurable connectors that query source stores (or follow their change logs) and pipe results into output event streams. All three framework options Bellemare names scale horizontally by adding instances (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Kafka Connect** — Kafka-platform-exclusive; the usual home for the **Debezium** log-based CDC connectors.
- **Apache Gobblin** — more general; supports multiple destinations.
- **Apache NiFi** — broader data-flow tool with routing and transformation.

Framework connectors typically integrate with the Confluent [[schema-registry]], and can be customized to use alternatives.

## Why teams reach for one

A centralized framework lets a single team operate the liberation infrastructure for the whole organization. Other teams contribute a small config — connection string, source table, target stream, schema — and get their data liberated without building anything bespoke. This is attractive at bootstrap time and in larger organizations where many data stores and teams need connecting (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

## The two organizational traps

### Shared ownership of connector health

The framework team owns stability, scaling, and health of both the framework and every connector. The team that owns the captured system owns the schema, the fields, the query volume — and can change any of them without involving the framework team. A schema change or logic change breaks the connector, often detected only by the framework team. This cross-team dependency **scales linearly with the number of connectors** and becomes a recurring interruption budget (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

### Complacency about being event-driven

Once monolith data is flowing into event streams via connectors, the motivation to refactor the source application into a native event producer drops sharply. Teams become content to "requisition new sources and sinks" instead of joining the [[event-driven-microservices|EDM]] ecosystem as active participants. Bellemare's line: CDC tools are **"primarily meant to help bootstrap the process"** — not to be the final destination (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

The broker's value is the quality of data inside it. Connectors that mirror internal data models out to public streams degrade that quality unless aggressively isolated.

## Anti-pattern it enables: internal-data-model exposure

Both [[query-based-cdc]] and log-based [[change-data-capture]] can be set up to dump the source's internal schema straight into public event streams. This is the single biggest recurring failure mode when organizations adopt liberation frameworks. Downstream consumers end up coupled to the producer's private data model, which defeats a primary goal of EDM (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

See [[coupling]] and [[data-contract]] for the principles being violated, and [[eventification]] for the downstream fix when the connector must produce normalized raw streams.

## When a framework is the right call

Bellemare concedes some cases where a centralized source/sink framework is a win (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- Products with **limited development resources**.
- Products in **maintenance-only** operation.
- Initial bootstrap of a new event-driven initiative before teams can take over production themselves.

For products under active development with significant event-stream requirements, he recommends teams take direct ownership of event production — usually via the [[outbox-table-pattern]].

## Mitigations when you must use one

- **Use database views** in front of relational sources so the connector cannot see the internal schema (works for [[query-based-cdc|query-based]] connectors; less applicable to log-based ones).
- **[[eventification|Eventify]] downstream** when log-based CDC forces normalized streams out; consumers should only see the public denormalized stream.
- **Register schemas in a [[schema-registry]]** and enforce [[schema-evolution|evolution compatibility]] at the stream boundary.
- **Plan to migrate off the connector** onto first-party event production as the source team matures.

## Related pages

- [[data-liberation]]
- [[change-data-capture]]
- [[query-based-cdc]]
- [[outbox-table-pattern]]
- [[event-sinking]]
- [[eventification]]
- [[schema-registry]]
- [[data-contract]]
- [[coupling]]
- [[event-driven-microservices]]
- [[event-broker]]
