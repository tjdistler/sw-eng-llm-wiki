# Evolutionary Architecture

**Summary**: An architecture designed from the start to support guided, incremental change over time. The core mechanism is the [[architecture-fitness-function]] — an automated objective assessment of an architectural characteristic that runs continuously, so the system can be changed without silently violating its architectural properties.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`

**Last updated**: 2026-04-16

---

## The idea

Neal Ford's *Building Evolutionary Architectures* (O'Reilly) introduces architecture designed to evolve *gracefully*. The premise: architectures always change — the only question is whether the change is guided and tested or ad-hoc and damaging. *Fundamentals of Software Architecture* Chapter 1 doesn't repeat the full book but introduces the vocabulary that infuses the rest of the text (source: chapter-01-introduction.md).

The argument hinges on three observations:

1. **Nothing stays static.** Requirements, technology, team composition, operational substrate — all drift.
2. **Big Design Up Front fails** because of [[unknown-unknowns]]: projects start with a list of known unknowns but are ambushed by things no one knew they'd encounter (source: chapter-01-introduction.md).
3. **Implementation drifts from design** unless something actively checks. See [[architecture-vitality]] and structural decay.

Given those, the architect's task shifts from "design the perfect system" to "design a system that can change and verify that it still works after each change."

## Fitness functions

Borrowed from evolutionary computing — where a fitness function measures how close a genetic algorithm's current solution is to optimal — an **[[architecture-fitness-function|architecture fitness function]]** is an objective integrity assessment of an architectural characteristic (source: chapter-01-introduction.md). Concretely, it might be:

- A unit test that fails if p95 page-load time exceeds 300 ms.
- A chaos-engineering injection that verifies failover completes within SLA.
- A static-analysis rule that fails CI if the presentation layer imports the persistence layer.
- A monitor that alerts if a daily metric crosses a threshold.

The mechanism is not important — the property is: **an objective, automatable check** on a named architectural characteristic that runs often enough to catch regressions before they compound.

## How fitness functions enable evolution

The feedback loop is the key. If page-load time is checked on every commit, a change that regresses it is caught immediately and can be fixed or reverted. If it's checked in a quarterly review, it regresses silently for three months and becomes expensive to untangle. Richards and Ford connect this directly to Agile engineering practices:

> Note the correlation between how often fitness functions execute and the feedback they provide. You'll see that adopting Agile engineering practices such as continuous integration, automated machine provisioning, and similar practices makes building resilient architectures easier. (source: chapter-01-introduction.md)

This is why Chapter 1 insists architecture has become intertwined with engineering practices — a fitness function without CI is a fitness function that doesn't fire often enough to help.

## Connection to the book's two laws

- **[[laws-of-software-architecture|First Law]]** (everything is a trade-off): evolutionary architecture doesn't avoid trade-offs — it makes them *legible* as fitness-function failures when the current design stops supporting the required trade-off.
- **[[laws-of-software-architecture|Second Law]]** (why beats how): fitness functions encode the *why* behind a characteristic as an executable artefact. A future developer who breaks page-load time learns the characteristic matters because a test fails — the why is live, not buried in a Confluence page.

## Relation to other wiki concepts

- [[architecture-vitality]] — vitality is the property; fitness functions are the mechanism for maintaining it.
- [[desired-state-management]] — operationally similar idea: declare the property, let the system enforce it.
- [[synthetic-transactions]] — a kind of fitness function for behavioural characteristics.
- [[end-to-end-testing]] — some fitness functions live at this level; Newman's framing of its costs and the observability-first alternative applies.
- [[unknown-unknowns]] — the fundamental justification for designing for evolution rather than for a fixed target.
- [[strangler-fig-pattern]] and [[feature-toggle]] — Agile restructuring patterns that make it safe to migrate an evolving architecture; Richards and Ford name both as things tight feedback loops enable (source: chapter-01-introduction.md).

## What Chapter 1 defers — and Chapter 6 delivers

The full book *Building Evolutionary Architectures* catalogues fitness-function families (holistic vs atomic, triggered vs continuous, static vs dynamic, etc.) and shows how to retrofit them. *Fundamentals* Chapter 1 only names the concept and promises to flag examples throughout the remaining chapters. Chapter 6 ("Measuring and Governing Architecture Characteristics") is the deep dive: it defines [[architecture-governance]] as a steering practice, introduces the operational/structural/process measurement axes (see [[measuring-architecture-characteristics]]), and catalogues concrete fitness functions — JDepend cyclic-dependency checks, ArchUnit/NetArchTest layer rules, [[cyclomatic-complexity]] ceilings, and Netflix's Simian Army as a holistic runtime fitness function. The full treatment now lives on [[architecture-fitness-function]].

## Related pages

- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[measuring-architecture-characteristics]]
- [[cyclomatic-complexity]]
- [[architecture-vitality]]
- [[architecture-characteristics]]
- [[architect-expectations]]
- [[unknown-unknowns]]
- [[software-architecture-definition]]
- [[laws-of-software-architecture]]
- [[architecture-decisions-vs-design-principles]]
- [[strangler-fig-pattern]]
- [[feature-toggle]]
- [[fundamentals-of-software-architecture]]
