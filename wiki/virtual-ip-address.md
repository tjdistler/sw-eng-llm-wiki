# Virtual IP Address (VIP)

**Summary**: An IP address that is not bound to any single network interface but is instead *shared* across many machines, with a [[network-load-balancer]] in front routing packets to one of the machines behind it. From the user's perspective the VIP is a single, regular IP address; the number of backends, their identities, and their lifecycle are completely hidden. The second layer of [[frontend-load-balancing]] — what [[dns-load-balancing|DNS]] resolves *to*.

**Sources**: `raw/site-reliability-engineering/chapter-19-load-balancing-at-the-frontend.md`

**Last updated**: 2026-04-17

---

## What a VIP is

A VIP is an IP address that (source: chapter-19-load-balancing-at-the-frontend.md):

- **Is not assigned to a specific network interface.** Instead it is shared across many devices.
- **Looks like a regular IP address to the user.** Clients resolve the service name, get a VIP, and make a normal TCP or UDP connection to it.
- **Is fronted by a network load balancer.** The balancer receives packets destined for the VIP and forwards them to one of the backend machines.

This is the mechanism that lets a service grow, shrink, and swap backends without users noticing. The VIP stays the same; the set of machines behind it changes freely.

## Why VIPs are the second load-balancing layer

[[dns-load-balancing|DNS]] can steer a user to a datacenter, but it cannot steer to a specific machine — its granularity is an IP address, and even that is cached at TTL granularity. VIPs pick up where DNS leaves off (source: chapter-19-load-balancing-at-the-frontend.md):

- **DNS resolves to a VIP**, not to a real backend IP.
- **The network load balancer** distributes the VIP's incoming packets across healthy backends.
- **Backend failure or maintenance** is absorbed by the load balancer, which simply stops forwarding to the affected backend — no DNS change, no client cache to wait out, no user-visible outage.

The two layers compose: DNS handles the coarse-grained "which datacenter", VIP handles the fine-grained "which machine inside it."

## What the load balancer must do

The [[network-load-balancer]] sitting in front of a VIP has two main jobs (source: chapter-19-load-balancing-at-the-frontend.md):

1. **Pick a backend for each new connection.** Strategies range from "least loaded" to hash-based selection to [[consistent-hashing]]. Each has trade-offs.
2. **Forward packets to that backend.** Approaches include Network Address Translation, layer-2 MAC rewriting for [[direct-server-return]], and [[packet-encapsulation-load-balancer|packet encapsulation]] (GRE).

Chapter 19 spends most of its VIP section on these two design axes. See [[network-load-balancer]] for the backend-selection discussion, [[direct-server-return]] for the asymmetric-traffic optimisation, and [[packet-encapsulation-load-balancer]] for the approach Google actually uses.

## Stateful vs stateless backend selection

Stateless services let the load balancer pick any backend per packet. Stateful services — most notably TCP connections — require that every packet belonging to a single connection is routed to the same backend for the connection's duration (source: chapter-19-load-balancing-at-the-frontend.md).

Two ways to achieve that:

- **Connection tracking.** The balancer remembers which backend got each connection and routes subsequent packets accordingly. Simple but requires per-connection state on the balancer, which is expensive and makes the balancer a stateful component that must itself be replicated carefully.
- **Hash-based selection.** Compute `id(packet) mod N` where `id` is some hash of connection-identifying fields (source/destination IP and port) and `N` is the backend count. Every packet in the same connection produces the same hash, so every packet lands on the same backend — without stored state.

The hash approach works until `N` changes. Adding or removing a backend shifts the modulus, and the hash of nearly every connection now maps to a *different* backend — forcing nearly every existing connection to reset. That is the motivation for [[consistent-hashing]] as the fallback: a mapping algorithm that stays mostly stable when the backend set changes, so only a small fraction of connections are disrupted. Google's production pattern (source: chapter-19-load-balancing-at-the-frontend.md) is simple connection tracking in the common case with consistent hashing as fallback under pressure (e.g., during DDoS when connection-tracking state explodes).

## Hiding implementation detail

The non-obvious but important property of a VIP: users see *one* IP. The service owner sees *many* backends behind it, which they can upgrade, reschedule, or expand freely. This hiding is what makes:

- **Rolling upgrades** transparent.
- **Capacity scaling** transparent.
- **Backend placement changes** (Borg rescheduling a task onto a different machine) transparent.

All of this happens without the client ever knowing.

## Relationship to existing wiki concepts

### VIP and the layered frontend

VIP-level balancing is the second layer of [[frontend-load-balancing]]. [[dns-load-balancing|DNS]] picks the datacenter by returning a VIP; the [[network-load-balancer]] picks the machine inside the datacenter. Chapter 20 then adds further layers *inside* the datacenter (service-level and RPC-level).

### VIP and service discovery

A VIP is an extreme version of [[service-discovery]]: clients discover exactly one address, and the "set of machines that actually serve this" is abstracted away entirely. Compare [[bns|BNS]] (returns a specific `IP:port` per task) and [[gslb|GSLB]] (layered DNS + service + RPC): VIPs collapse the whole discovery problem into "here is an IP, connect to it."

### VIP and the replicated-load-balanced-service pattern

Burns's [[replicated-load-balanced-service]] pattern assumes a load balancer sits in front of the replicas. A VIP is the network-layer *implementation* of that load balancer — what actually lives behind the Kubernetes `Service` LoadBalancer type, behind an AWS Network Load Balancer, or behind an internal VIP system like Google's.

### VIP vs GFE

The [[google-frontend|Google Frontend]] is an *application-layer* reverse proxy: it terminates TCP/TLS and speaks HTTP. A VIP is a *packet-level* component: it forwards raw IP packets. At Google the stack is layered — DNS returns a VIP, the VIP's network load balancer forwards packets to a GFE machine, the GFE speaks HTTP and forwards to service frontends over Stubby. See [[life-of-a-request]].

## Related pages

- [[network-load-balancer]]
- [[direct-server-return]]
- [[packet-encapsulation-load-balancer]]
- [[consistent-hashing]]
- [[frontend-load-balancing]]
- [[dns-load-balancing]]
- [[google-frontend]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
