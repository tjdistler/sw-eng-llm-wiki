# Storage Raw Ingredients

**Summary**: Reis and Housley's framing for the lowest level of storage design: before you reach for an object store or a warehouse, understand the **physical and software building blocks** they are assembled from — magnetic disk, SSD, RAM, networking, CPU, serialization, compression, and caching. Every storage system higher in the stack inherits the trade-offs of its raw ingredients.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Why this layer matters

Chapter 6 opens with a three-layer model (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Raw ingredients** — magnetic disks, SSDs, RAM, networking, CPU, serialization, compression, caching.
2. **Storage systems** — single-machine vs distributed storage, object storage, HDFS, cache systems, streaming storage.
3. **Storage abstractions** — data warehouses, data lakes, lakehouses, data platforms.

Even when cloud services hide the hardware, "data engineers still need to be aware of underlying components' essential characteristics, performance considerations, durability, and costs" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). In most architectures, data passes through magnetic storage, SSDs, and memory several times on its way through a pipeline.

## Magnetic disk (HDD)

HDDs spin a ferromagnetic platter under a read/write head. They remain the backbone of bulk storage because they are ~10× cheaper per gigabyte than SSDs — roughly **3 cents/GB** vs. 20–30 cents/GB at the time of the book (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

Key physical limits:

- **Transfer speed** scales with linear bit density, while capacity scales with areal density. Double capacity and you only get ~40% more transfer. Current data-center HDDs top out at 200–300 MB/s — reading a 30 TB drive end-to-end takes over 20 hours.
- **Seek time** — the head must physically move between tracks.
- **Rotational latency** — 7,200 RPM drives add ~4 ms average access latency.
- **IOPS** — 50 to 500 per drive; terrible for transactional workloads.

Tricks help (higher RPM, narrower platter radius) but do not close the gap to SSDs. What HDDs still do well is **parallel bulk throughput**: a cluster of thousands of HDDs can aggregate to multiple GB/s, limited by network rather than disk. This is the design point of [[object-storage]] and [[distributed-filesystems]] (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

## Solid-state drive (SSD)

SSDs store charges in NAND flash cells. No moving parts means (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Random lookups** in under 0.1 ms (100 μs).
- **IOPS** in the tens of thousands per drive.
- **Transfer speeds** of multiple GB/s.

SSDs revolutionised OLTP — PostgreSQL/MySQL/SQL Server routinely handle thousands of TPS on them. They are the accepted standard for commercial OLTP deployments. For OLAP at scale, cost wins: magnetic object storage is still the economic foundation, with SSDs used as cache tiers for hot analytics data.

SSDs have their own quirks not fully explored in Chapter 6 but relevant: flash cells wear with writes, the firmware runs a log-structured garbage collector, and block sizes differ from HDDs — see [[write-amplification]] for the downstream consequences.

## RAM

RAM is **volatile**: on power loss it clears in under a second. But it offers ~100 ns access latency (~1,000× faster than SSD), ~100 GB/s CPU-to-memory bandwidth, and millions of IOPS (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Price is ~$10/GB — roughly 50× SSD, 300× HDD.

Chapter 6 flags three architectural uses:

- **Caching** — the normal case; data is also persisted elsewhere.
- **Data processing** — Spark's in-memory model; see [[storage-compute-separation]].
- **Primary storage layer** — in-memory databases (Redis with persistence, SAP HANA, MemSQL). Durability requires battery backups or aggressive snapshotting to disk because a single power event can destroy the dataset.

The CPU itself has **multiple cache tiers** (L1–L4) that sit above RAM in the hierarchy — faster still, but much smaller and fully managed by the hardware.

## Networking and CPU

"Why mention networking and CPU as raw ingredients for storing data?" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Because modern storage is distributed:

- Single HDDs are slow, but a cluster of thousands aggregates to enormous throughput. The bottleneck is the network.
- Cloud object-storage clusters span availability zones, data centers, even regions — **CPUs** handle request routing, load balancing, and aggregation; **network performance and topology** determine realised throughput.
- Spreading data geographically buys durability and availability at the cost of latency — engineers constantly balance the two.

The practical implication: storage becomes a **web application** with APIs and backend services. Understanding the network is part of understanding storage.

## Serialization

Serialization packs in-memory data structures into a byte stream that can be stored or transmitted and later decoded. Choices here ripple upward:

- **Row-oriented** formats (CSV, JSON, XML, Avro) suit quick lookups and in-place updates.
- **Columnar** formats ([[column-oriented-storage|Parquet, ORC]]) suit high-compression scans over huge volumes.
- **Hybrid** formats (Apache Hudi) combine aspects of both.
- **In-memory** formats (Apache Arrow) optimise for zero-copy sharing between processes.

Chapter 6 recommends data engineers become familiar with Parquet, Hudi, and Arrow in particular (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). See [[encoding-formats]] for the broader DDIA treatment, and [[schema-evolution]] for how format choice constrains evolution.

## Compression

Compression pays off three ways (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Smaller on disk** — direct storage cost savings.
2. **Higher effective scan speed** — at 10:1 compression, a 300 MB/s HDD delivers 3 GB/s of logical data.
3. **Higher effective network bandwidth** — a 10 Gbps EC2-to-S3 link at 10:1 delivers 100 Gbps of logical payload.

The cost is CPU time to compress and decompress. See [[compression-algorithms]] for concrete algorithm trade-offs (gzip, bzip2, snappy, LZ4, LZMA, zstd).

## Caching and the storage hierarchy

Caching is the glue. Every practical storage system assembles multiple cache layers with varying latency, bandwidth, and cost. Chapter 6 lays out a heuristic cache hierarchy (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

| Tier | Fetch latency | Bandwidth | Price |
|---|---|---|---|
| CPU cache | 1 ns | 1 TB/s | — |
| RAM | 0.1 μs | 100 GB/s | $10/GB |
| SSD | 0.1 ms | 4 GB/s | $0.20/GB |
| HDD | 4 ms | 300 MB/s | $0.03/GB |
| Object storage | 100 ms | 3 GB/s per instance | $0.02/GB per month |
| Archival storage | 12 hours | same as object once retrieved | $0.004/GB per month |

Chapter 6 introduces **archival storage as a reverse cache**: worse access for lower cost, used for backups and retention compliance.

The hierarchy is the starting point for two critical downstream ideas:

- **[[data-temperature|Hot / warm / cold data]]** — matching access frequency to the right tier.
- **[[storage-compute-separation]]** — object storage at the bottom, faster tiers spun up on demand.

## Related pages

- [[data-storage-stage]]
- [[object-storage]]
- [[block-storage]]
- [[file-storage]]
- [[compression-algorithms]]
- [[encoding-formats]]
- [[column-oriented-storage]]
- [[data-temperature]]
- [[storage-compute-separation]]
- [[write-amplification]]
- [[distributed-filesystems]]
