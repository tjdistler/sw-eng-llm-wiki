# Service Mesh

**Summary**: An architecture in which each service instance communicates with other services through its own dedicated *local* proxy (sidecar), with central control and monitoring via a control plane. Avoids the contention of a shared "smart pipe" while still centralising cross-cutting concerns like protocol translation, retries, and observability.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## The problem it solves

Putting a single shared proxy in front of all services lets you do useful things — protocol translation, routing, retries — but as the proxy accumulates per-service logic it becomes a shared dependency that multiple teams must coordinate to change. That undermines [[independent-deployability]] and re-introduces deployment contention (source: chapter-03-splitting-the-monolith.md).

A service mesh keeps each service's piece of the "pipe" *with* the service. Each service has its own sidecar proxy, configured for its own needs. A control plane provides centralised monitoring and policy without becoming a deployment bottleneck.

## Square's experience

Square migrated from a homegrown RPC system to gRPC with minimal disruption to each service by introducing a service mesh built on Envoy. They reduced the change required in each individual service while still centralising the new protocol's behaviour (source: chapter-03-splitting-the-monolith.md). Newman cites this as a sympathetic illustration of the pattern but notes Square ended up building something custom around Envoy because the off-the-shelf options didn't quite fit at the time.

## Newman's caution (as of writing)

Newman is conceptually positive about service meshes but warns that the tooling space took a while to stabilise. Istio appeared to be the leader but many alternatives were emerging weekly. His advice was to **let the space settle** before committing if you can (source: chapter-03-splitting-the-monolith.md).

## Relationship to migration patterns

A service mesh is not itself a migration pattern but a piece of infrastructure that supports them. In particular:

- It can host the proxy used by [[strangler-fig-pattern]] without making that proxy a shared bottleneck.
- It can centralise policy for [[progressive-delivery]] (canary, traffic-shifting) across many services.

## Related pages

- [[strangler-fig-pattern]]
- [[independent-deployability]]
- [[rpc]]
- [[progressive-delivery]]
- [[migration-pattern-selection]]
