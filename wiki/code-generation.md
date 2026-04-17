# Code Generation

**Summary**: Turning an event schema into a language-specific class definition (or equivalent structure) that producers and consumers program against. Code generation turns the [[data-contract]] into a compile-time check: the producer cannot ship code that violates the schema, and the consumer gets typed access to fields with IDE and compiler support.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Last updated**: 2026-04-17

---

## Producer workflow

On the producer side, code generation closes the loop between schema and runtime (source: chapter-03-communication-and-data-contracts.md):

1. The schema is written in an IDL (Avro IDL, `.proto`, Thrift IDL).
2. A generator tool produces a class/struct in the producer's language.
3. The producer populates an instance of that class and hands it to a serializer.
4. The serializer (or compiler, depending on language) **enforces** that required fields are present and types match before the event is sent to the [[event-broker]].

Bellemare's "producer event production workflow using a code generator" (Figure 3-1 in Chapter 3) makes this explicit: the generated class is the gate between business logic and broker-facing bytes.

## Consumer workflow

On the consumer side (source: chapter-03-communication-and-data-contracts.md):

1. The consumer maintains its own version of the schema — which may be older or newer than the producer's, depending on [[schema-evolution]] compatibility.
2. The event arrives; the consumer looks up the writer's schema (from the event or from a [[schema-registry]]) and deserializes.
3. The deserialized record is then converted to the consumer's own schema version, applying defaults for missing fields and dropping fields the consumer does not know about. This is where [[backward-forward-compatibility|compatibility rules]] do their work.
4. Finally the record is materialized as an instance of the generated class, and business logic begins.

Bellemare illustrates this as "Figure 3-2: consumer event consumption and conversion workflow using a code generator," noting explicitly that under full compatibility a producer on schema v2 and a consumer on schema v1 can coexist indefinitely.

## Benefits

Two benefits compound (source: chapter-03-communication-and-data-contracts.md):

- **Compiler checks in static languages.** In Java, Go, C#, Rust, etc., code will not compile unless it respects the schema — unpopulated non-null fields, wrong types, and mis-handled enums are caught before the build artifact exists.
- **IDE support in dynamic languages.** Even Python, Ruby, or JavaScript code benefits: IDEs can complete field names, flag type mismatches in setters, and surface the schema as documentation. This is far better than the generic key/value map alternative that has none of those affordances.

The deeper win is that mishandling event data — the single largest class of EDM integration bug — becomes a compile-time or author-time failure instead of a 3am page.

## Relationship to other encoding formats

This is also the DDIA Chapter 4 treatment of the same topic (source: chapter-04-encoding-and-evolution.md): Thrift and Protocol Buffers are designed around code generation, whereas [[avro|Avro]] supports optional code generation because it can also operate with a dynamically supplied writer's schema. In strongly typed languages, the compile-time guarantees are the whole point; in dynamically typed languages, some teams skip code generation and work with the deserialized records directly.

## Related pages

- [[data-contract]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[schema-registry]]
- [[avro]]
- [[encoding-formats]]
- [[explicit-vs-implicit-schemas]]
- [[event-structure]]
