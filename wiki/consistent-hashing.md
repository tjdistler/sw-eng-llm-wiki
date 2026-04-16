# Consistent Hashing

**Summary**: A technique originally designed for distributing load across internet-wide caches (CDNs) by using randomly chosen partition boundaries, avoiding the need for central control or distributed consensus. In practice, the term is misleading in a database context and "hash partitioning" is preferred.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`

**Last updated**: 2026-04-15

---

## Origin and definition

Consistent hashing was defined by Karger et al. for evenly distributing load across a system of caches such as a content delivery network (CDN). The key idea is to use randomly chosen partition boundaries so that adding or removing a node only redistributes a small fraction of keys, without requiring central coordination or [[distributed-consensus|distributed consensus]].

The word "consistent" here has nothing to do with replica consistency (see [[eventual-consistency]]) or ACID consistency. It refers specifically to the property that most keys stay mapped to the same partition when the number of nodes changes.

## Why databases avoid the term

Although some database documentation still refers to "consistent hashing," the technique as originally defined does not work well for databases in practice (source: chapter-06-partitioning.md). The random partition boundaries can produce uneven data distribution, and the approach is rarely used as-is. Modern systems use fixed or dynamic partition counts with hash-based key assignment instead.

To avoid confusion, it is better to use the term **hash partitioning** when discussing database [[partitioning-strategies]].

## Relationship to rebalancing strategies

The "partitioning proportionally to nodes" strategy (used by Cassandra and Ketama) is the closest modern analogue to the original consistent hashing definition. New nodes randomly split a fixed number of existing partitions and take ownership of half of each split. This requires hash-based partitioning so boundaries can be drawn from the hash function's range. The randomization can produce unfair splits, but averaged over many partitions (Cassandra defaults to 256 per node), the result is reasonably fair. Cassandra 3.0 introduced an alternative rebalancing algorithm that avoids unfair splits (source: chapter-06-partitioning.md). Newer hash functions can achieve a similar effect with lower metadata overhead.

See [[rebalancing-partitions]] for details on how this compares to fixed and dynamic partition counts.

## Related pages

- [[partitioning-strategies]]
- [[partitioning]]
- [[rebalancing-partitions]]
- [[hot-spots]]
