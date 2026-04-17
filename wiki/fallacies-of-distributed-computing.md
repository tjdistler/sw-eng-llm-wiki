# Fallacies of Distributed Computing

**Summary**: The eight assumptions that distributed-system builders reflexively make but that are all false. Coined by L. Peter Deutsch and colleagues at Sun Microsystems in 1994, and used by Richards and Ford to frame the shared cost structure that every distributed architecture style in Part II of *Fundamentals of Software Architecture* has to pay. Each fallacy is independently covered in depth by [[designing-data-intensive-applications]] Chapter 8; this page is the Richards-and-Ford architect-facing summary plus cross-links.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-09-foundations.md`

**Last updated**: 2026-04-16

---

## Origin

The *fallacies of distributed computing* were first coined by L. Peter Deutsch and other colleagues at Sun Microsystems in 1994. Richards and Ford define a fallacy as *something that is believed or assumed to be true but is not* (source: chapter-09-foundations.md). All eight still apply to every distributed architecture style in the book.

A [[monolith|monolithic architecture]] dodges all eight by construction — everything is in one process and the network isn't part of the business-request path. That's most of what makes the [[monolithic-vs-distributed]] trade-off asymmetric: the monolithic styles share an operational complexity floor that distributed styles never touch.

## The eight fallacies

### 1. The network is reliable

Developers and architects assume networks are reliable; they are not. A call to a healthy downstream service can still fail because the request, response, or both were lost in transit (source: chapter-09-foundations.md). This is why [[timeouts]] and [[circuit-breaker|circuit breakers]] exist between services.

Richards and Ford's formulation: *the more a system relies on the network (such as microservices), the potentially less reliable it becomes* (source: chapter-09-foundations.md).

Kleppmann covers the mechanics in depth: see [[unreliable-networks]] (shared-nothing asynchronous packet networks; six indistinguishable request-outcome cases), [[network-faults]] (empirical prevalence — 12 faults/month in one medium datacenter; human error as the dominant cause), and [[partial-failures]] (the nondeterminism that the network introduces at the system level).

### 2. Latency is zero

A local method call is measured in nanoseconds or microseconds; a remote call over REST, messaging, or RPC is measured in milliseconds. `t_remote > t_local` always (source: chapter-09-foundations.md).

Richards and Ford's operational prescription: **know your production average latency and your p95–p99**. The average might be 60ms while the p95 is 400ms — it's the *long tail* that kills distributed-architecture performance (source: chapter-09-foundations.md). Chaining 10 service calls at 100ms average adds a full second to every request.

The percentiles argument matches [[response-time-percentiles]] (Kleppmann): averages are misleading; p95/p99 are what users feel and what an SLO has to target. See also [[tail-latency-amplification]] — Burns's point that a backend's p99 becomes a scatter-gather system's p50 at modest fan-out.

### 3. Bandwidth is infinite

Bandwidth is usually irrelevant inside a monolith — once the request enters the process, no bandwidth is consumed. Distributed architectures re-introduce it: interservice chatter can saturate links, which feeds back into fallacies #1 and #2 (source: chapter-09-foundations.md).

Richards and Ford's worked example: a wish-list service calls a customer-profile service for 45 attributes totalling 500 kB when it only needs the 200-byte name. At 2,000 requests/second, that single interservice call consumes **1 Gb/s** of bandwidth. This is called **stamp coupling** — the service returns a fixed large payload when the caller only needs a fragment (source: chapter-09-foundations.md).

Ways to fix stamp coupling (source: chapter-09-foundations.md):

- Private, caller-specific RESTful API endpoints
- Field selectors in the contract
- GraphQL
- Value-driven [[consumer-driven-contracts]]
- Internal messaging endpoints with narrow event shapes

The general rule is the same rule Kleppmann gives from the other direction: **ensure the minimal amount of data is passed between services**.

### 4. The network is not secure

VPNs, trusted networks, and firewalls make architects complacent. In a distributed architecture, every endpoint — including internal interservice endpoints — must be secured. The attack surface grows by orders of magnitude compared with a monolith (source: chapter-09-foundations.md).

This is one of the reasons synchronous, highly-distributed styles ([[microservices]], service-based) tend to perform worse than equivalent monoliths: **every hop pays authentication and authorization cost**.

### 5. The topology never changes

The "topology" here means routers, switches, firewalls, load balancers, and the wiring between them. It changes constantly. Richards and Ford's worked scenario: a "minor" network upgrade at 2 a.m. Monday invalidates every latency assumption in production, tripping timeouts and circuit breakers across the system (source: chapter-09-foundations.md).

The practical implication is relational, not technical: architects must be in continuous communication with network and ops teams so topology changes aren't surprises. This hands off directly to fallacy #6.

### 6. There is only one administrator

A small team works with one sysadmin. A large enterprise has dozens of network administrators across dozens of specialties. Knowing *who to ask* about latency changes (fallacy #2) or topology changes (fallacy #5) is itself a distributed-architecture skill (source: chapter-09-foundations.md).

Monolithic architectures don't pay this coordination tax. The single-deployable-unit property means one ops owner and one change window; distribution pushes that into an organizational problem.

### 7. Transport cost is not zero

Often confused with latency, but different: **transport cost here means money**. The infrastructure required to make a "simple RESTful call" — additional hardware, servers, gateways, firewalls, subnets, proxies — is not usually already in place (source: chapter-09-foundations.md).

Richards and Ford's prescription before embarking on a distributed architecture: analyse current server and network topology for capacity, bandwidth, latency, and security-zone suitability. Distribution is significantly more expensive than monolithic deployment.

### 8. The network is not homogeneous

Most real networks are mixed-vendor. Juniper and Cisco mostly interoperate, but not in all load, traffic, and failure combinations — packets occasionally get lost in ways that no vendor's testing predicted (source: chapter-09-foundations.md).

The significance is that this fallacy *compounds* the other fallacies. Heterogeneous hardware amplifies unreliability (#1), latency variability (#2), and bandwidth uncertainty (#3) into an "endless loop of confusion and frustration when dealing with networks" (source: chapter-09-foundations.md).

## Why the fallacies matter for architecture choice

The fallacies are the floor of operational cost for *any* distributed architecture style. When choosing between a monolithic style (layered, pipeline, microkernel) and a distributed style (service-based, event-driven, space-based, SOA, [[microservices]]), the fallacies are what's actually on the distributed side of the scale. The performance, scalability, and availability upside of distribution is real — but the eight fallacies are what you buy with it.

See [[monolithic-vs-distributed]] for the trade-off as Richards and Ford frame it, and [[partial-failures]] for the deeper systems-theory reason all eight fallacies are inescapable rather than engineerable-away.

## Related pages

- [[monolithic-vs-distributed]]
- [[monolith]]
- [[microservices]]
- [[unreliable-networks]]
- [[network-faults]]
- [[timeouts]]
- [[circuit-breaker]]
- [[partial-failures]]
- [[response-time-percentiles]]
- [[tail-latency-amplification]]
- [[consumer-driven-contracts]]
- [[schema-evolution]]
- [[fundamentals-of-software-architecture]]
