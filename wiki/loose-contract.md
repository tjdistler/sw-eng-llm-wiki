# Loose Contract

**Summary**: A contract expressed as minimally as possible — usually name-value pairs in JSON or YAML with no schema attached. The opposite pole of [[strict-contract|strict contracts]] on Chapter 13's contract-strictness spectrum. Loose contracts deliver high decoupling and easy evolution at the cost of no structural verification — the safety net must be recovered through [[consumer-driven-contracts|consumer-driven contract tests]] acting as [[architecture-fitness-function|fitness functions]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## Definition

At the far end of the spectrum, loose contracts are *just the raw facts* — no metadata, no type information, no required/optional markers (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

```json
{
  "name":   "Mark",
  "status": "active",
  "joined": "2003"
}
```

This is the *lingua franca of integration architecture*: every common platform can produce and consume name-value pairs (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

## Advantages

Chapter 13 enumerates three (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Highly decoupled.** The minimum possible structural commitment between producer and consumer. Microservices architectures explicitly aim for this.
2. **Easier to evolve.** Add a new field and no existing consumer breaks — they simply don't read it. Remove an optional field and consumers that expected it can fall back to defaults. Implementation-side evolution is nearly free (semantic changes still require coordination).
3. **Platform independence.** Name-value pairs cross any technology boundary. If one service is Python and another is Go and a third is Java, JSON name-value pairs work identically. No code generation required on any side.

## Disadvantages

Chapter 13 enumerates two (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Contract management.** No schema means no type-checking, no required-field enforcement, no detection of misspelled field names. Bugs that a schema would have caught at compile time now surface as runtime exceptions.
2. **Requires fitness functions.** The recommended remedy for the above is [[consumer-driven-contracts|CDC testing]] run as an [[architecture-fitness-function|architectural fitness function]] in CI — consumers publish their expectations, and the provider's pipeline validates every candidate build against them.

## The microservices default

Chapter 13 is explicit: **loose contracts plus consumer-driven contracts are the microservices default** (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). This pair resolves the seeming contradiction between "microservices want loose coupling" and "microservices need integration correctness":

- Loose contracts deliver the decoupling the architecture style aspires to.
- CDCs deliver the contract fidelity developers need.
- The two *together* give architects the ability to dial strictness up per consumer — one consumer can enforce numeric ranges on a field that another consumer doesn't even read.

The trade-offs (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

- Requires engineering maturity — teams that respect failing contract tests and run them on every build.
- Requires two interlocking mechanisms (name-value pairs plus CDC tests), rather than one end-to-end schema tool. Two simple tools often beat one complex one, but the operational burden must be accounted for.

## Loose contracts are not unverified contracts

A common misreading of "loose" is "no validation". Chapter 13's pitch is subtler: the validation moves from *schema-at-build-time* to *consumer-test-at-build-time*. The correctness budget is the same; the ownership shifts from producer to consumer, which is appropriate — the consumer is the party who actually knows what fields they depend on and what ranges they can tolerate.

## When to pick loose

- **Microservices with many independent consumers.** The loose-plus-CDC pattern scales better than versioning a strict contract across N consumers.
- **Rapidly evolving integration points.** Loose contracts let producers add fields freely without coordinating with consumers.
- **Cross-language, cross-organisation integration.** JSON name-value pairs are the universal serialization.
- **When producer and consumer have independent release cadences.** Loose contracts are compatible with any release timing; strict contracts force coordination.

## When not to pick loose

- **Regulated or safety-critical integrations** where runtime validation is too late.
- **Teams without the discipline to maintain CDC tests.** Without the fitness-function layer, loose contracts *are* unsafe.
- **Integrations that need rich tooling.** If IDE autocomplete and generated client libraries are load-bearing for developer productivity, a strict format earns its keep.

## Loose does not forbid schemas

A JSON document is loose *by default*; it becomes strict when you attach a JSON Schema. The spectrum is continuous — teams can add just enough structure to catch the errors that matter while leaving the rest evolvable. Chapter 13's example of a JSON contract with a `$schema` reference is precisely the middle ground: loose wire format, strict validation (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

## Relation to connascence

Loose contracts minimise connascence across the integration boundary to **connascence of name only** — producer and consumer must agree on the names of the fields they both care about, and nothing else. No type agreement (the receiver parses), no positional agreement (order doesn't matter in name-value pairs), no schema-meaning agreement until CDC tests add it back. This is the [[connascence|Page-Jones rule-of-locality]] ideal: weakest forms at longest distances.

## Related pages

- [[contracts]]
- [[strict-contract]]
- [[consumer-driven-contracts]]
- [[architecture-fitness-function]]
- [[stamp-coupling]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[connascence]]
- [[static-coupling]]
- [[encoding-formats]]
- [[software-architecture-the-hard-parts]]
