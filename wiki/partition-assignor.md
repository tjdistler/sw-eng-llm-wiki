# Partition Assignor

**Summary**: The component responsible for distributing stream partitions across the consumer instances of a [[consumer-group]], rebalancing those assignments when membership changes, and honoring [[copartitioning]] constraints. It may live in the consumer client (Kafka) or in the broker (Pulsar).

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## Where the assignor lives

Different [[event-broker|brokers]] place the assignor differently (source: chapter-05-event-driven-processing-basics.md):

- **Apache Kafka** — delegates partition assignment to the first online client for each consumer group. That instance becomes the **consumer-group leader** and performs assignor duties whenever membership changes.
- **Apache Pulsar** — maintains centralized ownership of partition assignment inside the broker itself.

In both cases the identification mechanism — the [[consumer-group]] name — is the same; only who computes the assignment differs.

## Bringing instances online

The first instance to register with the broker using the group's name is assigned some partitions and begins consuming from each partition's last committed [[consumer-offset|offset]]. When a new instance joins, assignments are recomputed; when an instance leaves (clean shutdown or failure), its partitions are redistributed to the survivors. Work is typically **suspended briefly during reassignment** to avoid race conditions where two instances think they own the same partition — preventing duplicate output (source: chapter-05-event-driven-processing-basics.md).

## Copartitioning constraints

The assignor must honor [[copartitioning]] requirements: partitions marked as copartitioned must be assigned to the **same** single consumer instance, so that keyed events from all copartitioned streams arrive at the same node. Bellemare recommends the assignor verify that copartitioned streams have equal partition counts and fail loudly if they do not (source: chapter-05-event-driven-processing-basics.md).

## Assignment strategies

The goal of any assignment algorithm is to distribute partitions **evenly** across instances of equal capacity. Secondary goals may include minimizing the number of partitions moved during a rebalance — particularly important when materialized state is sharded across instances, because a reassignment can misdirect future updates (source: chapter-05-event-driven-processing-basics.md).

Bellemare names three common strategies (source: chapter-05-event-driven-processing-basics.md):

### Round-robin assignment

All partitions are tallied into a list and assigned in round-robin fashion to each consumer. A separate list is kept per copartitioned group so colocation constraints hold. When instances are added, partitions rebalance outward to the newcomers; adding more instances than partitions yields no additional parallelism — the excess instances sit idle, matching the [[consumer-group|consumer-group parallelism ceiling]].

### Static assignment

Specific partitions are assigned to specific consumers. This is most useful when instances hold **large materialized state** (internal state stores) and reassigning a partition would require moving or rebuilding that state. Under static assignment, a departed consumer's partitions are held open for its return, rather than reassigned immediately. Implementations may fall back to dynamic reassignment if the consumer fails to return within a grace period.

### Custom assignment

External signals drive the assignment decision — for example, balancing based on **input-stream lag** so busy partitions land on less-loaded instances. This is the escape hatch for workloads that the default strategies handle poorly.

## Relationship to rebalancing at the storage layer

The assignor's role in a consumer group parallels — but is not the same as — [[rebalancing-partitions|partition rebalancing]] in a database. The database case redistributes *data*; the streaming case redistributes *consumption rights* over a fixed partitioning scheme. The same concerns (evenness, minimal movement, availability) nonetheless recur at both layers.

## Related pages

- [[consumer-group]]
- [[consumer-offset]]
- [[copartitioning]]
- [[repartitioning]]
- [[event-broker]]
- [[log-based-message-brokers]]
- [[partitioning]]
- [[rebalancing-partitions]]
- [[stateless-stream-processing]]
