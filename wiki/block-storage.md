# Block Storage

**Summary**: The raw storage interface provided by SSDs and magnetic disks — the disk is divided into **fixed-size addressable blocks**, and the client can read or write any block directly. In the cloud, **virtualised block storage** (Amazon EBS, equivalents on GCP and Azure) is the default storage for VMs; it preserves fine-grained random access while adding durability, snapshots, and scaling beyond a single physical disk.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## What a block is

A **block** is the smallest addressable unit of data on a disk: historically 512 bytes, now typically **4,096 bytes** on current drives (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Every disk write is block-aligned; blocks carry extra bits for error detection and metadata beyond the usable payload.

On magnetic media, blocks on the same track can be read without moving the head; blocks on different tracks require a seek. On SSDs, seek time between blocks is negligible by comparison.

Block storage provides **random-access** reads and writes. This is what transactional databases exploit: they lay out rows into blocks for optimal disk layout, use the disk's high random IOPS to service many small concurrent operations, and rely on predictable per-block write latency for write-ahead logging.

## RAID

**Redundant Array of Independent Disks (RAID)** treats multiple physical disks as one logical block device (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Various encoding and parity schemes exist, each trading bandwidth against fault tolerance:

- Striping for throughput (RAID 0).
- Mirroring for fault tolerance (RAID 1).
- Parity-based schemes (RAID 5/6) for capacity-efficient fault tolerance.

RAID is the single-server forerunner of cluster-level replication and erasure coding used by [[distributed-filesystems|HDFS]] and [[object-storage]].

## SAN and NAS

Two older network-storage abstractions worth distinguishing (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Storage Area Network (SAN)** — presents **block-level** storage over the network. The OS sees it as a block device and manages the filesystem. Used heavily on-premises for database and VM storage.
- **Network-Attached Storage (NAS)** — presents a **filesystem** over the network (NFS, SMB). See [[file-storage]].

Cloud virtualised block storage is essentially the cloud version of SAN.

## Cloud virtualised block storage

Chapter 6 uses **Amazon EBS** as the canonical example (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- Default storage for EC2 VMs; other clouds have equivalents.
- Exposed to the VM as a block device; the VM's OS formats and mounts it.
- Performance tiered by IOPS and throughput; higher tiers are SSD-backed, lower tiers are magnetic-backed.
- **Stored separately from the instance host**, but in the same availability zone for low latency. Volumes survive instance shutdown, host failure, and even instance deletion.
- **Replicated to at least two host machines** for fault tolerance. Suitable for databases where durability matters.
- **Point-in-time snapshots** while the drive is in use: EBS freezes block state at snapshot time while the VM keeps writing. Snapshots are **differential** after the first; only changed blocks are saved to [[object-storage|S3]].
- Scales to tens of TiB, hundreds of thousands of IOPS, multi-GiB/s throughput per volume.

Critical limitation: **EBS is not resilient to an availability-zone failure**. Cross-zone or cross-region durability requires snapshots, replication, or higher-level storage.

## Local instance volumes

The other block-storage flavour in the cloud: **instance store volumes** physically attached to the VM host (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Characteristics:

- **Low cost** — often bundled into the VM price.
- **Very low latency and high IOPS** — like a physical disk in the same box.
- **Ephemeral.** When the VM shuts down, is deleted, or the host fails, the contents are gone. This is by design: the host clears the disk before allocating it to another customer.
- **No snapshots, no replication, no advanced virtualization features.**

Instance stores are useful as a **local cache** rather than durable storage: pull from object storage, stage locally, process, write results back to durable storage, then delete the VM. This is the standard pattern for ephemeral processing clusters like AWS EMR running Spark or MapReduce (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

## Block vs object storage

| Aspect | Block storage | [[object-storage]] |
|---|---|---|
| Interface | Fixed-size blocks, random read/write | Key → immutable object |
| Update semantics | In-place | Rewrite whole object |
| Typical latency | 0.1 ms (SSD) / 4 ms (HDD) | ~100 ms |
| Parallelism ceiling | Bounded by disk/controller IOPS | Virtually unlimited across cluster |
| Cost per GB | $0.03–$0.20/GB | ~$0.02/GB per month |
| Best fit | OLTP, VM boot disks, databases | OLAP, data lakes, backups |

Modern data architectures use **both**: object storage for durable long-term data, block storage on VMs as a faster cache or working area during processing. This hybrid is part of what [[storage-compute-separation]] actually looks like in practice.

## Related pages

- [[storage-raw-ingredients]]
- [[object-storage]]
- [[file-storage]]
- [[storage-compute-separation]]
- [[data-storage-stage]]
- [[distributed-filesystems]]
- [[storage-engines]]
