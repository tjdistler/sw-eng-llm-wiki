# Service-Based Architecture

**Summary**: A distributed architecture style that pairs a separately deployed **user interface**, a small number (4–12, usually ~7) of separately deployed **coarse-grained domain services**, and — most distinctively — a **single shared monolithic database**. Richards and Ford call it **one of the most pragmatic architecture styles available**: most of the benefits of a distributed architecture (agility, testability, deployability, fault tolerance, modularity) at a fraction of the cost and complexity of [[microservices]] or event-driven architecture. The pragmatic sweet spot between [[monolith]] and [[microservices]] for "most" business applications.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-13-service-based-architecture-style.md`, `raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md`, `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## What it is

Service-based architecture is a **hybrid of the microservices architecture style** (source: chapter-13-service-based-architecture-style.md). It is distributed — the UI, services, and database are separately deployed — but its services are **coarse-grained "portions of an application"** (called **domain services**), not the fine-grained single-purpose services of microservices. The number of services sits in a deliberately small band: **typically 4 to 12, averaging about 7**. Each domain service is the size of a bounded chunk of the application (OrderService, AssessmentService, QuotingService), not of a single business capability.

Three properties make the style distinct:

1. **Coarse-grained domain services** — each service owns a substantial slice of the application, not one operation. The chapter's `OrderService` places the order, generates an order ID, applies the payment, and updates inventory — *all inside one service* via class-level orchestration, where microservices would orchestrate multiple network hops.
2. **A shared monolithic database** — services typically share one relational database and use normal SQL joins and ACID transactions across it. Database connections are not a problem because there are only 4–12 services.
3. **A separately deployed user interface** — the UI is its own deployment unit, talking to the services remotely (usually REST, but messaging / RPC / SOAP are all valid).

Services are typically deployed as **monolithic-style artifacts** (EAR, WAR, assembly) and do not require containerisation, although they can be containerised (source: chapter-13-service-based-architecture-style.md).

## Basic topology

```
 [    User Interface (monolithic)    ]
              |
    --------------------------
    |     |     |     |     |
  [Svc] [Svc] [Svc] [Svc] [Svc]     <- 4 to 12 coarse-grained domain services
    |     |     |     |     |
    +-----+--+--+--+--+-----+
              |
         [  Shared DB  ]
```

Most services run as a **single instance** — multiple instances exist only when scalability, fault tolerance, or throughput require them, and then a load balancer fronts the domain service (source: chapter-13-service-based-architecture-style.md). The UI reaches services directly via a service-locator pattern; an API gateway is optional.

## Topology variants

The chapter stresses that service-based architecture has more topology flexibility than any other style in the book (source: chapter-13-service-based-architecture-style.md). Three dimensions of variability:

### User-interface variants

- **Single monolithic UI** — the default (Figure 13-1).
- **UI split by domain** — e.g. a customer-facing UI, an internal-operations UI, a reporting UI. Common when different audiences have different access paths or security requirements.
- **One UI per domain service** — the maximally federated form, analogous to micro-frontends in microservices.

### Database variants

- **Single shared monolithic database** — the default, and the property the style is best known for.
- **Logically partitioned single database** — schemas within one physical database carved into domain areas; discussed below under "Database partitioning".
- **Multiple physical databases** — up to one per domain service (approaching microservices' database-per-service). The rule: **the data in each separate database must not be needed by another domain service** (source: chapter-13-service-based-architecture-style.md). This avoids inter-service communication and data duplication, both of which are to be **definitely avoided** in service-based architecture.

### API-layer variant

- **UI calls services directly** — the default.
- **API gateway / reverse proxy between UI and services** — recommended when exposing services to external systems, or when cross-cutting concerns (metrics, security, auditing, service discovery) should live outside the UI (source: chapter-13-service-based-architecture-style.md).

## Service design and granularity

A domain service is itself usually designed as **a small [[layered-architecture|layered architecture]]** (API facade + business layer + persistence layer) or as a **[[modular-monolith|modular monolith]]** with internal sub-domains (source: chapter-13-service-based-architecture-style.md). Each design is a way to keep the coarse-grained service internally organised.

Every domain service must expose an **API access facade** — the entry point the UI calls. The facade typically takes responsibility for **orchestrating the business request** inside the service:

> "Consider a business request from the user interface to place an order (also known as catalog checkout). This single request, received by the API access facade within the `OrderService` domain service, internally orchestrates the single business request: place the order, generate an order ID, apply the payment, and update the product inventory for each product ordered. In the microservices architecture style, this would likely involve the orchestration of many separately deployed remote single-purpose services to complete the request." (source: chapter-13-service-based-architecture-style.md)

**This difference between internal class-level orchestration and external service orchestration is the central distinction between service-based architecture and microservices.**

### ACID vs BASE

Because domain services are coarse-grained, each business transaction usually lives inside a single service, which means **regular ACID database transactions** (commits, rollbacks) are used for database integrity (source: chapter-13-service-based-architecture-style.md). Microservices, being fine-grained, rely on **BASE transactions** (basic availability, soft state, eventual consistency) through [[saga|sagas]] — and take a corresponding hit in data integrity.

The chapter's worked example: a credit card expiring during checkout. In service-based architecture, the `OrderService` rolls the whole transaction back atomically — order row, payment attempt, inventory decrement — and notifies the customer. In microservices, the `OrderPlacement` service has already inserted the order before `PaymentService` rejects the card; now inventory, order status, and reservation all need reconciling via compensating actions. Service-based architecture avoids this class of problem by keeping the transaction inside one service (source: chapter-13-service-based-architecture-style.md).

### The trade-off

Coarse-grained services give better data integrity but mean **more code gets deployed for every change**:

- A change to order placement in `OrderService` forces testing of *everything else in `OrderService`* (including payment processing).
- The same change in a microservices architecture affects only the small `OrderPlacement` service — `PaymentService` is untouched.
- More code being deployed means more blast radius — something in payment might break because of an order-placement change.

Service-based architecture trades microservices' deployment granularity for transactional simplicity.

## Database partitioning

The shared monolithic database is the style's most visible feature and its most frequently cited risk. **Database table schema changes can potentially impact every service** if not managed carefully (source: chapter-13-service-based-architecture-style.md).

The chapter catalogues two approaches:

### Single shared entity library (least effective)

All entity objects (the classes representing database tables) live in **one shared library** (JAR, DLL) used by every domain service. Any table change forces a redeploy of every service, even services that don't touch the changed table. Shared-library versioning helps marginally, but the blast-radius problem remains. Figure 13-6 in the chapter is the illustration; this is the approach the chapter names as the **least effective way of implementing service-based architecture**.

### Federated shared libraries (recommended)

**Logically partition the database** into domain areas (the chapter's example: common, customer, invoicing, order, tracking) and create **one shared entity library per domain**. A change to an invoicing table touches only the invoicing shared library, which is used only by the services that care. Figure 13-7 is the illustration.

A **`common` domain** tends to emerge for cross-domain tables. These are genuinely shared and changes to them genuinely impact every service — the chapter's mitigation is to **lock the common entity objects in source control and restrict change access to the database team**, which emphasises the weight of common-table changes (source: chapter-13-service-based-architecture-style.md).

**Rule of thumb**: make the logical partitioning as fine-grained as possible while still maintaining well-defined data domains (source: chapter-13-service-based-architecture-style.md).

## Architecture characteristics ratings

The chapter's scorecard (source: chapter-13-service-based-architecture-style.md).

| Characteristic | Rating | Why |
|---|---|---|
| **Agility** | ★★★★ | Changes are isolated to one coarse-grained service — faster time to market than a monolith |
| **Testability** | ★★★★ | Per-service test scope is far smaller than a monolith; not as small as microservices |
| **Deployability** | ★★★★ | Each service deploys independently; far fewer units than microservices so pipeline and coordination overhead is low |
| **Fault tolerance** | ★★★★ | Services are self-contained and avoid inter-service calls — a failed service doesn't cascade |
| **Availability** | ★★★★ | Same logic as fault tolerance |
| **Reliability** | ★★★★ | Coarse granularity means less network traffic, fewer distributed transactions, less bandwidth — fewer network-related failures than finer-grained distributed architectures |
| **Modularity** | ★★★★ | Domain services are the modularity unit |
| **Simplicity** | ★★★ | Distributed architecture, but manageable — fewer moving parts than microservices |
| **Overall cost** | ★★★ | Cheaper than microservices, event-driven, or space-based; pricier than a monolith |
| **Scalability** | ★★★ | Possible but inefficient — coarse-grained services replicate more functionality per instance than microservices |
| **Performance** | ★★★ | Fewer network hops than microservices (single-service orchestration) |
| **Elasticity** | ★★ | Coarse-grained services are expensive to spin up elastically; typically single instances |

**Quantum count**: **≥ 1, often more than one**. The shared database and shared UI collapse the system into a single [[architectural-quantum|quantum]] by default, but the topology variants let this change. In the chapter's electronics-recycling example (below), the system has **two quanta** — a customer-facing one (separate UI, separate DB, Quoting + ItemStatus services) and an internal-operations one (the remaining services, another UI, another DB). Federating the UI or the database is what multiplies the quantum count.

### The distinctive shape: no five-star ratings, but many four-star ratings

Richards and Ford are explicit about the profile: **service-based architecture contains no five-star ratings, but many four-star ones** (source: chapter-13-service-based-architecture-style.md). That is the point. It is **the pragmatic sweet spot**: you get four stars on every operational and evolutionary characteristic that matters for most business applications, without paying the five-star cost and complexity of microservices, event-driven, or space-based architecture. The style's rhetoric is explicit — "it's like having the power, speed, and agility of a Ferrari used only for driving back and forth to work in rush-hour traffic at 50 kilometers per hour — sure it looks cool, but what a waste of resources and money" (source: chapter-13-service-based-architecture-style.md).

## Worked example: electronics recycling

The chapter's extended example (source: chapter-13-service-based-architecture-style.md):

**Domain**: a company that recycles old electronics. Customers get a quote (**Quoting**), ship the device (**Receiving**), have it evaluated (**Assessment**), get paid (**Accounting**), can check status at any time (**ItemStatus**), and the company eventually destroys or resells the device (**Recycling**). Financial and operational reports run periodically (**Reporting**).

**Implementation**: seven domain services, one per domain area, each separately deployed. The customer-facing UI (Quoting, ItemStatus) is a separate deployment from the internal-operations UI (Receiving, Assessment, Accounting, Recycling) and the reporting UI. **Two physical databases**: one customer-facing, one internal, with one-way firewall access from internal to customer-facing. Result: **two quanta**, with security (network-zone isolation), scalability (only Quoting and ItemStatus scale), and fault tolerance (customer-facing vs internal failure domains) all emerging from the topology decision.

The example showcases what the style was designed for: **domain variability is expressed as separately deployed domain services, and topology variations are used deliberately to achieve specific architecture characteristics** (security, scalability, fault tolerance) without paying for them uniformly across the whole system.

## When to use it

The chapter's case is strong and worth repeating near-verbatim (source: chapter-13-service-based-architecture-style.md):

- **"Most" business applications.** The flexibility plus the many three- and four-star ratings make service-based architecture **one of the most pragmatic architecture styles available**. Many teams reach for microservices when service-based would get them most of what they actually need.
- **When you want a distributed architecture but not at microservices' cost**. Cheaper and simpler than microservices, event-driven, or space-based; richer than a monolith.
- **When [[domain-driven-design|domain-driven design]] is a fit.** Coarse-grained domain services map naturally onto [[bounded-context|bounded contexts]]. Each domain service encompasses a particular domain, compartmentalising functionality into a single unit of software.
- **When ACID transactions matter.** Service-based architecture **preserves ACID transactions better than any other distributed architecture** because each business transaction usually lives inside one domain service (source: chapter-13-service-based-architecture-style.md). Cross-service orchestration falls back to sagas and BASE, but those cases are the minority.
- **When architectural modularity is the goal without granularity pain.** Richards and Ford: as services become more fine-grained, orchestration and choreography complexity appears — **central mediator (orchestration) vs peer-to-peer (choreography) coordination of multi-service business transactions**. Coarse-grained services largely dodge this class of problem (source: chapter-13-service-based-architecture-style.md).

## When not to use it

- **When five-star operational characteristics are required.** Elasticity is two stars; scalability is three. Systems that need to scale elastically to large, variable loads are better served by microservices, event-driven, or space-based architecture.
- **When independent data ownership matters per service.** The shared database is the style's defining feature; if each service must own its own data (regulatory, team-autonomy, or bounded-context reasons), microservices is the right shape.
- **When the domain has more than ~12 bounded contexts of roughly equal importance.** Service-based architecture's small-number-of-large-services assumption doesn't fit a large domain with many small pieces.
- **When the team is already on a path toward full microservices.** Service-based architecture is a useful intermediate state but is not automatically a migration step; if the organisation has microservices-grade operational maturity, skipping to microservices may be cheaper in the long run.

## As a migration stepping-stone (Hard Parts Ch 4)

*The Hard Parts* Chapter 4 reframes service-based architecture from "a destination" (*Fundamentals*'s framing) to **an intermediate target in a monolith-to-microservices migration** (source: raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md). The [[component-based-decomposition]] patterns in Chapter 5 extract components from a monolith into domain services — that's service-based architecture by definition.

The recommendation:

> When migrating monolithic applications to microservices, consider moving to a service-based architecture first as a stepping-stone to microservices. (source: raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md)

The reasoning restates the points on this page from a migration angle:

- **Service-based architecture does not require the database to be broken apart.** Architects can focus on domain and functional partitioning *first*, and tackle the hardest problem (data) later (Chapter 6 of *The Hard Parts*). See [[database-decomposition]].
- **Service-based architecture does not require operational automation or containerisation.** Each domain service can be deployed using the same deployment artefact as the original monolith (EAR, WAR, assembly). Kubernetes, service meshes, and observability platforms are optional additions, not preconditions.
- **Moving to service-based architecture is a *technical* migration, not an organisational one.** It doesn't involve business stakeholders, doesn't require reorganising the IT department, and doesn't force a change to the QA and deployment pipelines.
- **It acts as a decision checkpoint.** Some domains can stop as coarse-grained domain services forever. Others reveal — once load profiles and rate-of-change are understood under production traffic — that they need further decomposition into microservices (Chapter 7 of *The Hard Parts* covers that decision).

This reframing is the main reason service-based architecture shows up so prominently in the *Hard Parts* decomposition chapters: it is the natural output of disciplined component-based decomposition, and the natural launch pad for any subsequent microservices work.

### The "soft landing" from Chapter 5

Chapter 5 of *The Hard Parts* operationalises this positioning: the sixth and last [[component-based-decomposition]] pattern — [[create-domain-services-pattern]] — takes the logical component domains produced by the preceding five patterns and extracts each one as a separately deployed domain service. The output of that pattern **is** a service-based architecture by construction (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md). The chapter explicitly calls it a "soft landing":

> Moving to service-based architecture first allows the architect and development team to learn more about each domain service to determine whether it should be broken into smaller services within a microservices architecture or left as a larger domain service. Too many teams make the mistake of starting out too fine-grained. (source: chapter-05-component-based-decomposition-patterns.md)

The landing is soft because nothing about it is irreversible: the shared database stays, the deployment artefacts stay (EAR/WAR/assembly), the team structure stays. The architect can pause at service-based architecture indefinitely for some domains and only decompose the ones that demonstrate a need under production traffic. See [[create-domain-services-pattern]] for the pattern's mechanics and [[create-component-domains-pattern]] for the logical grouping that feeds it.

## The shared database question

This is the style's most controversial property. Newman's [[shared-database-antipattern]] treatment in *Monolith to Microservices* names direct database sharing as the single biggest obstacle to [[independent-deployability]]; microservices discipline requires each service to own its data. Richards and Ford **explicitly endorse** the shared database for service-based architecture — they frame it as a feature, not a bug, under two conditions:

1. **The service count is small** (4–12, average 7) — so the number of schema-change stakeholders is bounded.
2. **Federated shared-entity libraries** are used to bound the blast radius of schema changes to the domain that needs them.

The two sources are not contradicting each other. **Newman is describing microservices discipline; Richards and Ford are describing a different architecture style with different priorities.** Service-based architecture explicitly trades microservices-grade independent deployability for ACID transactions and operational simplicity. See [[shared-database-antipattern]] for Newman's framing and [[service-based-architecture]] (this page) for the case where the trade-off is deliberate.

## Relationship to other concepts

- **[[microservices]]** — service-based architecture is a **hybrid / pragmatic alternative to microservices**. Same instinct (break the monolith into separately deployed services), different granularity (4–12 coarse vs dozens to hundreds of fine), different data stance (shared DB vs per-service DB), different transaction model (ACID vs BASE/saga). Use service-based when microservices is more power than the problem needs.
- **[[monolith]]** — service-based architecture is **what you get when you stop at coarse domain services**. Monolith is one quantum, service-based is ≥ 1. A monolith with a well-factored modular interior ([[modular-monolith]]) is the natural migration source.
- **[[modular-monolith]]** — the monolithic sibling. A modular monolith's modules are the same conceptual unit as service-based architecture's domain services; going from modular monolith to service-based is primarily a deployment change.
- **[[layered-architecture]] / [[pipeline-architecture]] / [[microkernel-architecture]]** — the three monolithic Part II styles. Service-based architecture is the first distributed style in the book and the cheapest on-ramp from monolithic to distributed.
- **[[shared-database-antipattern]]** — Newman's pattern, framed from a microservices discipline. Service-based architecture deliberately accepts the shared database; the two views are consistent when read as "the antipattern is shape-dependent, not universal".
- **[[architectural-quantum]]** — service-based architecture is typically one quantum but can be more once UI and DB are federated. The electronics-recycling example is two quanta.
- **[[technical-vs-domain-partitioning]]** — service-based architecture is **domain-partitioned** (services are domains, not layers). The interior of each domain service may still be technically partitioned (API facade + business + persistence).
- **[[monolithic-vs-distributed]]** — service-based architecture is **distributed**. It pays the [[fallacies-of-distributed-computing|distribution tax]] but less of it than microservices because inter-service calls are rare (coarse-grained services + shared DB mean transactions stay local).
- **[[domain-driven-design]] / [[bounded-context]]** — service-based architecture's domain services align naturally with DDD bounded contexts. The chapter names service-based as "a natural fit when doing domain-driven design".
- **[[saga]]** — falls back to sagas and BASE transactions only for the minority case where a business transaction genuinely spans two domain services. Most transactions stay inside a single service and use ACID.

## Related pages

- [[microservices]]
- [[monolith]]
- [[modular-monolith]]
- [[layered-architecture]]
- [[pipeline-architecture]]
- [[microkernel-architecture]]
- [[shared-database-antipattern]]
- [[architectural-quantum]]
- [[technical-vs-domain-partitioning]]
- [[monolithic-vs-distributed]]
- [[fallacies-of-distributed-computing]]
- [[domain-driven-design]]
- [[bounded-context]]
- [[saga]]
- [[component-based-decomposition]]
- [[create-domain-services-pattern]]
- [[create-component-domains-pattern]]
- [[tactical-forking]]
- [[migration-pattern-selection]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
