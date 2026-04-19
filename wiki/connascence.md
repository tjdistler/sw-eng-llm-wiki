# Connascence

**Summary**: Meilir Page-Jones's 1996 framework for classifying how two components are coupled — if changing one would require changing the other to preserve correctness, they are connascent. The framework separates **static** forms (source-code level, refineable by refactoring) from **dynamic** forms (runtime), and scores each form on **strength**, **locality**, and **degree** to guide where coupling is tolerable and where it should be refactored away.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-03-modularity.md`, `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`, `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19
---

## Definition

> "Two components are connascent if a change in one would require the other to be modified in order to maintain the overall correctness of the system." — Meilir Page-Jones (source: chapter-03-modularity.md)

Page-Jones introduced connascence in *What Every Programmer Should Know About Object-Oriented Design* (Dorset House, 1996), refining the afferent/efferent [[coupling-metrics|coupling metrics]] from Yourdon and Constantine's *Structured Design* and recasting them for object-oriented languages. Where structured programming only asked "is there coupling here?", connascence asks "**what kind** of coupling is it, and how hard is it to change?" (source: chapter-03-modularity.md).

Richards and Ford use connascence as the third leg of the modularity-measurement stool, alongside [[cohesion]] and [[coupling]].

## Static connascence

Static connascence is source-code-level coupling — visible by reading the code, and generally addressable with refactoring tools (source: chapter-03-modularity.md). The five static types, ordered from weakest (easiest to refactor) to strongest:

**Connascence of Name (CoN)** — multiple components must agree on the name of an entity. Method names across a codebase are the canonical example. Modern refactoring tools make this the most desirable form of connascence, because renames are cheap and safe (source: chapter-03-modularity.md).

**Connascence of Type (CoT)** — multiple components must agree on the type of an entity. Statically typed languages express most of this through type declarations; some dynamically typed languages (Clojure with Spec is the example given) offer opt-in typing (source: chapter-03-modularity.md).

**Connascence of Meaning / Convention (CoM / CoC)** — multiple components must agree on the meaning of particular values. The classic case is hard-coded magic numbers rather than named constants. Page-Jones's example: defining `int TRUE = 1; int FALSE = 0`, and the havoc if someone flips them (source: chapter-03-modularity.md). CoM can be refactored down to CoN by extracting a named constant.

**Connascence of Position (CoP)** — multiple components must agree on the order of values. Positional method parameters are the everyday example: `updateSeat("14D", "Ford, N")` type-checks but is semantically wrong if name and seat-location are swapped (source: chapter-03-modularity.md). CoP can be refactored down to CoN by using named parameters or a parameter object.

**Connascence of Algorithm (CoA)** — multiple components must agree on a particular algorithm. The example given is a security hashing algorithm that must run identically on client and server; any divergence in detail breaks the handshake (source: chapter-03-modularity.md). This is the strongest form of static connascence.

## Dynamic connascence

Dynamic connascence is coupling visible only at runtime, where call-graph analysis cannot catch it (source: chapter-03-modularity.md). All four forms are stronger than any static form.

**Connascence of Execution (CoE)** — the order of execution matters. Page-Jones's example:

```
email = new Email();
email.setRecipient("foo@example.com");
email.setSender("me@me.com");
email.send();
email.setSubject("whoops");
```

The subject arrives after the send, which doesn't work. Properties must be set in order (source: chapter-03-modularity.md).

**Connascence of Timing (CoT — dynamic)** — the timing of execution matters. The canonical case is a race condition between threads, where the interleaving affects the result (source: chapter-03-modularity.md). Note that the static CoT (Type) and dynamic CoT (Timing) share the abbreviation in the text.

**Connascence of Values (CoV)** — several values relate to one another and must change together. A rectangle stored as four corner points: you cannot move one point without considering the others. More consequentially in distributed systems: a single logical value updated across multiple databases — all must change together or none should (source: chapter-03-modularity.md). This is where the concept meets [[saga|saga]]-style coordination and distributed-transaction problems.

**Connascence of Identity (CoI)** — multiple components must reference the same entity. Two independent components sharing and updating a distributed queue is the example given (source: chapter-03-modularity.md).

Richards and Ford note that dynamic connascence is harder to analyse than static because we lack tools to instrument runtime calls as thoroughly as static call graphs (source: chapter-03-modularity.md).

## Properties: strength, locality, degree

Connascence is not just a type taxonomy — it comes with three orthogonal properties that tell you how harmful a given instance is.

**Strength** measures how easy the coupling is to refactor. The ordering above (CoN weakest, CoA strongest for static; all dynamic forms stronger still) is the strength ordering. Architects and developers can improve coupling characteristics by refactoring toward weaker forms — e.g., convert CoM (magic number) to CoN (named constant) by extracting a constant. **Prefer static connascence to dynamic**, because static is visible to source analysis and refactoring tools (source: chapter-03-modularity.md).

**Locality** measures how proximal the connascent components are in the code base. Forms of connascence that are unacceptable across module boundaries may be perfectly fine within the same module. Two classes in the same component sharing CoM is tolerable; two separate components sharing CoM is a code smell (source: chapter-03-modularity.md). Strength and locality must be weighed together.

**Degree** measures how many classes/modules are affected. A small amount of dynamic connascence among a handful of modules isn't fatal; the same coupling spread across hundreds of modules is. Codebases tend to grow, so small problems scale into big ones (source: chapter-03-modularity.md).

## Page-Jones's three guidelines

Page-Jones offered three rules for using connascence to improve modularity (source: chapter-03-modularity.md):

1. **Minimize overall connascence** by breaking the system into encapsulated elements
2. **Minimize any remaining connascence that crosses encapsulation boundaries**
3. **Maximize the connascence within encapsulation boundaries**

This is [[information-hiding]] re-stated in connascence vocabulary: push the strong, painful couplings inside module boundaries; expose only weak, refactorable couplings outward.

## Jim Weirich's two rules

Richards and Ford credit Jim Weirich with repopularising connascence and distilling it to two rules of thumb (source: chapter-03-modularity.md):

- **Rule of Degree**: convert strong forms of connascence into weaker forms of connascence.
- **Rule of Locality**: as the distance between software elements increases, use weaker forms of connascence.

In practice: inside a class, CoP and CoM are fine. Between classes in the same module, prefer CoN and CoT. Across [[bounded-context|bounded contexts]] or service boundaries, only the weakest forms should remain — and ideally none of the dynamic ones at all.

## Connascence vs afferent/efferent coupling

Static connascence is a *refinement* of the afferent/efferent coupling metrics from Structured Design. Where those metrics only counted incoming and outgoing connections, connascence tells you **what kind** of connection, and which kinds are better than others. Richards and Ford render this explicit in the book's "Unifying Coupling and Connascence" section: structured programming's "data coupling" (method calls) is refined by static connascence into CoN/CoT/CoM/CoP/CoA, and dynamic connascence covers territory structured programming never addressed — synchronous vs. asynchronous, thread safety, distributed transactions (source: chapter-03-modularity.md). See [[coupling-metrics]] for afferent/efferent and the Martin-derived abstractness/instability metrics.

## Limits of the 1996 framework

Richards and Ford flag two problems for modern architects (source: chapter-03-modularity.md):

1. Connascence operates at code-quality level, not architectural-structure level. An architect often cares *whether* two services communicate synchronously or asynchronously, not the specific code-level shape of the call.
2. The original framework predates microservices. It doesn't address the synchronous-vs-asynchronous distributed-architecture question.

Chapter 7 resolves both limits via the [[architectural-quantum]] construct (see below).

Even so, connascence remains the most precise vocabulary available for naming *why* a particular piece of coupling hurts. It is the refactoring compass: see strong, far-apart, high-degree connascence and the fix is obvious — push it closer, weaken it, or break the dependency.

## Communication connascence (Chapter 7 revision)

Chapter 7 extends the 1996 framework with a new axis that the original couldn't see: **synchronous vs asynchronous communication between distributed components**. This sits alongside the static-vs-dynamic split rather than replacing any of the existing types, and Richards and Ford render it explicit in Figure 7-1 (the updated unified coupling-and-connascence diagram) (source: chapter-07-scope-of-architecture-characteristics.md).

**Synchronous connascence** — two components communicate via a blocking call: the caller waits for the callee to respond. For the duration of the call, the two components are *operationally* connascent — if one is much more scalable than the other, timeouts and reliability failures occur. In effect, synchronous calls collapse the operational architecture characteristics of the participants: they must match for the duration of the call (source: chapter-07-scope-of-architecture-characteristics.md).

**Asynchronous connascence** — fire-and-forget semantics (message queues, event buses). Two components can legitimately differ in operational architecture characteristics because a buffer absorbs the mismatch. Asynchronous connascence creates a more flexible architecture.

The Payment / Auction example in the book: if the Payment service can only handle one payment per 500 ms, synchronous calls from the Auction service cause the second and later calls to time out when many auctions end at once. An asynchronous queue between the two lets each service keep its own operational profile (source: chapter-07-scope-of-architecture-characteristics.md). Event-driven architectures (Chapter 14) lean heavily on this insight.

## Connascence and the architecture quantum

The new synchronous-vs-asynchronous axis is load-bearing for the [[architectural-quantum]] definition: a quantum is an independently deployable artifact with high functional cohesion *and synchronous connascence* (source: chapter-07-scope-of-architecture-characteristics.md). Synchronous connascence is what ties components into a single quantum; asynchronous connascence is what lets them be in different quanta with independent operational characteristics.

Two practical consequences for applied connascence analysis:

- **Inside a quantum**, synchronous calls are expected. The quantum shares operational characteristics by construction, so code-level and call-level connascence are governed by the original 1996 Page-Jones guidelines.
- **Across quanta**, synchronous connascence is the red flag. If service A must synchronously call service B for A to function, the two are part of the same quantum whether the architect intended it or not. The Page-Jones Rule of Locality — weaker connascence at longer distances — upgrades in the quantum era to: *prefer asynchronous connascence across quantum boundaries*.

This also reframes the Jim Weirich rule of thumb. The old formulation was "as the distance between software elements increases, use weaker forms of connascence." At the architectural-quantum scale, the strongest handle on connascence is not *type* but *synchronicity* — asynchronous connascence is the architectural equivalent of weaker.

## Hard Parts: static vs dynamic generalised to the architecture scale

*Software Architecture: The Hard Parts* Chapter 2 lifts Page-Jones's static-vs-dynamic distinction from the code scale to the **architecture scale** and treats it as the central analytical lens for distributed systems (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **[[static-coupling]]** is the architectural counterpart to Page-Jones's static connascence. It asks *how quanta are wired together*: operational dependencies (OS, frameworks, libraries, databases, brokers, URLs), contracts, topology — everything that must be in place for a service to bootstrap. Visible on a deployment diagram.
- **[[dynamic-coupling]]** is the architectural counterpart to Page-Jones's dynamic connascence. It asks *how quanta call one another at runtime*, and it's now a three-dimensional decision space: **communication** (sync/async) × **consistency** (atomic/eventual) × **coordination** (orchestrated/choreographed).

The two frameworks nest rather than compete. The code-level connascence types on this page describe *what kind* of coupling exists between source elements; the architecture-level static/dynamic split describes *which tier of the architecture* the coupling binds at. A cross-service synchronous call is architecturally dynamically coupled *and* contains Page-Jones's dynamic connascence of execution and timing. A shared database schema is architecturally statically coupled *and* contains static connascence of type and meaning across every consumer.

The practical generalisation: Page-Jones's Rule of Locality — *weaker forms of connascence at longer distances* — extends to the architectural scale as *weaker forms of dynamic coupling across quantum boundaries*. Inside a quantum, synchronous calls and shared types are fine. Across quanta, prefer asynchronous communication, eventual consistency, and choreography. Chapter 2's three-dimensional framing makes that preference actionable by naming the specific axes architects can move along.

## Contract strictness as the connascence dial

*Software Architecture: The Hard Parts* Chapter 13 implicitly treats contract strictness as the lever that controls **how much connascence** crosses an integration boundary (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

- A **[[strict-contract|strict contract]]** maximises cross-boundary connascence — name, type, position, and often meaning all must match exactly. The architect buys compile-time verification of all that connascence, but the contract is only as stable as the slowest side can keep up with.
- A **[[loose-contract|loose contract]]** (name-value pairs) reduces cross-boundary connascence to CoN alone — producer and consumer only need to agree on the names of fields they both use. CoT, CoP, and CoM are either erased or deferred to [[consumer-driven-contracts|CDC]] tests.
- **[[stamp-coupling|Stamp coupling]]** is the explicit anti-pattern where a contract imposes structural connascence over *more of the data* than the consumer actually needs, propagating breakage far beyond where the semantic coupling actually requires it.

The Page-Jones rule of locality — *weaker connascence at longer distances* — operationalises at the architectural scale as *looser contracts across quantum boundaries*. Ch 13's loose-contract-plus-CDC recommendation for microservices is the direct application.

## Related pages

- [[coupling]]
- [[cohesion]]
- [[coupling-metrics]]
- [[modularity]]
- [[information-hiding]]
- [[architectural-quantum]]
- [[architecture-characteristics]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
- [[fundamentals-of-software-architecture]]
- [[saga]]
- [[bounded-context]]
- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[stamp-coupling]]
