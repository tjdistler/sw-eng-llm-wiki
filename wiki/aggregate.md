# Aggregate

**Summary**: A domain-driven design concept representing a real domain entity (such as Order, Invoice, or Stock Item) along with the state machine that governs its life cycle. Aggregates are self-contained units that decide for themselves whether to allow a state transition.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`

**Last updated**: 2026-04-16

---

## The concept

In DDD, *aggregate* is a famously slippery concept. The model Newman uses is to treat an aggregate as a representation of a real domain concept — something like an Order, Invoice, or Stock Item (source: chapter-01-just-enough-microservices.md). Aggregates typically have a life cycle, which makes them naturally implementable as state machines.

Aggregates should be self-contained units in which the code handling state transitions is grouped with the state itself. The crucial invariant: **if an outside party requests a state transition in an aggregate, the aggregate can say no.** Ideally, illegal state transitions should be impossible to express (source: chapter-01-just-enough-microservices.md).

## Aggregates and microservices

A single microservice will handle the life cycle and data storage of one or more aggregate types. If functionality in another service wants to change one of these aggregates, it must either:

1. **Directly request a state change** through the owning service's interface, or
2. **Have the aggregate react to events** in the system to initiate its own state transitions (source: chapter-01-just-enough-microservices.md).

Newman gives the example of a Payment service triggering a "Paid" transition in an Invoice aggregate — either by direct API call or by reaction to a payment event.

## Relationships between aggregates

Aggregates can have relationships with other aggregates. A Customer aggregate may be associated with one or more Order aggregates. The decision to model Customer and Order as separate aggregates — potentially handled by different services — is the kind of design choice that shapes the service map (source: chapter-01-just-enough-microservices.md).

## Boundary choices

There are many ways to break a system into aggregates, and the choices are highly subjective. Newman advises starting with the mental model the system's users carry, and reshaping aggregate boundaries later for performance or implementation reasons (source: chapter-01-just-enough-microservices.md). *Event Storming* (introduced in Chapter 2) is a collaborative technique for shaping these models with non-developer colleagues.

## Aggregate vs bounded context

A [[bounded-context]] contains one or more aggregates. When mapping to microservices:

- A coarse-grained service can encapsulate an entire bounded context (recommended starting point).
- A finer-grained service can encapsulate a single aggregate.

Newman recommends starting coarse and decomposing along aggregate boundaries later if needed (source: chapter-01-just-enough-microservices.md).

## Related pages

- [[bounded-context]]
- [[domain-driven-design]]
- [[microservices]]
- [[event-sourcing]]
