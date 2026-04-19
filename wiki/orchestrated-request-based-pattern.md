# Orchestrated Request-Based Pattern

**Summary**: An [[eventual-consistency]] pattern where an **orchestrator** drives a distributed transaction to completion *during the end-user's request*, coordinating all participating services and handling errors with [[compensating-update|compensating updates]]. Favours **consistency over responsiveness** and makes error handling very complex.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The shape

A single orchestrator service owns the business request. It knows:

- The business process (the step sequence).
- The participants (which services do which steps).
- Multicast logic (what to call in parallel vs serial).
- Error handling (what to do when a step fails).
- Contract ownership (the orchestrator owns the end-to-end API contract).

The end user waits until the orchestrator reports success or failure. By the time the response returns, all participating services have committed (or all have been compensated).

## The book's worked example

The Sysops Squad customer-unsubscribe flow:

```
11:23:00  User clicks Unsubscribe
11:23:00  Unsubscribe Orchestrator receives the request
11:23:00  Orchestrator -> Customer Profile Service: delete profile
11:23:01  Customer Profile Service acks
11:23:01  Orchestrator -> Support Contract Service (parallel) + Billing Payment Service (parallel)
11:23:02  Both services ack
11:23:02  Orchestrator -> user: "Unsubscribed"
```

Two seconds of end-user wait vs the one second of the purely async [[background-synchronization-pattern]] or [[event-based-consistency-pattern]] (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

## Dedicated orchestrator vs overloaded participant

Chapter 9 names two implementation options (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **Designated primary service** takes on orchestration in addition to its own responsibilities (e.g., Customer Profile Service orchestrates the unsubscribe flow).
2. **Dedicated orchestration service** is introduced solely to coordinate this flow.

The book **prefers the dedicated orchestrator**. It avoids overloading an existing service with a second responsibility, and it keeps tight domain coupling out of the participant services.

This corresponds to Richards & Ford's [[mediator-topology]] framing in [[event-driven-architecture]] and to the orchestrated variant of [[saga|sagas]].

## The error-handling nightmare

The Hard Parts spends significant ink on this. When a step fails mid-flight, the orchestrator must choose among bad options (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **Retry the failing step.** May succeed. May fail again. Blocks the user.
2. **Issue [[compensating-update|compensating updates]]** to the already-successful services. May itself fail.
3. **Return an error to the user and try to repair in the background.** But *this pattern is the repair*; there is no second-chance process.
4. **Ignore the error and hope someone else fixes it.** Not really an option.

Options 3 and 4 are not viable in this pattern because the pattern **is** the consistency mechanism. That leaves retry-then-compensate as the realistic choice.

### Compensation-of-compensation failure

The truly nasty case: a compensation itself fails. The orchestrator tried to reinsert the customer after the billing step failed; the reinsert also failed. The data is now genuinely inconsistent, and there is no further automated process to fall back on. **Human intervention** is the normal answer (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

See [[compensating-update]] for the prerequisites that make compensation workable.

## Sync vs async within the orchestrator

The orchestrator has two knobs:

- **Serial** — call services one after another. Better error handling (a failed early step means no later step happened). Worst latency.
- **Parallel** — fan out to independent steps. Faster. Harder error recovery (if the parallel steps committed partially, compensations must roll back an arbitrary subset).

Chapter 9's example leans towards **serial for the decisive step, parallel for the rest**: delete the customer profile first (if it fails, nothing else needs compensating), then fan out to Contract and Billing in parallel.

## Trade-off summary

| | For | Against |
|---|---|---|
| **Orchestrated request-based** | Strong consistency by response time; single place to reason about the business process; explicit error handling; state visibility at the orchestrator | Poor responsiveness; adds a network hop/service; error handling is complex and has compensation-of-compensation failure modes; orchestrator becomes a hot service and a coordination choke point |

## When to use

The chapter's framing: reach for this pattern when **you cannot tolerate the user seeing inconsistent state** and the business workflow has well-understood failure modes that compensation can address. A financial operation where the user must see the fully committed result before walking away is a canonical fit.

Avoid it when the same workflow could be satisfied by the [[event-based-consistency-pattern]] at much better response times and simpler error handling.

## Relation to orchestrated sagas

This pattern is essentially a **synchronous orchestrated saga**. Chapter 12 of *The Hard Parts* generalises the same shape into the broader [[saga|saga pattern catalogue]], adding async-orchestrated, choreographed, and combined variants. See [[saga]] for the full breakdown.

## Related pages

- [[eventual-consistency]]
- [[background-synchronization-pattern]]
- [[event-based-consistency-pattern]]
- [[base-properties]]
- [[compensating-update]]
- [[saga]]
- [[mediator-topology]]
- [[distributed-transactions]]
- [[two-phase-commit]]
- [[software-architecture-the-hard-parts]]
