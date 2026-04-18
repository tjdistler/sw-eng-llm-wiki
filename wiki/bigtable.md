# Bigtable

**Summary**: Google's NoSQL database for petabyte-scale data. A Bigtable is a "sparse, distributed, persistent multidimensional sorted map" indexed by row key, column key, and timestamp, with values as uninterpreted byte arrays. Bigtable supports eventually consistent cross-datacenter replication.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## Data model

A Bigtable is (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- **Sparse** — cells can be absent; no schema-required shape.
- **Distributed** — data is partitioned across many machines.
- **Persistent** — backed by [[colossus]] for durability.
- **Multidimensional sorted map** — indexed by `(row key, column key, timestamp)`.
- **Uninterpreted values** — each cell is an array of bytes; the client decides how to read it.

The tuple-indexed sorted-map model is different from both the [[relational-model|relational]] and [[document-model|document]] worlds. It descends from Google's 2006 Bigtable paper and is the inspiration for HBase, Cassandra's column family layout, and Accumulo.

## Consistency

Bigtable supports **eventually consistent, cross-datacenter replication** (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). For use cases that need real global consistency, Google offers [[spanner]] instead.

This makes Bigtable a concrete instance of the [[eventual-consistency|eventually-consistent]] trade-off discussed in the Kleppmann chapter: sacrifice synchronous coordination for bandwidth and latency.

## Where it fits at Google

Bigtable is one of several database-like services built on top of [[colossus]]. Others include [[spanner]] and Blobstore (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Each comes with its own trade-offs; Chapter 26 of the SRE book covers them in depth.

In the Chapter 2 Shakespeare example, Bigtable is the backend store for the word-index: the [[mapreduce|MapReduce]] batch job writes `(word, list of locations)` tuples into Bigtable rows keyed by the word. See [[life-of-a-request]] for the full trace.

## Cross-book connections

- [[nosql]] — Bigtable is a canonical NoSQL store.
- [[eventual-consistency]] — its replication model.
- [[sstables-and-lsm-trees]] — SSTables were invented inside Bigtable; the wiki's LSM page cites Bigtable as the origin.
- [[column-oriented-storage]] — Bigtable's column families are a stepping stone toward columnar storage, though Bigtable itself is not a pure column store.

## Related pages

- [[colossus]]
- [[spanner]]
- [[eventual-consistency]]
- [[nosql]]
- [[sstables-and-lsm-trees]]
- [[site-reliability-engineering]]
