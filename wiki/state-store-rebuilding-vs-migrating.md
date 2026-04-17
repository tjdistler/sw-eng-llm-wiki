# State Store Rebuilding vs Migrating

**Summary**: When a stateful microservice's schema or business logic changes, the existing [[state-store]] must catch up. Two strategies: **rebuild** from scratch by replaying the input streams with the new code, or **migrate** the existing data in place. Rebuilding is simpler and always correct; migrating is cheaper for large stores but error-prone and hard to verify. Bellemare treats rebuilding as the default and reserves migration for narrow cases where reprocessing cost is prohibitive.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## Why this comes up

Business requirements change. A new output field is added; a new join is introduced; a derived aggregate is recomputed differently. In all these cases, the state store's schema or contents need to reflect the new logic, and the service must decide: throw the old state away and rebuild it, or transform the old state in place (source: chapter-07-stateful-streaming.md).

## Rebuilding

The default and "typically the most common method of updating the internal state" (source: chapter-07-stateful-streaming.md). Steps:

1. Stop the microservice.
2. Reset consumer input offsets to 0.
3. Delete intermediate state: the local state store, the [[changelog-stream]], and any external store data.
4. Deploy the new version.
5. Consume the inputs from the beginning; let the new business logic rebuild state as it processes.

### Properties

- **Correct by construction.** State is exactly what the new logic says it should be, because the new logic produced it.
- **New output events are emitted.** These are not considered duplicates — the schema and business logic may have changed, and downstream consumers need the new output.
- **Requires that input history still exists.** If a source stream has short retention and important early events have been deleted, rebuilding is not an option.
- **Takes time.** Account for rebuild duration in the microservice's SLA.

A useful side benefit: periodic rebuilds are a **disaster-recovery drill**. Running through the full recovery path regularly keeps the process tested (source: chapter-07-stateful-streaming.md).

### When rebuilding is the *only* option

Some business requirements require reprocessing from the beginning of time — e.g., when a new field must be extracted from historical input events that was not previously captured. The data simply isn't anywhere else, so you have to replay the inputs, which means rebuilding state (source: chapter-07-stateful-streaming.md).

## Migrating

Migrating transforms the existing state store in place rather than rebuilding it. Use case: the change is small and the rebuild cost is large.

### The easy case

Bellemare's example: adding an optional field to an output event. For a state store backed by a relational database, this is:

- `ALTER TABLE ADD COLUMN new_field TYPE NULL DEFAULT NULL;`
- Deploy the new code that populates the column on new events.
- Old rows have `NULL`; new rows have the new field.

No historical reprocessing needed if the business is fine with the new logic applying only to new events (source: chapter-07-stateful-streaming.md).

### The hard case

Complex migrations require transformation logic that is **not** part of the business logic of the service. This is the danger:

- The migration code and the business code are different; they can drift.
- Migration bugs can produce inconsistencies that a full rebuild would never introduce.
- Errors are hard to detect without a rebuild to compare against.

Bellemare's guidance: "when following a migration-based approach, be sure to perform strict testing and use representative test data sets to compare that approach with a rebuild-based one" (source: chapter-07-stateful-streaming.md). If you can't afford a full rebuild to verify the migration produced correct state, you probably shouldn't trust the migration.

## Choosing

A rough decision rule:

| Condition | Prefer |
|---|---|
| Schema change is additive (new nullable column/field) | Migrate |
| Business logic has changed materially | Rebuild |
| Input retention insufficient for rebuild | Migrate (you have no choice — but your input retention strategy is the real problem) |
| State store is small; rebuild fits in SLA | Rebuild |
| State store is huge; full reprocessing is hours/days | Migrate, with very careful testing |
| Verification is critical | Rebuild |

## Related pages

- [[state-store]]
- [[internal-state-store]]
- [[external-state-store]]
- [[changelog-stream]]
- [[stateful-stream-processing]]
- [[reprocessing-event-streams]]
- [[schema-evolution]]
