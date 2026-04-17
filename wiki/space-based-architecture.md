# Space-Based Architecture

**Summary**: A distributed architecture style that removes the central database from the synchronous request path and replaces it with an in-memory replicated data grid spread across dynamically-scaled processing units, achieving near-infinite scalability and elasticity for workloads like ticketing, auctions, and booking systems.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-15-space-based-architecture-style.md`

**Last updated**: 2026-04-16

---

## The problem it solves

Traditional web applications follow a triangular topology: many web servers → fewer application servers → a single database. Under extreme concurrent load the bottleneck walks down the triangle until it hits the database, which is the hardest and most expensive layer to [[scaling-approaches|scale]]. Caching and read replicas push the ceiling upward but do not remove it. Space-based architecture solves the problem architecturally — it **removes the database as a synchronous constraint** rather than trying to scale it (source: chapter-15).

The motivating workloads are systems with **unpredictable spikes in concurrent user volume**: online concert ticketing (idle until tickets drop, then tens of thousands of concurrent users for minutes), online auctions (bid volume invisible until the auction starts), airline booking, and similar high-concurrency burst domains. These are exactly the workloads where a database-centric architecture — even a well-tuned one — collapses.

## Where the name comes from

The style is named after the **tuple space** concept from the Linda coordination language (1980s): multiple parallel processors communicating through a shared, associative memory rather than through point-to-point messages. In SBA the "space" is the **replicated in-memory data grid** that lives inside every processing unit and stays synchronized across them (source: chapter-15).

## Topology

Five named components (source: chapter-15):

| Component | Role |
|---|---|
| [[processing-unit]] | Contains application logic + an in-memory replicated data grid. Dynamically scaled. |
| Virtualized middleware | Four managers that coordinate processing units (messaging, data, processing, deployment). |
| [[data-pump]] | Asynchronous one-way conduit from processing units to the persistent database. |
| Data writers | Consume data pumps and persist to the database. |
| Data readers | Retrieve data from the database into a cold cache at processing-unit startup. |

The critical structural fact: **processing units never read from or write to the database synchronously**. All durability flows through data pumps and is [[eventual-consistency|eventually consistent]] with the in-memory grid.

## Virtualized middleware

The "middleware" is not a single product — it is the collection of four managers that coordinate the processing units (source: chapter-15):

### Messaging manager (messaging grid)

Routes incoming requests to an available processing unit. Complexity ranges from round-robin to next-available tracking. Usually implemented with a standard load-balancing web server (HA Proxy, Nginx).

### Data grid manager

Handles cache replication between processing units. In most modern implementations the data grid is implemented **entirely inside the processing units** as a peer-to-peer replicated cache (Hazelcast, Apache Ignite, Oracle Coherence); the middleware "data grid" component only exists when an external controller is needed or when using a distributed cache. Replication is asynchronous but usually completes in under 100 milliseconds.

Each processing unit maintains a **member list** of the IP addresses and ports of all other processing units sharing the same named cache. Members are added automatically when a processing unit starts and the cache is synced from an existing member; members are removed automatically when a processing unit goes down. This is the mechanism by which cache membership tracks dynamic scaling.

### Processing grid (optional)

Orchestrates requests that require coordination between multiple processing-unit types (e.g., an Order processing unit plus a Payment processing unit). When present it mediates and composes the cross-processing-unit call. An SBA system with a single processing unit class does not need one.

### Deployment manager

Monitors response times and load and **dynamically starts and stops processing units** in response. This is what makes SBA elastic: there is no separate autoscaler — elasticity is built into the middleware.

## Replicated vs distributed caching

SBA mostly uses **replicated caching** (each processing unit owns a full copy of the named cache, kept in sync by the data grid product) because it is extremely fast and has no single point of failure. Replicated caching breaks down when (source: chapter-15):

- **Cache size exceeds ~100 MB** — per-VM memory limits cap the number of processing units you can start
- **Update rate is high enough that the replication engine can't keep up** — see data collisions below

In those cases switch to **distributed caching**: a central cache server that processing units read from and write to remotely. Distributed caching gives stronger consistency (single source of truth) but costs performance (remote access) and fault tolerance (the cache server is a SPOF).

The two models are not mutually exclusive within one application. The chapter's recommendation is to **pick per data domain**: distributed caching for data that needs strong consistency (live inventory), replicated caching for lookup/reference data (product catalogue, customer profile).

### Near-cache — avoided

A **near-cache** is a hybrid where each processing unit holds a small "front cache" (MRU / MFU / random-replacement) in front of a shared distributed "full backing cache". Front caches sync with the backing cache but **not with each other**, so processing units see inconsistent data and inconsistent performance. The chapter explicitly recommends against near-caches in SBA.

## Data collisions

The distinctive risk of replicated caching in active-active SBA: two processing units update the same cache key within the replication window, and the replication arrives after the local update — both processing units end up with the other's old value. The chapter gives a worked example: starting at 500 units of inventory, A decrements to 490 (10 sold) and B decrements to 495 (5 sold) concurrently; after cross-replication, both end at values that ignore one of the two sales (source: chapter-15).

The probability of collision is modelled as:

```
CollisionRate = N × UR² / (S × RL)
```

- **N** = number of processing units with the same named cache
- **UR** = update rate (updates per ms, squared)
- **S** = cache size (rows)
- **RL** = replication latency of the caching product (ms)

Collision rate is **proportional to N and UR², inversely proportional to S and RL**. Collisions drop sharply as replication latency decreases: the chapter's worked example at 72,000 updates/hour shows 14 expected collisions at 100 ms replication latency but only 0.1 collisions per hour at 1 ms — a 140× improvement from a 100× faster replication path. Replication latency is rarely published by caching products and usually has to be measured in production.

The chapter's practical guidance is to calculate **minimum, normal, and peak** collision rates using peak update rates for the peak estimate, since systems rarely sustain one rate over a long period.

## Cloud vs on-prem

SBA has a **distinctive hybrid deployment option**: put the processing units and virtualized middleware in the cloud where elasticity is cheap, and keep the physical database on-prem. The asynchronous [[data-pump|data pumps]] plus the eventual-consistency model naturally tolerate the cross-environment latency. This lets transactional processing ride cloud elasticity while data management, reporting, and analytics stay under local control (source: chapter-15). Most other styles cannot split cleanly this way.

## Characteristics star-rating

| Characteristic | Rating | Explanation |
|---|---|---|
| Elasticity | ★★★★★ | The deployment manager starts and stops processing units in response to load; this is what SBA is *for*. |
| Scalability | ★★★★★ | No DB bottleneck in the request path; millions of concurrent users possible. |
| Performance | ★★★★★ | In-memory access for every operation; no network-to-DB per request. |
| Simplicity | ★ | Many moving parts; caching + eventual consistency + asynchronous persistence together produce high operational complexity. |
| Testability | ★ | Testing millions of concurrent users is expensive and usually done only in production with actual load — which is itself risky. |
| Cost | ★ | Licensing for commercial caching products is high, and the resource footprint under elastic scaling is large. |
| Evolvability | tricky | Cache schemas and DB schemas need to evolve in lockstep, but data writers/readers contain transformation logic that can buffer the mismatch incrementally (data abstraction layer pattern). |

No five-star column is free. The chapter is explicit that SBA is hard to get right and that the cost-and-simplicity tax is the permanent price of the three five-star operational ratings.

## Partitioning and quantum

SBA resists clean classification along the [[technical-vs-domain-partitioning|technical-vs-domain axis]]: it is both. Processing units can act as domain services (like [[service-based-architecture|service-based]] or [[microservices]]), and the layering of processing units / data pumps / data writers / database is a technical partitioning very similar to an n-tier [[layered-architecture|layered architecture]].

[[architectural-quantum|Quantum count]] is *not* driven by the database (processing units don't synchronously depend on it). Quanta are delineated by the association between user interfaces and processing units and by synchronous coupling between processing units (including through the processing grid).

## Implementation products

- **Apache Ignite** — open source in-memory data grid
- **Hazelcast** — open source in-memory data grid (the chapter's code examples use it)
- **Oracle Coherence** — commercial in-memory data grid
- **Gigaspaces** — commercial SBA platform (historically the canonical SBA product)

## Use cases

- **Concert ticketing** — low-volume until tickets drop, then spike to tens of thousands of concurrent users for minutes. The deployment manager can be configured to pre-warm processing units just before the drop.
- **Online auctions** — unpredictable bidder count; per-auction processing units can be dedicated for consistency and destroyed when auctions end.
- **Airline and hotel booking** — similar burst + consistency profile.
- In general: **> 10,000 concurrent users with unpredictable spikes**.

## When to use

- Extreme, variable, unpredictable concurrent load
- The database is the known bottleneck and caching alone won't fix it
- Budget, operational maturity, and tolerance for eventual consistency are all high

## When not to use

- Predictable, moderate load — cheaper styles ([[service-based-architecture]], [[layered-architecture]]) will do fine
- Strong single-system consistency required — the in-memory-then-async-DB model is eventually consistent by construction
- Small team or tight budget — the licensing, resource, and operational costs are high
- Most business applications — the chapter is explicit that SBA is the Ferrari of architecture styles, not the daily driver

## Relationship to other styles

SBA is often **embedded inside other styles** as a hybrid, the way [[event-driven-architecture]] is. **Event-driven space-based** is the common hybrid where processing units communicate via asynchronous events rather than synchronous calls through the processing grid — this removes the processing-grid bottleneck while preserving SBA's caching and elasticity model.

## Related pages

- [[processing-unit]]
- [[data-pump]]
- [[scaling-approaches]]
- [[scalability]]
- [[eventual-consistency]]
- [[replication]]
- [[cap-theorem]]
- [[architectural-quantum]]
- [[monolithic-vs-distributed]]
- [[technical-vs-domain-partitioning]]
- [[layered-architecture]]
- [[service-based-architecture]]
- [[event-driven-architecture]]
- [[microservices]]
