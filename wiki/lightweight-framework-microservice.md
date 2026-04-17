# Lightweight Framework Microservice

**Summary**: An [[event-driven-microservices|EDM]] built with an **embedded stream-processing library** — Kafka Streams, or Apache Samza in embedded mode — that ships as an ordinary JVM application and leans on the [[event-broker|broker]] plus the [[container-management-system|CMS]] for everything a [[heavyweight-framework-microservice|heavyweight framework]] would otherwise run in a dedicated cluster. No extra master or worker nodes, no cluster-level resource allocation, no external shuffle service. Parallelism is just [[consumer-group]] membership; durability is just [[changelog-stream|changelogs]] in the broker; scaling and recovery are just the CMS adding and removing instances (source: chapter-12-lightweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-12-lightweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## What "lightweight" means

Lightweight frameworks provide the same stream-processing features as heavyweight frameworks — topologies, materialized tables, primary-key and foreign-key joins, aggregations, windowing — but with a very different runtime posture (source: chapter-12-lightweight-framework-microservices.md):

- **No dedicated cluster.** There is no Spark master, no Flink JobManager, no worker pool. The library runs *inside* the application process.
- **No framework-specific resource manager.** The CMS (Kubernetes et al.) schedules instances like any other microservice.
- **No external shuffle service.** The broker itself is the shuffle medium — see [[broker-as-shuffle-service]].
- **No checkpoint storage separate from the broker.** State durability is [[changelog-stream|changelogs]] in the broker, not HDFS/S3 snapshots. Contrast [[checkpointing-stream-processing]].

Applications are deployed as individual microservices, just like any [[basic-producer-consumer-microservice|BPC]] service. Parallelism is controlled by consumer-group membership and partition ownership. When instances join or leave, partitions are redistributed — including [[copartitioning|copartitioned]] assignments — by the [[partition-assignor]] (source: chapter-12-lightweight-framework-microservices.md).

## Lightweight processing

The processing model itself closely mirrors the heavyweight model. Each instance processes events according to the topology, and the broker provides the inter-instance communication layer for anything that exceeds a single instance (source: chapter-12-lightweight-framework-microservices.md):

- Data of the same key must be local to one instance for key-based operations (join, `groupByKey` + `reduce`/`aggregate`).
- Shuffles send events through an **internal event stream** (a broker topic), one event of a given key per partition — see [[repartitioning]] and [[copartitioning]].
- There is no direct instance-to-instance communication. The broker carries everything.

Contrast with the heavyweight model, where shuffles coordinate directly between worker nodes. The lightweight model's deeper broker integration is what lets it fit modern microservice deployment conventions cleanly.

## State and changelogs

Internal state backed by [[changelog-stream|changelogs]] is the default. Every state mutation is mirrored to a compacted broker topic; on scale-up or failure, a new instance rebuilds from the changelog before processing new input (source: chapter-12-lightweight-framework-microservices.md).

Because each lightweight application is fully independent:

- One service can request high-performance local SSD; another can request large, slower HDDs. Different storage engines can be plugged in — graph databases, document stores — while still keeping the broker as the durability backbone.
- An [[external-state-store]] remains available when the query model demands it, but the default is an [[internal-state-store]] (typically RocksDB).

This is the lightweight analogue of [[checkpointing-stream-processing]] — same problem (restart-safe internal state), different substrate (broker-hosted changelog instead of HDFS/object-storage snapshot).

## Scaling and failure recovery

Scaling and recovery are the **same process** in the lightweight model: instances joining (scale-up or replacement) acquire partitions and rebuild state; instances leaving (scale-down or failure) release partitions that will be picked up by survivors (source: chapter-12-lightweight-framework-microservices.md).

The sequence for adding an instance:

1. New instance starts, joins the [[consumer-group]].
2. The [[partition-assignor]] rebalances, including any internal (shuffle) streams.
3. The new instance pauses while state is rematerialized from the changelog — the **state restoration phase**. Processing of any event before state is fully restored would risk nondeterministic results.
4. Once each state store is fully restored, consumption of input *and* internal streams resumes.

Dynamic scaling under load is supported without restart — the only delay is rebalance plus state rematerialization. See [[stream-processing-scaling-strategies]] for how this compares with heavyweight "scale while running" and "scale by restart."

### Event shuffling

Event shuffling is simple: events are repartitioned into an internal event stream for downstream consumption. The internal stream **isolates upstream producers from downstream consumers** — the exact role of the [[external-shuffle-service]] in heavyweight frameworks, now played by the broker itself. Dynamic scaling only needs to reassign the downstream consumers; the producers are irrelevant (source: chapter-12-lightweight-framework-microservices.md). See [[broker-as-shuffle-service]].

### State assignment

Upon rebalance, an instance with a new partition must load the partition's state from the changelog before processing new events. Operator state — `<partitionId, offset>` for every input and internal stream — is tracked via the consumer group. Keyed state — `<key, state>` — is tracked in each state store's changelog. Both must be current before processing resumes (source: chapter-12-lightweight-framework-microservices.md).

### Hot replicas

[[hot-replicas]] work the same way they do for any stateful internal-state service: each partition is materialized on N > 1 instances, with one as leader and the rest tailing the changelog. On leader failure a replica is promoted with no rebuild delay (source: chapter-12-lightweight-framework-microservices.md).

Chapter 12 highlights a **second use** specific to lightweight frameworks: hot replicas can also seamlessly *scale up* the instance count without the usual rematerialization pause. The workflow under development for Kafka Streams:

1. Pre-populate a replica of the state on the new instance.
2. Wait until it has caught up to the head of the changelog.
3. Then rebalance to assign it ownership of the input partitions.

This reduces outages due to changelog rematerialization to near zero in exchange for the extra bandwidth of the pre-warm (source: chapter-12-lightweight-framework-microservices.md).

## The two current options

Both available lightweight options require Apache Kafka as the broker (source: chapter-12-lightweight-framework-microservices.md):

- **Kafka Streams.** The canonical lightweight framework. Feature-rich embedded library; deep integration with the Kafka cluster; JVM-only. Supports primary-key *and* foreign-key table-table joins. KSQL (Confluent community license) provides a SQL dialect on top.
- **Apache Samza: embedded mode.** Predates Kafka Streams but originally deployed against a heavyweight cluster. Embedded mode mirrors Kafka Streams' lifecycle. Uses Zookeeper by default for cross-instance coordination; other coordinators (e.g. Kubernetes) are possible. Offers a limited SQL-like language out of the box for simple stateless queries. Samza's embedded mode may not provide all of the functionality of its cluster mode (source: chapter-12-lightweight-framework-microservices.md).

Both are Java-based; high-level APIs are MapReduce-style chained operators, familiar to anyone who has used a heavyweight framework or functional programming.

Both expose **indefinitely retained materialized streams** in their high-level APIs — which is what unlocks primary-key joins, foreign-key joins, and the broader handling of relational data without the cognitive overhead of external state stores.

## Limitations

Bellemare's warning (source: chapter-12-lightweight-framework-microservices.md): lightweight frameworks are not as common as heavyweight frameworks or the [[basic-producer-consumer-microservice|basic producer/consumer pattern]]. They depend heavily on broker integration, which limits portability across broker technologies (both current options require Kafka). The domain is still young and evolving.

## How lightweight fits the EDM family

| Implementation style | Cluster? | Durability | Shuffle | Chapter |
|---|---|---|---|---|
| [[basic-producer-consumer-microservice\|BPC]] | No | Manual/external store | N/A (mostly stateless) | 10 |
| [[functions-as-a-service\|FaaS]] | Managed runtime | External store | N/A | 9 |
| **Lightweight framework** | **No — CMS + broker** | **Changelog (broker)** | **Internal topic (broker)** | **12** |
| [[heavyweight-framework-microservice\|Heavyweight framework]] | Yes — dedicated | Checkpoint (HDFS/S3/etc.) | [[external-shuffle-service\|ESS]] or equivalent | 11 |

The recurring axis: how much of the state, coordination, shuffling, scaling, and recovery work is done by the framework versus by the [[event-broker|broker]] plus [[container-management-system|CMS]] plus your own code. Lightweight sits squarely in the broker+CMS quadrant — the framework is just a library.

## When to choose lightweight

Good fit (source: chapter-12-lightweight-framework-microservices.md):

- You are building long-running, independent, stateful microservices.
- Your organization already runs Kafka at the scale the service needs.
- You want MapReduce-style stream-table and table-table joins without standing up a separate streaming cluster.
- You want the deployment lifecycle, scaling, and observability of an ordinary CMS-managed microservice — no framework-specific submission APIs.
- JVM is acceptable.

Reach elsewhere:

- Non-JVM languages required → [[basic-producer-consumer-microservice|BPC]] (or FaaS).
- Very large pre-existing analytics stack on Spark/Flink → [[heavyweight-framework-microservice|heavyweight framework]].
- Simple stateless transforms only → BPC is cheaper.
- Broker is not Kafka → the current lightweight options don't apply.

## Example: stream-table-table join

Chapter 12's worked example is a stream-table-table enrichment pattern implemented in Kafka Streams — aggregating ad-conversion events and joining them against a materialized advertisement-entity table for billing. It composes [[repartitioning]], `groupByKey` + `aggregate`, and a full-outer join, with copartitioning handled automatically by the topology. See [[stream-table-table-join]].

## Related pages

- [[event-driven-microservices]]
- [[heavyweight-framework-microservice]]
- [[basic-producer-consumer-microservice]]
- [[functions-as-a-service]]
- [[broker-as-shuffle-service]]
- [[stream-table-table-join]]
- [[changelog-stream]]
- [[internal-state-store]]
- [[external-state-store]]
- [[global-state-store]]
- [[hot-replicas]]
- [[stateful-stream-processing]]
- [[stream-processing-scaling-strategies]]
- [[checkpointing-stream-processing]]
- [[consumer-group]]
- [[partition-assignor]]
- [[repartitioning]]
- [[copartitioning]]
- [[stream-joins]]
- [[event-broker]]
- [[container-management-system]]
- [[microservice-topology]]
