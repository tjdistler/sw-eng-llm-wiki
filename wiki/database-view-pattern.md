# Pattern: Database View

**Summary**: Project a limited, read-only schema from an underlying database so consumers see a stable subset while the owning team is free to change internals. A coping pattern when the [[shared-database-antipattern|shared database]] cannot be split right now.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

In a situation where you want a single source of data for multiple services, a view can mitigate the [[coupling]] concerns. With a view, a service is presented with a schema that is a *limited projection* from an underlying schema. The projection can hide tables and columns the consumer shouldn't see. (source: chapter-04-decomposing-the-database.md)

The view becomes a form of [[information-hiding]]: you control what is shared and what is hidden, even though the data still lives in one physical schema.

## Use case: the database as a public contract

In Newman's credit-derivative-system anecdote (see [[shared-database-antipattern]]), more than 20 external applications had read access to the schema. The team's solution was to create a dedicated schema hosting *views that looked like the old schema*, and have clients point at that view-schema. This let them refactor the underlying schema for write throughput while preserving the consumer-facing shape. "Lots of stored procedures were involved." (source: chapter-04-decomposing-the-database.md)

A simpler example: the new `Loyalty` service needs only customer ID and loyalty-card ID. A view exposes those two columns from the `Customer` table; everything else stays hidden. (source: chapter-04-decomposing-the-database.md)

## Materialized views

Some databases support **materialized views** — the view is precomputed and cached. Reads avoid hitting the underlying schema, improving performance at the cost of staleness. (source: chapter-04-decomposing-the-database.md)

## Limitations

Newman calls out several (source: chapter-04-decomposing-the-database.md):

- **Read-only.** Views are typically the result of a query, so writes are not supported. This bounds their usefulness sharply.
- **Same database engine.** The view-hosting schema must run on the same engine as the source. This increases physical deployment coupling and creates a potential single point of failure.
- **Engine support varies.** Common in relational DBs and mature NoSQL (Cassandra, Mongo), but not universal.
- **Schema-shape coupling.** A view can only project shapes the underlying tables can produce. For richer transformations, see [[database-wrapping-service]] or [[database-as-a-service-interface]].

## Ownership

Changes to the underlying source schema may require updating the view. Newman: "I suggest considering any published database views to be akin to any other service interface, and therefore something that should be kept up-to-date by the team looking after the source schema." (source: chapter-04-decomposing-the-database.md)

## Where to use it

Use a database view when decomposing the existing monolithic schema is impractical, but you need to mitigate the worst of the coupling. Ideally, push toward proper [[change-data-ownership|schema decomposition]] instead — the limitations of views are significant. But views are a real step in the right direction. (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[shared-database-antipattern]]
- [[database-wrapping-service]]
- [[database-as-a-service-interface]]
- [[information-hiding]]
- [[coupling]]
- [[aggregate-exposing-monolith]]
