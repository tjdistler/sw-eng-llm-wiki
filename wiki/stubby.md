# Stubby

**Summary**: Google's internal [[rpc|RPC]] framework. Every Google service communicates via Stubby. The open-source version is **gRPC**. Stubby uses [[protocol-buffers]] for on-the-wire data.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`, `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## What Stubby is

Stubby is the RPC infrastructure used by every Google service (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Two characterising notes from the chapter:

- **Even intra-process calls often go over Stubby.** "Often, an RPC call is made even when a call to a subroutine in the local program needs to be performed. This makes it easier to refactor the call into a different server if more modularity is needed, or when a server's codebase grows."
- **[[gslb|GSLB]] load-balances RPCs** the same way it load-balances externally visible services.

The first is essentially Google's house style for [[independent-deployability]]: prefer RPC boundaries even in-process so that the boundary can later be moved across machines without refactoring.

## Frontend vs backend terminology

The SRE book's RPC vocabulary inverts the traditional one (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

> A server receives RPC requests from its **frontend** and sends RPCs to its **backend**. In traditional terms, the frontend is called the client and the backend is called the server.

So inside Google, "frontend" = RPC client side and "backend" = RPC server side, regardless of who is browser-facing.

## What Stubby does beyond RPC

Chapter 20 shows that Stubby's responsibilities extend well past "send a request, get a response" (source: chapter-20-load-balancing-in-the-datacenter.md). The same framework implements:

- **The [[backend-task-states|three-state backend model]]** — healthy, refusing connections, and [[lame-duck-state|lame duck]] — as an RPC-framework primitive, not a per-application concern. Every Google service inherits graceful shutdown without writing shutdown code.
- **Piggybacked UDP health checks on idle connections**, so the lame-duck signal reaches inactive clients in 1-2 RTT. This is what lets the [[change-management-sre|rolling push]] be non-disruptive across a fleet where most client-backend pairs are idle at any moment.
- **An idle-connection optimisation** that drops the TCP connection in favour of UDP and lowers health-check frequency when a client-backend pair has no recent requests; the full connection is revived when traffic returns.
- **[[subsetting]] of backends per client** via [[deterministic-subsetting]], bounding per-client connection pools without coordinating clients.
- **[[load-balancing-policies|Client-side load balancing]]** — Simple, Least-Loaded, and [[weighted-round-robin|Weighted Round Robin]] — with backend utilisation and error rate reported on *every* response, including responses to health checks.

These are the mechanisms Chapter 20 develops; they live in Stubby and are therefore free for every Google service.

## Connection-level costs Stubby manages

Chapter 21 adds a further set of Stubby responsibilities that aren't directly about picking a backend but about *maintaining* the connection pool cheaply (source: chapter-21-handling-overload.md):

- **Idle-connection optimisation.** After a connection has been idle for a configurable time, Stubby drops the TCP connection and switches to cheaper UDP health checks. This matters because at Google's scale, a backend may have many clients that each send requests rarely; full TCP connections for all of them would cost more than the work itself. See [[connection-level-load]] for the pathology where health-checking dominates real work, and the recommended further tuning ("significantly decreasing the frequency of health checks" for very-low-rate clients).
- **Automatic criticality propagation.** Stubby carries [[request-criticality]] in the RPC envelope. If a backend processes request A (criticality `CRITICAL_PLUS`) and issues outgoing RPCs B and C as part of handling it, B and C inherit A's criticality by default. This is how the criticality set at the browser-facing edge reaches the bottom of a deep RPC stack without per-service classification.
- **Retry-count metadata.** Stubby carries a retry-counter in the request metadata (0 for first attempt, incrementing on each retry). Backends keep histograms of these counters and use them to detect widespread overload: when the histogram reveals a significant proportion of already-retried requests, the backend returns "overloaded; don't retry" instead of the standard "task overloaded." See [[retry-budget]].

Taken together, Chapters 20 and 21 make clear that Stubby is substantially more than a wire protocol — it is the distribution point for Google's entire request-admission, load-balancing, and overload-handling story.

## Stubby as a framework precedent (Chapter 32)

Chapter 32's [[frameworks-and-sre-platform|Frameworks and SRE Platform]] model generalises the Stubby pattern: rather than a single RPC framework carrying load balancing and overload handling, a broader set of [[service-framework|service frameworks]] carries instrumentation, logging, configuration, and the full control surface (source: chapter-32-the-evolving-sre-engagement-model.md). Stubby is the earliest and most successful example of the principle — production concerns encapsulated in infrastructure code so services inherit them by construction — and Chapter 32's argument is that the same pattern should apply to every other cross-cutting concern SRE cares about.

## gRPC

gRPC is the open-source release of Stubby. It uses Protocol Buffers for encoding, supports streaming RPC, and is the standard modern RPC framework. See the [[rpc]] page for the wiki's existing coverage of gRPC and how it compares to REST.

## Cross-book connections

- [[rpc]] — the general RPC discussion; gRPC gets mentioned there but Stubby is its internal ancestor.
- [[protocol-buffers]] — the wire format Stubby uses.
- [[service-discovery]] / [[gslb]] — how clients find Stubby backends.
- [[independent-deployability]] — the cultural reason even intra-process calls go over Stubby.

## Related pages

- [[rpc]]
- [[protocol-buffers]]
- [[gslb]]
- [[independent-deployability]]
- [[datacenter-load-balancing]]
- [[backend-task-states]]
- [[lame-duck-state]]
- [[subsetting]]
- [[load-balancing-policies]]
- [[weighted-round-robin]]
- [[handling-overload]]
- [[connection-level-load]]
- [[request-criticality]]
- [[retry-budget]]
- [[site-reliability-engineering]]
