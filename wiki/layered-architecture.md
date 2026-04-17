# Layered Architecture

**Summary**: Also known as the **n-tier architecture**, this is the de facto default architecture style for most applications — simple, familiar, cheap, and a natural fit for organisations already split by technical competency ([[conways-law|Conway's law]] in action). Components are organised into horizontal layers (presentation, business, persistence, database), each performing a specific technical role. The style's strengths are cost and simplicity; its weaknesses are elasticity, scalability, fault tolerance, and deployability. This is the first Part II style chapter in *Fundamentals of Software Architecture* and the canonical example of a [[monolithic-vs-distributed|monolithic]] + [[technical-vs-domain-partitioning|technically partitioned]] architecture.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-10-layered-architecture-style.md`

**Last updated**: 2026-04-16

---

## Why it's the default

Richards and Ford open Chapter 10 with a blunt claim: the layered architecture is *the de facto standard for most applications, primarily because of its simplicity, familiarity, and low cost* (source: chapter-10-layered-architecture-style.md). Two structural forces keep it there:

1. **Conway's law.** Most organisations have UI developers, backend developers, rules developers, and DBAs — separate competency silos. Those silos map one-to-one onto presentation / business / rules / persistence layers, so the architecture falls out of the org chart without anyone having to choose it. See [[conways-law]] and the Inverse Conway Maneuver on [[technical-vs-domain-partitioning]].
2. **It's what happens when no one picks a style.** The chapter names two anti-patterns that converge on this style: the **architecture by implication** anti-pattern (no one documented a style, but one exists) and the **accidental architecture** anti-pattern (a team "just started coding"). If you don't know which style you're using, you're almost certainly using layered (source: chapter-10-layered-architecture-style.md).

This is why Chapter 10 comes first: every architect has met it, and many have shipped it without naming it.

## Topology

Components are organised into horizontal layers, each with a specific role. Most layered architectures use four standard layers (source: chapter-10-layered-architecture-style.md):

| Layer | Responsibility |
|---|---|
| **Presentation** | User interface, browser communication, rendering |
| **Business** | Business rules associated with the request |
| **Persistence** | Mapping objects to storage (SQL, HQL, ORM) |
| **Database** | The actual data store (usually external) |

Smaller applications may fold persistence into business (three layers); larger applications may add a rules or services layer (five or more). The chapter illustrates three physical deployment variants:

1. Presentation + business + persistence as one deployable; database external.
2. Presentation as its own deployable; business + persistence as a second; database external.
3. All four combined into one deployable (embedded or in-memory DB — common for on-prem products).

Each layer forms an **abstraction** around the work needed to satisfy a business request. The presentation layer doesn't know how customer data is fetched, only how to render it. The business layer doesn't know how to render or where data comes from — it just applies rules. This separation of concerns is the style's central virtue.

## Technical partitioning

The layered architecture is the canonical example of **[[technical-vs-domain-partitioning|technical partitioning]]**: components are grouped by their technical role (presentation, business, persistence) rather than by business domain (Catalog, Checkout, Delivery). The Chapter 8 trade-offs apply directly (source: chapter-10-layered-architecture-style.md):

- Any given business domain — e.g. `Customer` — is **smeared across every layer**. Changing how customers work touches presentation, business, rules, services, and database.
- Change cost is high because every domain change crosses layer boundaries.
- Domain-driven design *does not work well* in a layered architecture, because DDD wants the top-level boundary to be the domain.

This is the Chapter 8 `CatalogCheckout` change-smear problem stated specifically for the layered style.

## Closed vs open layers: layers of isolation

A layer can be **closed** or **open** (source: chapter-10-layered-architecture-style.md):

- **Closed layer**: a request moving top-down *cannot* skip the layer — it must pass through. In a fully-closed layered architecture, a presentation-layer request must go through business, then persistence, then database.
- **Open layer**: a request can bypass the layer and go to the next one down.

Which is better? The answer is the **layers of isolation** principle: changes to one layer should not affect the others, provided the contracts between layers are stable. For that to hold, the layers on the major request path **must be closed**. If the presentation layer can reach the persistence layer directly, any change in persistence ripples back to presentation and to business — tight coupling, brittle architecture, expensive change.

Closed layers also enable **replacement**: swap a JSF presentation layer for React.js without touching business or persistence, provided the contract holds (with help from the **business delegate** pattern).

### When open layers are useful: shared services

Closed layers have a governance problem. If the business layer contains shared utility classes (date/string utilities, auditing, logging) and architecture policy restricts the presentation layer from using them, *nothing architecturally enforces that rule* — the presentation layer can already reach the business layer, so the restriction is an honour system (source: chapter-10-layered-architecture-style.md).

The fix is to extract shared utilities into a new **services layer** sitting between business and persistence. The business layer is closed (so presentation can't reach services). The services layer is **open** (so business can use it *or* bypass it on the way to persistence). That arrangement uses the open/closed distinction to enforce a restriction that closed-layers-only cannot.

The editorial lesson: every layer needs an **open/closed label**, and both the label and its rationale need to be documented. Failing to do so usually results in tightly-coupled, brittle architectures.

## Architecture sinkhole anti-pattern

The signature pathology of the layered style. A **sinkhole** is a request that moves layer-to-layer as **simple pass-through** with no business logic at any layer (source: chapter-10-layered-architecture-style.md):

> Presentation receives "get customer name and address" → passes to Business → passes to Rules → passes to Persistence → issues a SQL SELECT → returns the row → Persistence returns → Rules returns → Business returns → Presentation renders. No aggregation, no calculation, no rule application, no transformation. Just plumbing.

Every layered architecture has *some* sinkholes. The question is **what percentage**. Richards and Ford propose the **80-20 rule** as a diagnostic:

- ~20% sinkhole requests: acceptable, characteristic of the style.
- ~80% sinkhole requests: the layered architecture is the wrong style for this problem.

Two fixes when the percentage is high:

1. Make all layers **open** — requests can skip layers that don't add logic. The trade-off is that change management gets much harder.
2. **Change the style** — if most requests are pass-through, the application isn't really doing layer-appropriate work and another style (pipeline, service-based, microservices) will likely serve better.

The sinkhole is the canonical operational cost of the "layers of isolation" design: you pay for the isolation whether or not the request needs it.

## When to use it

The layered architecture is the right pick when (source: chapter-10-layered-architecture-style.md):

- The application is **small or simple** — a basic website, internal tool, or CRUD application.
- The project has **tight budget and time constraints** — layered is the lowest-cost style to build because it's familiar to everyone.
- The architect is **still analysing requirements** and doesn't yet know which style fits — layered is a reasonable starting point that can be migrated later.

Common microservices teams legitimately start here: begin with a layered monolith while the architectural question is still open, then extract services as the boundaries become clear. Two disciplines keep the later migration feasible:

- Keep **reuse minimal** (reuse creates coupling that crosses future service boundaries).
- Keep **object hierarchies shallow** (deep inheritance trees are the classic obstacle to extraction).

## When not to use it

The layered architecture scales poorly — **maintainability, agility, testability, and deployability degrade as the application grows** (source: chapter-10-layered-architecture-style.md). If any of the following are critical, choose another style:

- **Elasticity or scalability** — layered is monolithic; scaling means cloning the whole thing.
- **Fault tolerance** — one out-of-memory condition crashes everything.
- **High deployment cadence** — every three-line change redeploys the whole app.
- **Domain-driven design** — DDD wants domain-shaped top-level boundaries; layered gives technical ones.

The cautionary pattern: applications that *started* layered and grew. Every characteristic rating in the next section gets worse as the codebase gets bigger.

## Architecture characteristics ratings

Richards and Ford close every Part II style chapter with a star-rating scorecard along a standard set of architecture characteristics (one star = poorly supported, five stars = one of the style's strongest features). This is the framework Chapter 9 forward-referenced.

**Layered architecture scorecard** (source: chapter-10-layered-architecture-style.md):

| Characteristic | Rating | Why |
|---|---|---|
| **Overall cost** | ★★★★★ | Lowest-cost style: simple, familiar, no distribution tax |
| **Simplicity** | ★★★★★ | Easy to understand; no distributed complexity |
| **Deployability** | ★★ | Whole deployable ships for a three-line change; ceremony, risk, infrequent deployment |
| **Testability** | ★★ | Entire regression suite needed for small changes; mocking/stubbing raises it from one star to two |
| **Reliability** | ★★★ | No network traffic mitigates some failure modes; monolithic deployment and low testability drag it down |
| **Availability** | ★★ | High MTTR — startup times of 2–15 minutes for larger applications |
| **Elasticity** | ★ | Monolithic deployment; parallel-processing techniques don't fit naturally |
| **Scalability** | ★ | Single-quantum architecture — scales only by cloning the whole system |
| **Fault tolerance** | ★ | One out-of-memory condition crashes the whole application |
| **Performance** | ★★ | Caching and multithreading can help but aren't natural; closed layers and the sinkhole anti-pattern drag it down |

**Monolithic quantum**: the layered architecture is always a **single [[architectural-quantum|architectural quantum]]** — monolithic UI + monolithic backend + monolithic database. That single-quantum shape is why every "scale / elasticity / fault tolerance" rating is as low as it is. See [[architectural-quantum]] and [[monolithic-vs-distributed]].

**The shape of the scorecard**: cost and simplicity max out; everything operational (elasticity, scalability, fault tolerance, availability, deployability) is poor. That profile is the style's defining trade-off: you buy cheapness and familiarity with ceilings on every operational characteristic.

**Cautionary note**: these ratings assume a *reasonably-sized* application. As monolithic layered architectures get bigger, even the strong ratings (cost, simplicity) start to degrade. The chapter is explicit: *these ratings start to quickly diminish as monolithic layered architectures get bigger and consequently more complex* (source: chapter-10-layered-architecture-style.md).

## Relationship to other concepts

- [[monolithic-vs-distributed]] — layered is the archetypal monolithic style; it dodges every [[fallacies-of-distributed-computing|fallacy of distributed computing]] by construction.
- [[technical-vs-domain-partitioning]] — layered is the canonical technical partitioning; all the trade-offs there (the `CatalogCheckout` change-smear, the Inverse Conway Maneuver, the industry drift toward domain) apply directly.
- [[components]] — in a layered architecture the top-level components *are* the layers (presentation, business, persistence); inside each layer, domain-named sub-components handle their slice of every domain.
- [[architectural-quantum]] — a layered architecture is always a quantum of one.
- [[conways-law]] — the org chart (UI / backend / DBAs) reproduces itself as the layer structure; the Inverse Conway Maneuver is the counter-move when you want to leave the style.

## Related pages

- [[monolithic-vs-distributed]]
- [[technical-vs-domain-partitioning]]
- [[components]]
- [[architectural-quantum]]
- [[conways-law]]
- [[fallacies-of-distributed-computing]]
- [[modular-monolith]]
- [[monolith]]
- [[microservices]]
- [[fundamentals-of-software-architecture]]
