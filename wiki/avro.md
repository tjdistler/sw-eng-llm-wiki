# Avro

**Summary**: Apache Avro is a binary encoding format distinguished by having no field tags — it encodes only values, relying on schema resolution to match writer's schema against reader's schema by field name. This makes it the most compact of the major binary formats and uniquely suited to dynamically generated schemas.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Last updated**: 2026-04-15

---

## Origins

Avro was started in 2009 as a subproject of Hadoop, because Thrift was not a good fit for Hadoop's use cases — specifically, the need to generate schemas dynamically from external sources like relational database tables.

## How Avro Encodes Data

Avro has two schema languages: Avro IDL (human-editable) and a JSON-based representation (machine-readable).

```
// Avro IDL
record Person {
  string               userName;
  union { null, long } favoriteNumber = null;
  array<string>        interests;
}
```

The encoded binary for this record is **just 32 bytes** — the most compact of any encoding discussed in [[encoding-formats]]. The encoding contains *no field names, no field tags, no type annotations*. It is purely values concatenated in schema-defined order. Without the schema, the bytes are uninterpretable.

## Writer's Schema and Reader's Schema

This is Avro's defining concept. Avro distinguishes two roles:

- **Writer's schema**: the schema the encoder used when writing the data (compiled into the application at write time).
- **Reader's schema**: the schema the decoder expects (compiled into the application at read time).

These two schemas need not be identical — they only need to be **compatible**. The Avro library resolves differences by comparing the two schemas side by side:

| Situation | Resolution |
|---|---|
| Field in writer's schema, not in reader's schema | Field is ignored |
| Field in reader's schema, not in writer's schema | Reader's declared default value is used |
| Fields in different order | Matched by field name, not position |

This is fundamentally different from Thrift and Protocol Buffers, where the encoded data carries field tag numbers that the decoder uses directly. In Avro, the schema itself performs that lookup at read time.

## Schema Evolution Rules

See [[schema-evolution]] for the full treatment. The key rules:

- You may only add or remove a field that **has a default value**.
- Null is not a default for all types — to allow null, you must declare `union { null, long }` and the default must match the first branch.
- Avro has no `required` or `optional` markers; it uses union types and default values instead.
- Field renaming is backward compatible (new reader can alias old name) but not forward compatible.

## How Readers Know the Writer's Schema

Since the encoded bytes contain no schema information, the writer's schema must be transmitted through one of these mechanisms:

- **Avro object container files**: writer's schema is embedded once at the file header. All records in the file use the same schema. This is the standard approach in Hadoop batch jobs and is ideal for [[data-warehousing|archival storage]].
- **Schema version in each record**: each database record stores a schema version number; a schema registry resolves version → schema. Used by LinkedIn's Espresso document database.
- **Connection-level negotiation**: two processes communicating over a long-lived connection negotiate schema version at setup and use it for all messages on that connection (Avro RPC protocol).

A shared schema registry is valuable in all cases — it acts as documentation and enables pre-deployment compatibility checking.

## Dynamically Generated Schemas

This is Avro's key advantage over Thrift and Protocol Buffers. Because Avro has no tag numbers, schemas can be generated automatically:

**Example**: Dump a relational database to Avro.
1. Generate an Avro schema from the database table schema (one field per column, field name = column name).
2. Encode all rows using that schema.
3. When the database schema changes, regenerate the Avro schema and re-export.
4. Old readers still work because Avro matches fields by name — if a column was added, old readers ignore it; if a column was removed, old readers fill in their default.

With Thrift or Protocol Buffers, a human would need to manually maintain tag number assignments with each schema change — tags must be unique and never reused, so auto-generation risks tag collisions.

## Code Generation

Thrift and Protocol Buffers are designed around code generation — the schema produces language-specific classes. This works well for statically typed languages (Java, C++, C#) but is awkward for dynamically typed languages (Python, Ruby, JavaScript) where there is no compile-time type checker and an explicit compilation step is considered undesirable.

Avro supports optional code generation for statically typed languages, but can also be used without it. An Avro object container file is self-describing — it includes the writer's schema in the header. Tools like Apache Pig can open Avro files, inspect fields, and write derived output in Avro format without any schema pre-definition.

## Related pages

- [[encoding-formats]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[data-outlives-code]]
- [[rpc]]
