# Partitioning and Secondary Indexes

**Summary**: Secondary indexes do not map neatly to partitions because they search by value rather than by primary key. Two approaches exist: document-partitioned (local) indexes that require scatter/gather reads, and term-partitioned (global) indexes that require multi-partition writes.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`

**Last updated**: 2026-04-15

---

## The problem

[[partitioning-strategies|Partitioning strategies]] assign records to partitions based on their primary key. [[indexes|Secondary indexes]], however, search by a non-primary attribute (e.g., "find all red cars"). There is no guarantee that all records matching a secondary index query live on the same partition. This creates a fundamental tension between read efficiency and write efficiency.

Some key-value stores (HBase, Voldemort) originally avoided secondary indexes entirely because of this complexity. Others (Riak, Elasticsearch, Solr) treat them as essential. Search servers like Solr and Elasticsearch exist specifically to provide secondary indexes.

**Caution on DIY indexes**: If your database only supports a key-value model, you might be tempted to implement a secondary index yourself by maintaining a mapping from values to document IDs in application code. This is risky -- race conditions and intermittent write failures can easily cause the index to go out of sync with the underlying data. Multi-object transactions are needed to keep such indexes consistent (source: chapter-06-partitioning.md).

## Document-partitioned indexes (local indexes)

Each partition maintains its own secondary index covering only the documents stored in that partition. The index is local to the partition.

**Writes are simple**: when a document is added or updated, only the partition containing that document needs to update its local index.

**Reads require scatter/gather**: a query like "find all red cars" must be sent to every partition because red cars may exist on any partition. All results are combined by the client or a coordinating node. This scatter/gather pattern is prone to tail latency amplification (see [[response-time-percentiles]]) because the overall query is only as fast as the slowest partition.

**Used by**: MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud, VoltDB.

Database vendors recommend structuring partitioning so that secondary index queries can be served from a single partition, but this is not always possible, particularly when filtering on multiple secondary indexes simultaneously (e.g., cars filtered by both color and make).

## Term-partitioned indexes (global indexes)

A global secondary index covers data from all partitions. The index itself is partitioned, but by the indexed term rather than by the document's primary key. The name "term" comes from full-text indexes, where the terms are all the words that occur in a document (source: chapter-06-partitioning.md). For example, index entries for colors a-r might live on partition 0, and s-z on partition 1.

The global index can be partitioned by the term value itself (enabling range scans on the indexed field) or by a hash of the term (for more even load distribution).

**Reads are efficient**: a client only needs to query the single partition that owns the relevant term, avoiding scatter/gather.

**Writes are more complex**: writing a single document may require updating multiple index partitions (one per indexed term), potentially on different nodes. In an ideal world, the index would update synchronously, but this would require a distributed transaction. In practice, global secondary index updates are often **asynchronous** — a read shortly after a write may not yet reflect the change.

**Example**: Amazon DynamoDB states that its global secondary indexes are updated within a fraction of a second normally, but may lag during infrastructure faults.

**Used by**: Riak (search feature), Oracle data warehouse (offers a choice between local and global indexing), Amazon DynamoDB. The topic of implementing term-partitioned secondary indexes is revisited in later chapters on derived data (source: chapter-06-partitioning.md).

## Comparison

| Property | Document-partitioned (local) | Term-partitioned (global) |
|---|---|---|
| Write cost | Single partition | Multiple partitions |
| Read cost | Scatter/gather (all partitions) | Single partition |
| Index freshness | Immediate | Often asynchronous |
| Complexity | Simpler | Requires cross-partition coordination |

## Related pages

- [[partitioning]]
- [[partitioning-strategies]]
- [[indexes]]
- [[response-time-percentiles]]
- [[rebalancing-partitions]]
