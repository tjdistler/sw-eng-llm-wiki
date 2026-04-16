# Why Microservices?

**Summary**: Microservices are not a goal — they are a means to specific outcomes that an existing architecture can't deliver. Newman's three-question test and the catalogue of legitimate motivations (autonomy, time to market, scale, robustness, more developers, new technology) for adopting them.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## Microservices are not the goal

You don't "win" by having microservices (source: chapter-02-planning-a-migration.md). The decision to adopt them should be conscious, rational, and driven by something you can't currently achieve with your existing architecture. Without a clear goal, you will:

- Suffer analysis paralysis when faced with the many decisions a [[microservices]] architecture forces.
- Drift into cargo-cult thinking ("If microservices are good for Netflix, they're good for us!").
- Be unable to measure progress or compute return on investment.

Newman has met teams who, a year into a microservices transition, can no longer remember why they started.

## The three questions

When working with an organisation considering microservices, Newman asks the same three questions (source: chapter-02-planning-a-migration.md):

1. **What are you hoping to achieve?** Outcomes aligned with what the business wants, expressible as benefits to end users.
2. **Have you considered alternatives?** Many of the same benefits can be obtained more cheaply by other means. (Each motivation below has a "How else could you do this?" answer.)
3. **How will you know if the transition is working?** Defined measures, both quantitative and qualitative. See [[measuring-microservice-transition]].

## Legitimate motivations

Each of these is a reason to consider microservices, but every one has a cheaper alternative worth trying first.

### Improve team autonomy

Smaller, self-directing units (Gore's 150-person business units, Amazon's two-pizza teams, Timpson's two-rule retail empowerment) outperform centrally controlled ones (source: chapter-02-planning-a-migration.md). Teams that own their microservices end-to-end gain the most autonomy.

*Cheaper alternatives*: assign codebase modules to teams within a [[modular-monolith]]; designate per-area decision-makers; introduce self-service infrastructure to remove central operations bottlenecks. See [[team-autonomy]].

### Reduce time to market

Independently deployable services let teams ship without waiting for coordinated releases (source: chapter-02-planning-a-migration.md). See [[independent-deployability]].

*Cheaper alternative*: do a path-to-production modelling exercise first. Newman's colleague Kief Morris discovered at one investment bank that 40 weeks of the 46-week delivery cycle happened *before* developers ever started work — automating the 6-week dev pipeline would have changed almost nothing.

### Scale cost-effectively for load

Scale only the parts of the system under load; turn the rest off when idle. SaaS companies adopt microservices partly for this control over operational cost (source: chapter-02-planning-a-migration.md).

*Cheaper alternatives*: vertical scaling (a bigger box); horizontal scaling of the existing monolith behind a load balancer; replacing a bottleneck technology. See [[scaling-approaches]].

### Improve robustness

Decomposing into independent processes opens up new mechanisms for keeping critical functionality available when other parts fail (source: chapter-02-planning-a-migration.md). But microservices do not give robustness for free — they only open the design space. Spreading functionality across processes can equally *increase* the failure surface.

Newman cites David Woods and John Allspaw on the [[robustness-vs-resilience|distinction between robustness and resilience]]: robustness is reacting to expected variations; resilience is adapting to the unforeseen.

*Cheaper alternative*: run multiple monolith copies behind a load balancer or queue, distributed across failure planes (different racks, different data centres).

### Scale the number of developers

Per Brooks's *Mythical Man-Month*, adding people only helps when work can be partitioned with limited interaction. Microservices with clear boundaries and minimal coupling create those partitionable units (source: chapter-02-planning-a-migration.md). Just having microservices isn't enough — team alignment to service ownership matters too.

*Cheaper alternative*: a [[modular-monolith]] where each team owns a module — but coordination is still required at deployment time.

### Embrace new technology

A microservice boundary is a safe place to try a new language, runtime, or database. The blast radius of a bad bet is contained (source: chapter-02-planning-a-migration.md). Mature microservice organisations rarely standardise on a single stack; they don't sprawl either.

*Cheaper alternative*: same-runtime polyglot (e.g., multiple JVM languages). Database technology change is harder — that's an argument that pushes towards decomposition.

## Reuse is not a goal

Reuse is one of the most common stated motivations and, in Newman's view, a bad one (source: chapter-02-planning-a-migration.md). Reuse is not a direct outcome — it's a hoped-for path to faster delivery or lower cost. But chasing reuse can slow you down: coordinating with another team that owns the existing PDF generator may be slower than writing your own. Track the actual outcome you want; don't optimise the proxy.

## Multiple goals: trade-offs

In practice, organisations want several things at once: scaling *and* autonomy *and* a new programming language. Without a clear ranking, the change initiative balloons and microservices become locked in even when (e.g.) horizontal scaling of the existing monolith would have solved the original problem (source: chapter-02-planning-a-migration.md).

Newman recommends a slider exercise: each desired outcome starts in the middle; making one more important forces another down. The relative priorities can and should change over time, but at any moment the team should know which goal wins when they conflict.

## Related pages

- [[microservices]]
- [[when-microservices-are-a-bad-idea]]
- [[independent-deployability]]
- [[team-autonomy]]
- [[robustness-vs-resilience]]
- [[scaling-approaches]]
- [[measuring-microservice-transition]]
