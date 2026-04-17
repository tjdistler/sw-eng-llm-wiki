# Merger Pattern

**Summary**: The fifth and final of Burns's linking patterns for [[event-driven-batch-pattern|event-driven batch workflows]]. A **merger** is the structural opposite of a [[copier-pattern|copier]]: it combines multiple upstream work queues into a single downstream queue so one shared worker pool can drain them all. Burns implements it as a multi-source [[adapter-pattern|adapter]] — one adapter transforming several running source containers into a single merged source.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

A merger takes N upstream work queues and produces a single merged stream that a downstream queue-manager can consume (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Items arriving on any upstream source appear in the merged stream, tagged with enough context to identify their origin.

"A merger is the opposite of a copier; the job of a merger is to take two different work queues and turn them into a single work queue" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

## Worked example: shared build infrastructure

Burns's example is a CI pipeline serving many source repositories (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

> "Suppose, for example, that you have a large number of different source repositories all adding new commits at the same time. You want to take each of these commits and perform a build-and-test for it. It is not scalable to create a separate build infrastructure for each source repository."

Each repository is a separate source of commit events. Without a merger, each would need its own build workers, its own autoscaling, its own failure handling. With a merger:

1. Each repo is modelled as its own [[source-container-interface|source ambassador]], producing a per-repo stream of commits.
2. A **merger adapter** combines all those source containers into a single logical merged source.
3. The downstream build queue consumes from the merger and runs builds with one shared worker pool, one autoscaler, one dashboard.

## The multi-source adapter shape

Burns is explicit that the merger is an [[adapter-pattern|adapter]], but with a twist: "the adapter is actually adapting multiple running source containers into a single merged source" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The *input* side of the adapter is a **collection** of containers, not a single one.

This makes the merger structurally similar to the [[multi-worker-pattern]] from Chapter 10, flipped around the axis of the queue:

| Pattern | Inward | Outward |
|---|---|---|
| [[multi-worker-pattern]] (Ch 10) | Many processing containers | One worker interface |
| Merger (this page) | Many source containers | One source interface |

Both compose a set of narrow containers into a single standard interface that the rest of the work-queue machinery can consume unchanged.

## Relationship to the other linking patterns

The merger is the *fan-in* primitive. Combined with the fan-out [[copier-pattern|copier]] and the [[sharder-pattern|sharder]], it closes the loop on the workflow vocabulary — any DAG topology can be built from these primitives plus [[filter-pattern|filter]] and [[splitter-pattern|splitter]]:

| Primitive | Shape |
|---|---|
| [[copier-pattern]] | 1 → N (identical) |
| [[filter-pattern]] | 1 → 1 (smaller) |
| [[splitter-pattern]] | 1 → N (routed) |
| [[sharder-pattern]] | 1 → N (hashed) |
| Merger | N → 1 |

## Relationship to message-broker fan-in

Modern pub/sub brokers provide native fan-in — a single consumer subscription against multiple topics does exactly what a merger does (see [[publisher-subscriber-infrastructure]], [[message-brokers]]). Burns's merger pattern is the container-level *naming* of that capability in the workflow vocabulary; at implementation time, the merger is often a single broker consumer listening on multiple topics rather than a bespoke adapter container.

## Merger is not a join: the Chapter 12 distinction

Burns opens [[coordinated-batch-pattern|Chapter 12]] with an explicit contrast between the merger and the coordinated-batch [[join-pattern|join]] (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

> "While the merge pattern is sufficient in some cases, it does not ensure that a complete dataset is present prior to the beginning of processing. This means that there can be no guarantees about the completeness of the processing being performed, as well as no opportunity to compute aggregate statistics for all of the elements that have been processed."

Both patterns take N streams and produce one, but the merger lets items flow through as they arrive while the [[join-pattern|join]] holds everything until every upstream path has completed. The merger is cheap and streaming; the join is strong and blocking. When completeness matters — destructive steps, global aggregates, phase fences — reach for the join. When it doesn't, the merger is enough.

See [[coordinated-batch-pattern]] for the three-way table comparing merger, [[join-pattern|join]], and [[reduce-pattern|reduce]].

## Relationship to DDIA stream joins

At the DDIA layer, [[stream-joins]] are what happens when the merged streams need to be joined on a key rather than simply interleaved. Burns's merger is the simpler union case: items go into one bucket, each preserving its identity, no key matching required. For key-joined fan-in, a [[dataflow-engines|dataflow engine]] with stream-join operators is the more appropriate substrate.

## Related pages

- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[adapter-pattern]]
- [[multi-worker-pattern]]
- [[source-container-interface]]
- [[publisher-subscriber-infrastructure]]
- [[message-brokers]]
- [[stream-joins]]
- [[dataflow-engines]]
- [[work-queue-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[coordinated-batch-pattern]]
- [[designing-distributed-systems]]
