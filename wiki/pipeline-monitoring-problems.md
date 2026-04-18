# Pipeline Monitoring Problems

**Summary**: For [[periodic-pipeline|periodic pipelines]] of nontrivial duration, **real-time** runtime metrics are as important as overall metrics — they are the only signal an operator has during emergency response. The standard pattern of collecting metrics during a job and reporting only at completion produces a structural blind spot: if the job fails or hangs mid-run, no statistics are produced, and the operator is debugging blind. Continuous pipelines do not share this problem, because their tasks are constantly running and their telemetry is naturally real-time.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The structural blind spot

Chapter 25 names this directly (source: chapter-25-data-processing-pipelines.md):

> The standard monitoring model involves collecting metrics during job execution, and reporting metrics only upon completion. If the job fails during execution, no statistics are provided.

For pipelines whose execution duration is long enough that operators care what's happening during the run — i.e., almost any non-trivial periodic pipeline — this pattern is structurally inadequate. The very situations operators most need visibility for (job hanging, failing, behaving anomalously) are exactly the situations where the completion-time metric report never fires.

The chapter's qualifier is honest: periodic pipelines **shouldn't** have inherent monitoring problems — there is nothing about the periodic model that prevents real-time telemetry — but the chapter notes "we have observed a strong association." The pattern emerges because periodic pipelines are typically built around discrete-job frameworks ([[mapreduce]], Flume) whose default monitoring model is "report when done."

## Why continuous pipelines escape this

Continuous pipelines (the [[google-workflow|Workflow]] design Chapter 25 advocates) have constantly-running tasks. Their telemetry is naturally designed for real-time exposure because there's no terminal "completion" event to defer reporting to:

- Workers expose [[varz-endpoints|`/varz`]]-style metrics that [[borgmon|Borgmon]] scrapes continuously.
- Per-stage throughput, error rates, and queue depths are visible at any moment.
- The operator's mental model — "what is the system doing right now" — matches the telemetry's reporting model.

This is one of several places where continuous pipelines are not just a different point on a frequency spectrum from periodic pipelines, but a structurally different shape that solves operational problems by construction.

## Why this matters operationally

The monitoring blind spot interacts with the other periodic-pipeline failure modes:

- A [[pipeline-uneven-work-distribution|hanging chunk]] looks identical to a slow-but-progressing job from the outside if no per-chunk progress metric is exposed. The operator cannot distinguish "running" from "stuck" without inside visibility.
- The [[pipeline-thundering-herd|thundering herd]] is hard to diagnose retrospectively if the failed cycle never produced metrics; you see "the job failed" and not "the job spawned 10× the expected workers and saturated the network."
- A [[moire-load-pattern|Moiré load pattern]] only shows up in plots of resource usage over time across multiple pipelines. If each pipeline's metrics only appear at end-of-cycle, the time alignment that exposes the pattern is missing.

Adding real-time metrics to a periodic pipeline is possible but does not address the underlying problems — it just makes some of them easier to diagnose after the fact. The architectural answer the chapter prefers is to switch to a continuous model.

## Cross-references

- [[four-golden-signals]] (SRE Ch 6) — the canonical metric set is designed for continuously-running services; mapping it onto periodic batch jobs is awkward, which is part of why periodic-pipeline monitoring tends to be poor
- [[symptoms-vs-causes]] (SRE Ch 6) — without real-time metrics, the operator is stuck at "the job didn't finish" (a coarse symptom) with no way to drill into the cause
- [[black-box-vs-white-box-monitoring]] (SRE Ch 6) — periodic pipelines force operators into pure black-box monitoring (did the output appear, was it correct), because the white-box signals the workers exposed are gone with the workers themselves
- [[varz-endpoints]] / [[borgmon]] (SRE Ch 10) — Google's monitoring stack is built around continuously-running binaries that expose metrics on a known endpoint; periodic pipelines fit this model badly because the endpoint goes away when the cycle ends
- [[consumer-lag-monitoring]] (Bellemare) — the continuous-streaming equivalent: a long-running consumer's lag metric is always available, which is why streaming systems naturally have better operational visibility than periodic batch chains

## Related pages

- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[pipeline-uneven-work-distribution]]
- [[pipeline-thundering-herd]]
- [[moire-load-pattern]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[four-golden-signals]]
- [[varz-endpoints]]
- [[borgmon]]
