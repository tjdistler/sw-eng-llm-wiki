# MOC: Decomposing a Monolith

**Summary**: Entry point for questions about pulling services out of a monolith — sequencing, extraction patterns, database untangling, organizational pressure, and the operational step-up required for the new service. Start here when someone asks "should we split this?" or "how do we split this?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have a monolith. Someone wants to extract a service from it, or you're weighing whether a split is the right move at all. This MOC is the decision frame plus the pattern catalogue plus the handoffs to sibling topic areas (data, consistency, microservices, reliability) that any real extraction touches.

The canonical shape of a question that lands here: *"We need to pull X out of the monolith so we can scale / ship independently / stop the blast radius — what are our options and what should we consider?"* The answer almost always crosses six clusters, not one. Follow this MOC end-to-end before drafting.

## Is extraction the right move?

Before reaching for any pattern below, pressure-test the premise. Microservices are a means, not an end — and a migration costs real time and real reliability before it buys anything back.

- [[why-microservices]] — Newman's three-question test. If you can't name the outcome you want and the cheaper alternative you've ruled out, don't extract.
- [[when-microservices-are-a-bad-idea]] — unclear domain, true startup, customer-installed software, no clear reason. Any of these and the answer is usually "not yet."
- [[modular-monolith]] — the cheaper alternative Newman invokes throughout *Monolith to Microservices*. A well-modularised monolith gets you most of the independent-change benefits without the distributed-systems tax.
- [[independent-deployability]] — the central discipline that makes microservices worth the cost. If you can't ship the extracted service without coordinating a monolith release, you've paid the cost and bought nothing.
- [[extraction-prioritization]] — Newman's two-axis effort-vs-benefit model for *which* service to pull out first. Start where the upside is highest and the database entanglement is lowest.
- [[architectural-quantum]] — Ford and Richards's term for the smallest independently-deployable unit with its own data and operational boundary. If the candidate can't form its own quantum, you're not really extracting a service.
- [[reversible-vs-irreversible-decisions]] — keep the experiments reversible. Database splits and public API shapes are the one-way doors that warrant the slow deliberation.
- [[cost-of-change]] — push whiteboard experiments hard before committing code. The bill comes due during database decomposition.

Deeper reading: [[monolith-to-microservices#chapter-2-planning-a-migration]].

## Finding the seams

Once the decision is "yes, extract," the next question is *where to cut*. Seams come from the domain, not the codebase.

- [[domain-driven-design]] — Evans's modeling discipline is the source of microservice boundaries. Extract along domain seams or expect to pay the re-cut later.
- [[bounded-context]] — the natural starting unit for a service. One context per service is the default; sub-divide only when scaling pressure demands it.
- [[aggregate]] — the domain entity with a self-governing life cycle. Aggregates rarely split cleanly across services — if your candidate service owns half an aggregate, rethink the boundary.
- [[coupling]] — Newman's four types (implementation, temporal, deployment, domain). Judge each candidate seam by what stays coupled after the split; implementation coupling is the one that actually goes away, the others travel with you.
- [[cohesion]] — "the code that changes together stays together." A split that cuts across a high-cohesion cluster will re-cohere at the network boundary and cost you latency for nothing.
- [[information-hiding]] — Parnas's principle, applied to service boundaries. The extracted service's API is the *only* way in; leaks (shared tables, shared constants, shared deploy pipelines) re-create the coupling you paid to remove.
- [[event-storming]] — Brandolini's collaborative workshop format. The single best way to surface real seams with domain experts before committing to a split.
- [[incremental-migration]] — chip away one service at a time; production is what counts. Don't batch extractions, because every extraction teaches you something about the next one.

Deeper reading: [[monolith-to-microservices#chapter-1-just-enough-microservices]].

## Extraction patterns (the code side)

The catalogue of moves for getting the code out. Most real migrations use a mix — pick by the shape of the problem, not by pattern fashion.

- [[strangler-fig-pattern]] — Newman's default. Intercept at the perimeter, route to the new service, let the new service grow alongside the monolith. Works when you can intercept at a network edge.
- [[branch-by-abstraction]] — when the functionality is deep inside the monolith and you can't intercept at the edge. Wrap it in an abstraction, build a new implementation alongside, flip the switch.
- [[parallel-run-pattern]] — call both old and new on every request; compare results; cut over only when the new side has proven correct. Use this for money, safety-critical, or legally-exposed domains where "oops" is not an acceptable outcome.
- [[decorating-collaborator-pattern]] — proxy in front of the monolith triggers calls to a new service based on the outcome. The minimal-code option when you can't change the monolith at all.
- [[change-data-capture]] — react to data changes inside the monolith's database when no API or proxy interception is available. Also the default async bridge that lets the new service read a projection of the monolith's state during transition — see the next section.
- [[ui-composition]] — splice the UI from old and new sources at page, widget, or micro-frontend granularity. Don't forget the UI needs its own extraction plan.
- [[migration-pattern-selection]] — the guide for choosing among the patterns; includes the change-the-monolith-or-not question and the copy-vs-reimplement question.
- [[seams-and-legacy-code]] — Michael Feathers's seam concept. The unit of refactoring inside the monolith, and what most of the above patterns are operating on.
- [[deployment-vs-release]] — the foundational separation every one of these patterns depends on. Deploy the new service dark; flip release via feature toggle.
- [[feature-toggle]] — runtime switch for cutover and rollback. Pair with strangler fig and branch by abstraction; plan toggle-removal into the extraction itself or the toggles become their own legacy.
- [[progressive-delivery]] — the umbrella that covers parallel run, canary, dark launch, and feature toggles. The operational posture that lets you extract without a big-bang release.
- [[service-mesh]] — per-service local proxies. Useful when the strangler-fig interception layer starts accumulating per-service logic and becoming a shared smart pipe.

Deeper reading: [[monolith-to-microservices#chapter-3-splitting-the-monolith]].

## Database decomposition (the hard part)

This is where extractions stall. The move is almost always [[change-data-capture]] plus [[shared-database-antipattern]] as an *explicit transitional state* — a thing you know you have and will get out of, not a thing you pretend isn't there.

The hub:

- [[database-decomposition]] — the overarching catalogue and Newman's sequencing guidance.

Coping with the shared DB when you can't yet split:

- [[shared-database-antipattern]] — why multiple services writing to one schema is the default starting point and the default problem. The antipattern is *ending up here permanently*, not passing through.
- [[database-view-pattern]] — read-only projection from the shared schema. Cheapest read-side decoupling.
- [[database-wrapping-service]] — thin service in front of a schema to turn DB dependencies into service dependencies. A stepping stone, not a terminal state.
- [[database-as-a-service-interface]] — intentionally expose a *separate* read-only DB (Fowler's reporting database, generalised). The right move when downstream consumers genuinely need a DB-shaped integration.

Transferring ownership:

- [[aggregate-exposing-monolith]] — expose data still owned by the monolith via a proper endpoint. Inverts the dependency so the new service doesn't reach into the old schema.
- [[change-data-ownership]] — actually move the data into the new service and flip the source of truth.

Synchronising during migration:

- [[synchronize-data-in-application]] — the three-step pattern from Trifork's Danish medical records migration. Application writes both stores, then reads switch, then old store retires.
- [[tracer-write]] — incrementally move source-of-truth data; Square's Fulfillments example. Useful when the cutover must happen row-by-row rather than all-at-once.

Sequencing and low-level refactorings:

- [[split-the-database-first]] — schema-first vs code-first vs both-at-once. Newman's hot take: schema-first if you're worried about performance or consistency; code-first otherwise; never both at once. This one page covers both sides of the schema-vs-code debate.
- [[repository-per-bounded-context]] — factor data-access code along context lines as a first step inside the monolith.
- [[database-per-bounded-context]] — separate schemas inside a modular monolith. The halfway house that buys most of the benefit for a fraction of the cost.
- [[monolith-as-data-access-layer]] — expose an API on the monolith; JustSocial's pattern.
- [[multischema-storage]] — the new service holds its own schema and still reads from the monolith during transition.
- [[split-table-pattern]] — separate a table along service boundaries. Painful; save for when the seam really is inside the row.
- [[move-foreign-key-to-code]] — replace a DB join with a service call and handle the consistency fallout in application code.
- [[shared-static-data]] — four patterns for country-code-style reference data; the one kind of "shared table" that's usually fine.

Deeper reading: [[monolith-to-microservices#chapter-4-decomposing-the-database]]. This is the longest chapter in the book, for good reason — read it in full if the domain is money or safety-critical.

## Correctness across the split

Once data spans two stores, the transaction you used to take for granted is gone. You need compensations, not two-phase commit.

- [[saga]] — the alternative to distributed transactions; orchestrated vs choreographed; backward and forward recovery; compensating actions. The core pattern for multi-step correctness across services.
- [[outbox-table-pattern]] — atomic write of business state and the event that announces it. The async publication mechanism that makes sagas safe in the face of service failures.
- [[two-phase-commit]] — Newman's "just say no" framing. Included here so you can recognise it and route around it.
- [[distributed-transactions]] — sagas as the microservice alternative; the trade-offs that make 2PC a bad fit.
- [[transactions]] — what you lose when splitting a database. Start here to calibrate how much correctness is actually at stake.
- [[eventual-consistency]] — framing in microservice migrations; reconciliation as an ongoing practice, not a one-time cleanup.

If the domain is money or safety-critical, this section is not optional — combine parallel run (above) with saga-based correctness, and read the full *Consistency and Transactions* material (MOC forthcoming) end to end.

## Organisational pressure

Conway's Law is unforgiving. A technical extraction that ignores the org chart will snap back.

- [[conways-law]] — why three-tier architectures are everywhere, and what changes with microservices. You cannot extract a service past a team boundary that doesn't exist.
- [[team-autonomy]] — Gore, Timpsons, two-pizza teams; the cheaper alternatives that don't require microservices. If you can't give the extracted service to an autonomous team, question whether you're actually extracting.
- [[reorganizing-teams]] — moving from competency silos to product teams; Newman's warning not to copy the Spotify model. The extraction may require the reorg, not the other way around.
- [[microservice-to-team-assignment]] — how to parcel services across teams; the handoff points that determine whether independence survives contact with reality.
- [[kotters-change-model]] — eight-step process for organisational change applied to microservice adoption. Most migrations die of change-management failure, not technical failure.
- [[skills-self-assessment]] — private 1–5 self-rating; anonymised aggregate informs team-level investment. Names the skill gap the new service will expose.
- [[code-ownership-models]] — strong, weak, collective. Collective stops working past ~20 developers; extractions often force the move from collective to strong ownership whether or not you planned for it.
- [[measuring-microservice-transition]] — quantitative and qualitative checkpoints; the sunk-cost antidote. Name success and failure conditions before you start.

Deeper reading: [[monolith-to-microservices#chapter-5-growing-pains]] catalogues what breaks at scale.

## Operational step-up for the extracted service

A new service isn't done when the code compiles. It's done when it has its own reliability posture, its own observability, and its own on-call.

- [[service-level-objective]] — the target the new service commits to. Don't extract without one; "same as the monolith" is not an answer.
- [[service-level-indicator]] — the metrics the SLO is built on. Latency, error rate, availability — pick the two or three that actually reflect user experience.
- [[service-level-agreement]] — if the service has external contractual obligations, the SLA shapes the SLO (and the SLO must beat the SLA with margin).
- [[slo-expectations]] — published SLOs set expectations. Set them deliberately, with an internal-vs-external margin; don't accidentally overachieve.
- [[error-budget]] — the operational currency that lets feature velocity and reliability trade against each other without shouting matches.
- [[risk-management-sre]] — the framing behind SLOs: nobody wants 100%, because 100% costs more than the marginal reliability is worth.
- [[monitoring-and-observability]] — the shift from "watch known causes" to "ask open-ended questions." Newman frames this as a prerequisite, not a nice-to-have, once you pass one service.
- [[log-aggregation]] — Newman's "do this first" recommendation. ELK, Humio, your cloud equivalent — the litmus test for whether the organisation can support a second service at all.
- [[correlation-ids]] — single ID propagated through call chains. The prerequisite for distributed tracing; add it before the first extraction, not after the third.
- [[distributed-tracing]] — Jaeger and friends; latency attribution where logs cannot help. Becomes essential the moment a user request touches more than one service.
- [[synthetic-transactions]] — scripted fake users that exercise the new service in production. Catches the failure modes that unit and integration tests miss.
- [[robustness-and-resiliency-at-scale]] — Newman's two questions per call: what happens if this call fails? what happens if it's slow? Isolation, timeouts, circuit breakers.
- [[end-to-end-testing]] — its limits once services multiply. Lean on consumer-driven contracts and progressive delivery instead of growing a cross-team E2E suite.
- [[consumer-driven-contracts]] — Pact-style consumer-written specifications. The contract-testing discipline that prevents the new service from silently breaking consumers after cutover.
- [[orphaned-services]] — the shape of the failure mode this MOC exists to prevent. A service with no owner, no SLO, no on-call. Plan ownership and operations *before* cutover, not after.

Deeper reading: [[monolith-to-microservices#chapter-5-growing-pains]] for the full pain catalogue; Newman's Ch 5 is essentially the operational playbook for everything an extraction unleashes.

## Sibling MOCs

Once the corresponding MOCs land, the handoffs below become wikilinks. For now they're plain pointers to where the jurisdictional boundary sits.

- *moc-microservices* (forthcoming) — owns the ownership, independence, and organisation-around-services view once the decision to have microservices is made. `moc-decomposition` gets you *to* microservices; `moc-microservices` is about *running* them.
- *moc-domain-driven-design* (forthcoming) — owns the deep DDD material. This MOC borrows bounded contexts and aggregates as seam-finding tools; the DDD MOC owns the modelling discipline itself.
- *moc-data-models-and-storage* (forthcoming) — owns the target schema shape on the other side of the split. This MOC gets you out of the shared DB; the data MOC is about what the new store should look like.
- *moc-consistency-and-transactions* (forthcoming) — owns saga, outbox, and the full correctness-across-stores story. This MOC cites saga and outbox as the minimum you need during extraction; the consistency MOC owns the deeper trade-offs.
- *moc-distributed-systems* (forthcoming) — owns the failure-mode material once the extracted service is in production. Partial failures, unreliable networks, clock skew, consensus — the problems the monolith didn't have and the new service inherits.
- *moc-reliability-and-operations* (forthcoming) — owns the full SLO/SLI/error-budget, observability, on-call, and incident-response story. This MOC names the operational step-up as a gate before cutover; the reliability MOC is the playbook.

## Related pages

- [[index]]
- [[monolith-to-microservices]]
- [[microservices]]
- [[monolith]]
- [[modular-monolith]]
- [[independent-deployability]]
- [[database-decomposition]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[parallel-run-pattern]]
- [[change-data-capture]]
- [[saga]]
- [[outbox-table-pattern]]
- [[shared-database-antipattern]]
- [[conways-law]]
- [[service-level-objective]]
- [[error-budget]]
- [[monitoring-and-observability]]
