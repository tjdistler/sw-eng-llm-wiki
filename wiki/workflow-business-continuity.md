# Workflow Business Continuity

**Summary**: How [[google-workflow|Workflow]] survives whole-datacenter failures. A single-cluster Workflow is vulnerable to fiber cuts, weather events, and cascading power-grid failures. Workflow addresses this by running **two or more local Workflows in distinct clusters**, plus a **global Workflow** holding **reference tasks** that mirror the local work units. A helper "stage 1" binary in each local cluster maintains the reference tasks and a heartbeat in the global Workflow; if the heartbeat lapses, a remote local Workflow seizes the in-progress work using the reference tasks. The global Workflow journals to [[spanner|Spanner]] for global consistency, and [[chubby|Chubby]] elects which Task Master is authoritative.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The problem

Big Data pipelines need to continue processing despite failures of all types — fiber cuts, weather events, cascading power-grid failures — that can disable entire datacenters (source: chapter-25-data-processing-pipelines.md). Pipelines that do not employ system prevalence to obtain strong job-completion guarantees are often disabled and enter an undefined state, making for a brittle business-continuity strategy with costly mass duplication of effort to restore pipelines and data.

A single-cluster Workflow is better than that — its [[task-master|Task Master]] uses [[system-prevalence-pattern|system prevalence]] for durability — but it is still vulnerable to losing the cluster itself.

## The single-cluster Task Master backbone

Workflow's first layer of business continuity is at the Task Master level (source: chapter-25-data-processing-pipelines.md):

> To obtain global consistency, the Task Master stores journals on Spanner, using it as a globally available, globally consistent, but low-throughput filesystem. To determine which Task Master can write, each Task Master uses the distributed lock service called Chubby to elect the writer, and the result is persisted in Spanner. Finally, clients look up the current Task Master using internal naming services.

So even at the single-cluster level, the Task Master journals globally (Spanner), elects via consensus (Chubby), and is discoverable via naming. This is the standard SRE pattern of consensus-backed leader selection over a globally-consistent datastore — see [[reliable-replicated-datastore]].

The cost: Spanner is "globally available, globally consistent, but low-throughput." It can absorb the journal traffic of a Task Master but not the bulk-data traffic of the pipeline itself. The data plane stays in [[colossus|Colossus]]; only Task Master metadata goes through Spanner.

## The multi-cluster reference-task pattern

Spanner's low throughput means it cannot serve as the substrate for high-volume work itself. To distribute work geographically, **globally distributed Workflows employ two or more local Workflows running in distinct clusters**, plus a notion of **reference tasks** stored in the global Workflow (source: chapter-25-data-processing-pipelines.md).

The flow:

1. As units of work (tasks) are consumed through a local pipeline, equivalent **reference tasks** are inserted into the global Workflow by a binary labeled "stage 1" running inside the local cluster.
2. The local Workflow processes the task as normal — local Task Master, local workers, local I/O.
3. As tasks finish, the reference tasks are **transactionally removed from the global Workflow**.
4. If the tasks cannot be removed from the global Workflow, **the local Workflow blocks** until the global Workflow becomes available again, ensuring transactional correctness.

The reference tasks are a **distributed analogue of the work-in-flight set**: at any moment, the global Workflow knows which work units are claimed by which local cluster. Bulk data and processing happen locally; only the claim metadata is global.

## Failover via heartbeat

Failover is automatic. The "stage 1" helper binary in each local Workflow does two things (source: chapter-25-data-processing-pipelines.md):

- Creates reference tasks in the global Workflow as work is consumed locally.
- Updates a special **heartbeat task** inside the global Workflow at regular intervals.

If the heartbeat task is **not updated within the timeout period**, the remote Workflow's helper binary "seizes the work in progress as documented by the reference tasks and the pipeline continues, unhindered by whatever the environment may do to the work."

The chapter is explicit that this is the **MVC controller pattern**: the helper binary acts as a controller, with the local Workflow itself otherwise unaltered as a "do work" box in the diagram. The business-continuity logic is layered on top of the steady-state Workflow rather than mixed into it.

## Why this works

The pattern composes because of the structural correctness guarantees on [[workflow-correctness-guarantees]]:

- **Reference tasks document claims, not bytes.** The remote Workflow knows what work was in flight even though it doesn't have the local Task Master's full state.
- **Lease and unique-filename guarantees still hold.** Even if the original local Workflow comes back to life and tries to commit work that has been seized, its commits are rejected by the new lease holder; its output files are unique and harmless.
- **Configuration barriers cross clusters.** As long as both clusters have the same configuration, work seized by the remote cluster is consistent with work the original was producing.

The Spanner + Chubby + naming service combination is the same substrate Chapter 23 develops at length: [[managing-critical-state]] over [[reliable-replicated-datastore|reliable replicated datastores]] using [[paxos|Paxos]]-family consensus.

## What it costs

The pattern is not free:

- **Every work unit pays a global-Spanner round-trip** to insert and remove the reference task. This is what the "low throughput" caveat constrains — the rate at which work units can be processed end-to-end is bounded by Spanner's throughput on the reference-task table.
- **Cross-cluster bandwidth for the heartbeat and reference-task traffic.** Modest but nonzero.
- **Operational complexity.** Multi-cluster deployments are harder to operate than single-cluster ones; the stage-1 binary has its own failure modes; configuration drift between clusters can produce subtle bugs.

For pipelines whose business value justifies surviving datacenter loss, the trade is worth it. For pipelines that don't, single-cluster Workflow with Spanner-backed Task Master journaling is sufficient.

## Cross-references

- [[google-workflow]] — the system this layer protects
- [[task-master]] — what the local-cluster Workflow holds; what fails over
- [[workflow-correctness-guarantees]] — why the failover is safe (leases, filenames, configuration barriers, server tokens)
- [[spanner]] (SRE Ch 2) — the globally-consistent low-throughput substrate the global Workflow uses
- [[chubby]] (SRE Ch 2) — the lock service that elects the authoritative Task Master writer
- [[managing-critical-state]] (SRE Ch 23) — the broader pattern Workflow's continuity layer is an instance of
- [[reliable-replicated-datastore]] (SRE Ch 23) — Spanner-as-consensus-backed-datastore is the canonical example; Workflow uses it for the global-Workflow tier
- [[colossus]] (SRE Ch 2) — where the bulk data lives; out of band from the reference-task layer
- [[cross-cluster-replication]] (Bellemare) — the EDM analogue: MirrorMaker-style stream replication across regions; structurally similar (control-plane sync of metadata so consumers can fail over) but operating on event streams rather than work units

## Related pages

- [[google-workflow]]
- [[task-master]]
- [[workflow-correctness-guarantees]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
- [[spanner]]
- [[chubby]]
- [[managing-critical-state]]
- [[reliable-replicated-datastore]]
- [[colossus]]
- [[cross-cluster-replication]]
