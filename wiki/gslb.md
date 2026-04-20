# Global Software Load Balancer (GSLB)

**Summary**: Google's three-tier load balancer. Directs users to the closest datacenter with available capacity, then to a user-service-level frontend, then across RPC backends. Operates on symbolic service names plus per-location capacity declarations, using Google's internal naming-service addresses as its inputs.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## Three levels of load balancing

GSLB load-balances at three different levels in the request path (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. **Geographic DNS** — for requests like `www.google.com`, GSLB picks which datacenter's IP to return based on load and proximity. Covered in SRE Chapter 19.
2. **User-service level** — for a service like YouTube or Google Maps, balances traffic across service frontend instances.
3. **RPC level** — inside the datacenter, balances RPC calls across backend servers. Covered in SRE Chapter 20.

## How service owners use it

Service owners register with GSLB (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- A **symbolic name** for the service.
- A list of **naming-service addresses** of the servers implementing it.
- The **capacity** available at each location, typically in queries per second.

GSLB then routes traffic to the registered addresses, weighted by capacity and proximity. Because the naming service is already the stable naming layer for [[borg]] tasks, GSLB inherits fluid placement automatically — a task rescheduled by Borg keeps its symbolic name and GSLB keeps routing to it.

## How the DNS level actually works

Chapter 19 is the deep dive on the first level (the DNS tier). The mechanics (source: chapter-19-load-balancing-at-the-frontend.md):

- **Authoritative nameservers behind an [[anycast-dns|anycast]] address**, so DNS queries flow to the nearest Google authority instance.
- **Geographic map of known recursive resolvers**, with estimated user-base size and distribution, so the reply can be optimised for the users behind each resolver rather than for the resolver itself.
- **[[edns0-client-subnet|EDNS0 Client Subnet]]** support, so where the recursive resolver forwards the user's subnet, Google's authority can return an answer tuned to the *user*'s location rather than the resolver's.
- **Integration with live control systems** that track traffic, capacity, and infrastructure health. A datacenter experiencing a power event or running near capacity stops appearing in DNS replies.
- **Short TTLs** to bound stale-cache impact, with the understanding that some resolvers don't respect TTL.

The first level of GSLB is therefore not just "return an IP near the user" — it is "return a healthy, capacity-checked IP near the user, accepting the resolver middleman and caching constraints that [[dns-load-balancing]] imposes." Chapter 19 also makes clear that DNS alone is insufficient; the second level (service-level balancing via [[virtual-ip-address|VIPs]]) is what absorbs the limitations DNS can't fix. See [[frontend-load-balancing]] for the full layered architecture.

## Role in the Shakespeare request walkthrough

GSLB appears at every cross-machine hop in the Chapter 2 Shakespeare example (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. The user's DNS query resolves via GSLB to the nearest frontend IP.
2. An edge HTTP reverse proxy uses GSLB to find a Shakespeare frontend server.
3. The Shakespeare frontend uses GSLB to find an unloaded Shakespeare backend.

Every service-to-service hop goes through GSLB. This makes GSLB a single point of potential failure — the chapter is explicit: "a failing GSLB would wreak havoc" — which is why it is protected by rigorous testing, careful rollouts, and graceful degradation (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). See [[life-of-a-request]] for the full trace.

## Cross-book connections

- [[service-discovery]] — GSLB is Google's service-discovery plus load-balancing fusion; it goes beyond the pure-discovery role that DNS or [[zookeeper]] play.
- [[replicated-load-balanced-service]] (Burns) — GSLB is how Google implements the multi-level version of this pattern at global scale.
- [[smart-load-balancer]] (Bellemare) — partition-aware routing. GSLB is not partition-aware in the EDM sense; it is capacity-aware at the service-replica level.
- [[tail-latency-amplification]] — GSLB tries to steer around overloaded or slow backends, mitigating the tail-amplification problem.

## Related pages

- [[borg]]
- [[life-of-a-request]]
- [[service-discovery]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
- [[frontend-load-balancing]]
- [[dns-load-balancing]]
- [[anycast-dns]]
- [[edns0-client-subnet]]
- [[virtual-ip-address]]
