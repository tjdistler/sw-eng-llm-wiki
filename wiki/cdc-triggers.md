# CDC via Triggers

**Summary**: An older [[data-liberation]] mechanism in which database triggers fire on INSERT/UPDATE/DELETE and write a corresponding row to a change-data (audit) table, which is then drained by a publisher. Triggers predate binlogs and write-ahead logs and are supported by most relational databases, but scale poorly and cannot generally validate output schemas before the fact.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## Mechanics

An AFTER trigger on the source table fires on INSERT, UPDATE, or DELETE and inserts a row into a change-data table. The trigger captures the event time and an autoincrementing sequence ID for the publisher to use. A separate publisher process then reads the change-data table and emits events to the event stream — typically using [[query-based-cdc|query-based CDC]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

If the trigger itself fails, the underlying command also fails — update atomicity is preserved.

## After-the-fact schema validation

The change-data table schema sits **between** the source-table schema and the output-event schema. Triggers typically cannot run the output-schema validation during execution because:

- Many databases restrict the languages triggers can run in. PostgreSQL can execute C, Python, or Perl and therefore can host validation logic; most others cannot.
- Even when technically supported, trigger overhead per row is nontrivial, and embedding serialization is often too expensive at production load.

So validation usually happens **after** the row lands in the change-data table. Unserializable rows must be error-handled — typically requiring human intervention (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md). Bellemare's practical advice: keep the change-data table schema tightly synchronized with the output event schema, and **test for incompatibilities before deploying to production**.

This is the same after-the-fact failure mode that [[outbox-table-pattern#schema-validation-before-vs-after-the-write|after-the-write outboxes]] suffer from.

## Benefits

- **Supported by most databases.** Triggers are a long-standing feature of relational systems (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Low overhead for small data sets.** A handful of triggers are easy to configure and maintain.
- **Customizable logic.** Trigger code can project only a subset of fields, providing some isolation from the internal data model.

## Drawbacks

- **Performance overhead.** Triggers execute inline with every write. Services with tight SLAs may find the load unacceptable.
- **Change management complexity.** Application changes or DDL changes require corresponding trigger changes; an overlooked trigger silently diverges the capture from the source (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).
- **Poor scaling.** The trigger count grows linearly with the number of tables being captured, on top of any triggers already in use for business logic.
- **After-the-fact schema enforcement.** As above; invalid rows land in the change-data table before anyone knows they are invalid.

## When triggers are still a reasonable choice

Bellemare's guidance: **prefer more modern mechanisms when available**, but triggers can be a fine fit for legacy systems (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- The technology is old and stable; trigger support is rarely a concern.
- Access and load patterns are well understood, so trigger overhead can be estimated accurately.
- Schemas are unlikely to change — minimizing the after-the-fact validation problem.

Newman arrives at a related judgement from a different direction — in [[change-data-capture]] he quotes Randy Shoup: *"Having one or two triggers isn't terrible. Building a whole system off them is a terrible idea."* The two books' guidance aligns: triggers are a local tactic, not an architectural substrate.

## Relationship to other patterns

- [[data-liberation]] — triggers are one of the mechanisms for populating a capture table, alongside [[query-based-cdc]], log-based [[change-data-capture]], and the [[outbox-table-pattern]].
- [[outbox-table-pattern]] — the modern replacement; the application layer (not the database) writes the outbox row in the same transaction, usually with **before-the-write** schema validation.
- [[change-data-capture]] — the log-based alternative is generally preferable to triggers where supported.

## Related pages

- [[data-liberation]]
- [[outbox-table-pattern]]
- [[query-based-cdc]]
- [[change-data-capture]]
- [[schema-evolution]]
- [[schema-registry]]
- [[data-contract]]
