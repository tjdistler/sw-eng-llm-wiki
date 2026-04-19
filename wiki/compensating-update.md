# Compensating Update

**Summary**: A **new** transaction that semantically reverses an earlier committed transaction in a distributed workflow. The fundamental building block of [[saga|sagas]] and the [[orchestrated-request-based-pattern|orchestrated request-based]] [[eventual-consistency]] pattern. Newman calls these **semantic rollbacks** — the original transaction really happened; the compensation is a second transaction that undoes its effect as far as possible.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`, `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-19

---

## What it is

In a [[distributed-transactions|distributed business transaction]] with no cross-service ACID envelope, the only available "rollback" is to issue **another transaction** that semantically reverses a previously committed one.

If Service A inserted a `Customer` row and Service B subsequently failed, there is no way to "un-commit" A's insert. What you can do is issue an explicit *delete* on `Customer` — a compensating update. The database is not pretending the insert never happened; it happened, was durable, and has now been undone by a second transaction.

Chapter 9 of *The Hard Parts* names this mechanism as the answer when the [[orchestrated-request-based-pattern]] encounters a partial failure: the orchestrator issues compensating updates to reverse the services that already committed (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

## Compensation vs rollback

| | ACID rollback | Compensating update |
|---|---|---|
| Scope | Single database, single transaction | New transaction, usually in a separate service |
| Visibility of the original | Invisible — never committed | Visible — briefly observable, then reversed |
| Side effects | None (nothing happened) | Any side effects of the original *did* happen; compensation must deal with them |
| Can always be performed | Yes — abort the transaction | Not always — emailing a confirmation cannot be literally un-sent |

The [[saga|saga page]]'s coverage of backward recovery dives into this distinction in more detail. The key point: a compensating update is a *forward* action that looks backward in meaning. It takes code, it takes error handling, and it can itself fail.

## When compensation fails

The Hard Parts flags this as one of the nastiest distributed-transaction failure modes (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

> Another complication with compensating transactions in a distributed architecture is failures that occur during compensation. For example, suppose a compensating transaction was issued to the Customer Profile Service to reinsert the customer, and that operation failed. Now what? Now the data is really out of sync, and there's no other service or process around to repair the problem.

The practical answer in most real systems: **human intervention**. The system raises an alert, flags the inconsistent state, and a human operator reconciles the data sources. This is why compensating updates are "try to make it better"; they are not a safety net with theoretical atomicity.

## Prerequisites for reliable compensation

Compensating updates work in practice only when:

- **Each step's compensation is idempotent.** Retries must be safe. The [[idempotence]] page has the full treatment.
- **The original step was complete enough to compensate.** If the system crashed mid-step, the compensation may not apply cleanly. Two-phase status tracking (pending-state coordination — see [[saga]] Ch 17 framing) helps, but adds its own complexity.
- **The compensation has access to the data it needs.** Reinserting a deleted customer requires knowing the customer's original fields — the orchestrator must have retained them, or the services must support "restore from soft-delete" semantics.
- **No irreversible side effects in the step being compensated.** If the step shipped a physical package or sent an email, the compensation is a different business action (return shipment, apology email), not a technical reversal.

## Where it lives in the book

Chapter 9 introduces compensating updates as the fallback inside the orchestrated request-based pattern. Chapter 12 (transactional saga patterns) is the deeper treatment — eight saga variants characterised by their coupling, communication style, and consistency, each using compensating updates as its failure-recovery primitive.

## Ch 12: compensating updates vs saga state machines

Chapter 12 names an **alternative** to compensating updates inside [[eventual-consistency|eventual-consistency]] sagas: **[[saga|saga state machines]]**. Instead of compensating a failed step by rolling back prior commits, the saga transitions to an **error state** (the book's example uses `NO_SURVEY` for when the Survey Service was unreachable) and the orchestrator retries or escalates asynchronously. The end user is not blocked on the error; the system takes responsibility for eventual resolution (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

The practical trade-off (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

| | Compensating updates | Saga state machine |
|---|---|---|
| Intent | Return system to pre-transaction state | Track progress; resolve errors asynchronously |
| Responsiveness | Lower — user blocked until compensation completes | Higher — user gets a response once the happy path reaches a terminal state |
| Consistency model | Attempts atomicity | Accepts eventual consistency |
| Natural fit | Atomic sagas ([[epic-saga|Epic]], [[phone-tag-saga|Phone Tag]], [[fantasy-fiction-saga|Fantasy Fiction]], [[horror-story-saga|Horror Story]]) | Eventual sagas ([[fairy-tale-saga|Fairy Tale]], [[time-travel-saga|Time Travel]], [[parallel-saga|Parallel]], [[anthology-saga|Anthology]]) |

Chapter 12's bias: **prefer state machines when the consistency axis permits it**. Compensating updates stay in the toolkit for the cases where atomicity is genuinely required (i.e. where an Epic Saga or close relative is the only workable pattern).

Chapter 12 also adds a concrete practice for managing compensating-update logic across a codebase: a `@Saga` [[saga#managing-sagas-with-annotations-custom-attributes|annotation/attribute]] on service entry points that declares which sagas a service participates in. A simple CLI tool can then list every service in a named saga — useful for test scope and change-impact analysis.

## Related pages

- [[saga]]
- [[orchestrated-request-based-pattern]]
- [[distributed-transactions]]
- [[eventual-consistency]]
- [[base-properties]]
- [[idempotence]]
- [[compensation-workflow]] — the business-level alternative to strict compensating updates
- [[two-phase-commit]] — what compensating updates replace
- [[software-architecture-the-hard-parts]]
- [[epic-saga]]
- [[fairy-tale-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
- [[dynamic-coupling]]
