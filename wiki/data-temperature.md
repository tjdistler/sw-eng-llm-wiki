# Data Temperature

**Summary**: A framing from the [[data-storage-stage|storage stage]] of the [[data-engineering-lifecycle|data engineering lifecycle]]: data is classified as **hot, warm, or cold** based on access frequency, and each temperature maps to a different cost/performance storage tier. Chapter 6 of *Fundamentals of Data Engineering* expands this into the operational foundation of [[data-retention|data retention]] and automated [[data-lifecycle-management|lifecycle]] policies.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The three temperatures

Reis and Housley define the temperatures by how often the data is read (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

| Temperature | Access pattern | Typical home |
|---|---|---|
| **Hot** | Many times per day, perhaps multiple times per second | Fast storage for low-latency retrieval; serves live user requests |
| **Lukewarm** | Every so often — weekly or monthly | Standard warehouse / lake tables |
| **Cold** | Seldom queried; retained for compliance or in case of catastrophic failure elsewhere | Archival tier (cheap storage, expensive retrieval) |

"Fast" is relative to the use case — hot data for a dashboard is not hot data for an advertising auction (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Cold-storage economics

In the "old days" cold data went onto tapes shipped to remote archival facilities. In the cloud, vendors offer specialised archival object-storage tiers (e.g., S3 Glacier, GCS Archive, Azure Archive) with **very cheap monthly storage costs but high retrieval prices** (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). This pricing shape reflects the economics: the physical media is slow and cold data is rarely read, so the cost of the rare read is amortised into the storage price.

This is a trap the engineer must be aware of: moving data to cold storage "to save cost" can backfire dramatically if the data ends up being queried more often than planned.

## Why it matters for architecture

Temperature is one of the primary inputs when choosing a storage technology (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Putting cold data on hot storage wastes money; putting hot data on cold storage destroys the user experience. [[data-lifecycle-management]] is partly about moving data through the temperature tiers as it ages.

## Ch 6 — hot, warm, cold with examples

Chapter 6 tightens the definitions and pairs each with typical hardware (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Hot data.** Instant or frequent access. Storage is SSD or RAM. Most expensive storage tier, but retrieval is cheap. **Examples:** product-recommendation results, product-page rendering. **Query-results cache** is another canonical hot-data store — re-serving the same query from cache rather than rerunning it.
- **Warm data.** "Semi-regular" access — roughly monthly. Cloud storage offers dedicated tiers: **S3 Standard-Infrequent Access**, **GCS Nearline**. Cheaper storage than hot; higher retrieval costs.
- **Cold data.** Rarely accessed; retained for compliance or disaster recovery. Typical storage: HDD, tape, or cloud archival tiers (S3 Glacier, GCS Archive). Storage is cheap; retrieval is slow and expensive.

The pricing shape is deliberate: cold-storage cost inverts between storage and retrieval so that the rare read carries most of the cost.

## Ch 6 — the cold-storage trap

Chapter 6 is explicit about the operational hazard: "Be aware of how you plan to utilize archival storage, as it's easy to get into and often costly to access data, especially if you need it more often than expected" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). S3 Glacier Deep Archive can cost as little as $1/TB/month, but retrieval takes up to 12 hours and is priced for one-to-two accesses per year over 7–10 year retention. Data that gets accessed more often than planned erases the saving many times over.

## Ch 6 — spillover and lifecycle automation

A practical operational pattern Chapter 6 introduces (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- Memory is expensive and finite — hot data in RAM spills to SSD/HDD when memory fills up.
- Databases increasingly spill infrequently accessed data to warm/cold tiers, often to **object storage** for cost efficiency. In cloud managed services this is automatic.
- For cloud object storage, the engineer should **set up lifecycle policies**: after 30 days move to Infrequent Access, after 180 days move to archival, and so on. Chapter 6 is explicit: "This will drastically reduce your storage costs."

The lifecycle policy is the automation mechanism that makes the temperature model operational instead of aspirational. See [[data-retention]] for the retention-policy side.

## The storage cache hierarchy

Temperature slots into Chapter 6's broader cache hierarchy (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

| Tier | Latency | Price | Typical role |
|---|---|---|---|
| CPU cache | 1 ns | — | Processor-level cache |
| RAM | 0.1 μs | $10/GB | Hot data, caches |
| SSD | 0.1 ms | $0.20/GB | Hot-to-warm working storage |
| HDD | 4 ms | $0.03/GB | Bulk warm storage |
| Object storage | 100 ms | $0.02/GB/mo | Warm to cold |
| Archival | 12 hours | $0.004/GB/mo | Cold |

See [[storage-raw-ingredients]] for the underlying physics and [[storage-compute-separation]] for why the hot tiers are increasingly **caches in front of object storage** rather than primary storage.

## Related pages

- [[data-storage-stage]]
- [[data-lifecycle-management]]
- [[data-retention]]
- [[data-engineering-lifecycle]]
- [[backups-vs-archives]]
- [[storage-raw-ingredients]]
- [[object-storage]]
- [[cache-memory-storage]]
- [[storage-compute-separation]]
