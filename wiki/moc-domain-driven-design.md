# MOC: Domain-Driven Design

**Summary**: Entry point for the modelling discipline that turns "what does the business actually do?" into a boundary map the architecture can be built on. Covers the core DDD vocabulary (domain, subdomain, bounded context, aggregate, ubiquitous language), the collaborative techniques for discovering them (event storming, workflow analysis), the architectural consequences (domain partitioning, alignment on business requirements not technical ones), and the DDD-to-implementation bridge into microservices, data ownership, and event-driven systems. Start here when the question is *"where should the domain boundaries go and how do we find them?"* rather than *"which pattern do I apply?"*

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You are about to draw a line between one service and another — or one team and another, or one database schema and another — and you want that line grounded in the domain rather than in the current code's accidental shape. Or you've inherited a system whose boundaries feel arbitrary and you suspect they are. Or you're trying to find the right starting unit for a decomposition and the options all look plausible.

This MOC is the modelling layer that *other* MOCs borrow from. [[moc-decomposition]] reaches in for [[bounded-context]] and [[aggregate]] as seam-finding tools. [[moc-microservices]] reaches in because "modelled around a business domain" is one of its three defining properties. [[moc-components-and-partitioning]] reaches in because the technical-vs-domain partitioning choice is the outermost decision that every component decision then hangs off. This MOC owns the modelling craft itself — the thing all three of those MOCs depend on and would rather not duplicate.

The canonical shape of a question that lands here: *"How do we find the right boundaries?"*, *"What is a bounded context, really?"*, *"We tried to split this and the seams keep re-coupling — why?"*, *"Our architecture tracks the database schema — is that a problem?"* (yes — see [[entity-trap]]), *"How much modelling is enough before we start cutting?"* The answer is almost always a technique plus a vocabulary, not a pattern.

## The core vocabulary

Before anything else, get the four words straight. Most DDD arguments are arguments about which word applies to which thing.

- [[domain-driven-design]] — the hub: Eric Evans's 2004 discipline; Newman's two-concept distillation (aggregate + bounded context) for microservices; Bellemare's crisp four-term vocabulary. The page worth reading first if the distinction between *domain*, *subdomain*, *domain model*, and *bounded context* isn't second-nature.
- [[bounded-context]] — the larger organisational boundary within which explicit responsibilities are carried out and implementation details are hidden. Newman's canonical example is the warehouse vs finance at Music Corp. A bounded context contains one or more aggregates and exposes a deliberate interface to outside contexts. The natural starting unit for drawing a service boundary.
- [[aggregate]] — the self-contained domain entity with a life cycle — typically a state machine — that decides for itself whether to allow a state transition. *If an outside party requests a transition, the aggregate can say no.* Order, Invoice, Stock Item are canonical aggregates. The finer-grained unit sitting inside a bounded context.
- [[entity-event]] — Bellemare's keyed-on-entity-id event type. Entity events are the implementation of an aggregate's state transitions on an event stream; the latest entity event per key *is* the current state. The bridge between DDD's aggregate concept and the event-log substrate of [[event-driven-microservices]].

The one-line relationship: *the domain is the problem space; a bounded context is a region of the solution space; aggregates are the self-governing units inside a bounded context; entity events are how aggregates' state transitions become durable facts for the rest of the organisation to consume.*

Deeper reading: [[monolith-to-microservices#chapter-1-just-enough-microservices]] for Newman's distillation; [[building-event-driven-microservices#chapter-1-why-event-driven-microservices]] for Bellemare's crisper restatement.

## Ubiquitous language — the unglamorous load-bearing discipline

DDD's load-bearing idea, half-hidden behind the glamorous patterns, is that the business and the code should speak the same words. Every place the business's language leaks out of the code is where the next bug, the next misunderstanding, and the next rewrite starts.

The wiki does not (yet) carry a dedicated `ubiquitous-language` concept page — when a ubiquitous-language question lands here, frame from the following proxies until the gap is filled:

- [[bounded-context]] — ubiquitous language is *bounded by context*. The word "customer" in the Sales context and the word "customer" in the Fulfilment context can legitimately mean different things. Forcing them to share one canonical definition is the [[orchestration-driven-soa]] failure mode; letting them drift inside clear context boundaries is the DDD recommendation.
- [[entity-trap]] — the symptom of a language failure. When the architecture reads like a list of database tables ("CustomerManager", "OrderManager", "InvoiceManager"), the language has collapsed into the database's noun list and the domain's verbs have disappeared. See the *correct response* section on that page.
- [[information-hiding]] — Parnas's principle, which DDD's context boundaries are an organisational realisation of. The ubiquitous language inside a context is the context's internal vocabulary; outsiders only see the published interface.

When a dedicated *ubiquitous-language* page lands in the wiki, it slots in here. Treat this section as a placeholder with the cross-links that currently carry the load.

## The workshop techniques — how to discover the model

DDD is collaborative or it fails. The model the architect draws alone will miss the rules the business actually runs on. The techniques below are how you surface those rules in a room with the people who actually know them.

- [[event-storming]] — Brandolini's collaborative workshop: participants brainstorm *domain events* on sticky notes, group them into *aggregates*, group those into *bounded contexts*. Bottom-up; event-first; the single best format the wiki covers for producing a domain model with non-developer colleagues in the room. Works both as Newman's migration-prioritisation tool and as Richards and Ford's Chapter 8 component-discovery technique — same exercise, adjacent problems.
- [[component-identification-cycle]] — Richards and Ford's five-step iterative loop for turning domain discoveries into components. Step 4 (*analyse architecture characteristics*) is where most technical-partitioning mistakes happen and where domain partitioning earns its keep.
- [[extraction-prioritization]] — the two-axis model (effort vs. benefit) that turns a bounded-context map into a ranked migration sequence. Inbound dependency count from the map is a rough but useful proxy for extraction effort.

The three alternatives Richards and Ford offer under [[component-identification-cycle]]/Chapter 8 — *actor/actions*, *event storming*, *workflow analysis* — cover a spectrum. Event storming is the DDD-native default; workflow analysis is the middle ground when the system genuinely isn't message-driven; actor/actions is the generic option when neither fits.

Deeper reading: [[monolith-to-microservices#chapter-2-planning-a-migration]] for Newman's event-storming-plus-prioritisation pattern; [[fundamentals-of-software-architecture#chapter-8-component-based-thinking]] for the three-technique catalogue.

## How much modelling is enough?

DDD has a reputation for demanding a vast up-front model; the practitioners cited in the wiki push back hard on that. You don't need a detailed model of the whole system to start — you need *enough* information to make a reasonable decision about where to cut next.

- [[extraction-prioritization]] (re-cited) — Newman's anti-perfectionist position. A high-level bounded-context map plus deeper analysis only on the parts you're considering extracting first is fine. Deeper analysis is a cost; spend it where it will change a decision.
- [[cost-of-change]] — push experiments hard on the whiteboard *before* committing code. The bill comes due during database decomposition, so cheap remodelling is high-leverage.
- [[reversible-vs-irreversible-decisions]] — bounded-context boundaries are relatively reversible on the whiteboard; they become hard to reverse once they're enshrined in a database schema or service contract. Delay the irreversible move as long as the model is still shifting.

The model is a living artefact, not a one-shot deliverable. Revisit it as you learn — every extraction teaches you something about the next.

## The architectural consequence — domain partitioning

DDD's operational consequence, at the architecture level, is that components are organised *by business domain*, not by technical layer. This is the outermost decision that every later component decision hangs off.

- [[technical-vs-domain-partitioning]] — the top-level partitioning axis. The *CatalogCheckout change-smear* worked example: in a technically-partitioned system, adding a checkout feature touches four layers; in a domain-partitioned system, the same change lands inside one component. The industry drift over the last decade has been toward domain partitioning; DDD is the intellectual framework that explains why.
- [[conways-law]] — the organisational complement. The fleet's shape follows the team structure; domain partitioning presupposes cross-functional product teams, not tech-skill silos. See [[moc-microservices]]' organisation section for the team shape.
- [[communication-structures]] — Bellemare's three-structure refinement of Conway: business, implementation, and data. His business-requirement-alignment rule on [[bounded-context]] is the DDD injection into this frame — align bounded contexts with business requirements, *not* with technical systems; business requirements change at the same pace as the implementation boundary needs to move.
- [[entity-trap]] — the anti-pattern DDD is designed to prevent. One `*Manager` component per database entity; verbs collapsed to CRUD, domain logic homeless. The test: if the application genuinely is thin-UI-over-entities, use a framework like Naked Objects or Rails scaffolding — don't call entity-CRUD an architecture.

Deeper reading: [[fundamentals-of-software-architecture#chapter-8-component-based-thinking]] for the technical-vs-domain axis and the entity trap; [[building-event-driven-microservices#chapter-1-why-event-driven-microservices]] for the "align on business requirements" principle as it lands in event-driven systems.

## The microservices bridge — from model to service map

The most-cited DDD-to-architecture transition in the wiki is the one that turns bounded contexts and aggregates into microservice boundaries. This section is the bridge; for the running-the-services material itself, go to [[moc-microservices]].

- [[microservices]] — the destination. Newman's three defining properties include "modelled around a business domain" as the second, and DDD is Newman's recommended means for finding those boundaries. Richards and Ford's Chapter 17 goes further — microservices are *the physical embodiment of bounded contexts*, full stop.
- [[architectural-quantum]] — the DDD-to-deployment bridge. The bounded context is a *logical* boundary; the architecture quantum is a *physical* one. In a well-designed microservices architecture the two align: one bounded context, one quantum, one service plus its own database. The alignment is not automatic — a bounded context that depends synchronously on a data store owned by another context collapses both into a single quantum regardless of their logical separation.
- [[bounded-context]] (re-cited) — Newman's migration recommendation: start with services that encompass entire bounded contexts (coarse-grained), and decompose along aggregate boundaries later if scaling pressure demands it. Do not split along aggregate lines on day one; you will discover your aggregate boundaries are wrong and pay for the mistake twice.
- [[event-driven-microservices]] — Bellemare's style of microservices whose cross-boundary communication is durable events rather than synchronous API calls. Built directly on the two DDD load-bearing properties: bounded contexts should be highly cohesive (minimise cross-boundary chatter) and loosely coupled (change in one minimises impact on neighbours). Events are the mechanism.
- [[entity-event]] (re-cited) — the aggregate-to-event-stream bridge. An aggregate's state transitions become a stream of entity events keyed on the aggregate's identifier; [[table-stream-duality]] then lets any other bounded context materialise a read-only projection of that state in its own store without coupling to the owning service's runtime.

See [[moc-microservices]] for everything that follows service-map discovery — ownership, independence, reuse, granularity, platform.

## Data ownership and bounded contexts

DDD modelling is incomplete if it stops at *components*; *Hard Parts* reconciles the application-architect and data-architect views by extending the bounded-context idea onto the data side.

- [[data-domain]] — *Hard Parts* Chapter 6's data-architect unit: a collection of coupled database artifacts (tables, views, foreign keys, triggers) within a limited functional scope. Ideally one bounded context maps to one data domain. The alignment is what lets per-service [[data-ownership]] actually work.
- [[data-ownership]] — the writer-owns-the-table rule. Assigns tables to services based on who writes them; keeps writes aligned with the owning bounded context. The three ownership scenarios (single / common / joint) all presuppose a clear bounded-context map.
- [[database-per-bounded-context]] — a concrete halfway house: each bounded context gets its own schema inside a modular monolith. Buys most of the data-decoupling benefit at a fraction of the cost of extraction.
- [[repository-per-bounded-context]] — the data-access-layer equivalent: each bounded context owns its own repository abstractions. A useful refactor inside the monolith to make later extraction cheaper.
- [[aggregate-exposing-monolith]] — the extraction-era pattern: expose aggregates owned by the monolith via a proper API endpoint so new services don't reach into the old schema. Inverts the dependency direction without yet moving the data.

For the deeper correctness-across-contexts material — sagas, outbox, distributed transactions, eventual consistency — see [[moc-consistency-and-transactions]]. For the full database decomposition playbook see [[moc-decomposition]]'s database section.

## When DDD isn't a fit

DDD is not universally applicable. The techniques cost real time; the vocabulary adds cognitive overhead; the modelling discipline only pays off when the domain is genuinely the hardest part.

- [[when-microservices-are-a-bad-idea]] — the microservices-adjacent version of the same caution. Unclear domains, true startups, and customer-installed software are the cases where DDD-driven decomposition is premature. Newman's reasoning applies to the modelling discipline too: if you don't yet know what the domain *is*, you can't model it.
- [[modular-monolith]] — the lighter-weight destination for DDD modelling when distribution isn't needed. A well-modularised monolith informed by bounded contexts gets you most of the domain-alignment benefit without the microservices tax. Newman cites this as the cheaper alternative throughout.
- [[entity-trap]] (re-cited) — the inverse risk. If the application really is entity-CRUD, don't invent domain structure where none exists; use the frameworks built for that shape.

Deeper reading: [[monolith-to-microservices#chapter-2-planning-a-migration]] for Newman's *"you don't need a detailed domain model of the entire system to start"* framing.

## Sibling MOCs

- [[moc-architecture-fundamentals]] — owns characteristics, the quantum, fitness functions, trade-off discipline. This MOC supplies the *domain alignment* input that Chapter 5's *identifying architectural characteristics* cycle depends on; that MOC supplies the frame this modelling work is scored against.
- [[moc-components-and-partitioning]] — owns the inside-the-box coupling-cohesion-connascence toolkit plus the technical-vs-domain partitioning axis. This MOC produces the *domain* partitioning; that MOC operationalises it with measurement.
- [[moc-architecture-styles]] — owns the catalogue of shapes. Several styles ([[modular-monolith]], [[service-based-architecture]], [[microservices]], [[event-driven-architecture]]) presuppose domain partitioning; this MOC owns the modelling that makes them possible.
- [[moc-decomposition]] — owns the monolith-extraction playbook. This MOC supplies the domain seams (*where*); that MOC owns the mechanics of pulling a service out (*how*) and the database untangling that follows.
- [[moc-microservices]] — owns the running-microservices view. This MOC owns the modelling that produces the service map; that MOC owns what happens after the services exist.
- [[moc-events-and-streaming]] — owns the event-driven architectural patterns. This MOC's entity-event framing is the DDD-to-stream bridge; that MOC owns the broker, schema-evolution, and workflow choreography patterns built on top.
- [[moc-data-models-and-storage]] — owns the target schema shape inside a bounded context. This MOC aligns bounded contexts with data domains; that MOC owns what the per-context schema should look like.
- [[moc-consistency-and-transactions]] — owns saga, outbox, and cross-context correctness. This MOC draws the boundaries; that MOC owns what to do when a workflow has to cross them.

## Related pages

- [[index]]
- [[monolith-to-microservices]]
- [[fundamentals-of-software-architecture]]
- [[building-event-driven-microservices]]
- [[software-architecture-the-hard-parts]]
- [[domain-driven-design]]
- [[bounded-context]]
- [[aggregate]]
- [[event-storming]]
- [[entity-event]]
- [[entity-trap]]
- [[technical-vs-domain-partitioning]]
- [[information-hiding]]
- [[communication-structures]]
- [[data-domain]]
- [[architectural-quantum]]
- [[microservices]]
- [[modular-monolith]]
- [[event-driven-microservices]]
- [[extraction-prioritization]]
