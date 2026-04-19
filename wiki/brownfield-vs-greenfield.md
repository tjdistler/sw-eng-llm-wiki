# Brownfield vs Greenfield Projects

**Summary**: The two kinds of architecture project the data engineer encounters. **Brownfield** refactors or replaces an existing architecture, constrained by the past. **Greenfield** starts from scratch. Each has characteristic failure modes — for brownfield, big-bang overhauls; for greenfield, shiny-object syndrome.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Brownfield projects

Chapter 3 defines brownfield work as **refactoring and reorganising an existing architecture**, constrained by the choices of the present and past (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

Key attitudes:

- **Empathy and context first**. It is easy to criticise a prior team's work. It is more useful to dig deep, ask questions, and understand why the decisions were made. Empathy goes a long way toward diagnosing the real problem.
- **Design a path forward, not a plan to blame**. Change management is part of architecture, so the work is figuring out how to evolve the system rather than leaping over it.

### Two replacement strategies

**Big-bang overhaul** — rip out the old system all at once and replace it. Chapter 3 explicitly advises against this: "This path often leads to disaster, with many irreversible and costly decisions" (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). It produces irreversible, high-stakes choices where the engineer's job is to produce reversible high-ROI ones.

**[[strangler-fig-pattern|Strangler pattern]]** — new systems slowly and incrementally replace legacy components. Targeted and surgical, one piece at a time. Allows flexible and reversible decisions while assessing each replacement's impact on dependent systems. Chapter 3 cites Martin Fowler's *StranglerFigApplication* (2004) as the source.

### "Legacy is what makes money"

Chapter 3 warns that deprecation is sometimes "ivory tower advice" — impossible in practice at large organisations. Someone somewhere is depending on the legacy system, and "legacy is a condescending way to describe something that makes money" (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

If deprecation is possible, demonstrate value on the new platform first, grow maturity gradually, then follow an exit plan to shut down the old.

## Greenfield projects

A fresh start, unconstrained by prior architecture. Easier than brownfield; often more fun; full of hazards (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

### Characteristic failure modes

Chapter 3 names two:

- **Shiny object syndrome** — feeling compelled to reach for the latest and greatest tech without understanding how it impacts project value
- **Resume-driven development** — stacking impressive new technologies for career reasons rather than project goals (citing Loukides 2004)

The discipline: **always prioritise requirements over building something cool**.

Chapter 4 adds a third closely related failure mode — **[[cargo-cult-engineering]]**: small teams emulating giant-tech architectures without the context or scale that make them valuable (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md). Same root cause as shiny-object syndrome: decoupled from the actual business problem and the team's capabilities.

## Common tenets

Whatever the starting point, Chapter 3 says: focus on the tenets of good data architecture (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- Assess trade-offs
- Make flexible and reversible decisions
- Strive for positive ROI

The same [[principles-of-good-data-architecture|nine principles]] govern both.

## Cross-book framing

- Newman's [[migration-pattern-selection]] and [[monolith-to-microservices]] coverage extends the brownfield-strangler framing for microservice migrations
- [[incremental-migration]] is the underlying discipline that makes strangler replacement possible
- [[parallel-run-pattern]] is a specific tool used during brownfield replacements

## Related pages

- [[strangler-fig-pattern]]
- [[incremental-migration]]
- [[reversible-vs-irreversible-decisions]]
- [[principles-of-good-data-architecture]]
- [[data-architecture]]
- [[migration-pattern-selection]]
- [[cargo-cult-engineering]]
- [[technology-selection]]
