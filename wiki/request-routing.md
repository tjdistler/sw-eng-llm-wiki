# Request Routing

**Summary**: Once data is partitioned across nodes, clients need a way to find the right node for a given key. Three approaches exist -- client-side routing, a dedicated routing tier, and node-forwarding -- each relying on some mechanism to track the ever-changing assignment of partitions to nodes.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## The problem

As [[rebalancing-partitions|rebalancing]] moves partitions between nodes, the mapping of partitions to IP addresses changes. Every component that routes requests must stay up to date with these changes. This is an instance of the general [[service-discovery]] problem, which applies to any software accessible over a network, especially systems aiming for high availability across redundant machines (source: chapter-06-partitioning.md).

## Three routing approaches

### 1. Contact any node (node-forwarding)

Clients send requests to any node (e.g., via a round-robin load balancer). If the contacted node owns the target partition, it handles the request directly. Otherwise, it forwards the request to the correct node, receives the reply, and returns it to the client.

**Used by**: Cassandra, Riak (via gossip protocol).

### 2. Routing tier

All client requests go to a partition-aware load balancer (a routing tier) that determines the correct node and forwards each request. The routing tier itself does not store data; it only maintains the partition-to-node mapping.

**Used by**: LinkedIn Espresso (via Helix/ZooKeeper), MongoDB (via mongos daemons and a config server), HBase, SolrCloud, Kafka.

Burns's [[sharded-service-pattern|sharded services]] use the term **root** for this component — a shard-aware load balancer in front of the shards. His Chapter 6 hands-on explicitly describes deploying twemproxy (or an nginx consistent-hashing proxy) as a **shared shard-routing service**: a [[replicated-load-balanced-service]] of routing processes fronted by a Kubernetes `Service` (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). The trade-off against the client-side-ambassador approach: a shared service means less per-client complexity but introduces an extra network hop and must itself be scaled as load grows. See [[sharded-service-pattern#Deployment variants: ambassador vs shared routing service]].

### 3. Client-side awareness

Clients themselves know the partitioning scheme and the partition-to-node assignment, and connect directly to the appropriate node with no intermediary.

A practical refinement of client-side awareness is to move the routing logic out of the client process and into a coresident ambassador container. Burns's [[client-side-sharding]] example uses a twemproxy ambassador in each client [[pod]]: the application opens a plain Redis connection to `localhost:6379`, and the ambassador hashes each key and picks the right shard using [[consistent-hashing|ketama]]. This keeps the client application code routing-agnostic while still avoiding a shared server-side routing tier. See [[ambassador-pattern]] (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

## Keeping routing information current

The central challenge is ensuring that all routing participants agree on partition assignments. Stale routing information means requests go to the wrong node.

### The agreement challenge

It is critical that all participants in routing agree on the current partition assignment -- otherwise requests go to the wrong node and are not handled correctly. There are protocols for achieving [[consensus]] in a distributed system, but they are hard to implement correctly (source: chapter-06-partitioning.md). Most systems therefore rely on a dedicated coordination service.

### ZooKeeper-based coordination

Many systems use a separate coordination service such as **ZooKeeper** to maintain the authoritative partition-to-node mapping. Each node registers itself in ZooKeeper. When partitions change ownership or nodes are added/removed, ZooKeeper notifies subscribers (the routing tier or partition-aware clients).

**Used by**: HBase, SolrCloud, Kafka, LinkedIn Espresso (via Helix, which uses ZooKeeper).

MongoDB uses a similar architecture but with its own config server implementation rather than ZooKeeper.

### Gossip protocol

Cassandra and Riak disseminate cluster state changes via a **gossip protocol** among nodes. Any node can route a request, forwarding it internally if needed. This avoids a dependency on an external coordination service but puts more complexity into the database nodes themselves.

### Static configuration

Couchbase does not rebalance automatically. Its routing tier (moxi) learns about routing changes directly from cluster nodes.

For finding the initial set of node IP addresses, DNS is typically sufficient since these change far less frequently than partition assignments.

## Parallel query execution

Simple key-value queries need routing to a single partition. But massively parallel processing (MPP) database products (used for [[data-warehousing|analytics]]) support complex queries with joins, filtering, grouping, and aggregation. The MPP query optimizer breaks such queries into execution stages that run in parallel across many nodes and partitions. This is a specialized topic covered in more depth in later chapters.

## Related pages

- [[partitioning]]
- [[rebalancing-partitions]]
- [[partitioning-strategies]]
- [[service-discovery]]
- [[zookeeper]]
- [[consensus]]
- [[fault-tolerance]]
- [[data-warehousing]]
- [[ambassador-pattern]]
- [[client-side-sharding]]
- [[sharded-service-pattern]]
- [[shard-key-selection]]
