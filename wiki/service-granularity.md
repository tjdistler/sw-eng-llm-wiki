# Service Granularity

**Summary**: The size and scope of an individual service — the architect's hardest single decision when drawing service boundaries in any distributed architecture style. Richards and Ford frame it as the decision that most determines whether a [[microservices]] architecture succeeds or collapses under communication overhead, and [[service-based-architecture]], [[orchestration-driven-soa]], and [[event-driven-architecture]] each answer the granularity question differently.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`, `raw/fundamentals-of-software-architecture/chapter-13-service-based-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-16-orchestration-driven-service-oriented-architecture.md`, `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`

**Last updated**: 2026-04-16

---

## The hardest decision

Chapter 17 of *Fundamentals of Software Architecture* is blunt: *"making determining the granularity of services the key to success in this architecture"* (source: chapter-17-microservices-architecture.md). Architects routinely get it wrong in both directions — too fine creates a communication tangle that defeats the decoupling the style was chosen for; too coarse produces services that are really small monoliths and forfeit the operational benefits.

"Microservice" is a label, not a description. Martin Fowler's quote from Chapter 17 captures the source of the over-fine mistake: the name was chosen to contrast with SOA's *gigantic services*, not as a commandment to build the smallest possible service. Many developers hear it and over-decompose (source: chapter-17-microservices-architecture.md).

## The two failure modes

### Too fine

Symptoms:

- **Communication tangle** — every user request requires a dozen service-to-service calls.
- **Fan-out latency** — request latency becomes the sum of a long call chain (the 10-hop × 100-ms = 1-second example on [[fallacies-of-distributed-computing]]).
- **Shared-data gravity** — services constantly ask each other for data they already had in a previous service; stamp coupling emerges (see the [[fallacies-of-distributed-computing#3. Bandwidth is infinite|bandwidth-math worked example]] on the fallacies page).
- **Transaction pressure** — workflows that were one database transaction now cross many services, driving architects toward [[saga|sagas]] or, worse, attempted distributed transactions.
- **Operational overhead** — N services means N deployments, N dashboards, N oncall rotations, N sets of cross-cutting concerns to maintain (even with sidecars).

Richards and Ford's diagnostic from Chapter 17: *"architects who build microservices architectures who then find a need to wire them together with transactions have gone too granular in their design. Transaction boundaries is one of the common indicators of service granularity"* (source: chapter-17-microservices-architecture.md). The quotable form: **"Don't do transactions in microservices — fix granularity instead!"**

### Too coarse

Symptoms:

- **Multiple [[bounded-context|bounded contexts]] per service** — the service doesn't have one clear business purpose.
- **Deploy-coupled teams** — multiple teams must coordinate to ship a release, defeating [[independent-deployability]].
- **Internal tangle** — the service becomes a small monolith with all the maintenance pains monoliths have.
- **Scaling inefficiency** — scaling the whole service because one feature inside it is hot.
- **Testing inefficiency** — tests must cover the full surface of the coarse service even when the change is localised.

The coarse-grained failure is the ghost of [[orchestration-driven-soa]]: services like the enterprise `Customer` service that accumulated every consumer's attribute became the opposite of modular.

## The three Chapter 17 guidelines

Richards and Ford offer three concrete tests for the right boundary (source: chapter-17-microservices-architecture.md):

### 1. Purpose

Each service should be **extremely functionally cohesive** — one significant behaviour on behalf of the overall application. This is the [[cohesion|functional cohesion]] criterion from Chapter 3 applied at the service level: can you describe what this service does in one sentence without "and"?

### 2. Transactions

Bounded contexts are business workflows, and the entities that must cooperate in a transaction usually belong in the same service. Needing a transaction across services is evidence that the split was wrong.

Because transactions are inherently problematic in distributed architectures (see [[distributed-transactions]], [[two-phase-commit]]), designing the architecture to **avoid** distributed transactions produces better systems. Keep the cooperating entities inside one service boundary.

### 3. Choreography

If a set of services offers excellent domain isolation but requires extensive interservice communication to do useful work, the architect has gone too granular. Bundle them back up. The decoupling benefit is eaten by the communication overhead.

## Iteration, not clairvoyance

Chapter 17's honest admission: *"Iteration is the only way to ensure good service design. Architects rarely discover the perfect granularity, data dependencies, and communication styles on their first pass"* (source: chapter-17-microservices-architecture.md). The tests above are applied repeatedly, with the resulting granularity refined as the architecture evolves.

Newman makes the complementary point in *Monolith to Microservices*: start coarse (at the [[bounded-context]] level), then split by [[aggregate]] if and when needed. The coarse-first discipline defends against the over-fine failure mode while keeping the future-decomposition option open (source: chapter-01-just-enough-microservices.md). See [[incremental-migration]] for the migration-side view.

## How the other Part II styles answer the granularity question

Granularity is a cross-cutting concern in Richards and Ford's style catalog. Each style picks a different point on the axis:

| Style | Granularity | Mechanism | Trade-off |
|---|---|---|---|
| [[layered-architecture]] / [[pipeline-architecture]] / [[microkernel-architecture]] | N/A — one quantum | No service boundary decision to make | Simplicity; operational ceilings |
| [[service-based-architecture]] | **Coarse** — 4–12 services, ~7 average | One service per business domain; each service is internally a small layered architecture; shared database preserves ACID | Four-star fault tolerance / availability / reliability without microservices complexity; shared DB schema coupling |
| [[event-driven-architecture]] | **Per-event-processor** | Each processor is one bounded piece of business logic reacting to one or a few event types | Natural fine granularity from event decomposition; saga-style state management required |
| [[space-based-architecture]] | Processing-unit-per-domain | Each [[processing-unit]] is a deployable with its own in-memory grid; count driven by UI/domain associations | Granularity mostly determined by cache-membership economics, not domain decomposition |
| [[orchestration-driven-soa]] | **Mixed and never stable** | Business services defined at workflow granularity; enterprise services fine-grained for reuse; application services one-off | Failed partly *because* granularity was never stable — the reuse thesis kept pushing enterprise services toward finer grain while business services stayed coarse |
| [[microservices]] | **Fine, but not atomic** | One service per bounded context; split further by aggregate only when the three-guideline test demands it | Central architect decision; success hinges on getting this right |

The pattern across the catalog: styles with a single [[architectural-quantum|quantum]] don't have a granularity problem (there's no boundary to draw); styles with many quanta must solve it. Microservices is the style where getting it right matters most, because the style's entire value proposition depends on the boundaries being in the right places.

## Relationship to [[architectural-quantum|architectural quanta]]

The Chapter 7 framing provides the physical interpretation of granularity: a service's quantum is the service-plus-its-database-plus-its-dependent-components. A finer-grained split that breaks a logical bounded context in half produces two quanta that share synchronous connascence — they look independent on the deployment diagram but collapse operationally into one unit during any call chain spanning them.

Thus the right granularity is, structurally, **the granularity at which each quantum can carry a distinct architecture-characteristics profile without the synchronous-connascence-collapse problem erasing the separation.** When splitting a service doesn't produce meaningfully different characteristics profiles, the split added complexity without structural payoff.

## Relationship to [[coupling]] and [[connascence]]

Granularity decisions are the upstream cause of the coupling and connascence that appear downstream:

- **Finer** services push coupling **into the network** (more synchronous calls, more stamp coupling, more connascence of position/meaning across service boundaries — the worst kind because it's dynamic and non-local).
- **Coarser** services push coupling **inside the service** (more shared classes, more [[cohesion|lower-cohesion]] modules, but all of it local and refactorable).

The architect's granularity choice is therefore a choice between which *kind* of coupling to pay. Neither is free. The microservices bet is that in-service coupling is refactorable and cross-service coupling is expensive to discover — so pay the in-service cost and save the cross-service cost by drawing wider boundaries. This is why the guidelines above prefer **coarser** granularity when in doubt.

## Related pages

- [[microservices]]
- [[bounded-context]]
- [[aggregate]]
- [[architectural-quantum]]
- [[service-based-architecture]]
- [[orchestration-driven-soa]]
- [[event-driven-architecture]]
- [[cohesion]]
- [[coupling]]
- [[connascence]]
- [[saga]]
- [[distributed-transactions]]
- [[independent-deployability]]
- [[fallacies-of-distributed-computing]]
- [[entity-trap]]
- [[incremental-migration]]
