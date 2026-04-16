# Team Autonomy

**Summary**: One of the strongest motivations for microservice adoption: giving small teams end-to-end ownership of their services so they can make decisions and ship without waiting for others. Newman cautions that microservices are not the only path to autonomy.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## Why autonomy

Autonomous teams empower people, help them grow, and get the job done faster (source: chapter-02-planning-a-migration.md). Newman cites three concrete examples:

- **Gore** caps every business unit at 150 people so everyone knows each other.
- **Timpsons** (UK retailer): chairman John Timpson scrapped internal rules and replaced them with two — "Look the part and put the money in the till" and "You can do anything else to best serve customers". Local stores decide their own refunds.
- **Amazon's two-pizza team model** and (the often-misunderstood) **Spotify model** — both attempts to push responsibility into small, self-directed groups.

When a team owns a microservice end-to-end — code, deployment, operations, on-call — its autonomy inside the larger organisation grows.

## Microservices are not the only way

Newman is careful to point out that distributing responsibility doesn't strictly require an architectural change (source: chapter-02-planning-a-migration.md):

- **Modular monolith with codebase ownership.** Different teams own different modules. As long as inter-module interfaces stay stable, each team can work in isolation.
- **Functional decision-making.** Designate a person empowered for an area ("Ryan owns display ads; Jane owns query performance"). Route decisions in those areas to them.
- **Self-service infrastructure.** A surprising amount of perceived bureaucracy is just waiting for a central operations team to provision machines or environments. Self-service tooling removes that wait without changing architecture at all.

## Microservices amplify autonomy when other conditions are met

Microservices help most when team autonomy is *limited by deployment coupling*. If your bottleneck is "we can't ship without coordinating with three other teams", aligning service ownership to teams (one team, one or more services, no shared services) cleanly removes that block. See [[independent-deployability]] and [[conways-law]].

If the bottleneck is something else — slow procurement, blocked decisions at the executive level, a 40-week pre-development phase — microservices won't fix it. Newman's [[why-microservices|three-question test]] catches this.

## The flip side: global vs local optimisation

Chapter 5 surfaces autonomy's downside (source: chapter-05-growing-pains.md): when teams own decisions, they tend to optimise locally. Three teams independently picking three different databases — each defensible — composes into an organisation paying for skills, licences, and operations on three database technologies. Without ways to surface local decisions in their global context, you can't even ask whether one would suffice.

The remedy isn't to take autonomy away; it's to build forums (cross-cutting technical groups, free-form proposals) where teams can discuss decisions that may benefit from a global view. See [[global-vs-local-optimization]].

## Connection to organisational change

Pushing autonomy into delivery teams usually means [[reorganizing-teams|reorganising]] away from technical-competency silos (Java team, DBA team, ops team) toward end-to-end product teams. This is itself a major organisational change — see [[kotters-change-model]] and [[reorganizing-teams]] for how to approach it.

## Related pages

- [[why-microservices]]
- [[microservices]]
- [[independent-deployability]]
- [[conways-law]]
- [[reorganizing-teams]]
- [[modular-monolith]]
- [[code-ownership-models]]
- [[global-vs-local-optimization]]
