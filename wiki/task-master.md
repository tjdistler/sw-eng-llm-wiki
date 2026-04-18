# Task Master

**Summary**: The "model" in [[google-workflow|Workflow]]'s MVC adaptation. The Task Master is a server that holds **all job state in memory** for fast availability, while **synchronously journaling mutations to persistent disk** via the [[system-prevalence-pattern|system prevalence pattern]]. It is the source of truth that stateless workers update transactionally; if pipeline data is too large to fit in memory, the Task Master holds only **pointers to work** with the actual bulk data living in a [[distributed-filesystems|distributed filesystem]].

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What the Task Master holds

The Task Master is the in-memory model holding all job state of a Workflow pipeline (source: chapter-25-data-processing-pipelines.md):

- The **task groups** corresponding to each pipeline stage.
- The **tasks** within each group — work units to be processed, in-flight work units (with their leases), and completed work units.
- The **pipeline configuration** — the chapter is specific that "all pipeline configuration in Workflow is stored inside the Task Master in the same form as the work units themselves."
- For each task, **a pointer to where the actual data lives** (typically in a common filesystem) and the **lease** held by the worker currently processing it (if any).

Holding all of this in RAM is what makes the Task Master fast — workers can lease a task in a single in-memory operation rather than a multi-step database transaction. The cost is RAM: the Task Master is bounded by what fits in memory, which is why bulk data is kept out of it.

## How durability works

The Task Master uses the [[system-prevalence-pattern|system prevalence pattern]]: state lives in RAM for read access; mutations are **synchronously journaled to persistent disk** before being applied. This gives the durability of a database without the per-operation transaction-log cost — the mutation log is append-only and naturally batched.

On Task Master restart, state is rebuilt by replaying the journal (typically with periodic snapshots to bound recovery time). This is the same pattern as [[redis|Redis]] AOF persistence, [[event-sourcing|event-sourced]] applications, and the in-memory-database literature generally — it predates them all conceptually but they are the modern packaging.

## Why a Task Master and not a database

The chapter anticipates the natural question — why a specialised in-memory system rather than [[spanner|Spanner]] or another transactional database (source: chapter-25-data-processing-pipelines.md):

> Workflow is special because each task is unique and immutable. These twin properties prevent many potentially subtle issues with wide-scale work distribution from occurring. For example, the lease obtained by the worker is part of the task itself, requiring a brand new task even for lease changes.

The lease being part of the task itself means a lease change requires a new task with a new ID. With a general database backing the same model, every read of a task would have to be part of a long-running transaction (because the lease is an attribute of the task being read, and any subsequent lease update is a write). This is "most certainly possible, but terribly inefficient" — and inefficiency at the Task Master is fatal because every worker action goes through it.

The unique-and-immutable task design is what makes the Task Master cheap. A relational substrate could provide the same correctness, but at much higher per-operation cost.

## Pointers, not bulk data

Although all pipeline data **may** be stored in the Task Master, "best performance is usually achieved when only pointers to work are stored in the Task Master, and the actual input and output data is stored in a common filesystem or other storage" (source: chapter-25-data-processing-pipelines.md).

This is the classic control-plane / data-plane split:

- **Task Master (control plane):** task IDs, pointers, leases, configuration, status. RAM-bound, latency-sensitive.
- **Distributed filesystem (data plane):** actual record bytes, intermediate results, final outputs. Storage-bound, throughput-sensitive.

The split lets the Task Master scale on RAM (which is much cheaper per byte than the bandwidth required to handle bulk data through it), and lets the storage layer scale on its own dimensions ([[colossus|Colossus]] is designed for the byte volumes Workflow pipelines produce).

## Task Master uniqueness via server tokens

A subtle correctness concern: what if the Task Master's network address changes and a different Task Master replaces it at the same address? Or memory corruption alters the IP/port? Or — more commonly — someone (mis)configures their Task Master setup by inserting a load balancer in front of a set of independent Task Masters?

Workflow embeds a **server token** — a unique identifier for this particular Task Master — in each task's metadata. Both client and server check the token on every operation, avoiding the very subtle misconfiguration in which all operations run smoothly until a task identifier collision occurs (source: chapter-25-data-processing-pipelines.md). This is the fourth of the [[workflow-correctness-guarantees|four correctness guarantees]].

## Task Master as the failover unit

For business continuity, what fails over is the Task Master, not the workers. Workers are stateless and discardable. In Workflow's [[workflow-business-continuity|business-continuity layer]], the Task Master journals to [[spanner|Spanner]] for global consistency, [[chubby|Chubby]] elects which Task Master can write, and clients look up the current Task Master via internal naming services. The MVC layering pays off here: replacing the model is straightforward because workers don't depend on its identity.

## Cross-references

- [[google-workflow]] — the system Task Master is the heart of
- [[system-prevalence-pattern]] — the storage technique Task Master uses
- [[workflow-correctness-guarantees]] — the four guarantees Task Master enforces (lease, filename, configuration, server token)
- [[workflow-business-continuity]] — the multi-cluster pattern that makes Task Master failover safe
- [[distributed-filesystems]] (Kleppmann) — where the bulk data lives; Task Master holds the pointers
- [[colossus]] (SRE Ch 2) — Google's specific distributed-filesystem implementation
- [[spanner]] (SRE Ch 2) — the globally-consistent substrate Workflow's business-continuity layer journals to
- [[chubby]] (SRE Ch 2) — the lock service that elects which Task Master is authoritative
- [[event-sourcing]] (Kleppmann) — the modern packaging of the same in-memory-state-with-journaling pattern; Task Master predates the term
- [[task-group]] — Workflow's terminology for what corresponds to a pipeline stage; the unit of work the Task Master subdivides processing into
- [[stream-processing-cluster]] (Bellemare) — Flink/Spark's JobManager is the open-source structural equivalent of Task Master; both hold per-job topology and progress as a long-lived in-memory model

## Related pages

- [[google-workflow]]
- [[system-prevalence-pattern]]
- [[workflow-correctness-guarantees]]
- [[workflow-business-continuity]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
- [[distributed-filesystems]]
- [[colossus]]
- [[spanner]]
- [[chubby]]
- [[event-sourcing]]
- [[stream-processing-cluster]]
