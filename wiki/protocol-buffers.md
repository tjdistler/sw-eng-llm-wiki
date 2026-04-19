# Protocol Buffers

**Summary**: Google's binary, schema-driven serialization format. Language- and platform-neutral, compact, and fast. Data crossing a [[stubby|Stubby]] or gRPC RPC boundary is encoded as a **protobuf**. Comparable to Apache Thrift; 3-10x smaller and 20-100x faster than XML.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## The short version

Protocol Buffers — "protobufs" — are Google's mechanism for serializing structured data. They share a category with Thrift and [[avro]]: binary, schema-driven, explicit about [[schema-evolution|evolution]] via field tags. See [[encoding-formats]] for the three-category framing and the head-to-head on-wire size comparison.

## The SRE book's pitch

Chapter 2 justifies protobufs against XML in one pointed sentence (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

> Protocol buffers have many advantages over XML for serializing structured data: they are simpler to use, 3 to 10 times smaller, 20 to 100 times faster, and less ambiguous.

The chapter cites Protocol Buffers as the transport format for all [[stubby|Stubby]] RPCs.

## How it works

Full details are on [[encoding-formats]] (the general tree-and-category discussion) and [[schema-evolution]] (the field-tag rules that make forward and backward compatibility work). The briefest summary:

- Developers write a `.proto` schema.
- Code generators produce typed classes in C++, Java, Go, Python, etc. (See [[code-generation]].)
- On the wire, field names are replaced by small integer tags. Unknown tags are preserved when a new code version reads old data; missing fields have defaults.

## Where it fits at Google

- [[stubby]] / gRPC — the RPC transport.
- Persistent storage — writing protobuf bytes directly is common.
- [[bigtable]] — uninterpreted byte-array values are often protobuf-encoded.

## On the contract-strictness spectrum

*Software Architecture: The Hard Parts* Chapter 13 places Protobuf at the **strict end** of the [[contracts|contract-strictness spectrum]], alongside RMI, SOAP/XSD, and gRPC generally (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). The design goal — mimic the semantics of a local method call on a remote one — is what drives the strictness. See [[strict-contract]] for the generalised trade-offs: compile-time safety, rich tooling, and excellent documentation, at the cost of tight coupling and versioning overhead.

gRPC-over-Protobuf defaults to strict contracts. Architects who want looser coupling for a specific integration point either pick a different format (JSON name-value pairs) or pair Protobuf with a [[consumer-driven-contracts|consumer-driven-contract]] test layer so each consumer can declare which fields it actually reads.

## Cross-book connections

- [[encoding-formats]] — the three-category framing (language-specific / textual / binary-schema-driven) that protobuf sits in.
- [[schema-evolution]] — the field-tag evolution rules.
- [[code-generation]] — typed producer/consumer classes.
- [[rpc]] — gRPC context; the wire format vs the call abstraction.

## Related pages

- [[encoding-formats]]
- [[schema-evolution]]
- [[stubby]]
- [[rpc]]
- [[avro]]
- [[code-generation]]
- [[site-reliability-engineering]]
- [[contracts]]
- [[strict-contract]]
- [[software-architecture-the-hard-parts]]
