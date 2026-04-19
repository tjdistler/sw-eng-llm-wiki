# Maintainability

**Summary**: Maintainability is about making life better for the engineers and operators who must work with a system over its lifetime — fixing bugs, adapting to new use cases, and keeping it running. Ford and Richards frame it more narrowly as the ease of adding, changing, or removing features; it is one of the three components of [[agility]] and one of the five drivers of [[architectural-modularity]].

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`, `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`

**Last updated**: 2026-04-19

---

## Why maintainability matters

The majority of software cost is not in initial development — it is in ongoing maintenance: fixing bugs, adapting to new platforms, investigating failures, repaying technical debt, and adding features. Systems designed without maintainability in mind tend to become "legacy systems" that developers dread touching. (source: chapter-01)

## Three design principles

### Operability — making life easy for operations

Good operability means routine tasks are easy, freeing operations teams to focus on high-value work. A good operations team handles:

- Monitoring system health and restoring service quickly
- Tracking down root causes of failures or degraded performance
- Keeping software and platforms up to date (including security patches)
- Anticipating future problems (capacity planning)
- Maintaining security as configuration changes

Data systems support operability by:

- Providing good visibility into runtime behavior via monitoring
- Supporting automation and integration with standard tooling
- Avoiding dependency on individual machines (enabling rolling maintenance)
- Providing clear documentation and predictable operational behavior
- Offering self-healing behavior while also allowing manual override

### Simplicity — managing complexity

As systems grow, complexity accumulates. Symptoms include: explosion of state space, tight coupling, tangled dependencies, inconsistent naming, performance hacks, and special-cases. This complexity slows everyone down and increases the risk of bugs when making changes.

**Accidental complexity** is complexity not inherent in the problem being solved, but arising from implementation choices. This is the kind that can and should be removed. See [[accidental-complexity]].

The primary tool for removing accidental complexity is **abstraction** — hiding implementation detail behind a clean, simple interface. Good abstractions improve both reuse and quality: improvements to an abstracted component benefit all systems that use it. Examples: high-level programming languages abstracting over machine code; SQL abstracting over on-disk data structures and concurrency. (source: chapter-01)

### Evolvability — making change easy

System requirements change constantly: new facts emerge, use cases shift, business priorities change, platforms evolve, regulations change, scale forces architectural rethinking.

Evolvability (also called extensibility, modifiability, or plasticity) is the ease with which a system can be modified for unanticipated future needs. It is closely linked to simplicity: simple, well-abstracted systems are easier to change than complex ones.

Agile practices (TDD, refactoring) address evolvability at the code level. At the data system level, evolvability requires different thinking — how do you evolve a system consisting of multiple services and applications with different characteristics?

## Relationship to other properties

Reliability and scalability are prerequisites for maintainability — a system that constantly fails or slows under load is harder to maintain. But maintainability is also a precondition for sustained reliability and scalability: a system that can't be safely modified can't be adapted as requirements grow.

## The Hard Parts framing: scope of change

Chapter 3 of *Software Architecture: The Hard Parts* defines maintainability specifically as (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> the ease of adding, changing, or removing features, as well as applying internal changes such as maintenance patches, framework upgrades, third-party upgrades, and so on.

The chapter's central mechanical argument is about **scope of change**. The same feature (add an expiration date to a wishlist item) produces different scopes in different architectures:

- **Monolithic layered architecture** — change touches UI, backend, and database *layers*, typically coordinated across three teams. Scope of change is the **application** (Figure 3-4).
- **[[service-based-architecture|Service-based architecture]]** — change is contained within one domain service. Scope of change is one **domain** (Figure 3-5).
- **[[microservices]]** — change is contained within one small service. Scope of change is one **function** (Figure 3-6).

Maintainability tracks scope of change inversely: the smaller the scope, the higher the maintainability. [[architectural-modularity|Architectural modularity]] is therefore the primary structural lever for maintainability.

## The von Zitzewitz incoming-coupling metric

Chapter 3 cites a maintainability metric from software architect Alexander von Zitzewitz (founder of hello2morrow) that, stripped of its mathematics, captures one load-bearing idea (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> the higher the incoming coupling level between components, the lower the overall maintainability level of the codebase.

The practical metrics this points to — for reasoning about a codebase's maintainability without the full ML formula — are the usual suspects:

- **Component coupling** — the degree and manner to which components know about one another (see [[coupling]]).
- **Component cohesion** — the degree and manner to which the operations of a component interrelate (see [[cohesion]]).
- **[[cyclomatic-complexity]]** — level of indirection and nesting within a component.
- **Component size** — lines/statements per component.
- **[[technical-vs-domain-partitioning|Technical vs domain partitioning]]** — whether components are aligned by technical layer or business purpose.

Large monolithic architectures generally fail on most of these: heavy incoming coupling (the component graph is dense), technical partitioning (not domain-aligned), and weak cohesion from a domain perspective. Modular architectures — even modular monoliths — invert the pattern.

## Relation to Kleppmann's framing

Kleppmann's three design principles (operability, simplicity, evolvability) are the data-systems-oriented framing of the same concern. The Ford-Richards framing is narrower and more structural: maintainability is specifically about *scope of change per feature request*, and the architect's tool for reducing scope is decomposition into smaller deployment units. The two framings are compatible — low incoming coupling and small components are exactly what produces Kleppmann's simplicity, and simplicity is what enables evolvability.

## Related pages

- [[accidental-complexity]]
- [[reliability]]
- [[scalability]]
- [[fault-tolerance]]
- [[agility]]
- [[testability]]
- [[deployability]]
- [[architectural-modularity]]
- [[coupling]]
- [[cohesion]]
- [[cyclomatic-complexity]]
- [[technical-vs-domain-partitioning]]
