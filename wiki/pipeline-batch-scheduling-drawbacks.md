# Pipeline Batch Scheduling Drawbacks

**Summary**: Periodic pipelines at Google run as **low-priority batch jobs** because they are not latency-sensitive in the same way Internet-facing services are. That priority designation has structural consequences: open-ended startup delays, preemption risk that grows with cluster batch utilisation, and — most importantly — a **lower bound on execution frequency**. Below that bound, scheduling the next run only produces overlapping or aborted executions, not faster turnaround.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## Why periodic pipelines run at batch priority

Google's cluster manager [[borg|Borg]] supports an alternative scheduling mechanism for periodic pipelines that runs them as lower-priority batch jobs (source: chapter-25-data-processing-pipelines.md). The reasoning is straightforward: batch work is not sensitive to latency the way Internet-facing web services are, so it can absorb the variability of being scheduled into whatever capacity is available after the user-facing services have what they need.

Batch scheduling is also the way Google maximises machine workload to control cost — Borg fills the unused capacity left by user-facing jobs with batch work. From the global cost-of-fleet perspective this is the right answer; from any single periodic pipeline's perspective it produces a list of natural limitations.

## The four limitations

### 1. Open-ended startup delay

Jobs invoked through the batch mechanism can experience open-ended startup delays. A pipeline scheduled for "midnight" may start anywhere from a few seconds to many minutes after midnight depending on what's available in the cluster. The cost equation: **execution cost is inversely proportional to requested startup delay, and directly proportional to resources consumed**. You can pay more to start sooner, but the cheaper your batch slot, the more the wait.

### 2. Pricing and stability of access

Jobs scheduled in the gaps left by user-facing services get whatever resources happen to be free. They may be on slower machines, on machines that were just freed up after a long-running job ended (so caches are cold), or in datacenter regions where there is excess capacity for unrelated reasons. The pipeline has limited control over the quality of the resources it gets.

### 3. Preemption risk

Excessive use of the batch scheduler places jobs at risk of preemption (source: chapter-25-data-processing-pipelines.md). When cluster load is high — typically because higher-priority work is competing for the same machines — batch jobs are killed to free resources. A periodic pipeline that runs deeply enough to span a load spike may have any of its workers killed mid-cycle.

Running a well-tuned periodic pipeline successfully is a "delicate balance between high resource cost and risk of preemptions": pay more for higher-priority resources to cut preemption risk, or pay less and accept that some cycles will be killed.

### 4. The execution-frequency floor

The fourth limitation is the most operationally interesting. Even granted batch resources, the **average startup delay sets a lower bound on how often a periodic pipeline can actually fire** (source: chapter-25-data-processing-pipelines.md):

> Reducing the job execution interval below this effective lower bound simply results in undesirable behavior rather than increased progress.

The chapter's worked example: a ~20-minute job running on a scheduler with average ~20-minute startup delay has its idle interval cross the scheduling delay around 40 minutes. Lowering the interval much below 40 minutes produces overlapping executions.

The specific failure mode depends on the batch scheduler's policy:

- New runs may **stack up on the scheduler** because the previous run is not complete.
- The currently-executing run might be **killed when the next is scheduled to begin** — completely halting all progress in the name of increasing executions.

Either way, the periodic-pipeline operator cannot improve freshness below the floor by turning the periodicity dial.

## The recommended (and unsatisfying) workaround

The chapter's stated solution is to **secure sufficient server capacity for proper operation** — i.e., move the pipeline up the priority ladder so it can run reliably (source: chapter-25-data-processing-pipelines.md). But this runs into resource economics: in a shared distributed environment, development teams are reluctant to go through the processes of acquiring resources that must be contributed to a common pool. Distinguishing **batch-scheduling resources** from **production-priority resources** is what lets each be costed and acquired separately — but that distinction is itself an operational discipline, not a technical fact.

The implicit recommendation, developed in the rest of Chapter 25, is to **stop running the work as a periodic batch job** and adopt [[continuous-data-processing|continuous data processing]] with [[google-workflow|Workflow]]. A continuous pipeline doesn't have batch-priority startup delay (its workers are already running), doesn't have the execution-frequency floor (there is no per-cycle scheduling), and trades off preemption-vulnerability for the leader-follower replication that makes Workflow tolerant of individual worker loss.

## Cross-references

- [[borg]] (SRE Ch 2 / Ch 7) — the cluster scheduler whose batch-tier policies are the source of all four limitations
- [[handling-overload]] (SRE Ch 21) / [[request-criticality]] (SRE Ch 21) — Chapter 21's criticality framework is the request-level analogue of the batch-vs-production-priority distinction Chapter 25 invokes; both are mechanisms for telling the scheduler/serving layer which work to drop first when capacity is tight
- [[capacity-planning]] (SRE Ch 1 / Ch 18) — the "secure sufficient capacity" recommendation is a capacity-planning problem; [[auxon]]'s intent-based plans would naturally express "I need this pipeline to run within X minutes 99% of cycles" as an SLO and let the planner allocate the priority needed
- [[cron-leader-follower]] (SRE Ch 24) — for the cron service itself, Google avoided batch priority and ran the cron leader at production priority to ensure scheduling latency. The same calculus applies in reverse: any system that is on the critical path of business operations should not be on batch tier

## Related pages

- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[borg]]
- [[handling-overload]]
- [[capacity-planning]]
