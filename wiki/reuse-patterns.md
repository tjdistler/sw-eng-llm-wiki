# Reuse Patterns

**Summary**: Hub page for the four techniques *Software Architecture: The Hard Parts* offers for handling code reuse across services in a distributed architecture: [[code-replication-pattern|code replication]], [[shared-library-pattern|shared library]], [[shared-service-pattern|shared service]], and [[sidecar-pattern|sidecar / service mesh]]. Each manages reuse along a different coupling dimension; the right choice depends on rate of change, polyglot needs, and whether the concern is domain or operational.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19

---

## Why reuse is hard in distributed architectures

In a monolith, reuse is "import the class." In a distributed architecture, every reuse decision becomes a trade-off across [[static-coupling]], [[dynamic-coupling]], change cadence, and operational characteristics (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

The chapter opens with the genre-defining slogans of the early microservices era — *"reuse is abuse!"*, *"share nothing!"*, the WET acronym (Write Every Time / Write Everything Twice) deliberately opposing DRY — but concludes that reuse is "a fact of life in software development and must be addressed." The four patterns below are the toolkit.

## The four patterns

| Pattern | Coupling axis | Bound at | Best for |
|---|---|---|---|
| [[code-replication-pattern]] | None — copy | Build of each service | Tiny, truly static one-offs (annotations, marker types) |
| [[shared-library-pattern]] | [[static-coupling|Static]] (compile-time) | Service compile | Homogeneous stack; low-to-moderate change rate |
| [[shared-service-pattern]] | [[dynamic-coupling|Dynamic]] (runtime) | Network call | Polyglot environment; frequently-changing logic |
| [[sidecar-pattern]] / [[service-mesh]] | Orthogonal (cross-cutting) | Pod assembly | Operational/cross-cutting concerns (monitoring, mTLS, tracing) |

Each pattern has its own page with full trade-offs. This page is the index.

## The decision matrix

For each candidate piece of common code, walk these questions in order (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

1. **Is the code an operational / cross-cutting concern** (logging, metrics, tracing, mTLS, circuit breaker)?
   → Push it into a [[sidecar-pattern|sidecar]] or [[service-mesh]]. This is *orthogonal coupling*: necessary across services but independent of any one domain.

2. **Is the code essentially static and tiny** (an annotation, a marker attribute, a one-off utility) and unlikely ever to change?
   → [[code-replication-pattern|Replicate]] it. Avoid the overhead of a library for code that won't churn.

3. **Is the environment homogeneous and the code's change rate low to moderate?**
   → [[shared-library-pattern|Shared library]]. Compile-time binding means no runtime risk, no scalability tax, and versioning gives controlled change. Strongly prefer fine-grained, functionally partitioned libraries.

4. **Is the environment polyglot, or does the code change frequently?**
   → [[shared-service-pattern|Shared service]]. Pay the dynamic-coupling tax (latency, scalability, fault tolerance, runtime risk) in exchange for instant rollout and language-independence.

The chapter is explicit that this is *guidance, not algorithm* — every concrete situation needs trade-off analysis (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

## Reuse via abstraction; operationalized via slow rate of change

A separate, sharper observation runs through the chapter: reuse has **two** ingredients, and architects routinely remember only the first (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

- **Abstraction** — the technique that lets us *spot* reuse candidates.
- **Slow rate of change** — the property that makes reuse actually pay off.

Things everyone successfully reuses (operating systems, open-source frameworks, well-versioned libraries) all share slow, predictable change cadence. Things that fail at reuse (the centralized "Customer service" that every domain in an insurance company must use, the [[orchestration-driven-soa|orchestration-driven SOA]] reuse-everything mandate) couple fast-changing internal concerns into a single brittle artifact.

The Chapter 8 corollary: **never make a fast-changing internal capability the target of reuse**. If you must reuse it, hide it behind a platform-style API designed for a slow external rate of change with an aggressive internal one. This is the lens through which *Hard Parts* rehabilitates reuse — it isn't bad, it just has to be applied to the right kind of code.

This connects back to the [[gather-common-domain-components-pattern]] from Chapter 5: that pattern *finds* domain reuse candidates inside a monolith; this chapter decides *what shape* each consolidated component should take in the distributed result.

## Orthogonal coupling

Chapter 8 also formalises [[orthogonal-coupling]]: two parts of an architecture with distinct purposes that must intersect to form a complete solution. Domain logic (catalog checkout) and operational logic (monitoring) are orthogonal — necessary together, independent in concern. The sidecar pattern is the architectural answer to orthogonal coupling: it lets cross-cutting concerns *cross* the architecture's domain seams without being entangled with any single domain.

## Worked Sysops Squad outcomes

The chapter's running Sysops Squad saga ends with two concrete reuse decisions (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

- **Common infrastructure logic** (monitoring, service discovery, circuit breakers, JSON-to-XML utilities) — sidecar.
- **Shared domain functionality** (common database access logic for ticketing) — choice between a *Ticket Data shared service* and a *shared library*. The chapter walks both options through trade-off analysis without dictating one.

The pattern: operational concerns get the orthogonal treatment automatically; domain concerns require explicit per-case trade-off analysis between library and service.

## Forward link: data reuse

Chapter 8 covers *code* reuse. Data reuse — how multiple services share read access to common reference data, how a [[shared-database-antipattern|shared database]] differs from a deliberate data-sharing pattern — is the subject of Chapter 10 of *The Hard Parts*. The Sysops Squad "Ticket Data service" choice teased at the end of Chapter 8 lives at the boundary between the two chapters.

## Related pages

- [[code-replication-pattern]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[orthogonal-coupling]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[gather-common-domain-components-pattern]]
- [[shared-database-antipattern]]
- [[orchestration-driven-soa]]
- [[software-architecture-the-hard-parts]]
