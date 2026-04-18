# Cron Idempotency and Skip vs Double-Launch

**Summary**: Chapter 24's framing of the correctness-at-the-edges problem for a distributed scheduler: cron jobs are enormously diverse — some are idempotent and some aren't; some tolerate skipping and some don't — and the scheduler cannot know in advance which flavour each job is. The resulting design choice is to **fail closed**: prefer skipping a launch to risking a double-launch, because skipped launches are usually recoverable by the job owner while double launches (e.g., of a mass email or a payroll run) may be impossible to undo.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## Cron jobs span a spectrum

Chapter 24's observation: "the variety of requirements that the diverse set of cron jobs entails obviously impacts reliability requirements" (source: chapter-24-distributed-periodic-scheduling-with-cron.md). Two orthogonal axes of that variety:

### Idempotent vs non-idempotent

- **Idempotent**: garbage collection, log rotation, cache refresh. Launching twice is harmless because the second launch either has nothing to do or performs the same deterministic work. See [[idempotence]].
- **Non-idempotent**: sending an email newsletter to a distribution list, running monthly payroll, mailing physical statements. A second launch sends two emails, runs payroll twice, mails duplicate statements.

### Skippable vs not-skippable

- **Skippable**: a 5-minute GC cron that misses one launch is fine — it will run again in 5 minutes.
- **Not skippable**: a monthly payroll that misses its run is a major operational problem.

These axes are independent. The four corners are all common:

| | Idempotent | Non-idempotent |
|---|---|---|
| **Skippable** | GC (ideal — either direction is fine) | Best-effort notifications (skipping is fine, duplicates are annoying) |
| **Not skippable** | Billing-rollup that is safe to retry (must run, duplicates harmless) | Payroll, one-time email blasts (must run, duplicates harmful) |

The cron service has no way to know where each job sits on this grid.

## The fail-closed choice

Chapter 24's design principle: "we favor skipping launches rather than risking double launches, as much as the infrastructure allows" (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The rationale:

- A **skipped launch** is visible to the job owner (if they monitor) and can be remediated manually — re-run the payroll, send the newsletter late, re-emit the notification.
- A **double launch** of a non-idempotent job may be impossible to undo. You cannot un-send a million emails. Payroll run twice requires claw-back or accounting reversal. Mailed physical statements are already in the post.

So the system's default bias is toward the recoverable failure (skip) rather than the potentially-unrecoverable one (double launch).

## The job owner's responsibility

The chapter explicitly points out that job owners can and should **monitor their cron jobs** — either via the cron service exposing state about managed jobs, or by setting up independent monitoring of the effects (source: chapter-24-distributed-periodic-scheduling-with-cron.md). The scheduler's fail-closed stance makes this monitoring necessary because skipped launches still need human remediation for the not-skippable class of jobs.

This is an applied form of the [[end-to-end-argument]]: correctness at the scheduler layer is not sufficient. Only the job owner can decide what a skipped-but-must-run launch requires.

## Where idempotency shows up in the cron service's own mechanics

The same idempotency / dedup discipline that [[idempotence|the general idempotence page]] covers is also the *cron service's own* tool for handling partial failures:

- When the leader dies mid-launch and a new leader takes over, it must decide whether to re-issue the incomplete launch RPC.
- Safety requires either (a) the RPC target be **idempotent** so re-issuing is harmless, or (b) the new leader can **look up** whether the previous RPC succeeded. See [[cron-partial-failure-resolution]] for the detailed technique.

So idempotency appears at two layers in Chapter 24: at the **cron job** layer (a property of the user's code that the scheduler cannot assume) and at the **cron service internals** (a property the service builds into its interaction with the datacenter scheduler).

## Monitoring as the safety net

Chapter 24 makes tracking launches a first-class part of the distributed cron design (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- Every scheduled launch is recorded in [[paxos|Paxos]] before it starts and when it finishes.
- The cron service exposes per-job launch state so users can detect skipped launches.
- Independent user-side monitoring is still recommended for the "must run exactly once" class of jobs.

The fail-closed bias and the launch-tracking infrastructure together mean the service is honest about what it does (and does not) guarantee: it will not double-launch you by design, but it may skip a launch in rare failure modes, and you are responsible for noticing.

## Relationship to effectively-once

Chapter 24 does not explicitly claim "exactly-once" or "effectively-once" semantics. Its guarantee is weaker and more honest: **at-most-once by default, with the job owner responsible for detecting misses and remediating the not-skippable cases.**

This is the inverse of the more common [[exactly-once-semantics|effectively-once]] story in stream processing, which favours at-least-once with deduplication on the consumer. Cron inverts the default because the cost of duplicate side effects (mass email, payroll) is much higher than the cost of a skipped scheduled tick plus owner-side remediation.

## Related pages

- [[distributed-cron]]
- [[cron-partial-failure-resolution]]
- [[cron-leader-follower]]
- [[idempotence]]
- [[exactly-once-semantics]]
- [[end-to-end-argument]]
- [[effectively-once-processing]]
