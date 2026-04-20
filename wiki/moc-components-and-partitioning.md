# MOC: Components and Partitioning

**Summary**: Entry point for the inside-the-box decisions that decide a system's modularity: what a component is, how to identify the right ones, the technical-vs-domain partitioning axis, the coupling-cohesion-connascence triad that measures whether the modularity is real, and the granularity forces that decide whether two components belong in the same deployment unit. Start here when the question is "where should the boundaries go?" rather than "which style should this system be?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You're staring at a candidate seam — between two layers, two services, two teams, two databases — and you need a principled way to decide whether to keep them together or pull them apart. Or you've inherited a system whose components feel arbitrary and you want to know whether they actually are. Or you're sizing a microservice and want to ground "how big is too big?" in something more durable than instinct.

This MOC is the inside-the-box counterpart to [[moc-architecture-styles]]. The styles MOC tells you the *shape* of the box; this one tells you what goes in the box and where the lines run between things inside it. The decomposition MOC ([[moc-decomposition]]) operates *on* the boundaries this MOC tells you how to find.

The canonical shape of a question that lands here: *"How do I decide where to draw the component boundaries?"*, *"This service is doing too much / too little — how do I know?"*, *"What should the metric be when I argue this code shouldn't be in this module?"*, *"How do I tell whether the partitioning we have is technical or domain?"* The answer is rarely a pattern — it's a measurement plus a force diagram.

## Components — the architect's unit of design

Before partitioning anything, get clear on what the unit being partitioned actually is.

- [[components]] — the hub: the *physical packaging of modules* (libraries / layers / services); the architect's primary unit of design; the abstraction that lets the same modular structure be deployed as a monolith, a service-based architecture, or a microservice swarm without changing the *components* themselves. Read this first — most "is this a service or a module?" arguments are arguments about packaging, not about boundaries.
- [[component-identification-cycle]] — the five-step iterative loop (identify initial components → assign requirements → analyse roles and responsibilities → analyse architecture characteristics → restructure). The page worth memorising is *step 4*: characteristics analysis is what turns an apparently-monolithic design into a distributed one when one component needs different reliability or scalability than the rest. Most premature distribution comes from skipping this step.
- [[entity-trap]] — the named anti-pattern: one *Manager-per-database-entity* component (CustomerManager, OrderManager, ProductManager); ORM in architectural clothing; produces a system whose components track the schema rather than the workflow. Naked Objects and Rails are the legitimate alternative when you genuinely *do* want one-component-per-entity. Most internal complaints that "the architecture is just CRUD" are this anti-pattern.

Deeper reading: [[fundamentals-of-software-architecture#chapter-8-component-based-thinking]].

## The top-level partitioning axis: technical vs domain

The first decision that shapes every component below: do components group by *technical role* (presentation / business / persistence) or by *business domain* (Catalog / Checkout / Shipping)? This decision propagates everywhere.

- [[technical-vs-domain-partitioning]] — the top-level partitioning axis; the *CatalogCheckout change-smear* worked example showing how a technical partitioning forces a single business change across every layer; the trade-offs (technical: better separation of concerns, easier reuse of layers; domain: better team alignment, smaller change blast-radius); the *Inverse Conway Maneuver* as the recommendation when you want domain partitioning but the org is structured technically; the industry drift toward domain partitioning in recent decades. Read this *before* picking an architecture style — most styles in [[moc-architecture-styles]] presuppose one or the other.

The partitioning axis is the row in [[architecture-style-comparison]]'s structural-shape table. Layered, pipeline, and most monolithic styles are technically partitioned by default; modular monolith, service-based, microservices, and (uniquely) microkernel are domain-partitioned. Event-driven and space-based can be either depending on how processors are sliced.

## The measurement triad: cohesion, coupling, connascence

Modularity is the implicit characteristic — it doesn't appear on a requirements doc, it appears in everyone's velocity decay over time. The three measurement tools below are how you stop it from being aesthetic and start treating it as engineering.

- [[modularity]] — Richards and Ford's umbrella: the logical grouping of related code; the *implicit characteristic*; the three measurement tools introduced and contrasted. Read this first; the rest of this section assumes its framing.
- [[cohesion]] — *the code that changes together stays together*; Constantine's seven-level scale (functional → coincidental); LCOM as the structural metric; the business-cohesion vs technology-cohesion distinction. Cohesion is the *internal* virtue — it scores how tightly the things inside one component belong together.
- [[coupling]] — Newman's four types (implementation, temporal, deployment, domain) plus the Structured Design afferent/efferent axes. Coupling is the *boundary* property — it scores how much one component depends on the internals of another. Implementation coupling is the one extraction actually removes; the others travel with you.
- [[coupling-metrics]] — afferent (Ca) and efferent (Ce) coupling; Robert Martin's *abstractness*, *instability* (I = Ce / (Ce + Ca)), and *distance from the main sequence* (D = |A + I − 1|). The metrics that turn coupling from intuition into a build-failable rule.
- [[connascence]] — Page-Jones's framework: five static types (name, type, meaning, position, algorithm), four dynamic types (execution, timing, value, identity); three properties (strength, locality, degree). The most precise vocabulary the wiki has for *what kind* of coupling exists between two components — and the only one that distinguishes static from dynamic coupling at the implementation level.
- [[information-hiding]] — Parnas's principle: stable interfaces hide what changes; the *engine of independent deployability*. Cited here because hiding-information *across* a component boundary is the discipline that turns a candidate boundary into a real one. Most leaky boundaries fail this test.

Deeper reading: [[fundamentals-of-software-architecture#chapter-3-modularity]].

## Granularity — how big should one component be?

Granularity is the question that combines partitioning with characteristics: which forces *pull components apart* into smaller deployment units, and which forces *push them together* into larger ones?

### The architectural-modularity frame

- [[architectural-modularity]] — *Hard Parts*'s degree-of-decomposition concept; the five-driver rubric for *whether* a system needs more deployment units (maintainability, testability, deployability, scalability, fault tolerance). The *yes you should split* rubric.
- [[agility]] — *Hard Parts*'s compound characteristic: agility = maintainability + testability + deployability. Cited explicitly because the agility argument is the one most often offered for splitting (and the one most often misused — agility *can* improve with smaller deployment units, but only if testability and deployability genuinely improve, not just the deploy *cadence*).
- [[testability]] — ease + completeness of testing; the *chatter* failure mode; consumer-driven contracts as the preserver. A small service with poor test discipline is no more testable than a large one.
- [[deployability]] — ease + frequency + risk of deployment; Matt Stine's *big ball of distributed mud* warning. The single characteristic most often overestimated when teams reach for microservices.

### The disintegrator/integrator force diagram

- [[granularity-disintegrators]] — *Hard Parts*'s six forces *pulling services apart*: scope and function, code volatility, scalability and throughput, fault tolerance, security, extensibility. The vocabulary for "why we should split this further."
- [[granularity-integrators]] — *Hard Parts*'s four forces *keeping services together*: database transactions, workflow and choreography, shared code, data relationships. The vocabulary for "no, that split would cost more than it would save."
- [[code-volatility]] — change-rate as an objective, measurable decomposition driver. The single most underused signal — components that change together belong together; components on wildly different change rates probably don't.
- [[service-granularity]] — the canonical microservices-fundamentals page; *the hardest decision in microservices and the dividing axis across Part II styles*; the three Chapter-17 guidelines (purpose, transactions, choreography); the *fix granularity, not transactions* maxim. The right answer to "our distributed transactions are painful" is almost always "you split too small," not "let's add a 2PC coordinator."

Deeper reading: [[software-architecture-the-hard-parts]] (Chapters 3 and 7) for the architectural-modularity rubric and the granularity drivers/integrators side-by-side; [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]] for service-granularity within the microservices style.

## Coupling, deeper — the *Hard Parts* framework

Newman's four-coupling-type framework (under [[coupling]]) is the operational vocabulary; the *Hard Parts* coupling axes below are the analytical framework. Use them together — Newman tells you what kind of coupling you have, *Hard Parts* tells you what to do about it.

- [[static-coupling]] — *how the quanta are wired together*: dependencies, contracts, topology. Measured via the *bootstrap test* — what does this quantum need to start? The static side of the architectural-quantum analysis.
- [[dynamic-coupling]] — runtime coupling along three axes: *communication* (sync / async) × *consistency* (atomic / eventual) × *coordination* (orchestrated / choreographed). The triple that produces the eight transactional-saga shapes catalogued in [[moc-consistency-and-transactions]] and shows up implicitly in every distributed style on [[moc-architecture-styles]].
- [[semantic-coupling]] — domain-concept coupling inherent in the workflow itself; the *floor* implementation can only worsen, never go below. The argument-stopper for "let me just refactor the boundaries one more time" — sometimes the boundary is doing the best it can given the domain.
- [[stamp-coupling]] — passing whole structures when only a subset is needed; GraphQL and field-mask APIs as the counter-pattern. The bandwidth-fallacy ([[fallacies-of-distributed-computing]]) version of "your services are a bit too chatty."
- [[orthogonal-coupling]] — distinct-purposes-that-must-intersect; sidecars and service meshes as the cleanest implementation. The right model for cross-cutting concerns (security, telemetry, rate limiting) layered orthogonally on top of any partitioning scheme.

## Decomposition patterns — *Hard Parts*'s six-step playbook

Once you've decided to decompose a monolith into components, *Hard Parts* gives a sequenced six-pattern playbook. This sequence operates at the *component* level inside the monolith — getting it into shape *before* extracting any component into its own service.

- [[component-based-decomposition]] — the hub: six-pattern sequence; the preferred approach when a monolith is decomposable (and an explicit fallback when it isn't).
- [[big-ball-of-mud]] — Foote's 1999 antipattern; the decomposability gate. If you're past this, the pattern sequence below applies; if you're not, jump to [[tactical-forking]].
- [[tactical-forking]] — De La Torre's *clone-then-delete* pattern: copy the whole monolith, delete what each fork doesn't need; coarse-grained services from coupled code. The escape hatch when the monolith is too tangled for ordered decomposition.
- [[identify-and-size-components-pattern]] — pattern 1: inventory every component; statements metric; standard-deviation balance rule that flags suspiciously-large or suspiciously-small components.
- [[gather-common-domain-components-pattern]] — pattern 2: consolidate cross-cutting domain logic; the *leaf-name* heuristic; the shared-component-vs-shared-library decision.
- [[flatten-components-pattern]] — pattern 3: leaf-node definition; eliminate orphaned classes; push-down vs pull-up flattening to fix accidental component nesting.
- [[determine-component-dependencies-pattern]] — pattern 4: component-level Ca/Ce; the *golfball / basketball / airliner* triage (small, medium, terrifying coupling fan-outs); ArchUnit enforcement to keep the triage durable as the codebase changes.
- [[create-component-domains-pattern]] — pattern 5: namespace-prefix domains; one-to-many service-to-components mapping that becomes the candidate-service map for the next pattern.
- [[create-domain-services-pattern]] — pattern 6: physical extraction to a service-based architecture; the *soft landing* before microservices, not a leap straight to them. Stop here unless an explicit force (granularity-disintegrators) says further extraction will pay off.

For *what to do after* the components are extracted into services — extraction patterns, database decomposition, correctness across the split — see [[moc-decomposition]].

## Sibling MOCs

- [[moc-architecture-fundamentals]] — owns characteristics (including modularity as the implicit one), the quantum, fitness functions, ADRs. This MOC's coupling-and-cohesion measurements operationalise the modularity characteristic introduced there.
- [[moc-architecture-styles]] — owns the catalogue of canonical shapes. The partitioning axis on this MOC is the structural-shape row of every style on that MOC; the granularity material here decides where to land within a chosen style.
- [[moc-risk-and-communication]] — owns risk surfacing, diagramming, and the architect-soft-skills view. Component-boundary fights are the most common architect-developer disagreements; the negotiation and guidance pages there are the practical complements to this MOC's frameworks.
- [[moc-decomposition]] — owns the monolith-extraction playbook *after* component decomposition. This MOC takes you to "we have well-defined components and an extraction candidate"; that MOC takes the candidate the rest of the way to a running, owned, observable service.
- [[moc-microservices]] — owns the running-microservices view (independence, ownership, organisation, scaling, scale-out failure modes). [[service-granularity]] sits on the boundary; this MOC carries the granularity decision; that MOC carries what you live with afterwards.
- [[moc-domain-driven-design]] — owns the modelling discipline (bounded contexts, aggregates, ubiquitous language). Domain partitioning on this MOC presupposes DDD; the DDD MOC owns the modelling craft that produces the domain boundaries this MOC measures.
- [[moc-consistency-and-transactions]] — owns saga, outbox, and the correctness-across-stores story. The dynamic-coupling triple on this MOC is the same triple that produces the eight saga shapes there.

## Related pages

- [[index]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
- [[components]]
- [[component-identification-cycle]]
- [[technical-vs-domain-partitioning]]
- [[modularity]]
- [[cohesion]]
- [[coupling]]
- [[connascence]]
- [[information-hiding]]
- [[architectural-modularity]]
- [[granularity-disintegrators]]
- [[granularity-integrators]]
- [[service-granularity]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[component-based-decomposition]]
