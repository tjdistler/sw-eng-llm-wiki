# Ambassador Pattern

**Summary**: A single-node multi-container pattern in which an **ambassador container** brokers interactions between an application container and the rest of the world. The application always connects to a service on `localhost`; the ambassador handles the real networking — sharding, service discovery, request splitting, or any other outward-facing concern — so the application code stays simple and unchanged.

**Sources**: `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`, `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

Ambassadors, like [[sidecar-pattern|sidecars]], are single-node patterns: two containers are coscheduled into a [[pod]] on the same machine and linked symbiotically. The distinction is which *direction* the add-on container faces (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- A **sidecar** augments the application container's *own behaviour* — TLS termination for the app's inbound traffic, dynamic config reloads, in-process introspection.
- An **ambassador** brokers the application container's *connections to the outside world* — the logic of "how do I find the right backend?" or "where should this request actually go?" is moved out of the application and into a coresident proxy.

In practice the two patterns share the same substrate (atomic container group, shared network namespace, `localhost` communication) and sometimes the same off-the-shelf tool (nginx, Envoy). The meaningful difference is intent: an ambassador's whole job is to proxy the application's outbound or backend-facing traffic, wrapping it in whatever smarter behaviour the deployment needs.

## Why the pattern is valuable

Burns gives two reasons (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

1. **Modular, reusable containers.** The same separation-of-concerns argument as for sidecars: because the ambassador is independent of the application, it can be built once and dropped in front of many different applications. The implementation is "both more consistent and of a higher quality because it is built once and used in many different contexts." This is the [[modular-reusable-containers]] discipline applied to outbound connectivity.
2. **Ease of maintenance.** Each container stays slim and focused on one job; the ambassador's complexity does not spread into application codebases.

Because ambassadors bind to `localhost` inside the pod, the application's view of the world is a single, stable endpoint — even when the real topology on the other side of the ambassador is sharded, rebalancing, or split across experimentation arms. This is a form of [[information-hiding]] at the deployment layer: the connection logic's implementation is hidden behind a stable local interface.

## The three canonical uses

Chapter 3 is organised around three concrete uses of the ambassador pattern, each substantial enough to have its own page on this wiki:

### 1. Sharding a backend service

When a storage layer is [[partitioning|sharded]] across many machines, some logic has to decide which shard gets which request. An ambassador container can hold that sharding logic and present a single `localhost` endpoint to the application. The application connects as if to a single backend; the ambassador routes each request to the correct shard. Burns's worked example is Redis sharded via twemproxy using consistent hashing. See [[client-side-sharding]] for depth.

### 2. Service brokering

When an application needs to be portable across environments — public cloud with a managed MySQL SaaS, private cloud with on-demand MySQL VMs, etc. — the [[service-discovery]] and binding logic is environment-specific. A service-broker ambassador introspects its environment and brokers the appropriate connection. The application again connects to `localhost:3306` and never knows the difference. See [[service-brokering]].

### 3. Experimentation and request splitting

A production system often wants to send some fraction of traffic to an alternative implementation — a canary, a dark-launch, a parallel-run tee. An ambassador sitting between the application and the backend can split or duplicate requests according to configurable rules. Burns's example is an nginx ambassador that weight-routes 10% of traffic to an experimental backend. See [[request-splitting]].

All three uses share the same mechanical shape: the application sees a single local endpoint; the ambassador applies outward-facing logic; the application code is unchanged.

## The client-side / server-side trade-off

For each of the three uses, there is an alternative: deploy the same logic as a standalone network service in front of the backend instead of as a client-coresident ambassador. Burns calls the server-side version "a distributed ambassador as a service" (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

The trade-off he articulates:

- **Client-side ambassador** — simpler to deploy the backend (no extra proxy tier), more complex to deploy each client (it must now carry the ambassador container in its pod). Good when the logic is lightweight and stable.
- **Server-side proxy** — simpler clients, but the proxy fleet becomes another service to scale, monitor, and maintain. Good when the logic is longstanding and shared across many clients.

Burns is explicit that either choice is valid, and that the right answer depends on "particulars of your specific application": where team lines fall, whether you are writing code or deploying off-the-shelf software, and how long-lived the logic is likely to be. For experimentation in particular, occasional use argues for client-side ambassadors while permanent infrastructure argues for a server-side tier (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

This is the same design tension that underlies [[service-mesh]] vs shared-proxy architectures: per-service coresident proxies avoid the shared-bottleneck problem but push deployment complexity to every pod.

## Relationship to sidecars and adapters

Mechanically, an ambassador is a particular kind of sidecar — a container that shares the application's pod and network namespace. The chapter positions it as a sibling pattern rather than a subtype because of intent. With the Chapter 4 [[adapter-pattern]] now in the wiki, the Part I trilogy can be laid out cleanly (source: raw/designing-distributed-systems/chapter-04-adapters.md):

| Aspect | [[sidecar-pattern]] | Ambassador (this page) | [[adapter-pattern]] |
|---|---|---|---|
| Intent | Augment the app's own behaviour | Broker the app's outbound / backend connections | Transform the app's outward interface to a fleet standard |
| Traffic direction | Inbound or in-pod | Outbound | Outbound observation / probe |
| Canonical example | nginx terminating HTTPS for a legacy HTTP service | twemproxy sharding Redis; nginx splitting 10% experiment traffic | Redis-to-Prometheus exporter; fluentd log normaliser; MySQL rich health check |
| Application view | "My pod now has HTTPS" | "I connect to `localhost` and get the right backend" | (Unchanged from app's perspective; the rest of the fleet now sees a standard interface) |

In real deployments the line blurs: an Envoy instance in a [[service-mesh]] is structurally a sidecar but behaves as an ambassador for outbound traffic and as an adapter for standardised telemetry.

## Relationship to existing wiki concepts

### Ambassadors and service mesh

A [[service-mesh]] is, operationally, a fleet-wide deployment of ambassador-pattern proxies (plus sidecar-pattern ones). Each service instance runs with a local Envoy/Linkerd proxy that handles outbound service discovery, load balancing, retries, and traffic shifting — exactly the concerns that Chapter 3's examples factor out. The ambassador pattern is the single-service, hand-rolled version of that story.

### Ambassadors and RPC

Historically, [[rpc]] frameworks baked service discovery, load balancing, and retry logic into client-side libraries. The ambassador pattern moves that logic out of the client library and into a coresident container, making the client code language-agnostic and keeping the smart logic reusable across applications.

### Ambassadors and progressive delivery

Request-splitting ambassadors are one of the most direct implementations of [[progressive-delivery]] techniques — canary releases, dark launches, parallel runs. See [[request-splitting]].

### Ambassadors and partitioning

Client-side sharding is a specific instance of the ambassador pattern applied to [[partitioning]]; see [[client-side-sharding]] and [[request-routing]] for how it fits with DDIA's partitioning vocabulary.

### Ambassadors as work-queue sources

Burns's [[work-queue-pattern|Chapter 10]] picks up the ambassador again, this time in the batch context: the producer side of a work queue is an **application-specific source ambassador** that proxies the generic queue-manager's "give me the items" request out to the real backing store — a cloud-storage bucket, an NFS share, a Kafka or Redis topic (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The queue-manager connects to `localhost:8080` and never learns what the store actually is. See [[source-container-interface]].

Chapter 11 then composes source ambassadors: the [[filter-pattern]] is a source ambassador that wraps another source ambassador and applies a predicate, returning the filtered list transparently (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Ambassador-on-ambassador composition is one of the cleanest uses of the pattern in Burns's catalogue — each layer is narrow, each is reusable, the downstream work queue is unchanged. See [[event-driven-batch-pattern]] for the full workflow picture.

### Ambassadors and sharded services

Burns's [[sharded-service-pattern|Chapter 6]] revisits the ambassador as one of two deployment options for the "root" router of a sharded service (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). Chapter 3 covers the *client side* of the sharded service (how an application connects to one via an ambassador); Chapter 6 covers the *service side* (how the sharded service itself is built, and what shard-router deployment options exist). The per-pod ambassador and the shared shard-routing service are the two ends of the same client-side/server-side trade-off this page describes.

## Design discipline

Because ambassadors are long-running, general-purpose containers, they benefit from the same three-part discipline Burns lays out for all reusable containers (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

1. Parameterize the ambassador (e.g. shard list, upstream service name, split ratio).
2. Define the API surface — including the protocol it proxies, the config-file shape, and the signals/endpoints it exposes.
3. Document how to use it.

See [[modular-reusable-containers]] for the full treatment.

## Related pages

- [[sidecar-pattern]]
- [[adapter-pattern]]
- [[pod]]
- [[modular-reusable-containers]]
- [[client-side-sharding]]
- [[service-brokering]]
- [[request-splitting]]
- [[service-mesh]]
- [[service-discovery]]
- [[request-routing]]
- [[partitioning]]
- [[information-hiding]]
- [[rpc]]
- [[progressive-delivery]]
- [[sharded-service-pattern]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[event-driven-batch-pattern]]
- [[filter-pattern]]
- [[designing-distributed-systems]]
