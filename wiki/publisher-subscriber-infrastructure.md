# Publisher/Subscriber Infrastructure

**Summary**: The transport layer that wires together Burns's [[event-driven-batch-pattern|event-driven batch workflows]]. A pub/sub API lets a workflow define named **topics**, publish work items to them, and have downstream stages subscribe as consumers. Burns walks through Kafka-on-Kubernetes-via-Helm as the concrete substrate; cloud equivalents (Azure EventGrid, AWS SQS, Google Pub/Sub) are interchangeable at the pattern level.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## Why it matters

Burns opens the pub/sub section by considering what could go wrong if you built a workflow on a local filesystem — each stage writes items to a directory, next stage watches for new files (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). This works on one node but does not distribute; adding a network filesystem adds complexity to both code and deployment.

The pub/sub answer: "a popular approach to building a workflow like this is to use a publisher/subscriber (pub/sub) API or service. A pub/sub API allows a user to define a collection of queues (sometimes called topics). One or more publishers publishes messages to these queues. Likewise, one or more subscribers is listening to these queues for new messages" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

Each stage of the workflow becomes a publisher (to its output topic) and a subscriber (to its input topic). The broker handles durability, delivery, fan-out, and buffering.

## The topic-per-output-shard convention

Burns's convention: one topic per logical output stream of each stage (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). For a [[sharder-pattern|sharder]] with three shards on a `Photos` pipeline, you provision three topics:

- `photos-1`
- `photos-2`
- `photos-3`

The sharder module publishes each item to the topic selected by its sharding function; three downstream queue-managers each subscribe to one of the three topics. A [[copier-pattern|copier]] with N downstream targets publishes to N topics. A [[merger-pattern|merger]] subscribes to multiple topics.

This is the **topics-as-workflow-edges** convention that underlies the whole pattern: the graph of topics *is* the workflow diagram.

## Implementations

Burns lists the interchangeable options (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

| Implementation | Type | Notes |
|---|---|---|
| Apache Kafka | Open source, self-hostable | Burns's worked example; runs on Kubernetes via Helm |
| Azure EventGrid | Public-cloud managed | Azure's pub/sub API |
| Amazon SQS | Public-cloud managed | AWS's pub/sub API |

The patterns are "relatively simple to port to alternate pub/sub APIs" — the workflow shape is substrate-independent, the specific broker choice is an operational decision. See [[message-brokers]] and [[log-based-message-brokers]] for the DDIA-level treatment.

## Hands-on: Kafka on Kubernetes via Helm

Burns's walkthrough installs Kafka as a container workload using Helm, Kubernetes's package manager (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

```bash
helm init
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name kafka-service incubator/kafka
```

Burns notes the maturity caveat: `stable` Helm charts are more strictly vetted; `incubator` charts (where Kafka lived at the time of writing) "are more experimental and have less production mileage" but are useful for proofs of concept and as a starting point for production deployments (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

### Creating a topic

```bash
for x in 0 1 2; do
kubectl run kafka --image=solsson/kafka:0.11.0.0 --rm --attach --command -- \
  ./bin/kafka-topics.sh --create --zookeeper kafka-service-zookeeper:2181 \
  --replication-factor 3 --partitions 10 --topic photos-$x
done
```

Two Kafka parameters are load-bearing (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

- **`--replication-factor`** — "how many different machines messages in the topic will be replicated to. This is the redundancy that is available in case things crash. A value of 3 or 5 is recommended."
- **`--partitions`** — "represents the maximum distribution of the topic onto multiple machines for purposes of load balancing. In this case, since there are 10 partitions, there can be at most 10 different replicas of the topic for load balancing."

These correspond directly to DDIA's [[replication]] and [[partitioning]] concepts — Kafka's `replication-factor` is replication for durability, its `partitions` are the partitioning for throughput.

### Producing and consuming

Burns demonstrates the CLI producer and consumer:

```bash
# Producer
kubectl run kafka-producer --image=solsson/kafka:0.11.0.0 --rm -it --command -- \
  ./bin/kafka-console-producer.sh --broker-list kafka-service-kafka:9092 \
  --topic photos-1

# Consumer
kubectl run kafka-consumer --image=solsson/kafka:0.11.0.0 --rm -it --command -- \
  ./bin/kafka-console-consumer.sh --bootstrap-server kafka-service-kafka:9092 \
  --topic photos-1 \
  --from-beginning
```

In a real system, each stage of the workflow runs its own producer/consumer against the appropriate topics — using a proper Kafka SDK rather than the shell CLI (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). "But on the other hand, never underestimate the power of a good Bash script!"

## Relationship to the work-queue source interface

The pub/sub broker lives **beneath** the [[source-container-interface|source ambassador]] in Burns's stack. The downstream queue-manager still speaks the same `GET /api/v1/items` interface; the source ambassador on its side subscribes to the topic and returns the drained messages as its item list. The queue-manager never learns that Kafka is behind the ambassador. See the "brokers as a work-queue source" section in [[message-brokers]].

This is important: swapping pub/sub implementations (Kafka to EventGrid, for example) only changes the source ambassador container; the queue-manager, worker, and workflow graph are unchanged.

## Kafka's partition count as a load-balancing cap

Burns's note that "there can be at most 10 different replicas of the topic for load balancing" when `--partitions 10` is set ties the pub/sub substrate to the [[dynamic-worker-scaling|dynamic worker scaling]] math. The maximum parallelism of a single-topic consumer group is bounded by the topic's partition count; scaling the worker pool beyond that gives no additional throughput on that topic. Provision partitions generously up front — the partition count is hard to change later on most brokers.

## Relationship to DDIA stream infrastructure

This page is Burns's container-level framing of the infrastructure that [[event-streams]] and [[log-based-message-brokers]] cover at the DDIA layer. The vocabulary overlaps: Burns's "topic" is DDIA's topic; the partition/replication terminology is the same Kafka model described in both books. The difference is perspective — DDIA covers the semantics (delivery guarantees, offsets, replay); Burns covers the deployment (Helm chart, `kubectl run` commands, workflow-level conventions).

For ordering, delivery, and fault-tolerance semantics, see:

- [[log-based-message-brokers]] — the Kafka partition model and consumer offsets.
- [[event-streams]] — the broader event-stream vocabulary.
- [[stream-processing-fault-tolerance]] — exactly-once and checkpointing on top of streams.

## Related pages

- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[event-streams]]
- [[dynamic-worker-scaling]]
- [[replication]]
- [[partitioning]]
- [[designing-distributed-systems]]
