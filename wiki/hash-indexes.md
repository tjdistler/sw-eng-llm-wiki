# Hash Indexes

**Summary**: A hash index maps every key to a byte offset in an append-only log file. It offers very fast reads and writes when all keys fit in RAM, but cannot support range queries.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## How it works

The simplest possible key-value store: append every write to the end of a file. To read, scan backward for the last occurrence of the key.

Writes are fast (sequential append). Reads are O(n) without an index.

The hash index adds an in-memory hash map where every key maps to the byte offset of its most recent value in the log file. On a write, append the record and update the hash map. On a read, look up the offset in the hash map, then seek directly to that position in the file.

This is essentially what **Bitcask** (the default storage engine in Riak) does. It offers high-performance reads and writes with one constraint: all keys must fit in RAM. Values can exceed available memory because they're loaded from disk with a single seek.

## Segment compaction

Appending forever would exhaust disk. The solution:

1. **Segments** — close the log file when it reaches a size threshold, start a new segment for subsequent writes.
2. **Compaction** — within a segment, throw away duplicate keys and keep only the most recent value per key.
3. **Merging** — compact multiple segments together into a new file simultaneously. Merging runs in a background thread; reads continue against the old segments until merging completes, then reads switch to the new merged segment and old segments are deleted.

Each segment has its own in-memory hash map. A lookup checks the most-recent segment's hash map first, then works backward through older segments.

## Implementation details

Several practical issues in a real implementation:

**File format** — Binary format (length-prefixed) is faster and simpler than CSV.

**Tombstones** — To delete a key, append a tombstone record. During compaction, the tombstone signals that all prior values for that key should be discarded.

**Crash recovery** — In-memory hash maps are lost on restart. Rebuild them by scanning segment files (slow for large files). Bitcask speeds this up by storing a snapshot of each segment's hash map on disk.

**Partial writes** — A crash mid-write leaves a corrupted record. Bitcask uses checksums to detect and ignore corrupted parts.

**Concurrency** — Writes are strictly sequential, so a single writer thread is typical. Multiple threads can read concurrently since segment files are immutable after writing.

## Why append-only is better than overwriting in place

Counterintuitive but true:
- **Sequential writes are much faster than random writes**, especially on spinning disks, and meaningfully faster on SSDs too.
- **Crash recovery is simpler** — no risk of a half-written value splicing old and new data.
- **Merging prevents fragmentation** — data files don't develop holes over time.

## Limitations

- **All keys must fit in RAM.** On-disk hash maps require too many random I/O accesses to be practical.
- **No range queries.** Cannot scan keys between `kitty00000` and `kitty99999`; each would require a separate lookup.

These limitations led to [[sstables-and-lsm-trees]], which address both.

## Related pages

- [[storage-engines]]
- [[indexes]]
- [[sstables-and-lsm-trees]]
- [[write-amplification]]
