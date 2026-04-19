# Replicated Caching Pattern

**Summary**: A [[distributed-data-access]] pattern where each service holds a **read-only in-memory replica** of data it doesn't own, kept in sync peer-to-peer by a replicated-cache product (Hazelcast, Apache Ignite, Oracle Coherence). Nanosecond reads, strong fault tolerance, and independent scalability — at the cost of startup coupling, memory per-instance, a ceiling on data volume, and poor fit for volatile data.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md`

**Last updated**: 2026-04-19

---

## The three caching models

Chapter 10 contrasts three models to make the replicated version's niche clear (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md):

| Model | Data location | Shared across services? |
|---|---|---|
| Single in-memory cache | In-process, per-service | No — each service has its own private data |
| **Distributed cache** | External cache server (Redis, Memcached) | Yes, via remote call |
| **Replicated cache** | In-process, in **every** service | Yes, kept in sync peer-to-peer |

The [[cache-memory-storage]] page treats the first two; this page is specifically the replicated model, because only the replicated model solves distributed data access without reintroducing a network hop or a shared dependency.

### Why distributed cache is not the answer for Ch 10

A shared external cache looks tempting but fails three of Ch 10's criteria:

- **Fault tolerance** — the reader now depends on the cache server instead of the owner service. Dependency shifted, not removed.
- **Ownership** — any service with cache credentials can write any key. The bounded context around data ownership breaks.
- **Latency** — every read is still a network call; nanoseconds become milliseconds.

## The mechanics

The owning service (Catalog) populates an in-memory cache of product descriptions. Every consuming service (Wishlist) gets a **read-only replica** of that cache in its own process. When Catalog updates the cache, the caching product propagates the change asynchronously to every replica peer (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

Product examples from the book:

- **Hazelcast**
- **Apache Ignite**
- **Oracle Coherence**

Not every caching product supports replicated mode — Ch 10 reminds architects to verify before committing.

## The advantages

- **Responsiveness** — nanosecond reads; no network hop.
- **Fault tolerance** — if the Catalog Service goes down, the Wishlist Service keeps serving from its own replica. When Catalog comes back, the caches reconnect with no Wishlist disruption.
- **Independent scalability** — Wishlist instances can scale without scaling Catalog.
- **Ownership preserved** — only the owner writes; replicas are read-only, so the bounded context holds.

## The trade-offs

Chapter 10 is careful to catalogue the costs (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md):

### Startup dependency

The **initial** Wishlist instance needs the Catalog Service up at boot to populate its cache from the owner. Once loaded, Catalog can go up and down freely. Additional Wishlist instances can bootstrap from peer Wishlist caches — so the coupling is literal first-instance-only, not ongoing.

### Data volume ceiling

Because every instance carries a full in-process replica, total memory scales as `cache_size × instance_count`. The book's example: 500 MB × 5 instances = 2.5 GB. Much beyond that, the pattern becomes economically impractical — the chapter treats ~500 MB per cache as a rough ceiling.

### Volatile data doesn't replicate well

Replication latency is finite. If the update rate is high (think: inventory counts, prices ticking), replicas constantly chase the owner and drift. For **relatively static** data (product descriptions, category codes) the pattern works well; for volatile data it doesn't.

### TCP/IP discovery and setup

Replicated caches discover each other via TCP/IP broadcast and lookup. Cloud and containerized environments — dynamic IPs, restricted broadcast — make discovery fragile. Too-broad broadcast ranges slow the socket handshake; too-narrow ones miss peers entirely.

## Trade-offs summary (Table 10-3)

| Dimension | Rating |
|---|---|
| Service dependency | **Medium** — startup-only |
| Response time | **Excellent** — in-memory |
| Data currency | Fair — async replication lag |
| Fault tolerance | **Excellent** — survives owner outage |
| Data volume | **Poor** above ~500 MB × instance count |
| Scalability | Independent |
| Complexity | **High** — cluster + discovery + ops |
| Contract versioning | Cache DTO is the contract |

(source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md, Table 10-3)

## When to use it

Good fit:

- Small, slow-changing reference data shared across many services.
- Hard fault-tolerance or latency requirements.
- Few enough instances that memory footprint is manageable.

Poor fit:

- Large datasets.
- Volatile data (inventory counts, pricing, balances).
- Environments where multicast/TCP-discovery is flaky.

For those cases, reach for [[column-schema-replication-pattern]] (large volume), [[interservice-communication-pattern]] (always-fresh), or [[data-domain-pattern]] (everything at once).

## Related pages

- [[distributed-data-access]]
- [[interservice-communication-pattern]]
- [[column-schema-replication-pattern]]
- [[data-domain-pattern]]
- [[cache-memory-storage]]
- [[data-ownership]]
- [[fault-tolerance]]
- [[scalability]]
- [[eventual-consistency]]
- [[software-architecture-the-hard-parts]]
