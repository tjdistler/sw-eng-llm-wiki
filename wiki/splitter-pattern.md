# Splitter Pattern

**Summary**: The third of Burns's five linking patterns for [[event-driven-batch-pattern|event-driven batch workflows]]. A **splitter** routes each incoming work item to one or more downstream queues based on per-item criteria — none of the items are dropped, they are *divided* among different queues. Conceptually it is a [[filter-pattern|filter]] that keeps the rejected items instead of discarding them.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

A splitter evaluates a predicate on each item — same shape as a [[filter-pattern|filter]] — but instead of dropping the non-matching items, it routes them to a different queue (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

"Sometimes you don't want to just filter things out by dropping them on the floor, but rather you have two different kinds of input present in your set of work items and you want to divide them into two separate work queues without dropping any of them" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

The common case is a binary split — two queues — but splitters can have N branches for N categories.

## Worked example: shipping notifications

Burns's example is an order-shipping pipeline where users can opt into shipping notifications via email or text message (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The upstream queue contains shipped orders; the splitter routes them:

- Users who chose **email** → email-notification queue.
- Users who chose **text** → text-notification queue.
- Users who chose **both** → both queues (the splitter acts as a [[copier-pattern|copier]] for that item).
- Users who chose **neither** → dropped (the splitter acts as a [[filter-pattern|filter]] for that item).

This makes the splitter the most general of the routing primitives — it subsumes both copier (send to all matching branches) and filter (no branch matches, so the item is dropped).

## Relationship to copier and filter

Burns observes that a splitter can be expressed as a [[copier-pattern|copier]] followed by two [[filter-pattern|filters]] — copy every item to both queues, then have each downstream queue's source ambassador filter to only the items it should process (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The equivalence shows the primitives are not orthogonal; the splitter is a convenience shortcut:

| Pattern | Items out | Output branches |
|---|---|---|
| [[filter-pattern]] | Subset of input | 1 (plus the implicit "dropped" bucket) |
| [[copier-pattern]] | Every item, duplicated | N (all identical) |
| Splitter | Every item, each routed somewhere | N (by criterion) |
| [[sharder-pattern]] | Every item, hashed to one | N (by hash) |

Burns prefers the splitter name because it "is a more compact representation that captures the job of the splitter more succinctly" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md) — naming the pattern makes the workflow graph more readable even if the mechanical decomposition is equivalent.

## Relationship to sharder

The [[sharder-pattern]] also routes each item to one of N queues, but the routing function is a **hash** rather than a semantic predicate. Use a splitter when the branches mean different things (email vs text); use a sharder when the branches are interchangeable and you just want even distribution.

## Related pages

- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[work-queue-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[designing-distributed-systems]]
