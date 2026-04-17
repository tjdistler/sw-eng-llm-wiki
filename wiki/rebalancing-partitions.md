# Rebalancing Partitions

**Summary**: Rebalancing is the process of moving data and request load from one node to another as the cluster grows, shrinks, or recovers from failures. The three main strategies -- fixed partition count, dynamic splitting, and proportional to nodes -- each handle differently the tension between operational simplicity and adapting to changing data volumes.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## Why rebalancing is needed

Over time a database cluster changes: query throughput grows (need more CPUs), dataset size grows (need more disks and RAM), or a machine fails and its responsibilities must shift to surviving nodes. All of these require moving load between nodes.

## Requirements

Any rebalancing approach should satisfy three properties:

1. **Fair load distribution**: after rebalancing, data and request load should be shared evenly across nodes.
2. **Availability during rebalancing**: the database should continue serving reads and writes while data moves.
3. **Minimal data movement**: only move what is necessary, to limit network and disk I/O.

## Anti-pattern: hash mod N

Using `hash(key) mod N` to assign keys to N nodes is tempting but dangerous. When N changes, most keys must move. For example, a key with hash 123456 goes to node 6 with 10 nodes, node 3 with 11 nodes, and node 0 with 12 nodes. This makes rebalancing excessively expensive.

## Strategy 1: Fixed number of partitions

Create many more partitions than nodes at the outset (e.g., 1,000 partitions for 10 nodes). Each node owns roughly 100 partitions. When a node joins, it steals partitions from existing nodes; when a node leaves, its partitions are redistributed. Only whole partitions move -- the mapping of keys to partitions never changes, only the mapping of partitions to nodes.

Stronger hardware can be assigned more partitions to take a larger share of load.

**Used by**: Riak, Elasticsearch, Couchbase, Voldemort.

**Trade-off**: the partition count is fixed at setup time and acts as the ceiling for node count. Choosing too few limits future growth; choosing too many adds management overhead. If the dataset size varies widely, partition sizes may become too large (expensive rebalancing and recovery) or too small (excessive overhead).

## Strategy 2: Dynamic partitioning

When a partition exceeds a configured size threshold (e.g., 10 GB in HBase), it splits into two halves. When a partition shrinks below a threshold, it merges with an adjacent partition. This resembles the splitting behavior of [[b-trees]].

After a split, one half can transfer to another node to balance load. The partition count adapts to total data volume automatically.

**Caveat**: an empty database starts with a single partition, so all writes initially go to one node. HBase and MongoDB mitigate this with **pre-splitting** -- configuring initial partition boundaries on an empty database, which requires knowing the key distribution in advance.

Dynamic partitioning works for both key-range and hash-partitioned data. MongoDB (since version 2.4) supports dynamic splitting for both modes.

**Used by**: HBase, RethinkDB, MongoDB.

## Strategy 3: Proportional to nodes

The number of partitions is proportional to the number of nodes, with a fixed number of partitions per node (e.g., Cassandra defaults to 256 per node). When a new node joins, it randomly splits a fixed number of existing partitions and takes one half of each.

The randomization can produce unfair splits, but when averaged over a larger number of partitions (Cassandra defaults to 256 per node), the new node ends up taking a fair share of load. Cassandra (since 3.0) uses an alternative rebalancing algorithm that avoids unfair splits (source: chapter-06-partitioning.md).

Partition size stays roughly stable as the cluster grows because adding nodes also adds partitions. This approach requires hash-based [[partitioning-strategies]] so that boundaries can be drawn from the hash range. It is the closest modern analogue to [[consistent-hashing]]. Newer hash functions can achieve a similar effect with lower metadata overhead.

**Used by**: Cassandra, Ketama.

## Rebalancing at the service layer

The same anti-pattern and strategies recur in the design of [[sharded-service-pattern|sharded services]] like caches. Burns's Chapter 6 of *Designing Distributed Systems* makes the point concretely (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- **Naive `hash % N` in a sharded cache.** Scaling from 10 to 11 shards changes most key-to-shard mappings and "in the worst case, rolling out a new sharding function for your sharded cache will be equivalent to a complete cache failure."
- **[[consistent-hashing|Consistent hashing]] is the default.** A consistent-hashing sharding function remaps only ~`K/N` keys when scaling from `N-1` to `N` shards. This is what makes ketama the default in memcached / Redis sharding ambassadors.
- **Per-shard replication changes what "rebalancing" means.** In a [[replicated-sharded-service]], response to traffic shifts is to add replicas to hot shards and remove them from cold shards — not to change the sharding function at all. See [[hot-sharding]] for this operational pattern.

In DDIA's vocabulary, Burns's hot-sharding pattern resembles the fixed-partition-count strategy: the *number* of partitions (shards) does not change; only the mapping of partitions to machines and the per-partition replica count does. Burns does not explicitly consider dynamic splitting of sharded cache partitions, which is unusual in caches because cache working-set size is self-limiting via eviction.

## Automatic vs. manual rebalancing

Fully automatic rebalancing reduces operational burden but carries risk. If combined with automatic failure detection, a temporarily slow node may be declared dead, triggering rebalancing that adds further load to an already stressed cluster -- potentially causing a cascading failure.

Many systems take a middle path: the database proposes a partition assignment, but an administrator must approve before it takes effect (Couchbase, Riak, Voldemort). Having a human in the loop is slower but prevents operational surprises.

## Comparison

| Property | Fixed count | Dynamic | Proportional to nodes |
|---|---|---|---|
| Partition count changes? | No | Yes (split/merge) | Yes (with node count) |
| Adapts to data volume? | No | Yes | Indirectly |
| Initial config required? | Partition count | Pre-splitting recommended | Partitions per node |
| Used by | Riak, Elasticsearch, Couchbase | HBase, RethinkDB, MongoDB | Cassandra, Ketama |

## Related pages

- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[hot-spots]]
- [[b-trees]]
- [[request-routing]]
- [[fault-tolerance]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
