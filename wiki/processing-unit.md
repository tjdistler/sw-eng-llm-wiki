# Processing Unit

**Summary**: The compute-and-cache unit of [[space-based-architecture]]: application code plus an in-memory replicated data grid deployed together, dynamically started and stopped by the deployment manager to handle elastic load without any synchronous database access during request processing.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-15-space-based-architecture-style.md`

**Last updated**: 2026-04-16

---

## What it contains

A processing unit bundles two things (source: chapter-15):

1. **Application logic** — usually both web-layer and backend business logic. For small apps the whole application lives in one processing unit; for larger apps the application is split by functional area across multiple processing-unit *classes*. Processing units can also be small single-purpose services in the [[microservices]] sense.
2. **An in-memory data grid + replication engine** — typically implemented with Hazelcast, Apache Ignite, or Oracle Coherence. The cache is the authoritative data the application code reads and writes during request handling. The database is *not* in the synchronous path.

The processing unit is the only place in [[space-based-architecture]] where application code runs. Every other component (messaging manager, data grid manager, processing grid, deployment manager, [[data-pump|data pumps]], data writers, data readers) is infrastructure.

## Named caches and member lists

Processing units of the **same class** share a named cache (e.g. `CustomerProfile`). A trivial Hazelcast example from the chapter:

```java
HazelcastInstance hz = Hazelcast.newHazelcastInstance();
Map<String, CustomerProfile> profileCache = hz.getReplicatedMap("CustomerProfile");
```

Every processing unit instance with this code joins the same replication group. The caching product maintains a **member list** of all processing units currently participating in the named cache, with IP and port. When a processing unit starts up, it joins the group and hydrates its cache from an existing member; when it shuts down, it leaves the group and the remaining members update their lists (source: chapter-15, which prints the Hazelcast `Members {size:1…3, ver:1…4}` log lines showing members coming and going).

This is the mechanism by which the cache membership tracks the deployment manager's dynamic scaling — no external service discovery is needed for cache membership.

## Inter-processing-unit data access

Two options when one processing unit needs data owned by another class:

- **Remote call** to the other processing unit (choreography — direct peer-to-peer)
- **Processing grid** orchestration (the middleware mediates; optional component of [[space-based-architecture]])

Synchronous calls between processing units pull them into the same [[architectural-quantum]] for the duration of the call; asynchronous event-driven coupling keeps them in separate quanta.

## Startup and hydration

A processing unit has three cache-load paths:

1. **Hot start** — at least one other processing unit in the same named cache is already running. The starting instance joins the member list and replicates the cache from an existing peer. No database read.
2. **Cold start** — this is the first instance of the class to come up (system-wide crash, redeployment of all instances, or archival data not in any live cache). The instance acquires a lock on the named cache (one instance wins), sends a request message to the data-reader queue, and loads the cache from the **reverse data pump** as the data reader streams records back. Other instances wait on the lock until the cache is populated and then sync from the new primary.
3. **Archive read** — a specialised cold-read path for data not kept in the live replicated cache.

Hot starts are the common case in a well-behaved SBA system; cold starts are the fallback after catastrophic failure and are designed for correctness rather than speed.

## Memory sizing

Because processing units are usually one-per-VM, the **cache size directly constrains how many processing units can start**. The chapter's guidance: caches over roughly 100 MB start to create elasticity problems under replicated caching. Beyond that threshold either switch to distributed caching or split the cache into smaller named caches owned by different processing-unit classes.

## Stateless-ish

The application *code* in a processing unit is stateless with respect to individual requests (any instance can handle any request), but the processing unit as a whole is **stateful with respect to the named cache** — that's the point. Elasticity is preserved because the cache replicates, not because each instance is independent.

## Related pages

- [[space-based-architecture]]
- [[data-pump]]
- [[replication]]
- [[eventual-consistency]]
- [[scaling-approaches]]
- [[architectural-quantum]]
- [[microservices]]
