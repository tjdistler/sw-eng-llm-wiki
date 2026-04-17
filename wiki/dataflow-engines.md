# Dataflow Engines

**Summary**: Dataflow engines (Spark, Tez, Flink) improve on MapReduce by modeling an entire workflow as a single job with flexible operators, avoiding the unnecessary materialization of intermediate state to disk and enabling pipelined execution.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## Motivation

[[mapreduce]] has fundamental execution model problems that no higher-level abstraction can fix (source: designing-data-intensive-applications, chapter 10):

- Jobs must fully write intermediate state to [[distributed-filesystems|HDFS]] before downstream jobs can start.
- Mapper stages are often redundant — they just read back what a reducer wrote and re-partition it.
- Sorting happens between every map and reduce stage, even when unnecessary.
- HDFS replication of intermediate data is overkill for temporary state.

See [[materialization-of-intermediate-state]] for details.

## The dataflow model

Spark, Tez, and Flink model a workflow as a single job — a directed acyclic graph (DAG) of **operators** connected by data channels. Unlike MapReduce's rigid map-then-reduce alternation, operators can be assembled flexibly (source: designing-data-intensive-applications, chapter 10).

Three ways to connect operators:

1. **Repartition and sort** — Like MapReduce's shuffle. Enables sort-merge joins and grouping.
2. **Repartition without sorting** — Useful for partitioned hash joins where order doesn't matter.
3. **Broadcast** — Send one operator's output to all partitions of another (for broadcast hash joins).

## Advantages over MapReduce

| Improvement | Detail |
|---|---|
| Sort only when needed | Expensive sorting happens only where the algorithm requires it |
| No redundant mappers | A mapper's work can be folded into the preceding reduce operator |
| Locality optimization | The scheduler knows all data dependencies and can co-locate tasks |
| In-memory intermediate state | Intermediate data stays in memory or on local disk, not HDFS |
| Pipelined execution | Operators start as soon as input is ready, no waiting for full stage completion |
| JVM reuse | Existing processes handle new operators, avoiding per-task JVM startup |

(source: designing-data-intensive-applications, chapter 10)

Code written for higher-level frameworks (Pig, Hive, Cascading) can switch from MapReduce to Tez or Spark with a configuration change — no code modifications needed (source: designing-data-intensive-applications, chapter 10).

## Fault tolerance

Without intermediate state on HDFS, dataflow engines take a different approach to recovery (source: designing-data-intensive-applications, chapter 10):

- **Spark**: Uses the **Resilient Distributed Dataset (RDD)** abstraction to track the lineage of each piece of data — which input partitions and operators produced it. Lost data is recomputed from the lineage.
- **Flink**: Periodically **checkpoints operator state**, allowing resumption from the last checkpoint.

### Determinism requirement

Recomputation assumes operators are **deterministic** — given the same input, they produce the same output. If lost data was already sent downstream and the recomputed version differs, contradictions arise. Non-deterministic operators require killing and restarting downstream operators too (source: designing-data-intensive-applications, chapter 10).

Sources of accidental nondeterminism: hash table iteration order, random numbers, system clock access, external data sources. These must be controlled (e.g., fixed random seeds) for reliable fault recovery (source: designing-data-intensive-applications, chapter 10).

### When to materialize anyway

If intermediate data is much smaller than source data, or if computation is very CPU-intensive, materializing to files may be cheaper than recomputing on failure (source: designing-data-intensive-applications, chapter 10).

## Architecture differences

| | Tez | Spark | Flink |
|---|---|---|---|
| Design | Thin library on YARN | Full framework | Full framework |
| Network layer | YARN shuffle service | Own network stack | Own network stack |
| Execution model | DAG of tasks | RDD transformations | Pipelined operators |
| Scheduling | YARN | Own scheduler | Own scheduler |

(source: designing-data-intensive-applications, chapter 10)

## High-level APIs

Dataflow engines provide relational-style building blocks: join, group, filter, aggregate. These high-level APIs enable (source: designing-data-intensive-applications, chapter 10):

- **Interactive exploration** — Write analysis code incrementally in a shell, reminiscent of the [[unix-philosophy]].
- **Cost-based query optimization** — Hive, Spark, and Flink can automatically choose join algorithms and reorder joins to minimize intermediate state. See [[declarative-vs-imperative-queries]].
- **Vectorized execution** — Simple filter and map operations expressed declaratively allow the engine to use [[column-oriented-storage]] layouts and tight CPU-cache-friendly loops. Spark generates JVM bytecode; Impala uses LLVM native code.

As batch frameworks gain declarative operators and query optimizers, and MPP databases become more programmable, the two are converging. See [[hadoop-vs-mpp-databases]] (source: designing-data-intensive-applications, chapter 10).

## Unifying batch and stream processing

Chapter 12 discusses how dataflow engines are evolving to handle both batch and stream workloads in a single system, eliminating the need for the [[lambda-architecture]]. Apache Flink performs batch processing on top of its stream engine; Spark supports streaming via microbatching. Apache Beam provides a unified API that can run on either Flink or Google Cloud Dataflow. Key requirements for unification (source: chapter-12-the-future-of-data-systems.md):

- Replay historical events through the same engine that handles live streams
- [[exactly-once-semantics]] -- discarding partial output of failed tasks
- [[windowing]] by event time, not processing time (processing time is meaningless when reprocessing historical data)

This convergence means a single codebase can handle both real-time event processing and historical reprocessing for [[derived-data|derived data]] systems, without maintaining separate batch and stream implementations.

## Heavyweight streaming descendant

Bellemare's [[heavyweight-framework-microservice]] page covers the same engines — Spark, Flink, Storm, Heron, Beam — from the event-driven-microservices angle (source: raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md). The dataflow-engine architecture described here is the runtime these frameworks execute on; the BEDM framing adds the deployment question ([[stream-processing-cluster|dedicated cluster]] vs CMS-native per-job), application submission modes ([[application-submission-modes|driver vs cluster]]), [[checkpointing-stream-processing|checkpointing]] for long-running stream state, [[external-shuffle-service|ESS-based dynamic scaling]], and the [[multitenancy-in-streaming-clusters|multitenancy]] trade-offs when many streaming jobs share one cluster. DDIA covers the engine; BEDM covers what it takes to run dozens of them as microservices.

## Container-level counterpart: Burns's event-driven batch

Burns's *Designing Distributed Systems* Chapter 11 — the [[event-driven-batch-pattern]] — is the container-level form of the dataflow-DAG idea (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The shape is the same — a DAG of processing stages connected by data channels — but the granularity and transport differ:

| Aspect | DDIA dataflow engines | Burns event-driven batch |
|---|---|---|
| DAG unit | Operator (map, join, filter, aggregate) | [[work-queue-pattern\|Work queue]] (one topic, one worker pool) |
| Transport | In-memory / shuffle files in one cluster | Pub/sub broker ([[publisher-subscriber-infrastructure\|Kafka]], EventGrid, SQS) |
| Scheduling | Single engine owns the whole DAG | Each stage is independent; broker is the glue |
| Fault tolerance | RDD lineage or operator checkpoints | Per-item Kubernetes Job retries + broker durability |
| DAG vocabulary | `join`, `groupBy`, `filter`, `broadcast` | [[copier-pattern\|copier]], [[filter-pattern\|filter]], [[splitter-pattern\|splitter]], [[sharder-pattern\|sharder]], [[merger-pattern\|merger]] |

Dataflow engines win on throughput and fine-grained DAG optimisation within a cluster. Burns's workflow pattern wins on heterogeneity, participant diversity, and the ability to splice work across loosely-coupled teams and systems (because the transport is a broker rather than an engine-internal shuffle). They solve the same abstract problem at different deployment scales.

Chapter 12 — [[coordinated-batch-pattern|coordinated batch processing]] — adds aggregation primitives that close the loop (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). The [[join-pattern|join]] (barrier; wait for every upstream worker to finish) and the [[reduce-pattern|reduce]] (associative pairwise combine; pipelines with upstream work) at container granularity are the same choices dataflow engines make at operator granularity — whether to materialise an intermediate result across a barrier (MapReduce-style) or to pipeline through a reducer as outputs arrive (dataflow-style). Burns's pattern-level distinction between join and reduce is the coarse-grained form of the dataflow optimiser's fine-grained decision about where to pipeline and where to materialise.

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[event-driven-batch-pattern]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[work-queue-pattern]]
- [[materialization-of-intermediate-state]]
- [[distributed-filesystems]]
- [[sort-merge-joins]]
- [[map-side-joins]]
- [[hadoop-vs-mpp-databases]]
- [[declarative-vs-imperative-queries]]
- [[column-oriented-storage]]
- [[unix-philosophy]]
- [[lambda-architecture]]
- [[derived-data]]
- [[exactly-once-semantics]]
- [[stream-processing]]
- [[heavyweight-framework-microservice]]
- [[checkpointing-stream-processing]]
- [[external-shuffle-service]]
- [[stream-processing-cluster]]
