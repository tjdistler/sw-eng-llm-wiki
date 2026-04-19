# BASE Properties

**Summary**: The informal complement to [[acid|ACID]] — **B**asically **A**vailable, **S**oft state, **E**ventual consistency. Used to describe the consistency model that [[distributed-transactions|distributed transactions]] across microservices actually deliver: no cross-service atomicity, no cross-service isolation, only the promise that the data will align "eventually" (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-19

---

## The acronym

BASE was coined as a play on ACID — both chemistry terms, both acronyms, opposites in flavour (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

| Letter | Meaning |
|---|---|
| **B**A | Basically Available |
| **S** | Soft state |
| **E** | Eventually consistent |

It is deliberately vague — it essentially means "not ACID." The point of naming it is not to specify a guarantee, but to give architects a shared vocabulary for *the properties that remain* once a request crosses a service boundary.

## The three letters in detail

### Basically available (BA)

All services or systems involved in the distributed transaction are **expected to be available to participate**. Asynchronous comms can decouple participants so one being slow doesn't block the others, but the trade-off is longer time to consistency (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

### Soft state

During the transaction, the state of the overall business request is **in progress and indeterminate**. Some services have committed; others haven't. If parallel async calls are in flight, the exact "where are we?" answer may be genuinely unknown at any single point in time until all participants report back.

Example from the book: during customer registration, the Customer Profile row exists, but the Contract and Billing rows are pending. The atomic business-level transaction has no single "committed / rolled back" status during soft state.

### Eventually consistent

Given enough time, all parts of the distributed transaction will complete and the data across services will align. **How long "enough" is** depends on the [[eventual-consistency|consistency pattern]] used and on how errors are handled. See [[eventual-consistency]] for the deeper treatment of what eventual consistency does and does not guarantee.

## How BASE arises from microservices

The Hard Parts frames BASE as the **automatic consequence of service decomposition** (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

- **Atomicity is lost** — each service commits its own local transaction. A failure in one service leaves others committed.
- **Consistency is lost** — a partial failure means tables across services are out of sync; DB-level constraints (FK → PK) cannot be enforced across the boundary.
- **Isolation is lost** — once a service commits, the committed data is visible to every other caller immediately, even while the business-level transaction is still in flight.
- **Durability is local only** — each service's commit is durable, but the overall business request's completion is not guaranteed by any single service.

The net result: an atomic business request across services gets BASE, not ACID. ACID exists only **within** a service.

## Reconciling BASE data: patterns

BASE is not a solution; it is a description of the problem. Chapter 9 names three patterns for getting the data eventually-consistent once BASE semantics are accepted:

1. **[[background-synchronization-pattern]]** — an external process (batch or periodic) reconciles data sources.
2. **[[orchestrated-request-based-pattern]]** — an orchestrator drives the transaction through to completion in-request.
3. **[[event-based-consistency-pattern]]** — pub/sub events let participants align asynchronously.

Each has trade-offs; see their individual pages and [[eventual-consistency]] for the synthesis.

## Relationship to ACID

Equivalence matters: **ACID lives inside a service, BASE lives across services** (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md). A microservices architecture is BASE at the edges and ACID at each node. The architect's job is not to restore ACID across boundaries (that's [[two-phase-commit]]; don't) but to design for BASE deliberately — with [[saga|sagas]], [[compensating-update|compensating updates]], or [[compensation-workflow|compensation workflows]] where needed.

Joe Hellerstein's quip on the original ACID acronym — that the C was "tossed in to make the acronym work" — is worth keeping in mind here too. BASE is less a rigorously defined model than a mnemonic that lets architects agree they've lost the safety net and must design around its absence.

## FoDE's view

*Fundamentals of Data Engineering* Chapter 6 defines BASE in the same three letters and offers the memorable worked example of S3: until December 2020, Amazon S3 was eventually consistent — a recently written object might return its prior version for a while. The "eventual" means exactly that: after enough time, only the latest version will appear (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). See [[eventual-consistency]] for more.

## Related pages

- [[acid]]
- [[eventual-consistency]]
- [[distributed-transactions]]
- [[data-ownership]]
- [[saga]]
- [[compensating-update]]
- [[background-synchronization-pattern]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[two-phase-commit]]
- [[cap-theorem]]
- [[software-architecture-the-hard-parts]]
