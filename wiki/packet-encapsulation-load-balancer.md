# Packet-Encapsulation Load Balancer

**Summary**: The [[network-load-balancer]] design Google uses, in which the balancer wraps each forwarded packet inside an outer IP + GRE (Generic Routing Encapsulation) header addressed to the chosen backend. The backend strips the outer header and processes the inner packet as if delivered directly. Combined with [[consistent-hashing]] for backend selection and [[direct-server-return|DSR]] on the reply path, this is the "Maglev-like" architecture Chapter 19 endorses, and it replaces the layer-2-MAC-rewriting scheme that didn't scale.

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## What the design does

When a packet arrives at a VIP, the load balancer (source: chapter-19-load-balancing-at-the-frontend.md):

1. **Selects a backend** (via connection tracking, [[consistent-hashing]], or a combination).
2. **Encapsulates the original packet** inside a new IP packet whose outer destination is the backend's address, using **GRE** (Generic Routing Encapsulation, RFC 1701/2784) as the tunnelling protocol.
3. **Forwards the encapsulated packet** to the backend over the normal network.
4. **The backend strips** the outer IP+GRE layer and processes the inner packet exactly as if it had arrived on its own network interface — with the original source (client) and destination (VIP) IP addresses intact.

The backend then replies using the VIP as its source address, sending the reply directly to the client — the [[direct-server-return|DSR]] property — bypassing the load balancer.

## Why encapsulation beats layer-2 MAC rewriting

Chapter 19 presents encapsulation as the evolution of the L2 approach (source: chapter-19-load-balancing-at-the-frontend.md):

- **L2 rewriting requires layer-2 adjacency.** Balancer and backend must share a broadcast domain, because MAC addresses are only meaningful within one.
- **GRE encapsulation only requires IP reachability.** Balancer and backend can be on different subnets, different racks, different datacenters — as long as a route between them exists.

Google outgrew the L2 approach: once the load-balancer fleet and the backend fleet combined exceeded what a single broadcast domain could hold, layer-2 adjacency became a hard scaling ceiling. Encapsulation removes that ceiling. The chapter notes explicitly that it gives great flexibility in how the networks evolve.

## The MTU cost

Encapsulation is not free. Every encapsulated packet carries 24 bytes of extra header (IPv4 + GRE), which reduces the effective payload by the same amount (source: chapter-19-load-balancing-at-the-frontend.md). Consequences:

- **Fragmentation risk.** A packet that was exactly at the link MTU now exceeds it after encapsulation. Fragmentation is expensive and has historically been a source of interop problems.
- **Mitigation: larger internal MTU.** Google uses a larger MTU inside the datacenter network so encapsulated packets fit without fragmenting. Requires infrastructure that supports jumbo frames or larger Protocol Data Units — not always available in general-purpose networks.

This is a concrete trade-off the chapter calls out: encapsulation is flexible and scalable, but it pushes back on the network fabric in a way that layer-2 rewriting does not.

## Pairing with backend selection and DSR

Packet encapsulation is one axis of the load-balancer design space. The Chapter 19 pattern combines it with (source: chapter-19-load-balancing-at-the-frontend.md):

- **Connection tracking** in the common case, for stable backend selection.
- **[[consistent-hashing]] fallback** when tracking state would overflow (e.g., DDoS).
- **[[direct-server-return|DSR]]** on the reply path, so only request packets traverse the balancer.

Together these give a stateless-fallback, horizontally-scalable, DSR-capable load balancer that can front an essentially unlimited backend fleet. This is what the Maglev paper ([Eis16]) describes and what Google runs in production.

## Relationship to existing wiki concepts

### Encapsulation and the layered frontend

The packet-encapsulation balancer is one implementation of the [[virtual-ip-address|VIP]] layer — the second tier of [[frontend-load-balancing]] after [[dns-load-balancing]]. It is orthogonal to the DNS layer; changing how the DNS layer steers users between datacenters does not change what happens inside a datacenter once the connection arrives.

### Encapsulation and Jupiter

Google's Jupiter ([[jupiter-network]]) intra-datacenter fabric is the network that carries the encapsulated packets between load balancers and backends. Running a larger MTU in Jupiter is the infrastructure precondition that makes the encapsulation approach practical without mass fragmentation.

### Encapsulation and SDN

Encapsulation is a classic [[software-defined-networking]] move: the forwarding hardware just sees IP packets, and the intelligence lives in the controller that programs the tunnel endpoints. Maglev is often called the "SDN load balancer" for exactly this reason.

### Encapsulation vs VXLAN / IPinIP

GRE is one of several encapsulation protocols used in load balancing and networking generally. VXLAN (common in Kubernetes overlay networks), IPinIP, and GENEVE all serve similar roles. Chapter 19 uses GRE specifically because that is what Google's production load balancer uses; the design argument generalises to any tunnel protocol.

## Related pages

- [[network-load-balancer]]
- [[virtual-ip-address]]
- [[direct-server-return]]
- [[consistent-hashing]]
- [[jupiter-network]]
- [[software-defined-networking]]
- [[frontend-load-balancing]]
- [[site-reliability-engineering]]
