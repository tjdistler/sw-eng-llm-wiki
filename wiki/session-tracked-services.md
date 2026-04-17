# Session Tracked Services

**Summary**: An adaptation of the [[replicated-load-balanced-service]] pattern in which all requests from a single user are routed to the same replica, usually to maintain in-memory per-user state (caches, long-running interactions). Session tracking is typically implemented by hashing stable identifiers (source and destination IP, or an application-level cookie) to select the replica; [[consistent-hashing]] is preferred so that scaling events relocate as few users as possible.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Last updated**: 2026-04-16

---

## Why break strict statelessness

A pure stateless replicated service sends every request to any replica — maximising even load distribution and fault tolerance. Sometimes that is the wrong trade-off (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **Per-user cache hit rate.** If each replica caches a user's data in memory, landing that user on the same replica every time yields a much higher hit rate than spreading them across the fleet.
- **Long-running interactions.** Some session-based protocols keep state across requests — preferences computed once, a progressive form, a negotiated authentication handshake. Routing mid-session traffic to a different replica means losing that state.

Session tracking keeps the replication and load balancing of the underlying pattern but constrains the distribution so that each user consistently maps to one replica.

## How it's implemented

Two layers of implementation are common (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

### IP-hash affinity

The load balancer hashes the source and destination IP address of each connection and uses the hash to pick a backend replica. So long as the IPs remain constant for a user, every request from them lands on the same replica.

Limitations:

- **Works inside a cluster** where internal IPs are stable.
- **Breaks with NAT.** On the public internet, many users share outbound IPs via NAT, collapsing them onto one backend; a single user's IP can also change mid-session as they move between networks.
- **Breaks with proxy tiers in front.** If the load balancer sees the IP of an upstream cache or edge proxy rather than the user's IP, affinity collapses onto the upstream tier's address. Burns flags this explicitly in the context of a [[caching-layer]]: with a small number of large cache instances in front of the web tier, IP-based affinity sends almost all traffic to one or two replicas.

### Application-level tracking (cookie / header)

For external traffic — or whenever IP affinity is unreliable — tracking is moved up the stack. A cookie or HTTP header carrying a session ID is hashed to pick a replica. The load balancer must understand the application protocol to read the header, which is why this is an *application-layer* refinement of the pattern.

Any stable per-user identifier works: `Set-Cookie` tokens, OAuth `sub` claims, custom `X-User-ID` headers added at the edge. The essential property is that it varies per user and is carried on every request.

## Why consistent hashing matters here

Naïve hashing — `hash(user) % N` — is fine when `N` (replica count) is constant but catastrophic when it changes. Scaling up or down re-hashes almost every user to a new replica, throwing away every in-memory cache and breaking every live session (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

[[consistent-hashing]] solves this: when a replica is added or removed, only a small fraction of users get remapped. The rest stay on their current replica and their caches and sessions are unaffected. This is the same reason [[client-side-sharding|sharding ambassadors]] like twemproxy use consistent-hashing variants (ketama) for key-to-shard mapping — and why, in the caching world, consistent hashing has been standard since its original CDN use case.

Consistent hashing is therefore the default choice for any load balancer or service-mesh proxy that implements session affinity.

## The interaction with caching tiers

Adding a [[caching-layer]] in front of a session-tracked web tier introduces a subtle failure mode Burns calls out directly (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- Requests from the user no longer arrive at the web tier's load balancer with the user's source IP — they arrive with the cache tier's IP.
- If the cache tier has only two or three large instances (which is what Burns recommends for hit-rate reasons), IP affinity sends almost all web-tier traffic to a tiny number of backends. Some replicas see no traffic at all.
- Worse, two users sharing a cache proxy now share a backend replica, which was never the intent.

The correction is to switch from IP-based affinity to **cookie- or header-based** affinity once a caching layer is in play. The cache tier propagates the cookie (Varnish does by default for non-cacheable endpoints), the web-tier load balancer reads it, and user-to-replica affinity is preserved despite the upstream proxy.

## When not to use session tracking

Session tracking makes the service *less* tolerant of replica failure. If a user's replica dies, their cache or session is gone, and even after re-routing to a surviving replica they pay a cold-start cost. If the only reason for affinity is cache hit rate, consider:

- A shared cache tier (Redis, memcached) that survives replica restarts.
- Short-lived in-memory caches that tolerate being rebuilt on failover.
- Stateless-plus-fast-backend designs in which the application tier is fully stateless and all per-user state lives in an external store.

Session tracking is the right answer when in-memory state is large, expensive to rebuild, or genuinely tied to a single process (e.g. long-running connections), not just as a performance convenience.

## Relationship to existing wiki concepts

### Session tracking and the base pattern

Session tracking is a refinement of, not a replacement for, the [[replicated-load-balanced-service]] pattern. All of the base pattern's properties — horizontal scaling, [[health-probes|readiness probes]], rolling upgrades — still apply. The only change is how the load balancer picks a replica for a given request.

### Session tracking and consistent hashing

The "consistent" in "consistent hashing" means that when the backend set changes, most keys stay mapped where they were. For session tracking, "keys" are user identifiers — and "most users stay mapped where they were" is exactly the property that keeps caches warm and sessions intact across scaling events. See [[consistent-hashing]].

### Session tracking and service mesh

A [[service-mesh]] proxy can implement the session-tracking logic uniformly across the fleet — reading a cookie or header, consistent-hashing to a backend — without each service configuring its own load balancer. This is the same fleet-wide-ambassador pattern described on [[service-mesh]] extended to carry affinity state.

### Session tracking and request routing

Session affinity for stateless services is structurally similar to [[request-routing]] for partitioned databases: both map a stable client identifier to one of N backends via a hash. The difference is that partition routing is correctness-critical (the wrong node cannot answer at all), whereas session routing is only performance- or continuity-sensitive (the wrong replica *can* answer, just not with the cached state).

## Related pages

- [[replicated-load-balanced-service]]
- [[caching-layer]]
- [[consistent-hashing]]
- [[client-side-sharding]]
- [[request-routing]]
- [[service-discovery]]
- [[service-mesh]]
- [[ambassador-pattern]]
- [[designing-distributed-systems]]
