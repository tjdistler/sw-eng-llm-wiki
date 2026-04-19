# CRUD

**Summary**: CRUD — **Create, Read, Update, Delete** — is the four-operation pattern that underlies most persistent-storage interfaces. It is simultaneously the dominant model for storing application state and the reason history is routinely lost at the [[source-systems|source-system]] layer: a CRUD update overwrites the previous value without retaining it.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The four operations

CRUD is "the most common pattern for storing application state in a database" and expresses the four basic operations on persisted data (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

| Operation | Meaning |
|---|---|
| **Create** | Insert a new record |
| **Read** | Retrieve an existing record |
| **Update** | Mutate an existing record in place |
| **Delete** | Remove a record |

A basic tenet: data must be created before it is used. After creation, it can be read and updated; eventually it may be destroyed. CRUD guarantees these four operations occur on data "regardless of its storage" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). A web application will routinely use CRUD for both RESTful HTTP request handling and database access.

## Why CRUD is hard on downstream data systems

The defining property of CRUD for a data engineer is that **Update** overwrites. Once the previous value is gone, downstream systems that wanted to see the change history must have captured it in some other way. Reis and Housley state this explicitly: for a CRUD-style source, "we can use snapshot-based extraction to get data from a database where our application applies CRUD operations. On the other hand, event extraction with CDC gives us a complete history of operations and potentially allows for near real-time analytics" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

The two alternatives to accepting the lossy snapshot view of a CRUD source:

- **[[change-data-capture|CDC]].** Observe the database's change log to capture each update as an event. Preserves history *externally* to the source table.
- **[[insert-only|Insert-only]] at the source.** Make the application append rather than overwrite. Preserves history *inside* the source table.

## CRUD is not universal

Not every data model follows CRUD. Notable exceptions:

- **[[event-sourcing|Event-sourced systems]]** don't update state; they append immutable events and derive state by replaying the events.
- **Append-only log stores** (Kafka, Kinesis, the Raft log) only allow appends — there is no update operation.
- **Immutable object storage** (S3 versioning, content-addressable stores) treats "update" as "new object with new identity."

For source systems of these shapes, the CRUD lens doesn't apply, and the engineer's extraction strategy changes accordingly — see [[event-streams]] and [[log-based-message-brokers]].

## CRUD in APIs

CRUD appears not only at the database but at the application-interface layer. REST APIs typically map CRUD operations to HTTP verbs:

| CRUD | HTTP verb (conventional) |
|---|---|
| Create | POST |
| Read | GET |
| Update | PUT / PATCH |
| Delete | DELETE |

See [[rpc]] and [[third-party-api-integration]] for how these API-level CRUD shapes look to a downstream data engineer.

## Cross-book connections

- [[insert-only]] — the direct alternative pattern; keeps history instead of overwriting.
- [[change-data-capture]] — the standard workaround when CRUD has to be preserved but history is still needed.
- [[event-sourcing]] — the inversion: events are primary, state is derived, updates don't exist.
- [[application-database-as-source]] — the CRUD-vs-insert-only choice at the source system level.

## Related pages

- [[insert-only]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[application-database-as-source]]
- [[source-systems]]
- [[rpc]]
- [[third-party-api-integration]]
