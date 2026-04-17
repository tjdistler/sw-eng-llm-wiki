# Single Writer Principle

**Summary**: A governance convention for event-driven microservices: **each event stream has exactly one producing microservice**, and that microservice is the authoritative owner of every event on the stream. Knowing the single writer lets anyone trace data lineage and resolve "who is the source of truth for this fact?" without ambiguity.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The rule

Each event stream has **one and only one** producing microservice. That microservice **owns** every event on the stream (source: chapter-02-event-driven-microservice-fundamentals.md).

Two direct consequences:

- **Authoritative source of truth is always known.** For any event on any stream, you can point to the single service responsible for producing it. Data lineage through the [[business-topology|business topology]] is tractable.
- **Multiple writers are disallowed.** Even if two services have access to similar data, they do not both publish to the same stream. If two logical producers need to cooperate, one owns the stream and the other feeds it internally.

## Enforcement

Bellemare points to **access control mechanisms** — covered in Chapter 14 of the book — as the way the single writer principle is enforced in practice (source: chapter-02-event-driven-microservice-fundamentals.md). The [[event-broker]] grants write access on a stream only to the owning microservice's identity; other services are readers only.

Chapter 14 makes this concrete: the owning microservice is the only identity that holds `CREATE` and `WRITE` on a stream; consumers get `READ` only (source: chapter-14-supportive-tooling.md). See [[event-stream-acls]] for the permission model and [[microservice-to-team-assignment]] for how identity is resolved to a team.

## Why this matters for EDM

The single writer principle is what makes the event stream usable as the organization's **single source of truth**. Without it:

- Schemas on a stream could evolve in incompatible ways if two producers disagree on the format.
- Event ordering for a given key could be violated if two producers race.
- Downstream consumers could not tell which producer to talk to when investigating bad data.
- Ownership of streams could not be assigned to teams cleanly, breaking Conway's-law alignment of the data [[communication-structures|communication structure]] onto the business structure.

## Relationship to existing wiki coverage

- **[[communication-structures]]** — the single writer principle is the structural invariant that keeps the data communication structure authoritative.
- **[[event-broker]] / [[log-based-message-brokers]]** — the substrate where the write access is granted.
- **[[bounded-context]]** — typically the producing microservice is the owner of a bounded context, and its output streams carry the context's public events.

## Related pages

- [[event-driven-microservices]]
- [[event-broker]]
- [[event-streams]]
- [[communication-structures]]
- [[bounded-context]]
- [[log-based-message-brokers]]
- [[event-stream-acls]]
- [[microservice-to-team-assignment]]
