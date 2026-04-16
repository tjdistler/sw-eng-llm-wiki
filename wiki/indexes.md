# Indexes

**Summary**: An index is additional metadata derived from the primary data that lets a database locate values quickly. Every index speeds up reads at the cost of slowing writes.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## The core tradeoff

Without an index, finding a value requires scanning every record — O(n). An index maintains a data structure that can locate a value in O(log n) or O(1).

The cost: every index must be updated on every write. The more indexes, the slower writes become. Databases don't index everything by default — the developer chooses which indexes to create based on query patterns.

> "Well-chosen indexes speed up read queries, but every index slows down writes." (source: chapter-03-storage-and-retrieval.md)

## Primary vs secondary indexes

A **primary key index** uniquely identifies one row, document, or vertex. Other records reference it by ID.

A **secondary index** is built on non-unique fields. Multiple rows may share the same key, so the index value is either a list of matching row IDs or each entry is made unique by appending a row identifier.

Both [[b-trees]] and [[sstables-and-lsm-trees|log-structured]] storage support secondary indexes.

## How the value is stored

When a key matches, the index points to the data in one of two ways:

**Heap file reference** — The index stores a pointer to a heap file where rows are stored in no particular order. Multiple secondary indexes all point to the same heap, avoiding data duplication. Updating a value in place works as long as the new value fits in the same space; otherwise, all indexes need updating or a forwarding pointer is left.

**Clustered index** — The actual row data is stored within the index itself. MySQL InnoDB always uses the primary key as a clustered index; secondary indexes store the primary key value rather than a heap location. Eliminates the extra hop, but duplicates data and adds write overhead.

**Covering index** (index with included columns) — A middle ground: stores some columns inside the index but not all. Allows certain queries to be answered from the index alone ("the index covers the query").

## Multi-column indexes

**Concatenated index** — Combines several columns into one key in a fixed order (e.g., lastname + firstname). Useful for queries on the prefix columns; useless for queries on non-prefix columns alone.

**Multi-dimensional index** — Necessary when querying multiple independent dimensions simultaneously (e.g., latitude AND longitude, date AND temperature). Standard B-tree and LSM-tree indexes can only efficiently range-query one dimension at a time. Solutions:
- Space-filling curves (translate 2D to 1D, then use a regular B-tree)
- R-trees (used by PostGIS for geospatial data)
- HyperDex uses multi-dimensional indexing for key-value stores

## Fuzzy / full-text indexes

All the index structures above assume exact data. Full-text search requires fuzzy matching — synonyms, grammatical variations, edit distances, proximity. Lucene stores its term dictionary in SSTable-like sorted files and uses a finite state automaton (similar to a trie) to support efficient search within a given edit distance (Levenshtein automaton).

## In-memory considerations

All indexing structures discussed here were developed to manage disk's constraints. The key insight about in-memory databases: their performance advantage is not from avoiding disk reads (the OS caches hot pages anyway) — it's from avoiding the overhead of encoding in-memory data structures into a disk-serializable form.

## Indexes and partitioning

In a partitioned database, secondary indexes create a fundamental tension: the index may reference data spread across multiple partitions. Two approaches exist -- document-partitioned (local) indexes that are co-located with the data but require scatter/gather reads, and term-partitioned (global) indexes that enable single-partition reads but require multi-partition writes. See [[partitioning-secondary-indexes]] for details (source: chapter-06-partitioning.md).

## Related pages

- [[storage-engines]]
- [[hash-indexes]]
- [[sstables-and-lsm-trees]]
- [[b-trees]]
- [[column-oriented-storage]]
- [[partitioning-secondary-indexes]]
