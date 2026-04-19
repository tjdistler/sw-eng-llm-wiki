# Schema Evolution

**Summary**: Schema evolution is the set of rules a binary encoding format provides for safely changing a schema over time — adding fields, removing fields, changing types — without breaking [[backward-forward-compatibility]].

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## The Problem

Schemas inevitably change. Fields are added when features are added; fields are removed when features are deprecated; types change. But encoded data from old schemas persists in databases, queues, and files long after the code that wrote it has been replaced. See [[data-outlives-code]].

Each [[encoding-formats|encoding format]] has a different mechanism for handling these changes.

## Thrift and Protocol Buffers: Field Tags

Both Thrift and Protocol Buffers use **field tags** — small integers assigned to each field in the schema definition:

```
// Protocol Buffers
message Person {
  required string user_name       = 1;
  optional int64  favorite_number = 2;
  repeated string interests       = 3;
}
```

The field tag (1, 2, 3) is what appears in the encoded binary — not the field name. This has a critical consequence: **field names can be changed freely; field tags cannot**.

### Adding Fields

Add a new field with a new, never-previously-used tag number. Old code (which doesn't know this tag) will encounter it, see an unfamiliar tag, and skip it — the datatype annotation tells the parser how many bytes to consume. **Forward compatibility is preserved**.

New code reading old data will simply not see the new field — it fills in the default value. **Backward compatibility is preserved**, *provided the new field is optional or has a default*. A required new field breaks backward compatibility because old data won't contain it.

### Removing Fields

You can only remove an optional field. After removal, **never reuse that tag number** — old encoded data may still contain records with that tag, and if new code assigns the tag to a different field, it will misinterpret the old data.

### Changing Types

Type changes are risky. Widening (e.g., 32-bit → 64-bit integer) works for new code reading old data (fills missing bits with zeros), but old code reading new data may truncate the value.

Protocol Buffers has no list/array type; instead it uses `repeated` — the same tag appears multiple times. This allows safely evolving a single-valued `optional` field into a multi-valued `repeated` field. Thrift has a dedicated list type, which doesn't allow this evolution but supports nested lists.

## Avro: Writer's Schema and Reader's Schema

Avro takes a completely different approach — there are **no field tags in the schema**:

```
record Person {
  string               userName;
  union { null, long } favoriteNumber = null;
  array<string>        interests;
}
```

The encoded binary is just values concatenated in schema order, with no field identifiers at all. The schema is required to interpret the bytes. This makes Avro the most compact format (32 bytes for the sample record).

### Schema Resolution

Avro distinguishes the **writer's schema** (what was used to encode the data) from the **reader's schema** (what the reading code expects). These don't need to be the same — only **compatible**. The Avro library resolves differences by matching fields by name:

- Field in writer's schema but not reader's schema → ignored.
- Field in reader's schema but not writer's schema → filled in with the reader's declared default.
- Fields in different order → matched by name, not position.

### Rules for Avro Schema Evolution

- **Adding a field**: must have a default value. New readers fill in the default when reading old data.
- **Removing a field**: must have a default value (so old readers can fill it in from their schema). 
- **Null values**: Avro does not allow null by default. To allow null, you must use a union type: `union { null, long } field`. The default value must match the first branch of the union.
- **Renaming a field**: the reader's schema can declare aliases for field names, allowing backward compatibility. This is backward compatible (new reader can match old writer's name via alias) but not forward compatible.
- **Changing a type**: possible if Avro can convert the type.

### How Readers Know the Writer's Schema

Avro must transmit the writer's schema alongside data; the mechanism varies by context:

- **Large files (Avro object container files)**: writer's schema included once at the file header. Common in Hadoop/batch contexts.
- **Database records**: each record includes a schema version number; a schema registry maps version numbers to schemas (used by LinkedIn's Espresso).
- **Network connections**: schema version negotiated at connection setup (Avro RPC).

### Avro's Advantage: Dynamically Generated Schemas

Because Avro has no field tags, schemas can be generated automatically without manual tag management. For example: generate an Avro schema from a relational database table, one field per column. When the DB schema changes, regenerate the Avro schema. Readers with old schemas still work because field matching is by name.

With Thrift or Protocol Buffers, an administrator would need to manually maintain tag assignments each time a column is added or renamed — tags cannot be auto-assigned without risk of collision with previously used tags.

## Why Schemas Are Valuable

Beyond compatibility, schemas provide:

- **Documentation**: the schema must be current for decoding to work — unlike hand-maintained docs, it can't silently diverge.
- **Pre-deployment compatibility checks**: a schema registry can verify that a proposed change is compatible before deployment.
- **Code generation**: statically typed languages get type-safe generated code with IDE support.
- **Compactness**: field names are omitted from the encoded data.

## Bellemare's three compatibility types

Chapter 3 of *Building Event-Driven Microservices* names the three compatibility modes every event-driven [[data-contract]] must be configured with (source: chapter-03-communication-and-data-contracts.md):

- **Forward compatibility** — data written with a *newer* schema is readable as if written with an *older* schema. This is the most common pattern in practice: the producer updates its schema and begins writing the new format while consumers still hold the old schema. Consumers only update if they need access to the new fields.
- **Backward compatibility** — data written with an *older* schema is readable as if written with a *newer* schema. Useful when the consumer needs to be released before the producer (schema-already-defined), when a producer's release cadence lags (customer-installed software like a phone app reporting metrics), or when consumers reprocess historical data under the current schema.
- **Full compatibility** — the union of forward and backward. Bellemare's explicit recommendation: *use this whenever possible*. "You can always loosen the compatibility requirements at a later date, but it is often far more difficult to tighten them" (source: chapter-03-communication-and-data-contracts.md).

Full compatibility also enables a specific freedom in [[code-generation|consumer code generation]]: under full compatibility the consumer can use any version of the schema — older, newer, or the same — to generate its class definitions.

## Why schema evolution is non-negotiable in EDM

Bellemare frames schema evolution as a *requirement*, not a convenience (source: chapter-03-communication-and-data-contracts.md). Without it, producers and consumers must coordinate closely on releases; previously compatible data stops being readable; old consumers are forced to update whenever a producer changes its schema. All of those pathologies directly contradict the [[independent-deployability]] property that [[event-driven-microservices]] are supposed to deliver. Schema evolution is the mechanism that makes the data contract *evolvable* without producer/consumer lock-step.

## Schema-format selection and evolution

The format you pick directly determines what evolution rules are available. Bellemare recommends [[avro|Apache Avro]] or [[encoding-formats|Protobuf]] and explicitly warns against JSON because "it does not provide full-compatibility schema evolution" (source: chapter-03-communication-and-data-contracts.md). Plain-text key/value events are similarly discouraged.

A [[schema-registry]] is the enforcement point — it evaluates proposed schema changes against the configured compatibility mode and rejects registrations that would break the rule, before the producer can deploy.

## FoDE framing — schema evolution across the lifecycle

Reis and Housley's Chapter 2 treats schema evolution as a cross-cutting problem the data engineer must plan for at every lifecycle stage (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **At source systems.** "One of the most challenging nuances of source data is the schema." Chapter 2 calls out **Agile's encouragement of schema evolution** as a direct cause of pain downstream: "a key part of the data engineer's job is taking raw data input in the source system schema and transforming this into valuable output for analytics. This job becomes more challenging as the source schema evolves." The source-system evaluation questions include "If schema changes (say, a new column is added), how is this dealt with and communicated to downstream stakeholders?" See [[source-systems]].
- **At storage.** The evaluation of a storage system includes "Are you capturing metadata about schema evolution, data flows, data lineage, and so forth?" — schema change is operational metadata that belongs in the [[data-catalog|catalog]]. See [[data-storage-stage]].
- **As technical metadata.** Schema is one of the three key technical-metadata examples Chapter 2 calls out (alongside pipeline metadata and data lineage). See [[metadata]].

The FoDE take is not adding technical mechanism beyond what DDIA and Bellemare already describe; it's positioning schema evolution as a **communication and governance problem** that extends from source-system owners, through ingestion, into the catalog, and out to downstream analysts.

## FoDE Ch 7 — ingestion-layer automation and the three-part defense

Chapter 7 of *Fundamentals of Data Engineering* treats schema evolution as a first-class [[data-ingestion|ingestion]] concern. Two Ch 7 additions to the picture:

### Automation is a mixed blessing

"It's becoming increasingly common for ingestion tools to automate the detection of schema changes and even auto-update target tables. Ultimately, this is something of a mixed blessing. Schema changes can still break pipelines downstream of staging and ingestion" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Even when ingestion auto-accommodates a change:

- Pipelines further downstream may still break.
- The new schema may silently degrade report or model performance.
- Analysts and data scientists relying on the data "should be informed of the schema changes that violate existing assumptions."

**Communication remains essential** regardless of automation — the human channel is not replaceable by a tool.

### Three-part defense

Ch 7 prescribes three mechanisms against schema-evolution damage during stream ingestion (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

1. **[[schema-registry|Schema registry]]** — version schema changes at the platform level.
2. **[[dead-letter-queue|Dead-letter queue]]** — investigate events that are not properly handled because of an unexpected schema.
3. **Upstream communication** — "the low-fidelity route (and the most effective): regularly communicating with upstream stakeholders about potential schema changes and proactively addressing schema changes with the teams introducing these changes instead of reacting to the receiving end of breaking changes."

The third is the one Ch 7 specifically calls out as most effective — a direct application of the broader FoDE thesis that the data engineer's communication with upstream software engineers is a high-leverage investment.

### Git-style branching for schema change (DataOps undercurrent)

Ch 7's undercurrent section floats a forward-looking idea: cloud storage is cheap enough that an organization could maintain multiple versions of a table with different schemas in orchestration tools like Airflow. Schema changes, upstream transformations, and code changes could appear in "development" versions of the table before being merged into the main one — modeled on Git's branching approach to concurrent versioning. "A few years ago, such an approach to data was unthinkable. On-premises MPP systems are typically operated at close to maximum storage capacity" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

This is not a concrete pattern yet but a direction; Reis and Housley describe it as an approach they "have meditated on for a while" as a possible resolution to the command-and-control-review vs auto-rewrite-everything extremes.

## Hard Parts Ch 13 framing — evolution is a contract-strictness trade-off

*Software Architecture: The Hard Parts* Chapter 13 places schema evolution inside the broader **[[contracts|strict-to-loose contract spectrum]]** trade-off (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). The evolution mechanism a format provides is part of its strictness profile:

- **Strict contracts with formal evolution rules** (Protobuf, Avro, Thrift) — evolution is explicit, enforceable at build time, and caught by schema registries. The cost is coordinated versioning discipline.
- **Strict contracts without explicit evolution** (RMI, SOAP/XSD in full ceremony) — evolution requires new versioned endpoints, leading to "integration nightmare" when deprecation discipline is absent.
- **Loose contracts** (JSON name-value pairs) — evolution is free on the wire but contract fidelity must be recovered via [[consumer-driven-contracts|consumer-driven contract tests]] running as [[architecture-fitness-function|fitness functions]].

The Ch 13 editorial point: **you don't pick a strictness and then figure out evolution — you pick an evolution story and that determines how strict the contract can usefully be.** The three compatibility types from Bellemare (forward, backward, full) and the field-tag / reader-writer-schema mechanics from DDIA are the concrete tools a strict-with-evolution contract uses to avoid becoming a strict-without-evolution nightmare.

## Testing compatibility at code-submission time

Chapter 15 recommends moving the compatibility check *earlier* than deployment: pull the registered schemas from the [[schema-registry]] and run evolutionary-rule checking as part of the code-submission/CI pipeline (source: chapter-15-testing-event-driven-microservices.md). For stacks that auto-generate schemas from class/struct definitions at compile time, this becomes a mechanical diff between the previous registered schema and the new compile-time-generated one — a failing check blocks the PR rather than the deploy. Good candidate for a [[architecture-fitness-function]].

## Related pages

- [[encoding-formats]]
- [[backward-forward-compatibility]]
- [[avro]]
- [[data-outlives-code]]
- [[data-contract]]
- [[schema-registry]]
- [[code-generation]]
- [[breaking-changes]]
- [[event-driven-microservices]]
- [[source-systems]]
- [[metadata]]
- [[data-catalog]]
- [[data-ingestion]]
- [[ingestion-payload]]
- [[dead-letter-queue]]
- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[consumer-driven-contracts]]
- [[software-architecture-the-hard-parts]]
