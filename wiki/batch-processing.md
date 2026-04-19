# Batch Processing

**Summary**: Batch processing systems take a large, bounded dataset as input, run a computation over it, and produce output data. They prioritize throughput over latency, and their design philosophy of immutable inputs and deterministic outputs enables fault tolerance and easy reasoning.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`, `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18
---

## Three types of systems

Data systems fall into three categories based on how they process data (source: designing-data-intensive-applications, chapter 10):

| Type | Also called | Response model | Primary metric |
|---|---|---|---|
| Services | Online systems | Request/response, user waiting | Response time |
| Batch processing | Offline systems | Run job, produce output | Throughput |
| Stream processing | Near-real-time | Continuous input/output | Latency (lower than batch) |

Batch processing is the oldest form of computing — punch card tabulating machines used in the 1890 US Census were a semi-mechanized form of batch processing (source: designing-data-intensive-applications, chapter 10).

## Core principles

Batch processing inherits the [[unix-philosophy]] of data processing (source: designing-data-intensive-applications, chapter 10):

- **Immutable inputs**: The input data is never modified. You can rerun a job as many times as you like without corrupting state.
- **Outputs replace previous outputs**: Each run produces a complete new output, not a mutation of existing data.
- **No side effects**: Beyond producing output, the job has no externally visible effects.
- **Composability**: Small, well-defined jobs can be chained into larger workflows.

These properties enable **human fault tolerance** — if you deploy buggy code that produces wrong output, you can roll back the code and rerun the job. The old output is still intact. Databases with read-write transactions do not have this property (source: designing-data-intensive-applications, chapter 10).

## From Unix pipes to distributed systems

The chapter traces a lineage from Unix command-line tools through [[mapreduce]] to modern [[dataflow-engines]] (source: designing-data-intensive-applications, chapter 10):

1. **Unix tools** (`awk`, `sort`, `uniq`, `grep`) — single-machine batch processing with pipes connecting stages. Limited to one machine.
2. **[[mapreduce]]** — distributed batch processing on commodity clusters, using [[distributed-filesystems]] (HDFS) instead of pipes. Robust but slow due to full materialization of intermediate state.
3. **[[dataflow-engines]]** (Spark, Tez, Flink) — generalize MapReduce by treating an entire workflow as a single job with flexible operators, keeping intermediate state in memory rather than writing to disk.

## Key problems batch processing solves

### Partitioning
Mappers are partitioned according to input file blocks. Mapper output is repartitioned, sorted, and merged into reducer partitions. The goal is to bring all related data (same key) to the same place. See [[partitioning]] (source: designing-data-intensive-applications, chapter 10).

### Fault tolerance
[[mapreduce]] writes frequently to disk, making it easy to retry individual failed tasks but slowing the common case. [[dataflow-engines]] keep more intermediate state in memory and recompute from earlier stages on failure (source: designing-data-intensive-applications, chapter 10).

### Joins
Batch join algorithms include [[sort-merge-joins]] (reduce-side), [[map-side-joins]] (broadcast hash, partitioned hash, merge), and various skew-handling techniques. These same algorithms are used internally by MPP databases (source: designing-data-intensive-applications, chapter 10).

## Outputs of batch workflows

Batch jobs rarely produce human-readable reports. Common outputs include (source: designing-data-intensive-applications, chapter 10):

- **Search indexes** — Google originally used MapReduce to build search indexes; Hadoop MapReduce is still used for building Lucene/Solr indexes.
- **Key-value stores** — Machine learning models, recommendation databases, and precomputed query results are built as immutable database files and bulk-loaded into serving systems.
- **Inputs to other batch jobs** — Workflows of 50–100 chained jobs are common in recommendation systems.

See [[batch-workflow-outputs]] for details.

## Hadoop vs MPP databases

The same parallel join algorithms existed in MPP databases (Teradata, Tandem NonStop SQL) a decade before MapReduce. The key difference is that Hadoop provides a general-purpose operating system for arbitrary programs on a distributed filesystem, while MPP databases are monolithic systems optimized for SQL analytics. See [[hadoop-vs-mpp-databases]] (source: designing-data-intensive-applications, chapter 10).

## Relationship to stream processing

Batch processing assumes bounded input -- the job knows when it has finished reading. In reality, most data is unbounded (users produce data continuously), so batch processing must artificially divide it into time chunks (e.g., daily or hourly). The delay between data arriving and being reflected in output is at least one batch interval (source: chapter-11-stream-processing.md).

[[stream-processing]] removes this artificial boundary by processing each event as it arrives. The two approaches are complementary rather than competing (source: chapter-11-stream-processing.md):

- **[[message-brokers]] and event logs** are the streaming equivalent of a filesystem -- they transport and store the data that stream processors consume.
- **[[log-based-message-brokers]]** bridge the gap: they provide batch-like properties (immutable, replayable input) with streaming-like properties (low-latency notification). Consuming messages is read-only, and consumer offsets can be reset to reprocess data, just like rerunning a batch job on the same input files.
- **Fault tolerance**: Batch processing retries failed tasks and discards partial output. Stream processing uses [[stream-processing-fault-tolerance|microbatching, checkpointing, or idempotent writes]] to achieve the same effectively-once guarantee.
- **Joins**: The same join patterns from batch processing ([[sort-merge-joins]], [[map-side-joins]]) appear in stream processing, adapted for unbounded data. See [[stream-joins]].

## Reprocessing for application evolution

Beyond producing [[derived-data|derived datasets]], batch processing enables schema evolution far beyond adding optional fields. By reprocessing the entire historical dataset with new derivation code, you can restructure data into a completely different model. Old and new schemas can coexist as independently derived views, allowing **gradual migration**: shift users to the new view incrementally, roll back if something goes wrong. This is analogous to converting railway track gauges via a third rail (source: chapter-12-the-future-of-data-systems.md).

## Unifying batch and stream processing

The [[lambda-architecture]] originally proposed running batch and stream processing in parallel, but maintaining the same logic in two frameworks proved burdensome. Modern systems unify both in a single engine: Spark performs stream processing via microbatching, while Apache Flink performs batch processing on top of its stream engine. Requirements for unification include replay of historical events, [[exactly-once-semantics]], and [[windowing]] by event time (source: chapter-12-the-future-of-data-systems.md).

See [[lambda-architecture]] and [[data-integration]] for the full picture.

## Container-level perspective: Burns's work queue

Burns's *Designing Distributed Systems* Chapter 10 opens Part III of that book with the **[[work-queue-pattern]]** — the simplest batch computational pattern, for wholly independent items with no shuffle, join, or cross-item dependency (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The work queue sits **below** the DDIA batch lineage in the stack: it is the dispatch-one-item-per-worker primitive that [[mapreduce]] composes with partitioning, and that [[dataflow-engines]] generalise into arbitrary DAGs. A MapReduce job is structurally a work queue for mappers, plus a shuffle, plus a work queue for reducers.

Burns's contribution is **container-level**: the generic queue-management logic (fetch items, schedule workers, track completion, handle failure) is packaged once as a reusable library container, with the application-specific parts reduced to a [[source-container-interface|source ambassador]] and a [[worker-container-interface|file-based worker]]. Kubernetes Jobs with annotations provide the durable state — the queue-manager itself stores nothing. This is the deployment-shape counterpart to DDIA's algorithmic coverage.

Burns's Chapter 11 — the [[event-driven-batch-pattern]] — chains these work queues into multi-stage workflows, a named vocabulary of linking patterns ([[copier-pattern]], [[filter-pattern]], [[splitter-pattern]], [[sharder-pattern]], [[merger-pattern]]) wired over a [[publisher-subscriber-infrastructure|pub/sub broker]] (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). This is the container-level analogue of a [[dataflow-engines|dataflow engine's]] DAG, with each node a work queue rather than an operator and the transport a broker rather than in-cluster shuffles. It covers the same design ground as Airflow, Argo Workflows, Prefect, and Luigi — workflow schedulers that operate at batch-stage granularity rather than per-record.

Chapter 12 closes Burns's batch trilogy with [[coordinated-batch-pattern|coordinated batch processing]] (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md): pulling parallel workflow outputs back together into a single aggregate result. Two primitives do that work — the [[join-pattern|join]] (barrier synchronization, waits for every upstream worker) and the [[reduce-pattern|reduce]] (associative pairwise combine, pipelines with upstream work). Burns's framing makes the identity with [[mapreduce|MapReduce]] explicit: map = [[sharder-pattern|sharder]], reduce = reduce-pattern, the MapReduce "wait for all mappers" barrier = join-pattern. This names at container granularity the same structural choices that [[dataflow-engines]] expose at operator granularity when they decide to pipeline through a reduce or to materialise for a barrier.

## FoDE framing — batch is a specialisation of streaming

Reis and Housley invert the usual batch-vs-streaming framing. In Chapter 2 of *Fundamentals of Data Engineering* they argue that **virtually all data is inherently streaming**: data is nearly always produced and updated continually at its source. Batch ingestion is "simply a specialized and convenient way of processing this stream in large chunks — for example, handling a full day's worth of data in a single batch" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

This is the same insight Kleppmann develops technically in DDIA Ch 11 (every database write is an event; batch and stream differ only in where the file boundary is drawn), but Reis and Housley turn it into a **decision heuristic** for the data engineer at the [[data-ingestion|ingestion]] stage: treat streaming as the default framing, then choose batch as a deliberate specialisation when its trade-offs favour you.

Their recommendation (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

> We think batch is an excellent approach for many common use cases, such as model training and weekly reporting. Adopt true real-time streaming only after identifying a business use case that justifies the trade-offs against using batch.

See [[data-ingestion]] for the streaming-first checklist they offer.

## Operational pathology of large periodic batch chains (SRE Ch 25)

Kleppmann and Burns describe the algorithmic and container-level shape of batch processing; SRE Chapter 25 (Dan Dennison) is the **operational** complement that names what goes wrong at large scale. The chapter develops two contrasts (source: raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md):

- A [[periodic-pipeline|periodic pipeline]] — the cron-scheduled chained-program design pattern — is stable when carefully tuned but **fragile under organic growth**. Five named failure modes accumulate as the pipeline grows: [[pipeline-uneven-work-distribution|hanging chunks]], [[pipeline-batch-scheduling-drawbacks|batch-scheduling drawbacks including the execution-frequency floor]], [[pipeline-monitoring-problems|monitoring blackouts when jobs fail mid-run]], [[pipeline-thundering-herd|start-of-cycle thundering herds]], and the multi-pipeline [[moire-load-pattern|Moiré load pattern]] on shared infrastructure.
- The architectural alternative is [[continuous-data-processing|continuous data processing]] — workers that never stop running and process work units as they arrive. Google's specific implementation is [[google-workflow|Workflow]], a 2003 system with leader-follower coordination, an in-memory [[task-master|Task Master]] using the [[system-prevalence-pattern|system prevalence pattern]] for durability, [[workflow-correctness-guarantees|four structural correctness guarantees]] providing exactly-once semantics, and a [[workflow-business-continuity|multi-cluster business-continuity layer]] for surviving datacenter loss.

The chapter's recommendation: if the data processing problem is continuous or will organically grow to become continuous, do not use a periodic pipeline. The Kleppmann immutable-input/replaceable-output principles still apply at the algorithmic level; the SRE Ch 25 contribution is naming when the **deployment shape** of those algorithms (cron-driven batch chain) breaks down and what the alternative shape (long-running workers + coordinator) looks like. Workflow predates the modern open-source [[stream-processing|stream processing]] family by ~10 years and is one of the systems whose design choices the Flink/Spark/Beam lineage absorbed.

## Related pages

- [[unix-philosophy]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[distributed-filesystems]]
- [[periodic-pipeline]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[data-processing-pipelines]]
- [[sort-merge-joins]]
- [[map-side-joins]]
- [[batch-workflow-outputs]]
- [[hadoop-vs-mpp-databases]]
- [[materialization-of-intermediate-state]]
- [[graph-batch-processing]]
- [[oltp-vs-olap]]
- [[partitioning]]
- [[stream-processing]]
- [[log-based-message-brokers]]
- [[stream-joins]]
- [[stream-processing-fault-tolerance]]
- [[lambda-architecture]]
- [[derived-data]]
- [[data-integration]]
- [[exactly-once-semantics]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[worker-container-interface]]
- [[dynamic-worker-scaling]]
- [[multi-worker-pattern]]
- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[data-ingestion]]
- [[data-transformation]]
