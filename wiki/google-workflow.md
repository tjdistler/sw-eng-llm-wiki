# Google Workflow

**Summary**: Google's continuous data-processing system, developed in 2003 to replace overwhelmed periodic pipelines with a leader-follower architecture providing **exactly-once semantics** for very large transactional data pipelines. Workflow combines two distributed-systems patterns — **leader-follower (workers)** and the **system-prevalence pattern** — and structures itself like an MVC application: the [[task-master|Task Master]] is the model (in-memory job state with synchronous journaling), stateless workers are the view (transactional updates with the master), and an optional controller adds runtime scaling, snapshotting, and rollback. Workflow is the chapter's worked example of [[continuous-data-processing|continuous data processing]] done right.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What Workflow is

Chapter 25 introduces Workflow as Google's response to the periodic-pipeline pathology (source: chapter-25-data-processing-pipelines.md):

> Faced with these needs, Google developed a system in 2003 called "Workflow" that makes continuous processing available at scale. Workflow uses the leader-follower (workers) distributed systems design pattern and the system prevalence design pattern. This combination enables very large-scale transactional data pipelines, ensuring correctness with exactly-once semantics.

Workflow is not a stream-processing engine in the modern Flink/Spark sense, but it occupies the same niche structurally — a long-running coordinator plus stateless workers, with strong correctness guarantees that allow continuous processing of Big Data without the periodic-pipeline failure modes.

## The MVC analogy

The chapter's framing is that Workflow is the distributed-systems equivalent of MVC (source: chapter-25-data-processing-pipelines.md):

| MVC role | In Workflow | What it does |
|---|---|---|
| Model | [[task-master\|Task Master]] | Holds all job state in memory for fast access; synchronously journals mutations to persistent disk via the [[system-prevalence-pattern\|system prevalence pattern]] |
| View | Workers | Stateless processes; continually update system state transactionally with the Task Master from their local perspective as a subcomponent of the pipeline |
| Controller (optional) | Auxiliary system | Runtime scaling, snapshotting, work-cycle state control, rollbacks, global interdiction for business continuity |

The chapter notes the analogy is "very loosely borrowed from Smalltalk" but it captures the architectural decomposition well: the Task Master is the source of truth, workers do not hold state of their own and can be discarded at any time, and the controller is where operational concerns that are not part of the steady-state processing live.

## What lives in the Task Master, and what doesn't

Although all pipeline data **may** be stored in the Task Master, the chapter is explicit that the **best performance is achieved when only pointers to work are stored in the Task Master, and the actual input and output data is stored in a common filesystem or other storage** (source: chapter-25-data-processing-pipelines.md). This is the same control-plane / data-plane split [[mapreduce]] uses: the framework manages metadata, [[distributed-filesystems|distributed storage]] holds the bulk data.

The Task Master is limited by RAM. Storing only pointers keeps it from becoming a bottleneck for storage scale; the actual byte volume of the pipeline data is bounded by [[colossus|Colossus]] (or whatever distributed filesystem is in use), not by the Task Master's memory.

## Stages of execution

Pipeline depth grows arbitrarily by **subdividing processing into task groups** held in the Task Master (source: chapter-25-data-processing-pipelines.md). Each task group corresponds to a pipeline stage that can perform any operation — mapping, shuffling, sorting, splitting, merging, anything. Each stage usually has an associated worker type:

- Multiple concurrent instances of a given worker type can exist.
- Workers can **self-schedule** by looking for different types of work and choosing which to perform.
- The worker consumes work units from a previous stage and produces output units for the next.

The output can be a pipeline endpoint or input for some other processing stage. Within the system, all work is executed (or at least reflected in permanent state) **exactly once** — this is the headline correctness property Workflow provides, developed in detail on [[workflow-correctness-guarantees]].

## Correctness mechanism summary

The chapter develops four guarantees that compose to make exactly-once safe (full detail on [[workflow-correctness-guarantees]]):

1. **Worker output through configuration tasks creates barriers** on which to predicate work. Configuration changes invalidate in-flight work that used the old configuration.
2. **All work committed requires a currently valid lease held by the worker.** Orphaned workers cannot commit because their lease has expired.
3. **Output files are uniquely named by the workers.** Even if two workers race, they write to distinct files; the loser's file is unreferenced and harmless.
4. **The client and server validate the Task Master itself by checking a server token on every operation.** Prevents misconfigured load balancers in front of multiple Task Masters from corrupting state.

Together these provide the exactly-once semantics; importantly, they provide them **without** requiring idempotence in the pipeline payload — the chapter's mechanism is structural rather than defensive.

## Why not just use a database?

The chapter anticipates the natural objection: why a specialised Task Master rather than [[spanner|Spanner]] or another database (source: chapter-25-data-processing-pipelines.md)?

> Workflow is special because each task is unique and immutable. These twin properties prevent many potentially subtle issues with wide-scale work distribution from occurring.

The lease obtained by a worker is part of the task itself, so a lease change requires a brand new task with a new ID. With a general-purpose database backing the same model, every read would have to be part of a long-running transaction (because the lease is an attribute of the task being read, and any lease change is a write). This is "most certainly possible, but terribly inefficient."

The Task Master is engineered for the exactly-once semantics it provides, with the data shape that makes those semantics cheap. A relational/transactional substrate could provide the same correctness but at much higher per-operation cost.

## Business continuity

A single-cluster Task Master is vulnerable to whole-datacenter loss. Chapter 25 develops a multi-cluster pattern for surviving such failures: see [[workflow-business-continuity]]. The summary: two or more local Workflows in distinct clusters, plus a global Workflow holding **reference tasks** that mirror the local work units; on local-cluster failure, the remote local Workflow seizes the in-progress work using the reference tasks. Spanner provides the globally-consistent low-throughput substrate; [[chubby|Chubby]] elects the writer.

## Cross-references

- [[task-master]] — the in-memory state model at the heart of Workflow; the "M" in the MVC analogy
- [[system-prevalence-pattern]] — the storage technique Task Master uses (in-memory + synchronous journaling)
- [[workflow-correctness-guarantees]] — the four guarantees that make exactly-once work
- [[workflow-business-continuity]] — multi-cluster deployment for surviving datacenter loss
- [[continuous-data-processing]] — the broader category Workflow is the worked example of
- [[stream-processing]] (Kleppmann Ch 11) — the modern open-source family Workflow predates by ~10 years
- [[stream-processing-cluster]] / [[checkpointing-stream-processing]] (Bellemare) — the open-source equivalents of Workflow's coordinator-plus-workers and recovery machinery
- [[work-queue-pattern]] (Burns) — the container-level minimal version of the same shape: queue manager + stateless workers
- [[mapreduce]] / [[dataflow-engines]] (Kleppmann) — the periodic-batch family Workflow was designed to replace for continuous workloads
- [[paxos]] / [[chubby]] / [[spanner]] (SRE Ch 2 / Ch 23) — the substrate Workflow's business-continuity layer relies on
- [[idempotence]] (Kleppmann / Bellemare) — Workflow notably does **not** require idempotence in the payload; correctness comes from the structural lease + filename mechanism instead

## Related pages

- [[task-master]]
- [[system-prevalence-pattern]]
- [[workflow-correctness-guarantees]]
- [[workflow-business-continuity]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
- [[periodic-pipeline]]
- [[stream-processing]]
- [[stream-processing-cluster]]
- [[checkpointing-stream-processing]]
- [[work-queue-pattern]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[paxos]]
- [[chubby]]
- [[spanner]]
- [[exactly-once-semantics]]
