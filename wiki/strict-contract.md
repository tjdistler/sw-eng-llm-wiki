# Strict Contract

**Summary**: A contract that fixes names, types, count, and order of every field, leaving no ambiguity for the consumer. Examples: RMI, gRPC, SOAP/XSD, versioned REST with JSON Schema. Strict contracts buy compile-time safety, rich tooling, and excellent documentation at the cost of tight coupling, versioning overhead, and fragility in the face of change.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## Definition

> A strict contract requires adherence to names, types, ordering, and all other details, leaving no ambiguity. (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md)

The strictest possible contract in software is a **remote method call** (e.g., Java RMI): the remote call mimics an internal method call exactly, down to parameter names and types. Many strict contract formats share this "imitate a local method call" stance; the RPC family is built on it (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

Strict doesn't require a binary format. A JSON document with a `$schema` reference becomes a strict contract: required fields, types, and value ranges are all enforced (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "properties": {
    "acct":   {"type": "number"},
    "cusip":  {"type": "string"},
    "shares": {"type": "number", "minimum": 100}
  },
  "required": ["acct", "cusip", "shares"]
}
```

## Examples on the strict end of the spectrum

- **RMI / CORBA / DCOM** — method-call mimicry (location transparency). The tightest possible contract.
- **gRPC** — strict contracts by default, carried over Protocol Buffers. See [[rpc]] and [[protocol-buffers]].
- **Thrift** and **Avro RPC** — binary, schema-driven, compatibility rules enforced by the format.
- **SOAP with WSDL/XSD** — heavyweight XML-based schemas; dominant in early-2000s enterprises.
- **REST with JSON Schema** — JSON with an attached schema document that the endpoint validates against.

## Advantages

Chapter 13 enumerates four (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Guaranteed contract fidelity.** Schema verification ensures exact adherence to values, types, and other metadata. Some problem spaces benefit from tight coupling on contract changes — finance, medical, regulated systems.
2. **Versioned.** Strict contracts admit an explicit version number, letting two endpoints serve different clients as the domain evolves.
3. **Easier to verify at build time.** Schema tools turn contract adherence into a compile step, adding a type-checking layer for integration points.
4. **Better documentation.** Distinct parameters and types leave no ambiguity about what a call means.

## Disadvantages

Chapter 13 enumerates two (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Tight coupling.** If two services share a strict contract and the contract changes, both services must change. This is the connascence-of-type/name/position tax.
2. **Versioning is also a disadvantage.** Precision is nice until you're supporting v1, v2, v3, and v4 simultaneously with no deprecation discipline. Strict contracts make versioning *possible*, which means teams end up maintaining multiple versions forever unless they're disciplined about removing old ones.

The chapter's caution: strict contracts are brittle *in proportion to change rate*. A contract that rarely changes can be strict with few downsides. A contract that must change every sprint turns every release into a multi-service coordination.

## When to pick strict

From the chapter and adjacent material:

- **Rich tooling mandates.** If the team depends on code generation, IDE autocomplete, and type-safe client libraries, strict formats deliver those for free.
- **Regulated or safety-critical domains.** If an API violation is a liability event, the format should guarantee structural correctness.
- **Stable, infrequently-changing APIs.** A contract whose shape is settled suffers little from strictness.
- **Single-organisation, coordinated-deployment scope.** Strict contracts are manageable when the teams on both sides of the contract report up the same tree.

## When not to pick strict

- **Microservices architectures that prize [[independent-deployability]].** Strict contracts force lock-step upgrades across independently-deployed services — the opposite of the microservices goal. Chapter 13 explicitly recommends loose contracts plus [[consumer-driven-contracts|CDCs]] as the microservices default (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).
- **Cross-organisation or public APIs with no upgrade authority over consumers.** Strict contracts require versioning to maintain compatibility for unknown clients, leading to long-tail maintenance burdens.
- **Rapidly evolving domains.** If the contract changes faster than teams can coordinate, strict contracts become a bottleneck.

## Strict contracts and compatibility

Strict binary formats (Thrift, Protobuf, Avro) handle evolution via explicit rules — field tags, optional fields with defaults, never-reuse-a-tag. See [[schema-evolution]] and [[backward-forward-compatibility]]. Strictness doesn't forbid evolution; it codifies it.

Strict JSON is the interesting edge case: JSON Schema validates shape but doesn't enforce the same tag-level evolution discipline. Bellemare explicitly warns off JSON for event-driven systems for this reason (source: chapter-03-communication-and-data-contracts.md, via [[schema-evolution]]).

## Relation to connascence

A strict contract maximises **static connascence across the integration boundary**: connascence of name (every field name must match), type (every type must match), position (for positional parameters), and often meaning (enum values, unit conventions). The Page-Jones [[connascence]] rule of locality — weaker forms at longer distances — is the theoretical objection to strict contracts across service boundaries. The practical rebuttal: strict contracts buy compile-time verification of all that connascence, which can be worth it when the integration is stable.

## Related pages

- [[contracts]]
- [[loose-contract]]
- [[rpc]]
- [[protocol-buffers]]
- [[avro]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[breaking-changes]]
- [[connascence]]
- [[static-coupling]]
- [[encoding-formats]]
- [[software-architecture-the-hard-parts]]
