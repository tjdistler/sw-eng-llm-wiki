# Breaking Schema Deployment

**Summary**: The deployment shape required when a [[schema-evolution|schema]] change is genuinely breaking — the [[event-structure|event definition]] changes in a way that no compatibility rule can absorb. Two concrete migration strategies: **eventual migration via two event streams** (producer writes both formats; consumers migrate over time) and **synchronized migration** (producer switches wholesale; all consumers must have moved already). The mechanics are simple; the hard part is coordinating the renegotiation of the [[data-contract]] with every consumer.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why this is a separate pattern

A breaking schema change violates at least one prerequisite of the [[rolling-update-pattern]] and usually produces incorrect results under [[basic-full-stop-deployment]] unless downstream consumers also upgrade. Bellemare treats it as its own deployment pattern because the **coordination** dominates the technical work (source: chapter-16-deploying-event-driven-microservices.md).

> "Deploying a breaking schema change is a fairly straightforward technical process. The difficult part is renegotiating the schema definition, communicating that with stakeholders, and coordinating deployment and migration plans."

This is the deployment-time execution of [[breaking-changes|Newman's and Bellemare's breaking-changes guidance]] — the rules decide *that* you break; this page is about *how* you ship the break.

## Entity events vs non-entity events

The impact differs sharply (source: chapter-16-deploying-event-driven-microservices.md):

- **[[entity-event|Entity]] streams** must be **re-created under the new schema**, because consumers rematerialize from source. Reprocessing is required — either from the producer's batch source or its own input streams.
- **Non-entity events** often don't need reprocessing. Consumers can add the new event type as a new stream and modify business logic to handle both; old events drain out of the old stream as retention elapses, and the old stream can then be dropped.

This is the same entity-vs-event split that pervades [[breaking-changes]]; Chapter 16 makes it operational.

## Producer options for re-creating entities

Two shapes (source: chapter-16-deploying-event-driven-microservices.md):

- **Single producer** — extend the existing producer with logic to re-create events in the new schema from the source. Keeps all logic in one service.
- **New producer alongside** — build and deploy a second producer for the new stream. The original continues untouched, minimizing impact on its existing downstream consumers.

## Strategy 1: Eventual migration via two event streams

The producer writes events in **both** the old and new formats, each to its own stream. The old stream is **marked deprecated** via [[event-stream-metadata]] tags. Consumers migrate in their own time. Once all have migrated, the old stream is removed or archived.

Assumptions (source: chapter-16-deploying-event-driven-microservices.md):

- The producer has enough data to emit both formats.
- The domain change is small enough that a 1:1 old→new mapping still makes sense.
- Eventual inconsistency (consumers on different versions) is tolerable.

Risk: **the migration never finishes**. Similar-yet-different streams remain indefinitely; new services may register on the deprecated stream by mistake. Mitigations:

- **Metadata tagging** streams as deprecated.
- Small, explicit **migration windows** with owners and dates.

## Strategy 2: Synchronized migration to the new stream

The producer is updated to emit **only** the new format on a new stream and to stop producing to the old one. Simpler technically, but requires all consumers to have migrated first (source: chapter-16-deploying-event-driven-microservices.md).

Assumptions:

- The old format is no longer usable — concurrent old+new would cause major inconsistencies.
- Downstream services must all be ready in lockstep.

Biggest risk: if a consumer fails to migrate, there is **no fallback** — the old stream is gone. Mitigation: rehearse the migration in an integration test environment using programmatically generated source data; register the producer and every consumer in that environment; run the whole migration end-to-end before doing it in production.

Bellemare's observation: synchronized migrations are rare because they require domain-level upheaval — core business entities usually have stable domain models.

## Strategy comparison

| Dimension | Eventual migration | Synchronized migration |
|---|---|---|
| Number of streams during migration | 2 | 1 (new) |
| Producer complexity | Higher (emits both) | Lower (emits new only) |
| Consumer migration timing | Independent, asynchronous | All at once |
| Fallback if a consumer isn't ready | Stay on old stream | None |
| Risk | Migration never finishes | Consumer breakage |
| Fit | Small-to-moderate domain shift | Major domain redefinition |

## Coordination checklist

Before deploying either strategy:

1. Agree the new schema with every consumer owner.
2. Agree migration timeline and cutover (eventual) or coordinated deploy window (synchronized).
3. Set up metadata tagging / deprecation signals on the old stream.
4. Ensure [[application-reset-tool]] access and [[consumer-lag-monitoring]] for anyone about to reprocess.
5. Rehearse in a transient integration environment (see [[continuous-integration-delivery-deployment]]).

## Related pages

- [[edm-deployment-principles]]
- [[edm-deployment-patterns]]
- [[breaking-changes]]
- [[schema-evolution]]
- [[data-contract]]
- [[entity-event]]
- [[event-streams]]
- [[singular-event-definition-per-stream]]
- [[reprocessing-event-streams]]
- [[application-reset-tool]]
- [[basic-full-stop-deployment]]
- [[continuous-integration-delivery-deployment]]
