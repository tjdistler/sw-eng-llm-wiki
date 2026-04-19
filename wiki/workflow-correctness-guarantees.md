# Workflow Correctness Guarantees

**Summary**: The four structural mechanisms that make [[google-workflow|Workflow]]'s exactly-once semantics safe under all the failure modes a continuous data pipeline encounters: **configuration as barrier tasks**, **lease-bound commits**, **uniquely-named output files**, and **server-token validation of the Task Master itself**. Together they ensure that orphaned workers cannot destroy committed work, lease changes cannot be silently lost, post-configuration-change work is consistent with the new configuration, and a misconfigured Task Master cannot corrupt the pipeline. The mechanism is **structural** rather than defensive — Workflow does not require pipeline payloads to be idempotent.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## Why the guarantees are needed

A continuous data pipeline runs many concurrent workers, each leasing a unit of work from the [[task-master|Task Master]] and committing the result. The failure modes that have to be handled (source: chapter-25-data-processing-pipelines.md):

- A worker may be **orphaned** — the Task Master no longer hears from it, the lease expires, the work is reassigned, but the original worker is still running and will eventually try to commit.
- A **lease may be reassigned** mid-task; both the old and new lease-holder may attempt to commit.
- The **configuration may change** while work is in flight; results from workers using the old config may not be valid under the new one.
- The **Task Master itself may be misconfigured** — load balancer in front of multiple Task Masters, IP/port collision after a restart, network corruption — and accept operations that should have been rejected.

A naive "trust the worker to commit" model fails on the first three; a naive "trust the address of the Task Master" fails on the fourth.

## The four guarantees

Chapter 25 enumerates them explicitly (source: chapter-25-data-processing-pipelines.md):

> The four Workflow correctness guarantees are:
>
> - Worker output through configuration tasks creates barriers on which to predicate work.
> - All work committed requires a currently valid lease held by the worker.
> - Output files are uniquely named by the workers.
> - The client and server validate the Task Master itself by checking a server token on every operation.

Together these provide what the chapter calls a "double correctness guarantee" extended through versioned tasks and server tokens to a "triple" and ultimately to the four enumerated here.

### Guarantee 1: Configuration as barrier tasks

Configuration changes are stored in the Task Master in the **same form as work units themselves** (source: chapter-25-data-processing-pipelines.md). To commit work, a worker must reference the **task ID number of the configuration it used** to produce its result. If the configuration changed while the work unit was in flight, all workers of that type will be unable to commit — their output references the old config-task ID, which is no longer current.

The cost: work performed under the old configuration after a config change is thrown away by workers unfortunate enough to hold old leases. The benefit: **all work performed after a configuration change is consistent with the new configuration**, with no manual reconciliation needed.

This is the chapter's term "barrier" used in a different sense from the [[distributed-barrier]] page — here a barrier is a versioned configuration object whose ID is part of every committed result, not a synchronisation point that blocks until a condition is met.

### Guarantee 2: Lease-bound commits

Workers acquire work with a **lease** and may only commit work from tasks for which they currently possess a valid lease (source: chapter-25-data-processing-pipelines.md). If a worker is orphaned and its lease has been reassigned, its commit attempt will be rejected because another worker now holds the lease.

Workflow also **versions all tasks**: if the task updates or the lease changes, each operation yields a new unique task replacing the previous one, with a new ID. So even checking "is my lease still valid" is a comparison against the current task's lease, which may have been replaced entirely.

The combination of leases + task versioning means that the commit operation is structurally tied to the specific lease the worker acquired — there is no "commit if you happen to have any lease" path.

### Guarantee 3: Unique output filenames

Each output file opened by a worker has a **unique name** (source: chapter-25-data-processing-pipelines.md). This is what handles the orphaned-worker case before lease enforcement kicks in:

> Even orphaned workers can continue writing independently of the master until they attempt to commit. Upon attempting a commit, they will be unable to do so because another worker holds the lease for that work unit. Furthermore, orphaned workers cannot destroy the work produced by a valid worker, because the unique filename scheme ensures that every worker is writing to a distinct file.

The orphaned worker's output files become unreferenced — no committed task points to them, so they're harmless. They will be garbage-collected by some background process. The valid worker's output, written to its own unique filename, is unaffected.

This is structurally identical to the temp-file-and-atomic-rename pattern Unix applications use for safe file replacement, generalised to a distributed-pipeline context.

### Guarantee 4: Server-token validation

The fourth guarantee addresses Task Master itself: what if the Task Master's network address changed and a different Task Master replaced it at the same address? Or memory corruption altered the IP/port? Or someone (mis)configured the system by inserting a load balancer in front of a set of independent Task Masters?

Workflow **embeds a server token**, a unique identifier for this particular Task Master, in each task's metadata (source: chapter-25-data-processing-pipelines.md). Both client and server check the token on every operation, avoiding "a very subtle misconfiguration in which all operations run smoothly until a task identifier collision occurs."

This is the kind of guarantee that protects against operator error and infrastructure misconfiguration rather than worker failure. Without it, Workflow would be a perfectly correct system that breaks the moment someone puts a load balancer in front of multiple Task Masters, with the failure mode being silent state corruption rather than visible errors.

## How the guarantees compose

The four guarantees address different layers of failure:

| Failure | Caught by |
|---|---|
| Orphaned worker overwriting valid worker's file | Unique filenames |
| Two workers committing the same task | Lease-bound commits |
| Lease change during work | Task versioning + lease check on commit |
| Worker uses old configuration | Configuration task ID barrier |
| Multiple Task Masters at same address | Server token validation |

A real distributed pipeline failure can hit any combination of these simultaneously. Workflow's safety is that the guarantees are independent — none requires the others — and together they cover the failure surface without requiring the application code to be idempotent or otherwise carefully written.

## Comparison to other exactly-once mechanisms

The wiki has several other approaches to exactly-once semantics:

- [[exactly-once-semantics]] / [[idempotence]] (Kleppmann / Bellemare) — the at-least-once + idempotent-handler approach. Cheaper to deploy but requires every handler to be idempotent.
- [[stream-processing-fault-tolerance]] (Kleppmann) — microbatching + checkpointing + atomic offset commits. The Flink-style approach.
- [[effectively-once-processing]] (Bellemare) — a near-synonym for the above, named more precisely.
- This page (Chapter 25) — the lease + unique-filename + barrier + server-token approach. Structural rather than defensive; correctness does not depend on application-code properties.

The trade-off: Workflow's approach requires the substrate to enforce all four guarantees, and it requires the unique-and-immutable-task data shape. The Flink/Bellemare approach lets you build on more general substrates (Kafka, any database) but requires application-level discipline. Both reach the same correctness destination by different paths.

## Cross-references

- [[google-workflow]] — the system these guarantees protect
- [[task-master]] — where the configuration tasks, leases, and server tokens live
- [[exactly-once-semantics]] (Kleppmann) — the broader concept; this page is the Workflow-specific realisation
- [[idempotence]] (Kleppmann / Bellemare) — the alternative path; Workflow notably does **not** require it
- [[stream-processing-fault-tolerance]] (Kleppmann) — the modern open-source family of mechanisms with the same goal
- [[effectively-once-processing]] (Bellemare) — Bellemare's preferred terminology for the same property
- [[fencing-tokens]] (Kleppmann / SRE Ch 23) — Workflow's task versioning is structurally similar to fencing tokens: monotonically-increasing IDs that let downstream operations reject stale work. The combination of "configuration task ID" + "task version" + "lease ID" is a multi-dimensional fencing system
- Atomic rename / safe file replacement — the Unix idiom Guarantee 3 generalises

## Related pages

- [[google-workflow]]
- [[task-master]]
- [[system-prevalence-pattern]]
- [[workflow-business-continuity]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
- [[exactly-once-semantics]]
- [[idempotence]]
- [[stream-processing-fault-tolerance]]
- [[effectively-once-processing]]
- [[fencing-tokens]]
