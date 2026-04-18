# Work Queue Pattern

**Summary**: The first of Burns's batch computational patterns. A **work queue** processes a batch of wholly independent work items by dispatching each item to a worker container; the system as a whole is responsible for ensuring every item is processed within some target time, and it scales workers up and down to keep up. Burns's thesis is that the machinery around the queue — pulling items, tracking which are done, scheduling workers — is almost entirely generic and can live in a **reusable library container**, while the application-specific parts collapse into two narrow interfaces: a **source container** that produces items and a **worker container** that processes them.

**Sources**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`, `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What a work queue is

In a work queue system there is a batch of work to be performed, each piece wholly independent of the others and processable in isolation (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The goal is to ensure that every item is processed within some target time; workers are scaled up or down to hit that target.

This is the simplest form of batch processing — there is no shuffle, no join, no cross-item dependency. In the broader taxonomy it corresponds to **embarrassingly parallel** offline jobs: generating thumbnails for a batch of videos, running a classifier over a set of images, producing per-file outputs from a directory of inputs.

## The reusable-container thesis

Most of the work-queue's logic — fetching work, scheduling workers, tracking completion, handling failures — has nothing to do with the specific job being run. Burns's observation is that this generic logic can be packaged once as a library container and reused across many different applications; what varies between applications is only **where the items come from** and **what to do with each item** (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

That split motivates two narrow container interfaces:

| Interface | Role | Lives in | API style |
|---|---|---|---|
| [[source-container-interface]] | Produces work items | Coresident with the queue manager (pod) | HTTP REST on `localhost` |
| [[worker-container-interface]] | Processes one work item | Separate per-item container group | File-based (env var points at a file) |

The generic queue-manager container consumes from the first and spawns instances of the second. The user supplies one source implementation and one worker implementation per application.

## The queue-manager algorithm

Burns's queue-manager runs this loop continuously (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

1. Load the available work by calling the source container interface.
2. Consult the work-queue state to determine which items have been processed or are in progress.
3. For remaining items, spawn jobs that use the worker container interface to process them.
4. When a worker container finishes successfully, record the item as completed.

Crucially, the queue-manager does not need its own database. Burns leans on **Kubernetes Job objects** and **annotations** to track progress (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

- A Kubernetes Job runs a worker container until it completes successfully, surviving machine failures — the orchestrator itself provides reliable execution of each item.
- Each Job is annotated with the work item it is processing, so the queue-manager can list running jobs and diff against the source's item list to find the unprocessed set.

This is a striking case of **pushing state into the orchestrator** — the queue manager stores no state of its own; Kubernetes is the source of truth about which items are in progress or done. Compare with [[operator-pattern]], which also leans on the orchestrator's API as durable storage.

The chapter includes a short Python driver (~30 lines) that implements exactly this loop against `localhost:8000/items` (the source ambassador) and `BatchV1Api.create_namespaced_job` (the worker launcher) (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

## The video-thumbnailer worked example

Burns's concrete example is a thumbnail-generation pipeline over a directory of MP4 files (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

- **Source container**: a ~30-line Node program that reads a `MEDIA_PATH` environment variable and returns the list of `*.mp4` files as the `items` response.
- **Worker container**: the off-the-shelf `jrottenberg/ffmpeg` Docker image invoked as `ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png`.

Neither container is bespoke to thumbnailing in interesting ways — the source is a directory listing, the worker is `ffmpeg`. That is Burns's point: the distance between an idea for a batch job and a running implementation is very short once the generic queue-manager exists.

## Relationship to existing wiki concepts

### Work queues vs DDIA batch processing

[[batch-processing]] in DDIA covers the Unix-to-MapReduce-to-dataflow lineage — partitioned shuffles, joins, distributed filesystems. Burns's work queue sits **below** that lineage: it is what you build when each item is wholly independent and you do not need a shuffle at all. A [[mapreduce]] job is a work queue for mappers plus a shuffle plus a work queue for reducers — in that sense the work queue is the primitive, and MapReduce composes it with partitioning.

The connection in the other direction: Burns's queue-manager **is** the orchestrator component that MapReduce, [[dataflow-engines]], and workflow schedulers (Airflow, Oozie) all contain. Chapter 10 is the container-level view of the task-dispatch core common to all of them.

### Work queues vs message brokers

A work queue conceptually resembles a [[message-brokers|message broker]] consumer loop — a pool of workers draining items from a queue. Two differences matter:

- Burns's work queue is a **pull model** driven by a generic manager against an ambassador source, and the source may be a filesystem listing, a cloud-storage bucket, or a pub/sub topic; the broker case is just one of several source shapes (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).
- Completion tracking lives in the **orchestrator** (Kubernetes Job objects and annotations), not in the broker's offset/ack machinery. That is a different design point than [[log-based-message-brokers|Kafka consumer offsets]]: work-item identity is the job's name, not a log offset.

Burns's pattern and the broker-consumer pattern can be composed: a source ambassador that reads from Kafka or Redis pub/sub turns a topic into a work queue's item list.

### Work queues vs FaaS

[[functions-as-a-service|FaaS]] is an event-driven substrate where each event becomes a short-lived function invocation. A work queue could be implemented on top of FaaS — enumerate items, fire one function per item — and in cloud environments this is often the right call for sufficiently small, stateless workers. Burns's container-based pattern is the self-hosted alternative when the worker's compute profile (duration, memory, side effects) does not fit FaaS's constraints. See the fit/no-fit discussion in [[functions-as-a-service]].

### Work queues and ambassador / adapter patterns

Burns explicitly frames the source container interface as an instance of the [[ambassador-pattern]]: the queue manager is the application, and the source container is the coresident ambassador that proxies "fetch the next items" out to the concrete backing store (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). See [[source-container-interface]].

He frames the [[multi-worker-pattern]] (composing several worker containers for a single item) as a specialisation of the [[adapter-pattern]] — the multi-worker aggregator transforms a collection of worker containers into a single unified container that implements the worker interface.

### Work queues and orchestrator-backed state

The work queue's use of Kubernetes Jobs as its durable state mirrors the [[operator-pattern]]'s use of orchestrator custom resources: rather than maintaining a sidecar database, treat the orchestrator's API server as the system of record. This is a recurring theme in Burns's container patterns — lean on the orchestrator for durability, scheduling, and restart semantics.

## When the pattern fits

The work queue fits when:

- Work items are independent (no cross-item ordering or joins).
- Each item has a natural identifier the queue manager can use to track completion.
- Items can be enumerated or streamed from a single source.
- Worker containers can be made idempotent (Kubernetes may restart a worker under a machine failure; the item must be safe to reprocess).

The pattern does not fit when items are not independent (you want [[mapreduce]] or [[dataflow-engines]]), when items stream continuously and never end (you want [[stream-processing]] or an event pipeline), or when per-item latency must be near-interactive (you want a [[replicated-load-balanced-service]] instead of a batch pattern).

## Composing work queues: event-driven batch workflows

When a single transformation isn't enough — when a job needs multiple outputs from one input, conditional routing, or a merge of several upstream streams — Burns's [[event-driven-batch-pattern|Chapter 11 event-driven batch pattern]] chains multiple work queues together into a DAG (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Each stage is still a standard work queue; a small vocabulary of linking patterns ([[copier-pattern|copier]], [[filter-pattern|filter]], [[splitter-pattern|splitter]], [[sharder-pattern|sharder]], [[merger-pattern|merger]]) wires them together over a [[publisher-subscriber-infrastructure|pub/sub broker]]. Chapter 11 builds directly on this chapter: the work queue is the stage, the workflow is the composition.

Burns's [[coordinated-batch-pattern|Chapter 12 coordinated batch pattern]] then closes the loop by adding two aggregation primitives that pull parallel workflow outputs back together: the [[join-pattern|join]] (barrier; wait for every upstream worker before continuing) and the [[reduce-pattern|reduce]] (pairwise associative combine; the container-level naming of MapReduce's reduce step) (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). Together, Chapters 10–12 form Burns's batch trilogy — work queue as the primitive, event-driven batch as the composition, coordinated batch as the aggregation.

## Industrial-scale equivalent: Google Workflow (SRE Ch 25)

Burns's container-level work queue is structurally the **simplest case** of the architecture SRE Chapter 25 (Dan Dennison) describes at much larger scale as Google [[google-workflow|Workflow]] (source: raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md). Both designs share the same architectural intuition:

- A **coordinator** holds the source of truth for "what work exists, what's in progress, what's done." Burns calls this the queue manager and pushes the state into Kubernetes Job annotations; Workflow calls it the [[task-master|Task Master]] and uses the [[system-prevalence-pattern|system prevalence pattern]] — in-memory state with synchronous journaling.
- **Stateless workers** lease work from the coordinator, process it, and commit results. Burns's worker container is one-shot per item (Kubernetes Job lifetime); Workflow's worker is long-running and processes many items, but each individual item-lease is structurally the same.
- **State lives outside the worker.** Burns pushes it into the orchestrator (Kubernetes); Workflow pushes it into the Task Master plus a [[distributed-filesystems|distributed filesystem]] for bulk data.

Workflow generalises Burns's pattern in three directions:

1. **Multi-stage pipelines.** Workflow's task groups let arbitrary-depth pipelines run inside one coordinator; Burns's [[event-driven-batch-pattern]] composes multiple work queues over a broker to do the same thing across containers.
2. **Strong correctness guarantees.** Workflow's [[workflow-correctness-guarantees|four guarantees]] (lease + unique filenames + configuration barriers + server tokens) provide exactly-once semantics without requiring idempotent workers. Burns's pattern relies on the application worker being idempotent because Kubernetes Jobs may restart on failure.
3. **Multi-cluster business continuity.** Workflow's [[workflow-business-continuity|reference-task pattern]] across two or more clusters survives whole-datacenter loss; Burns's pattern is single-cluster.

The progression Burns → Workflow is the path a work queue takes as the workload outgrows what container-level patterns alone can guarantee. For most batch workloads at human scale, Burns's pattern is sufficient; for production data pipelines whose business value justifies surviving datacenter loss with provable exactly-once correctness, the additional machinery Workflow provides is warranted.

## Related pages

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
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[operator-pattern]]
- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[google-workflow]]
- [[task-master]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
- [[functions-as-a-service]]
- [[exactly-once-semantics]]
- [[designing-distributed-systems]]
