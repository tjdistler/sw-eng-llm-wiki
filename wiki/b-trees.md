# B-Trees

**Summary**: B-trees are the dominant indexing structure in relational databases. They organize data in fixed-size pages on disk and keep keys sorted, enabling efficient key-value lookups, range queries, and consistent read performance.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## Design

Introduced in 1970, B-trees break the database into fixed-size **pages** (traditionally 4 KB, sometimes larger). Each page can be identified by its disk address, allowing pages to reference each other like pointers.

One page is the **root**. The root contains keys and references to child pages. Each child is responsible for a continuous range of keys. Traversal follows references down the tree until reaching a **leaf page**, which contains the actual values (or references to where values are stored).

The **branching factor** — number of child references per page — is typically several hundred in practice, determined by page size and key sizes. A four-level B-tree with a branching factor of 500 and 4 KB pages can address 256 TB of data.

A B-tree with n keys has depth O(log n). Most databases fit into three or four levels.

## Reads and writes

**Lookup**: Start at the root, follow page references based on key ranges until reaching the leaf page containing the target key.

**Update**: Find the leaf page, modify the value in place, write the page back to disk.

**Insert**: Find the right page, add the key. If the page is full, split it into two half-full pages and update the parent page to reflect the split. This may cascade upward if the parent is also full.

This is a fundamental difference from [[sstables-and-lsm-trees|log-structured]] engines: B-trees overwrite pages in place rather than appending to files.

## Crash safety: the write-ahead log (WAL)

Overwriting multiple pages in a single operation (e.g., a page split) is dangerous: a crash mid-operation can leave the tree in a corrupted state.

The standard solution is a **write-ahead log** (WAL, also called redo log): an append-only file to which every B-tree modification is written before it is applied to the tree pages. On restart after a crash, the WAL is used to restore the tree to a consistent state.

This means every write touches disk at least twice: once to the WAL, once to the tree page. This contributes to B-tree [[write-amplification]].

## Concurrency

When multiple threads access a B-tree, careful concurrency control is required — a thread must not see the tree in an inconsistent state during a page split. This is handled with **latches** (lightweight locks) on the tree's data structures.

Log-structured engines like [[sstables-and-lsm-trees|LSM-trees]] are simpler here: compaction happens in the background, atomically swapping old segments for new ones.

## B-tree optimizations

Several refinements developed over decades:

- **Copy-on-write** (used by LMDB) — Instead of overwriting pages and maintaining a WAL, write modified pages to a new location and create a new version of parent pages pointing to the new location. Simplifies crash recovery and is useful for snapshot isolation.
- **Key abbreviation** — Interior pages don't need to store full keys, only enough to act as range boundaries. More keys per page → higher branching factor → fewer levels.
- **Sequential leaf layout** — Implementations try to keep leaf pages in sequential disk order for range scans, though maintaining this as the tree grows is difficult. (LSM-trees naturally achieve this during compaction.)
- **Sibling pointers** — Leaf pages may reference their left and right siblings, enabling in-order key scans without returning to parent pages.
- **Fractal trees** — A B-tree variant that borrows log-structured ideas to reduce disk seeks.

## B-trees vs LSM-trees

| Property | B-tree | LSM-tree |
|---|---|---|
| Read performance | Generally faster (one location per key) | Slower (must check memtable + multiple SSTable levels) |
| Write performance | Slower (page overwrites, WAL) | Generally faster (sequential appends) |
| Write amplification | Higher | Lower in many configurations |
| Disk space | More fragmentation | Better compression, less fragmentation |
| Read latency consistency | Predictable | Can spike during compaction |
| Transaction isolation | Easier (key exists in one place; lock ranges directly) | Harder (key may be in multiple segments) |

As a rule of thumb: LSM-trees are faster for writes; B-trees are thought to be faster for reads. Always benchmark with your actual workload — results are sensitive to configuration and access patterns.

## B-tree splitting in other contexts

The split-and-merge behavior of B-trees reappears in [[rebalancing-partitions#Strategy 2 Dynamic partitioning|dynamic partition splitting]]: when a database partition exceeds a configured size, it splits into two halves, similar to what happens at the top level of a B-tree. Conversely, when a partition shrinks below a threshold, it can merge with an adjacent partition (source: chapter-06-partitioning.md).

## Related pages

- [[storage-engines]]
- [[indexes]]
- [[sstables-and-lsm-trees]]
- [[write-amplification]]
- [[rebalancing-partitions]]
