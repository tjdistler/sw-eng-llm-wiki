# Decorating Collaborator Pattern

**Summary**: A migration pattern that wraps the [[monolith]] with a proxy that triggers calls to a new microservice based on the *outcome* of a request to the monolith — making the monolith appear to call the new service when in reality it doesn't know the service exists. Useful when you cannot change the monolith and the inbound call carries enough information to drive the new behaviour.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Last updated**: 2026-04-16

---

## The idea

The Gang of Four Decorator pattern attaches new behaviour to an object without modifying it. The decorating collaborator does the same to a whole monolith: a proxy sits in front of the monolith, lets requests pass through normally, then — based on the request and/or response — invokes a new microservice (source: chapter-03-splitting-the-monolith.md).

Where [[strangler-fig-pattern]] *replaces* monolith functionality, the decorating collaborator *adds* new behaviour triggered by existing monolith functionality.

## Example: loyalty points

Music Corp wants to award loyalty points when customers place orders, but they don't want to change the existing order-placement code. A proxy intercepts the order request, lets the monolith handle it as normal, and then — if the order succeeded — calls a new Loyalty service to add points (source: chapter-03-splitting-the-monolith.md).

## The complexity warning

Unlike the strangler fig's simple redirect-or-pass-through, the decorating collaborator's proxy has to do real work: parse the response, decide whether to call the new service, marshal the call, and tunnel any reply back. The more logic accumulates in the proxy, the closer the proxy itself drifts toward being its own (technical) microservice — with all the operational concerns that implies (source: chapter-03-splitting-the-monolith.md).

## Information availability is the key constraint

The pattern works cleanly only when **the request and response carry enough information** for the new service to do its job. If the loyalty service needs the order value but the order request and response don't include it, the proxy must call back into the monolith to fetch it — adding load and arguably creating a circular dependency (source: chapter-03-splitting-the-monolith.md).

When information is missing, Newman's options in order of preference:

1. **Change the monolith** to include the needed information in the response. Rules out the pattern's main attraction (no monolith changes), but cleanest if feasible.
2. **Use [[change-data-capture]]** to react to the underlying database change instead.

## When to use it

Use the decorating collaborator when (source: chapter-03-splitting-the-monolith.md):

- You cannot change the monolith.
- The information needed is available from the inbound request or the monolith's response.
- The new behaviour is *additive* — triggered by an existing operation rather than replacing it.

If the request/response don't carry the information you need, Newman counsels thinking carefully before adopting this pattern: complexity will grow rapidly.

## Not to be confused with the FaaS decorator

Burns's [[faas-decorator-pattern]] sounds similar but is a different pattern. The decorating collaborator is a **migration-time proxy** used specifically when extracting a new service from a legacy system you cannot modify — its job is to trigger new-service behaviour based on the *outcome* of a request to the monolith. The FaaS decorator is a **stateless request/response transformer** used as a permanent architectural piece: defaulting, validation, projection, auth. One is transitional scaffolding that disappears once the extraction is complete; the other is ongoing composition. A FaaS function can serve as the implementation substrate for a decorating collaborator (see next section), which is why the names collide.

## FaaS as the implementation substrate

Burns's [[faas-decorator-pattern]] is structurally the same idea — intercept calls to a service, transform or augment, and optionally dispatch to new functionality — implemented with a [[functions-as-a-service|FaaS]] invocation instead of a hand-rolled proxy (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md). During a migration, a FaaS decorator is often the cheapest way to deploy Newman's decorating collaborator: the function is small, deploys in seconds, scales on its own axis, and can be retired as easily as it was created.

## Related pages

- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[change-data-capture]]
- [[migration-pattern-selection]]
- [[coupling]]
- [[faas-decorator-pattern]]
- [[functions-as-a-service]]
