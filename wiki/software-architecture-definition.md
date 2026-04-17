# Software Architecture (Definition)

**Summary**: Richards and Ford's four-part working definition: software architecture is the **structure** of a system combined with the **architecture characteristics** it must support, the **architecture decisions** that constrain how it is built, and the **design principles** that guide implementation choices.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`

**Last updated**: 2026-04-16

---

## Why define it at all

The industry has historically refused to pin software architecture down. Martin Fowler's "Who Needs an Architect?" famously falls back on Ralph Johnson's quip *"architecture is about the important stuff…whatever that is"* (source: chapter-01-introduction.md). Richards and Ford argue that vagueness leaves the role incoherent, so they offer a working definition built from four dimensions you can actually analyse.

They caution that any definition is context-bound and will age: the Wikipedia definition's line that "architecture is about making fundamental structural choices which are costly to change once implemented" is already outdated because [[microservices]] are designed so that structural change is cheap (source: chapter-01-introduction.md). All architectures are a product of their context.

## The four dimensions

### 1. Structure

The type of architectural style (or styles) the system is implemented in — microservices, layered, microkernel, event-driven, and so on. Describing a system as "a microservices architecture" specifies the structure but does not specify the architecture — the other three dimensions are still unspecified (source: chapter-01-introduction.md).

### 2. [[architecture-characteristics]]

The "-ilities" the system must support: availability, reliability, scalability, performance, security, elasticity, and so on. These define the success criteria of the system and are generally orthogonal to its functionality — you could read the list of required characteristics without knowing what the system does, yet they constrain nearly every structural choice (source: chapter-01-introduction.md).

### 3. [[architecture-decisions-vs-design-principles|Architecture decisions]]

Hard-and-fast rules about how the system should be constructed — for example, "only the business and services layers may access the database; the presentation layer must not" (source: chapter-01-introduction.md). Decisions form the **constraints** of the system. An exception to a decision is handled through a formal **variance** process, typically reviewed by an architecture review board (ARB) or chief architect.

### 4. [[architecture-decisions-vs-design-principles|Design principles]]

Guidelines rather than rules — for example, "prefer asynchronous messaging between microservices for performance" (source: chapter-01-introduction.md). Principles cover situations where a rigid rule would be wrong in some cases; they guide developers toward the preferred approach while leaving room for the specific-case judgement.

## Why all four

Dropping any dimension makes the definition incomplete:

- Structure alone doesn't explain why the style was chosen or what it has to optimise for.
- Characteristics alone don't tell you how they're delivered.
- Decisions without principles over-specify; principles without decisions under-specify.

The [[laws-of-software-architecture|Second Law]] — "why is more important than how" — is the through-line: characteristics explain *why* the structure looks the way it does; decisions and principles explain *why* specific implementation choices are allowed or encouraged.

## Relationship to earlier wiki material

The book's definition is a superset of what [[monolith-to-microservices|Newman]] and [[designing-distributed-systems|Burns]] work with implicitly. Newman frames architecture in terms of [[coupling]], [[cohesion]], [[information-hiding]], and [[independent-deployability]] — effectively design principles and characteristics as named concepts. Burns frames architecture in terms of reusable patterns (sidecar, ambassador, scatter/gather, work queue) — effectively structural vocabulary at one level of granularity. Richards and Ford's contribution is to name the meta-framework into which all four pieces plug.

## Related pages

- [[architecture-characteristics]]
- [[architecture-decisions-vs-design-principles]]
- [[laws-of-software-architecture]]
- [[architect-expectations]]
- [[architect-role-intersections]]
- [[evolutionary-architecture]]
- [[fundamentals-of-software-architecture]]
