# Microservice Tax

**Summary**: Adam Bellemare's name for the **sum of up-front and ongoing costs** — financial, manpower, and opportunity — associated with implementing the tools and components of a microservice architecture (event broker, container management system, deployment pipelines, monitoring, logging). Paying the microservice tax is unavoidable; the question is whether it is paid centrally by the organization or duplicated across every team.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`

**Last updated**: 2026-04-17

---

## What the tax consists of

Running microservices at scale requires a substantial platform of supporting infrastructure (source: chapter-02-event-driven-microservice-fundamentals.md):

- **[[event-broker|Event broker]]** — operating a durable, partitioned, replicated broker cluster.
- **[[container-management-system|Container management system]]** — Kubernetes, Docker Engine, Mesos Marathon, Amazon ECS, Nomad.
- **Deployment pipelines** — CI/CD, image registries, environment-specific promotion.
- **Monitoring and alerting** — metrics, tracing, dashboards, pagers.
- **Logging services** — aggregation, retention, search.

Each of these is a running system with its own operational burden, security surface, and learning curve.

## Centralized vs per-team payment

Bellemare's key observation: the microservice tax is paid **either way** — the question is who pays and how (source: chapter-02-event-driven-microservice-fundamentals.md).

- **Centrally** — one platform team runs the broker, CMS, deployment tooling, and observability for everyone. Result: a **scalable, simplified, unified framework** for developing microservices. The platform is a product; teams consume it.
- **Per team** — each team implementing microservices rolls its own version of each component. Result: **excessive overhead, duplicate solutions, fragmented tooling, and unsustainable growth.** Ten teams each running a half-built Kafka platform is ten times more expensive than one team running a well-built one, and an order of magnitude more error-prone.

The organizational choice is therefore really between "one good platform" and "many bad ones" — not between "pay the tax" and "don't".

## Size of organization matters

Small organizations "would likely do best to stick with an architecture that better suits their business needs, such as a [[modular-monolith|modular monolith]]" (source: chapter-02-event-driven-microservice-fundamentals.md). Larger organizations need to account for total platform cost and ensure the long-term roadmap justifies the investment.

This is a direct echo of Newman's advice (see [[why-microservices]] and [[when-microservices-are-a-bad-idea]]): microservices' costs scale badly when the organization is not ready for the operational discipline they require.

## The tax is decreasing over time

Bellemare notes that the microservice tax is "being steadily reduced" by hosted services, open-source maturity, and tighter integration between CMSes, brokers, and other commonly needed tools (source: chapter-02-event-driven-microservice-fundamentals.md). The argument is not that the tax is negligible but that the cost curve is moving in the right direction — hosted event brokers, managed Kubernetes, and off-the-shelf observability stacks all reduce the manpower required to reach production readiness.

## Payment is incremental, not all-or-nothing (Chapter 17)

Bellemare's conclusion stresses that adopting the platform is a staged process, not a big-bang project (source: chapter-17-conclusion.md):

- **Start with one piece.** Most organizations begin with either the event broker or the [[container-management-system]] and add the other components as need drives them. Trying to stand up the whole stack at once is unnecessary and usually counterproductive.
- **Build vs outsource is a standing trade-off.** The major cloud providers (Google, Microsoft, Amazon) offer managed versions of every line-item on the tax — managed Kafka/EventHubs/Kinesis, managed Kubernetes, hosted schema registries, managed CI/CD, managed logging and monitoring. Each piece should be independently evaluated: *is the vendor's offering cheaper than the in-house version of this specific component at our scale?*
- **The essential services are unchanged from Chapter 2.** Ch 17 re-lists them: event broker, schema registry and data exploration service, container management system, CI/CD service, monitoring and logging. If you haven't thought about one of these, you haven't thought about your tax.

This is a softer framing than Chapter 2's centralized-vs-per-team dichotomy: *within* the centralized model, each platform piece can come from outside the organization instead of being built in-house, and pieces can be adopted in any order.

## Relationship to the wiki's existing coverage

- **[[why-microservices]]** and **[[when-microservices-are-a-bad-idea]]** — Newman's cost/benefit framing covers the same territory from the migration side.
- **[[running-too-many-things]]** — the operational tax of many services without automation.
- **[[event-broker]]** and **[[container-management-system]]** — the two biggest line items in Bellemare's tax.
- **[[modular-monolith]]** — the alternative Bellemare points small organizations toward.

## Related pages

- [[event-driven-microservices]]
- [[event-broker]]
- [[container-management-system]]
- [[why-microservices]]
- [[when-microservices-are-a-bad-idea]]
- [[running-too-many-things]]
- [[modular-monolith]]
- [[microservices]]
