# Periodic Pipeline

**Summary**: A **periodic pipeline** is a data-processing program (or chain of programs) executed under the control of a periodic scheduler such as cron — read input, transform, emit output, terminate, wait for the next scheduled tick. The pattern is intuitive, easy to reason about, and stable when the workload fits its initial sizing. Chapter 25's central observation is that periodic pipelines are **fragile under organic growth**: the moment data volumes, processing complexity, or dependency depth start changing, a long list of failure modes (uneven work distribution, batch-scheduling preemption, monitoring blackouts, thundering herds, moiré load) arises. The remedy is not to patch the failures one at a time but to refactor to [[continuous-data-processing|continuous data processing]].

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## What a periodic pipeline is

The classic data-processing approach: write a program that reads in data, transforms it, and outputs new data. Schedule it under a periodic scheduling program such as cron (source: chapter-25-data-processing-pipelines.md). The lineage runs back through ETL pipelines, the UNIX pipe, the DTSS communication files, and coroutines.

When data is large enough to require Big Data techniques, programs are usually organised into a **chained series**: the output of one program becomes the input of the next. Such a chain is a **multiphase pipeline**. The number of programs in series is the **depth** of the pipeline:

- A **shallow pipeline** has depth 1 — a single transformation program.
- A **deep pipeline** has depth in the tens or hundreds — a long chain.

Each program in the chain is a discrete data processing phase. The whole chain is scheduled to run periodically — daily, hourly, every five minutes — depending on data freshness needs.

## When periodic pipelines work fine

Chapter 25 is explicit that periodic pipelines are useful and practical, and Google runs them on a regular basis (source: chapter-25-data-processing-pipelines.md). The pattern is stable when:

- There are sufficient workers for the data volume and execution demand stays within computational capacity.
- The number of chained jobs and the relative throughput between jobs remain uniform — no stage becomes a bottleneck.
- Worker sizing, periodicity, chunking technique, and other parameters are carefully tuned for the initial workload.

Under those conditions a periodic pipeline can run reliably for a long time. The frameworks Google uses for them — [[mapreduce|MapReduce]] and Flume — are well-engineered, and small-to-medium periodic workloads are exactly what they were designed for.

## Why periodic pipelines become unreliable at scale

Chapter 25's collective SRE experience is that the periodic pipeline model is fragile (source: chapter-25-data-processing-pipelines.md). When a periodic pipeline is first installed with worker sizing carefully tuned, performance is initially reliable. **Organic growth and change inevitably begin to stress the system, and problems arise**:

- Jobs that exceed their run deadline.
- Resource exhaustion.
- Hanging processing chunks that entail corresponding operational load.

The chapter then catalogues five distinct failure modes, each with its own page:

1. [[pipeline-uneven-work-distribution]] — the **hanging chunk problem**. Embarrassingly-parallel chunking assumes the chunks are roughly the same size; they often aren't. End-to-end runtime is capped by the largest chunk. The default response (kill and restart) wastes all completed work because pipelines typically have no checkpointing.
2. [[pipeline-batch-scheduling-drawbacks]] — periodic pipelines are scheduled as low-priority batch jobs. Startup latency is open-ended, batch jobs face preemption when cluster load is high, and the scheduling system imposes a **lower bound on execution frequency** below which the next run starts colliding with the previous one.
3. [[pipeline-monitoring-problems]] — the standard pattern collects metrics during execution but reports them only on completion. A job that fails during execution produces no statistics, eliminating the real-time operational visibility needed for emergency response.
4. [[pipeline-thundering-herd]] — at each cycle, thousands of workers immediately start. If sizing or retry logic is wrong, the cluster scheduler, network, and shared services are all overwhelmed simultaneously.
5. [[moire-load-pattern]] — when multiple periodic pipelines run on overlapping schedules, their resource demand on shared infrastructure occasionally aligns and produces aggregate spikes that hurt on-call.

These failures are not independent — they compound. Hanging chunk causes deadline miss → engineer adds workers → next cycle has worse thundering herd → cluster more loaded → preemption probability rises → job more likely to fail mid-run → monitoring sees nothing → root cause is harder to find.

## Why "just patch the failures" doesn't work

Chapter 25's architectural argument is that each failure mode admits a local patch but the patches don't compose:

- Add checkpointing to fix hanging chunks → adds complexity and storage cost; the schema changes when the pipeline does.
- Distribute starts to fix the thundering herd → only mitigates the symptom; the underlying coordinated-cycle assumption is still there.
- Add real-time metrics to fix monitoring → the pipeline still terminates between runs, so dashboards still go blank in the gaps.
- Reduce the schedule period to improve freshness → hits the execution-frequency floor and starts producing overlapping runs.

Each fix moves the failure surface around. The architectural fix is to abandon the "schedule + run + terminate" cycle entirely and adopt [[continuous-data-processing|continuous processing]], where the pipeline never stops and these failure modes don't have a place to manifest.

## When to migrate

Chapter 25's closing recommendation (source: chapter-25-data-processing-pipelines.md):

> If a data processing problem is continuous or will organically grow to become continuous, don't use a periodic pipeline. Instead, use a technology with characteristics similar to [[google-workflow|Workflow]].

The signal that triggers the migration is usually business demand for continuously-updated results that the periodic interval can no longer supply. The chapter notes the unfortunate timing — this demand usually arrives at the least convenient moment to refactor, often paired with new feature requirements and immovable deadlines. The chapter's preventive recommendation is to scope **expected growth trajectory, design-modification demand, additional resources, and latency requirements at the outset** so the architectural choice is made before the periodic pipeline becomes load-bearing.

## Related concepts in the wiki

- [[batch-processing]] (Kleppmann) — the broader family of which periodic pipelines are an instance; the immutable-input/replaceable-output principles apply, but Chapter 25 names the operational fragility Kleppmann's algorithmic treatment leaves implicit
- [[mapreduce]] (Dean / Kleppmann) — the framework most periodic pipelines at Google are written in; named explicitly in Chapter 25 alongside Flume
- [[dataflow-engines]] (Spark, Flink) — the modern open-source successors to MapReduce; partially address some of the chapter's failure modes (in-memory pipelining cuts hanging-chunk severity) but still operate on a job-submission model
- [[continuous-data-processing]] — the architectural alternative the chapter recommends
- [[google-workflow]] — Google's specific implementation of continuous data processing
- [[cron-thundering-herd]] (SRE Ch 24) — the cron-level analogue of [[pipeline-thundering-herd]]; same synchronisation-based failure mode at a different layer

## Related pages

- [[data-processing-pipelines]]
- [[pipeline-uneven-work-distribution]]
- [[pipeline-batch-scheduling-drawbacks]]
- [[pipeline-monitoring-problems]]
- [[pipeline-thundering-herd]]
- [[moire-load-pattern]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[cron-thundering-herd]]
