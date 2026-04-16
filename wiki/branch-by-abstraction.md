# Branch by Abstraction

**Summary**: An in-place migration pattern for replacing functionality that lives deep inside the [[monolith]] without long-lived source-code branches. Wrap the existing implementation in an abstraction, build a new implementation alongside it, switch the abstraction over, then clean up. Best alternative when [[strangler-fig-pattern]] cannot intercept at the perimeter.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## The problem it solves

The [[strangler-fig-pattern]] depends on intercepting calls at the system's perimeter. But what if the functionality you want to extract is **deep inside** the monolith and triggered by many internal callers? The classic example is a Notifications module called from dozens of places throughout the codebase (source: chapter-03-splitting-the-monolith.md).

The traditional answer — pull the change into a long-lived branch — is precisely what continuous integration tells us not to do. The 2017 State of DevOps Report shows that trunk-based development with short-lived branches correlates with higher-performing IT teams (source: chapter-03-splitting-the-monolith.md). Branch by abstraction lets you migrate inside trunk.

## Five steps

1. **Create an abstraction** that represents the functionality to be replaced. If existing code is well-factored, an IDE Extract Interface refactoring may be enough; otherwise extract a [[seams-and-legacy-code|seam]] in the Michael Feathers sense.
2. **Switch existing clients** to use the abstraction. No functional change yet — small, incremental refactors.
3. **Create a new implementation** of the abstraction. In a microservice migration, this implementation calls out to the new service. The new service can be deployed to production immediately, even when the implementation returns "Not Implemented" — exercising deployment without affecting users.
4. **Switch the abstraction** to use the new implementation, ideally via a [[feature-toggle]] for fast rollback.
5. **Clean up**: remove the old implementation, remove the toggle (don't leave dead toggles around), and optionally remove the abstraction itself.

(source: chapter-03-splitting-the-monolith.md)

## Long phase 3 is fine

Step 3 — building out the new implementation while the old one still serves — can take a long time without blocking anything. Jez Humble's example: GoCD's persistence layer was migrated from iBatis to Hibernate using branch by abstraction over several months while the application continued shipping to clients twice a week (source: chapter-03-splitting-the-monolith.md).

## Verify branch by abstraction (Steve Smith)

A variant that adds automatic fallback: if a call to the new implementation fails, the old implementation is invoked as a backup. This complicates reasoning about system behaviour and, if both implementations are stateful, requires shared state for consistency. Conceptually adjacent to a [[parallel-run-pattern]] and shares the same data-consistency challenge (source: chapter-03-splitting-the-monolith.md).

## When to use it

Newman's preference order:

1. **Strangler fig first** — simpler, doesn't require touching the monolith.
2. **Branch by abstraction** when extraction must happen inside the monolith because there's no clean perimeter call to intercept.
3. Other patterns (e.g. [[change-data-capture]], [[decorating-collaborator-pattern]]) when you cannot change the monolith's source at all.

The pattern assumes you *can* change the monolith. If you cannot, this pattern is unavailable (source: chapter-03-splitting-the-monolith.md).

## Related pages

- [[strangler-fig-pattern]]
- [[parallel-run-pattern]]
- [[feature-toggle]]
- [[seams-and-legacy-code]]
- [[decorating-collaborator-pattern]]
- [[change-data-capture]]
- [[migration-pattern-selection]]
- [[incremental-migration]]
