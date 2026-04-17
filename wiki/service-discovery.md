# Service Discovery

**Summary**: The general problem of determining which network address and port to contact for a given service or resource, especially in systems with redundant machines where assignments change over time.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`

**Last updated**: 2026-04-15

---

## The problem

Any piece of software accessible over a network faces the service discovery problem: how does a client know which IP address and port number to connect to? This becomes especially difficult when the system aims for high availability by running on multiple machines, because the mapping of responsibilities to machines can change over time (source: chapter-06-partitioning.md).

In partitioned databases, [[request-routing]] is a specific instance of service discovery -- clients need to find the node that currently owns the partition for a given key. As [[rebalancing-partitions|rebalancing]] moves partitions between nodes, the assignment changes and all routing participants must stay current.

## Approaches

Service discovery solutions range from simple to sophisticated:

- **DNS**: sufficient for finding the initial set of node IP addresses, since these change far less frequently than partition-to-node assignments (source: chapter-06-partitioning.md).
- **Coordination services**: [[zookeeper]], etcd, and Consul provide dynamic, consensus-backed service registries where nodes register themselves and clients subscribe to changes.
- **Gossip protocols**: nodes disseminate cluster state changes among themselves (used by Cassandra and Riak), avoiding dependency on an external coordination service (source: chapter-06-partitioning.md).
- **In-house tools**: many companies have built proprietary service discovery systems, and several have been released as open source (source: chapter-06-partitioning.md).

## Container-level implementations

Burns frames service discovery as a container-composition concern too (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). A **service-broker ambassador** — a container coresident with the application that introspects the environment and brokers the right backend connection — is a practical way to deliver service discovery to an application without baking it into the application's code. See [[service-brokering]] for the pattern, and [[ambassador-pattern]] for the wider container pattern it sits inside. A fleet-wide generalization is the [[service-mesh]], where every pod's data-plane proxy performs service discovery for every outbound dependency.

## Related pages

- [[request-routing]]
- [[rebalancing-partitions]]
- [[zookeeper]]
- [[partitioning]]
- [[consensus]]
- [[ambassador-pattern]]
- [[service-brokering]]
- [[service-mesh]]
