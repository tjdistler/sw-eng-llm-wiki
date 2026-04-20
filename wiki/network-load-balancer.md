# Network Load Balancer

**Summary**: The device (or replicated software component) sitting in front of a [[virtual-ip-address|VIP]] that receives packets destined for the VIP and forwards them to one of the backend machines behind it. Chapter 19 walks through the two main design decisions: how to *pick* a backend per connection (connection tracking vs hash-based vs [[consistent-hashing]]), and how to *forward* packets to it (NAT vs layer-2 MAC rewriting for [[direct-server-return|DSR]] vs [[packet-encapsulation-load-balancer|GRE encapsulation]]).

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## The two axes of design

Every packet-level load balancer makes two decisions per incoming packet (source: chapter-19-load-balancing-at-the-frontend.md):

1. **Which backend receives this packet?** Call this *backend selection*.
2. **How do we deliver the packet to that backend and get replies back to the user?** Call this *packet delivery*.

Chapter 19 discusses three options for each axis. The options combine mostly independently, so the overall design space is the cross product.

## Backend selection

### Least-loaded

The intuitive approach: always pick the backend with the least load. Optimal for stateless services, but breaks for stateful protocols — subsequent packets on the same connection will see a different "least loaded" backend and be routed elsewhere, tearing the connection apart (source: chapter-19-load-balancing-at-the-frontend.md).

The fix is either to do connection tracking (remember which backend got this connection) or to accept that least-loaded only works for stateless protocols.

### Hash-based (modulo N)

Hash connection-identifying fields — a tuple like (source IP, source port, destination IP, destination port) is standard — and take `mod N` to pick a backend (source: chapter-19-load-balancing-at-the-frontend.md). Properties:

- **Stateless.** The balancer stores nothing about connections.
- **Connection-stable.** Every packet on a connection hashes to the same backend.
- **Sensitive to N.** Changing the backend count changes the modulus and remaps almost every connection, forcing mass resets. Not acceptable on backend failure or during backend rollout.

Hash-based with fixed N is fine when backends never change; in reality they do, so this approach is rarely used alone.

### Consistent hashing

[[consistent-hashing|Consistent hashing]] gives the same stateless property as modulo-N but with a much smaller disruption footprint when N changes: only a small fraction of connections remap when a backend is added or removed (source: chapter-19-load-balancing-at-the-frontend.md). Introduced by Karger et al. in 1997 for CDN distribution; now the standard fallback for packet-level load balancers.

Chapter 19's specific pattern: **connection tracking in the common case, consistent hashing as the fallback under pressure** (during a denial-of-service attack, for example, when connection-tracking state would explode). The balancer tries to keep connections stable via its tracking table, but if the table fills up, it falls back to consistent hashing so existing connections still land on their original backends.

## Packet delivery

### Network Address Translation (NAT)

The balancer rewrites destination addresses on inbound packets and source addresses on outbound replies, so backends see the balancer's address as the client and clients see the balancer's address as the server (source: chapter-19-load-balancing-at-the-frontend.md). Standard LVS/iptables territory.

- **Requires connection state** on the balancer (to reverse the translation on replies). This conflicts with the stateless-fallback goal.
- **All return traffic must traverse the balancer.** For asymmetric workloads (small request, large reply — most HTTP), this bottlenecks the balancer unnecessarily.

Chapter 19 notes these disadvantages and moves on.

### Layer-2 MAC rewriting (Direct Server Return)

The balancer rewrites only the destination *MAC address* on inbound packets — layer 2 of the OSI stack — leaving the IP addresses untouched. The backend sees the original destination IP (the VIP) as if the packet had been delivered directly, and sends replies **directly to the client, bypassing the load balancer entirely** (source: chapter-19-load-balancing-at-the-frontend.md). See [[direct-server-return]].

- **Huge savings on asymmetric traffic** (small HTTP requests, large HTTP responses): only inbound packets traverse the balancer.
- **Stateless.** No NAT table needed.
- **Requires layer-2 adjacency.** The balancer and every backend must share the same broadcast domain, which breaks down as the backend fleet grows beyond what a single L2 segment can hold. Google outgrew this approach.

### Packet encapsulation (GRE)

The balancer wraps the original packet in an outer IP + GRE header destined for the backend. The backend strips the encapsulation and processes the inner packet as if delivered directly (source: chapter-19-load-balancing-at-the-frontend.md). See [[packet-encapsulation-load-balancer]].

- **No layer-2 adjacency requirement.** Balancer and backend can be in different buildings or on different continents, as long as the network routes between them.
- **Stateless.** Like L2 rewriting, no connection state required.
- **DSR-compatible.** The backend can send replies directly to the client by using the original source IP from the inner packet.
- **Adds 24 bytes of overhead** (IPv4+GRE headers). Can push packets over MTU and force fragmentation; Google mitigates by running a larger internal MTU.

Google's current VIP load balancer uses packet encapsulation ([Eis16] — the Maglev paper); it is the approach Chapter 19 endorses.

## Google's "Maglev-style" load balancer

The Chapter 19 citation [Eis16] refers to the Maglev paper. Key points that the chapter summarises (source: chapter-19-load-balancing-at-the-frontend.md):

- **Packet encapsulation via GRE** for packet delivery.
- **Connection tracking plus consistent-hashing fallback** for backend selection.
- **Stateless enough to be horizontally scaled** across many load-balancer instances, each handling a share of the VIP's traffic.
- **Direct Server Return** on the reply path — the balancer sees only request packets, not replies.

This combination is what allows a handful of balancer machines to front an essentially unlimited fleet of backends at line rate.

## Relationship to existing wiki concepts

### Network load balancer and VIP

The network load balancer is the mechanism; the [[virtual-ip-address|VIP]] is the user-facing abstraction. They are two sides of the same component.

### Network load balancer vs L7 reverse proxy

A network load balancer operates at the IP/TCP level (L3/L4) — it forwards packets without understanding application-layer content. An L7 reverse proxy like nginx, Varnish, or Google's internal edge proxy terminates TCP and speaks the application protocol. The layers stack: at Google, the VIP's network load balancer forwards packets to an edge reverse proxy, which then terminates TLS, parses HTTP, and forwards inward over the internal RPC framework — where [[datacenter-load-balancing|Chapter 20's]] application-layer balancer ([[subsetting]] + [[load-balancing-policies]]) takes over.

### Network load balancer and consistent hashing

[[consistent-hashing]] is the specific algorithm that makes stateless backend selection robust to fleet changes. It originated for CDN distribution; Chapter 19 is the explicit network-load-balancer application.

### Network load balancer and the SRE tenets

The network load balancer is a production-critical component whose design choices have major availability and capacity implications — it is the kind of infrastructure [[capacity-planning]], [[change-management-sre]], and [[release-engineering]] all apply to. A Maglev-style rollout is the kind of change a general-purpose rollout framework orchestrates.

## Related pages

- [[virtual-ip-address]]
- [[direct-server-return]]
- [[packet-encapsulation-load-balancer]]
- [[consistent-hashing]]
- [[dns-load-balancing]]
- [[frontend-load-balancing]]
- [[datacenter-load-balancing]]
- [[load-balancing-policies]]
- [[site-reliability-engineering]]
