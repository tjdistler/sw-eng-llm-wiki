# Serving State from an EDM

**Summary**: Exposing an event-driven microservice's [[materialized-state|materialized view]] via a request-response API so external clients (UIs, other services) can query current state without touching the underlying event streams. Four architectural choices: internal-state single instance, internal-state sharded across instances (needs a [[smart-load-balancer]]), external-state all-in-one, or external-state with the processor and request-response API as separate deployables.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Why expose an API at all

Event streams are excellent for service-to-service communication but lousy for ad-hoc "what is the current state of X?" queries from a UI or an external system. Request-response APIs fill that gap (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). The microservice consumes input streams, builds its materialized view, and exposes a synchronous endpoint for key-based access to that view.

The caution: **access state only via the microservice's request-response API, never by directly coupling to the underlying state store.** Sharing the store introduces tight coupling between services and reintroduces the [[shared-database-antipattern]] (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

## Serving from internal state

With an [[internal-state-store]], state is sharded — each [[consumer-group|consumer-group]] instance owns only its assigned partitions. Any request must reach the one instance that owns the partition for the request's key.

Two properties enable routing (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- A key maps to a single partition (the [[partitioning-strategies|partitioner]] is deterministic).
- A partition is assigned to a single consumer instance ([[consumer-group]] / [[partition-assignor]]).

An instance that receives a request can therefore:

1. Apply the partitioner to the request's key to compute the partition ID.
2. Look up which peer owns that partition in its current assignment view.
3. Either handle the request (if it owns that partition) or forward to the peer that does.

### The round-robin problem

If a load balancer distributes requests round-robin across *N* instances and keys are evenly distributed, the probability that a request lands on the correct instance on the first try is `1/N`. For large fleets almost every request needs a redirect — each request becomes two network hops (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

### Smart load balancer

A [[smart-load-balancer]] applies the partitioner logic and current consumer-group assignments up-front, routing each request directly to the owning instance. Because rebalances are asynchronous and race conditions exist, **instances still must be able to redirect mis-forwarded requests** — the smart load balancer is a latency optimization, not a correctness mechanism (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

### Hot replicas

[[hot-replicas]] can serve direct-call reads too, if the framework supports it. The data may be stale by the replication lag, which may or may not be acceptable depending on the query (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

### Drawback

Internal-state serving entangles the processing topology with the serving topology. Every partition rebalance changes which instance answers which query. Scaling the processor scales the API (and vice versa) whether you want to or not.

## Serving from external state

With an [[external-state-store]], every instance can serve every key because all state lives in a shared networked store. Two structural advantages over the internal pattern (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- No request forwarding — any instance can handle any request.
- Consumer-group rebalances do not trigger state rematerialization, since state lives outside the instance. Seamless scaling and zero-downtime options become possible.

### All-in-one microservice

One binary does both: consumes events, materializes state to the external store, and exposes the request-response API. Each instance can serve any request (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

Instance count can exceed the partition count — extra instances don't process events but can still serve requests and stand by as failover capacity.

Advantage: minimal deployment coordination. One service, one codebase, one release cycle.

### Separate event processor and API microservice

Split the two responsibilities into two deployables within the same bounded context (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- An event-processing microservice consumes input streams and materializes state into the external store.
- A request-response microservice serves queries from that store.

They share a code repository, are tested and deployed together (single bounded context), but scale and fail independently.

**Advantages**:

- Pick implementation languages and frameworks per concern. A lightweight stream framework for processing; your organization's standard web stack for the API.
- Isolate processing failures from serving. A bug in the processor still lets the API serve the (now-stale) state.

**Disadvantages**:

- More complexity, more coordination. Schema, topology, and request-shape changes must land in both services.
- Coupling two services on a shared store *does* invalidate the "single deployable per bounded context" EDM principle. Bellemare calls this out but notes the pattern still succeeds in production when deployments and integration tests are managed carefully.

## Related pages

- [[event-driven-request-response-integration]]
- [[materialized-state]]
- [[internal-state-store]]
- [[external-state-store]]
- [[smart-load-balancer]]
- [[consumer-group]]
- [[partition-assignor]]
- [[hot-replicas]]
- [[shared-database-antipattern]]
- [[request-routing]]
