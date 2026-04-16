# Independent Deployability

**Summary**: The discipline of being able to change a microservice and deploy it to production without deploying anything else. Newman calls this the single most important takeaway about microservices; achieving it requires loose coupling, stable contracts, and not sharing databases.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The idea

Independent deployability is the idea that we can make a change to a microservice and deploy it into a production environment without having to deploy any other services (source: chapter-01-just-enough-microservices.md). Critically, it is not merely the *capability* — it is *the discipline you actually practice* for the bulk of your releases.

> "If there is only one thing you take out of this book, it should be this: ensure you embrace the concept of independent deployability of your microservices. Get into the habit of releasing changes to a single microservice into production without having to deploy anything else. From this, many good things will follow." (source: chapter-01-just-enough-microservices.md)

## What it requires

To guarantee independent deployability, services must be loosely coupled — you must be able to change one service without changing anything else (source: chapter-01-just-enough-microservices.md). This means:

- **Explicit, well-defined, stable contracts** between services.
- **Not sharing databases** — a shared database is one of the worst forms of [[coupling|implementation coupling]] for independent deployability (source: chapter-01-just-enough-microservices.md). See [[information-hiding]].
- **Stable interfaces**. If a service's exposed interface keeps changing, the change ripples through every consumer, forcing them to change too.

The desire for loosely coupled services with stable interfaces is what guides how we find service boundaries in the first place.

## Why it matters

Smaller, more frequent releases reduce risk:

- **Less to go wrong** in any single release.
- **If something goes wrong, it is easier to find and fix** because we changed less.
- **Faster feedback** — at the heart of continuous delivery.

Newman's own interest in microservices grew from a focus on continuous delivery: he was looking for architectures that made [[coupling|deployment coupling]] easier to reduce.

## What threatens independent deployability at scale

Chapter 5 catalogues several pain points that all attack independent deployability from different angles (source: chapter-05-growing-pains.md):

- **[[breaking-changes]]** — accidental contract breakages and lock-step deployments are independent deployability *failing*. Newman: organisations that don't sort this out won't last long enough to get big.
- **[[code-ownership-models]]** — collective ownership at scale produces "distributed monoliths" that nobody can change without touching multiple services.
- **[[end-to-end-testing]]** — heavyweight cross-service test suites turn each release into a coordinated event, eroding the deploy-one-service property.
- **[[orphaned-services]]** — services running for months untouched are a *symptom* of independent deployability working, but become risks when no one knows how to change them.

The Chapter 5 toolbox — [[consumer-driven-contracts]], [[progressive-delivery]], strong [[code-ownership-models|ownership]], [[monitoring-and-observability]] — is largely about preserving independent deployability as the architecture grows.

## Relationship to other ideas

- [[coupling]] — independent deployability fails under tight coupling, especially implementation, deployment, and temporal coupling.
- [[information-hiding]] — exposing as little as possible from a service interface preserves the freedom to change implementation without breaking consumers.
- [[bounded-context]] — domain-aligned boundaries reduce the rate at which one service must change because of changes in another.
- Erlang's hot-deployment of modules into a running process is an example of reducing deployment coupling without microservices (source: chapter-01-just-enough-microservices.md).

## Related pages

- [[microservices]]
- [[monolith]]
- [[coupling]]
- [[cohesion]]
- [[information-hiding]]
- [[bounded-context]]
- [[breaking-changes]]
- [[consumer-driven-contracts]]
- [[code-ownership-models]]
- [[end-to-end-testing]]
- [[orphaned-services]]
