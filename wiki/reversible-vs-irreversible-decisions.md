# Reversible vs Irreversible Decisions

**Summary**: Jeff Bezos's two-way-door / one-way-door distinction, adopted by Newman as a tool for thinking about microservice-migration decisions. Treat reversible decisions cheaply; reserve deliberation for irreversible ones; don't confuse the two.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

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

## Related pages

- [[incremental-migration]]
- [[cost-of-change]]
- [[microservices]]
