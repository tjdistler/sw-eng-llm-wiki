# DNS Load Balancing

**Summary**: Using the DNS resolution step itself as the first layer of [[frontend-load-balancing|frontend load balancing]] — returning different IP addresses in the DNS reply to steer users to different datacenters. The simplest implementation (multiple A/AAAA records, client picks randomly) is inadequate at scale; realistic deployments add [[anycast-dns|anycast]] on the authoritative nameservers, a geographic map of recursive resolvers, integration with capacity and health signals, and the [[edns0-client-subnet|EDNS0 client subnet]] extension to see past the recursive-resolver middleman.

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## Why DNS is a natural load-balancing point

Before a client can send an HTTP request, it has to resolve a hostname to an IP address. That resolution is a perfect hook for load balancing: the authoritative nameserver can pick *which* IP to return, and the client will connect to that one (source: chapter-19-load-balancing-at-the-frontend.md).

The simplest implementation is to return multiple A or AAAA records and let the client pick one arbitrarily. It is trivial to implement and conceptually clean. But at scale it breaks down for several reasons.

## The weaknesses of naive DNS load balancing

Chapter 19 catalogues the structural problems (source: chapter-19-load-balancing-at-the-frontend.md):

- **No control over client selection.** Clients pick records essentially at random, so each returned IP attracts roughly equal traffic regardless of capacity.
- **SRV records with weights and priorities exist but haven't been adopted for HTTP.** So the "weighted record" solution is theoretical, not operational.
- **The client usually cannot determine the closest address.** Without signals, it can't do anything intelligent with multiple returned records.
- **The 512-byte reply limit from RFC 1035** caps how many addresses fit in a single UDP DNS reply. Larger replies force a TCP fallback that adds latency and breaks the "cheap lookup" property.

These issues are all solvable (somewhat), but DNS has a deeper problem that is structural rather than protocol-level: **the middleman**.

## The recursive-resolver middleman

End users rarely talk to authoritative nameservers directly. A recursive resolver — typically run by the user's ISP or a public provider like 8.8.8.8 or 1.1.1.1 — sits between user and authority, proxying queries and caching results. This has three important implications (source: chapter-19-load-balancing-at-the-frontend.md):

### Recursive resolution obscures the client

The IP address the authoritative nameserver sees is the *resolver's* IP, not the user's. Any optimisation based on that IP optimises the wrong thing — the resolver-to-nameserver path, not the user-to-datacenter path.

- **The fix**: [[edns0-client-subnet|EDNS0 Client Subnet]], a DNS extension that lets the recursive resolver include the user's subnet in the upstream query. The authoritative server can then optimise for the user. Not yet a formal standard, but supported by OpenDNS, Google Public DNS, and the major DNS providers.

### Nondeterministic reply paths

A single ISP might run nameservers for an entire continent from one datacenter even though it has network interconnects in every metro area. Returning the "best IP for the resolver" produces a response that's wrong for most of the ISP's users.

- **The fix**: track every recursive resolver's *user-base size* and *approximate geographic distribution*, then return an IP that optimises for the majority of the users behind it. Even then, large-region resolvers require trade-offs that leave a minority of users sub-optimally routed.

### Caching and TTL

Recursive resolvers cache responses for up to the TTL the authoritative server specifies. Authoritative servers cannot flush remote caches, so TTL sets a lower bound on how quickly DNS changes propagate.

- **The mitigation**: keep TTLs short enough for fast propagation, while respecting that not every resolver respects the TTL. There isn't a fix — you live with it. This is also why DNS alone isn't enough for fast failover.

## What "best location" actually means

"Closest to the user" is the intuitive answer, but it's not sufficient on its own. The authoritative DNS server must also verify that the selected datacenter (source: chapter-19-load-balancing-at-the-frontend.md):

- **Has capacity** — enough headroom to absorb the traffic the DNS reply will direct at it.
- **Is healthy** — not experiencing power, networking, or software problems.

Google integrates its authoritative DNS with global control systems that track traffic, capacity, and infrastructure state, so the DNS reply reflects the live operational picture rather than a static geographic mapping. This integration is what turns a naive DNS setup into a real load balancer.

## Impact estimation per resolver

Because a single authoritative reply can reach anywhere from one user (tiny ISP resolver) to millions (Google Public DNS), estimating the traffic impact of a given decision is hard. Chapter 19 describes two compensating disciplines (source: chapter-19-load-balancing-at-the-frontend.md):

1. **Continuously update the known-resolvers list** with approximate user-base size behind each resolver, derived from traffic changes.
2. **Estimate the geographic distribution** of users behind each resolver so directing them to the "right" datacenter is probabilistically accurate even without per-user data.

EDNS0 makes both problems easier by moving the decision from per-resolver to per-subnet.

## Why DNS alone is not enough

Even with all of the above — anycast authoritative servers, geographic resolver maps, EDNS0, capacity integration, health signals — DNS remains a partial solution (source: chapter-19-load-balancing-at-the-frontend.md):

- **TTL bounds reaction time** on changes. You can't fail over in seconds via DNS; cached replies persist.
- **The 512-byte limit** bounds how many backends you can expose through DNS at once.
- **Client behaviour** (record selection, cache-vs-TTL compliance) is out of your control.

DNS is the simplest and most effective way to balance load *before the user's connection even starts*. But it must be followed by a second layer — [[virtual-ip-address|VIP-level load balancing]] with a [[network-load-balancer]] — to cope with what DNS can't do.

## Relationship to existing wiki concepts

### DNS as load balancer vs DNS as service discovery

In [[service-discovery]], DNS finds a service's IPs at low frequency — an initial lookup, rarely re-queried. In DNS load balancing, *every* user request starts with a DNS query and the reply drives steering. The higher query rate and the per-user reply optimisation are what make caching, TTL, and the resolver middleman operationally critical rather than ignorable.

### DNS load balancing and CDNs

The same mechanism drives CDN edge selection: your browser's DNS lookup for `cdn.example.com` returns the IP of a nearby edge node. CDNs use all of the same tricks — anycast authoritative servers, EDNS0, user-subnet geographic maps, capacity-aware replies.

### DNS load balancing and fault tolerance

Because TTLs bound reaction time, DNS is poor for failover on short timescales. Short TTLs (60 seconds or less) push the floor down but don't remove it. For rapid failover within a region, the VIP layer is the right tool: a [[network-load-balancer]] can stop forwarding to a sick backend immediately, without waiting for any DNS cache to age out.

## Related pages

- [[frontend-load-balancing]]
- [[anycast-dns]]
- [[edns0-client-subnet]]
- [[virtual-ip-address]]
- [[network-load-balancer]]
- [[gslb]]
- [[service-discovery]]
- [[site-reliability-engineering]]
