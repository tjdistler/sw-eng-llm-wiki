# Consumer Group

**Summary**: A set of consumer instances that are treated by the [[event-broker]] as a **single logical consumer**, with stream [[partitioning|partitions]] dynamically assigned across the instances so each partition is consumed by exactly one member at a time. Consumer groups are the primary mechanism for **horizontally scaling** event consumption while preserving per-partition ordering.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## What a consumer group is

A consumer group allows multiple consumer instances to be treated as the same logical entity — all events are delivered to the group as a whole, with the broker distributing partitions across the group's members (source: chapter-02-event-driven-microservice-fundamentals.md).

Three rules follow from this model (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Each partition is assigned to exactly one consumer** in the group at any time.
- **Each consumer in the group may be assigned one or more partitions.**
- **Every event for a given partition is processed by only one instance** of the group — preserving per-partition ordering.

## Rebalancing

When a new consumer joins the group, the broker redistributes partition assignments — the newcomer picks up some partitions, and older members relinquish them. Conversely, when a consumer leaves (cleanly or via failure), its partitions are reassigned to the remaining members (source: chapter-02-event-driven-microservice-fundamentals.md).

This rebalancing is what makes consumer groups **elastic**: you can add instances to increase throughput and remove them when load drops, and the broker handles the reassignment.

The actual distribution policy is the job of a [[partition-assignor]] — round-robin, static, or custom. In Kafka the assignor runs inside the first-online client (the group leader); in Pulsar the broker owns assignment. Work is briefly suspended during reassignment to avoid two instances claiming the same partition simultaneously, preventing duplicate output (source: chapter-05-event-driven-processing-basics.md). The assignor is also responsible for honoring [[copartitioning]] constraints — partitions marked copartitioned must land on the same instance.

## The parallelism ceiling

Because a partition cannot be split across multiple consumers in the same group, the **number of active consumer instances in a group is capped at the number of partitions** in the stream (source: chapter-02-event-driven-microservice-fundamentals.md). Extra consumers beyond the partition count sit idle.

Designing stream partition counts is therefore a forward-looking capacity decision — set the count high enough to accommodate future scaling, because changing it later generally requires stream rewrite.

## Multiple groups, same stream

Different consumer groups can each consume the same stream independently. Each group has its own [[consumer-offset|offsets]] and its own assignment of partitions, so a marketing-analytics group and a fulfilment group can both see every event without interfering with each other. This is the mechanism that makes an [[event-broker]] a broadcast medium — as many groups as you like, each with its own fan-in model.

## Relationship to the wiki's existing coverage

- **[[log-based-message-brokers]]** — already mentions that "at most one consumer per partition" and explains the per-partition load-balancing model; this page is the concept-level companion.
- **[[consumer-offset]]** — the mechanism used to track progress within each group.
- **[[event-broker]]** — the system that implements group membership and rebalancing.

## Related pages

- [[event-broker]]
- [[consumer-offset]]
- [[log-based-message-brokers]]
- [[event-streams]]
- [[partitioning]]
- [[partition-assignor]]
- [[copartitioning]]
- [[repartitioning]]
- [[event-driven-microservices]]
