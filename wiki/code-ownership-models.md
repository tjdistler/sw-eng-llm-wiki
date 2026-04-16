# Code Ownership Models

**Summary**: Martin Fowler's three models — strong, weak, and collective — applied by Newman to microservice ownership. The model that works at small scale (collective) breaks down at large scale; strong ownership is "almost universally" what 100+ developer organisations adopt.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The three models

Newman adopts Martin Fowler's generic code-ownership taxonomy and applies it to microservice ownership — specifically ownership from the *making code changes* point of view, not deployment, on-call, or first-line support (source: chapter-05-growing-pains.md).

### Strong code ownership

Every service has owners. Anyone outside the ownership group who wants to make a change must submit it to the owners, who decide whether to accept it (source: chapter-05-growing-pains.md). Pull requests across team boundaries are the canonical implementation.

### Weak code ownership

Most or all services are owned by someone, but anyone can directly change anyone's modules without resorting to pull requests (source: chapter-05-growing-pains.md). Source control allows the change; the social expectation is that you talk to the owner first.

### Collective code ownership

No one owns anything. Anyone can change anything (source: chapter-05-growing-pains.md).

## When each works

Newman's experience-based guidance (source: chapter-05-growing-pains.md):

- **Up to ~20 colocated developers**: collective ownership works. The group is small enough to maintain a shared understanding of "what a good change looks like" and the technical direction of each service.
- **Fast growth or distributed teams**: collective ownership breaks. Consensus needs time and space to emerge, and rapid hiring or geographic spread destroys both.
- **100+ developers, multiple teams**: strong ownership "almost universally" wins. Each team can adopt collective ownership *locally* — within the team — while strong ownership governs cross-team boundaries.

## The fintech "colander architecture" anecdote

Newman tells of a fintech company that scaled from 30–40 developers to over 100 with no assigned ownership. The result was no shared technical vision and a horribly tangled "distributed monolith". One developer called it "colander architecture" because people would just "punch a new hole" — exposing data or making point-to-point calls — whenever they felt like it (source: chapter-05-growing-pains.md).

The painful kicker: this kind of mess is much harder to untangle in a distributed system than in a monolith. The cost of detangling a distributed monolith is high.

## Why strong ownership scales

Two reinforcing reasons (source: chapter-05-growing-pains.md):

1. **Local consensus is cheaper than global consensus.** Within a team, "what makes a good change" can be decided quickly. Across 100+ developers, it cannot.
2. **It enables product-oriented teams.** If a team owns services aligned with the business domain, that team becomes focused on that area of the domain. This supports embedded product owners and customer-focused work — which is itself one of the [[why-microservices|legitimate reasons to adopt microservices]].

## Connection to other Chapter 5 problems

Ownership model interacts with several other Chapter 5 pain points:

- **[[local-developer-experience]]**: collective ownership requires running many services locally because developers move across them; strong ownership lets developers stub out everything outside their few services.
- **[[orphaned-services]]**: collective-ownership organisations may be more resilient because they already have tooling and conventions that let any developer touch any service.
- **[[global-vs-local-optimization]]**: strong ownership amplifies local optimisation; without cross-cutting forums, you get duplicated work. Collective ownership requires central consistency, which is expensive at scale.

## Related pages

- [[independent-deployability]]
- [[team-autonomy]]
- [[reorganizing-teams]]
- [[conways-law]]
- [[orphaned-services]]
- [[local-developer-experience]]
- [[global-vs-local-optimization]]
