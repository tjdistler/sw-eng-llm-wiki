# Cron Reliability Challenges

**Summary**: Chapter 24's catalogue of what changes when a single-machine `crond` becomes a datacenter-wide service. The failure domain expands from one machine to multiple machines plus their network; launches become multi-RPC operations subject to partial failure; resource requirements must be declared up-front because of container isolation; and the cron service needs diverse replica placement so that localised datacenter failures don't take it out entirely.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## The single-machine baseline

Classic Unix `crond` has three reliability-relevant properties (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- **Failure domain is one machine.** If the machine is down, neither the scheduler nor the jobs run.
- **Minimal state.** The only persistent state is the crontab config file itself. Launches are fire-and-forget; `crond` does not track them.
- **`anacron` is the one exception** that tracks last-launch timestamps so a laptop can catch up missed jobs on boot — useful for daily-or-less-frequent maintenance.

This baseline makes `crond` **simple** but means single-machine cron is not a model for a datacenter service — the whole point of a datacenter is that no single machine's failure should take out a whole service.

## Expanding the failure domain

Running cron across multiple machines introduces additional failure domains (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- The **scheduler machine** (which decides to launch) can fail.
- The **destination machine** (which runs the job) can fail.
- The **network between them** can fail.

A datacenter with 1,000 machines loses 1/1000th of its fleet regularly; co-locating the cron service with a single arbitrary machine makes the whole cron service as unreliable as that one machine. The obvious fix is to **decouple processes from machines** and let the datacenter scheduler ([[borg|Borg]]) pick where cron runs and reschedule on machine death. But that buys new problems:

- **Rescheduling takes time** — health-check timeouts plus software install plus process startup.
- **Local state on the old machine is lost** unless live-migrated or persisted externally.
- **Rescheduling time can exceed the cron scheduling interval** — a one-minute tick can fall inside the failover window. Hot spares are the mitigation.

## Partial launch failures

Launching a job in a datacenter is not a single atomic action. It is one or more RPCs to the datacenter scheduler. Those RPCs can succeed independently, and the cron-service process may die partway through the sequence (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

So the cron recovery procedure must handle cases where:

- Some RPCs in a multi-RPC launch succeeded and others didn't.
- The launcher crashed between "decided to launch" and "notified quorum of completion."
- A new leader takes over mid-launch and must decide whether to retry.

This is fundamentally different from single-machine `crond`, which has no such partial states. See [[cron-partial-failure-resolution]] for the resolution mechanism (precomputed names, launch-time disambiguation).

## Container isolation changes the resource story

On a single machine, `crond` and all its child jobs share the machine's resources with no enforced isolation. In a datacenter, processes run in **containers** with declared resource limits (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- Both the cron service itself and every launched job must declare their CPU / memory / etc. requirements up front.
- A cron job may be **delayed** if the datacenter does not have capacity for it when its scheduled time arrives.
- Users want to see the full lifecycle — from scheduled launch to completion — so the cron system must track launch state through to termination. That is new state that single-machine `crond` didn't have.

## Diverse replica placement

The cron service has "many obvious and nonobvious dependencies" at datacenter scale — far more than the single binary of classic `crond`. Chapter 24 explicitly requires the datacenter scheduler to place cron replicas in **diverse locations within the datacenter**, so that a single power-distribution-unit failure or rack outage cannot take out all cron replicas at once (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

This is the same failure-domain-diversity argument [[consensus-replica-placement]] makes for consensus systems generally, applied here at the datacenter-internal scale.

## Why within a datacenter, not across the globe

A cron service *could* be deployed globally, but Chapter 24 chooses **per-datacenter** deployment (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- **Low latency** between cron leader and its [[borg|Borg]] scheduler, because they are the same datacenter.
- **Shared fate** with the datacenter scheduler — cron's primary dependency. If the datacenter scheduler is down, cron cannot launch anyway, so there is no benefit to placing cron elsewhere.

This is an applied instance of [[consensus-replica-placement]]'s "don't be more geographically robust than your clients" principle.

## What this amounts to

Chapter 24's reliability-challenge section is the operational justification for everything else in the chapter. Because:

- The service has multiple failure domains → needs multiple replicas for availability → needs [[paxos|Paxos]] to keep them consistent.
- Launches are fire-and-forget on a single machine but multi-RPC in a datacenter → needs [[cron-partial-failure-resolution|partial-failure resolution]].
- Processes can be rescheduled at any time → local-only state is insufficient → needs [[cron-state-storage|replicated + distributed-backup state]].
- All these add complexity → strong cron-job reliability requires a carefully-chosen set of trade-offs. See [[cron-idempotency-and-skip-vs-double-launch]].

## Related pages

- [[distributed-cron]]
- [[cron-leader-follower]]
- [[cron-partial-failure-resolution]]
- [[cron-state-storage]]
- [[cron-idempotency-and-skip-vs-double-launch]]
- [[borg]]
- [[consensus-replica-placement]]
- [[partial-failures]]
- [[fault-tolerance]]
