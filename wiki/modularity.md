# Modularity

**Summary**: The logical grouping of related code — classes into packages, functions into namespaces, modules into components. Richards and Ford treat modularity as an **implicit architecture characteristic**: no requirement ever asks for it, yet sustainable codebases demand it. The three tools for reasoning about modularity are [[cohesion]], [[coupling]], and [[connascence]].

**Sources**: `raw/fundamentals-of-software-architecture/chapter-03-modularity.md`, `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`

**Last updated**: 2026-04-16
---

## Definition

> "95% of the words [about software architecture] are spent extolling the benefits of 'modularity' and that little, if anything, is said about how to achieve it." — Glenford J. Myers (1978), quoted in chapter-03-modularity.md

Modularity is a **logical grouping of related code** — a group of classes in an object-oriented language, functions in a structured or functional language (source: chapter-03-modularity.md). Every major platform offers mechanisms for it: `package` in Java, `namespace` in .NET, modules in Python and Go, and so on.

The word "logical" is load-bearing. Modularity is not about physical separation (separate files, separate deployables); it's about whether related code is *grouped as if* it belonged together, regardless of how it's packaged. A monolithic application with 10,000 classes in one directory can be logically modular if its dependency graph respects boundaries, and a microservices system can be logically entangled if its services leak each other's internals.

## An implicit characteristic

Richards and Ford describe modularity as an **implicit architecture characteristic**: virtually no project ever writes down a requirement saying "make this system modular," but without modularity the system will not be sustainable (source: chapter-03-modularity.md). This makes it the architect's job to preserve — no one else will ask for it.

The physics analogy they offer: software models complex systems, and complex systems tend toward entropy. Energy must be added to preserve order. The architect's ongoing work — [[architecture-vitality|vitality]] checks, enforcing module boundaries, refactoring — is that energy expenditure (source: chapter-03-modularity.md).

## Why architects must pay attention

Most of architecture's analytical tooling — metrics, [[architecture-fitness-function|fitness functions]], dependency visualisations — is built on top of modularity concepts. Without a coherent module structure, none of it works (source: chapter-03-modularity.md). Specific consequences Richards and Ford flag:

- **Reuse** — tightly coupled packages can't be extracted and reused without dragging their neighbours along (source: chapter-03-modularity.md).
- **Restructuring** — a monolith with loose internal partitioning is harder to split apart later, because the loose partitioning encouraged incidental coupling (source: chapter-03-modularity.md).
- **Migration** — moving from one architectural style to another (e.g., monolith to microservices) requires the ability to identify component boundaries; without modularity those boundaries don't exist.

## The short history of "modules"

The chapter traces the vocabulary:

- **Pre-structured-programming era**: GOTO-heavy code, no good grouping mechanism. Dijkstra's 1968 "Go To Statement Considered Harmful" letter pushed the industry toward structured languages like Pascal and C (source: chapter-03-modularity.md).
- **Structured-programming era**: functions, but no way to group them. Developers wanted more.
- **Modular-languages era (short-lived)**: Modula (Wirth's successor to Pascal) and Ada added a `module` construct — essentially today's package, minus classes (source: chapter-03-modularity.md).
- **Object-oriented era**: classes arrived with encapsulation and inheritance. Language designers kept the modular construct alongside classes — as packages, namespaces, etc. — producing today's multi-paradigm scoping rules.

Richards and Ford's aside on Java 1.0 makes the trade-off concrete: Java originally disallowed name conflicts by making the package directory structure match the physical filesystem (filesystems won't allow duplicate names in a directory). Java 1.2 added JAR files, which could re-introduce name conflicts on the classpath — exchanging the original guarantee for convenience (source: chapter-03-modularity.md).

## The three measurement tools

Richards and Ford organise modularity analysis around three concepts (source: chapter-03-modularity.md):

| Concept | What it measures | Origin |
|---|---|---|
| [[cohesion]] | How related the parts *inside* a module are | Constantine's seven-level scale; LCOM metric |
| [[coupling]] | Dependencies *between* modules | Yourdon & Constantine afferent/efferent; Martin's derived metrics — see [[coupling-metrics]] |
| [[connascence]] | What *kind* of coupling it is, and how hard to change | Meilir Page-Jones (1996) |

Each tool captures something the others miss. Cohesion tells you whether a module is a coherent unit. Coupling tells you how exposed the module is to change elsewhere. Connascence refines "exposed" into a taxonomy that guides refactoring.

## From modules to components

Richards and Ford use **module** as a generic term for "bundling of related code" and reserve **[[components|component]]** for the building block an architect actually manipulates — a module realised as a package, service, or deployable unit (source: chapter-03-modularity.md, chapter-08-component-based-thinking.md). Chapter 8 makes the step from logical to physical concrete: a component is the physical manifestation of a module (library, layer, subsystem, service). See [[components]] for the full Chapter 8 treatment, [[technical-vs-domain-partitioning]] for the top-level-partitioning axis, and [[component-identification-cycle]] for the iterative derivation loop. The connection to [[bounded-context|bounded contexts]] and [[domain-driven-design|DDD]] becomes explicit in the domain-partitioning case.

## Relationship to Newman's framing

Newman's *Monolith to Microservices* treats modularity as the engine of [[microservices]]: loose coupling between services, high [[cohesion|cohesion]] of business functionality, and [[information-hiding|hidden internals]] are what make services independently deployable. Richards and Ford's Chapter 3 is the *theoretical* layer underneath that practical framing — it names the code-level structures and metrics that modular systems (monolithic or distributed) must exhibit. Both framings converge on Constantine's law: **a structure is stable if cohesion is high and coupling is low** — see [[coupling]] and [[cohesion]] for Newman's expression of the same idea.

## Related pages

- [[cohesion]]
- [[coupling]]
- [[coupling-metrics]]
- [[connascence]]
- [[information-hiding]]
- [[modular-monolith]]
- [[architecture-characteristics]]
- [[components]]
- [[technical-vs-domain-partitioning]]
- [[fundamentals-of-software-architecture]]
