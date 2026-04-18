# Anycast DNS

**Summary**: Advertising the same IP address from multiple geographic locations and letting BGP (or the equivalent) route each querying resolver to the nearest advertisement. In [[dns-load-balancing|DNS load balancing]], the authoritative nameservers for a domain share a single anycast IP, so DNS queries flow to the *nearest* authoritative server, which can then return an IP set optimised for that region.

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## What anycast does

In normal *unicast* IP, an address identifies a single machine. In *anycast*, the same address is announced from many machines in different locations, and the network's routing layer picks which one to deliver each packet to — typically the topologically nearest advertiser (source: chapter-19-load-balancing-at-the-frontend.md).

For DNS, the usage is (source: chapter-19-load-balancing-at-the-frontend.md):

- **Every region runs its own authoritative nameserver instances**, each advertising the same anycast IP.
- **A resolver's DNS query flows to the nearest instance** by virtue of how BGP routes the anycast IP.
- **That nearest instance can return region-appropriate answers** — IPs near its own location, tuned for the assumption that most users behind the querying resolver are near the resolver.

This is a simple and deployable improvement over returning a single static authoritative IP that every resolver worldwide queries.

## Why anycast is not a complete solution

The "nearest resolver is near the user" assumption breaks down in exactly the cases Chapter 19 flags for [[dns-load-balancing|DNS load balancing]] more generally (source: chapter-19-load-balancing-at-the-frontend.md):

- **Large ISPs run their resolvers centrally**, with network interconnects in every metro. Anycast routes the ISP's query to the nameserver nearest the *resolver*, not the user.
- **Public DNS (Google, Cloudflare, OpenDNS)** serves users across the whole continent from the same anycast IP. Again, the query lands somewhere near the resolver farm, not near each individual user.

The complementary fix is [[edns0-client-subnet|EDNS0 Client Subnet]], which lets the resolver include the user's subnet in the query so the authoritative server can optimise for the *user*, not the resolver. Anycast + EDNS0 is close to what you want.

## Anycast for authoritative vs anycast for service IPs

Chapter 19 uses anycast specifically for the **authoritative nameserver** (the place DNS queries land). The IP addresses the nameserver *returns* in its replies can be anycast or unicast independently:

- **Anycast return addresses**: every datacenter advertises the service IP, and the user's actual service traffic flows to the nearest datacenter by BGP. Common for CDNs and for UDP services (DNS itself, QUIC in some configurations).
- **Unicast return addresses**: the authoritative server picks a specific datacenter's IP per reply. More common for TCP services where a BGP reroute mid-connection would break the TCP session.

Chapter 19's main treatment uses unicast return addresses chosen by the authoritative server — the control-the-reply model — and anycast only for authority.

## Relationship to existing wiki concepts

### Anycast and the layered frontend

Anycast authoritative DNS is one of several techniques layered together to make [[dns-load-balancing]] work at scale: anycast for authority, geographic maps of known recursive resolvers, integration with capacity and health signals, EDNS0 to see the user's subnet. None alone is sufficient.

### Anycast vs unicast + GSLB

Google's [[gslb|GSLB]] is in the unicast-return-address camp: authoritative DNS, informed by live capacity and health data from every datacenter, returns a specific datacenter's IP per reply. Anycast handles the authority path; GSLB's decision machinery handles the reply payload. See [[gslb]] for the three-level structure Chapter 2 describes.

## Related pages

- [[dns-load-balancing]]
- [[edns0-client-subnet]]
- [[frontend-load-balancing]]
- [[gslb]]
- [[site-reliability-engineering]]
