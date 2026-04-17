# Replicated Load-Balanced Service

**Summary**: The simplest multi-node serving pattern — a set of identical, stateless server replicas sitting behind a load balancer. Every replica can handle every request; replicas are added or removed to change capacity, and the load balancer provides the single stable address clients talk to. The first pattern in Part II of Brendan Burns's catalogue and the foundation the later serving patterns build on.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

A replicated load-balanced service consists of (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **A scalable number of identical server replicas.** Every replica is functionally equivalent to every other; any replica can service any request.
- **A load balancer in front of them.** Typically round-robin, or with some form of session stickiness. The load balancer provides one resolvable name that is independent of any specific replica.

This is the "simplest distributed pattern" Burns opens Part II with — and the one most practitioners already know. Its entire novelty, compared to a single-server deployment, is the load balancer plus the ability to add or remove backend instances without clients noticing.

Because replicas are identical and hold no per-request state locally, the service is trivially [[scaling-approaches|horizontally scalable]]: add replicas to handle more users, remove them when traffic falls. The load balancer ensures the new or surviving replicas start receiving traffic.

## Why stateless matters

The pattern only works cleanly when the service is **stateless** — individual requests do not depend on state retained in the serving process from previous requests (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

Burns's canonical examples:

- Static content servers.
- Middleware systems that receive and aggregate responses from numerous backends.

In such systems, every request can be routed to any replica with no behavioural difference. If the service needs state, that state lives in an external backend (a database, a cache tier, a session store) — not in the server process. When per-user affinity is needed, see [[session-tracked-services]].

## The two-replica minimum, and SLA math

Burns makes a specific argument that even very small services need at least two replicas to claim high availability (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- A three-nines SLA (99.9% uptime) allows 1.4 minutes of downtime per day.
- With a single replica, any software upgrade counts against that budget. Rolling out once a day gives you 1.4 minutes; hourly continuous delivery gives you 3.6 seconds per rollout.
- With two replicas behind a load balancer, the other replica serves traffic during a rollout or a crash and users never notice.

Two replicas are cheap; hitting stringent SLAs from a single instance is essentially impossible. This is the availability argument for replication — see [[replication]] for the general concept and [[fault-tolerance]] for why tolerating faults is preferable to preventing them.

## Why you also need a readiness probe

Replicating the service and adding a load balancer is only part of the pattern. The other essential piece is a **readiness probe** that tells the load balancer when a replica is actually ready to serve user traffic (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

Many replicas are *alive* but not yet *ready*: they may still be connecting to databases, loading plugins, or downloading serving files from the network. Without a readiness probe, the load balancer routes traffic to containers that haven't finished initializing, and users see errors.

See [[health-probes]] for the liveness-vs-readiness distinction and concrete implementation guidance.

## Kubernetes as the substrate

Burns's Chapter 5 worked example deploys a stateless NodeJS dictionary service in Kubernetes (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). The Kubernetes primitives map directly onto the pattern's two parts:

- **`Deployment`** — declares the replica count, the container image, and the readiness probe. Kubernetes maintains that many running replicas continuously.
- **`Service`** — the load balancer. Selects pods matching the Deployment's labels and exposes them behind a single resolvable DNS name.

The pattern is not Kubernetes-specific — any container orchestrator can host it — but Kubernetes's Deployment + Service split is a clean articulation of replicas + load balancer as distinct concerns.

## Caching and SSL termination as additional replicated tiers

Chapter 5's main thesis is that the basic pattern composes: any additional capability can be added as *another* replicated load-balanced tier in front of the first.

- **A caching layer** ([[caching-layer]]) fronts the application tier with replicated HTTP cache servers (Varnish in the chapter). Cache hits never reach the application tier.
- **An SSL-terminating edge** ([[ssl-termination]]) fronts the cache with a replicated nginx tier that terminates HTTPS and forwards plaintext to the cache.
- **[[rate-limiting]] and DoS defence** are pluggable onto the caching or edge layer.

Each tier is itself a stateless, replicated, load-balanced service. Burns's "complete pattern" (Figure 5-8) is three such tiers stacked: nginx SSL → Varnish cache → application. Every tier scales independently.

## Application-layer vs network-layer replication

The bare load-balanced pattern is protocol-agnostic above TCP/IP. Introducing tiers that understand the application protocol (HTTP) — caching proxies, SSL terminators, rate limiters — refines the pattern into what Burns calls **application-layer replicated services** (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). These are still stateless replicated load-balanced tiers; they just exploit HTTP-level knowledge to do more than dumb request distribution.

## Relationship to existing wiki concepts

### Scalability and horizontal scaling

The pattern is the textbook implementation of [[scaling-approaches|horizontal scaling]]. Capacity is added by provisioning more replicas — no single node becomes a bottleneck, and commodity machines suffice. See [[scalability]].

### Replication and availability

The pattern is [[replication]] applied to stateless services. Unlike database replication, there is no data to keep in sync between replicas — replicas hold no mutable state, so conventional replication concerns (lag, conflict resolution, consistency) don't apply. The benefit is pure fault tolerance and throughput scaling.

### Composing with sharding

The replicated pattern applies only when the service is stateless (or when its state fits in every replica). When the working set exceeds one replica's memory — as happens for caches of large corpora, session stores, or multiplayer game worlds — the next serving pattern in Burns's book is [[sharded-service-pattern|sharded services]] (Chapter 6), where each replica holds only a subset of the state. The two patterns combine: each shard can itself be a replicated load-balanced service, giving you both scale and resilience. See [[replicated-sharded-service]] and [[hot-sharding]].

### Composing with scatter/gather

The third serving pattern — the [[scatter-gather-pattern]] (Chapter 7) — uses replication for a third purpose: cutting single-request latency by doing a lot of parallel work at once. A robust scatter/gather deployment replicates each leaf as a load-balanced sub-service for exactly the same reliability reasons this pattern offers at the top level — leaf failures become degraded performance rather than outages. See [[tail-latency-amplification]] for why leaf-level p99 matters so much in that composition.

### Load balancers and service discovery

The load balancer abstracts replica identity from consumers. Clients resolve one stable name; the load balancer tracks which replicas are currently ready. This is an instance of [[service-discovery]]: the "set of ready replicas for service X" is the thing being discovered, and a readiness probe is how membership is decided.

### Session affinity and request routing

When requests for a single user need to land on the same replica (caching, ongoing interactions), the round-robin default gives way to session tracking. See [[session-tracked-services]].

### Relationship to single-node patterns

The chapter is the first multi-node pattern in the book. The Part I patterns — [[sidecar-pattern]], [[ambassador-pattern]], [[adapter-pattern]] — act inside a single replica (a single [[pod]]). The replicated load-balanced service wraps many such replicas behind a load balancer. All of the Part I patterns compose: each replica in a replicated service can internally use sidecars, ambassadors, and adapters as needed. Burns's Chapter 5 caching worked example specifically discusses cache-as-sidecar vs cache-as-separate-tier as a design choice (see [[caching-layer]]).

## Related pages

- [[health-probes]]
- [[session-tracked-services]]
- [[caching-layer]]
- [[rate-limiting]]
- [[ssl-termination]]
- [[scalability]]
- [[scaling-approaches]]
- [[replication]]
- [[fault-tolerance]]
- [[service-discovery]]
- [[load-parameters]]
- [[response-time-percentiles]]
- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[pod]]
- [[service-mesh]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[scatter-gather-pattern]]
- [[tail-latency-amplification]]
- [[designing-distributed-systems]]
