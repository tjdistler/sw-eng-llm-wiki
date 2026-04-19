# Elasticity

**Summary**: The ability of a scalable system to scale dynamically — automatically up and down — based on current workload. Distinct from raw [[scalability]]: scalability is whether the system **can** grow; elasticity is whether it grows **by itself**, and especially, whether it can absorb *instantaneous* bursts. Chapter 3 of *Fundamentals of Data Engineering* lists elasticity among the four characteristics of distributed data systems. Chapter 3 of *Software Architecture: The Hard Parts* identifies elasticity as a function of service **granularity** via mean time to startup (MTTS).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`

**Last updated**: 2026-04-19

---

## The four characteristics

Chapter 3 names four closely related characteristics of data systems (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **[[scalability]]** — can the capacity grow?
- **Elasticity** — does it grow dynamically and automatically?
- **[[availability-measurement|Availability]]** — percentage of time in an operable state
- **[[reliability]]** — probability of meeting defined standards during a specified interval

Dynamic scaling improves reliability: elasticity ensures adequate performance without manual intervention, and performance failures under load lead to unavailability.

## Scale to zero

A property of some elastic systems: when idle, they can shut down entirely (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Serverless functions and serverless OLAP databases are the canonical examples. Scale-to-zero is where elasticity meets [[finops]] — cost goes to zero while capacity is not needed, then scales with demand.

## Warning: inappropriate scaling costs money

Chapter 3 warns that deploying elaborate scaling machinery where it isn't warranted produces **overcomplicated systems and high costs** (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). A single relational database with a failover node is often the right answer for an application. Measure current load, approximate load spikes, and estimate near-term growth — then decide.

## The Hard Parts framing: MTTS and granularity

Chapter 3 of *Software Architecture: The Hard Parts* defines elasticity more narrowly than *Fundamentals of Data Engineering* does — not just "grows automatically" but specifically "absorbs instantaneous spikes in user load" (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md). The concert-ticket-on-sale example: a system goes from 20 concurrent users to 3,000 in seconds when tickets go on sale for a popular event. Elasticity requires not just *the ability* to add capacity but *the speed* to add it before the spike overwhelms the existing capacity.

The mechanical metric is **mean time to startup (MTTS)** — how long it takes a new service instance to come up and start serving traffic. MTTS is primarily a function of:

- **Deployment-unit size** — smaller services start faster.
- **Runtime weight** — lightweight runtimes (Go, Node, native images) start faster than heavy ones (classic JVM, .NET Framework).
- **Boot-time dependencies** — services that must warm caches, hydrate in-memory state, or establish many downstream connections take longer to become useful.

Fine-grained [[microservices]] can have MTTS measured in seconds or sub-second; service-based domain services and monoliths typically take tens of seconds to minutes.

Ford and Richards separate the two characteristics along a modularity / granularity axis (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> Although both scalability and elasticity improve with finer-grained services, elasticity is more a function of **granularity** (the size of a deployment unit), whereas scalability is more a function of **modularity** (the breaking apart of applications into separate deployment units).

This is why a [[service-based-architecture|service-based architecture]] (coarse domain services) scales reasonably but is only moderately elastic: the domain services can scale horizontally but MTTS is too long for burst response. [[microservices]] is the only architecture in the Chapter 3 star-rating table that maxes both scalability and elasticity.

### The chatter caveat

Synchronous inter-service calls negate elasticity the same way they negate the other modularity drivers. A newly-started instance that must synchronously call five peers to serve its first request spends more time waiting than processing; spin-up advantages cancel. Chapter 3's prescription — keep synchronous communication minimal when high elasticity is required — applies here.

## Cross-book framing

- Kleppmann's treatment of [[scalability]] and [[load-parameters]] is the theoretical foundation
- Burns's [[dynamic-worker-scaling]] is elasticity implemented at the batch-worker layer
- [[cold-start-warm-start]] (Burns, FaaS) names the latency tax elasticity imposes at scale-to-zero boundaries
- [[capacity-planning]] and [[intent-based-capacity-planning]] (SRE) are the Google operational counterparts

## Related pages

- [[scalability]]
- [[reliability]]
- [[availability-measurement]]
- [[principles-of-good-data-architecture]]
- [[finops]]
- [[dynamic-worker-scaling]]
- [[cold-start-warm-start]]
- [[data-architecture]]
- [[architectural-modularity]]
- [[microservices]]
- [[service-based-architecture]]
