# Application Reset Tool

**Summary**: A self-serve tool that lets the team owning a microservice wipe its offsets, internal state, and [[changelog-stream|changelog]] streams back to a clean slate — and optionally purge any external state stores it uses. Required whenever a stateful topology changes in a way that invalidates existing state; access is gated by the [[microservice-to-team-assignment]] system so only the owning team (or an admin) can trigger a reset.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The three offset operations

Operators need three distinct offset manipulations (source: chapter-14-supportive-tooling.md):

- **Reset to earliest** — reprocess from the start of the input stream. Needed after logic changes that invalidate historical outputs.
- **Advance to latest** — skip to the tail; consume only new data. Used when the service should not backfill.
- **Set to a specific point** — usually *"N minutes before a known crash"*. Common in multicluster failover where you want to replay just enough to avoid missed messages without doubling every historical event.

In all three cases only the microservice's owning team may change its offsets, enforced through [[microservice-to-team-assignment]] (source: chapter-14-supportive-tooling.md).

## Full application reset

A full reset is broader than offsets alone. When a stateful topology changes — [[internal-state-store|internal state stores]] restructured, [[changelog-stream|changelog]] layouts changed, join keys changed — the state must be rebuilt. The tool performs (source: chapter-14-supportive-tooling.md):

1. Delete the microservice's **internal streams** and [[changelog-stream|changelog streams]].
2. Delete any **[[external-state-store|external state store]]** materializations (Bigtable, DynamoDB, Cassandra tables, etc.) if they fall inside the officially-supported capability set.
3. **Reset consumer-group offsets** to earliest for each input stream.
4. Restart the service. It rebuilds state from scratch.

External stores outside the supported set must be reset manually by the team.

## Why this is gated

A reset is destructive. Mis-applied to another team's service it wipes real state and real business value. Bellemare insists: **another team must never be able to reset streams or state owned by a different team** (source: chapter-14-supportive-tooling.md). The ownership system is the gate.

## Relationship to existing wiki coverage

- **[[state-store-rebuilding-vs-migrating]]** — the reset tool is the rebuild path; the migrate path avoids the reset.
- **[[internal-state-store]] / [[external-state-store]] / [[changelog-stream]]** — the stores and streams the tool manipulates.
- **[[reprocessing-event-streams]]** — the methodology the rewind-to-earliest variant implements.
- **[[effectively-once-processing]]** — affects how cleanly a reset lands; deduplication on the output side matters if downstream consumers must not double-process.
- **[[basic-full-stop-deployment]]** — the deployment pattern whose step 4a typically invokes this tool; the [[rolling-update-pattern]] deliberately avoids needing it.

## Related pages

- [[edm-supportive-tooling]]
- [[microservice-to-team-assignment]]
- [[consumer-offset]]
- [[changelog-stream]]
- [[internal-state-store]]
- [[external-state-store]]
- [[state-store-rebuilding-vs-migrating]]
- [[reprocessing-event-streams]]
