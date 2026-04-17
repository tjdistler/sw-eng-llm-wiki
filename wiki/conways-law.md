# Conway's Law

**Summary**: Melvin Conway's 1968 observation that the structure of a system mirrors the communication structure of the organization that built it. For microservices, the implication is twofold: the three-tier architecture exists because organizations were structured around technical specialties, and aligning teams around business domains is a precondition for microservices to work.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`

**Last updated**: 2026-04-16 (Richards & Ford Inverse Conway Maneuver citation added)

---

## The law

> "Any organization that designs a system…will inevitably produce a design whose structure is a copy of the organization's communication structure." — Melvin Conway, *How Do Committees Invent?*

Conway's paper was presented at the same 1968 National Symposium on Modular Programming where Larry Constantine first articulated [[coupling]] and [[cohesion]] — an auspicious year for software architecture (source: chapter-01-just-enough-microservices.md).

## Why three-tier architectures are everywhere

Newman uses Conway's law to explain why the three-tier architecture (UI / business logic / database, each owned by a different team) is so common. In traditional IT organizations, people were grouped by core competency:

- DBAs in one team, with other DBAs.
- Java developers in another team.
- Frontend developers in a third.

Group people by competency, and you produce IT assets aligned to those competencies. The architecture isn't bad — it's optimized around how teams were traditionally organized (source: chapter-01-just-enough-microservices.md).

## What changed

The forces shifted. We now want to ship software much more quickly, and we group people in poly-skilled teams to reduce hand-offs and silos. That drives different choices about how to break systems apart. If business functionality is what changes, but the architecture spreads each business change across three tiers, you get [[cohesion|low cohesion of business functionality]] — the opposite of what you want.

Microservices invert this. Each service is a thin end-to-end slice of business functionality, which lets a poly-skilled product team own a service end to end (source: chapter-01-just-enough-microservices.md).

## Service ownership and the IT/business divide

In traditional organizations, software development is handled by a part of the business separate from the part defining requirements and meeting customers. The dysfunctions are familiar (source: chapter-01-just-enough-microservices.md).

True technology organizations are merging these silos: product owners now sit inside delivery teams, which align around customer-facing product lines rather than arbitrary technical groupings. Any centralized IT function exists to support these customer-focused delivery teams.

Microservice architectures make this organizational shift much easier:

- Services aligned around the business domain → ownership maps cleanly to product-oriented delivery teams.
- Reducing services shared across multiple teams reduces *delivery contention*.
- Business-domain-oriented microservice architectures make this organizational shift practically possible (source: chapter-01-just-enough-microservices.md).

The relationship runs both ways: the architecture follows the org structure (Conway), but choosing a domain-aligned architecture also pressures the org structure to follow.

## The Inverse Conway Maneuver

Jonny Leroy of ThoughtWorks coined the **Inverse Conway Maneuver**: deliberately evolve the team and organisational structure *toward* the architecture you want, rather than accepting whatever architecture falls out of the existing org (source: chapter-08-component-based-thinking.md). Richards and Ford name this explicitly in their Chapter 8 treatment of [[technical-vs-domain-partitioning|technical vs domain partitioning]]: domain partitioning makes the Inverse Conway Maneuver easy because domain components map cleanly onto cross-functional product teams.

The maneuver is the counter-move to Conway's pull. Conway's law is descriptive (the architecture *will* mirror the org); the Inverse Conway Maneuver is prescriptive (change the org to shape the architecture). It only works deliberately — most organisations drift into Conway-compliant technical partitioning without anyone choosing it.

See [[reorganizing-teams]] for the Newman-side treatment of the same shift, and [[technical-vs-domain-partitioning]] for the component-design payoff.

## The reverse pressure: reorganising teams

Chapter 2 develops the second direction in more detail. If you adopt microservices, the organisation usually has to change to match — moving from competency silos (Java team, DBA team, ops team) toward end-to-end product teams (source: chapter-02-planning-a-migration.md). Newman warns explicitly against copying other companies' structures (the misunderstood "Spotify model" being the most common cautionary tale). Instead, map your current state, decide where you want to go, and shift incrementally.

See [[reorganizing-teams]] for the full treatment, [[skills-self-assessment]] for the tactical approach to bridging skill gaps, and [[team-autonomy]] for autonomy as a microservices motivation.

## Related pages

- [[microservices]]
- [[bounded-context]]
- [[cohesion]]
- [[coupling]]
- [[monolith]]
- [[independent-deployability]]
- [[reorganizing-teams]]
- [[team-autonomy]]
- [[skills-self-assessment]]
- [[technical-vs-domain-partitioning]]
- [[components]]
- [[fundamentals-of-software-architecture]]
