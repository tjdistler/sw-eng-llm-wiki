# EDNS0 Client Subnet

**Summary**: A DNS extension that lets a recursive resolver include the client's IP subnet in the upstream DNS query, so the authoritative nameserver can return an answer optimised for the end user rather than the resolver. The practical fix for the "the authoritative server sees the resolver's IP, not the user's" problem at the heart of [[dns-load-balancing]].

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## The problem it fixes

Without EDNS0, the only IP address an authoritative nameserver sees is the **recursive resolver's** address. This produces bad answers whenever the resolver and the user are in different places (source: chapter-19-load-balancing-at-the-frontend.md):

- A user in Seattle uses Google Public DNS (8.8.8.8). The authoritative server sees a query from one of Google's globally-distributed resolver farms. It returns an IP close to that farm — which may or may not be close to Seattle.
- A user at an ISP that runs its nameservers in one central datacenter but has interconnects in every metro gets an answer tuned to the ISP's central datacenter location.

The authoritative server has no way to tell where the actual end user is, so it optimises for the wrong leg of the path.

## How EDNS0 Client Subnet works

EDNS0 Client Subnet (the extension defined in the [Con15] reference Chapter 19 cites, now RFC 7871) adds one piece of information to the DNS query (source: chapter-19-load-balancing-at-the-frontend.md):

- The **recursive resolver** includes a *subnet prefix* of the original client's IP (e.g., `192.0.2.0/24`) in the query it forwards upstream.
- The **authoritative server** uses that subnet to select a reply tuned to the user's network location.
- The authoritative server also returns a *scope* — the subnet prefix for which this answer is valid — so the resolver knows how finely to cache the response. Different users behind the same resolver but different subnets get different cached answers.

A truncated prefix is used (typically /24 for IPv4, /56 for IPv6) so the authoritative server sees enough to geolocate without seeing the exact client IP. This is a privacy-vs-routing-quality trade-off baked into the protocol.

## Adoption and the not-quite-a-standard status

Chapter 19 notes that EDNS0 Client Subnet was not yet an official standard at the time of writing but had already been adopted by the largest DNS providers — OpenDNS and Google Public DNS are named explicitly (source: chapter-19-load-balancing-at-the-frontend.md). It has since been published as RFC 7871 (2016) with informational status.

The practical situation: EDNS0 is widely supported by public resolvers and major authoritative DNS providers, but not universal. ISP-run recursive resolvers vary. Authoritative server implementations vary. A deployment that wants to exploit EDNS0 has to handle both the with-subnet and without-subnet cases gracefully.

## What it enables

With EDNS0 Client Subnet in place (source: chapter-19-load-balancing-at-the-frontend.md):

- **Per-subnet reply optimisation.** The authoritative DNS server can run a geographic map of subnets (not just resolvers) and return the IP closest to the *user*, not the resolver.
- **Correct routing for large centralised resolvers.** Public DNS services and large-ISP setups no longer funnel users to the resolver's location.
- **Finer-grained cache scoping.** The *scope* field makes each cached answer apply only to its announced subnet, so users on different subnets behind the same resolver don't collide.

Together with [[anycast-dns]] on the authoritative side, EDNS0 is most of what makes global [[dns-load-balancing]] work cleanly for public DNS traffic.

## Relationship to existing wiki concepts

### EDNS0 and the layered frontend

EDNS0 Client Subnet is one component of the Chapter 19 recipe for [[dns-load-balancing]]. Anycast authority moves the *query* close to the resolver. EDNS0 tells the authoritative server where the *user* is. Integration with capacity and health data picks which healthy datacenter to return. Low TTLs limit stale caching. Each piece addresses a different structural weakness of naive DNS.

### EDNS0 and privacy

Sending even a truncated client subnet upstream is a privacy cost that some resolvers (and some users) refuse to pay. Cloudflare's 1.1.1.1, for example, historically did *not* forward client subnet information upstream. Deployments that want EDNS0 for routing quality have to accept that some fraction of their traffic won't carry it.

## Related pages

- [[dns-load-balancing]]
- [[anycast-dns]]
- [[frontend-load-balancing]]
- [[gslb]]
- [[site-reliability-engineering]]
