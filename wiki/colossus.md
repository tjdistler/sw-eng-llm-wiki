# Colossus

**Summary**: Google's cluster-wide distributed filesystem, successor to GFS (the Google File System). Colossus is built on top of the D fileserver layer and offers standard filesystem semantics plus replication and encryption. It is the storage substrate for Bigtable, Spanner, and the rest of Google's higher-level database services.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## The storage stack

Google's cluster storage is layered. From the bottom up (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

| Layer | What it does |
|---|---|
| **D** | A fileserver running on almost every machine in a cluster, exposing its local disks (spinning and flash). |
| **Colossus** | A cluster-wide filesystem layered over all D instances. Offers normal filesystem semantics plus replication and encryption. |
| **Bigtable / Spanner / Blobstore** | Database-like services built on top of Colossus. |

The reason for the two bottom layers is that users don't want to remember which machine stores their data; Colossus hides that detail. D is the per-machine primitive that Colossus aggregates (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Successor to GFS

Colossus is the successor to GFS, the Google File System described in the 2003 SOSP paper (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). GFS inspired Hadoop's [[distributed-filesystems|HDFS]]: the SRE book notes that the Google storage stack is "comparable to Lustre and the Hadoop Distributed File System (HDFS), which are both open source cluster filesystems."

The HDFS cross-reference is important for the wiki: [[distributed-filesystems]] already covers the HDFS-side mechanics (NameNode, block replication, erasure coding, data locality). Colossus is the internal Google analogue, with the same shared-nothing principle but a proprietary implementation.

## What runs on top

- [[bigtable]] — NoSQL database for petabyte-scale sparse sorted maps.
- [[spanner]] — SQL-like globally consistent database.
- **Blobstore** — blob storage service.

Each comes with its own trade-offs; Chapter 26 of the SRE book covers them in more depth.

## Cross-book connections

- [[distributed-filesystems]] — HDFS, the open-source analogue; shared-nothing commodity-hardware design.
- [[unix-philosophy]] — HDFS is positioned as "the file descriptor" of the Hadoop ecosystem; Colossus plays the equivalent role inside Google.

## Related pages

- [[bigtable]]
- [[spanner]]
- [[distributed-filesystems]]
- [[google-datacenter-topology]]
- [[site-reliability-engineering]]
