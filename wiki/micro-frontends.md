# Micro-Frontends

**Summary**: An architecture that splits the monolithic frontend into independent, business-aligned components — each with its own backing [[microservices|microservices]] — and stitches them together with a thin composition layer. Contrasts with monolithic-backend and microservice-backend-plus-monolithic-frontend approaches. Bellemare argues micro-frontends pair especially well with event-driven backends because both are compositional by nature.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`, `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-17

---

## Three frontend/backend coupling styles

Bellemare frames three approaches to organizing products and teams for customer-facing content (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- **Monolithic backend + monolithic frontend** — separate frontend and backend teams communicate through a request-response API. End-to-end business functionality crosses team boundaries, making product delivery expensive to coordinate.
- **Microservice backend + monolithic frontend** — the backend is decomposed, each service owned by a team. But a shared aggregation layer still stitches everything together for the UI. This layer suffers the tragedy of the commons: everyone depends on it, nobody owns it. Business logic leaks in through "quick wins" and cross-product boundary patches.
- **Micro-frontends** — frontend is decomposed along the **same** business bounded contexts as the backend. Each micro-frontend owns its UI slice *and* the backend microservice(s) supporting it. The aggregation layer remains but is kept free of business logic — its only job is to compose.

## Benefits

Bellemare lists several (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- **Composition-based.** Like event-driven backends, micro-frontends compose. Adding a new service to an existing UI is a matter of plugging in another micro-frontend.
- **Business-aligned.** Each micro-frontend maps to a [[bounded-context]]. You can trace requirements directly to implementation.
- **Experimentation is cheap.** Inject an experimental product without touching the codebase of core services; remove it cleanly if it doesn't land.
- **Inherits microservice advantages.** Modularity, autonomous teams, independent deployment, language/codebase independence.

The pairing with [[event-driven-microservices]] is deliberate: backend services materialize the events and entities each micro-frontend's product needs, applying business logic locally. The state-store implementation is chosen per-service to suit that product's needs.

## Drawbacks

### Inconsistent UI elements and styling

Each micro-frontend is a potential point of UI divergence (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Mitigations:

- Strong style guide.
- Lean library of common UI elements, **kept free of business logic** (all business logic lives in bounded contexts, never in the shared library).
- A stewardship model, similar to open-source projects, for coordinating shared-asset changes.

Tradeoff: sweeping changes to common UI elements may require every micro-frontend to recompile and redeploy.

### Varying performance

Micro-frontends load at different rates, or may fail to load entirely. The composite layer must handle this gracefully — spinning placeholders for slow components, degraded-mode rendering when one is down (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

### Shared-backend operational concerns

Same as any microservices deployment: duplicate code, per-service operability, deployment complexity.

## Worked example: experience search and review

Bellemare's example (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

**Version 1** — a single monolithic service materializes both experiences and reviews into a KV store. Users search by city name, see experiences plus reviews for each.

**Version 2** — three micro-frontends:

- **Search micro-frontend** with its own backend microservice. Replaces the KV store with a geospatial-capable store. Consumes user-profile events to personalize results. Supports lat-lon search.
- **Review micro-frontend** with its own backend microservice. Publishes reviews as events first, then materializes them back into its own data store. Freed from coupling to search.
- **Product micro-frontend** — the composition layer. Stitches the two together, handles geolocation translation to lat-lon, contains no business logic pertaining to either service.

Three architectural properties the example highlights:

- Reviews are published as events first, then ingested back into the store. This lets the review service be broken out into its own microservice without a data-migration project — the event stream is the single source of truth.
- Event streams as source of truth means the backend can change (state store swap, implementation-language swap) without migration pain. The database is no longer also the data communication layer.
- Observers can tell which streams each bounded context consumes just by reading the stream list — implicit documentation of which business functions use which data.

## Relationship to `ui-composition`

[[ui-composition]] (from Newman's *Monolith to Microservices*) describes UI composition as a **migration** pattern: splice new functionality into an old UI at page, widget, or micro-frontend level. "Micro frontends" appears there as the newest variant of widget composition inside single-page-application frameworks.

Bellemare's Chapter 13 framing is orthogonal: micro-frontends as a **target architecture**, steady-state rather than transitional, aligned to bounded contexts and paired with event-driven backends by design.

The two framings agree on mechanics — decomposed, independently-deployable UI pieces stitched by a composition layer — but differ on *why*: migration vs first-class architectural choice.

## Related pages

- [[event-driven-request-response-integration]]
- [[ui-composition]]
- [[event-driven-microservices]]
- [[microservices]]
- [[bounded-context]]
- [[asynchronous-ui]]
- [[serving-state-from-edm]]
- [[materialized-state]]
