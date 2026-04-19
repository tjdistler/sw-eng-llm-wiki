# Service Granularity

**Summary**: The size and scope of an individual service — the architect's hardest single decision when drawing service boundaries in any distributed architecture style. Richards and Ford frame it as the decision that most determines whether a [[microservices]] architecture succeeds or collapses under communication overhead, and [[service-based-architecture]], [[orchestration-driven-soa]], and [[event-driven-architecture]] each answer the granularity question differently.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`, `raw/fundamentals-of-software-architecture/chapter-13-service-based-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-16-orchestration-driven-service-oriented-architecture.md`, `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`, `raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md`

**Last updated**: 2026-04-19

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

## "Not all microservices need be micro" (Bellemare, Ch 17)

Bellemare's conclusion to *Building Event-Driven Microservices* adds a pragmatic escape hatch for organizations that haven't fully paid the [[microservice-tax]]: **larger services are fine if they follow three principles** (source: chapter-17-conclusion.md). The point is that the EDM discipline is not about service size — it's about how services communicate and where the authoritative state lives. If you obey these three rules, you retain the ability to *later* split any of your large services into finer-grained ones decoupled from the existing landscape:

1. **Put important business entities and events into the event broker.** Your data must live on the shared [[event-streams|event streams]], not only inside the large service. This is [[data-liberation]] applied at whatever size your services happen to be.
2. **Use the event broker as the single source of truth.** Consumers — including new, fine-grained future services — read from the broker, not from the large service's database. See [[event-as-single-source-of-truth]].
3. **Avoid direct calls between services.** Synchronous point-to-point coupling is what makes later decomposition expensive. Keep the default communication asynchronous over streams.

Follow the rules and a large service is just a large bounded context that *could* be split later — not a dead end. Violate them and splitting any future fine-grained service out of the tangle becomes the same monolith-extraction job Newman's migration book is about.

Bellemare also reinforces the technical-vs-domain alignment point: **steer clear of technical boundaries; align with the business's bounded context.** A technical microservice (e.g., "the email service") couples itself to every unrelated workflow that uses it; a failure or inadvertent change takes down multiple business workflows at once. This is the same disease Richards and Ford diagnose in [[technical-vs-domain-partitioning]] and that the fine-grained-too-soon failure mode above hints at.

## The Hard Parts framing: disintegrators vs integrators

Chapter 7 of *Software Architecture: The Hard Parts* gives the most rigorous trade-off frame for granularity in the wiki's source canon. Ford, Richards, Sadalage, and Dehghani open with the **modularity vs granularity** distinction — modularity asks *how many pieces*, granularity asks *how small each piece is*. Most distributed-system pain is granularity, not modularity (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md). See [[architectural-modularity]] for the modularity side.

The chapter rejects lines-of-code and number-of-classes as granularity metrics — they vary too much by language, style, and developer. Two more objective metrics:

- **Number of statements** (lines of executable logic terminated by `;` or newline depending on language)
- **Number of public interfaces or operations** exposed by the service

Neither is fully objective, but both beat LOC.

The chapter then frames granularity as a balance between two opposing force groups, **disintegrators** (push services apart) and **integrators** (pull services together):

### The six disintegrators (full treatment in [[granularity-disintegrators]])

| # | Driver | Question |
|---|---|---|
| 1 | **Service scope and function** | Is the service doing too many unrelated things? |
| 2 | **[[code-volatility|Code volatility]]** | Are changes isolated to only one part of the service? |
| 3 | **[[scalability]] and throughput** | Do parts of the service need to scale differently? |
| 4 | **[[fault-tolerance]]** | Are there errors that cause critical functions to fail within the service? |
| 5 | **Security** | Do some parts of the service need higher security levels than others? |
| 6 | **Extensibility** | Is the service always expanding to add new contexts? |

### The four integrators (full treatment in [[granularity-integrators]])

| # | Driver | Question |
|---|---|---|
| 1 | **Database transactions** | Is an [[acid|ACID]] transaction required between separate services? |
| 2 | **Workflow and choreography** | Do services need to talk to one another? |
| 3 | **Shared code** | Do services need to share code among one another? |
| 4 | **Data relationships** | Although a service can be broken apart, can the data it uses be broken apart as well? |

### The central principle

> The secret of arriving at the appropriate level of granularity for a service is achieving an equilibrium between these two opposing forces. (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md)

The chapter is emphatic that the most common mistake is focusing on disintegrators while ignoring integrators. *Hold services together until a disintegrator outweighs all the integrators in play.* This is the disciplined version of "don't over-decompose."

### Worked architect/sponsor dialogues

The chapter shows trade-off resolution as a literal conversation with the business sponsor, not a unilateral architect call. Three examples (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md):

1. **Volatility (disintegrator) vs ACID transaction (integrator)** — *"Better agility (testability, deployability, time-to-market) or stronger data integrity?"* Sponsor chose data integrity; service stayed consolidated.
2. **Security (disintegrator) vs ACID transaction (integrator)** — *"Better data consistency or better security?"* Sponsor chose security; services were split and saga-style consistency was accepted as the cost.
3. **Extensibility (disintegrator) vs workflow/responsiveness (integrator)** — *"Better extensibility or better responsiveness for payment?"* Sponsor chose responsiveness; payment service stayed consolidated until extensibility actually became a pressing concern.

The pattern: identify the forces on both sides, frame the trade-off as a single sentence with two options, and bring it to the business sponsor with the implications spelled out. Capture the resolution in an [[architecture-decision-record|ADR]].

### Sysops Squad sagas in the chapter

The chapter ends with two Sysops Squad worked examples (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md):

- **Ticket Assignment Granularity** — should ticket creation, assignment, and routing be one service or several?
- **Customer Registration Granularity** — should customer profile and password live together or apart?

Both walk the disintegrator/integrator analysis and resolve via the architect/sponsor dialogue pattern.

## "Microservices" vs "fine-grained" — clearing up the label

Hard Parts Ch 7 reinforces the *Fundamentals* Ch 17 point on the same page where it introduces granularity metrics: a microservice is "a single-purpose, separately deployed unit of software that does one thing really well." The trouble is that "single purpose" is in the eye of the beholder. Combined with the SRP-meets-microservices framing (Robert C. Martin's Single Responsibility Principle applied at the service layer), the temptation to make services as small as possible is structural — and the disintegrator/integrator balance is the corrective.

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
- [[event-driven-microservices]]
- [[data-liberation]]
- [[event-as-single-source-of-truth]]
- [[microservice-tax]]
- [[granularity-disintegrators]]
- [[granularity-integrators]]
- [[code-volatility]]
- [[architectural-modularity]]
- [[trade-off-analysis]]
- [[architecture-decision-record]]
- [[acid]]
- [[software-architecture-the-hard-parts]]
