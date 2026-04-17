# Rolling Update Pattern

**Summary**: A zero-downtime EDM deployment pattern where instances are stopped, updated, and restarted **one at a time** rather than all at once, so a mixture of old and new logic runs during the rollout window. Works only when the change is non-breaking across three dimensions: state stores, internal [[microservice-topology|topology]], and event schemas. The most common mistake is silently breaking the internal topology and corrupting state.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The prerequisites

All three must hold (source: chapter-16-deploying-event-driven-microservices.md):

1. **No breaking changes to any state stores.**
2. **No breaking changes to the internal [[microservice-topology|microservice topology]]** — particularly relevant for [[lightweight-framework-microservice|lightweight-framework]] services where the topology and [[changelog-stream|changelog]] layout are tightly coupled.
3. **No breaking changes to internal event schemas.**

If all three hold, this pattern fits scenarios like:

- A new input field added and now consumed by the business logic.
- A new input stream consumed.
- Bug fixes that do not require reprocessing.

## What changes vs the basic pattern

Only step 4 of [[basic-full-stop-deployment]] changes. Instead of stopping all instances simultaneously, stop **one instance at a time**, update it, restart it, wait for readiness, then move to the next. During the rollout window, old and new logic run concurrently against the same event streams.

## The silent-breakage risk

"Inadvertently altering the internal microservice topology is one of the most common mistakes people make when trying to use this deployment pattern. Doing so is a breaking change and will require a full application reset instead of a rolling update." (source: chapter-16-deploying-event-driven-microservices.md)

Internal topology changes in a [[lightweight-framework-microservice|lightweight framework]] typically change [[changelog-stream|changelog]] layout or [[internal-state-store|internal-state-store]] schema. A rolling update then has some instances writing the new layout and others the old, corrupting state.

Bellemare's mitigation: **a compatibility test in the pipeline that checks whether a rolling update is safe** (source: chapter-16-deploying-event-driven-microservices.md). Determining this manually is error-prone; automate it.

## Trade-offs

- **Benefit**: near-real-time processing continues through the rollout — no downtime.
- **Drawback**: the prerequisites rule out a lot of real changes. Schema evolution, state-store shape changes, and topology changes all require a different pattern.

## When to pick this vs the alternatives

| Change | Pattern |
|---|---|
| Logic-only bug fix, same schema and topology | Rolling update |
| New field on input event already in producer | Rolling update (if consumer can tolerate old events during rollout) |
| Topology change (new join, new aggregation) | [[basic-full-stop-deployment]] with [[application-reset-tool]] |
| Breaking schema change | [[breaking-schema-deployment]] |
| Request-response service that can't tolerate any downtime | [[blue-green-deployment]] |

## Related pages

- [[edm-deployment-principles]]
- [[edm-deployment-patterns]]
- [[basic-full-stop-deployment]]
- [[blue-green-deployment]]
- [[breaking-schema-deployment]]
- [[microservice-topology]]
- [[changelog-stream]]
- [[lightweight-framework-microservice]]
- [[schema-evolution]]
- [[application-reset-tool]]
