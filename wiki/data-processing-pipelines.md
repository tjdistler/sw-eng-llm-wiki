# Data Processing Pipelines

**Summary**: Chapter 25 (Dan Dennison) is about the operational pathology of running large-scale **periodic data pipelines** and the architectural alternative Google built — a leader-follower **continuous data processing** system called **Workflow** that uses the system-prevalence pattern to scale Big Data pipelines without the failure modes of cron-driven batch chains. The chapter's overall message: a pipeline that begins as a periodic cron job and grows into a deep multiphase chain becomes a reliability minefield, and refactoring to a continuous model with strong correctness guarantees is the durable fix.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What Chapter 25 is about

Dennison's chapter is structured as a **before / after**. First it explains the classic [[periodic-pipeline|periodic pipeline]] design pattern — a chain of programs each transforming the previous stage's output, scheduled by cron — and catalogues the failure modes that emerge as the workload grows. Then it introduces [[google-workflow|Workflow]], Google's 2003-vintage continuous data processing system, and shows how leader-follower coordination plus the system-prevalence pattern eliminates those failure modes (source: chapter-25-data-processing-pipelines.md).

The chapter sits adjacent to the [[batch-processing]] / [[mapreduce]] / [[dataflow-engines]] / [[stream-processing]] material from Kleppmann: it is the operational complement that asks what happens when you run those abstractions on real cluster infrastructure under organic load growth, and what reliability guarantees you actually get.

## Pipeline vocabulary

Chapter 25 uses a precise vocabulary:

- A **data pipeline** is a program that reads data, transforms it, and outputs new data — historically scheduled under cron. The lineage runs back to coroutines, the DTSS communication files, the UNIX pipe, and ETL pipelines (source: chapter-25-data-processing-pipelines.md).
- A **simple, one-phase pipeline** is a single program performing a periodic or continuous transformation on Big Data.
- A **multiphase pipeline** is a chain in which the output of one program feeds the next. The number of programs in series is the **depth** of the pipeline. A shallow pipeline has depth 1; a deep pipeline can have depth in the tens or hundreds (source: chapter-25-data-processing-pipelines.md).
- A **periodic pipeline** runs on a schedule (e.g., daily, hourly), as a low-priority batch job.
- A **continuous pipeline** never stops running — events flow through as they arrive.

The depth metric matters because the failure modes scale with depth: a deep periodic pipeline has more synchronisation points, more places for stragglers to delay completion, and more bottlenecks where downstream jobs wait for upstream ones to finish.

## The pathology of periodic pipelines

The chapter's first half is a catalogue of why periodic pipelines, despite working fine when first installed, become unreliable as they grow:

- [[periodic-pipeline]] — the design pattern itself: cron-scheduled chained transformations; stable when carefully tuned, but fragile under organic growth
- [[pipeline-uneven-work-distribution]] — the **hanging chunk problem**: end-to-end runtime is capped by the largest chunk, and the standard "kill and restart" response wastes all completed work because pipelines typically have no checkpointing
- [[pipeline-batch-scheduling-drawbacks]] — periodic pipelines run as low-priority batch jobs; startup latency is open-ended, preemption risk grows with batch utilisation, and the **execution-frequency floor** sets a lower bound on how often a periodic pipeline can actually fire
- [[pipeline-monitoring-problems]] — metrics collected during a run but reported only at completion; a job that fails mid-run produces no statistics, eliminating real-time operational visibility
- [[pipeline-thundering-herd]] — periodic schedules cause thousands of workers to start simultaneously each cycle, overwhelming the cluster scheduler, network, and shared services
- [[moire-load-pattern]] — when multiple periodic pipelines run on overlapping schedules, their resource demand on shared infrastructure occasionally aligns and produces aggregate spikes that hurt on-call

These are not independent bugs — they compound. A hanging chunk causes a job to miss its deadline; an engineer responds by adding more workers; the next run now has a worse thundering herd; the cluster is more loaded so preemption probability rises; the job is more likely to fail mid-run; monitoring sees nothing because the run never completed.

## The Workflow alternative

The chapter's second half describes Google's [[google-workflow|Workflow]] system, which addresses the entire catalogue at the architectural level rather than patching individual symptoms:

- [[google-workflow]] — hub: leader-follower distributed system pattern + [[system-prevalence-pattern|system prevalence]] for transactional data pipelines with exactly-once semantics
- [[task-master]] — the "model" in Workflow's MVC adaptation; in-memory job state with synchronous journaling to persistent disk
- [[system-prevalence-pattern]] — the storage technique Task Master uses: state is held in RAM for fast access, with synchronous journaling of mutations as the durability mechanism
- [[workflow-correctness-guarantees]] — the four guarantees that make Workflow safe under all the failure modes the chapter has been describing: configuration as barrier tasks, lease ownership for committed work, unique output filenames, server tokens to validate the Task Master itself
- [[workflow-business-continuity]] — the multi-cluster deployment pattern that lets Workflow survive whole-datacenter loss: local Workflows in distinct clusters with reference tasks in a global Workflow, helper-binary heartbeat for failover

The architectural punchline is the [[continuous-data-processing|continuous data processing]] page — when a data processing problem is continuous or organically becoming so, do not use a periodic pipeline; use a Workflow-style system with strong guarantees.

## Workflow as model-view-controller

Dennison's framing analogy is that Workflow is the distributed-systems equivalent of MVC (source: chapter-25-data-processing-pipelines.md):

| MVC role | In Workflow | What it does |
|---|---|---|
| Model | [[task-master|Task Master]] | Holds all job state in memory, synchronously journals mutations to disk |
| View | Workers | Stateless processes that update state transactionally with the Task Master from their local perspective |
| Controller | Optional auxiliary system | Runtime scaling, snapshotting, work-cycle state control, rollbacks, global interdiction |

Workers are completely stateless and discardable. Best performance is achieved when the Task Master holds only **pointers** to work and the actual input/output data lives in a common filesystem.

## Stages of execution

Workflow lets pipeline depth grow arbitrarily by **subdividing processing into task groups** held in the Task Master (source: chapter-25-data-processing-pipelines.md). Each task group corresponds to a pipeline stage. A stage usually has an associated worker type. Multiple concurrent instances of a worker type can exist, and workers can self-schedule by picking which type of work to perform.

The worker consumes work units from a previous stage and produces output units for the next. Within the system, **all work is executed (or at least reflected in permanent state) exactly once**.

## Why not just use a database?

Chapter 25 anticipates the natural question — why a specialised Task Master and not [[spanner|Spanner]] or another database (source: chapter-25-data-processing-pipelines.md):

> Workflow is special because each task is unique and immutable. These twin properties prevent many potentially subtle issues with wide-scale work distribution from occurring.

The lease obtained by a worker is part of the task itself, so a lease change requires a brand new task. With a general database, every read would have to be part of a long-running transaction — possible but terribly inefficient at the scale Workflow targets.

## Cross-book framing

Chapter 25 lines up with several existing wiki strands:

- [[batch-processing]] (Kleppmann) / [[mapreduce]] (Dean) / [[dataflow-engines]] (Spark, Flink) — the technologies the chapter critiques are exactly Kleppmann's batch lineage. MapReduce and Flume (Google's pipeline framework) are named directly. Workflow is positioned as the continuous successor that addresses the operational gap Kleppmann's text leaves implicit
- [[stream-processing]] (Kleppmann) — Workflow is structurally a stream-processing system with exactly-once semantics, predating the Flink/Kafka-Streams era by a decade. The "continuous data processing" framing matches Kleppmann's bounded-vs-unbounded distinction
- [[stream-processing-fault-tolerance]] (Kleppmann) — Workflow's [[workflow-correctness-guarantees|four correctness guarantees]] are an alternative realisation of the effectively-once goal: rather than checkpointing + idempotent writes + atomic offset commits, Workflow uses leases + unique filenames + barrier tasks
- [[stream-processing-cluster]] / [[checkpointing-stream-processing]] (Bellemare) — Bellemare's heavyweight-framework substrate (Flink/Spark JobManager + TaskManagers + checkpointing) is the modern open-source equivalent of what Chapter 25's Task Master + workers + Spanner-backed business continuity provides at Google
- [[work-queue-pattern]] (Burns) — Burns's container-level work queue is the simplest realisation of the same model: a queue manager (Task Master analogue) plus stateless workers that lease and commit work items. Workflow generalises this to arbitrary-depth multi-stage pipelines with strong correctness guarantees
- [[distributed-filesystems]] (Kleppmann / Google GFS/Colossus) — Workflow's "best performance when only pointers are stored in Task Master" pattern relies on a [[colossus|Colossus]]-style distributed filesystem to hold the actual bulk data, with the Task Master holding lightweight references. This is the same data/control-plane split [[mapreduce]] uses
- [[cron-thundering-herd]] (SRE Ch 24) — the [[pipeline-thundering-herd|periodic-pipeline thundering herd]] is structurally the same failure mode Chapter 24 addresses for cron, but with much higher per-cycle worker counts and at the application-pipeline rather than scheduler level
- [[cascading-failure]] (SRE Ch 22) — every Chapter 25 failure mode has a Chapter 22 named counterpart: the [[pipeline-thundering-herd]] is a [[cascading-failure-triggers|trigger]]; uneven work distribution is a [[bimodal-latency]]-style stuck-work amplifier; periodic-pipeline frequency-floor pathology is a [[server-overload]] mechanism
- [[paxos]] / [[chubby]] / [[spanner]] (SRE Ch 2 / Ch 23) — Workflow's business-continuity layer uses Chubby for leader election, Spanner as a globally-consistent low-throughput filesystem, and the same consensus-as-a-service substrate Chapter 23 develops
- [[exactly-once-semantics]] (Kleppmann) / [[idempotence]] (Bellemare) — Workflow achieves exactly-once via task uniqueness and immutability rather than via idempotence + dedup. The lease-and-filename-uniqueness mechanism is an alternative path to the same correctness destination

## Related pages

- [[periodic-pipeline]]
- [[pipeline-uneven-work-distribution]]
- [[pipeline-batch-scheduling-drawbacks]]
- [[pipeline-monitoring-problems]]
- [[pipeline-thundering-herd]]
- [[moire-load-pattern]]
- [[google-workflow]]
- [[task-master]]
- [[system-prevalence-pattern]]
- [[workflow-correctness-guarantees]]
- [[workflow-business-continuity]]
- [[continuous-data-processing]]
- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[stream-processing]]
- [[stream-processing-fault-tolerance]]
- [[stream-processing-cluster]]
- [[work-queue-pattern]]
- [[distributed-filesystems]]
- [[cron-thundering-herd]]
- [[cascading-failure]]
- [[exactly-once-semantics]]
- [[site-reliability-engineering]]
