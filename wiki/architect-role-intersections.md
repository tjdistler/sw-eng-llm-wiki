# Architect Role Intersections

**Summary**: A decade ago, software architects dealt almost entirely with purely technical concerns — modularity, components, patterns. Since then the role has expanded to intersect with engineering practices, operations/DevOps, software-development process, and data. Richards and Ford argue these intersections are now inseparable from architecture itself.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`

**Last updated**: 2026-04-16

---

## Why the role expanded

Late-20th-century architecture optimised for expensive, shared, commercially-licensed infrastructure (OS, app-server, database licences). That context made designs like [[microservices]] economically absurd — imagine pitching 50 Windows licences, 30 application-server licences, and 50 database licences in a 2002 data centre (source: chapter-01-introduction.md).

Two things changed that:

1. **Open-source software** collapsed the per-instance licence cost.
2. **The DevOps revolution** collapsed the human cost of managing many instances.

With those constraints gone, architectures that offload concerns to operations (like [[microservices]]) became viable — but only if architects understood and designed around the operational substrate. The role expanded because its dependencies did.

## The four intersections

### Engineering practices

Engineering practices — testing, continuous integration, automation, declarative configuration — are **process-agnostic** techniques with repeatable benefit. They emerged from Extreme Programming in the 1990s, matured into *Continuous Delivery*, and now inform architecture directly (source: chapter-01-introduction.md).

The architect often *is* the technical leader on a project and sets engineering practices accordingly. The chapter's sharpest framing:

> Just as architects must carefully consider the problem domain before choosing an architecture, they must also ensure that the architectural style and engineering practices form a symbiotic mesh. (source: chapter-01-introduction.md)

A microservices design on top of manual provisioning and no automated testing cannot succeed — not because microservices are wrong but because the engineering substrate they assume isn't there.

This intersection is the birthplace of [[evolutionary-architecture]] and [[architecture-fitness-function|architecture fitness functions]], which are about engineering practices supporting architectural governance.

### Operations / DevOps

Historically, operations was often outsourced as a cost-saving measure, and architects defensively built operational concerns *into* the architecture — elasticity, scaling, failover handled by application code. The side effect was vastly more complex architecture (source: chapter-01-introduction.md).

Microservices — built during the DevOps era — inverted this. Operations handles elasticity, scaling, and failover; the architecture is simpler because it *relies* on operations rather than working around their absence. The architect's job is now to design that liaison: what does ops own, what does the architecture own, what is the contract between them?

> Realizing a misappropriation of resources led to [[accidental-complexity|accidental complexity]], and architects and operations teamed up to create microservices. (source: chapter-01-introduction.md)

### Process

Software development process (how meetings happen, how teams are formed, how work flows) is "mostly orthogonal" to architecture — but only mostly. Iterative processes like Agile let architects assume short feedback loops and therefore be more aggressive about experimentation (source: chapter-01-introduction.md). Migration patterns like [[strangler-fig-pattern]] and [[feature-toggle]] are cited in Chapter 1 specifically because Agile's tight feedback loop makes them practical.

Trying to run a modern architecture on a Waterfall process creates friction from the process side, not the architecture side.

### Data

Code and data have a symbiotic relationship: one isn't useful without the other. Many books on architecture treat data lightly; Richards and Ford flag it as a first-class concern (source: chapter-01-introduction.md). Database administrators often work alongside architects on relationships, reuse, and portfolio effects. This comes to a head later in the book at [[architectural-quantum]]-level discussions (deferred to Chapter 7).

The DDIA, Monolith-to-Microservices, and Designing Distributed Systems coverage already in the wiki — [[database-decomposition]], [[replication]], [[partitioning]], [[transactions]], [[cap-theorem]], [[encoding-formats]] — is the deep substrate for this intersection.

## Pets.com and why we have elastic scale

Chapter 1's illustrative history: Pets.com built a celebrated sock-puppet mascot and an under-provisioned website. When orders arrived the site was slow, transactions were lost, deliveries delayed; the business closed shortly after (source: chapter-01-introduction.md). The need for **elastic scale** — ability to spin up more instances on demand — was born from failures like this. It's a commodity cloud feature now; in 2000 it was a novel engineering problem. The lesson Richards and Ford draw: architectural capabilities we take for granted were born from earlier hard lessons.

## The through-line

Each intersection expands what an architect needs to think about, and each one is a source of [[laws-of-software-architecture|trade-offs]] (First Law). Failing to consider operations, engineering practices, process, or data at design time produces [[accidental-complexity]] — the architect builds defences against problems that the intersecting discipline could have absorbed cheaply if it had been in the conversation.

## Related pages

- [[architect-expectations]]
- [[software-architecture-definition]]
- [[laws-of-software-architecture]]
- [[evolutionary-architecture]]
- [[architecture-fitness-function]]
- [[accidental-complexity]]
- [[microservices]]
- [[database-decomposition]]
- [[strangler-fig-pattern]]
- [[feature-toggle]]
- [[fundamentals-of-software-architecture]]
