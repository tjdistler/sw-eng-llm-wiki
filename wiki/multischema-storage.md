# Pattern: Multischema Storage

**Summary**: A microservice can store its *new* data in its own schema while still reading the monolith's database for legacy data it hasn't yet pulled out. Avoids the worst of both worlds — you don't extend the monolithic schema, but you don't have to migrate everything before adding new functionality.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

If new functionality requires storing data that the monolith doesn't already manage, *don't* put that data in the monolith's database. Put it in the microservice's own schema, even if the service still reads other (older) data from the monolith. (source: chapter-04-decomposing-the-database.md)

Newman's example: an `Invoice` service. Invoice core data still lives in the monolith and is read from there. New "review" functionality requires a `reviewer → invoice ID` mapping table. That table goes in the new service's schema, not the monolith's. (source: chapter-04-decomposing-the-database.md)

## Why it matters

The principle: **don't make a bad situation worse**. Just because you currently access some data in the monolith's database doesn't mean every related new data point should also live there. Otherwise the monolith's schema keeps growing, making the eventual extraction harder. (source: chapter-04-decomposing-the-database.md)

It also gives you an incremental migration path: as you pull data out of the monolith table by table, it can move into the schema you've already started building.

## Foreign keys across schemas

If your new data has a foreign-key-like reference to data still in the monolith, you can't enforce that with a database constraint. See [[move-foreign-key-to-code]] for what to do.

## Where to use it

- Adding new functionality to a microservice that needs to store new data.
- During the gradual migration of data out of the monolith — your microservice can hold partial schemas as you migrate table by table. (source: chapter-04-decomposing-the-database.md)

If the data you're accessing in the monolith is data you never plan to move out, combine this pattern with [[monolith-as-data-access-layer]] — call the monolith's API instead of reading its DB. (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[monolith-as-data-access-layer]]
- [[change-data-ownership]]
- [[move-foreign-key-to-code]]
- [[split-the-database-first]]
