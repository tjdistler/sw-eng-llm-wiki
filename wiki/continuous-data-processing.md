# Continuous Data Processing

**Summary**: Chapter 25's recommended alternative to [[periodic-pipeline|periodic pipelines]]: a data-processing system whose workers **never stop running** and whose work units flow through continuously, rather than being scheduled into discrete cycles. The chapter's central architectural claim is that periodic and continuous pipelines are not just two points on a frequency continuum — at high-enough frequency, the periodic model breaks structurally — and a system designed for continuous processing avoids the failure modes that emerge when periodic pipelines grow.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The recommendation

Chapter 25's closing rule (source: chapter-25-data-processing-pipelines.md):

> Periodic pipelines are valuable. However, if a data processing problem is continuous or will organically grow to become continuous, don't use a periodic pipeline. Instead, use a technology with characteristics similar to [[google-workflow|Workflow]].

The chapter is careful not to declare periodic pipelines obsolete — it explicitly says they remain useful and Google still runs many of them. The recommendation is conditional: if the problem is continuous, or has growth trajectory that will make it continuous, the continuous-processing tools are the appropriate choice.

## What "continuous" means structurally

Continuous data processing is not just "run the periodic pipeline more often." Below a certain interval, more frequent periodic execution stops working — see [[pipeline-batch-scheduling-drawbacks|the execution-frequency floor]]. Continuous processing is a structurally different shape:

| Property | Periodic pipeline | Continuous data processing |
|---|---|---|
| Worker lifetime | Spawned per cycle, terminate at end | Long-running, always present |
| Scheduling | Cron-like; one cycle = one start event | None; work flows in as it arrives |
| Peak-to-average load | High (concentrated at start of cycle) | Low (smoothed over time) |
| Telemetry | Reported at end of cycle | Real-time |
| State | Re-derived from inputs each cycle | Maintained continuously across work |
| Failure recovery | Restart the cycle | Lease re-acquisition, partial-result preservation |

These differences are why patches don't compose: addressing each periodic-pipeline failure mode individually still leaves you in the periodic shape. Going continuous moves you to a different shape where most of the failure modes don't have a place to manifest.

## What continuous processing escapes

Continuous data processing structurally avoids each Chapter 25 periodic-pipeline failure mode:

- [[pipeline-uneven-work-distribution|Uneven work distribution]] — work units flow through individually, leased one at a time. A slow chunk doesn't hold up unrelated chunks. The "kill and restart wastes everything" failure mode doesn't apply because per-task leases naturally checkpoint progress.
- [[pipeline-batch-scheduling-drawbacks|Batch-scheduling drawbacks]] — workers run at production priority because they're long-lived; there is no per-cycle startup latency to amortise. The execution-frequency floor doesn't apply because there are no "cycles."
- [[pipeline-monitoring-problems|Monitoring problems]] — workers are always running, so [[varz-endpoints|`/varz`]] endpoints are always exposing real-time metrics. Continuous-pipeline telemetry matches the operator's "what is it doing right now" mental model.
- [[pipeline-thundering-herd|Thundering herd]] — work arrives smoothly; existing workers acquire it as they become free. There is no synchronised launch event.
- [[moire-load-pattern|Moiré load pattern]] — load arrives evenly so multiple continuous pipelines don't have peaks to align. The Moiré pattern can still occur but is much less common.

## What continuous processing requires

The trade-off is that continuous processing requires a substrate that periodic pipelines don't:

- **A long-running coordinator** that holds the work-units state. In Workflow this is the [[task-master|Task Master]]; in Flink/Spark it's the JobManager; in Kafka Streams it's the broker plus per-instance state.
- **A leasing protocol** so that work is processed exactly once even when workers fail mid-task. In Workflow this is [[workflow-correctness-guarantees|the lease-and-unique-filename machinery]]; in stream-processing systems it's [[checkpointing-stream-processing|checkpoints + atomic offset commits]].
- **State migration** so that long-running stateful workers can be replaced without losing work in flight. In Workflow workers are stateless (state lives in the Task Master); in Flink state moves via savepoints; in Kafka Streams state rebuilds from changelog topics.
- **Business-continuity machinery** to survive whole-cluster loss without operator intervention. See [[workflow-business-continuity]] for Workflow's specific approach: local Workflows in distinct clusters with a global Workflow tracking reference tasks.

## The frequency continuum

Chapter 25's opening framing is that there is a frequency continuum from "very infrequently" (e.g., once per day) to "continuous (never stops)." The chapter's argument is not that the continuum is illusory — many real workloads naturally fit somewhere along it — but that there are **discontinuities** that produce significant operational problems:

- Below a certain interval, periodic pipelines hit the execution-frequency floor.
- Above a certain depth, periodic pipelines hit hanging-chunk problems.
- Above a certain worker count, periodic pipelines hit thundering-herd problems.

The wise choice is to identify which side of these discontinuities a workload sits on (now and projected) and use the appropriate technology — periodic for genuinely infrequent and small workloads, continuous for everything that's projected to outgrow the discontinuities.

## Cross-book framing

Continuous data processing as Chapter 25 describes it overlaps strongly with the [[stream-processing|stream processing]] family from Kleppmann's DDIA Ch 11:

- **Workflow's Task Master** corresponds to a stream-processing engine's job manager + state stores; both keep job topology and progress as a long-lived in-memory model.
- **Workflow's stateless workers** correspond to Flink's TaskManagers; both pull leases / partitions and execute against a coordinator.
- **Workflow's exactly-once via leases + unique filenames** is an alternative path to the same destination as Kleppmann's [[stream-processing-fault-tolerance|microbatching + checkpointing + idempotent writes]] or Bellemare's [[effectively-once-processing]].

The terminology overlap is not coincidental — Workflow predated the modern stream-processing era by a decade and is one of the systems whose ideas the open-source stream processors absorbed. The Kleppmann/Bellemare material is the contemporary public packaging of the same architectural intuitions Chapter 25 describes from inside Google.

## Cross-references

- [[stream-processing]] (Kleppmann Ch 11) — the modern open-source equivalent family of systems; the bounded-vs-unbounded framing maps directly to periodic-vs-continuous
- [[stream-processing-fault-tolerance]] (Kleppmann) — alternative implementations of the same exactly-once goal Workflow achieves with leases and unique filenames
- [[stream-processing-cluster]] (Bellemare) — the substrate for heavyweight stream-processing frameworks; the open-source analogue of Workflow's coordinator-plus-workers shape
- [[checkpointing-stream-processing]] (Bellemare) — the periodic-snapshot recovery primitive that solves the same "what if a worker fails mid-task" problem Workflow's leases solve
- [[work-queue-pattern]] (Burns) — the simplest continuous-processing pattern at container granularity: a queue manager (Task Master analogue) plus stateless workers that lease work
- [[batch-processing]] (Kleppmann) — the broader family of which periodic pipelines are an instance; continuous data processing is what you reach for when the batch model's bounded-input assumption breaks
- [[lambda-architecture]] (Kleppmann) — the historical attempt to bridge batch and stream by running both; the continuous-data-processing argument is one of the reasons the unified-engine approach (Flink, Spark Structured Streaming) won

## Related pages

- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[google-workflow]]
- [[task-master]]
- [[workflow-correctness-guarantees]]
- [[workflow-business-continuity]]
- [[stream-processing]]
- [[stream-processing-fault-tolerance]]
- [[stream-processing-cluster]]
- [[checkpointing-stream-processing]]
- [[work-queue-pattern]]
- [[batch-processing]]
