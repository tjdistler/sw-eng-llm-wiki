# Pattern: Repository per Bounded Context

**Summary**: Break a single shared data-access layer (typically Hibernate or similar ORM) into multiple repositories, one per [[bounded-context]], so it becomes obvious which parts of the schema each context touches. A preparatory refactoring before splitting either code or schema.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

Most monoliths have a single repository or DAO layer that maps every entity to and from the database. Refactor that layer into separate repository modules, one per bounded context. With ORMs like Hibernate, this is often as concrete as one mapping file per context. (source: chapter-04-decomposing-the-database.md)

This makes visible which tables each context reads and writes — information you otherwise have to reverse-engineer when planning a split.

## Why it helps

Two practical pay-offs (source: chapter-04-decomposing-the-database.md):

1. **You can see the shape of the data dependency.** "The finance code uses the `ledger` table; the catalog code uses the `line_item` table" is now explicit in the codebase, not buried in queries.
2. **The next decomposition step is mechanical.** When you decide to split a schema or extract a service, the repository module gives you a list of tables to take with you.

It does not, however, show you database-level constraints — particularly **foreign keys** that span what will become a service boundary. Newman recommends a separate tool like the freely available **SchemaSpy** to render the FK graph visually. (source: chapter-04-decomposing-the-database.md)

## Where to use it

Any time you're reworking a monolith and considering future extractions. It's cheap, reversible, and improves your understanding of the system regardless of whether you ever extract a service. (source: chapter-04-decomposing-the-database.md)

It pairs naturally with [[database-per-bounded-context]] — once your code is divided along context lines, dividing the schema along the same lines is the obvious next step.

## Related pages

- [[database-decomposition]]
- [[bounded-context]]
- [[database-per-bounded-context]]
- [[split-the-database-first]]
- [[seams-and-legacy-code]]
- [[modular-monolith]]
