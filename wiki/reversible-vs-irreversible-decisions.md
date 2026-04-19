# Reversible vs Irreversible Decisions

**Summary**: Jeff Bezos's two-way-door / one-way-door distinction, adopted by Newman as a tool for thinking about microservice-migration decisions. Treat reversible decisions cheaply; reserve deliberation for irreversible ones; don't confuse the two.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The distinction

From Bezos's 2015 letter to Amazon shareholders (source: chapter-02-planning-a-migration.md):

> "Some decisions are consequential and irreversible or nearly irreversible — one-way doors — and these decisions must be made methodically, carefully, slowly, with great deliberation and consultation… But most decisions aren't like that — they are changeable, reversible — they're two-way doors. If you've made a suboptimal Type 2 decision, you don't have to live with the consequences for that long."

Bezos calls these Type 1 and Type 2. Newman, following Martin Fowler, prefers the more descriptive **Irreversible** and **Reversible**.

## A spectrum, not two buckets

Newman doesn't see decisions as falling cleanly into either bucket — it's a spectrum. Where a decision sits depends on the cost of changing your mind later. The bigger that cost, the more it looks irreversible (source: chapter-02-planning-a-migration.md).

On a microservice migration, examples roughly along the spectrum:

- **Reversible**: refactoring code within a service; rolling back a deployment; choosing a CI tool.
- **In between**: extracting a single service from the monolith; introducing an event broker.
- **Irreversible**: splitting a database; rewriting a public API used by many consumers; choosing a vendor lock-in.

Software has a friendly property: most things can be rolled back. The cost of rollback is what shifts a decision toward "irreversible".

## Why this matters for microservices

A microservices architecture brings *more* decisions than a monolith — about boundaries, communication, data ownership, deployment topology, and so on. Newman warns of a specific anti-pattern: organisations that don't decide often start treating every Type 2 decision like a Type 1, and progress grinds to a halt (source: chapter-02-planning-a-migration.md).

Most microservice-migration decisions sit toward the reversible end. So:

- **Reversible decisions**: delegate to people closest to the problem. If they get it wrong, fix it later.
- **Irreversible decisions**: invest the time. Get more eyes on it. Don't rush.

The mistake to avoid is the *inverse* — applying heavyweight deliberation to reversible decisions (slowing the team down) while treating irreversible ones casually (incurring real long-term cost).

## Connection to incremental migration

The framing reinforces the case for [[incremental-migration]]. Smaller steps mean more decisions land on the reversible end of the spectrum, because the impact of any single step is smaller. It also makes irreversible decisions visible *as* irreversible, so you can apply appropriate care.

## In data architecture

Reis and Housley lift the same Bezos framing into the data world and make it **Principle 7** of their [[principles-of-good-data-architecture|nine principles of good data architecture]]. Chapter 3 frames it with a different emphasis (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- The **data landscape changes rapidly** — today's hot technology is tomorrow's afterthought
- Reversible decisions are therefore the *default posture* for data architects, not just the occasional one
- Chapter 3 quotes Martin Fowler directly: "one of an architect's most important tasks is to remove architecture by finding ways to eliminate irreversibility in software designs"

Chapter 3 also ties reversibility to Grady Booch's cost-of-change framing: "architecture represents the significant design decisions that shape a system, where significant is measured by cost of change" (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). A reversible decision is one whose cost of change stays low.

The principle also depends on [[loose-coupling|Principle 6 (loose coupling)]] — you can only swap a component without breaking everything if the coupling was loose to begin with.

## In technology selection (Chapter 4)

Chapter 4 of *Fundamentals of Data Engineering* turns the principle into concrete [[technology-selection|selection guidance]] (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **"Bear traps."** Inflexible technologies are "easy to get into and extremely painful to escape." The [[total-opportunity-cost-of-ownership|TOCO]] of a choice is the cost of the bear trap.
- **Two-year re-evaluation rule.** Evaluate tools every two years — build on [[immutable-vs-transitory-technologies|immutable foundations]], swap transitory tools around them.
- **Escape plans.** Every technology, even OSS, has some degree of lock-in. Prepare the escape plan even if you never use it — it makes today's decisions better and gives you an out if things go wrong.

## Related pages

- [[principles-of-good-data-architecture]]
- [[loose-coupling]]
- [[data-architecture]]
- [[incremental-migration]]
- [[cost-of-change]]
- [[microservices]]
- [[technology-selection]]
- [[immutable-vs-transitory-technologies]]
- [[total-opportunity-cost-of-ownership]]
