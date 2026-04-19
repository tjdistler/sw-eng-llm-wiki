# Loose Coupling

**Summary**: An architectural property where components interact through abstract interfaces that hide internal details, enabling each component to evolve, release, and scale independently. Reis and Housley make it one of their [[principles-of-good-data-architecture|nine principles of good data architecture]] and argue it is the precondition for reversibility.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The four technical properties

Chapter 3 lists the properties of a loosely coupled system (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Systems are broken into many small components**
2. **Components interface through abstraction layers** — a messaging bus or an API — that hide and protect internal details (database backends, internal classes, method calls)
3. **Internal changes don't require changes elsewhere** — code updates hide behind stable APIs; each piece evolves separately
4. **No waterfall, global release cycle** — each component is updated separately as changes and improvements are made

Property 2 is what enables properties 3 and 4. The abstraction layer is the load-bearing part.

## The Bezos API Mandate

Chapter 3 recounts the 2002 email that made Amazon's infrastructure possible (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. All teams will henceforth expose their data and functionality through service interfaces
2. Teams must communicate with each other through these interfaces
3. No other form of interprocess communication is allowed — no direct linking, no direct reads of another team's data store, no shared-memory model, no back-doors
4. Technology doesn't matter — HTTP, Corba, Pubsub, custom — as long as there is an interface
5. All service interfaces must be designed from the ground up to be **externalizable** — plannable to expose to outside developers

The mandate is widely viewed as a watershed moment that created the decoupling AWS was later built on.

## Organisational translation

The point Chapter 3 repeatedly emphasises is that loose coupling is **not just a technical property**. Translated into organisational terms (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. Many small teams engineer a large, complex system; each owns a component
2. Teams **publish** their component's abstract interface to other teams via API definitions, message schemas, etc.
3. Each team evolves its component independently, on its own schedule
4. Teams release continuously during regular working hours — no big-bang synchronised releases

[[conways-law|Conway's Law]] is implicit throughout: a loosely coupled system requires a loosely coupled organisation.

## Why it matters

Chapter 3 names loose coupling as the prerequisite for [[reversible-vs-irreversible-decisions|reversible decisions]] (Principle 7) — you can only swap a component without breaking the world if it was decoupled in the first place (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

It is also the structural property that lets teams collaborate at scale without cross-team coordination on every change.

## Cross-book framing

- [[microservices]] — the software-architecture embodiment of loose coupling; Chapter 3 cites Bezos's mandate as its proximate ancestor
- [[coupling]] and [[cohesion]] — the deeper taxonomy of coupling types
- [[connascence]] — Richards and Ford's fine-grained measure of coupling
- [[event-driven-architecture]] — loose coupling through asynchronous events
- [[data-mesh]] — loose coupling applied to data ownership

## Warnings

Chapter 3 notes a failure mode: in loosely coupled scenarios, **decentralised teams can build systems whose data isn't usable by their peers**. The fix is to assign common standards, ownership, responsibility, and accountability to teams. Loose coupling without shared standards is not modularity — it is fragmentation (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## Related pages

- [[principles-of-good-data-architecture]]
- [[reversible-vs-irreversible-decisions]]
- [[microservices]]
- [[coupling]]
- [[cohesion]]
- [[connascence]]
- [[event-driven-architecture]]
- [[data-mesh]]
- [[conways-law]]
