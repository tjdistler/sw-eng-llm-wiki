# Pattern: Monolith as Data Access Layer

**Summary**: Instead of letting a newly extracted service read the monolith's database directly, expose an API on the monolith for the data the new service needs. The monolith becomes a data-access layer for its own data. Susanne Kaiser shared this pattern from JustSocial.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

When a newly extracted service needs data still owned by the monolith, the obvious-but-wrong move is to let it read the monolith's database. Better: add an API to the monolith that exposes the data, and have the new service call that API. (source: chapter-04-decomposing-the-database.md)

This is structurally identical to [[aggregate-exposing-monolith]] — Newman uses different framings to highlight different angles. The "data access layer" framing emphasises the *role the monolith plays* (it's now a server in front of its own data) rather than the *aggregate ownership* perspective.

## Why it's under-used

Newman: "Part of the reason this isn't used more widely is likely because people sort of have in their minds the idea that the monolith is dead, and of no use. They want to move away from it. They don't consider making it more useful!" (source: chapter-04-decomposing-the-database.md)

The monolith doesn't have to be the enemy. Treating it as a usable building block — at least temporarily — avoids the trap of forcing premature data extraction.

## What you get

- **No data decomposition required yet.** The hard problem is deferred while you still benefit from a new, smaller service.
- **[[information-hiding]] preserved.** The new service is isolated from the monolith's schema.
- **A path to the next service.** If the API turns out to be cleanly scoped, the next obvious step is to extract that data and the API into a service of its own — the API has done the boundary-discovery work for you.

## Where to use it

Newman: "I'd be more inclined to adopt this model if I felt that the data in the monolith was going to stay there." (source: chapter-04-decomposing-the-database.md)

If the data really *belongs* with the new service (the new service owns the relevant state machine), don't use this pattern — use [[change-data-ownership]] and pull the data out. This pattern is for the case where the monolith continues to be the legitimate owner.

It's especially good when the new microservice is largely stateless and just needs to read information from the monolith.

## Related pages

- [[database-decomposition]]
- [[aggregate-exposing-monolith]]
- [[change-data-ownership]]
- [[multischema-storage]]
- [[information-hiding]]
- [[strangler-fig-pattern]]
- [[split-the-database-first]]
