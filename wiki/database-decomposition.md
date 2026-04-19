# Database Decomposition

**Summary**: Hub page for the patterns and trade-offs involved in pulling a [[monolith]]'s shared database apart so each microservice owns its data. Newman's central message: "Splitting a database apart is far from a simple endeavor" — but it is almost always worth it, and there is a well-defined catalogue of patterns to do it incrementally. Ford, Richards, and Sadalage add the complementary **five-step pattern** (Hard Parts Ch 6) and the explicit **disintegrator/integrator** framework that decides whether to split in the first place.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## Why split the database

[[microservices|Microservices]] work best when they practise [[information-hiding]], which leads each service toward totally encapsulating its own data storage and retrieval. A shared database undermines this from every angle (source: chapter-04-decomposing-the-database.md):

- **Implementation coupling.** Multiple services bound to the same schema cannot tell what is safe to change. A column rename or table split can break unknown consumers.
- **Lost cohesion of behaviour.** A microservice is a combination of *behaviour* and *state* encapsulating one or more state machines. If three services can all directly change `Order` rows, the state machine is scattered across the codebase. See [[cohesion]] and [[aggregate]].
- **Unclear ownership.** Where does the business logic live? Who owns the integrity invariants?

Newman names only two situations where direct sharing of a database is acceptable for a microservice architecture (source: chapter-04-decomposing-the-database.md):

1. **Read-only static reference data** (country codes, postal codes) — see [[shared-static-data]].
2. **A database that is intentionally exposed as a managed endpoint** — see [[database-as-a-service-interface]].

## Schemas vs databases

Newman uses "database" to mean *a logically isolated schema*. A single database engine can host many schemas; physical and logical separation are independent decisions. See physical-vs-logical database separation (covered in [[split-the-database-first]]). (source: chapter-04-decomposing-the-database.md)

## The pattern catalogue

Newman organises the patterns into four groups.

### 1. Coping with a shared database when you can't (yet) split

For when full decomposition is too expensive or too risky right now, but you want to stop things getting worse:

- [[shared-database-antipattern]] — what's wrong, what's unavoidable
- [[database-view-pattern]] — project a limited, read-only schema for outside consumers
- [[database-wrapping-service]] — wrap the schema behind a thin service to convert DB dependencies into service dependencies
- [[database-as-a-service-interface]] — expose a *separate* read-only DB as a managed endpoint (Martin Fowler's reporting database pattern)

### 2. Transferring ownership

When you extract a service, some data should come with it; other data should stay in the monolith and be exposed properly:

- [[aggregate-exposing-monolith]] — expose a monolith aggregate via API for the new service to call back into
- [[change-data-ownership]] — move data out of the monolith into the new service, and have the monolith call the service

### 3. Synchronisation patterns for the migration window

When the same data needs to live in two places during a [[strangler-fig-pattern]] cutover:

- [[synchronize-data-in-application]] — three-step process used in the Danish medical records migration
- [[tracer-write]] — incrementally move source-of-truth data, tolerating two sources during the migration; Square's Fulfillments example

### 4. Sequencing and refactoring patterns

How and when to split, and the low-level table refactorings:

- [[split-the-database-first]] — schema-first vs code-first vs both-at-once; Newman's preferences
- [[repository-per-bounded-context]] — factor data-access code along context lines first
- [[database-per-bounded-context]] — keep separate schemas inside a [[modular-monolith]] to preserve future options
- [[monolith-as-data-access-layer]] — expose an API on the monolith instead of pulling its data
- [[multischema-storage]] — let the new service hold its own schema *and* still read from the monolith
- [[split-table-pattern]] — separate columns of a shared table along service boundaries
- [[move-foreign-key-to-code]] — replace a DB join with a service call, and decide what to do about referential integrity
- [[shared-static-data]] — four patterns for country-code-style data (duplicate, dedicated schema, library, service)

## Transactions and sagas

Splitting a database means losing the ability to make changes across what used to be a single ACID transaction. Newman is firm: don't reach for [[two-phase-commit]] / [[distributed-transactions]]; reach for sagas instead.

- [[transactions]] / [[acid]] — what you lose when you split
- [[two-phase-commit]] — why Newman says "just say no" for microservices
- [[saga]] — the alternative: model long-lived business processes as sequences of local transactions, with compensating actions for rollback; orchestrated vs choreographed styles

## Hard Parts: should you split at all? (drivers and integrators)

Chapter 6 of *Software Architecture: The Hard Parts* reframes the decision as a **trade-off analysis** between two opposing force groups before any pattern is chosen (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md). Full treatment at [[data-decomposition-drivers-and-integrators]]:

**Six disintegrators push toward splitting:**

1. **Change control** — reduce the blast radius of schema changes across services.
2. **Connection management** — a shared DB cannot supply 1,000+ connections after services fan out.
3. **Scalability** — the DB must scale when services do; a shared DB can't.
4. **Fault tolerance** — remove the single-point-of-failure a shared DB represents.
5. **[[architectural-quantum|Architectural quantum]] boundaries** — a shared DB collapses everything into one quantum with one characteristic profile.
6. **Database type optimisation** — let each data domain move to its best-fit DB type ([[polyglot-persistence]]).

**Two integrators pull toward keeping data together:**

1. **Data relationships** — foreign keys, views, triggers, stored procedures.
2. **Database transactions** — [[acid|ACID]] across multiple tables in one unit of work.

The architect balances the forces, picks the trade-off, and documents the decision — no universal default.

## Hard Parts: the five-step pattern for how to split

Once the decision to split is made, Chapter 6 gives an evolutionary, reversible-at-each-step pattern that operates on the concept of a [[data-domain|data domain]] (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md). A data domain is a cluster of coupled tables, views, FKs, and triggers that belong together in one bounded functional scope — think of the database as a soccer ball where each white hexagon is a data domain.

The five steps:

### Step 1: Analyze the database and create data domains

Group tables by domain affinity. The Sysops Squad gets six: Customer, Survey, Payment, Profile, Knowledge base, Ticketing. Identify cross-domain artifacts (the dotted lines between hexagons) — these are the coupling points that will have to be broken.

### Step 2: Assign tables to data domains

Move tables into per-domain schemas (`ALTER SCHEMA payment TRANSFER sysops.billing`). Where tables genuinely belong in multiple domains, combine the domains or pick one and call the other via the service layer. **Synonyms** are a stepping-stone: create a DB-level alias for cross-schema tables, use it to find and refactor every caller, then remove the synonym once the caller uses a service call.

### Step 3: Separate database connections to data domains

Refactor each service's connection pool to point at exactly one schema. When a service needs data from another domain, **call that domain's service**; do not reach across into the other schema. This is the step that achieves [[data-sovereignty]] — the nirvana state where every service owns its data. It is also the hardest step because all cross-schema access must be resolved at the service layer.

### Step 4: Move schemas to separate database servers

The data now lives in one logical DB but many schemas. Move each schema to its own physical database server. Two options: **backup-and-restore** (simpler, requires downtime) or **replicate-then-cutover** (no downtime, more coordination). See [[split-the-database-first]] for the physical-vs-logical distinction.

### Step 5: Switch over to independent database servers

Once replication is caught up, switch the service connections to the new servers and remove the schemas from the original database. Each data domain is now in its own failure domain, with its own backup schedule, its own upgrade cadence, and the option to change [[database-type-selection|database type]].

## Newman's overall guidance

- Schema decomposition is the **most expensive end** of the [[cost-of-change]] spectrum — Newman flags it as the work that warrants real deliberation, in contrast to the easy reversibility of code changes.
- Prefer to split **incrementally**: pick a pattern that lets you keep operating, learn, and unwind if needed. See [[incremental-migration]].
- If you have to choose between splitting code first and splitting schema first, Newman's hot take: "If I'm able to change the monolith, and if I am concerned about the potential impact to performance or data consistency, I'll look to split the schema apart first. Otherwise, I'll split the code out, and use that to help understand how that impacts data ownership." (source: chapter-04-decomposing-the-database.md)
- The biggest danger of splitting code first is **stopping there** — leaving a shared database forever.

## Related pages

- [[monolith-to-microservices]]
- [[microservices]]
- [[independent-deployability]]
- [[information-hiding]]
- [[strangler-fig-pattern]]
- [[change-data-capture]]
- [[saga]]
- [[two-phase-commit]]
- [[distributed-transactions]]
- [[eventual-consistency]]
- [[data-decomposition-drivers-and-integrators]]
- [[data-domain]]
- [[data-sovereignty]]
- [[database-type-selection]]
- [[polyglot-persistence]]
- [[architectural-quantum]]
- [[software-architecture-the-hard-parts]]
