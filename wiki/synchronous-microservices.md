# Synchronous Microservices

**Summary**: Microservices that communicate directly via request/response APIs (typically HTTP/REST or gRPC), as opposed to asynchronously through durable [[event-streams]]. Adam Bellemare's Chapter 1 catalogues their drawbacks as the motivation for preferring [[event-driven-microservices]] by default while conceding that synchronous patterns remain the right fit for several specific use cases.

**Sources**: `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## What they are

Synchronous microservices are the classic service-oriented-architecture form: services communicate directly through APIs to fulfill business requirements, with a caller blocking on a callee's response (source: chapter-01-why-event-driven-microservices.md). Netflix, Lyft, Uber, and Facebook are cited as companies that have succeeded with large-scale synchronous microservice systems, so the style is clearly workable — but Bellemare warns against conflating a company's success with the quality of its underlying architecture.

## Drawbacks

Chapter 1 names seven structural weaknesses (source: chapter-01-why-event-driven-microservices.md):

### Point-to-point couplings

Every synchronous service depends on downstream services, which depend on their downstreams, and so on. The fan-out becomes staggering, tracing responsibility for a business outcome becomes hard, and the existing communication structure entrenches itself — each point-to-point edge is a coordination cost for future change.

### Dependent scaling

A service's scalability is bounded by the scalability of everything it calls. Implementation technology choices anywhere in the graph can become a bottleneck. Surging or variable loads must be absorbed synchronously across the whole chain.

### Service failure handling

When a dependent service is down, the caller must decide: retry, fail, fall back, or degrade. These decisions multiply with every edge in the service graph and interact non-obviously with data-consistency requirements.

### API versioning and dependency management

Multiple API versions often have to run simultaneously — you can't always force all clients to upgrade. Orchestrating API changes across many services is expensive, especially when the change includes the underlying data structures.

### Data access tied to the implementation

Synchronous microservices still need commonly used data from other services. The onus of providing that data — and scaling access to it — falls back on the implementation communication structure, reproducing the pathologies of overloaded implementations. (See [[communication-structures]].)

### Distributed monoliths

Teams decomposing a [[monolith]] via synchronous point-to-point calls often end up mimicking the monolith's internal coupling across the network. Function calls slot line-for-line into remote calls, and the bounded contexts never get redrawn. The result is a [[monolith|distributed monolith]] with all the deployment and operational costs of distribution and none of the decoupling benefits.

### Testing

Integration tests require fully operational dependents (which require their own fully operational dependents). Stubs help for unit tests but rarely suffice for broader testing.

## Where synchronous microservices remain the right tool

Bellemare is explicit that synchronous and event-driven are not strictly ranked — each has its place (source: chapter-01-why-event-driven-microservices.md). Synchronous request/response fits best when:

- **Authentication** — user login, session checks, permission lookups.
- **A/B-test reporting** — fetching experiment state for a specific request.
- **Third-party integrations** — almost always HTTP-based; usually the only option.
- **Tracing and debuggability** — synchronous call chains show up cleanly in detailed logs, unlike event flows where causality has to be reconstructed.
- **User-facing web and mobile experiences** — clients need timely, per-request responses regardless of how the backend is organized.
- **Talent availability** — many developers are much more experienced with synchronous, monolithic-style coding; hiring for synchronous systems is easier than for asynchronous event-driven development.

## Hybrid is the norm

A company's architecture could only rarely, if ever, be entirely event-driven (source: chapter-01-why-event-driven-microservices.md). Real systems deploy synchronous and asynchronous side-by-side and let each handle the problem shape it's best at:

- Use asynchronous [[event-driven-microservices]] for cross-domain data flows, decoupled business processes, and the **data communication structure** of the organization.
- Use synchronous calls where the interaction is genuinely request-shaped, where debuggability matters disproportionately, or where external systems dictate the protocol.

This mirrors Richards and Ford's [[event-driven-architecture]] framing that event-based and request-based models are complementary rather than competing.

Bellemare's Chapter 13 spells out the specific integration patterns at the boundary — see [[event-driven-request-response-integration]] for the hub. The main axes are: ingesting external requests as events ([[external-events-ingestion]], [[third-party-api-integration]]), serving EDM state over a synchronous API ([[serving-state-from-edm]]), turning user requests into events ([[request-as-event]], [[asynchronous-ui]]), and the frontend counterpart [[micro-frontends]].

## Relationship to other wiki coverage

- **[[microservices]]** — the umbrella page. The "three defining properties" (independent deployability, business-domain alignment, owning your own data) apply to both synchronous and asynchronous forms.
- **[[event-driven-microservices]]** — Bellemare's preferred default; this page is its explicit foil.
- **[[rpc]]** — the synchronous-call substrate.
- **[[circuit-breaker]], [[bulkhead]], [[timeouts]]** — the resiliency patterns synchronous microservices need because of the failure-handling drawback above.
- **[[fallacies-of-distributed-computing]]** — the assumptions that bite synchronous microservices hardest.
- **[[monolith|distributed monolith]]** — the anti-pattern synchronous decomposition most often falls into.

## Related pages

- [[event-driven-microservices]]
- [[microservices]]
- [[monolith]]
- [[rpc]]
- [[message-brokers]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[timeouts]]
- [[fallacies-of-distributed-computing]]
- [[event-driven-architecture]]
- [[communication-structures]]
- [[coupling]]
- [[distributed-tracing]]
- [[event-driven-request-response-integration]]
