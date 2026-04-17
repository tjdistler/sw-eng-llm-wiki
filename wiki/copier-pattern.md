# Copier Pattern

**Summary**: The first of Burns's five linking patterns for [[event-driven-batch-pattern|event-driven batch workflows]]. A **copier** takes a single stream of work items and duplicates it into two or more identical streams, so that different downstream workers can process the same input for different purposes.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

A copier replicates each incoming work item onto every one of its output streams. Every downstream queue sees every item, with no filtering or routing (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

This is useful "when there are multiple different pieces of work to be done on the same work item" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The copier is the fan-out primitive in the workflow vocabulary.

## Worked example: video transcoding

Burns's example is a video-rendering pipeline that needs multiple output formats from each input file (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

- A 4K high-resolution format for playback from a hard drive.
- A 1080p format for digital streaming.
- A low-resolution format for mobile users on slow networks.
- An animated GIF thumbnail for a movie-picking UI.

Each rendering target is a separate [[work-queue-pattern|work queue]] with its own worker image (the format-specific ffmpeg invocation). The input to every one of them is the same video file. A copier sits at the head of the workflow: one video enters, four identical references fan out.

Without the copier pattern named, each downstream queue would need its own source ambassador pointing at the same upstream — which works, but loses the explicit fan-out node in the graph. Naming it as a copier makes the topology obvious.

## Relationship to splitter and sharder

The [[splitter-pattern]] and [[sharder-pattern]] also produce multiple output streams, but with different semantics:

| Pattern | Each item goes to | Distribution |
|---|---|---|
| Copier | **All** output streams | Duplicated |
| Splitter | **One or more** output streams, chosen by criteria | Conditional routing |
| Sharder | **Exactly one** output stream, chosen by hash | Even distribution |

Burns notes that a splitter *can* act as a copier when its criteria send the same item to multiple queues (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md) — in the shipping-notification example, a user who chose both email and SMS gets copied onto both queues.

## Relationship to merger

The [[merger-pattern]] is the structural opposite: it combines multiple streams into one. Copier fans out; merger fans in. A common workflow shape combines them: copier at the head, parallel processing, merger at the tail.

## Unix analogy

A copier is `tee`: write the same input to multiple outputs. The [[unix-philosophy]] observation that small composable operators with a uniform interface make workflows expressive applies directly — Burns's copier is the container-level form of the shell's `tee` for batch pipelines.

## Related pages

- [[event-driven-batch-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[filter-pattern]]
- [[work-queue-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[unix-philosophy]]
- [[designing-distributed-systems]]
