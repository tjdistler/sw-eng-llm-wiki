# Direct Server Return (DSR)

**Summary**: A [[network-load-balancer]] design where only inbound request packets traverse the balancer; backends send reply packets **directly** to the original client, bypassing the balancer entirely. Exploits the fact that many workloads (notably HTTP) are asymmetric — small requests, large replies — so forcing replies through the balancer wastes its capacity. Chapter 19 discusses two DSR-compatible delivery mechanisms: layer-2 MAC rewriting and [[packet-encapsulation-load-balancer|GRE packet encapsulation]].

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## The asymmetry that motivates DSR

HTTP is the canonical asymmetric protocol: a request is often a few hundred bytes; a response can be megabytes (a web page, an image, a video chunk). The same is true for most user-facing protocols. Forcing every reply through the load balancer doubles the balancer's traffic for no benefit (source: chapter-19-load-balancing-at-the-frontend.md).

DSR inverts the topology on the reply path: backends speak directly to clients, so the balancer's capacity is spent only on the (small) request side. Chapter 19 calls this "tremendous savings" — a balancer sized for request traffic can front a backend fleet doing far more aggregate bandwidth on the reply side.

Beyond saving capacity, DSR has a second virtue: the balancer does not have to keep reverse-translation state for replies, which is what [[network-load-balancer|NAT-based]] balancers need. A DSR balancer can be stateless (modulo any connection tracking it chooses for backend-selection stability).

## How DSR is implemented

The challenge: the backend needs to send a reply to the client as if it came from the VIP, not from the backend's own IP. Otherwise the client's TCP stack would reject the reply (wrong source address for this connection).

Two mechanisms (source: chapter-19-load-balancing-at-the-frontend.md):

### Layer-2 MAC rewriting

The balancer rewrites only the destination MAC address on the packet, leaving the IP layer untouched. The backend receives a packet still addressed to the VIP at the IP level; it processes it, generates a reply with the VIP as the source address, and sends it out — directly to the client.

- **Requires layer-2 adjacency.** Balancer and backend must be in the same broadcast domain, since MAC rewriting is a layer-2 operation.
- **Minimal overhead.** No encapsulation, no extra headers, no fragmentation risk.
- **Doesn't scale to huge fleets.** As the backend pool outgrows a single L2 segment, this approach stops working. Google outgrew it.

### GRE packet encapsulation

The balancer wraps the original packet in an outer IP+GRE header targeting the backend. The backend strips the wrapper, sees the inner packet addressed to the VIP, processes it, and sends a reply with the VIP as the source address — again, directly to the client. See [[packet-encapsulation-load-balancer]].

- **No layer-2 adjacency required.** Backend can be on a different subnet, different rack, different datacenter, different continent.
- **Adds 24 bytes of overhead** (IPv4+GRE). Can cause MTU issues.
- **Stateless like L2 rewriting**, plus scalable.

The encapsulation approach is what lets Google run DSR at its current scale (source: chapter-19-load-balancing-at-the-frontend.md).

## What DSR does *not* do

DSR is about the reply path. The balancer still has to:

- **Pick a backend for each connection.** See [[network-load-balancer]] for connection tracking and [[consistent-hashing]] fallback.
- **Forward each inbound packet** to the chosen backend (via L2 rewriting or GRE encapsulation).
- **Handle connection lifecycle.** On backend failure, connections on that backend die; the balancer must stop forwarding new connections there. This is orthogonal to the DSR property.

## Relationship to existing wiki concepts

### DSR and the VIP layer

DSR is the reply-path optimisation for [[virtual-ip-address|VIP]] load balancing. It is orthogonal to backend selection but tightly coupled to the packet-delivery mechanism: any DSR implementation needs either L2 rewriting or packet encapsulation.

### DSR and NAT

Plain NAT-based load balancers are the opposite of DSR: they mangle source and destination addresses on both legs of the connection, forcing every reply through the balancer so it can reverse the translation. DSR avoids this entirely by leaving the IP addresses intact end-to-end and delegating the reply-path delivery to the backend.

### DSR and stateless balancers

DSR is a precondition for *cheaply* running a stateless load balancer at high bandwidth. Without DSR, you'd need either connection state (to reverse NAT) or a more complex scheme. With DSR, backend selection can still use connection state if you want, but the balancer's *per-packet* work is minimal and the reply path doesn't cost the balancer anything.

## Related pages

- [[network-load-balancer]]
- [[virtual-ip-address]]
- [[packet-encapsulation-load-balancer]]
- [[consistent-hashing]]
- [[frontend-load-balancing]]
- [[site-reliability-engineering]]
