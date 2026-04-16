# Information Hiding

**Summary**: David Parnas's 1971 principle that module boundaries should be stable and should hide the parts of the implementation expected to change. In microservices, information hiding is the engine of [[independent-deployability]]: by exposing as little as possible at a service boundary, you preserve freedom to change everything inside.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The principle

> "Information Hiding, like dieting, is somewhat more easily described than done." — David Parnas, *The Secret History of Information Hiding*

The core idea is to **separate the parts of the code that change frequently from the parts that are static**. The module boundary should be stable, and should hide the parts of the implementation that are expected to change more often. Internal changes can then be made safely as long as module compatibility is maintained (source: chapter-01-just-enough-microservices.md).

The concept was first outlined by David Parnas in 1971, in "Information Distributions Aspects of Design Methodology" at IFIP Congress, and elaborated in his well-known 1972 paper "On the Criteria to be Used in Decomposing Systems into Modules." Parnas himself later wrote *The Secret History of Information Hiding* (2002).

## Newman's rule of thumb

> "I adopt the approach of exposing as little as possible from a module (or microservice) boundary. Once something becomes part of a module interface, it's hard to walk that back. But if you hide it now, you can always decide to share it later." (source: chapter-01-just-enough-microservices.md)

This is also why Chris Richardson's framing — that the goal of a microservice is "as small an interface as possible" — is the closest useful definition of microservice "size."

## Information hiding vs encapsulation

Encapsulation in object-oriented programming has come to mean *bundling together* one or more things into a container — a class containing fields and the methods that act on them, with visibility modifiers hiding parts of the implementation. Information hiding is related but, depending on whose definition you accept, may not be the same thing (source: chapter-01-just-enough-microservices.md). Encapsulation is mechanism; information hiding is intent.

## In microservices

Information hiding shows up everywhere a microservice meets the outside world.

### Hiding the database

If service A directly reads service B's database tables, A is coupled to B's schema, SQL dialect, and even row layout. Renaming a column or splitting a table breaks A. Hiding the database behind a service interface — or behind a separately published, intentionally shaped read dataset — lets the owning service change internals freely (source: chapter-01-just-enough-microservices.md). See [[coupling]] for the four-type coupling taxonomy.

Newman dedicates a whole chapter to the patterns that put this principle into practice when extracting from a monolith — see [[database-decomposition]]. The two coping patterns to use when you can't yet split the schema are themselves explicit applications of information hiding: [[database-view-pattern|database views]] project a limited subset of the schema, and [[database-wrapping-service|wrapping services]] hide the schema behind an API. The "intentionally shaped read dataset" idea is formalised as the [[database-as-a-service-interface]] pattern. (source: chapter-04-decomposing-the-database.md)

### Outside-in interface design

Newman recommends "outside-in" thinking: shape a service's contract by asking the *people* who will call your service what they need, then implement to that contract. Treat the service interface like a user interface. The opposite — exposing a data model or internal abstraction outward — is unfortunately common (source: chapter-01-just-enough-microservices.md).

### Hiding internal decomposition

If you decide to split a service that models an entire [[bounded-context]] into smaller services, you can hide that decision behind a coarser-grained API. The decomposition becomes an implementation detail (source: chapter-01-just-enough-microservices.md).

### Hiding domain detail in messages

A Pick Instruction sent to a Warehouse service contains only what the warehouse needs to package and send the item — not the full Order, with credit card details and pricing. Exposing only what is needed is information hiding applied to inter-service messages (source: chapter-01-just-enough-microservices.md). See [[coupling|domain coupling]].

## Related pages

- [[microservices]]
- [[independent-deployability]]
- [[coupling]]
- [[cohesion]]
- [[bounded-context]]
- [[backward-forward-compatibility]]
- [[encoding-formats]]
- [[database-decomposition]]
- [[database-view-pattern]]
- [[database-wrapping-service]]
- [[database-as-a-service-interface]]
