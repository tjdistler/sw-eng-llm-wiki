# Filter Pattern

**Summary**: The second of Burns's five linking patterns for [[event-driven-batch-pattern|event-driven batch workflows]]. A **filter** reduces a stream of work items to a smaller stream by dropping items that do not meet some criterion. Burns's canonical implementation is a [[source-container-interface|source ambassador]] that wraps an upstream source and applies the predicate transparently — the downstream work queue never sees the filtered-out items.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

A filter evaluates a predicate on each item and passes only the items that match (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Items that don't meet the criterion are **dropped on the floor** — Burns's phrase. They don't go to another queue; they simply disappear from the workflow.

## Worked example: opt-in new users

Burns's example is a batch workflow that handles new user signups (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Some fraction of new users tick the checkbox opting in to promotional emails; the downstream email-send queue should only process that subset.

A filter sits between "all new signups" and "send promotional email": evaluate the opt-in flag, pass the opted-in users through, drop the rest.

## The ambassador-shaped implementation

Burns's preferred implementation: compose the filter as a [[source-container-interface|source ambassador]] that wraps an existing source container (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

```
[ upstream source ]  -- full list of items -->
       |
       v
[ filter ambassador ]  -- apply predicate -->
       |
       v
[ work-queue manager ]  -- only matching items -->
```

"The original source container provides the complete list of items to be worked on, and the filter container then adjusts that list based on the filter criteria and only returns those filtered results to the work queue infrastructure" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

Two virtues of this implementation:

1. **The downstream queue is unchanged** — it runs the same generic queue-manager, talks to the same `GET /api/v1/items` interface on `localhost`, and has no idea the items have been filtered.
2. **The filter is reusable** — stack it in front of any source container to produce a filtered variant of that source.

This is a textbook [[ambassador-pattern]] composition: one ambassador in front of another, each doing a narrow job.

## Relationship to splitter

A [[splitter-pattern|splitter]] is a filter that *keeps* the dropped items — instead of discarding, it routes them to a different queue (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Use a filter when the rejected items have no downstream meaning; use a splitter when they do.

Burns notes that a splitter can be simulated by a [[copier-pattern|copier]] plus two filters (one keeping items that match, one keeping items that don't), but the splitter is a "more compact representation that captures the job of the splitter more succinctly" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

## Unix analogy

A filter is `grep`. The [[unix-philosophy]] point that filtering is one of the primitive shell operations applies directly: Burns's filter is the container-level `grep` for batch pipelines.

## Related pages

- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[source-container-interface]]
- [[ambassador-pattern]]
- [[work-queue-pattern]]
- [[unix-philosophy]]
- [[designing-distributed-systems]]
