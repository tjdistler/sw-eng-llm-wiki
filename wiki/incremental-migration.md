# Incremental Migration

**Summary**: Newman's strongest methodological recommendation for moving to [[microservices]]: chip away one service at a time rather than attempting a big-bang rewrite. Small steps bound the cost of mistakes, surface real issues quickly, and unlock value before the whole project is done.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## The core argument

> "If you do a big-bang rewrite, the only thing you're guaranteed of is a big bang." — Martin Fowler (source: chapter-02-planning-a-migration.md)

Think of the [[monolith]] as a block of marble. Blowing it up rarely ends well. Chipping away incrementally:

- **Limits the cost of mistakes** — and you *will* make them. A small mistake is easier to recover from than a big one.
- **Provides real feedback** at each step. Doing everything at once makes it hard to attribute which change caused which outcome.
- **Lets you change course.** Each step is a learning opportunity that informs the next.
- **Unlocks value early.** Each extracted service can deliver benefits without waiting for the whole migration to complete.
- **Builds momentum.** Quick wins help sustain organisational support (see [[kotters-change-model]]).

## Production is what counts

A microservice extraction is not done until it is **in production and being actively used** (source: chapter-02-planning-a-migration.md). The most important lessons — about troubleshooting, tracing, latency, referential integrity, cascading failures — only surface in production.

Patterns covered in Chapter 3 ([[parallel-run-pattern]], [[strangler-fig-pattern]], [[feature-toggle|feature toggles]], [[branch-by-abstraction]], [[decorating-collaborator-pattern]], [[change-data-capture]]) let you deploy decomposition work into production while limiting blast radius. The separation of [[deployment-vs-release|deployment from release]] is the underlying enabler — see [[migration-pattern-selection]] for choosing among them.

## Choose one or two services to start

Standard advice: pick one or two areas of functionality, implement them as microservices, deploy them, and reflect. Newman's [[extraction-prioritization|two-axis prioritisation model]] (effort vs benefit) helps choose which.

## Cost of change

The reason for incrementalism is not just risk aversion — it's the steeply non-linear [[cost-of-change|cost-of-change]] across different kinds of decision (source: chapter-02-planning-a-migration.md):

- Moving code around within a codebase is cheap.
- Splitting a database is much more expensive.
- Untangling overly coupled services or rewriting a public API used by multiple consumers is a sizeable undertaking.

Make mistakes where they are cheapest. Do much of your initial thinking on the whiteboard, where the cost of "rolling back" is zero. Sketch service boundaries; trace user journeys (a customer searching, registering, purchasing) and look for circular references or chatty pairs that should probably be one service.

## Reversible vs irreversible decisions

Newman applies Bezos's [[reversible-vs-irreversible-decisions|two-way-door / one-way-door]] framing: most microservice-migration decisions are reversible, but a few (database splits, public API rewrites) are not. Treat reversible decisions as cheap; treat irreversible ones with deliberation. Don't conflate the two.

## Avoid the sunk cost fallacy

Incrementalism's other benefit: it makes it psychologically and organisationally easier to change direction. The bigger the bet, the louder the fanfare, the harder it is to back out — see [[measuring-microservice-transition]] on regular checkpoints to keep yourself honest.

## Don't change behaviour during migration

A subtle reinforcement of incrementalism: while a piece of functionality is being migrated, *don't change its behaviour*. Changes during migration make rollback harder — bug fixes added to the new implementation reappear as bugs after rollback; new features added during migration must be removed on rollback (source: chapter-03-splitting-the-monolith.md). The shorter each migration step, the easier this freeze is to enforce.

## Related pages

- [[microservices]]
- [[monolith]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[extraction-prioritization]]
- [[measuring-microservice-transition]]
- [[kotters-change-model]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[parallel-run-pattern]]
- [[migration-pattern-selection]]
- [[deployment-vs-release]]
