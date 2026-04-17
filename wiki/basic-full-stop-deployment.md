# Basic Full-Stop Deployment

**Summary**: The baseline EDM deployment pattern: halt the current instances, optionally reset state/offsets/internal streams, deploy the new version, and run post-deploy validation. All other patterns in [[edm-deployment-patterns]] are variations on this skeleton. Simple, always correct, but incurs the full downtime window.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The five steps

(source: chapter-16-deploying-event-driven-microservices.md)

### 1. Commit code

Merge to main, which kicks off the CI pipeline via commit hooks. See [[continuous-integration-delivery-deployment]].

### 2. Execute automated unit and integration tests

Part of the CI pipeline. Integration tests should run against **transient isolated environments** per-service rather than a shared long-lived one.

### 3. Run pre-deployment validation tests

Two EDM-specific checks (source: chapter-16-deploying-event-driven-microservices.md):

- **Event-stream validation** — input streams exist, output streams exist (or can be auto-created), correct read/write permissions granted.
- **Schema validation** — input and output schemas satisfy [[schema-evolution]] compatibility rules; the CI step ingests the schema-to-stream map and runs compatibility checks mechanically.

### 4. Deployment

Two sub-steps:

**4a. Stop and clean up.** Stop the existing instances. If the change invalidates existing state, run the [[application-reset-tool]]:

- Reset [[consumer-offset|consumer-group offsets]].
- Purge [[internal-state-store|internal state stores]] and [[changelog-stream|changelog streams]].
- Delete any service-owned internal topics.

If state rebuild after a failed deploy would be expensive, an alternative: **deploy as a new service** — leave old state, offsets, and internal topics in place so a quick rollback is possible by routing back to the old instance.

**4b. Deploy.** Start the new container(s); wait for readiness. On failure, abandon and roll back to the previous known-good version.

### 5. Run post-deployment validation

Confirm the service is processing normally: [[consumer-lag-monitoring|lag trending down]], no new error logs, endpoints healthy.

## Dependency coordination

Before (and after) running the basic pattern, Bellemare warns to consider impacts to dependent services (source: chapter-16-deploying-event-driven-microservices.md): SLAs, downtime, stream-processing catch-up time, output event load, new event streams, breaking schema changes. Communicate with downstream owners so the surprise is manageable. This aligns with [[edm-deployment-principles|deployment principles 4 and 5]].

## When to use it

As a baseline:

- Simplest to reason about.
- Always correct — there is no mixed-version window.
- Fine when the SLA can absorb the downtime window.

As a fallback:

- Required when the change invalidates the [[microservice-topology|internal topology]] (breaks the [[rolling-update-pattern]] prerequisites).
- Required when a [[changelog-stream|state-store changelog]] layout changes — a rolling update would mix incompatible state.

## Related pages

- [[edm-deployment-principles]]
- [[edm-deployment-patterns]]
- [[continuous-integration-delivery-deployment]]
- [[rolling-update-pattern]]
- [[blue-green-deployment]]
- [[breaking-schema-deployment]]
- [[application-reset-tool]]
- [[schema-evolution]]
- [[consumer-lag-monitoring]]
- [[state-store-rebuilding-vs-migrating]]
