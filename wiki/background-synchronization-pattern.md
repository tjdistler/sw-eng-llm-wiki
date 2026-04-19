# Background Synchronization Pattern

**Summary**: An [[eventual-consistency]] pattern where a separate external process (batch job or periodic service) reconciles data sources after business requests have already completed. Simple and responsive for end-users, but **breaks every [[bounded-context]]** by giving the sync process write access to all participating services' tables (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The shape

The end-user request returns as soon as the *primary* service has committed. The other services' tables are **not** updated in-band. Later — minutes, hours, or overnight — a background process wakes up and brings them into line.

The Hard Parts' worked example: a customer unsubscribes from the Sysops Squad support plan. The Customer Profile Service deletes the Profile row and immediately confirms the unsubscribe to the user. Hours later, a nightly batch process deletes the corresponding rows in the Support Contract and Billing tables — the system is now consistent (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

## How the background process finds what to change

Three common mechanisms (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **Event stream** — the primary service emits events; the sync process consumes them and applies corresponding changes to the secondary stores.
2. **Database triggers** — DB-level triggers record changes; the sync process processes the change log.
3. **Delta computation** — the sync process reads both sides and computes the difference. Expensive; simplest.

## Why it looks attractive

- **Fastest user-visible response.** The user-facing transaction is just the primary commit. No fan-out, no orchestrator, no wait-for-all latency.
- **Simple to reason about on the happy path.** A single job reconciles everything.
- **Good for closed heterogeneous systems.** The chapter's recommended fit: self-contained systems that don't share runtime data with each other (e.g., an order-entry system and a separate invoicing system kept in sync nightly).

## The structural problem: broken bounded contexts

Chapter 9 names this as the biggest disadvantage — not a trade-off to be weighed, a reason not to use the pattern in microservices:

> The biggest disadvantage of the background synchronization pattern is that it couples all of the data sources together, thus breaking every bounded context between the data and the services. (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md)

The sync process must have **write access** to every participating service's tables. Effectively, every table has shared ownership between its service and the sync process. The consequences cascade:

- **Schema changes** become a multi-party coordination exercise. Dropping a column means updating the service, the schema, *and* the sync job.
- **Business logic duplication.** The sync process must encode the same rules the services already encode. Worked example: an "unsubscribe" in the Billing Service may not be a hard `DELETE` — it may be a soft-delete with a `remove_date` set to three months out, checked daily. That business rule now exists in Billing Service *and* in the sync process. Drift is inevitable.
- **[[data-ownership|Data ownership]] is genuinely shared.** The pattern violates the writer-owns rule: the sync process and the service both write.

These are the same reasons the [[shared-database-antipattern]] is bad. Background synchronization is that antipattern, just with an extra service-that-also-writes in the middle.

## Where it is appropriate

Chapter 9's carve-out: closed (self-contained) heterogeneous systems that don't otherwise communicate. A contractor-orders system + a separate invoicing system running on a different platform with a nightly sync between them — the two systems are genuinely independent aside from the batch job, so the bounded-context breakage is priced in and accepted (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

This carve-out does **not** extend to microservices architectures where tight bounded contexts are a core structural premise.

## Trade-off summary

| | For | Against |
|---|---|---|
| **Background sync** | Best user-response time (nothing synchronous in the request path); simple to implement at first | Breaks bounded contexts — sync process becomes a co-owner of every table; business logic duplicates into the sync job; schema changes require multi-party coordination; long inconsistency windows; debugging split between services and sync |

## Relationship to other patterns

- **[[orchestrated-request-based-pattern]]** — opposite end of the spectrum: consistency is achieved in-request, at the cost of responsiveness and error-handling complexity.
- **[[event-based-consistency-pattern]]** — similar in that it's asynchronous, but each service owns the processing of its own events; no single sync process crosses bounded contexts.

The event-based pattern is Chapter 9's preferred default for modern distributed architectures; background sync is retained only for the closed-system edge case.

## Related pages

- [[eventual-consistency]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[base-properties]]
- [[bounded-context]]
- [[data-ownership]]
- [[shared-database-antipattern]]
- [[distributed-transactions]]
- [[software-architecture-the-hard-parts]]
