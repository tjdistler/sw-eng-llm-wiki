# Monolith to Microservices

**Summary**: A practical, evolutionary guide to migrating from monolithic systems to microservice architectures by Sam Newman. Where *Building Microservices* defines the destination, this book is about the journey — patterns, decompositional moves, and the organizational and database changes that make the transition tractable.

**Sources**: `raw/monolith-to-microservices/`

**Last updated**: 2026-04-16

---

## About the book

Sam Newman is the author of *Building Microservices* (O'Reilly), which became the canonical introduction to microservice architectures. *Monolith to Microservices* is the sequel-of-sorts that addresses the question most teams actually face: not "should we build a microservice architecture greenfield?" but "we have a monolith — what now?"

The book emphasizes:

- **Microservices are a means, not an end.** They buy you options, but at a cost. Monoliths are a valid architectural choice.
- **Incremental migration** over big-bang rewrites. Pull out one service at a time, learn, repeat.
- **Database decomposition is the hard part.** A whole chapter is dedicated to moving away from monolithic databases.
- **[[independent-deployability]]** is the central discipline that makes microservices worth the cost.

## Ingestion status

| Chapter | Title | Status |
|---|---|---|
| 1 | Just Enough Microservices | Ingested 2026-04-16 |
| 2 | Planning a Migration | Ingested 2026-04-16 |
| 3 | Splitting the Monolith | Ingested 2026-04-16 |
| 4 | Decomposing the Database | Ingested 2026-04-16 |
| 5 | Growing Pains | Ingested 2026-04-16 |

## Chapter 1: Just Enough Microservices

Chapter 1 establishes the foundation: what microservices are, what monoliths are, and the three forces (coupling, cohesion, domain modeling) that drive how to decompose one into the other.

Core architecture:

- [[microservices]] — independently deployable services modeled around a business domain
- [[monolith]] — the three variants: single-process, distributed, third-party black-box
- [[independent-deployability]] — the central discipline; the single most important takeaway

Domain modeling:

- [[domain-driven-design]] — Eric Evans's modeling discipline as the source of microservice boundaries
- [[bounded-context]] — DDD's organizational boundary; the natural starting unit for a service
- [[aggregate]] — DDD's domain entity with a self-governing life cycle

Design pressures:

- [[information-hiding]] — Parnas's principle, applied to service boundaries
- [[coupling]] — four types: implementation, temporal, deployment, domain
- [[cohesion]] — "the code that changes together, stays together"

Organizational alignment:

- [[conways-law]] — why three-tier architectures are everywhere, and what changes with microservices

## Chapter 2: Planning a Migration

Chapter 2 reframes the entire decision: microservices are not a goal, they are a means to specific outcomes. The chapter covers the *why*, *whether*, *how-to-prioritise*, and *how-to-survive-organisationally* questions of a migration.

The core decision frame:

- [[why-microservices]] — Newman's three-question test; the legitimate motivations and the cheaper alternative for each
- [[when-microservices-are-a-bad-idea]] — unclear domain, true startups, customer-installed software, no clear reason
- [[modular-monolith]] — the cheaper alternative Newman invokes throughout the chapter

Decomposition method:

- [[incremental-migration]] — chip away one service at a time; production is what counts
- [[reversible-vs-irreversible-decisions]] — Bezos's two-way / one-way doors applied to migration choices
- [[cost-of-change]] — push experiments toward the whiteboard; reserve deliberation for database splits and public APIs
- [[extraction-prioritization]] — two-axis effort/benefit model for choosing the first service to extract
- [[event-storming]] — Brandolini's collaborative bottom-up domain modelling technique

Microservice motivations as standalone concepts:

- [[team-autonomy]] — Gore, Timpsons, two-pizza teams; cheaper alternatives that don't require microservices
- [[robustness-vs-resilience]] — David Woods's distinction; microservices give you neither for free

People and organisation:

- [[kotters-change-model]] — eight-step process for organisational change applied to microservice adoption
- [[reorganizing-teams]] — moving from competency silos to product teams; don't copy the Spotify model
- [[skills-self-assessment]] — private 1-5 self-rating; anonymised aggregate informs team-level investment

Knowing when to change course:

- [[measuring-microservice-transition]] — quantitative + qualitative; checkpoints; the sunk cost fallacy

## Chapter 3: Splitting the Monolith

Chapter 3 is the pattern catalogue for actually moving functionality out of the monolith. Newman's central message: incremental migration to microservices is a portfolio of well-known patterns, each with a specific shape of problem it fits. Most real migrations use a mix.

The patterns:

- [[strangler-fig-pattern]] — Newman's first port of call; intercept calls at the perimeter and reroute to a new service that grows alongside the monolith
- [[branch-by-abstraction]] — when the functionality is deep inside the monolith and you can't intercept at the perimeter; wrap it in an abstraction, build a new implementation alongside, switch over
- [[parallel-run-pattern]] — call both old and new on every request; compare results; high-confidence verification for risky migrations
- [[decorating-collaborator-pattern]] — proxy in front of the monolith triggers calls to a new service based on the outcome; useful when you can't change the monolith
- [[change-data-capture]] — react to data changes inside the monolith's database when no API or proxy interception is available
- [[ui-composition]] — splice the UI together from old and new sources at the page, widget, or micro-frontend level

Pattern selection and supporting concepts:

- [[migration-pattern-selection]] — guide for choosing among the patterns; the change-the-monolith-or-not question; copy vs reimplement
- [[seams-and-legacy-code]] — Michael Feathers's seam concept; the unit of refactoring inside the monolith
- [[deployment-vs-release]] — the foundational separation that all the patterns rely on
- [[feature-toggle]] — runtime switch for cutover and rollback; pair with branch by abstraction and strangler fig
- [[progressive-delivery]] — umbrella term covering parallel run, canary, dark launch, feature toggles
- [[service-mesh]] — per-service local proxies; avoids the shared-smart-pipe problem when the strangler fig proxy starts accumulating per-service logic

## Chapter 4: Decomposing the Database

Chapter 4 is the longest and most technically detailed chapter: the pattern catalogue for decomposing the database itself. Newman's view is that schema decomposition is the most expensive end of the migration work, and worth slowing down for.

Hub page:

- [[database-decomposition]] — the overarching catalogue and Newman's guidance on sequencing

Coping with a shared database when you can't yet split:

- [[shared-database-antipattern]] — why multiple services writing to one schema is the default starting point and the default problem
- [[database-view-pattern]] — read-only projections from the shared schema
- [[database-wrapping-service]] — thin service in front of a schema to turn DB dependencies into service dependencies
- [[database-as-a-service-interface]] — intentionally expose a *separate* read-only DB (Fowler's reporting database, generalised)

Transferring ownership:

- [[aggregate-exposing-monolith]] — expose data still owned by the monolith via a proper endpoint
- [[change-data-ownership]] — move data into the new service, invert the dependency

Synchronisation during migration:

- [[synchronize-data-in-application]] — three-step pattern from Trifork's Danish medical records migration
- [[tracer-write]] — incrementally move source-of-truth data; Square's Fulfillments example

Sequencing and low-level refactorings:

- [[split-the-database-first]] — schema first vs code first vs both-at-once; physical vs logical separation
- [[repository-per-bounded-context]] — factor data-access code along context lines as a first step
- [[database-per-bounded-context]] — separate schemas inside a modular monolith
- [[monolith-as-data-access-layer]] — expose an API on the monolith; JustSocial's pattern
- [[multischema-storage]] — the new service holds its own schema and still reads from the monolith
- [[split-table-pattern]] — separate a table along service boundaries
- [[move-foreign-key-to-code]] — replace a DB join with a service call; handle the consistency fallout
- [[shared-static-data]] — four patterns for country-code-style reference data

Transactions and sagas:

- [[saga]] — the alternative to distributed transactions; orchestrated vs choreographed; backward and forward recovery; compensating actions

Augmented existing pages:

- [[two-phase-commit]] — Newman's "just say no" framing
- [[distributed-transactions]] — sagas as the microservice alternative
- [[transactions]] — what you lose when splitting a database
- [[change-data-capture]] — additional Ch 4 roles (mapping engine, catch-up sync, tracer-write sync)
- [[event-sourcing]] — Newman's footnote on event sourcing as an alternative to soft deletes
- [[eventual-consistency]] — framing in microservice migrations; reconciliation as a practice
- [[information-hiding]] — database-decomposition as the embodiment of the principle

## Chapter 5: Growing Pains

Chapter 5 — *Growing Pains* — is the final substantive chapter. Newman catalogues the operational and organisational pain points that emerge as service count grows. Each section follows the same shape: how the pain shows itself, when it might occur, and potential solutions. His framing: think of microservice adoption as a dial, not a switch — as you turn it up, you encounter different problems at different scales.

The pain points and their pages:

- [[code-ownership-models]] — strong, weak, collective; collective stops working past ~20 developers; strong "almost universal" past 100; the "colander architecture" anecdote
- [[breaking-changes]] — eliminate accidental breakage or the architecture becomes untenable; structural vs semantic; three rules; coexisting versions vs one-service-two-contracts
- [[consumer-driven-contracts]] — Pact-style consumer-written specifications; replace cross-service tests; "poorly underused practice for solving a really difficult problem"
- [[cross-service-analytics]] — split databases break the assumption that everything is queryable from one schema; push to a dedicated analytics database; same mechanism as Chapter 4's [[database-as-a-service-interface]]
- [[monitoring-and-observability]] — shift from monitoring (known causes) to observability (open-ended questions); the Honest Status Page murder-mystery quote
- [[log-aggregation]] — Newman's "do this first" recommendation; ELK and Humio; an organisational litmus test
- [[correlation-ids]] — single ID propagated through call chains; the prerequisite for distributed tracing; add early
- [[distributed-tracing]] — Jaeger and friends; latency attribution where logs can't help
- [[synthetic-transactions]] — test in production via scripted fake users; the Atomist onboarding example; the 200-washing-machines warning
- [[local-developer-experience]] — JVM hits the laptop ceiling; stubbing, hybrid setups, Telepresence, Azure Functions; ongoing investment, not a one-time fix
- [[running-too-many-things]] and [[desired-state-management]] — manual deployment doesn't scale; serverless-first on cloud; Kubernetes when needed; OpenShift; "don't adopt because everyone else is"
- [[end-to-end-testing]] — large cross-team test suites become slow, flaky, ambiguous; limit scope, use CDCs, lean on progressive delivery, refine the feedback cycle
- [[global-vs-local-optimization]] — three-databases example; cross-cutting technical groups; Monzo's free-form proposals; refuse to prescribe a balance
- [[robustness-and-resiliency-at-scale]] — Newman's two questions per call; isolation, time-outs, circuit breakers; Release It! and *Building Microservices* Ch 11
- [[orphaned-services]] — services running for years with no owner; FT's Biz Ops and the System Operability Score

Augmented existing pages:

- [[independent-deployability]] — added what threatens independent deployability at scale (breaking changes, ownership, end-to-end testing, orphans)
- [[microservices]] — added "Growing pains as you scale" section indexing all Chapter 5 pages
- [[progressive-delivery]] — added automated release remediation and Spinnaker
- [[robustness-vs-resilience]] — added how the Ch 2 distinction operationalises in Ch 5; documenting incidents
- [[team-autonomy]] — added the global-vs-local-optimisation flip side
- [[database-as-a-service-interface]] — added Chapter 5 framing as a pain-remedy

## Related pages

- [[microservices]]
- [[monolith]]
- [[modular-monolith]]
- [[independent-deployability]]
- [[bounded-context]]
- [[information-hiding]]
- [[coupling]]
- [[cohesion]]
- [[why-microservices]]
- [[incremental-migration]]
- [[extraction-prioritization]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[parallel-run-pattern]]
- [[migration-pattern-selection]]
- [[database-decomposition]]
- [[saga]]
- [[breaking-changes]]
- [[consumer-driven-contracts]]
- [[monitoring-and-observability]]
- [[end-to-end-testing]]
- [[code-ownership-models]]
