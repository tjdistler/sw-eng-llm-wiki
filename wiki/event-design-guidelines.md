# Event Design Guidelines

**Summary**: Adam Bellemare's collected best practices (and anti-patterns) for defining events in an event-driven microservice architecture. Hub page for the concrete rules that compose into the [[data-contract]] story — not hard laws, but strong defaults whose tradeoffs should be understood before they are broken.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## The set of guidelines

Bellemare's Chapter 3 closes with a "Designing Events" section listing what to do and what to avoid. As the number of event definitions grows across an organization, these guidelines minimize the otherwise-repetitive pain points for both producers and consumers (source: chapter-03-communication-and-data-contracts.md).

| # | Guideline | Page |
|---|---|---|
| 1 | Tell the whole truth — the event is the result, not a signal pointing to it | [[event-as-single-source-of-truth]] |
| 2 | Use a singular event definition per stream | [[singular-event-definition-per-stream]] |
| 3 | Use the narrowest data types | [[event-structure]] |
| 4 | Keep events single-purpose — no `type` field overloading | [[single-purpose-events]] |
| 5 | Minimize the size of events | see below |
| 6 | Involve prospective consumers in event design | see below |
| 7 | Avoid events as semaphores or signals | [[event-as-single-source-of-truth]] |

## Minimize the size of events

Events work well when they are small, well-defined, and easily processed (source: chapter-03-communication-and-data-contracts.md). When a proposed event is large:

- **Audit the relevance.** Fields added "just in case" rarely end up useful to downstream consumers. Strip them.
- **Revisit the [[bounded-context]] of the service.** If the event is large because the service is doing a lot, the scope may be wrong. Split the service and the event will follow.
- **Use a pointer only when genuinely unavoidable.** Some events legitimately reference large artifacts (image files, reports) that cannot fit in a broker message. In that case a pointer to the data is acceptable, but Bellemare flags the risk: multiple sources of truth and payload mutability, both of which erode the immutable-ledger property that the broker provides.

## Involve prospective consumers in event design

Designing a new event in isolation is a common failure mode. Consumers understand their own needs and anticipated business functions better than the producer does, and a joint design conversation surfaces ambiguity in the [[data-contract]] before either side writes code (source: chapter-03-communication-and-data-contracts.md). This is the EDM analogue of [[consumer-driven-contracts]] — moved earlier into the lifecycle, at design time rather than test time.

## These are not hard laws

Bellemare is explicit that none of these are hard-and-fast rules — they can be broken, but only after thinking carefully about the full scope of implications and tradeoffs for the specific problem space (source: chapter-03-communication-and-data-contracts.md). The default is to follow them; the burden of proof is on the exception.

## Related pages

- [[data-contract]]
- [[event-structure]]
- [[single-purpose-events]]
- [[singular-event-definition-per-stream]]
- [[event-as-single-source-of-truth]]
- [[schema-evolution]]
- [[consumer-driven-contracts]]
- [[event-driven-microservices]]
- [[bounded-context]]
