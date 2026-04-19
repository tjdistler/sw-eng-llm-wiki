# Static Coupling

**Summary**: How the pieces of a distributed architecture are **wired together** — the operational dependencies (OS, frameworks, libraries, databases, message brokers, container orchestrators, URLs/IPs), contracts, and topology that must be in place for a quantum to *bootstrap and run*. One of the two orthogonal axes of architectural coupling in *Software Architecture: The Hard Parts*; the other is [[dynamic-coupling]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`

**Last updated**: 2026-04-19

---

## Definition

> Static coupling represents how static dependencies resolve within the architecture via contracts. These dependencies include operating system, frameworks, and/or libraries delivered via transitive dependency management, and any other operational requirement to allow the quantum to operate. (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md)

Ford, Richards, Sadalage, and Dehghani draw a sharp line between two senses of "coupling" that architects routinely conflate (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **Static coupling** — *how services are wired together*. A service plus its database plus its OS plus its frameworks plus its upstream libraries plus its URLs and IPs. Visible on a deployment diagram.
- **[[dynamic-coupling]]** — *how services call one another at runtime*. Visible only under load.

A service depends on its database for static coupling (the service isn't operational without it). That same service may call another service during a workflow — that's dynamic coupling. Neither service requires the other to be present to function, except during that runtime workflow (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md).

Part I of *The Hard Parts* ("Pulling Things Apart") is entirely about static coupling. Part II ("Putting Things Back Together") is about dynamic coupling.

## The bootstrap question

The crisp test for whether something belongs in a quantum's static coupling set:

> Is this dependency of the architecture necessary to bootstrap this service? (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md)

If yes, it's part of the static coupling, and the service cannot form its own [[architectural-quantum]] independent of it. This includes transitive dependencies: even in a broker-style event-driven architecture, if some services don't directly access the database but *rely on services that do*, those upstream services become part of the same static coupling envelope.

## What counts as static coupling

The Chapter 2 enumeration (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **Operating system** the service runs on
- **Frameworks** and runtime platforms
- **Libraries** delivered via transitive dependency management
- **Data stores** — databases, caches, embedded stores the service reads/writes
- **Message brokers** the service binds to for its core operation
- **Container orchestration** substrate (Kubernetes, ECS, etc.)
- **Coupling points** such as IP addresses and URLs baked into configuration
- **Method signatures and contract formats** (REST, SOAP, gRPC schemas) — contracts are a first-class static-coupling concern covered in Chapter 13
- **User interfaces** if the backend cannot legitimately run without the UI (and vice versa)

The common thread: "any other operational requirement to allow the quantum to operate." If it must be running for the service to correctly serve its first request, it is part of the static coupling.

## Static coupling and the architecture quantum

The static-coupling measure **defines quantum boundaries**. An [[architectural-quantum]] is, in part, a measure of high static coupling — things that are wired together at the operational level belong in the same quantum (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md).

The measure is simple for most topologies:

| Architecture | Static coupling → quanta |
|---|---|
| Monolithic (any style, single DB) | **1** — the DB is part of the quantum; everything shares it |
| [[service-based-architecture]] | **1** — individual services, but one shared relational DB |
| Mediated event-driven | **1** — DB + request orchestrator both couple everything |
| Broker event-driven with one DB | **1** — shared DB still collapses the quantum |
| Broker event-driven with separate data stores and no cross-static-deps | **many** — each standalone subsystem is its own quantum |
| [[microservices]] with per-service DBs and no UI coupling | **many** — each service is its own quantum |
| Microservices coupled through a single monolithic UI | **1** — UI is a static coupling point across the backend |
| Micro-frontend microservices | **many** — each service + its UI fragment forms its own quantum |
| Two independent systems sharing a DB | **1** — shared DB is a coupling point even across system boundaries |

*Any holistic coupling point necessary for the architecture to function forms an architecture quantum around it.* A shared database, a central orchestrator, a tightly-coupled UI — each collapses its surroundings into one quantum. Conversely, absence of such shared points is what enables multiple quanta.

## Why this matters

Richards and Ford make three practical cases for the static coupling lens (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **Legacy archaeology.** A static quantum diagram of a legacy system — drawing what is wired to what — is a cheap, high-leverage way of understanding the blast radius of any change. "What systems will be impacted by change" becomes a visible question rather than a tribal one.
- **Decomposition planning.** To pull a system apart, you first need to see where it's glued together. Static coupling analysis finds the glue: shared databases, shared orchestrators, shared UI surfaces, shared libraries.
- **Quantum scoping.** Architecture characteristics ([[architecture-characteristics|scalability, availability, security]]) scope to a [[architectural-quantum|quantum]], and the quantum is defined by its static coupling envelope. Until you know what's in the envelope, you cannot reason about characteristics per subsystem.

## The reuse-pattern lens

Chapter 8's [[reuse-patterns]] choices map directly onto the static-coupling axis. Each reuse pattern adds a different kind (or amount) of static coupling to consuming services (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

| Reuse pattern | Effect on static coupling |
|---|---|
| [[code-replication-pattern]] | **None** — nothing is wired together; each service ships its own copy |
| [[shared-library-pattern]] | **Adds static coupling** — the library becomes part of each consumer's compile-time dependency envelope and must be present to build/boot |
| [[shared-service-pattern]] | **Does not add static coupling** — the coupling is [[dynamic-coupling|dynamic]] (runtime) because callers bootstrap without the shared service; they just fail if it's unavailable at request time |
| [[sidecar-pattern]] / [[service-mesh]] | **Adds per-pod static coupling** to the sidecar container, but not to any peer service — the sidecar joins the deployment unit, not the domain graph |

This is why the chapter treats the four reuse patterns as fundamentally different: they bind at different points in the static/dynamic coupling lattice. A shared library extends every consumer's static quantum envelope; a shared service leaves it alone but adds a [[dynamic-coupling|runtime call]]; a sidecar changes the shape of each pod's static envelope without introducing cross-quantum wiring.

## Contracts are the static-coupling primitive

Architects recognise REST or SOAP as contract formats, but *method signatures* and *operational dependencies* (IP addresses, URLs) are contracts too (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md). Every static-coupling point is a contract, whether explicit (a schema) or implicit (a hardcoded URL). Chapter 13 of the book treats contract design as the central "hard part" of managing static coupling across quantum boundaries.

This is the bridge back to [[connascence]]: static connascence (name, type, meaning, position, algorithm) is the code-level vocabulary for the *strength* of a contract-level coupling. Architectural static coupling adds the operational substrate — the database, the broker, the OS — that code-level analysis alone can't see.

### Chapter 13 — the contract-strictness dial

Chapter 13 formalises the above with the **[[contracts|strict-to-loose contract spectrum]]** (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). Every static-coupling point admits a strictness choice:

- **[[strict-contract|Strict]]** contracts (RMI, gRPC, SOAP/XSD, versioned REST+schema) tighten the static coupling — the consumer must bootstrap with matching names, types, and ordering, and a change on one side forces a matching change on the other.
- **[[loose-contract|Loose]]** contracts (JSON name-value pairs) weaken the static coupling — the consumer only needs the names of fields it reads; producer changes rarely cascade.

Contract design is therefore the **primary lever** for controlling how much static coupling an architect introduces at each quantum boundary. Chapter 13's microservices recommendation — loose contracts plus [[consumer-driven-contracts|CDCs]] as [[architecture-fitness-function|fitness functions]] — is a prescription for the minimum workable static coupling at a service boundary.

The [[stamp-coupling]] anti-pattern is the worked cautionary tale: over-specifying a contract introduces more static coupling than the domain requires, inheriting breakage from fields no one reads and bandwidth cost for data no one uses.

## Not the same as Newman's taxonomy

Newman's [[coupling]] page enumerates four types (implementation, temporal, deployment, domain) scoped to microservice interactions. *The Hard Parts'* static/dynamic split is a different axis — it asks not *what kind* of coupling but *when the coupling binds*:

- Newman's **implementation** and **deployment** coupling are primarily static.
- Newman's **temporal** coupling is dynamic.
- Newman's **domain** coupling spans both — the dependency is static, but how it's realised at runtime is a dynamic choice.

The frameworks compose rather than replace each other. Use Newman for service-interaction typology; use static/dynamic for quantum analysis.

## Related pages

- [[dynamic-coupling]]
- [[architectural-quantum]]
- [[coupling]]
- [[connascence]]
- [[software-architecture-the-hard-parts]]
- [[service-based-architecture]]
- [[microservices]]
- [[event-driven-architecture]]
- [[shared-database-antipattern]]
- [[independent-deployability]]
- [[reuse-patterns]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[stamp-coupling]]
- [[consumer-driven-contracts]]
