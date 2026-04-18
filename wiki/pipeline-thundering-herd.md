# Pipeline Thundering Herd

**Summary**: For each cycle of a sufficiently large [[periodic-pipeline|periodic pipeline]], potentially **thousands of workers immediately start work** at the scheduled instant. If sizing is wrong, retry logic is naive, or — most commonly — engineers under deadline pressure have added more workers to compensate for previous slow cycles, the simultaneous start overwhelms the cluster scheduler, the network, and any shared services the pipeline touches. Chapter 25 names this the **thundering herd** in the periodic-pipeline context, distinct from but related to the [[cron-thundering-herd|cron-level thundering herd]] and the [[retry-amplification|retry-amplification]] thundering herd.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The pattern

Chapter 25 names this directly (source: chapter-25-data-processing-pipelines.md):

> Given a large enough periodic pipeline, for each cycle, potentially thousands of workers immediately start work. If there are too many workers or if the workers are misconfigured or invoked by faulty retry logic, the servers on which they run will be overwhelmed, as will the underlying shared cluster services, and any networking infrastructure that was being used will also be overwhelmed.

The synchronisation comes from the periodic schedule itself: every worker is supposed to start at the same instant, because the next pipeline stage cannot begin until all upstream workers have finished, so launching them all at once minimises end-to-end runtime. The same property that makes periodic pipelines straightforward to reason about (everything is in lockstep) is what makes their start-of-cycle resource demand unbounded.

## The amplification factors

Three factors compound the basic synchronisation problem:

### 1. Worker count growing organically

Engineers with limited experience managing pipelines tend to add more workers when the job fails to complete in time (source: chapter-25-data-processing-pipelines.md). If the underlying problem is a [[pipeline-uneven-work-distribution|hanging chunk]] caused by uneven partitioning, more workers don't help completion time but they do make the start-of-cycle herd worse. The next cycle launches more workers; the cluster is now more loaded at start-of-cycle; some workers fail to schedule promptly; the engineer adds more workers; the cycle continues.

### 2. Retry logic interactions

The chapter is specific about retry behaviour:

- **No retry logic.** Work is dropped on failure. The job won't be retried. Correctness problems result.
- **Naive retry logic.** Failure causes immediate re-launch, so the herd that overwhelmed shared services on the first attempt is followed by a second herd seconds later.
- **Properly-implemented retry logic.** With exponential backoff and jitter, retries are spread out — but the *first* herd is still synchronised.

In all three cases, the first-attempt synchronisation problem remains. Retry policy can make it worse but cannot make it better.

### 3. Human intervention

Chapter 25 calls this out specifically: "Engineers with limited experience managing pipelines tend to amplify this problem by adding more workers to their pipeline when the job fails to complete within a desired period of time." The chapter's closing observation:

> Regardless of the source of the "thundering herd" problem, nothing is harder on cluster infrastructure and the SREs responsible for a cluster's various services than a buggy 10,000 worker pipeline job.

## Why continuous pipelines escape this

A continuous pipeline (the [[google-workflow|Workflow]] design) has workers that are already running. New work flows through the existing worker fleet rather than triggering a fresh worker launch:

- The Task Master gets new work units; existing workers acquire leases on them as they become free.
- There is no synchronised "start of cycle" event; work arrives continuously and is processed continuously.
- The peak-vs-average resource demand ratio is dramatically lower because demand is smoothed over the full cycle period.

This converts a peak-load problem into an average-load problem. A workload that requires 10,000 workers running for one hour out of every 24 has a 24× peak-to-average ratio in the periodic case and a 1× ratio in the continuous case (with appropriate sizing). The cluster need only provision for the continuous load level.

## Relationship to other thundering-herd patterns

The wiki has several related thundering-herd pages, each at a different layer:

- [[cron-thundering-herd]] (SRE Ch 24) — synchronised launches caused by users picking round numbers (`0 0 * * *`); fixed by hash-based time distribution via the `?` crontab extension. The cron-level version of the same synchronisation pathology.
- [[retry-amplification]] (SRE Ch 22) — synchronised retries from clients that all hit the same outage; fixed by randomised exponential backoff. The retry-loop version.
- [[slow-startup-and-cold-caching]] (SRE Ch 22) — restart-cascades from synchronised cold caches at boot. The cache-warming version.
- This page (SRE Ch 25) — synchronised worker launches from a periodic pipeline; the only fix that addresses the root is to **stop being periodic**.

The unifying theme: synchronisation that the underlying work doesn't actually require, imposed by the surrounding scheduling/retry/recovery machinery. The wiki page [[cron-thundering-herd]] frames this generally — "break synchronisation that the underlying time-distribution of events didn't intend to create."

## Cross-references

- [[cascading-failure]] (SRE Ch 22) — Chapter 25's thundering herd is a [[cascading-failure-triggers|cascading-failure trigger]] in Chapter 22's vocabulary; an overwhelmed cluster scheduler can cause unrelated services on the same infrastructure to time out, which can cause their clients to retry, and so on
- [[server-overload]] (SRE Ch 22) — the proximate consequence; a 10,000-worker pipeline that overwhelms shared infrastructure is producing the demand spike Chapter 22 catalogues as the dominant cause of cascades
- [[capacity-planning]] (SRE Ch 1) — the periodic-pipeline herd is what makes capacity planning hard for shared infrastructure: peak demand is concentrated at predictable but synchronised instants, and the planner has to provision for the peak even though the average is much lower

## Related pages

- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[pipeline-uneven-work-distribution]]
- [[moire-load-pattern]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[cron-thundering-herd]]
- [[retry-amplification]]
- [[cascading-failure]]
- [[server-overload]]
