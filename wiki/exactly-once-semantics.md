# Exactly-Once Semantics

**Summary**: Arranging a computation so that the final effect is the same as if no faults had occurred, even if operations were retried due to failures -- achieved primarily through idempotence and end-to-end operation identifiers rather than through infrastructure-level guarantees alone.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The problem

When processing fails partway through, you have two choices: drop the message (data loss) or retry. Retrying risks duplicate processing -- charging a customer twice, incrementing a counter twice, or otherwise corrupting data. **Exactly-once** (or **effectively-once**) semantics means the final result is the same as if each operation executed exactly once, even if retries occurred (source: chapter-12-the-future-of-data-systems.md).

## Idempotence

The most effective approach is making operations **idempotent**: ensuring the same effect whether executed once or multiple times. Making a non-idempotent operation idempotent requires (source: chapter-12-the-future-of-data-systems.md):

- Maintaining additional metadata (e.g., the set of operation IDs that have already been applied)
- Ensuring proper [[fencing-tokens|fencing]] when failing over between nodes

## Why infrastructure-level deduplication is insufficient

Deduplication mechanisms operate at different layers, and none covers the full end-to-end path (source: chapter-12-the-future-of-data-systems.md):

| Layer | Mechanism | Scope |
|---|---|---|
| Network | TCP sequence numbers | Single TCP connection |
| Database | Transaction semantics | Single database operation |
| Stream processor | Checkpoint-based recovery | Single processing stage |
| End-to-end | Application operation IDs | Full request lifecycle |

A client that loses its TCP connection and reconnects is outside TCP's deduplication scope. A user who retries an HTTP POST after a timeout is outside the database transaction's deduplication scope. Only end-to-end operation identifiers cover all hops. See [[end-to-end-argument]] (source: chapter-12-the-future-of-data-systems.md).

## Operation identifiers in practice

To achieve end-to-end exactly-once processing (source: chapter-12-the-future-of-data-systems.md):

1. Generate a unique identifier (UUID) at the client.
2. Include it in every request (e.g., as a hidden form field).
3. Pass it through all processing stages to the database.
4. Use a uniqueness constraint to reject duplicates.

The request record with a unique ID serves as both a deduplication mechanism and an event log. The actual state updates (e.g., balance changes) can be derived from this event asynchronously, as long as each event is processed exactly once (source: chapter-12-the-future-of-data-systems.md).

## Multi-partition exactly-once

For operations spanning multiple partitions (e.g., transferring money between two accounts), equivalent correctness can be achieved without [[distributed-transactions|atomic commit]] across partitions (source: chapter-12-the-future-of-data-systems.md):

1. The client assigns a unique request ID and appends the request to a log partition based on that ID.
2. A stream processor reads the request and emits separate debit and credit instructions to output streams, partitioned by account.
3. Downstream processors deduplicate by request ID and apply the changes.

This avoids [[two-phase-commit]] entirely. Single-object writes are atomic in almost all systems, so the request either appears in the log or it doesn't. Deterministic processing means duplicate instructions are identical and easily deduplicated (source: chapter-12-the-future-of-data-systems.md).

## Workflow as a structural alternative (SRE Ch 25)

Google's [[google-workflow|Workflow]] system, described in SRE Chapter 25 (Dan Dennison), achieves exactly-once semantics by a **structural** rather than defensive route (source: raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md). Instead of "at-least-once + idempotent handlers + end-to-end operation IDs," Workflow's [[workflow-correctness-guarantees|four guarantees]] make exactly-once a property of the substrate:

1. **Configuration tasks act as barriers** — workers can only commit if their result references the current configuration's task ID.
2. **Lease-bound commits** — only the current lease holder can commit; orphaned workers' commits are rejected.
3. **Unique output filenames** — orphaned workers and valid workers write to distinct files, so the orphan's output is unreferenced and harmless.
4. **Server-token validation** — every operation checks that it is talking to the expected Task Master, defending against load-balancer misconfiguration and address collision.

Critically, **Workflow does not require the application code to be idempotent**. Correctness comes from the substrate enforcing the four guarantees on every operation. This is the opposite design choice from Kleppmann's recommendation of "make operations idempotent" — both reach the same correctness destination, but by different paths and with different requirements on the surrounding ecosystem.

The trade-off:

| Aspect | Idempotence + operation IDs | Workflow's structural guarantees |
|---|---|---|
| Substrate requirement | General databases / brokers | Specialised Task Master with unique-and-immutable tasks |
| Application code requirement | All handlers must be idempotent | None |
| End-to-end operation IDs needed | Yes, for cross-stage dedup | No — leases serve the same role internally |
| Suitable for heterogeneous systems | Yes | No — limited to inside the Workflow boundary |
| Lineage | Open-source (Kafka, Flink, application code) | Google internal (2003) |

The two approaches are complementary. End-to-end operation IDs are still useful for crossing the boundary into Workflow from external systems (HTTP requests, third-party APIs); inside the Workflow boundary, the structural guarantees do the work.

## Integrity through exactly-once processing

Reliable exactly-once processing preserves [[timeliness-and-integrity|integrity]] in asynchronous [[derived-data|derived data]] systems through a combination of (source: chapter-12-the-future-of-data-systems.md):

- Representing writes as single, atomically written messages (aligns with [[event-sourcing]])
- Deriving all state updates from that single message using deterministic functions
- Passing client-generated request IDs through all levels for end-to-end deduplication
- Making messages immutable and allowing reprocessing to recover from bugs

## Related pages

- [[idempotence]]
- [[end-to-end-argument]]
- [[timeliness-and-integrity]]
- [[coordination-avoidance]]
- [[derived-data]]
- [[transactions]]
- [[distributed-transactions]]
- [[two-phase-commit]]
- [[event-sourcing]]
- [[fencing-tokens]]
- [[stream-processing]]
- [[google-workflow]]
- [[workflow-correctness-guarantees]]
- [[task-master]]
- [[continuous-data-processing]]
- [[data-processing-pipelines]]
