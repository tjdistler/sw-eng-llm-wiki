# File Storage

**Summary**: The middle layer between raw [[block-storage]] and the abstraction of [[object-storage]]: an operating-system-managed **tree of directories and files** with random-access reads and writes, append operations, and directory metadata. Local filesystems (ext4, NTFS), Network-Attached Storage (NAS), and cloud file services (Amazon EFS, Google Filestore) all share these semantics.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## What defines a "file"

Chapter 6 gives a crisp three-property definition (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Finite length** — each file is a bounded stream of bytes.
2. **Append operations** — bytes can be added up to the host's storage limit.
3. **Random access** — any position can be read from or written to.

A [[file-storage|filesystem]] arranges files into a **directory tree**; each directory is metadata describing the files and subdirectories it contains, plus permissions and pointers. Resolving `/Users/matthewhousley/output.txt` walks the tree from root to leaf.

[[object-storage|Object storage]] only preserves the *finite length* property. Appends and random writes are gone. This is why object-store-as-filesystem adapters (s3fs, S3 File Gateway) degrade on transactional workloads.

## Local disk storage

The most familiar form: an OS-managed filesystem on a local partition. Standard implementations:

- **ext4** on Linux.
- **NTFS** on Windows.

Typical properties (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Full read-after-write consistency** within a single host.
- **Locking** to serialise concurrent writes to the same file.
- **Crash resilience** via **journaling** — unwritten-on-crash data is still lost, but the filesystem stays consistent.
- Optional advanced features: snapshots, redundancy across multiple disks, full-disk encryption, transparent compression.

## Network-Attached Storage (NAS)

A **NAS** exposes a filesystem over the network to multiple clients (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Protocols are commonly **NFS** or **SMB/CIFS**. Advantages over local filesystems:

- Shared access across many machines.
- Virtualised storage pools spanning multiple disks.
- Built-in redundancy and failover at the appliance level.

The price is latency: filesystem operations now cross a network. Also, **consistency varies by implementation** — multiple clients writing the same file can see partial state or stale reads, depending on the protocol and caching layer. The engineer must know their NAS's consistency model.

Contrast with [[block-storage|SAN]], which provides block-level access over the network rather than filesystem-level.

## Cloud filesystem services

Fully managed cloud equivalents (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Chapter 6's canonical example is **Amazon Elastic File System (EFS)**:

- Exposed over **NFSv4** (same protocol as traditional NAS).
- **Automatic scaling** and pay-per-storage pricing — no advance reservation.
- **Local read-after-write consistency** when reading from the same machine that wrote.
- **Open-after-close consistency** across the filesystem — once a writer closes a file, subsequent readers on any client see the changes.
- Accessible from multiple cloud VMs and potentially from outside the cloud.

Do not confuse a cloud filesystem service with **block storage attached to a VM** (EBS) — the latter is block-level and formatted by the VM's own OS. Cloud filesystem services are explicitly shared across clients.

## When to reach for file storage

In data-engineering pipelines, Chapter 6 is cautious (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> In cases where file storage paradigms are necessary for a pipeline, be careful with state and try to use ephemeral environments as much as possible. Even if you must process files on a server with an attached disk, use object storage for intermediate storage between processing steps. Try to reserve manual, low-level file processing for one-time ingestion steps or the exploratory stages of pipeline development.

In modern architectures, **[[object-storage]] is the default persistence layer**; file storage shows up at the boundaries — loading from an SFTP server, handing data to a tool that requires a POSIX filesystem — or as a short-lived working area.

## Related pages

- [[storage-raw-ingredients]]
- [[block-storage]]
- [[object-storage]]
- [[storage-engines]]
- [[distributed-filesystems]]
- [[data-storage-stage]]
