# Frontend Load Balancing

**Summary**: The discipline of distributing user traffic across datacenters and across the machines inside a datacenter. SRE Chapter 19's thesis: a single enormously powerful machine is not the answer — not because you can't build one, but because the speed of light bounds latency and a single point of failure is unacceptable at scale. The solution is *layered* load balancing, combining [[dns-load-balancing|DNS]], [[virtual-ip-address|VIPs]], and [[network-load-balancer|network load balancers]] to steer requests to the right datacenter and then to the right machine.

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## Why not one big machine

Chapter 19 (Piotr Lewandowski) opens by rejecting the hypothetical "single unbelievably powerful machine" solution for two reasons (source: chapter-19-load-balancing-at-the-frontend.md):

- **The speed of light.** Fiber-optic propagation delay bounds how fast a single site can serve a user on another continent. A geographically distributed fleet is the only way to hit low-latency targets globally.
- **Single point of failure.** At Google's scale, putting all eggs in one basket is a recipe for disaster. Redundancy is the operational baseline, not a tuning knob.

Given a distributed fleet, *traffic load balancing* is the question of which of the many machines in the datacenters will serve a particular request.

## There is no single "optimal"

Optimality depends on three factors (source: chapter-19-load-balancing-at-the-frontend.md):

- **The hierarchical level** — global (which datacenter) vs local (which machine inside it).
- **The technical level** — hardware vs software.
- **The nature of the traffic** — latency-sensitive vs throughput-sensitive.

Two workload examples illustrate the consequence:

- **Search request.** Latency is the dominant variable. Send it to the datacenter with the lowest round-trip time.
- **Video upload.** Throughput is the dominant variable. Route via an underutilised link, possibly to a more distant datacenter, even at the cost of higher latency.

Inside a datacenter, the approximation "all machines are equally distant to the user" is good enough, so local optimisation becomes about resource utilisation and protecting individual servers from overload. [[datacenter-load-balancing|Chapter 20]] covers that level; Chapter 19 stays at the global level.

Real deployments layer additional criteria on top: keeping caches warm by directing some traffic to a slightly more distant datacenter; routing non-interactive traffic to a completely different region to avoid congestion. Load balancing at scale is anything but static.

## The layered architecture

Chapter 19 presents frontend load balancing as a two-layer stack (source: chapter-19-load-balancing-at-the-frontend.md):

1. **[[dns-load-balancing]]** — the first layer, before the user's HTTP connection even starts. A DNS reply steers the user to a datacenter by returning the appropriate set of IP addresses.
2. **[[virtual-ip-address|VIP-level load balancing]]** — the second layer, once the user's TCP connection arrives. A [[network-load-balancer]] forwards packets from the VIP to one of many backend machines.

Neither layer alone is sufficient. DNS has caching problems, TTL limits, the 512-byte reply cap, and the recursive-resolver middleman. VIPs can't help you pick a datacenter — the client has to have arrived at the right one already. The layered composition is what works.

[[datacenter-load-balancing|Chapter 20]] then covers the *intra-datacenter* layer (service-level and RPC-level balancing, the third and fourth layers in Google's real stack): [[backend-task-states]] and [[lame-duck-state]] for identifying bad tasks, [[subsetting]] and [[deterministic-subsetting]] for bounding the connection pool, and [[load-balancing-policies]] — culminating in [[weighted-round-robin]] — for per-request backend selection.

## Stateless vs stateful, TCP vs UDP

Chapter 19's concrete discussion uses HTTP over TCP. The mechanisms mostly transfer to stateless services (DNS over UDP, for example), with the simplification that without connection state the load balancer doesn't need to pin subsequent packets to the same backend (source: chapter-19-load-balancing-at-the-frontend.md). This matters in the VIP layer — [[network-load-balancer|network load balancers]] for stateful protocols need either connection tracking or a hash-based scheme like [[consistent-hashing]] to keep a connection's packets on the same backend.

## Relationship to Google's real stack

Chapter 2 introduces [[gslb|GSLB]] as Google's three-level load balancer (DNS / service / RPC). Chapter 19 is the *deep dive* on the first level; Chapter 20 is the deep dive on the second and third. The [[google-frontend|Google Frontend]] sits between them: DNS/VIP gets the user's TCP connection to a GFE; the GFE then uses GSLB for the service-level and RPC-level hops inward. See [[life-of-a-request]].

## Relationship to existing wiki concepts

### The Chapter 19 layering vs Burns's tiered stack

Burns's three-tier [[replicated-load-balanced-service]] stack (nginx [[ssl-termination]] → Varnish [[caching-layer]] → application) is entirely *inside* the datacenter — it is the detail of a single GSLB destination. Chapter 19's machinery sits *outside* Burns's stack: DNS picks which building, VIP picks which machine inside that building, and only then does the request hit Burns's edge nginx tier. The two are not alternatives; they stack.

### DNS as service discovery vs DNS as load balancer

[[service-discovery]] uses DNS to find "where is this service" at low frequency (node IPs change rarely). Chapter 19 uses DNS to steer *every user request* across datacenters — a very different operating point that exposes DNS's structural weaknesses (TTL, caching, 512-byte replies, resolver middlemen). See [[dns-load-balancing]].

### The layered frontend as a pattern

The Chapter 19 thesis — *load balance early and load balance often* — is the frontend analogue of defense in depth. Each layer is cheap individually and failure at any one layer degrades to the next. Compare [[four-golden-signals]] as the monitoring-side "measure at every layer" pattern.

## Related pages

- [[dns-load-balancing]]
- [[anycast-dns]]
- [[edns0-client-subnet]]
- [[virtual-ip-address]]
- [[network-load-balancer]]
- [[direct-server-return]]
- [[packet-encapsulation-load-balancer]]
- [[consistent-hashing]]
- [[gslb]]
- [[google-frontend]]
- [[datacenter-load-balancing]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
