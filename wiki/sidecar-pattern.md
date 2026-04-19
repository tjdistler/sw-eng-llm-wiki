# Sidecar Pattern

**Summary**: A single-node pattern made up of two coscheduled containers — an application container that holds the core logic, and a sidecar container that augments or extends the application container, often without the application container's knowledge. The sidecar shares filesystem, network, and other namespaces with the application via a [[pod]]-style atomic container group.

**Sources**: `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`, `raw/building-event-driven-microservices/chapter-10-basic-producer-and-consumer-microservices.md`, `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19
---

## The shape of the pattern

The sidecar pattern is the first of Burns's single-node patterns. Two containers are grouped into an atomic unit and scheduled together on the same machine (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

- The **application container** holds the core logic. Without it, the application would not exist.
- The **sidecar container** augments and improves the application container. It often does so transparently, without the application container being aware of it.

The two containers share filesystem paths, hostname and network namespace, and other Linux namespaces (like PID). The sharing is what makes the pattern possible: a sidecar can see the application's processes, listen on the same loopback interface, or watch a directory the application reads from.

Coscheduling is enforced by an atomic container group — the [[pod]] API object in Kubernetes is the canonical example (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

## Four illustrative uses

Burns gives four worked examples that span the range of sidecar motivations.

### 1. Adding HTTPS to a legacy HTTP service

A legacy web service speaks only unencrypted HTTP, but company policy now mandates HTTPS. The original build system no longer works, so rebuilding is expensive (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

The sidecar solution:

- Bind the legacy service to `127.0.0.1` only, so nothing outside the pod can reach it directly.
- Add an nginx sidecar in the same network namespace. It terminates HTTPS on the pod's external IP and proxies decrypted traffic to the legacy service over loopback.
- The unencrypted leg never leaves the pod, so the security team is satisfied.

The legacy application was modernized without touching its code. This is the archetypal [[legacy-modernization]] use of the pattern.

### 2. Dynamic configuration synchronization

An older application reads its configuration from a file on disk. Cloud-native deployments want configuration pushed via an API — both for ease of use and to enable automation like rollback (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

The sidecar solution:

- The sidecar and application share a directory containing the config file.
- The sidecar watches a configuration API and, when it detects a change, writes the new file and signals the application.
- Signalling mechanisms vary: some applications watch the file; some respond to `SIGHUP`; in extreme cases the sidecar sends `SIGKILL` and lets the orchestrator restart the application, which then reloads fresh config on startup.

Again, the application is unchanged.

### 3. Modular utility containers: the `topz` example

Not every sidecar exists to adapt a legacy system. A second major motivation is **modularity and reuse** (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

Burns's example is a `topz` sidecar: an HTTP server that exposes process-level resource usage (like the `top` command) over `/topz`. Deployed as a sidecar sharing the PID namespace with the application container, it works uniformly across every language without requiring each team to implement a `/topz` endpoint in their own framework.

Because orchestration systems can automatically inject the sidecar into every pod, the result is consistent introspection across the whole infrastructure — with zero application changes and zero duplicated effort.

The trade-off Burns flags: a sidecar is always somewhat less tailored than hand-written in-process code. He compares it to buying off-the-rack clothing vs bespoke — the bespoke option fits better but costs more to acquire. For most applications, the general-purpose modular container is the right call.

### 4. A simple PaaS built around git

The pattern can also implement the full deployment model for an application. Burns sketches a simple PaaS where a `git push` deploys new code to running servers (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

- Application container: a Node.js server running under `nodemon`, which reloads on file change.
- Sidecar: a shell loop that does `git pull` every 10 seconds into the shared filesystem.

Pushing to the repo updates the file, `nodemon` detects the change, and the server reloads. The sidecar provides the entire deployment mechanism as a reusable, composable component.

## Why the pattern works

The sidecar pattern is possible because of two substrate properties:

1. **Atomic container groups** ([[pod]]s) — the guarantee that two containers are scheduled together on the same node and share namespaces.
2. **Shared namespaces** — filesystem, network, PID, and others — let the sidecar observe or augment the application through well-understood OS primitives, not bespoke glue code.

Without these two pieces, you could only communicate across containers via the network, and the sidecar pattern would collapse into something much less useful.

## Motivations in summary

Burns identifies two broad motivations for reaching for a sidecar (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

1. **Legacy modernization** — adapt a pre-existing application to new requirements (HTTPS, dynamic config, observability) without changing its source. See [[legacy-modernization]].
2. **Modularity and reuse** — factor cross-cutting functionality into standalone containers that any application can compose with. See [[modular-reusable-containers]].

Both motivations share a single core idea: **add capability to an application through a separate deployable unit, not through changes to the application itself.**

## Relationship to existing wiki concepts

### Sidecars and information hiding

The sidecar pattern is [[information-hiding]] applied at the deployment layer. The application container's internals — the fact that it only speaks HTTP, that it reads config from a file, that it exposes no `/topz` endpoint — stay hidden behind a stable sidecar-augmented pod interface. Consumers of the pod see HTTPS, live config, and standardized introspection; the application is free to keep its implementation as it is.

### Sidecars and coupling

By moving cross-cutting functionality into a separate container, the sidecar pattern reduces [[coupling]] between the cross-cutting concern and the core application. The nginx HTTPS sidecar is not linked into the application's binary, is not statically bound to its build system, and does not need to be rewritten when the application is. Deployment coupling (see [[coupling]]) is reduced: the TLS logic and the business logic can ship on independent cadences.

### Sidecars and the service mesh

The [[service-mesh]] pattern — per-service local proxies with a central control plane — is one of the largest-scale applications of the sidecar idea. Each service instance runs alongside a sidecar proxy (Envoy, Linkerd, etc.) that handles mutual TLS, retries, traffic shifting, and observability. The chapter's nginx HTTPS example is a miniature service-mesh primitive.

### Sidecars and microservices

In a [[microservices]] architecture, the sidecar is the substrate for pushing cross-cutting concerns — TLS, metrics, tracing, config — out of each service and into reusable infrastructure. This enables service teams to keep their services small and focused while still meeting organization-wide operational requirements, supporting [[independent-deployability]].

Chapter 17 of *Fundamentals of Software Architecture* elevates this from an implementation detail to a **defining structural feature of the microservices style**. Richards and Ford pose the question directly: microservices prefer duplication to coupling for domain concerns, so how does the style handle the operational concerns that genuinely do benefit from coupling (monitoring, logging, circuit breakers, service discovery)? Their answer is the sidecar pattern (source: chapter-17-microservices-architecture.md):

- **Each service gets a common sidecar** containing the operational cross-cutting concerns. Owned by individual teams or, more commonly, a shared infrastructure team.
- **Upgrading the monitoring tool across the fleet is a sidecar update**, not a fleet-wide code change across every microservice. One team upgrades one container definition; every service receives the new functionality on next deploy.
- **Clean separation of concerns** — domain logic lives inside the bounded-context service with duplication accepted; operational logic lives inside the sidecar with reuse encouraged. This is the structural answer to the [[orchestration-driven-soa]] critique that conflated domain and operational reuse.

Richards and Ford explicitly frame the fleet-wide deployment of sidecars connecting via a service plane as the [[service-mesh]] — which, in their catalog, is not a bolt-on but a native part of the microservices style.

## The sidecar as the cleanest cross-cutting reuse pattern

Chapter 8 of *Software Architecture: The Hard Parts* positions the sidecar pattern as one of four [[reuse-patterns]] available in distributed architectures, alongside [[code-replication-pattern|replication]], [[shared-library-pattern|shared libraries]], and [[shared-service-pattern|shared services]]. The first three handle *domain* reuse along the static or dynamic coupling axis. The sidecar handles the **orthogonal** case (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

- Operational concerns (monitoring, logging, mTLS, circuit breakers, service discovery, auth) must intersect with every service, but are *independent* of any one domain — the definition of [[orthogonal-coupling]].
- Folding them into each service's code couples them to that service's lifecycle and tech stack. Building one big shared service for them creates a fault-tolerance and scalability bottleneck. Building one library per language multiplies effort across polyglot teams.
- The sidecar is the cleanest answer: package the cross-cutting concern as its own container, deploy it alongside every service, and keep its lifecycle independent of the domain code it accompanies.

The chapter draws an explicit analogy: the sidecar plays the role of the Decorator design pattern at architectural scale — *decorating* behaviour across a distributed architecture independent of the normal service-to-service connectivity.

This is the structural reason microservices' *"prefer duplication to coupling"* slogan doesn't break down for operational concerns: the duplication that *would* be needed to keep operational logic out of every service is replaced by a single sidecar definition deployed everywhere. The trade-off — orthogonal reuse without entangling domain concerns — is what makes the pattern a load-bearing piece of modern microservices, not just an option.

The Sysops Squad outcome in Chapter 8 follows this exact reasoning: monitoring, service discovery, circuit breakers, and even some utility functions (the JSON-to-XML library) get packaged into the sidecar; common *domain* code (database access for the ticketing flow) is debated as shared library vs shared service instead.

## Requirements for a good sidecar

The chapter closes by arguing that sidecars — to deliver on their modularity promise — need disciplined design. Three focus areas (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

1. **Parameterize** the container so it is configurable for different deployments.
2. Design the container's **API surface** — not just its HTTP API, but every observable behaviour — carefully, because consumers depend on all of it.
3. **Document** how to use the container.

All three are covered in depth on [[modular-reusable-containers]].

## A worked case of when not to use a sidecar

Chapter 5's caching discussion (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md) contains a rare explicit "don't use a sidecar here" case. Running a Varnish cache as a sidecar in every application pod is the *simplest* deployment of a cache, but it forces the cache and the application to scale together — and because each sidecar cache holds its own copy of the working set, ten small cache sidecars store ten copies of the same content, gutting the hit rate. Chapter 5 therefore recommends deploying the cache as a separate [[replicated-load-balanced-service]] tier (few large replicas, many small app replicas), not as a sidecar. See [[caching-layer]] for the full argument. This is a useful corrective case: the sidecar pattern is not always the right answer, and the sizing asymmetry between two workloads is a good test for whether they should share a pod.

## Sidecars in event-driven microservices

Bellemare reaches for the sidecar pattern in Chapter 10 of *Building Event-Driven Microservices* for the same reason Burns does: modernizing legacy systems without changing their code (source: chapter-10-basic-producer-and-consumer-microservices.md).

The worked example is an ecommerce frontend that sources its product and stock data from a read-only subordinate database via a scheduled batch job. The modernization goal is to replace batch synchronization with a near-real-time feed from two event streams (`products` and `stock-levels`) — but the frontend's code cannot be safely changed.

The sidecar solution:

- A [[basic-producer-consumer-microservice|BPC]] sidecar runs in the same deployable as the frontend.
- It consumes the two event streams and **upserts the events into the frontend's local data store**, which the frontend already reads from.
- The frontend sees near-real-time updates without any code change.

This is [[event-sinking]] implemented as a sidecar: an external source of truth (the event broker) is projected into a downstream system's data store through a coresident container. Bellemare notes that the sidecar must be part of the *single deployable* of the frontend — which means additional integration tests, because the sidecar's correctness is now load-bearing for the frontend's data freshness.

The broader point Bellemare makes: the sidecar pattern "allows you to add new functionality to a system without requiring significant changes to the legacy codebase" — exactly the Burns framing, applied to EDM integration rather than HTTPS termination or config sync.

## Sibling patterns: ambassador and adapter

Chapters 3 and 4 of the book introduce the [[ambassador-pattern]] and [[adapter-pattern]], the sidecar's two sibling patterns. All three are single-node multi-container patterns built on a shared [[pod]] and `localhost` communication; all three factor cross-cutting concerns into a separate container. The distinction is intent (source: raw/designing-distributed-systems/chapter-03-ambassadors.md; raw/designing-distributed-systems/chapter-04-adapters.md):

| Pattern | Intent | Canonical examples |
|---|---|---|
| Sidecar (this page) | Augment the application's *own behaviour* | nginx HTTPS termination, config sync, `topz` introspection |
| [[ambassador-pattern]] | Broker the application's *outbound / backend* connections | twemproxy sharding, service-broker probes, 10% experiment split |
| [[adapter-pattern]] | Transform the application's *outward interface* to match a fleet standard | Prometheus exporter, fluentd log normaliser, HTTP health-check wrapper |

In real deployments the line blurs (an Envoy in a [[service-mesh]] does bits of all three), but at the pattern-catalogue level they are three different applications of the same substrate.

## Related pages

- [[pod]]
- [[modular-reusable-containers]]
- [[legacy-modernization]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[service-mesh]]
- [[information-hiding]]
- [[coupling]]
- [[microservices]]
- [[independent-deployability]]
- [[caching-layer]]
- [[replicated-load-balanced-service]]
- [[designing-distributed-systems]]
- [[basic-producer-consumer-microservice]]
- [[event-sinking]]
- [[reuse-patterns]]
- [[orthogonal-coupling]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
