# Schema Evolution

**Summary**: Schema evolution is the set of rules a binary encoding format provides for safely changing a schema over time — adding fields, removing fields, changing types — without breaking [[backward-forward-compatibility]].

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

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
