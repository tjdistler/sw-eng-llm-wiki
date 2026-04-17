# EDM Deployment Patterns

**Summary**: Comparison hub for the four EDM deployment patterns Bellemare catalogs in Chapter 16: [[basic-full-stop-deployment|basic full-stop]], [[rolling-update-pattern|rolling update]], [[blue-green-deployment|blue-green]], and [[breaking-schema-deployment|breaking schema]]. Each makes a different trade-off against downtime, change-class supported, and coordination cost.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The comparison

| Pattern | Downtime | Change classes supported | Zero-coordination? |
|---|---|---|---|
| [[basic-full-stop-deployment]] | Full stop + rebuild window | Any | Yes (baseline) |
| [[rolling-update-pattern]] | None | Non-breaking state, topology, schema only | Yes |
| [[blue-green-deployment]] | None | Request-response and consume-only services; **not** producer-on-input-stream | Yes |
| [[breaking-schema-deployment]] | Depends on strategy | Breaking schema changes | **No** — requires renegotiation with all consumers |

## Decision flow

1. **Is the schema change breaking?** → [[breaking-schema-deployment]].
2. **Is the service a request-response API or consume-only?** → [[blue-green-deployment]] for zero downtime.
3. **Do all three rolling-update prerequisites hold** (no state-store break, no topology break, no schema break)? → [[rolling-update-pattern]].
4. **Otherwise** → [[basic-full-stop-deployment]] with the [[application-reset-tool]] as needed.

## Principles the patterns are constrained by

The four patterns all live under the seven [[edm-deployment-principles]]:

- Principle 4 (reprocessing impact) rules out full-stop + reset on very large streams unless SLAs allow.
- Principle 5 (SLA adherence) is what pushes zero-downtime teams to blue-green or rolling update.
- Principles 6–7 (minimize dependent changes, negotiate breaks) are the entire content of breaking-schema deployment.

## What Bellemare does *not* catalog here

The chapter is explicit that this is not a comprehensive list. Notably absent:

- **Canary release** as a standalone pattern — addressed implicitly inside blue-green's gradual traffic shift and generally via [[progressive-delivery]].
- **Parallel run** — covered separately at the verification layer; see [[parallel-run-pattern]].

The right framing is: Chapter 16 catalogs the four primary EDM deployment *shapes*, and the wider [[progressive-delivery]] umbrella describes the *rollout controls* layered on top.

## Related pages

- [[edm-deployment-principles]]
- [[basic-full-stop-deployment]]
- [[rolling-update-pattern]]
- [[blue-green-deployment]]
- [[breaking-schema-deployment]]
- [[continuous-integration-delivery-deployment]]
- [[progressive-delivery]]
- [[parallel-run-pattern]]
- [[independent-deployability]]
- [[application-reset-tool]]
