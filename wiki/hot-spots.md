# Hot Spots

**Summary**: A hot spot is a partition that receives a disproportionate share of reads or writes, undermining the scalability benefits of partitioning and making the overloaded node a bottleneck.

**Sources**: raw/designing-data-intensive-applications/chapter-06-partitioning.md, raw/designing-distributed-systems/chapter-06-sharded-services.md

**Last updated**: 2026-04-16

---

## What is skew

When partitioning is unfair — some partitions receiving more data or queries than others — the distribution is *skewed*. A partition with disproportionately high load is called a *hot spot*. In an extreme case, all load concentrates on one partition and the other nodes in the cluster are idle.

## Causes of hot spots

### Key-range partitioning with sequential keys

If the partition key is a monotonically increasing value (e.g., a timestamp), every new write goes to the latest partition. Other partitions receive no writes. This is a structural problem with key-range [[partitioning-strategies]].

*Example*: A sensor network writing measurements keyed by `year-month-day-hour-minute-second` will funnel all writes to the "today" partition.

*Mitigation*: Prefix the key with a higher-cardinality dimension (e.g., `sensor_name + timestamp`). Writes now spread across partitions, but multi-sensor range queries require one query per sensor.

### Hash partitioning with a single dominant key

Hash partitioning distributes keys uniformly, but cannot help when many requests target the *same* key. If two requests hash to the same value, they still land on the same partition.

*Example*: On a social media platform, a celebrity with millions of followers triggers massive write volume to a single user ID. Hashing `user_id` doesn't help — the hash of the same value is always the same.

## Application-level mitigation for extreme hot spots

Most databases today cannot automatically compensate for highly skewed workloads. The application must manage this.

**Write-side key splitting**: Add a small random suffix (e.g., a 2-digit decimal number) to a known hot key. This distributes writes across 100 distinct keys, which can land on different partitions.

**Read-side cost**: Any read for that logical key must now query all 100 keys and combine results. The application must track which keys have been split.

**Overhead**: Key splitting only makes sense for a small number of identified hot keys; applying it broadly adds unnecessary overhead. The split/unsplit status of keys requires bookkeeping.

This is an application-level trade-off with no clean general solution. Future database systems may detect and rebalance hot keys automatically (source: chapter-06-partitioning.md).

## Service-level mitigation: hot sharding

At the service layer, hot spots appear as "hot shards" — one shard of a [[sharded-service-pattern|sharded service]] receiving disproportionate traffic. Burns's response is to deploy each shard as a [[replicated-sharded-service|replicated sub-service]] and autoscale replica count per shard in response to load (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). When a viral photo drives massive traffic to its shard, the shard is replicated onto additional machines; cold shards can be packed onto fewer machines to free capacity. The shard count and sharding function stay constant — only per-shard replica count changes — so there is no re-sharding and no cache invalidation. See [[hot-sharding]] for the full pattern.

This service-level response complements the write-side key-splitting described above: key-splitting is an application-level workaround when you cannot change the serving topology; hot sharding is a deployment-level response that keeps the sharding function untouched. Key-splitting works for write-heavy database hot keys; hot sharding works for read-heavy cache / serving hot keys.

## Structural mitigation via compound keys

Cassandra's compound primary key approach can help avoid hot spots structurally. By hashing the first column of the key to determine the partition while using remaining columns for sort order within the partition, one-to-many relationships are spread across partitions by their parent key while remaining efficiently queryable within a partition. For example, a social media site can key updates as `(user_id, update_timestamp)` -- writes for different users go to different partitions, and within each user's partition, updates are sorted by time. See [[partitioning-strategies#Hybrid compound key partitioning]] for details (source: chapter-06-partitioning.md).

## Related pages

- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[rebalancing-partitions]]
- [[scalability]]
- [[hot-sharding]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
