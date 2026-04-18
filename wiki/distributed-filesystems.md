# Distributed Filesystems

**Summary**: A distributed filesystem spreads file storage across many machines in a shared-nothing cluster, providing a single logical filesystem with fault tolerance through replication or erasure coding. HDFS is the dominant open-source implementation.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## HDFS (Hadoop Distributed File System)

HDFS is an open-source reimplementation of Google File System (GFS). It is the standard filesystem for [[mapreduce]] and the broader Hadoop ecosystem (source: designing-data-intensive-applications, chapter 10).

### Architecture

HDFS uses a **shared-nothing** architecture — commodity machines connected by a conventional datacenter network, with no special hardware (source: designing-data-intensive-applications, chapter 10):

- A **daemon process** runs on each machine, exposing a network service for accessing locally stored files.
- A **NameNode** (central server) tracks which file blocks are stored on which machines.
- The result is one logical filesystem spanning the disks of all machines in the cluster.

### Fault tolerance

File blocks are replicated on multiple machines to tolerate disk and machine failures. Two approaches (source: designing-data-intensive-applications, chapter 10):

- **Full replication** — Multiple identical copies of each block, similar to [[replication]] in databases.
- **Erasure coding** (e.g., Reed-Solomon codes) — Allows recovery of lost data with lower storage overhead than full replication, similar to RAID but across machines over a network.

### Scale

The largest HDFS deployments run on tens of thousands of machines with combined storage of hundreds of petabytes. This scale is viable because HDFS uses commodity hardware and open-source software, at much lower cost than dedicated storage appliances (source: designing-data-intensive-applications, chapter 10).

### Data locality

The MapReduce scheduler tries to run map tasks on machines that store replicas of their input files — **putting computation near the data**. This saves network bandwidth. However, if erasure coding is used instead of replication, the locality advantage is lost because data from multiple machines must be combined to reconstruct the original file (source: designing-data-intensive-applications, chapter 10).

## Google's stack: D + Colossus

Google's internal cluster storage is the direct ancestor of this family. The SRE book's Chapter 2 describes a two-layer split (source: site-reliability-engineering, chapter 2):

- **D** — a fileserver running on almost every machine in a cluster, exposing its local spinning and flash disks.
- **[[colossus]]** — a cluster-wide filesystem layered over all D instances, offering normal filesystem semantics plus replication and encryption. Colossus is the successor to **GFS**, the Google File System described in the 2003 SOSP paper.

HDFS is an open-source reimplementation of GFS, so the Hadoop ecosystem and Google's internal stack are siblings descending from the same design. Bigtable, Spanner, and Blobstore all sit on top of Colossus, the same way HBase and Impala sit on top of HDFS.

## Other distributed filesystems

Besides HDFS, alternatives include GlusterFS and the Quantcast File System (QFS). Object storage services (Amazon S3, Azure Blob Storage, OpenStack Swift) are similar in many ways, though they typically separate storage from computation, while HDFS co-locates them (source: designing-data-intensive-applications, chapter 10).

## Shared-nothing vs shared-disk

HDFS's shared-nothing approach contrasts with shared-disk architectures like NAS (Network Attached Storage) and SAN (Storage Area Network), which use centralized storage appliances with custom hardware and special network infrastructure like Fibre Channel (source: designing-data-intensive-applications, chapter 10).

## Role in the data ecosystem

HDFS serves as the uniform interface for the Hadoop ecosystem — analogous to the file descriptor in [[unix-philosophy]]. Multiple processing models can coexist on the same cluster, all reading and writing HDFS (source: designing-data-intensive-applications, chapter 10):

- [[mapreduce]] for batch processing
- [[dataflow-engines]] (Spark, Tez, Flink) for optimized batch workflows
- HBase for random-access OLTP (using [[sstables-and-lsm-trees]])
- Impala for MPP-style analytics
- Pregel-style [[graph-batch-processing]]

This diversity of processing models on a shared filesystem is a key advantage over monolithic MPP databases. See [[hadoop-vs-mpp-databases]] (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[unix-philosophy]]
- [[replication]]
- [[hadoop-vs-mpp-databases]]
- [[partitioning]]
- [[colossus]]
