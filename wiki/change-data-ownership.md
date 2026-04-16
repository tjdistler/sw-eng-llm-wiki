# Pattern: Change Data Ownership

**Summary**: Move data out of the monolith into the newly extracted service that should own it, and reverse the dependency: the monolith now calls the new service to read or change that data, instead of accessing its own tables.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

When a microservice encapsulates the business logic that changes some data, that data should be under the microservice's control. The data is moved from the monolith's database into the new service's schema. The monolith then treats the new service as the source of truth, calling its endpoints to read or modify the data. (source: chapter-04-decomposing-the-database.md)

This is the *complement* of [[aggregate-exposing-monolith]]: that pattern keeps data in the monolith and exposes it; this pattern relocates data and inverts the dependency.

## The hard part

Untangling the data from the monolithic database is non-trivial. You may have to deal with (source: chapter-04-decomposing-the-database.md):

- **Foreign-key constraints** that span what will become a service boundary — see [[move-foreign-key-to-code]].
- **Transactional boundaries** — operations that used to be a single ACID transaction now span two databases. See [[transactions]] and [[saga]].
- **Joins** that now need to happen at the application layer or via service calls.
- **Reporting queries** that touched both sides of the now-split data.

These are the topics that occupy most of Newman's chapter.

## The interim view

If the monolith only needs *read* access to the data after the move, you can — as an interim measure — project the new service's data back into the monolith as a [[database-view-pattern|database view]]. All the limitations of database views apply (read-only, same engine, etc.). Newman prefers changing the monolith to call the new service directly, but the view is acceptable scaffolding during the migration. (source: chapter-04-decomposing-the-database.md)

## Where to use it

Newman is unusually direct: "This one is a little more clear-cut. If your newly extracted service encapsulates the business logic that changes some data, that data should be under the new service's control." (source: chapter-04-decomposing-the-database.md)

The judgement isn't *whether* to move the data; it's *how* to do so without breaking integrity. The synchronisation patterns ([[synchronize-data-in-application]], [[tracer-write]]) and the schema-refactoring patterns ([[split-table-pattern]], [[move-foreign-key-to-code]]) are how you actually carry it out.

## Related pages

- [[database-decomposition]]
- [[aggregate-exposing-monolith]]
- [[aggregate]]
- [[synchronize-data-in-application]]
- [[tracer-write]]
- [[split-table-pattern]]
- [[move-foreign-key-to-code]]
- [[saga]]
