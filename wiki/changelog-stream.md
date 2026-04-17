# Changelog Stream

**Summary**: A broker-backed **record of every change made to a [[state-store]]** — the stream half of the [[table-stream-duality]] applied to a microservice's own state. Changelogs turn volatile local state into durable, replayable state: a crashed instance is rebuilt by replaying its partitions' changelogs, and newly-scaled instances bootstrap the same way without re-running the original input through business logic.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## What goes on it

Every mutation to the state store — every put, every delete — is produced as an event to a corresponding **compacted** topic in the [[event-broker]]. The event key is the state-store key; the value is the new state (or a [[tombstone]] for deletion). The stream is [[log-compaction|compacted]] because only the most recent value per key is needed to rebuild state (source: chapter-07-stateful-streaming.md).

A changelog is stored in the broker like any other stream. It has partitions, retention, and offsets; consumers (specifically, the microservice's own recovery/bootstrap code) read from it the same way they read anything else.

## Who writes one

Changelogs are either:

- **Provided by the client framework.** [[lightweight-framework-microservice|Lightweight frameworks]] — Kafka Streams and Samza embedded — write a changelog for every state store automatically. The changelog is the lightweight model's **durability substrate** (source: chapter-07-stateful-streaming.md, chapter-12-lightweight-framework-microservices.md) — the analogue of [[checkpointing-stream-processing|checkpoints]] in the heavyweight model, but carried by the broker itself rather than by external snapshot storage.
- **Implemented by the developer.** Basic producer/consumer clients offer no stateful machinery; the application code must publish every state-store mutation to a changelog topic itself.

If you're writing a stateful EDM with bare producer/consumer clients and no changelog, recovery is going to be painful.

## Why compaction

A changelog exists to answer the question "what is the current state?" — not "how did we get here?". Old values for a key are wasted bytes after a new value is written. Running the broker's compaction job drops all but the latest value per key and shrinks the changelog toward the size of the live state (source: chapter-07-stateful-streaming.md). This is the same mechanism that keeps [[entity-event]] streams small; see [[log-compaction]].

## What recovery looks like

When an instance fails or a new one is added, its assigned stateful partitions are rebuilt before any new input events are processed (source: chapter-07-stateful-streaming.md):

1. The instance joins the [[consumer-group]] and is assigned partitions.
2. For each stateful partition, it consumes the corresponding changelog partition from offset 0 up to the latest offset.
3. The state store is repopulated from those events.
4. Only then does the instance begin consuming new input events.

Because the changelog stores the *result* of prior processing, recovery via changelog is far faster than recovery via input-stream replay — there is no business-logic work to re-do, only a sequence of writes to re-apply (source: chapter-07-stateful-streaming.md).

## Changelog vs input-stream rebuild

When no changelog exists, the fallback is to rebuild from the input streams: reset consumer offsets to 0, consume every input event, and let the business logic rebuild state by processing each event (source: chapter-07-stateful-streaming.md). Two big costs:

- **Time.** Every input event is reprocessed, not just every state mutation. For a service that filters heavily, this is wasted work.
- **Duplicate outputs.** The business logic re-emits output events as it rebuilds. Downstream consumers must dedupe or otherwise tolerate replay; see [[idempotence]] and [[reprocessing-event-streams]].

Chapter 7's verdict: input-stream rebuild is only viable "for simple topologies where duplicate output is not a concern, input event stream retention is short, and the entity event streams are sparse" (source: chapter-07-stateful-streaming.md).

## Use in effectively-once transactions

In a [[effectively-once-processing|client-broker transactional]] model (Kafka), the changelog writes, the input consumer-offset commit, and any output events are all wrapped in a single broker-level atomic transaction (source: chapter-07-stateful-streaming.md). A failed transaction rolls all three back together; on recovery the instance rebuilds from the last good changelog + offsets.

## Relationship to the wiki

- **[[table-stream-duality]]** — the general pattern; changelog is the "stream" direction applied to the service's own state.
- **[[log-compaction]]** — why the changelog stays small.
- **[[tombstone]]** — how deletes are represented on the changelog.
- **[[state-store]]**, **[[internal-state-store]]**, **[[external-state-store]]** — the table side of the duality.
- **[[stream-processing-fault-tolerance]]** — Kleppmann's "state change replication" row is this pattern as applied in Kafka Streams and Samza.

## Related pages

- [[state-store]]
- [[internal-state-store]]
- [[external-state-store]]
- [[stateful-stream-processing]]
- [[table-stream-duality]]
- [[log-compaction]]
- [[tombstone]]
- [[effectively-once-processing]]
- [[event-broker]]
- [[reprocessing-event-streams]]
- [[stream-processing-fault-tolerance]]
- [[lightweight-framework-microservice]]
- [[checkpointing-stream-processing]]
