# Blue-Green Deployment

**Summary**: A zero-downtime deployment pattern where a full copy of the new service (**blue**) is brought up alongside the running old service (**green**), each with its own [[consumer-group]], state store, and IP addresses. A router gradually shifts traffic from green to blue and the green side is kept briefly warm for fast rollback. Primarily a **request-response** pattern; Bellemare warns it breaks when the service emits events in reaction to input event streams.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The setup

(source: chapter-16-deploying-event-driven-microservices.md)

- **Green** — current, serving production traffic.
- **Blue** — new version, deployed in parallel. Fully isolated: its own external data store, its own [[consumer-group]], its own IP addresses.

Blue consumes input events until [[consumer-lag-monitoring|monitoring]] shows it is sufficiently caught up to green. The router in front of the services then begins shifting traffic: first a small canary fraction for validation, then more and more until green is idle.

## The cooldown window

After blue takes all traffic, green can be turned off immediately or left idle for a fixed cooldown period depending on the service's sensitivity. If an error surfaces during cooldown, the router reroutes back to green for fast rollback — no redeploy needed.

This is a concrete application of [[deployment-vs-release]]: blue was deployed without being released; release is the routing change.

## What monitoring must cover

Monitoring and alerting need to be **integrated into the color switch**, not added afterward (source: chapter-16-deploying-event-driven-microservices.md):

- Resource-usage metrics.
- [[consumer-lag-monitoring|Consumer-group lag]] (catch-up detection).
- Autoscaling triggers.
- System alerts.

Without this, "caught up enough to cut over" is a guess.

## Where it works

- **Event-stream consumers** where processing is the whole job (no output event stream, or an [[idempotence|idempotent]] output). Blue catches up from the input streams and takes over.
- **Request-response services** that happen to produce an event per request (see [[request-as-event]]).

## Where it does NOT work

Bellemare's explicit warning:

> "Blue-green deployments do not work when the microservice produces events to an output stream in reaction to an input event stream. The two microservices will overwrite each other's results in the case of entity streams or will create duplicated events in the case of event streams. Use either the rolling update pattern or the basic full-stop deployment pattern instead." (source: chapter-16-deploying-event-driven-microservices.md)

Both colors are consuming the same input stream and writing to the same output stream. For an [[entity-event|entity stream]], they race to write competing versions of the same key; the outcome depends on whoever wrote last. For a non-entity [[event-streams|event stream]], each color emits its own copy of every output event — consumers see duplicates. Neither is recoverable without replaying from source.

The remedies are the [[rolling-update-pattern]] (if prerequisites hold) or [[basic-full-stop-deployment]] (if they don't).

## Relationship to the general blue-green pattern

Blue-green is a standard release technique outside EDM — usually described as "two production environments and a router." The EDM wrinkle is the stateful-consumer catch-up phase before the cutover and the producer-collision constraint.

## Related pages

- [[edm-deployment-principles]]
- [[edm-deployment-patterns]]
- [[basic-full-stop-deployment]]
- [[rolling-update-pattern]]
- [[deployment-vs-release]]
- [[progressive-delivery]]
- [[consumer-lag-monitoring]]
- [[consumer-group]]
- [[entity-event]]
- [[idempotence]]
