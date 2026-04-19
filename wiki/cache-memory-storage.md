# Cache and Memory-Based Storage

**Summary**: Storage systems that keep data in **RAM** rather than disk to deliver sub-millisecond reads. **Memcached** and **Redis** are the canonical examples. They are primarily used as **caches** in front of slower durable storage, but Redis (with optional persistence) can also serve as the primary store for applications that tolerate small windows of data loss.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Why in-memory

RAM offers ~100 ns latency and ~100 GB/s bandwidth — roughly 1,000× faster than SSD — at ~$10/GB, roughly 50× the cost (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). For data that is read repeatedly at high rates, the performance improvement dwarfs the cost of keeping it in memory.

Chapter 6's framing: RAM is "extremely vulnerable to data loss because a power outage lasting even a second can erase data. RAM-based storage systems are generally focused on caching applications, presenting data for quick access and high bandwidth. Data should generally be written to a more durable medium for retention purposes" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

## Memcached

A classic key-value cache designed for simplicity (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Simple value types** — strings or integers.
- **Pure cache** — no persistence. On restart, all data is lost; the application repopulates from the backing database.
- **Low latency, high throughput.** Well-matched to caching database query results and API responses.
- **Load reduction.** Chapter 6 specifically flags offloading work from backend systems as a primary use.

Memcached deliberately does not try to be more than a cache. It is run as a fleet of independent servers; the client library hashes keys to servers.

## Redis

More ambitious. Redis is also a key-value store, but with important additions (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Richer data types.** Lists, sets, sorted sets, hashes, streams, HyperLogLogs, geospatial structures.
- **Optional persistence.** Two mechanisms:
  - **Snapshotting** — periodic point-in-time dumps to disk.
  - **Append-only file (AOF)** — journal of operations, replayed on restart.
  - Typical config writes every ~2 seconds — fast enough not to dominate write latency, but exposing a ~2-second window of potential data loss on crash.
- **Pub/sub, streams, and scripting.** Redis has grown features that approach primary-storage duties.

Redis thus sits between "pure cache" and "primary store": it is most common as a cache, but it is used in production as the primary store for workloads that can tolerate a second of loss on crash — e.g., session stores, rate-limiters, leaderboards.

## Where these systems fit

In a typical stack, cache-memory storage sits as the **fastest non-CPU tier** in the storage hierarchy (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

```
CPU cache → RAM (incl. Memcached, Redis) → SSD → HDD → object storage → archival
```

The practical patterns:

- **Cache-aside.** Application reads from Redis/Memcached first; on miss, reads from durable store and populates the cache.
- **Write-through.** Application writes to cache and durable store in one operation.
- **Query-result cache** on top of an OLAP engine: cache the result of expensive aggregation queries keyed by the query string. Chapter 6 flags this as an example of [[data-temperature|hot data]] — frequently-recomputed query results stored in RAM.

## Relationship to other storage

- **[[key-value-store]]** — Memcached and Redis are both key-value stores. The FoDE Ch 5 page on key-value stores is broader (covering DynamoDB, FoundationDB, etc.); this page is specifically the in-memory flavour.
- **[[data-temperature]]** — cache-memory storage *is* the hot tier.
- **[[state-store]]** — stream-processing local state stores (RocksDB, in-memory hash tables) occupy a similar role for streaming applications.
- **[[caching-layer]]** — the broader architectural concept; includes CDN caches, application-level caches, and database result caches.

## Related pages

- [[storage-raw-ingredients]]
- [[data-temperature]]
- [[key-value-store]]
- [[caching-layer]]
- [[state-store]]
- [[data-storage-stage]]
