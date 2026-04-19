# Stamp Coupling

**Summary**: Passing an entire data structure between services when each only reads or writes a small portion of it. Originally a structured-programming coupling category (Myers, 1974); Chapter 13 of *Software Architecture: The Hard Parts* revives it as a distributed-systems anti-pattern caused by over-specified contracts, with two serious consequences — **fragility** (unrelated changes break unrelated consumers) and **bandwidth waste** (the "bandwidth is infinite" fallacy). It has one legitimate use: **workflow-state passing in choreographed sagas**.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## Definition

> A common pattern and sometimes anti-pattern in distributed architectures is stamp coupling, which describes passing a large data structure between services, but each service interacts with only a small part of the data structure. (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md)

Four services sitting on a shared message pipeline might each read, write, or both read-and-write only a small slice of the document flowing between them. The canonical natural case: an industry-standard XML document (the travel industry's itinerary XML is Chapter 13's example) that every participant must pass through intact even though each modifies only a few fields.

The pattern is common; the *anti-pattern* is usually **accidental** — an architect over-specifies the contract either as misguided future-proofing, or by reflexively using a shared data structure rather than trimming the payload to only the fields the consumer needs.

## Anti-pattern consequences

### Fragility: unrelated changes break unrelated consumers

Chapter 13's worked example: the **Wishlist Service** needs only a customer's name, looked up by ID, from the **Profile Service**. If the architect contracts the entire `Profile` (name, addr1, addr2, country, …) as the payload, then a change to `state` in Profile — a field Wishlist never touches — still breaks the Wishlist contract and forces a coordinated redeploy (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

The corrective rule: **keep contracts at a "need to know" level**. Pass exactly the fields the consumer reads. This avoids introducing breaking changes where none are semantically warranted.

### Bandwidth: the fallacy bites at scale

Stamp coupling puts the "bandwidth is infinite" fallacy of distributed computing on full display. Chapter 13's arithmetic (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

| Payload | Rate | Bandwidth |
|---|---|---|
| 500 KB full Profile stamp | 2,000 req/s | **1,000,000 KB/s (≈1 GB/s)** |
| 200 bytes just-the-name | 2,000 req/s | **400 KB/s** |

A factor-of-2,500 saving for no loss of functionality. Stamp coupling is the distributed-architecture equivalent of shipping a full object through a function call when a reference would do — except the cost is network bandwidth, not a pointer dereference.

Monolithic architectures tolerate overpowered parameter passing because in-process calls don't cross the wire. Once the calls cross the wire, the cost becomes load-bearing, and an architect who didn't think about it inherits the bill.

## Where the pattern originates

Chapter 13 calls out two accidental routes into stamp coupling (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

1. **Over-specification for future-proofing.** The architect includes every field in the contract "because the consumer might want them later." They won't — and now every change ripples.
2. **Industry-standard document formats.** Natural case, usually XML; an architect inherits the pattern without making an explicit choice. The travel industry's shared itinerary XML is the example.

It is also the natural result of using strict contracts built from the *producer's* internal data model rather than the *consumer's* actual needs. A GraphQL-style consumer-driven selection sidesteps this; see [[graphql]].

## The legitimate use: workflow state in choreographed sagas

Chapter 13 balances the critique with a legitimate use: **workflow state passing in choreography**. When an architect picks a [[workflow-choreography|choreographed]] [[saga]] for scalability reasons but the workflow is complex, stamp coupling can *replace* a mediator by attaching workflow state (status, transaction flags, previous-step success/failure, error messages) to the message itself (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md).

The shape: each service receives the contract, updates *both* its domain slice and the workflow-state slice, and forwards. At the end the terminal receiver queries the accumulated state to decide success, failure, or retry.

This does create higher-than-nominal coupling between services, but the **semantic coupling has to go somewhere** ("an architect cannot reduce semantic coupling via implementation"). Stamp-coupled choreography vs. orchestration is a trade-off — the stamp-coupled version buys scalability at the cost of contract richness. See [[semantic-coupling]] for the underlying principle.

For the alternatives, see [[workflow-orchestration]] (centralised state) and [[workflow-choreography]] (distributed state).

## Stamp coupling vs strict contract

Stamp coupling is adjacent to but distinct from [[strict-contract|strict contract]] choice. A strict contract *can* be narrow (only the name field, strictly typed) — which has none of the stamp-coupling problems. A loose contract *can* be over-stamped (the full Profile, loosely serialised as JSON) — which still bleeds bandwidth and still propagates fragility, just without the compile-time breakage. The two axes are orthogonal:

| | Narrow (need-to-know) | Wide (stamp-coupled) |
|---|---|---|
| **Strict contract** | Compile-time safe; decoupled | Compile-time safe; high fragility |
| **Loose contract** | Runtime checked (CDC); decoupled | Runtime checked; high fragility + bandwidth bill |

The remedy is narrower contracts, regardless of strictness. Strictness determines *when* breakage is detected; stamp coupling determines *how often* breakage occurs and how much bandwidth the happy path costs.

## Trade-offs summary

Chapter 13 closes the stamp-coupling section with a trade-off table (the shape of Table 13-4 in the book; not reproduced verbatim in the extracted markdown, but summarised from the surrounding text):

**Advantages**

- Enables complex choreographed workflows without a mediator.
- Matches natural data formats in certain industries (XML-standard documents).

**Disadvantages**

- Fragility — unrelated changes propagate as breakage.
- Bandwidth — unneeded payload amplifies at request rate.
- Contract brittleness if combined with strict contracts.

## Related pages

- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[graphql]]
- [[workflow-choreography]]
- [[workflow-orchestration]]
- [[saga]]
- [[semantic-coupling]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[connascence]]
- [[software-architecture-the-hard-parts]]
