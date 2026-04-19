# Contracts

**Summary**: Chapter 13 of *Software Architecture: The Hard Parts* broadens the word *contract* from "REST/SOAP/gRPC endpoint" to **the format any two parts of an architecture use to convey information or dependencies** — including transitive library dependencies, caches, message schemas, URLs, and method signatures. Contracts are the cross-cutting dimension that sits orthogonally to the three-force model (communication/consistency/coordination) and decides how services couple. The central design axis is the **strict-to-loose spectrum**, and the trade-off is coupling-with-tooling versus evolvability-with-fragility.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## The broadened definition

> **Contract**: The format used by parts of an architecture to convey information or dependencies. (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md)

Ford, Richards, Sadalage, and Dehghani deliberately widen the definition. A contract is *any* wiring point between parts of a system — not just the REST or gRPC endpoint an architect instinctively thinks of. This includes (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

- Internal and external integration points.
- Transitive library and framework dependencies.
- Caches and other shared runtime state.
- Method signatures across module boundaries.
- URLs, IP addresses, and any hard-coded coupling point.

This framing is why [[static-coupling]] and contracts are the same topic from different angles. Every static coupling point *is* a contract; the question is only how strict it is.

## The strict-to-loose spectrum

Contracts live on a spectrum, not a binary (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

```
strict ───────────────────────────────── loose
 RMI / gRPC / SOAP-XSD     REST / GraphQL     JSON name-value pairs
```

- **[[strict-contract|Strict]]** — names, types, count, ordering, and other details are all fixed. Mimics the semantics of an internal method call. Tooling enforces adherence at build time.
- **Moderate** — REST resources and GraphQL sit in the middle. REST lets the resource grow without breaking old clients; GraphQL has strict types but consumer-driven field selection, so unused additions don't cascade.
- **[[loose-contract|Loose]]** — name-value pairs in JSON or YAML with no schema attached. Evolvable, decoupled, but offers no structural guarantees.

Even nominally loose formats can be tightened: JSON Schema can be layered over JSON to turn a loose contract into a strict one (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). The strictness is a design choice, not a property of the wire format.

## The trade-off table

Chapter 13 summarises the comparison across the spectrum:

| Dimension | Strict contracts | Loose contracts |
|---|---|---|
| **Coupling** | Tight — both sides must change together | Loose — services can evolve independently |
| **Verification** | Compile/build-time schema check | Runtime; requires [[consumer-driven-contracts|CDC]] tests |
| **Tooling** | Rich — generators, IDE support, validators | Thin — names only |
| **Versioning** | Explicit; can become a nightmare if deprecation discipline is weak | Implicit; evolution without version numbers |
| **Documentation** | Excellent — the schema is the doc | Poor — must be documented out-of-band |
| **Evolvability** | Hard — every change ripples | Easy — add fields freely |
| **Fragility** | Low structurally, high coordination cost | High structurally, low coordination cost |
| **Certainty** | Guaranteed contract fidelity | No guarantees without fitness functions |

The recurring theme: **Strictness buys certainty at the cost of coupling; looseness buys evolvability at the cost of certainty.** Neither is universally better; the architect picks per integration point.

## The microservices default

Chapter 13's explicit recommendation for microservices architectures: **default to loose contracts (name-value pairs) plus [[consumer-driven-contracts|consumer-driven contracts]] as a fitness function** (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). This pair resolves the apparent contradiction between "microservices want loose coupling" and "microservices need contract fidelity":

- Name-value pairs give the loose coupling microservices aspire to.
- CDCs let each consumer specify exactly what it relies on, and the provider's CI verifies every consumer's expectations on every build.
- The consumer can tighten the contract *specifically for itself* without forcing tightness on other consumers.

Two advantages of CDCs over schema-only tightness (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Variable strictness per consumer.** Different consumers can specify different levels of rigour, including value-range checks that most schemas can't express.
2. **Testing covers semantic as well as structural breakage** — schemas catch shape changes; CDCs catch behaviour changes.

The disadvantages: this approach requires **engineering maturity** (teams that respect failed contract tests) and **two interlocking mechanisms** (name-value pairs plus CDCs) rather than one end-to-end schema tool. The architect accepts two simple tools instead of one complex one.

See [[consumer-driven-contracts]] for the mechanics, and [[architecture-fitness-function]] for the CI-level enforcement pattern.

## GraphQL as the interesting middle

Chapter 13 singles out GraphQL as a middle-of-the-spectrum design that avoids the usual strict-contract brittleness (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). Two `Profile` representations — a Wishlist-facing one that exposes only `name`, and a full Customer-facing one that exposes name/address/country — can both be valid views of the same underlying data because GraphQL lets the consumer ask for only the fields it cares about.

The effect: strict types but **consumer-driven field selection**. Adding a new field to `Profile` doesn't break the Wishlist, because the Wishlist never requested that field. This is the structural defence against [[stamp-coupling]] that a naive strict contract lacks.

See [[graphql]] for the full treatment.

## Stamp coupling and over-specification

The anti-pattern the chapter names most aggressively: **[[stamp-coupling|stamp coupling]]** — passing a whole data structure when only a small subset is needed (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). Usually an accident; sometimes a misguided "just-in-case" future-proofing move.

Consequences:

- **Fragility.** A change to any field in the structure breaks every consumer's contract, even consumers that don't care about the changed field.
- **Bandwidth.** The "bandwidth is infinite" fallacy bites hard at scale: 2,000 req/s × 500 KB payloads burns 1 GB/s for no reason when the actual required field is a 100-byte name.

The corrective rule: **keep contracts at a "need to know" level** — include exactly the fields the consumer uses, no more. See [[stamp-coupling]] for the full treatment, including its *legitimate* use for workflow-state passing in choreographed sagas.

## Contract fitness functions

Loose contracts need a safety net. Chapter 13's recommendation is to run [[consumer-driven-contracts|consumer-driven contract tests]] as [[architecture-fitness-function|architectural fitness functions]] in CI:

- Each consumer commits a contract file describing the fields, types, and value constraints it depends on.
- The provider's build pipeline runs every consumer's contract against every candidate build.
- A failing consumer contract fails the build, not production.

This is the CDC-as-governance pattern — it makes loose contracts safe at scale by pushing verification from runtime to build time, and shifts the cost from incident response to CI minutes. See [[architecture-fitness-function]] and [[consumer-driven-contracts]].

## Semantic vs implementation coupling

A contract can only express **implementation coupling** — the coupling the architect introduces via the wire format and schema. It cannot reduce the underlying **[[semantic-coupling|semantic coupling]]** inherent in the domain. The architect's job is to keep implementation coupling as close to the semantic floor as possible; contract design is one of the main levers.

Loose contracts reduce *implementation* coupling without touching semantic coupling. Strict contracts let the architect pile on more implementation coupling — sometimes for good reasons (tooling, documentation), sometimes accidentally (stamp coupling).

## Where contracts sit in the *Hard Parts* framework

- Contracts are the **fourth dimension** that cuts across the three-axis dynamic-coupling space (communication × consistency × coordination). The trade-off matrix of the three axes is incomplete until contract strictness is also decided (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).
- Contracts are the primitive of [[static-coupling]]. Every static coupling point is a contract; Chapter 2's enumeration of static-coupling types (OS, frameworks, libraries, databases, method signatures, URLs) is a list of contracts at different levels of the stack.
- Contract strictness decisions are load-bearing for [[connascence]]. A strict contract maximises connascence of name, type, position, and meaning across the integration boundary; a loose contract exposes only connascence of name.

## Related pages

- [[strict-contract]]
- [[loose-contract]]
- [[stamp-coupling]]
- [[consumer-driven-contracts]]
- [[data-contract]]
- [[graphql]]
- [[rpc]]
- [[protocol-buffers]]
- [[avro]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[breaking-changes]]
- [[semantic-coupling]]
- [[static-coupling]]
- [[connascence]]
- [[architecture-fitness-function]]
- [[encoding-formats]]
- [[explicit-vs-implicit-schemas]]
- [[software-architecture-the-hard-parts]]
