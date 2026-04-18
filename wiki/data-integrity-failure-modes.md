# Data Integrity Failure Modes

**Summary**: Chapter 26's three-axis taxonomy for data-loss events. **Root cause** (6 options) × **scope** (2) × **rate** (2) = **24 distinct combinations**. No single defence covers all 24, which is why Chapter 26 prescribes [[defense-in-depth-data|three complementary layers]]. An effective restore plan must handle each of the 24 modes in any combination with any other mode.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## The three axes

### Root cause (6 options)

An unrecoverable loss of data may be caused by any of (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

1. **User action** — accidental deletion, misconfigured sharing, hijacker-initiated deletion.
2. **Operator error** — admin running the wrong command; privileged-access mistakes.
3. **Application bugs** — code that deletes or corrupts data; the category that dominates at Google.
4. **Infrastructure defects** — filesystem, storage engine, orchestrator misbehaviour.
5. **Hardware error** — disk, RAM, network device failure; silent bit-flips.
6. **Site catastrophe** — datacenter fire, flood, regional power loss.

### Scope (2 options)

- **Widespread** — many users, many entities affected.
- **Narrow and directed** — a specific small subset (one user's mailbox, one tenant's data).

### Rate (2 options)

- **Big-bang** — one minute replaces a million rows with ten.
- **Creeping** — ten rows deleted per minute for weeks.

## The 24 combinations

6 × 2 × 2 = 24. Each combination is a distinct scenario that an effective data-integrity program must plan for (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> An effective restore plan must account for any of these failure modes occurring in any conceivable combination. What may be a perfectly effective strategy for guarding against a data loss caused by a creeping application bug may be of no help whatsoever when your colocation datacenter catches fire.

## Google's empirical finding

A study of **19 data recovery efforts at Google** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Most common user-visible scenario: **data deletion or loss of referential integrity caused by software bugs** (root cause: application bugs).
- Most challenging variant: **low-grade corruption or deletion discovered weeks to months after the bug was released** (creeping rate, often narrow scope, application-bug root cause).

Google's safeguards are tuned for this combination specifically. That's the rationale behind [[soft-deletion]]'s 30-60 day default windows, the multi-tier [[tiered-backup-strategy|backup strategy's]] 30–90 day retention, and the specific emphasis on [[data-validation-pipelines|out-of-band validators]] that catch creeping corruption before it becomes unrecoverable.

## Point-in-time recovery

Creeping application bugs produce the hardest recovery scenarios: different users are affected at different times, each requiring recovery to a **different point in time**. The scenario is called "point-in-time recovery" externally, "time-travel" at Google (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md).

> A backup and recovery solution that provides point-in-time recovery for an application across its ACID and BASE datastores while meeting strict uptime, latency, scalability, velocity, and cost goals is a chimera today!

Chapter 26's pragmatic advice: if point-in-time recovery is available in your cloud APIs, use it. If not, adopt a **tiered backup strategy** (see [[tiered-backup-strategy]]) that retains expensive local snapshots for short windows and cheap full/incremental copies for longer windows. **Don't skip both.**

## Why 24 matters for defence design

The 24-combination framing makes explicit why single-mechanism protection is insufficient:

- **Replication** alone: protects against some hardware and site-catastrophe modes, but propagates every big-bang user/app-bug deletion instantly.
- **Backups** alone: protect against most modes if retention is long enough, but can't catch creeping corruption before it's backed up too.
- **Validators** alone: catch creeping corruption, but don't recover; they're a detection mechanism, not a restore mechanism.

The three layers — [[soft-deletion]], [[tiered-backup-strategy|backups]], [[data-validation-pipelines|validators]] — are each strongest against a different subset of the 24 modes. Together they cover the matrix.

## Why 24 matters for SLO design

An SLO stated as "data integrity" with no decomposition isn't operationalisable. Chapter 26's framing implies the SLO should be stated **per failure-mode class** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md): *"Teams define SLOs for data availability in a variety of failure modes. A team practices and demonstrates their ability to meet those SLOs."* Different classes warrant different recovery targets.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[soft-deletion]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[replication]]
- [[service-level-objective]]
