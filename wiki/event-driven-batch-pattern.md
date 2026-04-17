# Event-Driven Batch Pattern

**Summary**: The second of Burns's batch computational patterns and the hub for Chapter 11. Individual [[work-queue-pattern|work queues]] are **chained together** into a directed acyclic graph of processing stages, where the output of one queue becomes the input of the next. The resulting **workflow system** executes multi-step batch jobs that no single work queue could express — copying items into parallel streams, filtering them, sharding them, splitting them onto divergent paths, or merging them back together. A small vocabulary of named linking patterns — copier, filter, splitter, sharder, merger — covers the recurring topologies.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## From work queue to workflow

[[work-queue-pattern|Chapter 10's work queue]] processes wholly independent items with one transformation per item: one input, one output (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). That is enough for embarrassingly parallel jobs like thumbnailing a directory of videos, but many real batch applications need more: multiple outputs from a single input, conditional routing, load spreading across failure zones, or joining several upstream streams into one.

Burns's answer is to **chain work queues end-to-end**. The output of one queue becomes the input of one or more downstream queues. Each queue remains a standard [[work-queue-pattern]] instance — generic queue-manager, [[source-container-interface|source ambassador]], [[worker-container-interface|file-based worker]] — but the completion of a worker is itself an event that triggers the next queue (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

The result is a **workflow system**: "a directed, acyclic graph that describes the various stages and their coordination" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Events flowing through the graph are the completion signals of the preceding stages.

## Why a named vocabulary matters

The simplest chaining — single-queue-to-single-queue — is trivial, and Burns skips past it. The interesting cases are where queues fan out, filter, split, shard, or merge, and the graph becomes a non-linear topology (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

Without a vocabulary for these topologies, workflows become opaque: "the operation of an event-driven batch processor is similar to event-driven FaaS. Consequently, without an overall blueprint for how the different event queues relate to each other, it can be hard to fully understand how the system is operating" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

Burns's five named linking patterns are the blueprint vocabulary:

| Pattern | Job | Analogy |
|---|---|---|
| [[copier-pattern]] | Duplicate one stream into N identical streams | Unix `tee` |
| [[filter-pattern]] | Drop items that don't meet criteria | Unix `grep` |
| [[splitter-pattern]] | Route items to different queues based on criteria | Conditional routing |
| [[sharder-pattern]] | Evenly distribute items across N queues by a shard function | Partitioning |
| [[merger-pattern]] | Combine N streams into one | Union / merge |

Naming these lets the designer read a workflow diagram and immediately know what each node does, and lets the implementer reach for a library container rather than inventing glue from scratch.

## How the linking is implemented

Each linking pattern is implemented as an **adapter** or **ambassador** at the seam between queues (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

- A **filter** is a [[source-container-interface|source ambassador]] that wraps an upstream source; the original source returns the full list, the filter ambassador applies the predicate and returns the shorter list to the queue-manager. The downstream work queue is unaware it has been filtered.
- A **copier** or **splitter** is a worker-side adapter that writes the item into multiple downstream topics instead of one.
- A **merger** is a [[multi-worker-pattern|multi-source adapter]] — the adapted thing is a **set** of upstream sources rather than a single one.

Burns's recurring framing: "the merger is another great example of the adapter pattern, though in this case, the adapter is actually adapting multiple running source containers into a single merged source" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The same observation applies, with variations, to every other linking pattern.

## The pub/sub substrate

Burns treats publisher/subscriber infrastructure — Kafka, Azure EventGrid, AWS SQS, Google Pub/Sub — as the **transport layer** that wires the workflow together (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Each output stream in the workflow is a **topic**; each linking-pattern container publishes to or subscribes from topics; the broker handles durable storage, partitioning, and replication.

See [[publisher-subscriber-infrastructure]] for Burns's Kafka-on-Kubernetes walkthrough and the `photos-1, photos-2, photos-3` sharder-output-topics worked example.

## Worked example: user-signup workflow

Burns's chapter-length worked example composes several linking patterns for a new-user signup flow (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

1. **Stage 1 — verification email.** New signups are handed to a [[sharder-pattern|sharder]] that spreads them across multiple geographic failure zones. Each shard runs the same verification-email worker. Sharding here buys **reliability against datacenter failures** rather than load balancing.
2. **Stage 2 — email confirmation triggers a new workflow.** When the user clicks the verification link, a second workflow begins.
3. **Stage 3 — copier fans out.** A [[copier-pattern|copier]] duplicates the verified-user event into two parallel queues: one sends the welcome email, the other sets up notification preferences.
4. **Stage 4 — filter / splitter for notifications.** The notification-preferences queue feeds into a [[splitter-pattern|splitter]] that routes users onto email-notifications, text-notifications, both, or neither based on their chosen preferences.

Reading the graph tells you what happens on signup. That is the same payoff Burns highlights in [[event-pipeline-pattern|Chapter 8's FaaS event pipelines]]: the topology *is* the specification.

## Relationship to event pipelines (Chapter 8)

Burns explicitly notes the parallel: "the operation of an event-driven batch processor is similar to event-driven FaaS" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Both are graphs of handlers connected by events.

The differences are substrate and scope:

| Aspect | [[event-pipeline-pattern]] (Ch 8 FaaS) | Event-driven batch (Ch 11) |
|---|---|---|
| Unit of work | One short-lived function per event | One work queue per stage |
| Granularity | Fine — one webhook per event | Coarse — batch of items per stage |
| Throughput assumption | Interactive / bursty | Batch / high-volume |
| Transport | HTTP webhooks (often) | Pub/sub broker (typically Kafka) |
| Good for | User-facing async side-effects | Large bulk processing, ETL, media pipelines |

The patterns are cousins. Both rely on a named topology vocabulary; both are graphs; both admit heterogeneous participants. Burns builds Chapter 11 atop Chapter 10's work-queue primitives specifically to scale this shape up to throughput-oriented batch workloads.

## Relationship to DDIA dataflow engines

At the DDIA layer, [[dataflow-engines]] (Spark, Flink, Tez) model a batch workflow as a DAG of operators connected by data channels — the **same shape** as Burns's event-driven batch workflow (source: raw/designing-data-intensive-applications/chapter-10-batch-processing.md).

The differences are granularity and transport, again:

| Aspect | DDIA dataflow engines | Burns event-driven batch |
|---|---|---|
| DAG unit | Operator (map, join, filter, aggregate) | Work queue (one topic, one worker pool) |
| Transport between units | In-memory / shuffle files within one cluster | Pub/sub broker across arbitrary clusters |
| Scheduler | Single engine owns the whole DAG | Each queue is independent; broker is the glue |
| Fault tolerance | RDD lineage or operator checkpoints | Per-item Kubernetes Job retries + broker durability |

Dataflow engines win on throughput and fine-grained DAG optimisation inside one cluster; Burns's workflow wins on heterogeneity, participant diversity, and the ability to splice work across loosely-coupled teams and systems. They solve the same abstract problem at different deployment scales.

## Closing the loop: coordinated batch processing (Chapter 12)

The Chapter 11 linking patterns excel at splitting work and chaining it through a DAG, but they do not provide the aggregation primitives needed to close the loop back into a single result. That is the subject of [[coordinated-batch-pattern|Chapter 12]], which adds two primitives (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

- [[join-pattern]] — barrier synchronization; wait until every upstream parallel path has finished before releasing downstream work. Required when a downstream step is destructive or depends on completeness.
- [[reduce-pattern]] — associative pairwise combine; pipelines with upstream work by starting combines as soon as two outputs exist. The container-level naming of MapReduce's reduce step.

Burns is explicit that the [[merger-pattern|merger]] from Chapter 11 is *not* sufficient for these cases — it concatenates streams but guarantees neither completeness nor aggregation. The Chapter 12 primitives are the coordination vocabulary that Chapter 11's linking vocabulary lacks.

## Relationship to workflow schedulers

Airflow, Argo Workflows, Prefect, and Luigi are named workflow-scheduling systems that implement exactly the DAG-of-batch-stages model Burns describes. Burns does not cite them by name but his pattern is their vocabulary: a copier is a `fan-out` operator, a merger is a `join` node, a sharder is a `map-partition`. Understanding the Chapter 11 vocabulary gives you the primitives these schedulers implement.

## When the pattern fits

Event-driven batch workflows fit when:

- The job naturally decomposes into multiple stages with fan-out, filtering, or merging.
- Each stage is itself a [[work-queue-pattern|work queue]] — batch of independent items, embarrassingly parallel within the stage.
- Throughput matters more than per-item latency.
- Stages evolve at different rates or are owned by different teams.
- A pub/sub broker is available as the glue substrate.

It does not fit when:

- All items require the same single transformation — a plain work queue is simpler.
- Stages have fine cross-item dependencies that cross stage boundaries — you need [[mapreduce]] or [[dataflow-engines]] instead.
- Per-event latency matters more than throughput — [[event-pipeline-pattern|FaaS event pipelines]] are better.
- The graph is small and the stages live in one cluster — a single dataflow engine job is simpler than a broker-mediated multi-cluster workflow.

## Related pages

- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[worker-container-interface]]
- [[multi-worker-pattern]]
- [[event-pipeline-pattern]]
- [[functions-as-a-service]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[batch-processing]]
- [[dataflow-engines]]
- [[mapreduce]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[designing-distributed-systems]]
