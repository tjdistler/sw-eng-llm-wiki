# Partitioning Strategies

**Summary**: Two fundamental strategies exist for assigning records to partitions — key-range partitioning and hash partitioning — each with distinct trade-offs around range query efficiency and load distribution.

**Sources**: raw/designing-data-intensive-applications/chapter-06-partitioning.md

**Last updated**: 2026-04-15

---

## Why not random assignment?

The simplest way to avoid [[hot-spots]] would be to assign records to nodes randomly. This distributes data evenly, but has a fatal disadvantage: when reading a particular item, there is no way of knowing which node holds it, so every read must query all nodes in parallel. We can do better with structured partitioning schemes (source: chapter-06-partitioning.md).

## Key-range partitioning

Each partition owns a contiguous range of keys (minimum to maximum), like volumes of an encyclopedia. Given the boundaries, any node can quickly determine which partition holds a key.

**Advantages**:
- Enables efficient range scans — keys within a range are stored together.
- Within each partition, keys can be kept in sorted order (see [[sstables-and-lsm-trees]]). The key can be treated as a concatenated index to fetch several related records in one query (source: chapter-06-partitioning.md).
- Used by Bigtable, HBase, RethinkDB, and MongoDB (pre-2.4).

**Disadvantages**:
- Ranges are not necessarily evenly spaced — they must be sized to match actual data distribution. For example, in an encyclopedia, volume 1 might contain words starting with A and B, while volume 12 contains T, U, V, X, Y, and Z. Simply assigning one volume per two letters would produce very uneven volumes (source: chapter-06-partitioning.md). Boundaries are chosen manually or automatically.
- Certain access patterns cause [[hot-spots]]. If the partition key is a timestamp and writes are always "now", every write goes to the current day's partition. Prefixing the key with sensor name distributes the load, but requires separate range queries per sensor.

Boundaries adapt to data: this is typically handled via [[rebalancing-partitions#Strategy 2: Dynamic partitioning|dynamic partition splitting]].

## Hash partitioning

A hash function converts each key into a number, and partitions are assigned ranges of hash values. Even if input keys cluster together, a good hash function distributes outputs uniformly.

**Hash function selection**: The hash function need not be cryptographically strong. Cassandra and MongoDB use MD5; Voldemort uses Fowler–Noll–Vo. Language built-in hash functions (Java's `Object.hashCode()`, Ruby's `Object#hash`) are unsuitable — the same key can produce different values in different processes (source: chapter-06-partitioning.md).

**Advantages**:
- Distributes keys more evenly, reducing skew.
- Partition boundaries can be evenly spaced or pseudorandomly chosen.

**Disadvantages**:
- Destroys key ordering; range queries must be sent to all partitions (scatter/gather).
- MongoDB sends any range query to all partitions when hash sharding is enabled.
- Riak, Couchbase, and Voldemort do not support range queries on the primary key.

See [[consistent-hashing]] for the specific technique that uses random partition boundaries.

## Hybrid: compound key partitioning

Cassandra's approach blends both strategies. A table has a compound primary key; only the first column is hashed to determine the partition, while remaining columns define the sort order within the partition (stored in [[sstables-and-lsm-trees|SSTables]]).

This enables efficient lookups like: "all posts by user X within the last 30 days" — hash on `user_id` determines the partition, then range scan on `timestamp` within that partition. Sorting across users (across partitions) is not possible in one query.

## Choosing the right strategy

| Property | Key-range | Hash |
|---|---|---|
| Range queries | Efficient | Inefficient (scatter/gather) |
| Load distribution | Risk of hot spots | Uniform distribution |
| Partition management | Dynamic splitting | Fixed or proportional |

See [[hot-spots]] for application-level workarounds when hash partitioning still produces skew.

## Related pages

- [[partitioning]]
- [[hot-spots]]
- [[consistent-hashing]]
- [[rebalancing-partitions]]
- [[partitioning-secondary-indexes]]
- [[indexes]]
- [[sstables-and-lsm-trees]]
