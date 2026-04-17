# Service Mesh

**Summary**: An architecture in which each service instance communicates with other services through its own dedicated *local* proxy (sidecar), with central control and monitoring via a control plane. Avoids the contention of a shared "smart pipe" while still centralising cross-cutting concerns like protocol translation, retries, and observability.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`

**Last updated**: 2026-04-16 (Ch 17 added — service mesh as structural feature of microservices, not bolt-on)

---

## The problem it solves

Putting a single shared proxy in front of all services lets you do useful things — protocol translation, routing, retries — but as the proxy accumulates per-service logic it becomes a shared dependency that multiple teams must coordinate to change. That undermines [[independent-deployability]] and re-introduces deployment contention (source: chapter-03-splitting-the-monolith.md).

A service mesh keeps each service's piece of the "pipe" *with* the service. Each service has its own sidecar proxy, configured for its own needs. A control plane provides centralised monitoring and policy without becoming a deployment bottleneck.

## Square's experience

Square migrated from a homegrown RPC system to gRPC with minimal disruption to each service by introducing a service mesh built on Envoy. They reduced the change required in each individual service while still centralising the new protocol's behaviour (source: chapter-03-splitting-the-monolith.md). Newman cites this as a sympathetic illustration of the pattern but notes Square ended up building something custom around Envoy because the off-the-shelf options didn't quite fit at the time.

## Newman's caution (as of writing)

Newman is conceptually positive about service meshes but warns that the tooling space took a while to stabilise. Istio appeared to be the leader but many alternatives were emerging weekly. His advice was to **let the space settle** before committing if you can (source: chapter-03-splitting-the-monolith.md).

*Note (2026): the space has largely settled. Istio and Linkerd are the dominant control-plane choices, Envoy is the de facto data-plane proxy, and the service-mesh pattern itself is mainstream rather than emerging — Newman's "wait and see" advice has been overtaken by events.*

## The sidecar as underlying primitive

A service mesh is, architecturally, a fleet-wide deployment of the [[sidecar-pattern]]. Each service runs in a [[pod]] alongside a proxy container (Envoy, Linkerd-proxy, etc.) that shares the network namespace with the application; the proxy terminates mTLS, applies retry and routing policy, and emits telemetry — all without the application being aware. The chapter-2 HTTPS-terminating nginx sidecar Burns describes (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md) is a miniature, bespoke version of what a service mesh industrializes.

Viewed this way, service-mesh adoption is a special case of the more general discipline of [[modular-reusable-containers]]: the mesh's data-plane proxy is a standard sidecar, parameterized and documented well enough to be deployed alongside every application in the organization.

## The mesh as fleet-wide ambassador

The [[ambassador-pattern]] — a coresident container that brokers the application's *outbound* connections — maps directly onto the outbound side of a service-mesh data plane. The mesh proxy does for every outbound dependency what a hand-rolled ambassador does for one: service discovery, load balancing, retries, traffic shifting, mTLS. Burns's Chapter 3 examples (sharding via twemproxy, service brokering, 10% experiment via nginx) are the single-service, bespoke versions of what a service mesh generalizes and industrializes across the fleet (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). The mesh-vs-hand-rolled-ambassador choice is the same client-side-vs-server-side-proxy-tier trade-off Burns articulates in Chapter 3: mesh proxies are a per-pod solution; a central load-balancer/gateway is the server-side alternative.

## The mesh as fleet-wide adapter

The mesh proxy also plays the [[adapter-pattern]] role for a slice of observability: regardless of what internal metrics each application emits, the mesh produces a uniform set of request-level metrics (rates, errors, latencies), access logs, and traces — a fleet-standard observability interface laid on top of whatever each application does natively (source: raw/designing-distributed-systems/chapter-04-adapters.md). That covers the cross-cutting HTTP/gRPC layer; application-specific signals (Redis hit rate, MySQL replication lag, queue depth) still need dedicated adapter containers like the ones Burns walks through in Chapter 4. In practice a production pod combines a mesh proxy (sidecar + ambassador + partial adapter) with dedicated application-specific adapters for deeper telemetry.

## The mesh and serving-pattern cross-cutting concerns

Several pieces of Burns's Chapter 5 [[replicated-load-balanced-service]] stack end up handled by the mesh proxy in a fleet-wide deployment (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **Session affinity** ([[session-tracked-services]]) — cookie- or header-based sticky-session routing can be implemented uniformly at the mesh proxy instead of being configured per load balancer.
- **mTLS** — the mesh terminates and re-establishes TLS between services, replacing internal-only SSL termination. An edge-tier [[ssl-termination]] layer is still typically needed for external HTTPS.
- **[[rate-limiting]]** — mesh control planes (Istio, Linkerd) can enforce quota policies centrally.
- **[[health-probes|Readiness/liveness]] signal propagation** — mesh proxies participate in the load-balancer membership decisions the probes drive, so the probe contract is preserved across services.

Caching ([[caching-layer]]) is *not* typically a mesh responsibility — HTTP caching still wants a dedicated tier (Varnish) sized differently from application replicas.

## Richards & Ford: the mesh as a native feature of the microservices style

Chapter 17 of *Fundamentals of Software Architecture* treats the service mesh as **a structural feature of the [[microservices]] style rather than optional infrastructure**. The sequence the chapter lays out (source: chapter-17-microservices-architecture.md):

1. Each microservice deploys with a common **sidecar** carrying the operational cross-cutting concerns (logging, monitoring, circuit breakers, etc.).
2. Sidecars wire into a **service plane** — the uniform interface each sidecar exposes to the rest of the fleet.
3. The service plane forms the **service mesh** — a holistic view of the operational aspect of the architecture.
4. The mesh becomes a **console for unified control** over cross-cutting operational concerns across the whole architecture.

The style-level consequence: the mesh is how the microservices architecture honours its *"prefer duplication to coupling"* philosophy for domain logic while still allowing legitimate coupling for operational concerns. Domain reuse is rejected; operational reuse is centralised in the mesh. This is the architectural answer to the [[orchestration-driven-soa]] failure mode of conflating the two kinds of reuse in a single ESB.

Richards and Ford also note that **service discovery** is typically part of the mesh (or the API layer). Rather than invoking a specific service instance, a request goes through service discovery, which monitors request volume and can spin up new instances to handle elasticity demands. This is what lets microservices hit the five-star elasticity and scalability ratings on the Chapter 17 scorecard — the mesh is the mechanism that makes elastic behaviour possible.

## Relationship to migration patterns

A service mesh is not itself a migration pattern but a piece of infrastructure that supports them. In particular:

- It can host the proxy used by [[strangler-fig-pattern]] without making that proxy a shared bottleneck.
- It can centralise policy for [[progressive-delivery]] (canary, traffic-shifting) across many services.

## Related pages

- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[client-side-sharding]]
- [[service-brokering]]
- [[request-splitting]]
- [[unified-monitoring-interface]]
- [[pod]]
- [[modular-reusable-containers]]
- [[strangler-fig-pattern]]
- [[independent-deployability]]
- [[rpc]]
- [[progressive-delivery]]
- [[migration-pattern-selection]]
- [[replicated-load-balanced-service]]
- [[session-tracked-services]]
- [[ssl-termination]]
- [[circuit-breaker]]
- [[bulkhead]]
