# Data Pump

**Summary**: The asynchronous one-way messaging conduit by which a [[processing-unit]] in [[space-based-architecture]] sends updates to the persistent database; the mechanism that keeps the request-path database-free while still delivering durability, eventually.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-15-space-based-architecture-style.md`

**Last updated**: 2026-04-16

---

## Why it exists

[[processing-unit|Processing units]] in [[space-based-architecture]] never read from or write to the database synchronously — doing so would reintroduce the database bottleneck the style is built to avoid. But the cache is not the system of record; the database is. Something has to move updates from the in-memory replicated cache to the database without blocking the request path. That something is the data pump (source: chapter-15).

A data pump is **always asynchronous** and **always one-way**. The processing unit that performed the cache update owns the update and is responsible for publishing a message through its data pump. The database update is then handled off the request path by a data writer.

## Implementation

Data pumps are almost always built on **messaging** with persistent queues (source: chapter-15). Messaging is a good fit for four reasons:

1. **Asynchronous** — the processing unit does not wait for the database write.
2. **Guaranteed delivery** — persistent queues survive crashes on either side.
3. **Preserved order** — FIFO queues preserve the order of updates for a given key.
4. **Decoupling** — if the data writer is down, the processing unit keeps working; messages accumulate in the queue.

## Contracts

Data pump messages usually carry an **action plus a payload**: add, update, or delete, with the changed data and the primary key. For updates the payload is only the **delta** — for example, a customer profile phone-number change sends the new phone number plus the customer ID and an `update` action, not the entire profile. The contract itself can be JSON schema, XML schema, a serialised object, or a value-driven map message.

## Granularity

Most SBA systems have **multiple data pumps**, usually one per domain or subdomain. Two common splits:

- **Per-cache data pump** — a separate pump for each named cache (`CustomerProfile`, `CustomerWishlist`, `CustomerWallet`, `CustomerPreferences`). Fine-grained contracts; many pumps.
- **Per-domain data pump** — a single pump for a whole domain (`Customer`) covering all of its caches. Coarser contracts; fewer pumps.

Neither is universally right — the trade-off is between **alignment** (per-cache = one pump per data writer = easy to evolve) and **sprawl** (per-cache = many queues and contracts to manage).

## Reverse data pumps

The same mechanism runs in the opposite direction during **cold start**: when a processing-unit class has no live cache (system-wide crash or redeployment), the elected cache owner sends a read request to a queue; the data reader queries the database, streams records onto a **reverse data pump**, and the cache owner loads them into the cache. Only once the cache is populated do other processing units leave their startup wait state and sync (source: chapter-15).

## Eventual consistency by construction

Because the pump is asynchronous, the **cache and the database are always [[eventual-consistency|eventually consistent]]**, not strongly consistent. This is fundamental to the architecture — it is the trade that buys SBA's five-star scalability and elasticity — but it requires the architect to explicitly handle:

- **Read queries that must reflect cache state** — read from the cache, not the DB
- **Read queries that must reflect archival state** — read from the DB via a data reader (rare path)
- **Reports and analytics** — usually run against the database, and therefore see slightly stale data

## Data writers at the other end

Data writers consume data-pump messages and perform the actual DB update. They can be implemented as services, applications, or enterprise data hubs (Ab Initio). Granularity is either **domain-based** (one writer listens to all four customer-related data pumps and owns all customer DB updates) or **per-pump** (one writer per data pump, tightly aligned with one processing-unit class). Per-pump writers produce more components but better deployment and scaling alignment.

The data-writer-plus-data-reader pair is conventionally called a **data abstraction layer**: processing units know cache schemas, not DB schemas, and the writers/readers contain transformation logic. This lets DB and cache schemas evolve on independent cadences — the writer can buffer incompatible changes until the cache side catches up.

## Related pages

- [[space-based-architecture]]
- [[processing-unit]]
- [[eventual-consistency]]
- [[message-brokers]]
- [[replication]]
- [[event-driven-architecture]]
