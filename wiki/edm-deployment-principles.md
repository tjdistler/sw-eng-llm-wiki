# EDM Deployment Principles

**Summary**: Adam Bellemare's seven guiding principles for deploying [[event-driven-microservices]] at scale. The deployment story for EDM is dominated by state: input-stream replay, state-store rebuilds, and schema migrations all cross service boundaries, so deployment discipline must be codified rather than improvised.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`

**Last updated**: 2026-04-17

---

## The seven principles

(source: chapter-16-deploying-event-driven-microservices.md)

### 1. Give teams deployment autonomy

Teams control their own testing and deployment processes and deploy at their discretion. This is the same [[team-autonomy]] discipline microservices demand generally, tightened by the observation that any single EDM deployment can ripple through downstream consumers — autonomy demands tooling that lets a team deploy *safely* without waiting for central ops.

### 2. Implement a standardized deployment process

Deployment must be consistent across services. A new microservice is born with a deployment pipeline already available to it. The standard CI framework is the usual vehicle (see [[continuous-integration-delivery-deployment]]).

### 3. Provide necessary supportive tooling

EDM deployments commonly need to reset [[consumer-offset|consumer-group offsets]], purge [[internal-state-store|state stores]], validate [[schema-evolution]], and delete [[changelog-stream|internal streams]]. The [[application-reset-tool]] and [[edm-supportive-tooling|supportive tooling]] platform exist to make these operations self-serve instead of centrally gated.

### 4. Consider event-stream reprocessing impacts

[[reprocessing-event-streams|Reprocessing]] is slow and noisy: downstream consumers see stale outputs for the rewind window, then a surge when the service catches up. For high-volume streams or streams with many consumers the surge can be non-trivial. Side effects compound the risk — "resending multiple years' worth of promotional emails" is Bellemare's canonical example.

### 5. Adhere to service-level agreements (SLAs)

Deployments may be disruptive: rebuilding state stores causes downtime, reprocessing generates event storms. Treat the deployment as part of the SLA — if the rebuild would breach it, pick a different pattern (e.g. [[blue-green-deployment]] or [[state-store-rebuilding-vs-migrating|migration over rebuild]]).

### 6. Minimize dependent service changes

Deployments should not force API or data-model changes in other services. Forcing other teams to deploy violates *their* autonomy. If a planned change would require it, the usual remedy is [[breaking-changes|expansion over change]] — version the contract rather than break it.

### 7. Negotiate breaking changes with downstream consumers

When breakage is unavoidable, the negotiation happens **before** deployment: new [[event-streams|event stream]], renegotiated [[data-contract]], migration plan agreed with all consumers. See [[breaking-schema-deployment]] for the mechanics and [[breaking-changes]] for the general framing.

## The anti-pattern: synchronized deployments

Bellemare is explicit: **microservices should be independently deployable**. If a service's deployments regularly force others to synchronize, the [[bounded-context|bounded contexts]] are ill-defined and the boundary needs review (source: chapter-16-deploying-event-driven-microservices.md). This is [[independent-deployability]] applied to the EDM case, with an explicit architectural diagnosis for when it fails.

## The four-way deployment trade-off (Chapter 17)

Bellemare's conclusion reframes principles 4–5 as a single four-way trade-off. Every EDM deployment has to balance (source: chapter-17-conclusion.md):

1. **SLA to consumers** — how much latency or staleness downstream services will tolerate.
2. **Load on downstream consumers** — a rebuilding service's output surge may force every consumer to scale up; a rebuild can emit millions or billions of events in short order.
3. **Load on the event broker** — rebuild and reprocess storms are the most stressful workload brokers see. See [[event-broker-quotas]] for the throttling lever.
4. **Load on monitoring and alerting** — e.g., [[blue-green-deployment]] requires two [[consumer-group|consumer groups]] that must both be monitored (including by lag-based autoscaling).

There is no setting of these four dials that is free; deployment-pattern selection is fundamentally a choice of *which* dial to pay the most on.

## Design-over-tooling: the thin serving-layer alternative

Chapter 17's most useful fresh framing is that these trade-offs are sometimes best resolved by **changing the application's design rather than the deployment tooling** (source: chapter-17-conclusion.md). The worked example: instead of doing a blue-green swap of an event-processing service that also serves synchronous requests, split the application in two — a **thin, always-on serving layer** for the synchronous API, and a **backend event processor** that can be swapped out and reprocess in its own time. The serving layer may serve stale data briefly, but no bespoke deployment tooling or two-consumer-group monitoring is needed, and SLAs to dependent services can still be met.

This maps onto the [[serving-state-from-edm]] pattern from Chapter 13 — the always-on serving layer is exactly the materialized-state-over-REST shape, now recast as a *deployment-simplification* tool. When an EDM has both an event-processing and a request-response side, splitting them lets each side have an appropriate deployment model.

The principle is general: **if your deployment pattern is getting baroque, consider whether a design change would eliminate the need for the pattern.**

## Relationship to the deployment patterns

These principles don't pick a pattern for you; they constrain which patterns are acceptable in a given situation. The four Chapter 16 patterns each make different trade-offs against principles 4–7:

- [[basic-full-stop-deployment]] — simplest; maximal SLA impact (principle 5).
- [[rolling-update-pattern]] — zero-downtime when prerequisites hold; no good for topology or schema breaks.
- [[blue-green-deployment]] — zero-downtime for request-response; does **not** work for consumer-driven producers.
- [[breaking-schema-deployment]] — the principled response to principle 7 when breakage is unavoidable.

See [[edm-deployment-patterns]] for the comparison grid.

## Related pages

- [[event-driven-microservices]]
- [[edm-deployment-patterns]]
- [[continuous-integration-delivery-deployment]]
- [[microservice-tax]]
- [[application-reset-tool]]
- [[edm-supportive-tooling]]
- [[independent-deployability]]
- [[breaking-changes]]
- [[data-contract]]
- [[schema-evolution]]
- [[reprocessing-event-streams]]
- [[team-autonomy]]
- [[serving-state-from-edm]]
- [[consumer-group]]
- [[event-broker-quotas]]
