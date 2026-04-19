# Data Decomposition Drivers and Integrators

**Summary**: Ford, Richards, and Sadalage's trade-off framework for deciding *whether* to break a monolithic database apart. Six **disintegrators** push toward splitting; two **integrators** pull toward keeping data together. The architect's job is to balance them and document the decision — not to apply a universal rule.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The framing

Chapter 6 of *Software Architecture: The Hard Parts* opens with the sharpest line in the book about data: *"Breaking apart a database is hard — much harder, in fact, than breaking apart application functionality."* Data is the most important asset in the company, highly coupled to application behaviour, and its seams are less visible than code seams (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

So the decomposition decision needs a structured trade-off analysis, not a default. The authors name two opposing force groups:

- **Data disintegrators** — drivers that justify breaking data apart.
- **Data integrators** — drivers that justify keeping data together.

The [[trade-off-analysis]] is the balance. Neither side wins by default; the architect surfaces the forces on each side, weighs them against the specific system, and documents the decision in an [[architecture-decision-record|ADR]].

## The six disintegrators

The forces that push toward separating data (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

### 1. Change control

How many services are impacted when a table's schema changes? A rename, drop, or type change is a **breaking change** that cascades into every service using that table. In a shared database with 400 services, a single column rename requires coordinating the redeploy of every service that uses the column — and the real danger is that a service gets **forgotten** and fails silently in production until noticed.

Breaking apart the database into [[bounded-context|bounded-context]]-aligned schemas isolates the change. And the [[bounded-context]] provides a second abstraction: the service's external **contract** (JSON, etc.) can survive schema changes that would otherwise leak to every consumer. A `WishList.EXPIRATION_DT` column dropped from the DB doesn't have to ripple into the `exp_dt` JSON field other services consume — the service can backfill, default, or rename internally.

### 2. Connection management

Database connections are a finite, expensive resource. A monolith with a 200-connection pool becomes, after decomposition into 50 services with 10 connections each, a **1,000-connection** system — and once services scale to 5 instances each, **1,700 connections**. No shared database supports that without connection-wait starvation, cascading timeouts, and tripped [[circuit-breaker|circuit breakers]].

The book's mitigation for a still-shared database is the **connection quota**: each service gets an explicit cap, tuned by [[architecture-fitness-function|fitness functions]] that stream usage data. Quotas can be distributed evenly first (simple, wasteful) and later made variable per-service (efficient, requires data). This can buy time — but if the shape of the workload genuinely exceeds what a single connection pool can serve, splitting the database is the structural fix.

### 3. Scalability

A distributed system scales only if every part scales — including the database. When services multiply instances, they multiply database connections, query load, and capacity demand simultaneously. Splitting into data domains or a per-service database reduces the per-DB pressure linearly and lets each resulting database be sized and scaled independently.

### 4. Fault tolerance

A shared database is a **single point of failure**. If it goes down, *every* service depending on it becomes nonoperational. Fault tolerance of the whole system is bounded above by the availability of its shared DB.

Splitting the database turns a system-wide outage into a bounded-context outage. Only the services pointing at the failed schema stop working; the rest continue. See [[fault-tolerance]].

### 5. Architectural quantum boundaries

From *Hard Parts* Chapter 2: an [[architectural-quantum]] is an independently deployable artifact with high functional cohesion, high [[static-coupling]], and synchronous [[dynamic-coupling]]. **A shared database collapses everything touching it into one quantum** — regardless of how many services front it (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

If architectural characteristics (scalability, availability, security, elasticity) must differ across parts of the system, the data must be split. A monolithic database forces a monolithic quantum, and a monolithic quantum forces one set of characteristics for the whole system.

### 6. Database type optimisation

Not all data wants to live in the same kind of database. A relational monolith might be a poor fit for reference-data key-value pairs (country codes, product codes), for graph-shaped data (friend-of-a-friend), or for time-series event streams. Splitting allows moving each category of data to its **best-fit database type** — [[polyglot-persistence]]. See [[database-type-selection]] for the eight families the book surveys.

## The two integrators

The forces that push toward keeping data together (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

### 1. Data relationships

Foreign keys, triggers, views, stored procedures, and materialised views tie tables together. When those tables live in one database, the integrity artifacts are cheap and enforceable. When the tables move into separate schemas or servers, the FKs must be dropped, the views rewritten, and the triggers moved into the service layer. The relationships don't disappear — they become application code.

Telling a DBA "we need to remove every foreign key and view in the database" is the moment this integrator becomes concrete. Not every data relationship survives the trip to the application layer; some will require [[saga]]-style compensating logic, and others (cross-domain reporting) will need a separate analytics path.

### 2. Database transactions

When one service writes to multiple tables in the same schema, the writes can be wrapped in a single [[acid|ACID]] transaction — atomic commit or atomic rollback. Once the tables live in separate databases, that transactional envelope vanishes. A write can commit in one DB and fail in another, leaving data inconsistent.

The book addresses this in Chapter 12 with [[saga|sagas]] and orchestrated compensations, but the integrator stands: if *"a single transactional unit of work is necessary to ensure data integrity and consistency"*, splitting the data costs you that, and the cost must be paid explicitly elsewhere (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

## Other integrators that commonly appear

The book names two explicitly and mentions a third pair in passing:

- **Data consistency for reporting** — cross-domain queries for BI/reporting become federated or ETL-based once the data is split.
- **Schema simplicity** — one schema is easier to comprehend than many.

In practice, these reduce to variants of the two main integrators (data relationships and transactions).

## Balancing the trade-off

Every integrator/disintegrator pair is a trade-off to resolve against the specific system:

- Is change control (disintegrator) more important than foreign-key relationships (integrator)?
- Is fault tolerance (disintegrator) more important than materialised views (integrator)?
- Does quantum-level scalability (disintegrator) outweigh cross-domain ACID (integrator)?

The analysis is the point. The book's framing: don't default to "split" or "don't split" — enumerate the forces on both sides, rank them for this system, and document the decision.

## Where this sits in the decomposition workflow

These drivers tell the architect *whether* to decompose. Once the decision is made, the **five-step pattern** in [[database-decomposition]] tells the team *how* — group tables into [[data-domain|data domains]], split connections, move schemas, separate servers.

## Related pages

- [[database-decomposition]]
- [[data-domain]]
- [[database-type-selection]]
- [[bounded-context]]
- [[architectural-quantum]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[acid]]
- [[saga]]
- [[fault-tolerance]]
- [[polyglot-persistence]]
- [[trade-off-analysis]]
- [[architecture-decision-record]]
- [[software-architecture-the-hard-parts]]
