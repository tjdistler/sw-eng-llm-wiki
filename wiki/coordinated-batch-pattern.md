# Coordinated Batch Pattern

**Summary**: The third and final of Burns's batch computational patterns and the hub for Chapter 12. Where the [[work-queue-pattern|work queue]] dispatches independent items to workers and the [[event-driven-batch-pattern|event-driven batch]] chains queues into workflows, **coordinated batch processing** pulls the parallel outputs of those workflows **back together** into a single aggregate result. Burns covers two distinct coordination primitives — the [[join-pattern|join]] (barrier synchronization; wait for everything before continuing) and the [[reduce-pattern|reduce]] (optimistic streaming combine of partial outputs into one) — and illustrates their composition in an image-tagging pipeline that reuses every linking pattern from Chapter 11.

**Sources**: `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## Why coordination

Chapter 11's linking patterns ([[copier-pattern|copier]], [[filter-pattern|filter]], [[splitter-pattern|splitter]], [[sharder-pattern|sharder]], [[merger-pattern|merger]]) excel at **splitting** work and chaining it through a DAG, but they do not close the loop: "Duplicating and producing multiple different outputs is often an important part of batch processing, but sometimes it is equally important to pull multiple outputs back together in order to generate some sort of aggregate output" (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md).

Burns's motivating observation is that the MapReduce pattern itself is an instance of exactly this shape: "It's easy to see that the map step is an example of sharding a work queue, and the reduce step is an example of coordinated processing that eventually reduces a large number of outputs down to a single aggregate response" (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). Chapter 12 names and generalises the aggregate side of that pairing.

## Two primitives

Burns treats two coordination primitives as substantively distinct (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

| Primitive | Semantics | Starts when? | Typical use |
|---|---|---|---|
| [[join-pattern]] | Barrier: wait for **every** upstream item to complete | After the slowest upstream worker finishes | Guarantee completeness before aggregation; fence a destructive step |
| [[reduce-pattern]] | Optimistic: combine any two (or more) partial results into one | As soon as two outputs exist | Streaming aggregation where the combine is associative |

The join blocks the workflow; the reduce pipelines through it. They solve different problems and are often composed in the same pipeline.

## Contrast with the merger pattern

The [[merger-pattern|merger]] from Chapter 11 also takes N inputs and produces one output, but it is **not** a coordination primitive: "merge simply blends the output of two work queues into a single work queue for additional processing... it does not ensure that a complete dataset is present prior to the beginning of processing" (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md).

A merger is a concatenation; items flow through as they arrive, preserving no completeness guarantee and computing no aggregate. A join **holds** items until every parallel path has finished. A reduce **combines** items pairwise into a compressed representation. The three patterns all have an N-to-fewer shape and it is worth naming the distinction explicitly:

| Pattern | Shape | Completeness guarantee | Combines values? |
|---|---|---|---|
| [[merger-pattern]] | N → 1 stream | No | No — items pass through |
| [[join-pattern]] | N → 1 barrier | Yes | No — items pass through after wait |
| [[reduce-pattern]] | N → 1 value | Eventually (when last input drains) | Yes — values are combined |

## Worked example: image tagging and processing

Burns's chapter-length worked example composes Chapter 10, Chapter 11, and Chapter 12 patterns end-to-end (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). The job: take a set of highway images, blur the license plates, count cars/trucks/motorcycles, and build a color distribution.

1. **Stage 1 — license-plate blurring (sharded).** The [[sharder-pattern|sharder]] spreads images across multiple worker queues. Each queue runs a [[multi-worker-pattern|multi-worker]] pod containing a detector container and a reusable blurrer container — keeping the blurrer separable so it can be reused against other objects (faces, etc).
2. **Stage 2 — join before deletion.** A [[join-pattern|join]] holds all blurred images until every shard has finished. Only after the join releases does the pipeline delete the originals, guarding against partial failure that would leave some originals already deleted before their blurred copies exist.
3. **Stage 3 — copier fans out the post-join stream.** A [[copier-pattern|copier]] duplicates the verified-blurred events into two queues: one deletes the original images, one kicks off vehicle detection.
4. **Stage 4 — sharded vehicle classification.** Another [[sharder-pattern|sharder]] spreads the recognition work across worker queues. Each queue is a [[multi-worker-pattern|multi-worker]] pod — a vehicle-identifier container plus a color-identifier container — again composed for reuse.
5. **Stage 5 — reduce aggregates the JSON tuples.** Each worker produces a per-image JSON count; a [[reduce-pattern|reduce]] combines them pairwise until a single aggregate remains, giving the final counts of vehicles and colors across the entire dataset.

Reading the graph is a compact specification of the whole pipeline, which is the same topology-as-specification payoff Burns highlights in [[event-pipeline-pattern|Chapter 8's FaaS event pipelines]] and [[event-driven-batch-pattern|Chapter 11's event-driven batch workflows]].

## Relationship to MapReduce

[[mapreduce|MapReduce]] is the archetype of the Burns coordinated-batch shape: a sharded map stage (parallel work distribution) feeds a shuffled reduce stage (coordinated aggregation). In Burns's vocabulary (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

| MapReduce step | Burns pattern |
|---|---|
| Input split + map task scheduling | [[work-queue-pattern]] |
| Partition-by-key / shuffle | [[sharder-pattern]] |
| Reduce | [[reduce-pattern]] |
| "Wait for all mappers before reducing" semantics (when needed) | [[join-pattern]] |

MapReduce requires the full map phase to finish before reducers start, which is effectively a join; dataflow engines like Spark and Flink relax that barrier where the reduce is associative enough to pipeline — which is what Burns's distinction between join (barrier) and reduce (streaming) captures at the pattern level.

## Relationship to DDIA batch coverage

This chapter closes the loop between Burns's container-level batch trilogy (Chapters 10–12) and DDIA's batch-processing theory (Chapter 10 of DDIA):

- [[mapreduce]] — the canonical sharder + reduce composition, now explicitly named at container granularity.
- [[sort-merge-joins]] — DDIA's reduce-side join uses the shuffle to bring related records to the same reducer, then the reducer *does* a join in the SQL sense. That is a different meaning of "join" than Burns's Chapter 12 barrier-synchronization join; the DDIA join is a relational operator, the Burns join is a completeness fence. Both use the name because both "bring parallel work together," but the mechanism differs.
- [[dataflow-engines]] — Spark/Flink/Tez generalise the sharder + join + reduce composition into arbitrary DAGs with operator-level choices about where to materialise and where to pipeline. Burns's pattern-level distinction between join and reduce is the coarse-grained form of the dataflow engine's operator-level choice.
- [[batch-processing]] — the DDIA hub page; coordinated batch processing is the container-level companion to the DDIA shuffle-and-aggregate treatment.

## When the pattern fits

Coordinated batch processing is the right pattern when:

- A workflow splits work across many parallel workers and the end product needs to combine their outputs.
- The aggregation is associative (for [[reduce-pattern|reduce]]) or the downstream step must not start until every upstream path has finished (for [[join-pattern|join]]).
- A simple [[merger-pattern|merger]] does not suffice because completeness or aggregation is required.

It does not fit when:

- Work items are genuinely independent and no aggregate is needed — use a plain [[work-queue-pattern]].
- The workflow is purely a split/transform DAG with no need to combine outputs — [[event-driven-batch-pattern|Chapter 11's linking patterns]] alone are enough.
- The aggregation is complex enough to warrant a real analytic engine — use [[mapreduce]] or [[dataflow-engines]] directly.

## Related pages

- [[join-pattern]]
- [[reduce-pattern]]
- [[merger-pattern]]
- [[sharder-pattern]]
- [[copier-pattern]]
- [[multi-worker-pattern]]
- [[work-queue-pattern]]
- [[event-driven-batch-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[mapreduce]]
- [[sort-merge-joins]]
- [[dataflow-engines]]
- [[batch-processing]]
- [[adapter-pattern]]
- [[ambassador-pattern]]
- [[designing-distributed-systems]]
