# Data Integrity (SRE)

**Summary**: Chapter 26 hub. "Data integrity" in the user's eyes is a joint property of accuracy, consistency, **and** access — data that's correct but unreachable is effectively lost. The chapter develops the [[data-availability-vs-integrity|means/goal distinction]], catalogues the [[data-integrity-failure-modes|24 combinations of failure modes]], prescribes a three-layer [[defense-in-depth-data|defense in depth]] ([[soft-deletion]], [[tiered-backup-strategy|backups]], [[data-validation-pipelines|early detection]]), and closes with two real Google case studies ([[gmail-gtape-restore|Gmail GTape]] and [[google-music-runaway-deletion|Google Music runaway deletion]]).

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## What data integrity is (from the user's perspective)

The chapter's operational definition (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Data integrity is whatever users think it is. We might say data integrity is a measure of the accessibility and accuracy of the datastores needed to provide users with an adequate level of service.

The working revision after the Gmail 2011 incident: **data integrity means that services in the cloud remain accessible to users, and user access to data is especially important**. Data loss, data corruption, and extended unavailability are indistinguishable to users; therefore data integrity applies to all types of data across all services.

Empirical threshold for "too long": Google treats **24 hours** as the starting point for Google Apps, after observing that four days (the 2011 Gmail incident) was clearly too long.

## The strict requirement

Uptime SLOs and data integrity SLOs are independent, and the data side is much stricter than it might first appear. 99.99% uptime is a high bar (≤ 1 hour/year of downtime). 99.99% "good bytes" in a 2 GB artifact means up to 200 KB of corruption — catastrophic for executables and databases. From the user's perspective, **data integrity must be effectively 100% during the accessible lifetime of the object** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md).

The secret to superior data integrity: **proactive detection coupled with rapid repair and recovery**. If corruption is detected and fixed before users see it, data integrity stays at ~100%.

## Means vs goal

See [[data-availability-vs-integrity]]. Data integrity is the *means*; data availability is the *goal*. Preserving bytes on tape while users can't reach their mail for a week is a failure, not a success.

## Strategy trade-offs

Five things cloud applications optimise for (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- **Uptime** — service usability
- **Latency** — responsiveness
- **Scale** — concurrent users × workload
- **Velocity** — speed of innovation
- **Privacy** — data destroyed within reasonable time after user deletes it

Real cloud apps mix [[acid|ACID]]-style and BASE-style APIs to meet these, which produces a runtime surface riddled with referential-integrity and multi-datastore-coordination challenges — the environment the three-layer defence is designed for.

## Backups are for recovery

See [[backups-vs-archives]]. The common failure mode: teams invest in backups without ever testing restores, then discover at the worst possible moment that the backups aren't loadable, aren't complete, or can't restore fast enough. The chapter's reframing is to treat the restore as the first-class deliverable and the backup as a consequence:

> No one really wants to make backups; what people really want are restores.

## Why replication isn't a backup

See [[replication]] for the general treatment; Chapter 26 makes the specific claim that **replication and redundancy are not recoverability** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). Replication pushes corrupt rows and errant deletes to every copy, usually before anyone notices. Backups must live on *diverse* components — different media, different layers of the stack — so a zero-day in a disk driver can't take out your "backup" that was written to the same filesystem.

## The 24 failure-mode combinations

See [[data-integrity-failure-modes]]. Three axes — **root cause** (user / operator / application bug / infrastructure / hardware / site catastrophe) × **scope** (widespread / narrow) × **rate** (big-bang / creeping) — produce 6 × 2 × 2 = 24 distinct modes. No single defence covers all 24; the three-layer architecture is the structural response.

Google's own data: the most common user-visible loss is **data deletion or loss of referential integrity caused by software bugs**, and the most challenging variants are **low-grade corruption discovered weeks to months after release**. The safeguards are tuned for that.

## Defense in depth (three layers + replication)

See [[defense-in-depth-data]]. The chapter's architecture:

- **Layer 1: [[soft-deletion]]** — primary defence against accidental user deletion, developer bugs, and hijacker damage. Includes "lazy deletion" at the storage-service layer for developer-facing offerings.
- **Layer 2: [[tiered-backup-strategy|backups and recovery]]** — multi-tier backups calibrated to how much data you can lose, how fast you need to recover, and how far back you need to reach.
- **Layer 3: [[data-validation-pipelines|early detection]]** — out-of-band validators catch low-grade corruption before it propagates beyond recovery.
- **Overarching: replication** — useful for specific scenarios but **not a substitute for any of the three layers**.

## Knowing that recovery works

See [[recovery-testing]]. The only test that earns a good night's sleep is a **full end-to-end recovery test**, run continuously as part of normal operations, with alerts that fire when the test fails. Parts of any recovery process can quietly break between exercises: bad tapes, missing machine resources, unscheduled dependency changes, permission drift. You only know you can recover your recent state if you actually do so.

## Case studies

- [[gmail-gtape-restore]] — February 2011. The first large-scale use of Google's GTape offline backup system. Recovered 99%+ of affected user data within the estimated window because the recovery had been simulated many times before.
- [[google-music-runaway-deletion]] — March 2012. A refactored privacy-deletion pipeline with a race condition removed audio references for 21,000 users. 5,475 tape restores, 1.5 PB of data, one week to reinstate. The engineers' worst nightmare, caught only because a user complained about unplayable tracks.

## SRE principles applied to data integrity

See [[data-integrity-principles]]. The chapter closes with five SRE principles adapted to the data-integrity setting:

1. **Beginner's mind** — never assume you understand enough of a complex system to say it *won't* fail a certain way.
2. **Trust but verify** — any API will have defects; validate critical data out of band even when the API says you need not.
3. **Hope is not a strategy** — unexercised mechanisms fail when you need them most. Automate and exercise continuously.
4. **Defense in depth** — every single strategy eventually fails; multiple strategies covering a broad scenario surface beat one strong strategy.
5. **Revisit and reexamine** — yesterday's safety doesn't help tomorrow; re-prove assumptions as the system evolves.

## The goal state

The chapter's closing aspiration (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> As you get better at recovering from any breakage in reasonable time N, find ways to whittle down that time through more rapid and finer-grained loss detection, with the goal of approaching N = 0. You can then switch from planning recovery to planning prevention, with the aim of achieving the holy grail of all the data, all the time.

Recovery time is the operational metric; once it's low enough, prevention becomes the frontier.

## Related pages

- [[data-availability-vs-integrity]]
- [[data-integrity-failure-modes]]
- [[defense-in-depth-data]]
- [[soft-deletion]]
- [[backups-vs-archives]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[gmail-gtape-restore]]
- [[google-music-runaway-deletion]]
- [[data-integrity-principles]]
- [[fault-tolerance]]
- [[replication]]
- [[timeliness-and-integrity]]
- [[service-level-objective]]
- [[mttr-and-mttf]]
- [[testing-disaster-recovery]]
- [[learning-from-outages]]
