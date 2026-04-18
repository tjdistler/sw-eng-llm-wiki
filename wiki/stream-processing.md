# Stream Processing

**Summary**: Stream processing is the continuous, incremental processing of unbounded data as it arrives, in contrast to [[batch-processing]] which operates on fixed-size, bounded inputs. It occupies the "near-real-time" space between online services and batch jobs.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## From batch to streams

[[batch-processing]] artificially divides unbounded data into chunks of fixed duration (e.g., process a day's worth at the end of each day). The problem is that changes in the input are only reflected in the output after the batch interval completes, which can be too slow. Stream processing removes this artificial boundary: rather than waiting for a chunk to accumulate, each event is processed as it arrives (source: chapter-11-stream-processing.md).

A "stream" refers to data that is incrementally made available over time. The concept appears in Unix stdin/stdout, programming language lazy lists, filesystem APIs, TCP connections, and audio/video delivery (source: chapter-11-stream-processing.md).

## Core concepts

In streaming terminology (source: chapter-11-stream-processing.md):

- A **record** is called an **event** -- a small, self-contained, immutable object containing the details of something that happened at a point in time (e.g., a user action, a sensor reading, a CPU metric).
- An event is generated once by a **producer** (publisher/sender) and potentially processed by multiple **consumers** (subscribers/recipients).
- Related events are grouped into a **topic** or **stream** (analogous to a filename in a filesystem).

See [[event-streams]] for details on how events are represented and transmitted.

## Where streams come from

Streams originate from several sources (source: chapter-11-stream-processing.md):

1. **User activity events** -- page views, clicks, purchases
2. **Sensors and periodic readings** -- temperature, CPU utilization
3. **Database writes** -- every write to a database can be captured as a stream via [[change-data-capture]] or [[event-sourcing]]
4. **Data feeds** -- market data in finance, news feeds

The insight that database writes are themselves a stream connects databases and streams at a fundamental level. A [[replication]] log is a stream of write events. See [[change-data-capture]] and [[event-sourcing]] for how this idea is exploited.

## Transporting streams

Streams need to move from producers to consumers. Three approaches exist (source: chapter-11-stream-processing.md):

1. **Direct messaging** -- UDP multicast, brokerless libraries (ZeroMQ), webhooks. Simple but limited fault tolerance.
2. **[[message-brokers]]** -- Traditional AMQP/JMS-style brokers (RabbitMQ, ActiveMQ). Buffer messages, support acknowledgments, delete messages after delivery.
3. **[[log-based-message-brokers]]** -- Kafka, Amazon Kinesis. Append-only logs with consumer offsets. Retain messages for replay. Combine database durability with messaging notifications.

## Processing streams

Three things you can do with a stream once you have it (source: chapter-11-stream-processing.md):

1. **Write to storage** -- database, cache, search index. This is the streaming equivalent of [[batch-workflow-outputs]]. See [[change-data-capture]] for keeping derived systems in sync.
2. **Push to users** -- email alerts, push notifications, real-time dashboards.
3. **Produce derived streams** -- process input streams to produce output streams, forming a pipeline of stream processing stages.

A piece of code that processes streams is called an **operator** or **job**, closely related to Unix processes and MapReduce jobs. The key difference from batch jobs: a stream never ends, which affects sorting (impossible with unbounded data), joins (see [[stream-joins]]), and fault tolerance (see [[stream-processing-fault-tolerance]]).

## Uses of stream processing

- **Complex event processing (CEP)** -- searching for patterns of events using declarative rules (Esper, IBM InfoSphere Streams). Queries are stored long-term; events flow past them. This reverses the normal database relationship where data is stored and queries are transient (source: chapter-11-stream-processing.md).
- **Stream analytics** -- aggregations and statistical metrics over [[windowing|windows of time]]: rates, rolling averages, percentile comparisons. Frameworks: Apache Storm, Spark Streaming, Flink, Samza, Kafka Streams (source: chapter-11-stream-processing.md).
- **Maintaining materialized views** -- keeping derived data systems (caches, search indexes, data warehouses) up to date as the source changes. Unlike analytics, this requires a window stretching back to the beginning of time. See [[change-data-capture]] (source: chapter-11-stream-processing.md).
- **Search on streams** -- storing queries and running documents past them (Elasticsearch percolator). The inverse of conventional search (source: chapter-11-stream-processing.md).

## Relationship to batch processing

Stream and [[batch-processing]] are complementary (source: chapter-11-stream-processing.md):

- Batch processing operates on bounded, immutable inputs; stream processing operates on unbounded, continuous inputs.
- [[message-brokers]] and event logs serve as the streaming equivalent of a filesystem.
- [[log-based-message-brokers]] bridge the gap: they provide both database-like durability (replay old messages) and messaging-like low-latency notifications.
- The same join and partitioning patterns from batch processing appear in stream processing, adapted for unbounded data (see [[stream-joins]]).

## Dataflow application design

Chapter 12 extends stream processing beyond traditional data pipelines toward an application architecture. Key ideas (source: chapter-12-the-future-of-data-systems.md):

- **Stream operators as microservice replacements**: composing stream operators has similar organizational benefits to microservices (loose coupling, independent teams) but uses asynchronous one-directional message streams instead of synchronous REST calls. This is both faster (local database lookups vs network requests) and more fault-tolerant.
- **End-to-end event streams**: state changes can flow from a user interaction on one device, through event logs and stream processors, all the way to another user's display with sub-second latency. Technologies like Elm, React/Redux already manage client-side state this way.
- **Reads as events**: read requests can be represented as stream events, turning query serving into a [[stream-joins|stream-table join]]. This enables distributed multi-partition queries using existing stream infrastructure.

See [[unbundling-databases]] and [[derived-data]] for the broader vision of stream-centric application architecture.

## Historical precursor: Google Workflow (SRE Ch 25)

SRE Chapter 25 (Dan Dennison) describes a Google internal system called [[google-workflow|Workflow]] that has been providing continuous data processing with exactly-once semantics since 2003 — predating the modern open-source stream-processing family by approximately a decade (source: raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md). Structurally, Workflow is a stream-processing system: long-running stateless workers, a coordinator (the [[task-master|Task Master]]) holding job topology and progress, multi-stage pipelines via task groups, and strong correctness guarantees.

The mapping to modern terminology:

| Workflow concept (SRE Ch 25) | Modern stream-processing equivalent |
|---|---|
| [[task-master\|Task Master]] | Flink JobManager / Spark Driver / Kafka Streams broker-coordinated state |
| Stateless workers | Flink TaskManagers / Spark executors / Kafka Streams instances |
| Task groups (per pipeline stage) | Operator DAG nodes |
| Lease + unique-filename + barrier guarantees | [[stream-processing-fault-tolerance\|checkpointing + atomic offset commits]] |
| [[workflow-business-continuity\|Multi-cluster reference tasks]] | [[cross-cluster-replication\|MirrorMaker / Kafka cross-cluster replication]] |

The Kleppmann text on stream processing is the contemporary public packaging of architectural intuitions Workflow developed in production a decade earlier. The SRE Ch 25 chapter is also the operational counterpart to this page's optimistic framing: it names the **failure modes of periodic batch pipelines** that motivated the move to continuous processing in the first place — see [[periodic-pipeline]] and the subordinate failure-mode pages ([[pipeline-uneven-work-distribution]], [[pipeline-thundering-herd]], [[moire-load-pattern]]).

## Related pages

- [[event-streams]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[stream-joins]]
- [[windowing]]
- [[stream-processing-fault-tolerance]]
- [[batch-processing]]
- [[dataflow-engines]]
- [[partitioning]]
- [[unbundling-databases]]
- [[derived-data]]
- [[data-integration]]
- [[lambda-architecture]]
- [[exactly-once-semantics]]
- [[google-workflow]]
- [[task-master]]
- [[continuous-data-processing]]
- [[periodic-pipeline]]
- [[data-processing-pipelines]]
