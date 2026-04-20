# MOC: Architecture Styles

**Summary**: The catalogue of canonical architecture styles — what each one *is*, where each one wins and loses, and how to choose between them. Start here when the question is "what shape should this system be?" and you need a navigable map of the eight or so canonical answers before reaching for one.

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You are picking a style for a green-field system, evaluating whether the style you're already on is still the right one, or trying to make sense of a system whose shape you can't quite name. This MOC is the catalogue plus the comparison plus the choice frame.

The canonical shape of a question that lands here: *"Which architecture style fits this domain?"*, *"What do I actually buy and pay by going from a layered monolith to event-driven microservices?"*, *"What's the cheapest distributed style?"*, *"Why does everyone seem to skip orchestration-driven SOA on the way from layered to microservices?"* The answer is rarely a single style — it's a comparison plus a few characteristics scored as the swing votes.

Before reaching for any style on this page, calibrate from [[moc-architecture-fundamentals]]: characteristics ([[architecture-characteristics]]), the quantum ([[architectural-quantum]]), trade-off discipline ([[trade-off-analysis]] / [[least-worst-trade-offs]]). The style is the *answer*; without those frames, you don't yet have the question.

## The top-level fork: monolithic vs distributed

Every Part II style hangs off this distinction. Distribution is what most of the operational pain comes from; choose against it when you can.

- [[monolithic-vs-distributed]] — the structural split for every later style; what distribution buys (independent scaling, fault isolation, polyglot freedom, team autonomy) versus what it costs (latency, partial failure, network as fault domain, operational step-up); the relationship to partitioning and the [[architectural-quantum]]. Read this *before* choosing a style — it tells you which half of the catalogue to even look at.
- [[fallacies-of-distributed-computing]] — Deutsch's 1994 eight fallacies (the network is reliable, latency is zero, bandwidth is infinite, the network is secure, topology doesn't change, there is one administrator, transport cost is zero, the network is homogeneous); architect-facing summary with cross-links to *DDIA*; [[stamp-coupling]] and the bandwidth fallacy worked together. Distribution doesn't repeal these; *every* distributed style on this page pays them.

If the choice is genuinely close, default monolithic — distribution is a one-way door priced in operational complexity for the system's lifetime, not just its launch quarter.

Deeper reading: [[fundamentals-of-software-architecture#chapter-9-foundations]].

## The monolithic styles

These are the cheap, fast-to-ship, easy-to-reason-about styles. None of them score five stars on operational characteristics; all of them score well on simplicity and cost. Most systems should start here and move only when an actual force ([[granularity-disintegrators]]) demands it.

### Layered (n-tier) — the default monolith

- [[layered-architecture]] — the n-tier default; closed vs open layers and *layers of isolation* as the discipline that keeps the layering from collapsing; the *sinkhole* anti-pattern with the 80-20 rule (when 80%+ of requests pass straight through a layer untouched, you have a sinkhole, not a layer); characteristics scorecard with cost and simplicity maxed and operational ratings (deployability, scalability, fault tolerance, elasticity) all low. The *technically partitioned*, single-quantum default — and the right choice for many small-and-medium systems.

### Pipeline — Unix in architectural clothing

- [[pipeline-architecture]] — pipes-and-filters; the four filter types (producer, transformer, tester, consumer); Unix shells, ETL, Apache Camel, MapReduce as the lineage; *technically partitioned* and *single-quantum*. Slightly better modularity, deployability, and testability than layered at the same operational ceilings — because filter boundaries are sharper than layer boundaries. Pick over layered when the workload is naturally a chain of transformations.

### Microkernel — the plug-in style

- [[microkernel-architecture]] — Eclipse, Jira, browsers, tax-prep, claims-processing; minimal core + independent plug-in components communicating through a registry and standard contracts; the *only* Part II style that is both technically *and* domain partitioned (core technical, plug-ins domain); single quantum even when plug-ins are deployed remotely, because of synchronous coupling. Pick when the system has a stable core and an open-ended set of independently-developed extensions.

For the data-modelling and integration counterparts to these styles, see [[moc-data-models-and-storage]] and [[moc-data-engineering]].

## The distributed styles

The point at which distribution starts paying for itself. Operational complexity goes up sharply; reliability, scalability, performance, and elasticity start being negotiable rather than capped by hardware.

### Service-based — the pragmatic distributed sweet spot

- [[service-based-architecture]] — separately deployed UI + 4–12 coarse-grained domain services + *shared monolithic database*; ACID transactions preserved by virtue of the shared DB; no five-star ratings but many four-star ones; federated shared-entity libraries to contain schema-change blast radius. The cheapest and simplest distributed style — and the one with the best risk/reward profile when full microservices are too much.

If you've been told *"we want microservices"* and the actual force is *"we want independent deploys for the UI and a few backend domains"*, this is almost certainly the right answer. The shared database is a feature here, not a bug.

### Event-driven — the asynchronous distributed style

- [[event-driven-architecture]] — distributed asynchronous style built around decoupled event processors; five stars on performance, scalability, elasticity, fault tolerance; two canonical topologies (broker and mediator); often *embedded inside other styles* (event-driven microservices, event-driven space-based) rather than adopted neat.
- [[broker-topology]] — peer-to-peer pub/sub; no central mediator; past-tense-fact events; relay-race handoff; architectural extensibility as the killer feature. Equivalent to Newman's *choreographed saga*.
- [[mediator-topology]] — central mediator with point-to-point command queues; explicit workflow control; error handling has a home; recoverability is straightforward. Apache Camel / Mule / BPEL / jBPM by complexity tier. Equivalent to Newman's *orchestrated saga*.

The choice between broker and mediator is the same trade-off as the saga choreography-vs-orchestration choice — both pages cite the same underlying axes. For the deeper saga material see [[moc-consistency-and-transactions]] and [[moc-events-and-streaming]].

Deeper reading: [[fundamentals-of-software-architecture#chapter-14-event-driven-architecture-style]].

### Space-based — the burst-workload style

- [[space-based-architecture]] — tuple-space-inspired; *removes the database from the synchronous request path*; processing units + replicated in-memory data grid + asynchronous data pumps; five stars on elasticity, scalability, performance; one star on simplicity, testability, cost. The ticketing / auction / booking burst-workload style; hybrid cloud-plus-on-prem deployment as a distinctive option.
- [[processing-unit]] — SBA's compute-and-cache unit: application code + in-memory replicated data grid (Hazelcast / Ignite / Coherence); dynamically scaled; named-cache member lists track scaling automatically; three startup paths (hot / cold / archive).
- [[data-pump]] — SBA's asynchronous one-way messaging conduit from processing units to the database; the *eventual-consistency-by-construction* mechanism that keeps the request path DB-free; per-cache vs per-domain granularity; reverse data pumps for cold-start cache hydration.

Pick this *only* when burst workloads are the dominant force. The five-star characteristics come at a real cost in development complexity; smaller workloads pay the cost without buying the benefit.

Deeper reading: [[fundamentals-of-software-architecture#chapter-15-space-based-architecture-style]].

### Orchestration-driven SOA — the cautionary tale

- [[orchestration-driven-soa]] — the historical 2000s enterprise SOA: four-layer service taxonomy (business / enterprise / application / infrastructure) stitched together by a central ESB; the *reuse-through-orchestration* thesis that didn't deliver; one-star ratings on deployability, testability, performance, simplicity, and cost; single quantum despite being distributed (everything synchronously couples through the ESB). The architecture microservices is a direct backlash against.

Included here because the failure modes echo into modern designs. *Hard Parts*'s reuse warnings (see [[moc-microservices]]) are essentially the lessons learned from this style's collapse.

### Microservices — the polished distributed default

- [[microservices]] — independently deployable services modelled around a business domain, owning their own data; Richards and Ford's star-rating scorecard; the duplication-over-coupling philosophy as the deliberate inversion of the orchestration-driven-SOA reuse thesis; SOA-negation placement in the catalogue; operational-reuse-via-sidecars as the *Hard Parts* refinement.

Microservices is catalogued in depth in [[moc-microservices]]. This MOC carries its style-level placement and characteristics scorecard; that MOC will carry the running-the-services material.

Deeper reading: [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]].

## Choosing among them

The catalogue is only useful if you have a method for picking. Chapter 18 is the canonical procedure; the comparison page is the side-by-side scorecard.

- [[choosing-architecture-style]] — Chapter 18's selection process: six inputs (domain, characteristics, data, organisation, process, domain-architecture isomorphism), three decisions (monolith-vs-distributed via quantum analysis; data placement; sync-by-default communication), three deliverables (topology, ADRs, fitness functions). Catalogues *shifting architectural fashion* across six forces (Moore's law, network speed, cloud, microservice fashion, business agility, container ecosystem). Worked all the way to resolution on the *Silicon Sandwiches* and *Going, Going, Gone* katas.
- [[architecture-style-comparison]] — cross-cutting scorecard hub across all eight Part II styles: structural-shape table (partitioning, quantum, class), full scorecard on 15 characteristics, four scorecard *shapes* (cheap-low-ceiling, pragmatic middle, five-star-operational-costly, historical cautionary tale), and what the scorecard does *not* capture. The single highest-value side-by-side artefact for these styles.

The choice procedure leans on [[architectural-quantum]] from [[moc-architecture-fundamentals]] to make the monolith-vs-distributed call concrete. If the system has a single quantum, almost every distributed style is over-engineered for it; if it has many, the monolithic styles are under-engineered for it.

Deeper reading: [[fundamentals-of-software-architecture#chapter-18-choosing-the-appropriate-architecture-style]].

## Cross-style structural concepts

Some concepts slot across multiple styles and are easier to learn once than re-learn per style.

- [[architectural-quantum]] (re-cited) — the unit at which an architecture characteristic actually applies; layered = 1 quantum, microservices = many; the deciding analysis for monolith-vs-distributed.
- [[stamp-coupling]] — passing whole structures when only a subset is needed; GraphQL and field-mask approaches as the counter-pattern; the bandwidth-fallacy version of "your services are a bit too chatty."
- [[static-coupling]] vs [[dynamic-coupling]] — *Hard Parts*'s deeper coupling axes that cut across styles. Static coupling is "how the quanta are wired together"; dynamic coupling is the runtime triple of (sync/async × atomic/eventual × orchestrated/choreographed). Cited in this MOC because the dynamic-coupling triple is the same triple that distinguishes the eight saga shapes used by every distributed style on this page.
- [[semantic-coupling]] — the domain-concept coupling inherent in the workflow itself; the floor implementation can only worsen, never go below. Useful when the same workflow keeps re-coupling across redesigns.
- [[orthogonal-coupling]] — distinct-purposes-that-must-intersect; sidecars and meshes as the cleanest implementation. The right model for cross-cutting concerns (security, telemetry) layered on top of any of these styles.

For full coupling, cohesion, and modularity treatment, see [[moc-components-and-partitioning]].

## Sibling MOCs

- [[moc-architecture-fundamentals]] — owns characteristics, the quantum, fitness functions, trade-off discipline. This MOC's catalogue is meaningless without the *fundamentals* frame to score styles against.
- [[moc-components-and-partitioning]] — owns components, the technical-vs-domain partitioning axis, modularity, granularity drivers. The partitioning axis appears in every style's structural-shape row of the comparison scorecard.
- [[moc-risk-and-communication]] — owns the architect-soft-skills view. Style choices are typically the most contentious architectural decisions; the negotiation, diagramming, and risk-assessment skills determine whether the chosen style is adopted or quietly worked around.
- [[moc-decomposition]] — owns the monolith-extraction playbook. *Going from* one of this MOC's styles *to* another is what `moc-decomposition` covers in depth; this MOC covers *which destination is right* for the migration.
- [[moc-microservices]] — owns the running-microservices view (independence, ownership, organisation, scaling, scale-out failure modes). This MOC catalogues microservices as a style; that MOC owns the practice.
- [[moc-events-and-streaming]] — owns brokers, choreography, sagas, outbox, event design. This MOC catalogues event-driven architecture as a style; that MOC owns the patterns inside.
- [[moc-data-models-and-storage]] — owns the storage-shape decisions every style on this page implies (shared DB for service-based, per-service DB for microservices, in-memory grid for SBA). The data side is its own MOC because it cuts across all distributed styles.
- [[moc-reliability-and-operations]] — owns the SLO/SLI/error-budget, observability, and incident-response posture. The operational characteristics in [[architecture-style-comparison]]'s scorecard cash out as concrete practices in that MOC.

## Related pages

- [[index]]
- [[fundamentals-of-software-architecture]]
- [[monolithic-vs-distributed]]
- [[fallacies-of-distributed-computing]]
- [[layered-architecture]]
- [[pipeline-architecture]]
- [[microkernel-architecture]]
- [[service-based-architecture]]
- [[event-driven-architecture]]
- [[space-based-architecture]]
- [[orchestration-driven-soa]]
- [[microservices]]
- [[choosing-architecture-style]]
- [[architecture-style-comparison]]
