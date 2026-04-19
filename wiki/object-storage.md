# Object Storage

**Summary**: A **key-value store for immutable data objects** — any byte sequence, any size, addressed by a key inside a flat bucket namespace. Object storage is the economic and architectural foundation of modern cloud data platforms: [[data-lake|data lakes]], [[data-lakehouse|lakehouses]], and cloud [[data-warehousing|warehouses]] all sit on top of it. Amazon S3, Google Cloud Storage (GCS), and Azure Blob Storage are the big three.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## What makes it an object store

Object storage behaves *like* file storage but with sharper edges (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Finite length.** Each object is a fixed-length stream of bytes written once.
- **No in-place writes.** You cannot modify an object or append to it. To "change" an object you must **rewrite it fully** under the same key.
- **No directory tree.** Buckets are flat; keys with slashes *look* like paths but are just strings. "Directory" operations (`ls` a prefix) are filtered key scans and can be expensive.
- **Immutability.** The core affordance: once written, an object cannot change. This is what allows object stores to fan out across thousands of disks without coordination.

Reads support **range requests** (random byte-range reads within an object), though these are slower than SSD-backed random access.

## Why immutability buys scale

Because objects are never modified in place, object stores do not need locks or change synchronisation across the cluster. This lets them scale writes and reads massively:

- **Parallel throughput.** Write speed scales with the number of concurrent streams (up to vendor quotas). Read bandwidth scales with the number of parallel requests, VMs, and CPU cores (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).
- **Durability.** Typical cloud object stores replicate across multiple availability zones. An entire zone can fail without data loss.
- **Virtually limitless capacity.** Vendors handle exabytes. For a customer, the only practical limit is budget.
- **Serverless management.** "Object storage was arguably one of the first 'serverless' services; engineers don't need to consider the characteristics of underlying server clusters or disks" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

The trade-off is that **transactional workloads** with many small updates per second are a poor fit — those belong on transactional databases or [[block-storage]]. Object stores excel at **large batch reads and writes**, the OLAP access pattern.

## Key lookup — it is not a filesystem

A typical S3 reference:

```
S3://oreilly-data-engineering-book/project-data/11/23/2021/data.txt
```

The bucket is `oreilly-data-engineering-book`; the key is the full suffix. The path-like slashes are **part of the key string**, not a directory hierarchy. Listing "directory" contents means filtering keys by prefix — a cluster-wide operation whose cost scales with the number of keys in the bucket, not the number in the "directory" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Engineers used to filesystem semantics are frequently surprised by this.

## Consistency and versioning

Object stores have historically been **[[eventual-consistency|eventually consistent]]**. S3 was until late in its history: after a new version was written under the same key, a read might still return the old version for some time (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). AWS made S3 strongly consistent for PUTs and GETs in 2020, but many on-prem and smaller-cloud object stores remain eventually consistent.

Layering strong consistency on top is possible and standard. The canonical recipe (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. Write the object to the object store.
2. Write the returned version metadata (hash or timestamp + key) to a **strongly consistent database** (e.g. PostgreSQL).
3. To read: fetch the latest metadata from the database, then query the object by key+version. Retry if mismatch.

This is effectively how the [[lakehouse-table-formats|lakehouse table formats]] (Delta Lake, Iceberg, Hudi) achieve ACID transactions over eventually-consistent object storage.

**Object versioning** is closely related. With versioning on, rewriting a key creates a new version while prior versions remain accessible. Each (key, version) pair uniquely identifies an immutable object. Versioning solves the consistency problem for versioned reads, at the cost of storing full copies — not diffs — of every version (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). **Storage lifecycle policies** automate deletion of old versions or migration to archival tiers to keep costs in check.

## Storage classes and tiers

Cloud object stores expose a menu of **storage classes** that trade access speed and durability for price (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Standard.** Full durability, multi-zone replication, immediate access.
- **Infrequent Access** (S3 Standard-IA, GCS Nearline). Cheaper storage, higher retrieval cost.
- **One Zone-IA.** Single-zone replication; 99.5% rather than 99.9% availability; destroyed if the zone goes.
- **Archival** (S3 Glacier, Glacier Deep Archive, GCS Archive, Azure Archive). Cheap storage (starting ~$1/TB/month for Deep Archive); retrieval takes minutes to 12 hours; intended for 7–10 year retention, 1–2 accesses per year.

These map directly onto the [[data-temperature|hot/warm/cold]] framework and are the operational mechanism behind [[data-retention|data retention and lifecycle]] policies.

## Object storage for data engineering

From the data-engineering perspective (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Excellent** for large batch reads and writes — the OLAP pattern.
- **Poor** for high-frequency small updates — use an OLTP database instead.
- **Usable** for low-rate update workloads that touch large objects each time. The "object stores are bad for updates" folklore is only partially true.
- **Gold standard** for [[data-lake|data lakes]]. The early WORM (write-once, read-many) pattern was a workaround for update complexity, not a fundamental limitation. Systems like **Apache Hudi** and **Delta Lake** now make update/delete management practical. See [[lakehouse-table-formats]].
- **Ideal repository for unstructured data** — images, video, audio, raw text — used heavily by ML pipelines.

## Object-store-backed filesystems

Tools like **s3fs** and **Amazon S3 File Gateway** mount an object-storage bucket as a local filesystem. They work well for infrequently-updated files, but **high-speed transactional writing will overwhelm the update capabilities of the object store** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

## Role in storage-compute separation

Object storage is the central enabler of [[storage-compute-separation]]. Because it is cheap, serverless, and independently scalable, compute clusters can be spun up on demand, read what they need, do their work, and be torn down — without moving the data. This is the reason cloud data warehouses (Snowflake, BigQuery) and [[data-lakehouse|lakehouses]] outperform earlier colocated architectures for many workloads.

## Cross-book connections

- [[distributed-filesystems]] (DDIA) — HDFS and its descendants. Object stores are similar in spirit but typically separate storage from computation, where HDFS co-locates them.
- [[colossus]] (SRE) — Google's internal cluster filesystem. BigQuery uses Colossus features (like **fine-grained data block placement**, not exposed publicly) to achieve "hybrid object storage" with some of the locality of colocated systems.

## Related pages

- [[storage-raw-ingredients]]
- [[data-lake]]
- [[data-lakehouse]]
- [[storage-compute-separation]]
- [[data-temperature]]
- [[data-retention]]
- [[lakehouse-table-formats]]
- [[block-storage]]
- [[file-storage]]
- [[distributed-filesystems]]
- [[eventual-consistency]]
- [[colossus]]
