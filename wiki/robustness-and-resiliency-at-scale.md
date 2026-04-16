# Robustness and Resiliency at Scale

**Summary**: Failure modes that are theoretically possible in any distributed system become routine as the number of services grows. Newman's Chapter 5 framing: ask of every call "how could this fail?" and "what should I do if it does?", then apply isolation patterns, sensible time-outs, circuit breakers, and a way of working that learns from each incident.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## Why it gets worse with scale

Distributed systems can exhibit failure modes unfamiliar to monolith-trained engineers: lost network packets, timed-out calls, machines that die, machines that stop responding (source: chapter-05-growing-pains.md). A small distributed system encounters these rarely. As service count grows, rare events become commonplace; as inter-service connectivity grows, the chance of cascading failures and back pressure rises with it.

The hardest part: these problems are most likely to emerge in **production**. Development and test environments only re-create production-like conditions briefly, so the rare events rarely happen there — and when they do, they're often dismissed as flakes (source: chapter-05-growing-pains.md).

## Newman's two-question starting point

> "First, do I know the way in which this call might fail? Second, if the call does fail, do I know what I should do?" (source: chapter-05-growing-pains.md)

Asking these on every call into another service forces explicit decisions about failure handling that would otherwise sit as implicit assumptions until production exposed them.

## Patterns Newman names

(source: chapter-05-growing-pains.md)

### Isolation between services

Reduce the surface over which one service's problem can spread:

- Async communication via [[message-brokers]] avoids the **temporal coupling** of a synchronous call chain (see [[coupling]]). The producer doesn't have to wait for the consumer to be up.
- Bulkheads — separating resources so one workload's exhaustion doesn't starve another — limit blast radius.

### Sensible time-outs

Without time-outs, a slow downstream service holds your caller's resources indefinitely. Time-outs let you fail fast and free those resources.

### Circuit breakers

Pair time-outs with a circuit breaker (Newman names but doesn't describe in depth here). When repeated calls fail or time out, the breaker opens, immediately failing further calls without trying the downstream service. This prevents back pressure from accumulating and gives the downstream service room to recover.

The pattern is from Michael Nygard's *Release It!* — Newman's recommended deeper reference.

### Multiple copies of services

Run more than one instance of each service so that an instance dying doesn't take a capability offline. Combine with [[desired-state-management]] (e.g. Kubernetes) so failed instances are restarted automatically.

## Robustness vs resilience — the Chapter 2 distinction restated

This is where the [[robustness-vs-resilience|robustness/resilience distinction]] from Chapter 2 lands operationally:

- **Robustness** mechanisms — circuit breakers, time-outs, isolation, replication — handle the *known* failure modes.
- **Resilience** is the way of working — practising for incidents, learning from them, evolving your patterns. As Newman puts it: "It's about a whole way of working — building an organization that not only is ready to handle the unforeseeable problems that will inevitably crop up, but also evolves working practices as necessary." (source: chapter-05-growing-pains.md)

## Document what you learn

A specific organisational habit Newman calls out (source: chapter-05-growing-pains.md):

> "All too often I see organizations move on too quickly once the initial problem has been solved or worked around — only for those same problems to come back again some months later."

Document production issues when they arise. Keep a record of what you learned. Treat this as part of the resilience practice, not as overhead after the fact.

## Newman's "I've scratched the surface" note

The Chapter 5 treatment is intentionally short. Newman points to *Building Microservices* Chapter 11 for depth, and to Michael Nygard's *Release It!* (Pragmatic Bookshelf, 2018) for the pattern-language treatment of resilience.

## Connection to fault-tolerance from DDIA

Newman's microservice-flavoured patterns sit on top of the broader [[fault-tolerance]] literature from Kleppmann's *Designing Data-Intensive Applications*. The DDIA discussion focuses on storage and consensus; the M2M discussion focuses on inter-service call patterns. They're complementary lenses on the same underlying problem of [[partial-failures]].

## Related pages

- [[robustness-vs-resilience]]
- [[fault-tolerance]]
- [[partial-failures]]
- [[unreliable-networks]]
- [[network-faults]]
- [[timeouts]]
- [[coupling]]
- [[message-brokers]]
- [[desired-state-management]]
- [[independent-deployability]]
