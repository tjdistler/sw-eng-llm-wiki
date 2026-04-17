# Copartitioning

**Summary**: Two event streams are **copartitioned** when they share the same partition count **and** the same partitioner algorithm **and** are keyed the same way — so that events with a given key are colocated across streams. Copartitioning is the prerequisite for most stateful stream operations, including [[stream-joins]].

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## Definition

Copartitioning is the [[repartitioning]] of an event stream into a new one with the same partition count and partition assignor logic as another stream (source: chapter-05-event-driven-processing-basics.md). The result: for any key `k`, events for `k` on stream A and events for `k` on stream B both land on the same partition index. A single consumer instance owning that partition sees both sides of `k`'s history.

## Why it matters

Many stateful operations — most notably [[stream-joins]] — require that all events for a given key, regardless of which stream they come from, be processed through the **same node**. Without copartitioning, joining stream A's events for `user_42` against stream B's events for `user_42` would require cross-instance coordination, which defeats the parallelism benefits of partitioning (source: chapter-05-event-driven-processing-basics.md).

## Example: joining user events with user entities

Bellemare's worked example: a user-action stream has been [[repartitioning|repartitioned]] on `user_id`, and the service now needs to join it against a user-entity stream keyed on the same `user_id`. Both streams have the same partition count and the same partitioner, so partition `P0` of the action stream and partition `P0` of the entity stream contain the same set of users. A single consumer instance is assigned both partitions and performs the join locally (source: chapter-05-event-driven-processing-basics.md).

## Partition-assignor responsibility

The [[partition-assignor]] is responsible for ensuring that partitions marked as copartitioned are assigned to the **same** consumer instance. Any instance handling copartitioned streams must be assigned the same partition index across all of them. Bellemare's guidance: have the assignor verify equal partition counts across copartitioned streams and throw an exception on inequality — it is the one invariant the assignor can cheaply check (source: chapter-05-event-driven-processing-basics.md).

## The three requirements

For streams to be copartitioned they must share:

1. **The same key** — events that should be colocated must be keyed on the same field.
2. **The same partitioner** — the hash/routing function must be identical.
3. **The same partition count** — otherwise the same key's hash modulo-N will land on different partition indices.

Violating any of these breaks data locality silently: events look "partitioned correctly" but are actually scattered across consumer instances.

## Related pages

- [[repartitioning]]
- [[partition-assignor]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[stream-joins]]
- [[consumer-group]]
- [[data-locality]]
- [[stateless-stream-processing]]
- [[microservice-topology]]
