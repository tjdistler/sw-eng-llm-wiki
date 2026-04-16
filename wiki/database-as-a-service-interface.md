# Pattern: Database-as-a-Service Interface

**Summary**: Expose a dedicated, read-only database as a managed endpoint — *separately* from the database the service uses internally — for consumers that genuinely need to query data with database-shaped tools (Tableau, BI, ad-hoc SQL). A generalisation of Martin Fowler's reporting database pattern.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The pattern

Sometimes clients really do need a database to query — for large data exports, ad-hoc analysis, or because their tool chain expects a SQL endpoint. In those cases, expose *a separate database* as a documented, read-only interface. A mapping engine populates this external database from the service's internal database when data changes. (source: chapter-04-decomposing-the-database.md)

The same service can simultaneously expose a synchronous API, an event stream, *and* a database — each is just a different kind of endpoint. (source: chapter-04-decomposing-the-database.md)

## Why it's not the same as the shared database anti-pattern

The crucial distinction from the [[shared-database-antipattern|shared database]] anti-pattern: the database that is exposed is **not** the database the service uses internally. The internal schema remains hidden and free to change. The external schema is a deliberately designed contract maintained by the service team. (source: chapter-04-decomposing-the-database.md)

## Reporting Database

Martin Fowler documented this earlier as the **reporting database pattern**. Newman uses a different name because reporting is just one application — the broader idea is supporting clients who need ad-hoc queries against your service's data. (source: chapter-04-decomposing-the-database.md)

## The mapping engine

The mapping engine takes changes from the internal database and writes them to the external one. It can ignore some changes, expose others directly, or transform them. When the internal schema changes, the mapping engine changes; the public-facing database stays consistent for consumers. (source: chapter-04-decomposing-the-database.md)

In virtually all cases the external database lags the internal one. Consumers must understand they are seeing potentially stale data. Newman suggests programmatically exposing the last-update timestamp so consumers can reason about staleness. (source: chapter-04-decomposing-the-database.md)

### Implementation choices

| Approach | Notes |
|---|---|
| [[change-data-capture]] (e.g. Debezium) | Most robust, most up-to-date. Newman's preferred choice. |
| Batch copy | Simple but lags badly; fragile when "changed since" is hard to compute. |
| Service emits events; mapper consumes | Works well if you already have an event-driven architecture. |

(source: chapter-04-decomposing-the-database.md)

Newman: "I've been bitten too many times by batch processes not running or taking too long to run. With the world moving away from batch jobs, and wanting data faster, batch is giving way to real time." (source: chapter-04-decomposing-the-database.md)

## Compared to database views

This pattern is more sophisticated than [[database-view-pattern]] (source: chapter-04-decomposing-the-database.md):

- Views constrain you to the same database engine as the source. The exposed database here can use a totally different stack (Cassandra internally, SQL externally).
- Views are read-only projections of existing tables; this pattern gives full freedom to shape the public schema.
- The cost is more work and more moving parts. If a view will do, start with that.

## Where to use it

Read-only consumers who need database-shaped access — reporting, BI, ad-hoc analytics. Often a precursor to importing the data into a wider data warehouse where data from multiple services can be joined. (source: chapter-04-decomposing-the-database.md)

Don't underestimate the work required to keep the external database properly up to date. (source: chapter-04-decomposing-the-database.md)

## As a Chapter 5 pain remedy

Chapter 5 returns to this pattern as the answer to a specific growing pain: existing analytics stakeholders losing direct SQL access when the monolith database is split (source: chapter-05-growing-pains.md). Same mechanism, different motivation — you discover this pattern reactively when analytics users complain, rather than proactively while planning the database decomposition. See [[cross-service-analytics]].

## Related pages

- [[database-decomposition]]
- [[shared-database-antipattern]]
- [[database-view-pattern]]
- [[database-wrapping-service]]
- [[change-data-capture]]
- [[data-warehousing]]
- [[information-hiding]]
- [[cross-service-analytics]]
