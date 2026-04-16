# Modular Monolith

**Summary**: A [[monolith]] internally structured into well-bounded modules with stable interfaces, often owned by different teams. Newman repeatedly cites it as the cheaper alternative to a [[microservices]] architecture for several specific goals.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## What it is

A modular monolith is a single deployable application whose internals are decomposed into modules with explicit boundaries and stable inter-module interfaces (source: chapter-02-planning-a-migration.md). Different teams can own different modules; as long as a module's interface remains stable, its internals can change in isolation.

This is the structure encouraged by classic [[information-hiding|information hiding]] (Parnas, 1971) and [[domain-driven-design|domain-driven design]] applied without process boundaries.

## Where Newman recommends it

Throughout Chapter 2, Newman invokes the modular monolith as the "How else could you do this?" answer for several common microservice goals (source: chapter-02-planning-a-migration.md):

- **Improving team autonomy.** Codebase ownership of modules can give teams a meaningful slice of independence without the cost of distributed systems.
- **Scaling the number of developers.** Different teams own different modules; as long as interfaces stay stable, parallel work proceeds with limited contention.
- **Acting as a stepping stone.** When the SnapCI team's microservice boundaries turned out to be wrong, they merged everything back into a monolith, learned the domain, then re-decomposed. Modular monolith was the safe interim shape.

## Where it stops short

The modular monolith is genuinely limited compared to microservices on certain axes (source: chapter-02-planning-a-migration.md):

- **Deployment is still coordinated.** Even if Team A only changes its own module, the *act of deployment* still requires coordination with everyone else's code in the same artifact.
- **Technology homogeneity is largely forced.** All modules typically share the runtime, language, and database.
- **Independent scaling is hard.** Scaling one module up requires scaling the whole process up.
- **Failure isolation is weak.** A bug or memory leak in one module can take down the whole process.

These limits are exactly the conditions under which Newman says microservices are worth their cost — and conversely, when none of them bind, the modular monolith is the right architecture.

## Relationship to microservices

A well-built modular monolith is the *easiest* starting point for an eventual microservice extraction. The modules already represent meaningful boundaries; the work of [[extraction-prioritization|deciding what to extract]] becomes a question of *which module first*, not *what are the boundaries even*.

Newman's overall position: don't reach for microservices unless you have a clear reason. For many of the stated reasons, a modular monolith gets you most of the way for a fraction of the cost.

## Related pages

- [[monolith]]
- [[microservices]]
- [[information-hiding]]
- [[bounded-context]]
- [[independent-deployability]]
- [[team-autonomy]]
- [[why-microservices]]
