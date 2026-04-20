# MOC: Microservices

**Summary**: Entry point for questions about *running microservices* — the defining properties, the granularity decisions, the ownership and data disciplines, the reuse trade-offs, the operational substrate (sidecars, service mesh, platform tax), and the organisational shape required to keep independent deployability actually independent. Start here when the question is "how do we organise *around* services?" rather than "should we extract?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have — or are about to have — microservices, and you need a principled frame for how to live with them. The decision to adopt has already been made (or you're returning to pressure-test it); what's in front of you now is *service boundaries, ownership, data, communication, reuse, platform, operations, and organisation*. This MOC is the practitioner's map of that territory.

This MOC sits beside [[moc-decomposition]]. Two-sentence rule for where to land:

- **[[moc-decomposition]]** gets you *to* microservices — is extraction the right move, where are the seams, how do we pull a service out, how do we untangle the database, how do we stay correct across the split.
- **moc-microservices** (this one) is about *running* microservices — what defines the style, how big each service should be, who owns what data, how services talk, how reuse is managed, what platform the fleet needs, how teams organise around the services.

If the question starts with *"we have a monolith and we need to..."*, you're on the wrong MOC — go to [[moc-decomposition]]. If the question starts with *"we have (or will have) microservices and we need to..."* — or the question is about the style itself, abstracted from any particular migration — you're in the right place.

The canonical shape of a question that lands here: *"How big should a service be?"*, *"Should we share this library or duplicate?"*, *"What belongs in the service vs the sidecar?"*, *"How do services talk to each other?"*, *"Who owns this data?"*, *"Why is our microservices architecture so painful to change?"* The answer is rarely a pattern — it's a set of disciplines applied consistently.

## What microservices actually are

Before any of the running-them material, get the definition straight. The pain in most "our microservices are awful" conversations traces to one of the three defining properties being quietly broken.

- [[microservices]] — the hub: Newman's three-property definition (independently deployable, modelled around a business domain, own their own data) plus Richards and Ford's Chapter 17 style-catalogue framing (the physical embodiment of [[bounded-context|bounded contexts]]; duplication preferred over coupling; the star-rated scorecard of extremes). The most dense single page in this cluster — read it before anything else here.
- [[monolithic-vs-distributed]] — microservices sit firmly on the distributed side, with all the cost that implies. The reminder that "just use microservices" is a decision to pay the distributed tax for the system's entire lifetime, not just its first year.
- [[fallacies-of-distributed-computing]] — the eight fallacies microservices pay continuously. Every interservice call is a bet that the network is reliable, latency is negligible, and the payload is small enough. Every *successful* microservices architecture has disciplined answers to each fallacy.
- [[architectural-quantum]] — Richards and Ford's physical-deployment unit; a microservices architecture is multi-quantum *if and only if* each service owns its data and avoids synchronous coupling to other services. Shared databases or pervasive sync calls collapse the quantum count back to one and revoke the characteristic-per-service benefit the style exists to deliver.
- [[distributed-monolith]] — the failure mode: multiple services, but coupled so tightly that you pay the distributed cost without gaining any of the benefits. Newman's frame: "all the disadvantages of a distributed system, and the disadvantages of a single-process monolith, without enough upsides of either." This is what badly-run microservices become.

Deeper reading: [[monolith-to-microservices#chapter-1-just-enough-microservices]], [[fundamentals-of-software-architecture#chapter-9-foundations]], [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]].

## Should we even have microservices? (the gate before the rest of this MOC)

This section is deliberately short. Most of it lives on [[moc-decomposition]]'s "Is extraction the right move?" section — but the question lands here too when the framing is greenfield rather than extraction.

- [[why-microservices]] — Newman's three-question test: what outcome are you hoping to achieve; have you considered cheaper alternatives; how will you know if the transition is working. If you can't answer all three, the answer to "microservices?" is "not yet."
- [[when-microservices-are-a-bad-idea]] — unclear domain, true startup, customer-installed software, no clear reason. The checklist of cases where the style costs more than it can pay back.
- [[modular-monolith]] — the under-valued alternative. A well-modularised monolith buys most of the independent-change benefits of microservices without the operational step-up; Newman and Bellemare both argue that most smaller organisations will do better here.
- [[measuring-microservice-transition]] — Newman's quantitative-plus-qualitative checkpoint rubric. Name success and failure conditions *before* you commit.

If the answer is still "yes, microservices," continue. Otherwise return to [[moc-architecture-styles]] for alternatives ([[service-based-architecture]] is often the underrated compromise) or [[moc-decomposition]] if you're working out of a monolith.

## Independent deployability — the load-bearing discipline

If there is only one thing to take out of this MOC, it's this: microservices without independent deployability are a distributed monolith in a trenchcoat. Newman is emphatic — *"If there is only one thing you take out of this book, it should be this."*

- [[independent-deployability]] — the ability to change one microservice and ship it to production without deploying anything else. Not a capability, a practised *discipline*. What it requires (explicit contracts, no shared DBs, stable interfaces); what threatens it at scale (breaking changes, collective ownership, heavyweight E2E test suites, orphaned services).
- [[breaking-changes]] — contract breakage is independent deployability *failing*. Organisations that don't solve this for a fleet don't survive to grow the fleet.
- [[consumer-driven-contracts]] — Pact-style consumer-authored contracts. The discipline that prevents accidental breakage; the alternative to the heavyweight cross-team E2E suite that kills independent deployability as service count grows.
- [[contracts]] / [[strict-contract]] / [[loose-contract]] — the axis of contract rigidity; Bellemare's distinction between data-schema contracts (the EDM default) and API contracts (the synchronous default). Schemas give change-management properties APIs alone cannot match.
- [[deployment-vs-release]] — the separation that lets independent deployability coexist with safe rollout. Ship the new service dark; flip release via feature toggle.
- [[feature-toggle]] — runtime switch for cutover and rollback. Plan toggle-removal into the feature itself, or the toggles become their own legacy.
- [[progressive-delivery]] — canary, blue-green, parallel run, feature toggles. The operational posture that keeps independent-deploy deploys *safe*; without it the discipline collapses under incident pressure.
- [[blue-green-deployment]] — the classic low-risk cutover for a service with external callers.
- [[canary-test]] — gradual rollout to a traffic fraction; the default for higher-risk changes in a fleet.

Deeper reading: [[monolith-to-microservices#chapter-1-just-enough-microservices]] for Newman's framing; [[monolith-to-microservices#chapter-5-growing-pains]] for what breaks independent deployability as the fleet grows.

## Service granularity — the hardest single decision

Granularity is the architect's central ongoing decision in the style. Get it wrong one way and you have a distributed monolith; get it wrong the other way and you have a choreography mess plus a sagas problem. "Microservice" is a label, not a commandment to build the smallest possible services (Fowler, via Richards and Ford).

- [[service-granularity]] — the canonical page: the hardest decision in microservices; Chapter 17's three guidelines (purpose, transactions, choreography); the *fix granularity, not transactions* maxim. The right answer to "our distributed transactions are painful" is almost always "you split too small," not "let's add a coordinator."
- [[granularity-disintegrators]] — the six forces *pulling services apart*: scope/cohesion, code volatility, scalability, fault tolerance, security, extensibility. Six sharp arguments for why a given service should be smaller.
- [[granularity-integrators]] — the four forces *keeping services together*: database transactions, workflow/choreography, shared code, data relationships. Four sharp arguments for why a given split would cost more than it saves.
- [[architectural-modularity]] — *Hard Parts*'s architectural-modularity rubric; the five-driver test for *whether* a system needs more deployment units (maintainability, testability, deployability, scalability, fault tolerance). The yes-you-should-split checklist.
- [[code-volatility]] — the most underused signal on the disintegrator side. Modules on wildly different change rates probably belong in different services; modules that change together probably belong together.
- [[entity-trap]] — the standing anti-pattern: one `*Manager` component per database entity. If your service map reads like a list of tables, you've built an ORM, not an architecture. See [[moc-domain-driven-design]] for the positive replacement (workflow- or event-based decomposition).
- [[service-based-architecture]] — the coarser-grained sibling style, worth naming here because many teams who "want microservices" actually want service-based and would get better outcomes from 4–12 coarse services with a shared ACID database. Recognise when it's the right answer.

Deeper reading: [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]] for Richards and Ford's three guidelines; [[software-architecture-the-hard-parts]] Chapters 3 and 7 for the full architectural-modularity plus disintegrator/integrator treatment.

See also [[moc-components-and-partitioning]] for the inside-the-box coupling-cohesion-connascence measurements that operationalise the granularity intuition.

## Data ownership — own your own data

Data ownership is the second of Newman's three defining properties. Breaking it is the fastest way to turn microservices into a distributed monolith: a shared database collapses every service depending on it into a single quantum, defeats the per-service characteristic scoping, and re-creates the implementation coupling extraction was supposed to remove.

- [[data-ownership]] — *Hard Parts* Chapter 9: the writer-owns-the-table rule. Reads don't confer ownership, writes do. The three ownership scenarios: single (trivial), common (dedicated service fix), joint (four techniques).
- [[joint-ownership-techniques]] — table split, data domain, delegate, service consolidation. Four resolutions for the legitimately-shared-table case; no universally-right answer — pick by trade-off.
- [[shared-database-antipattern]] — the failure mode to know by name. Why multiple services writing to one schema is the pathology every microservices architecture is trying to escape.
- [[information-hiding]] — Parnas's principle, applied at the service boundary. The extracted service's API is the *only* way in; leaks (shared tables, shared constants) re-create the coupling you paid to remove.
- [[polyglot-persistence]] — the natural payoff of per-service data ownership. Each service team picks the storage technology that fits its workload; the architecture doesn't pay a global relational-schema tax for capabilities only one service needs.
- [[distributed-data-access]] — the other side of the coin: once each service owns its data, *reads* across the fleet need a story. The four *Hard Parts* Chapter 10 patterns: [[interservice-communication-pattern]], [[column-schema-replication-pattern]], [[replicated-caching-pattern]], [[data-domain-pattern]] — each trading latency, staleness, fault coupling, and storage cost differently.
- [[data-domain]] — the unit of [[database-decomposition]] on the data-architect side. Ideally one bounded context per data domain; the alignment is what makes per-service data sovereignty work.

If the domain is money, safety-critical, or otherwise cross-service-transactional, the correctness story across owned data is as much a design concern as the ownership assignment itself. See *moc-consistency-and-transactions* when it lands; the preview is [[saga]] for cross-service workflows and [[outbox-table-pattern]] for atomic state-plus-event publication.

Deeper reading: [[monolith-to-microservices#chapter-4-decomposing-the-database]] for the monolith-to-microservices split; [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]] for the structural-consequence framing.

## Communication — sync, async, and the event-driven default

Once services own their data, the second design surface is how they talk. The options fall on a sync/async axis that maps closely onto the orchestration/choreography axis; each combination is a trade-off between loose coupling and workflow clarity.

- [[synchronous-microservices]] — the classic request/response form. Bellemare's seven structural weaknesses (point-to-point coupling, dependent scaling, failure-handling complexity, etc.) are the motivation for preferring asynchronous when either end of the call can tolerate it.
- [[event-driven-microservices]] — Bellemare's style of microservices that communicate by producing and consuming durable events on shared event streams. The entire organisational data communication structure becomes explicit infrastructure rather than ad hoc point-to-point pipework. A natural match for microservices because it preserves the decoupling the style is built on.
- [[rpc]] — the wire-level default for sync calls. gRPC, REST-over-HTTP, Thrift; the baseline protocol family.
- [[interservice-communication-pattern]] — the default cross-service read: call the owning service over the network. The three *Hard Parts* latencies (network 30–300ms, security 20–400ms, data 10–50ms) summed argue for caching and replication when the pattern is hot.
- [[broker-topology]] / [[mediator-topology]] — the inter-service event-driven shapes. Broker = choreography (services react to events, emergent workflow); mediator = orchestration (central service holds the workflow, issues commands). The same trade-off applies at the [[saga]] level.
- [[choreography]] — the decoupled default for microservices. Each service listens for events and reacts; no central controller. Preserves the style's decoupling philosophy; cost is distributed workflow state (the "front controller" anti-pattern emerges when a would-be orchestrator gets bolted on informally).
- [[orchestration]] — the centralised alternative. One orchestrator holds the workflow; error handling has a home; recoverability is straightforward. The right call when the workflow is complex, regulatory, or needs a single place to inspect state — but watch for the "God service" anti-pattern.
- [[saga]] — the alternative to distributed transactions; orchestrated or choreographed; backward/forward recovery via compensating actions. Needed any time a business operation writes to more than one owned data store. Warning: frequent need for sagas is a granularity smell — see [[service-granularity]].
- [[outbox-table-pattern]] — atomic write of business state and the event that announces it. The async publication mechanism that makes choreography safe in the face of service failure.
- [[event-streams]] — the substrate for durable, replayable event-driven communication; [[log-based-message-brokers|Kafka-style log brokers]] as the canonical implementation.
- [[message-brokers]] — the broader family; the contrast with [[event-broker|event brokers]] (events are persisted, replayable, multi-consumer) is load-bearing for event-driven microservices.
- [[event-driven-request-response-integration]] — Bellemare's Chapter 13: how event-driven microservices cohabit with request/response where each is best suited. Hybrid is the norm; a pure-one-or-the-other fleet is rare and usually a smell.
- [[stamp-coupling]] — passing whole structures when only a subset is needed. The bandwidth-fallacy version of "our services are a bit too chatty." GraphQL, field masks, and narrow event types are the counter-patterns.

Deeper reading: [[building-event-driven-microservices#chapter-1-why-event-driven-microservices]] for the motivational argument against sync-by-default; [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]] for how Richards and Ford place communication choice within the style.

See also *moc-events-and-streaming* (forthcoming) for the deeper event-driven architectural material; *moc-consistency-and-transactions* (forthcoming) for the full saga/outbox/eventual-consistency treatment.

## Reuse — prefer duplication to coupling

The microservices style inverts a reflex every working programmer has. Two decades of DRY training says *don't repeat yourself*; the microservices Chapter 17 slogan says *prefer duplication to coupling*. Reuse is not bad — it's just narrower than you're used to, and the wrong kind of reuse kills independent deployability by making every service wait for a shared-library upgrade.

- [[reuse-patterns]] — the *Hard Parts* Chapter 8 hub: the four techniques available in distributed architectures ([[code-replication-pattern|code replication]], [[shared-library-pattern|shared library]], [[shared-service-pattern|shared service]], [[sidecar-pattern|sidecar/mesh]]) plus the decision matrix. The chapter's resolution of the "reuse is abuse" / "share nothing" early-microservices slogans.
- [[code-replication-pattern]] — just copy it. The right move for genuinely static, tiny one-offs; avoids the overhead of a library for code that won't churn.
- [[shared-library-pattern]] — compile-time coupling; the right move for homogeneous stacks and low-to-moderate change rates. Versioning gives controlled change; fine-grained libraries beat god-libraries.
- [[shared-service-pattern]] — runtime coupling; the right move for polyglot environments or fast-changing logic. Pay the dynamic-coupling tax (latency, scalability, fault coupling) in exchange for instant rollout and language-independence.
- [[sidecar-pattern]] — the orthogonal-coupling answer. Cross-cutting operational concerns (monitoring, logging, mTLS, circuit breaker, service discovery) deployed as a separate container alongside every service. The structural answer to "microservices prefer duplication, but monitoring genuinely needs one implementation."
- [[service-mesh]] — the fleet-scale version of the sidecar idea: every pod gets a local proxy, centrally controlled. The operational reuse vehicle Richards and Ford treat as a first-class part of the microservices style, not a bolt-on.
- [[orthogonal-coupling]] — the *Hard Parts* coupling axis that the sidecar answers. Two parts with distinct purposes that must intersect; the right model for cross-cutting concerns layered on top of a domain-partitioned architecture.

The single decision rule: *domain concerns → duplicate; operational concerns → sidecar; shared state → dedicated service*. The [[orchestration-driven-soa]] failure mode was conflating these — the modern style keeps them architecturally separate.

## The operational substrate — what a running fleet needs

Microservices without a platform is an unrunnable architecture. This section is the checklist of infrastructure that has to exist before the first service ships to production, plus the organisational posture for paying for it.

- [[microservice-tax]] — Bellemare's name for the cost of running a fleet: event broker, container management system, CI/CD, monitoring, logging, schema registry. Paid either centrally (one platform team, one well-built stack) or per-team (ten bad versions of each piece). *The tax is paid either way; the question is who pays and how.* The single most important budgeting concept in this cluster.
- [[frameworks-and-sre-platform]] / [[service-framework]] — Google's per-language service frameworks: prescriptive packaging of instrumentation, logging, load-shedding, and overload-handling behaviour. Same API and behaviour across languages; development teams pick language freely, SRE gets uniform operational semantics. The anti-snowflake discipline that keeps the fleet operable.
- [[containers]] / [[container-management-system]] — Kubernetes, ECS, Nomad. The substrate for scheduling many small services, handling health checks, and supporting elastic scaling. The bare-minimum platform piece alongside the broker for event-driven microservices.
- [[service-discovery]] — which instance-IP-port combo to talk to, in an environment where those change continuously. DNS, coordination services (Zookeeper, etcd, Consul), service mesh, ambassador pattern — the catalogue of answers.
- [[microservice-creation-workflow]] — the automated "create a repo, wire CI/CD, register ownership, set up streams and ACLs, apply a template" process. The leverage point where platform improvements propagate automatically, instead of drifting as each team copies last month's project.
- [[microservice-to-team-assignment]] — the ownership-registry piece. Every service has exactly one owning team; ownership is queryable, authoritative, and enforced by tooling.
- [[heavyweight-framework-microservice]] / [[lightweight-framework-microservice]] / [[basic-producer-consumer-microservice]] — the three implementation postures for event-driven microservices, trading framework weight against operational complexity. BPCs for simple flows, lightweight (Kafka Streams, Samza) for the stateful-topology sweet spot, heavyweight (Spark, Flink) for analytics-scale workloads.
- [[functions-as-a-service]] — the far-end-of-the-spectrum option: per-event serverless compute. Useful when invocation cost and elasticity matter more than steady-state throughput.
- [[microservice-topology]] / [[business-topology]] — Bellemare's two-scale distinction: the internal processing graph of one service (microservice topology) vs the inter-service graph of streams and APIs (business topology). Keeps the architecture tractable — reason about one service's internals without needing to know every other's.
- [[edm-deployment-patterns]] / [[edm-deployment-principles]] — deployment patterns and principles specific to event-driven microservices: rolling updates, consumer-group coordination, schema-registered contract changes, offset management for reprocessing.
- [[self-service-release-model]] — the SRE-era release posture that lets small teams ship their own services without platform-team bottlenecks; the organisational complement to independent deployability.

Deeper reading: [[building-event-driven-microservices#chapter-2-event-driven-microservice-fundamentals]] for the microservice-tax and platform-piece framing; [[building-event-driven-microservices#chapter-14-supportive-tooling]] for the self-serve tooling catalogue.

See also *moc-container-and-serving-patterns* (forthcoming) for the deeper container-patterns material and *moc-reliability-and-operations* (forthcoming) for SLO/SLI, observability, incident response, and the full operations playbook that complements this section.

## Growing pains — what breaks as the fleet scales

Newman's Chapter 5 is essentially the operational playbook for everything a mid-sized microservices fleet unleashes. Most of these pains are "didn't show up at five services, become existential at fifty." Read this section *before* the fleet reaches that size, not after.

- [[code-ownership-models]] — strong, weak, collective. Collective ownership stops working around 20 developers and causes distributed-monolith pathology by 100. The move to strong ownership is usually forced by the architecture whether or not it's planned for.
- [[local-developer-experience]] — running a representative slice of the fleet on a laptop becomes impossible past a handful of services; stubs, hybrid cloud-dev setups, or remote development become load-bearing. Plan for this explicitly.
- [[running-too-many-things]] — manual deployment doesn't scale past a small fleet. The forcing function for Kubernetes, serverless, or whatever automation substrate the org lands on.
- [[end-to-end-testing]] — large cross-team E2E suites become slow, flaky, and ambiguous as the fleet grows. Shift to [[consumer-driven-contracts]], [[progressive-delivery]], and in-production observation instead of expanding the suite.
- [[global-vs-local-optimization]] — local team decisions compose into global duplication, inconsistent choices, and forklift rewrites. Build cross-cutting forums without centralising decisions.
- [[cross-service-analytics]] — split databases break the assumption that everything is queryable from one schema. BI teams hit this first; the answer is usually a warehouse fed by CDC or event streams, not a cross-service join layer.
- [[monitoring-and-observability]] — monolith-era monitoring assumes binary failure; microservices need rich, queryable telemetry. See *moc-reliability-and-operations* when it lands.
- [[robustness-and-resiliency-at-scale]] — Newman's two-questions-per-call test: what happens if this call fails? what happens if it's slow? Isolation, [[timeouts]], [[circuit-breaker|circuit breakers]], [[bulkhead|bulkheads]]. Rare distributed failures become routine; harden against them before they become incidents.
- [[orphaned-services]] — services running for months untouched until no one knows what they do. Plan ownership *at creation time*, enforce periodic rediscovery, and name explicit retirement criteria.
- [[distributed-monolith]] — the organisation's path to this failure mode. The growing pains above are early-warning signs; ignore enough of them and the fleet converges on a distributed-monolith steady state.

Deeper reading: [[monolith-to-microservices#chapter-5-growing-pains]] is the full catalogue.

## Organisation and Conway — the fleet's shape follows the org's shape

Microservices is as much an organisational decision as a technical one. An architecture that cuts across the org chart will snap back; an org that tries to own a monolith as ten teams will produce a distributed monolith.

- [[conways-law]] — organisations ship their communication structure. The fleet's shape *will* match the teams' shape; the only question is whether that happens deliberately or by accident.
- [[communication-structures]] — Bellemare's three-structure refinement of Conway: business, implementation, and data communication structures. Most microservices pain traces to a weak data communication structure being silently handled by the implementation structure — which is why event streams as a first-class substrate matters.
- [[team-autonomy]] — the cheaper alternative to full microservices; two-pizza teams, Gore's 150-person units, Timpson's two-rule empowerment. Every microservices case study leans on team autonomy; try autonomy first without the architectural commitment.
- [[reorganizing-teams]] — moving from competency silos to product teams; the org change that usually must come *with* the architectural change. Newman's warning against copying the Spotify model verbatim.
- [[microservice-to-team-assignment]] (re-cited) — how services are parcelled across teams; the handoff points determine whether independence survives contact with reality.
- [[kotters-change-model]] — eight-step change model applied to microservice adoption. Most migrations die of change-management failure, not technical failure.
- [[technical-vs-domain-partitioning]] — the partitioning axis that decides whether the team map aligns with the service map. Technical partitioning smears every business change across layers; domain partitioning keeps one change in one team. Microservices presupposes domain partitioning.

See also [[moc-domain-driven-design]] for the modelling discipline that turns "domain-aligned" from an aspiration into a workable team-and-service map; [[moc-decomposition]]'s *Organisational pressure* section for the extraction-era framing.

## Sibling MOCs

Once the corresponding MOCs land, the handoffs below become wikilinks. For now they're plain pointers to where the jurisdictional boundary sits.

- [[moc-architecture-fundamentals]] — owns characteristics, the quantum, fitness functions, trade-off discipline. This MOC's defining properties cash out as structural realisations of [[architecture-characteristics]]; read that MOC for the frame, then this one for the realisation.
- [[moc-architecture-styles]] — owns the catalogue of shapes. Microservices is one style in that catalogue; this MOC picks up where Chapter 17's star-rating scorecard leaves off, in depth on running the style rather than placing it.
- [[moc-components-and-partitioning]] — owns the coupling-cohesion-connascence measurement toolkit plus the granularity force diagram. This MOC reaches into that one for the measurements; that MOC is where the operational vocabulary lives.
- [[moc-decomposition]] — owns the monolith-extraction playbook (decision frame, extraction patterns, database decomposition, correctness, operational step-up). This MOC picks up *after* extraction — ongoing running of microservices once they exist.
- [[moc-domain-driven-design]] — owns the modelling discipline (bounded contexts, aggregates, ubiquitous language, event storming). This MOC names domain alignment as the second defining property; the DDD MOC owns the modelling craft that produces the boundaries.
- *moc-consistency-and-transactions* (forthcoming) — owns saga, outbox, distributed-transaction avoidance, eventual consistency. This MOC names cross-service correctness as a granularity smell and a data-ownership concern; the consistency MOC owns the deeper trade-offs.
- *moc-events-and-streaming* (forthcoming) — owns the event-driven architectural patterns (brokers, choreography, event design, schema evolution). This MOC cites event-driven microservices as the preferred communication default; the events MOC owns the full broker-plus-contracts story.
- *moc-container-and-serving-patterns* (forthcoming) — owns the container patterns (sidecar, ambassador, adapter, replicated services). This MOC cites them as the operational-reuse substrate; that MOC owns the patterns themselves in depth.
- *moc-reliability-and-operations* (forthcoming) — owns SLO/SLI/error-budget, observability, on-call, incident response. This MOC names the operational step-up as a gate; the reliability MOC is the playbook.
- *moc-data-models-and-storage* (forthcoming) — owns the target schema shape for owned-per-service data. This MOC enforces "own your own data" as a discipline; that MOC owns what the new per-service store should look like.

## Related pages

- [[index]]
- [[monolith-to-microservices]]
- [[building-event-driven-microservices]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
- [[microservices]]
- [[monolith]]
- [[modular-monolith]]
- [[distributed-monolith]]
- [[independent-deployability]]
- [[service-granularity]]
- [[data-ownership]]
- [[event-driven-microservices]]
- [[synchronous-microservices]]
- [[saga]]
- [[outbox-table-pattern]]
- [[reuse-patterns]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[microservice-tax]]
- [[conways-law]]
- [[communication-structures]]
