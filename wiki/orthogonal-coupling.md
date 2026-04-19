# Orthogonal Coupling

**Summary**: A *Software Architecture: The Hard Parts* term for two parts of an architecture with **distinct purposes** that nevertheless **must intersect** to form a complete solution. The canonical example is operational concerns (monitoring, logging, security) coupling across domain seams without being entangled with any one domain. Orthogonal coupling is what the [[sidecar-pattern]] and [[service-mesh]] are designed to handle cleanly.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19

---

## The definition

> In mathematics, two lines are orthogonal if they intersect at right angles, which also implies independence. In software architecture, two parts of an architecture may be orthogonally coupled: two distinct purposes that must still intersect to form a complete solution. (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md)

The classic case: **monitoring** is necessary for the system to function operationally, but it is independent of *any specific domain*. Catalog checkout doesn't care how it's monitored; monitoring doesn't care that it's checkout. They must intersect — every domain service needs monitoring — but conceptually they are perpendicular.

## Why this matters as a named concept

Most coupling discussions in distributed architecture are about parts that share a *purpose*: two services in the same domain workflow, two libraries in the same dependency graph. Orthogonal coupling names a different shape: parts that share *no* purpose but still must connect everywhere.

Naming it lets architects:

- **Spot it deliberately** — "is this concern orthogonal to the domain?" Yes → don't try to fold it into domain services; it will accumulate as cross-cutting cruft.
- **Treat it differently** — orthogonal concerns deserve orthogonal mechanisms (sidecars, service meshes, [[aspect-oriented-programming]]-style decoration), not domain-style modules.
- **Avoid false trade-offs** — "should monitoring live in each service or a shared service?" is a wrong question; the orthogonal answer is *neither*.

## The architectural answer: sidecars and service mesh

The [[sidecar-pattern]] is *Software Architecture: The Hard Parts'* recommended response to orthogonal coupling (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

- Each service runs alongside a sidecar containing the orthogonal concerns.
- The sidecar's interface forms a consistent operational layer across services.
- Wired together via a service plane, the sidecars form a [[service-mesh]] — a unified control surface for the orthogonal concerns.

The chapter likens this to the Decorator design pattern at architectural scale: *decorate* behaviour across a distributed architecture independently of normal connectivity.

## Examples that fit the orthogonal mould

- **Monitoring** — every service must be observable, in the same way, but the metrics are independent of the domain logic.
- **Logging** — uniform log shape across services regardless of what they do.
- **Tracing** — request IDs propagated through every service in a workflow.
- **mTLS / authentication** — every inter-service call must be authenticated; auth is independent of the call's domain meaning.
- **Circuit breakers / retries** — uniform reliability policies applied to every outbound call.
- **Service discovery** — every service needs to find its dependencies; the discovery mechanism is domain-agnostic.

## Examples that *don't* fit

- **Customer service** in an insurance company — every domain wants customer info, but the customer schema *is* domain logic. Treating it as orthogonal (one shared service that everyone calls) is the [[orchestration-driven-soa]] failure mode the chapter explicitly warns about.
- **Discount calculator** — the rules are domain logic, even if many services need them. This is candidate territory for a [[shared-library-pattern]] or [[shared-service-pattern]], not a sidecar.
- **Date/string formatting** — borderline; tiny formatters are usually a [[shared-library-pattern]] candidate, not orthogonal infrastructure.

The test: **does the concern's behaviour change when the domain changes?** If yes, it's domain coupling, not orthogonal. If no, it's orthogonal.

## Related pages

- [[reuse-patterns]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[orchestration-driven-soa]]
- [[software-architecture-the-hard-parts]]
