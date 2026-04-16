# Pattern: Synchronize Data in Application

**Summary**: A three-step pattern for migrating data from one store to another with no downtime: bulk-copy first, then have the application write to both stores while reading from the old, then flip reads to the new store while still writing to both. Used by Trifork to migrate Danish citizens' medical records from MySQL to Riak.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The setup

You need to move data from an existing database to a new one — perhaps because you're extracting a microservice (see [[change-data-ownership]]), or perhaps because you've outgrown your current technology. You can't take the system offline. You need a fast rollback path. The application itself does the synchronisation. (source: chapter-04-decomposing-the-database.md)

## The three steps

### Step 1: Bulk synchronise data

Take a snapshot of the old database and bulk-import it into the new one while the existing system stays online. Then run a [[change-data-capture]] process to apply any changes that happened during the import, bringing the new database in sync with the old. (source: chapter-04-decomposing-the-database.md)

### Step 2: Synchronise on write, read from old schema

Deploy a new version of the application that writes every change to **both** databases. All reads still come from the old database. This step verifies the new database can handle production write load and that the synchronisation logic is correct, without putting reads at risk. (source: chapter-04-decomposing-the-database.md)

### Step 3: Synchronise on write, read from new schema

Once confidence in the new database is high, switch reads to it. Writes still go to both databases, so if anything goes wrong you can flip reads back. Eventually, retire the old database. (source: chapter-04-decomposing-the-database.md)

## The Danish medical records example

Trifork used this pattern to move Danish citizens' consolidated medical records from MySQL to Riak. The data was uniquely valuable — they couldn't lose it and they couldn't take the system offline for any meaningful period. The phased approach gave them verification at each step and a rollback option throughout. (source: chapter-04-decomposing-the-database.md)

## Application to microservice migration

Newman's framing: this pattern is a strong fit when you want to **split the schema before splitting the application code** (see [[split-the-database-first]]). The monolith keeps two schemas in sync until the new schema is trusted, then the code that owns it can be extracted into a service. (source: chapter-04-decomposing-the-database.md)

It is much harder if both the monolith *and* the new microservice are simultaneously trying to keep the same two schemas in sync — both of them have to do the synchronisation correctly, and a mistake in either creates inconsistency. This is workable if you can guarantee that at any moment only *one* of them is the writer (e.g. a clean [[strangler-fig-pattern]] cutover with no canary). It is risky if requests can land on either implementation. (source: chapter-04-decomposing-the-database.md)

## Where to use it

- When you have a single application doing the writing.
- When you can tolerate the application doing extra writes.
- When you want a fast, safe rollback during the migration.
- Less suited when you're already partway into a microservice extraction and writes can come from multiple services — consider [[tracer-write]] instead.

## Related pages

- [[database-decomposition]]
- [[change-data-ownership]]
- [[tracer-write]]
- [[change-data-capture]]
- [[strangler-fig-pattern]]
- [[split-the-database-first]]
- [[eventual-consistency]]
