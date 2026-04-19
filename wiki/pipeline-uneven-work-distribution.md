# Pipeline Uneven Work Distribution

**Summary**: The first named failure mode of [[periodic-pipeline|periodic pipelines]]: Big Data techniques rely on splitting a workload into chunks small enough to fit on individual machines, but real-world chunks rarely have uniform resource needs. The slowest chunk caps end-to-end runtime — the **hanging chunk problem** — and the standard "kill and restart" response wastes all completed work because periodic pipelines typically have no checkpointing.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## Why chunks are uneven

The breakthrough enabling Big Data is the application of **embarrassingly-parallel algorithms** that cut a workload into chunks small enough to fit on individual machines (source: chapter-25-data-processing-pipelines.md). The implicit assumption is that chunks have roughly comparable resource requirements. In practice, chunks vary in size and cost for reasons that are often non-obvious at design time:

- The natural partitioning key (often a customer ID) produces wildly different chunk sizes — a few customers may dominate the data volume.
- Real-time operations on streams (e.g., sorting "steaming" data) require all data to be present before the next stage can begin.
- Different machines in a cluster have different real-world performance characteristics.
- A job that is overallocated resources may have its largest chunks sized too aggressively for the actual machines they land on.

When the partitioning key is the **point of indivisibility** — say, "customer" in a customer-keyed workload — end-to-end runtime is capped by the runtime of the largest chunk. There is no algorithmic way to split a single customer's chunk further without changing the join semantics.

## The hanging chunk problem

The chapter names this failure mode the **hanging chunk problem** (source: chapter-25-data-processing-pipelines.md). The pattern:

- N − 1 chunks complete in approximately the expected time.
- One chunk is much larger or runs on a slower machine — it hangs.
- The next pipeline stage cannot start because its inputs are not ready (typical user code waits for the total computation to complete before progressing, often because a sort step requires all data).
- Pipeline completion time is dictated by the worst-case chunk.

Resource overallocation makes this worse. A job that has been generously sized may produce chunks the worker machine cannot quite fit, causing the chunk to swap or thrash.

## Why kill-and-restart is the wrong response

When monitoring or engineers detect a hanging chunk, the "sensible" or "default" response is to kill the job and let it restart, on the assumption that the blockage may be due to nondeterministic factors (a transient slow disk, a flapping network, a noisy neighbour) (source: chapter-25-data-processing-pipelines.md).

**This response can make matters worse** because periodic pipelines are typically implemented without checkpointing. Restarting the job means restarting **all chunks from the beginning** — even the N − 1 chunks that had nearly completed are thrown away. The restart wastes:

- All the time spent on the completed chunks.
- All the CPU cycles spent computing them.
- All the human effort invested in the previous cycle.

If the underlying cause was deterministic (a chunk that genuinely is too big), the restart will hang on the same chunk again. The failure mode is now infinite rather than merely slow.

## Why no checkpointing is the norm

Chapter 25 does not develop a deep argument for why periodic pipelines lack checkpointing, but the implicit reasoning is that pipelines built around the "schedule, run, terminate" cycle naturally treat each run as atomic. Adding checkpointing means:

- Defining what a recoverable intermediate state looks like for every stage.
- Storing it durably between runs (or between attempts within a run).
- Coping with the schema/code changes that necessarily happen across runs of a long-lived pipeline.

The architectural answer the chapter prefers is to abandon the periodic model entirely. In [[google-workflow|Workflow]], every task carries a lease, every output file is uniquely named, and the lease/file machinery doubles as natural checkpointing — orphaned workers cannot destroy committed work, and a failed worker's partial output never corrupts the pipeline. See [[workflow-correctness-guarantees]].

## Why monitoring tends to make this worse

Two further amplifiers come from the operational layer:

- The hanging-chunk symptom looks generic. Without per-chunk metrics it is hard to tell whether the cause is a single chunk that's too big, a single machine that's too slow, or a systemic issue. See [[pipeline-monitoring-problems]] for the broader monitoring blindness of periodic pipelines.
- Engineers under deadline pressure often "fix" hanging chunks by adding more workers, which doesn't help (the largest chunk still runs on one machine) and worsens the [[pipeline-thundering-herd|thundering herd]] for the next cycle.

## Cross-references

- [[bimodal-latency]] (SRE Ch 22) — the same general phenomenon at the request-handling layer: a small fraction of unservable work consumes resources for a long time and starves the rest. The hanging chunk is a stuck-work problem; bimodal latency is a stuck-request problem; both require visibility into the *distribution* of completion times rather than the mean
- [[hot-spots]] (Kleppmann) — Kleppmann's hot-spot mitigations (key salting, dynamic splitting) are the database-level analogue of fixing uneven chunks at the partitioning layer
- Straggler mitigation in MapReduce (Kleppmann Ch 10) — Hadoop's speculative-execution feature launches duplicate copies of straggler tasks; partial answer to the hanging chunk problem at the framework level
- [[work-queue-pattern]] (Burns) — Burns's batch pattern explicitly relies on Kubernetes Jobs as the durable per-item state, which gives natural per-chunk recovery; the periodic-pipeline pattern Chapter 25 critiques is what you get when this discipline is absent

## Related pages

- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[pipeline-monitoring-problems]]
- [[pipeline-thundering-herd]]
- [[google-workflow]]
- [[workflow-correctness-guarantees]]
- [[bimodal-latency]]
- [[hot-spots]]
