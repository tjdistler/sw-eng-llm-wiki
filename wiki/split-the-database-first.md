# Split the Database First, or the Code?

**Summary**: Newman's discussion of the order-of-operations question for a microservice extraction. Three options — schema first, code first, or both at once — each with different risks. Newman's hot take: schema first if you're worried about performance or consistency; code first otherwise; never both at once.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The three sequencing options

A microservice extraction isn't done until both the application code and the data live in their own places. There are three ways to sequence that work (source: chapter-04-decomposing-the-database.md):

1. **Split the database first**, then the code.
2. **Split the code first**, then the database.
3. **Split both at once.**

Newman recommends *against* option 3 — it's too big a step to assess before commit. Choose between options 1 and 2.

## Physical vs logical separation

A digression Newman insists on first: when he talks about splitting databases, he primarily means **logical** separation — different schemas. A single database engine can host many schemas, giving you logical isolation without separate hardware. (source: chapter-04-decomposing-the-database.md)

The two kinds of separation serve different goals (source: chapter-04-decomposing-the-database.md):

- **Logical decomposition** enables independent change and [[information-hiding]].
- **Physical decomposition** improves robustness (no single point of failure) and removes resource contention.

Logically decomposing while sharing a database engine leaves a single point of failure, but many engines have HA mechanisms (multi-primary, warm failover) and separate clusters cost real money (and license fees). And to *have the option* of separate physical engines, you have to logically decompose first.

## Split the database first

Pull the schema apart while keeping the application code monolithic (source: chapter-04-decomposing-the-database.md).

**Pros:**
- Surfaces the hard problems early — broken transactional boundaries, slower queries from cross-schema joins.
- You can revert easily because no consumers see the schema split.
- Once the schema works split, the code split is downstream.

**Cons:**
- Little short-term benefit; you still have a monolithic deployable.
- Doesn't work if the monolith is a black box (commercial software, can't change it).

Use this when you suspect performance or data-consistency problems will be the dominant risk.

### Patterns that fit this approach

- [[repository-per-bounded-context]] — factor your data-access code along context lines first, so you can see what each context touches.
- [[database-per-bounded-context]] — keep separate schemas inside the monolith. Newman recommends this for *new* systems where you don't yet know whether you'll go to microservices.
- [[synchronize-data-in-application]] — three-step pattern for moving data with rollback safety.
- [[split-table-pattern]], [[move-foreign-key-to-code]] — the low-level schema refactorings.

## Split the code first

Most teams do this. Pull a service out, leave its data in the shared schema temporarily, then come back and split the data later. (source: chapter-04-decomposing-the-database.md)

**Pros:**
- Independently deployable artifact early — real microservice payoff.
- Easier to see what data the new service needs once it's separate.

**Cons:**
- The trap: teams stop after the code split, leaving a shared database forever. Newman has seen this many times.
- You may delay finding nasty surprises caused by joins moving up into the application layer.

JustSocial is a real example of doing this well — they followed through and split the data. (source: chapter-04-decomposing-the-database.md)

### Patterns that fit this approach

- [[monolith-as-data-access-layer]] — instead of letting the new service read the monolith's DB, expose an API on the monolith. (Newman: surprisingly under-used.)
- [[multischema-storage]] — the new service has its own schema for *new* data, while still reading old data from the monolith.

## Newman's recommendation

> "If I'm able to change the monolith, and if I am concerned about the potential impact to performance or data consistency, I'll look to split the schema apart first. Otherwise, I'll split the code out, and use that to help understand how that impacts data ownership." (source: chapter-04-decomposing-the-database.md)

The "and don't both-at-once" rule is the only hard rule. The rest depends on your context.

## A note on tooling

Database refactoring lacks the tooling that code refactoring has. Newman urges using a tool like FlywayDB that captures each schema change as a version-controlled delta script. (source: chapter-04-decomposing-the-database.md)

Visualising existing relationships is also worthwhile — SchemaSpy can render the foreign-key graph and help you spot constraints that span what will become a service boundary. (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[repository-per-bounded-context]]
- [[database-per-bounded-context]]
- [[monolith-as-data-access-layer]]
- [[multischema-storage]]
- [[synchronize-data-in-application]]
- [[modular-monolith]]
- [[incremental-migration]]
- [[cost-of-change]]
