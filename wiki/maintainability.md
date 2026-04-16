---
name: Maintainability
description: Designing systems so engineering and operations teams can work on them productively over time
type: concept
---

# Maintainability

**Summary**: Maintainability is about making life better for the engineers and operators who must work with a system over its lifetime — fixing bugs, adapting to new use cases, and keeping it running.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[accidental-complexity]]
- [[reliability]]
- [[scalability]]
- [[fault-tolerance]]
