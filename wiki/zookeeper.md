# ZooKeeper

**Summary**: A coordination service (along with etcd and Consul) that provides [[consensus]]-based primitives -- linearizable atomic operations, [[total-order-broadcast]], failure detection, and change notifications -- enabling distributed systems to outsource leader election, locking, and membership management.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`, `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What it is

ZooKeeper (and etcd, Consul) is often described as a "distributed key-value store," but it is fundamentally a coordination service built on [[consensus]] algorithms. It holds small amounts of data that fit entirely in memory (replicated to disk for durability), using fault-tolerant [[total-order-broadcast]] to keep replicas consistent. (source: designing-data-intensive-applications, chapter 9)

ZooKeeper is modeled after Google's Chubby lock service. Zab is ZooKeeper's consensus algorithm; etcd uses Raft. (source: designing-data-intensive-applications, chapter 9)

## Key features

**Linearizable atomic operations**: compare-and-set operations that are atomic and [[linearizability|linearizable]] even under node failures or network interruptions. Used to implement distributed locks (typically as leases with expiry times). (source: designing-data-intensive-applications, chapter 9)

Note: strictly speaking, ZooKeeper provides linearizable writes, but reads may be stale by default (served by any replica). Linearizable reads require calling sync() before reading. etcd calls this a quorum read. (source: designing-data-intensive-applications, chapter 9)

**Total ordering of operations**: every operation gets a monotonically increasing transaction ID (zxid) and version number (cversion), providing fencing tokens for lock safety. (source: designing-data-intensive-applications, chapter 9)

**Failure detection**: clients maintain long-lived sessions with periodic heartbeats. If heartbeats stop for longer than the session timeout, ZooKeeper declares the session dead. Locks held by dead sessions can be automatically released via **ephemeral nodes**. (source: designing-data-intensive-applications, chapter 9)

**Change notifications (watches)**: clients can subscribe to changes on keys, avoiding the need to poll. This enables detecting when other clients join, leave, or fail. (source: designing-data-intensive-applications, chapter 9)

## Common use patterns

**Leader election**: multiple instances compete to acquire a lock; the winner becomes the leader. If the leader fails, its session times out, the ephemeral node disappears, and another instance acquires the lock. (source: designing-data-intensive-applications, chapter 9)

**Work allocation and partition assignment**: deciding which partition to assign to which node, rebalancing when nodes join or leave. Achievable through atomic operations, ephemeral nodes, and notifications. (source: designing-data-intensive-applications, chapter 9)

**Service discovery**: services register their network endpoints on startup. Other services look them up via ZooKeeper/etcd/Consul. Note: service discovery itself does not require consensus (DNS works fine without it), but leader election does -- and if the consensus system already knows the leader, it makes sense to publish that information for discovery. (source: designing-data-intensive-applications, chapter 9)

**Membership services**: determining which nodes are currently active members of a cluster. Combined with failure detection and consensus, nodes can agree on membership even though failure detection alone is unreliable due to unbounded network delays. (source: designing-data-intensive-applications, chapter 9)

## Architecture

ZooKeeper runs on a fixed number of nodes (typically 3 or 5) performing majority votes among themselves, while supporting a potentially large number of clients. This avoids the impracticality of majority votes over thousands of application nodes. (source: designing-data-intensive-applications, chapter 9)

Some consensus systems support **read-only caching replicas** that asynchronously receive the decision log but do not participate in voting, enabling non-linearizable reads at scale. (source: designing-data-intensive-applications, chapter 9)

## Partition-to-node tracking

In partitioned databases, ZooKeeper serves as the authoritative source of the partition-to-node mapping for [[request-routing]]. Each database node registers itself in ZooKeeper, and ZooKeeper maintains the mapping of partitions to nodes. Routing tiers or partition-aware clients subscribe to this information. When a partition changes ownership or a node is added or removed, ZooKeeper notifies subscribers so routing information stays current. Systems using this pattern include HBase, SolrCloud, Kafka, and LinkedIn's Espresso (via Helix). MongoDB uses a similar architecture with its own config server implementation rather than ZooKeeper (source: chapter-06-partitioning.md).

## Container-level perspective (Burns)

Burns's *Designing Distributed Systems* treats ZooKeeper, etcd, and Consul as interchangeable consensus-backed KV stores at the pattern level — "a large number of distributed key-value stores that have implemented such consensus algorithms for you" — and explicitly discourages implementing Paxos or Raft yourself: "akin to implementing locks on top of assembly code compare-and-swap instructions." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

His chapter's hands-on walkthroughs use etcd (because it is Kubernetes-native) and the CoreOS etcd [[operator-pattern|operator]] via Helm. The lock/lease construction he derives from first principles — compare-and-swap + TTL + resource version — is structurally identical to what ZooKeeper provides via ephemeral nodes + zxid/cversion, just mapped onto etcd's API. See [[distributed-locks-on-kv-stores]] for the applied construction and [[ownership-election-pattern]] for the full container-level pattern.

## Google's Chubby: the ancestor

[[chubby|Chubby]] is Google's internal lock service, and ZooKeeper is modelled directly after it (source: site-reliability-engineering, chapter 2). Chubby provides a filesystem-like API for locks across datacenter locations, uses Paxos for asynchronous [[consensus]], and is the canonical home for "data that must be consistent" inside Google — [[bns|BNS]] stores its name-to-address mappings in Chubby, for example. The lock-plus-consistent-KV fusion is exactly the ZooKeeper/etcd shape, with Paxos/Zab/Raft as the three consensus algorithms in the family.

## Consensus-as-a-service (SRE Chapter 23)

Laura Nolan's Chapter 23 framing ties ZooKeeper's prominence to a specific architectural choice: "providing consensus primitives as a service rather than as libraries that engineers build into their applications frees application maintainers of having to deploy their systems in a way compatible with a highly available consensus service (running the right number of replicas, dealing with group membership, dealing with performance, etc.)" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is why Nolan treats ZooKeeper, etcd, and Consul as first-class citizens of the chapter and names ZooKeeper as "the first open source consensus system to gain traction in the industry because it was easy to use, even with applications that weren't designed to use distributed consensus." Chubby fills the same niche inside Google, and the ZooKeeper/etcd/Chubby family all expose the same shape of higher-level abstraction on top of their respective consensus protocols.

Chapter 23 places ZooKeeper as a packaged [[replicated-state-machine]] whose API surface is a [[reliable-replicated-datastore]] plus coordination primitives ([[distributed-barrier|barriers]], locks, [[consensus-coordination-failures|leader election]]). See [[managing-critical-state]] for the chapter's framing of why this packaging is the right answer for almost every team.

## Higher-level tools

Libraries like Apache Curator provide higher-level recipes on top of the ZooKeeper client API. Projects that depend on ZooKeeper include HBase, Hadoop YARN, OpenStack Nova, and Kafka. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[consensus]]
- [[total-order-broadcast]]
- [[linearizability]]
- [[leader-based-replication]]
- [[failover]]
- [[fault-tolerance]]
- [[distributed-transactions]]
- [[request-routing]]
- [[partitioning]]
- [[ownership-election-pattern]]
- [[distributed-locks-on-kv-stores]]
- [[renewable-leases]]
- [[operator-pattern]]
- [[chubby]]
- [[managing-critical-state]]
- [[replicated-state-machine]]
- [[reliable-replicated-datastore]]
- [[paxos]]
- [[multi-paxos]]
