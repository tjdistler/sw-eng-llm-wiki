---
name: Encoding Formats
description: Three categories of data encoding (language-specific, textual, binary schema-driven) and their compatibility and portability tradeoffs
type: reference
---

# Encoding Formats

**Summary**: When data moves between processes — over a network or to disk — it must be encoded as a byte sequence. Encoding formats fall into three categories with very different tradeoffs around portability, human-readability, compactness, and schema evolution support.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Last updated**: 2026-04-15

---

## The Translation Problem

In memory, data lives in objects, structs, hash tables, and trees — optimized for CPU access via pointers. On the wire or on disk, data must be a self-contained byte sequence with no pointers. The translation is called **encoding** (also: serialization, marshalling); the reverse is **decoding** (parsing, deserialization, unmarshalling).

## Category 1: Language-Specific Formats

Built-in serialization mechanisms: Java's `java.io.Serializable`, Python's `pickle`, Ruby's `Marshal`, Kryo for Java.

**Problems**:
- Tied to a single language — sharing data across language boundaries is difficult or impossible.
- Decoding requires instantiating arbitrary classes, which is a security vulnerability (attackers can execute arbitrary code by crafting a malicious byte sequence).
- Versioning is an afterthought — forward and backward compatibility are not designed in.
- Often poor performance and bloated output (Java serialization is notorious).

**Verdict**: Only use for ephemeral, transient purposes. Never for storage or cross-system communication.

## Category 2: Textual Formats (JSON, XML, CSV)

Widely supported, human-readable, language-independent. JSON is popular because of browser support and simplicity. XML is more verbose. CSV is minimal.

**Strengths**: Universally readable, easy to debug, agreed-upon by most parties.

**Problems**:
- **Numeric ambiguity**: XML and CSV cannot distinguish numbers from digit-strings without an external schema. JSON distinguishes strings from numbers but not integers from floats, and has no precision specification — numbers > 2⁵³ are misrepresented in JavaScript (Twitter's workaround: send tweet IDs as both number and string).
- **No binary strings**: Binary data must be Base64-encoded, adding ~33% overhead and requiring out-of-band schema knowledge to interpret correctly.
- **Optional schemas**: JSON Schema and XML Schema exist but are often omitted. Without them, applications must hardcode encoding/decoding logic.
- **CSV is vague**: No schema, ambiguous escaping, fragile with commas or newlines in values.

**Verdict**: Good enough for cross-organizational data interchange where human-readability and universal support matter more than precision or compactness. Compatibility depends entirely on application-level discipline.

### Binary JSON Variants

MessagePack, BSON, BJSON, UBJSON, Smile (for JSON); WBXML, Fast Infoset (for XML). These preserve the JSON/XML data model but encode more compactly. Because they still embed field names in every record, the space savings are modest (e.g., 81 bytes → 66 bytes for MessagePack vs. 32 bytes for Avro on the same record).

## Category 3: Binary Schema-Driven Formats

Thrift, Protocol Buffers, and Avro all require an explicit schema and use that schema to encode data compactly. Field names are not stored in every record — only field identifiers or positional order are used.

**Strengths**:
- Much more compact than textual formats (the same record: JSON = 81 bytes, Thrift CompactProtocol = 34 bytes, Avro = 32 bytes).
- Schema is authoritative documentation — it must be current for decoding to work, unlike hand-maintained docs.
- Compatibility rules are explicit: forward and backward compatibility are built into the format. See [[schema-evolution]].
- Code generation enables compile-time type checking in statically typed languages.
- Schema databases enable compatibility checking before deployment.

**Tradeoffs**:
- Data is not human-readable without a decoder.
- Schema must be managed — stored, versioned, and distributed.

**Verdict**: Preferred for internal service-to-service communication and storage at scale. Each format has a distinct approach to schema evolution; see [[avro]] for the most distinctive one.

## Encoding formats in batch processing

In the Hadoop ecosystem, structured binary formats replace the ad hoc text parsing used by Unix tools. The two most common formats (source: designing-data-intensive-applications, chapter 10):

- **Avro** — Row-oriented binary format with schema-based encoding. Often used for data transport and storage in [[distributed-filesystems|HDFS]]. Supports [[schema-evolution]] via writer's/reader's schema resolution.
- **Parquet** — Columnar format based on Google's Dremel. Enables [[column-oriented-storage]] optimizations: reading only needed columns and applying vectorized execution in [[dataflow-engines]].

These formats eliminate the low-value syntactic parsing (e.g., `{print $7}`) that Unix tools require, while providing efficient, schema-aware encoding that evolves over time (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[backward-forward-compatibility]]
- [[schema-evolution]]
- [[avro]]
- [[rpc]]
- [[message-brokers]]
- [[batch-processing]]
- [[distributed-filesystems]]
- [[column-oriented-storage]]
