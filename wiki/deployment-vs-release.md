# Deployment vs Release

**Summary**: Treating software *deployment* (putting code into a production environment) and software *release* (exposing it to users) as two separate activities. The separation is what makes [[strangler-fig-pattern]], [[parallel-run-pattern]], canary release, and dark launch possible.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## The distinction

> "Just because software is deployed into a given environment doesn't mean it's actually being used by customers." (source: chapter-03-splitting-the-monolith.md)

- **Deployment**: the artifact is installed and running in a production environment. Operational concerns (config, monitoring, performance) become observable.
- **Release**: real user traffic is routed to the deployed artifact. Functional behaviour starts to matter to users.

## Why the separation matters in migration

Conflating deployment and release means every deployment is also an exposure event. Separating them lets you (source: chapter-03-splitting-the-monolith.md):

- **De-risk the rollout** by validating the new service in the actual production environment with no users on it. You can return 501 Not Implemented for the migrating endpoint, prove the deployment pipeline, exercise observability and config, then later switch traffic.
- **Roll forward and back** by changing routing rather than redeploying.
- **Use [[progressive-delivery]] techniques** — canary, dark launch, parallel run — all of which assume deployment and release can be controlled independently.

## In each migration pattern

- **[[strangler-fig-pattern]]**: deploy the new service behind the proxy first; release by reconfiguring the proxy redirect.
- **[[branch-by-abstraction]]**: deploy the new implementation behind the abstraction first; release by switching the abstraction (often via a [[feature-toggle]]).
- **[[parallel-run-pattern]]**: deploy both implementations and call both; release by changing which one is treated as authoritative.

## Related pages

- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[parallel-run-pattern]]
- [[progressive-delivery]]
- [[feature-toggle]]
- [[independent-deployability]]
- [[incremental-migration]]
