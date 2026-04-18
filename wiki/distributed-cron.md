# Distributed Cron

**Summary**: Google's datacenter-wide cron service — a [[paxos|Paxos]]-replicated scheduler that launches periodic jobs reliably despite machine and process failures. Chapter 24 is the worked example for what changes when a small, deceptively-simple Unix utility becomes a distributed [[consensus]]-backed service: the failure domain shifts from one machine to the whole datacenter, the state (which launches have fired) must be kept consistent across replicas, and partial-launch failures become the central correctness problem.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## What Chapter 24 is about

Štěpán Davidovič's Chapter 24 describes the distributed cron service that serves most Google internal teams needing periodic job scheduling. It is structured as a **before / after** contrast: first it analyses classic single-machine Unix cron, then it walks through the reliability problems of running cron in a datacenter, and finally it describes the Google implementation — a small replica set using [[paxos|Paxos]] (specifically [[fast-paxos|Fast Paxos]]) to maintain consistent state, and [[borg|Borg]] as the datacenter scheduler that actually launches the jobs (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The chapter is short but instructive because cron looks trivially simple yet exposes, at scale, almost every distributed-systems concern the rest of the book treats separately — consensus, idempotency, partial failures, state replication, log compaction, and the operational pathology of synchronised client behaviour ([[cron-thundering-herd|the thundering herd]]).

## The three arcs

Chapter 24 moves through three sections:

1. **Single-machine cron and its reliability properties.** Classic `crond` has one failure domain (the machine), no state beyond the crontab file, and fire-and-forget launches. `anacron` is the one exception that tracks last-launch timestamps so it can catch up missed launches on a laptop (source: chapter-24-distributed-periodic-scheduling-with-cron.md).
2. **What changes when cron is distributed.** See [[cron-reliability-challenges]]: multiple failure domains, container isolation, partial launch failures, resource-acquisition delays, diverse-location replica placement.
3. **The Google design.** See [[cron-leader-follower]], [[cron-partial-failure-resolution]], [[cron-state-storage]], and [[cron-thundering-herd]].

## The reliability properties of cron jobs that make this hard

Cron jobs are enormously diverse and the appropriate reliability story depends on what each job does (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- Some are **idempotent** (garbage collection) — double-launch is safe.
- Some are **not idempotent** (email newsletter, monthly payroll) — double-launch is harmful or unrecoverable.
- Some jobs **can tolerate skipping** (5-minute GC).
- Some cannot (monthly payroll).

There is no single answer that fits every situation. The system cannot know in advance which flavour each job is. The chapter's stance: **fail closed** — prefer skipping over risking a double-launch — because skipped launches are generally recoverable by the job owner, while double launches may be impossible to undo. See [[cron-idempotency-and-skip-vs-double-launch]] for the detailed framing.

## The architecture in one picture

- A **small replica set** (default three) runs the cron service, scheduled by [[borg|Borg]] onto diverse failure domains within a single datacenter.
- [[paxos|Paxos]] (specifically [[fast-paxos|Fast Paxos]]) synchronises state across the replicas. A single **leader** replica performs the actual launches; **followers** maintain the state so they can take over (source: chapter-24-distributed-periodic-scheduling-with-cron.md).
- Each launch is bracketed by two synchronous Paxos entries: **launch-about-to-start** and **launch-completed**. This is what lets a new leader determine, after a failover, which launches were in flight.
- The leader launches jobs by sending RPCs to the datacenter scheduler ([[borg|Borg]]). Because a logical launch may consist of multiple RPCs, partial failures in the middle are possible, and the architecture has to resolve them — see [[cron-partial-failure-resolution]].
- Paxos logs and periodic **snapshots** live on local disk; snapshots are additionally backed up to a distributed filesystem. See [[cron-state-storage]].
- A crontab extension — the `?` wildcard — addresses the [[cron-thundering-herd]] problem of midnight-synchronised MapReduce spawn.

## Why within a datacenter, not globally

Chapter 24 explicitly notes that a single global cron service is possible but that Google chose **per-datacenter** deployment: low latency, and shared fate with the datacenter scheduler ([[borg|Borg]]), cron's core dependency. If the datacenter scheduler is unavailable, the cron leader cannot launch anyway; co-locating them keeps the fate-sharing explicit (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

## Why the state lives in Paxos rather than a distributed filesystem

Chapter 24 weighs two options for where cron-job-launch state lives (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- **External distributed filesystem (GFS / HDFS / [[colossus|Colossus]]).** These are optimised for large files; the small writes cron needs are expensive and high-latency.
- **In-service replicated state (Paxos).** Keeps cron's dependency surface small. A base service with wide blast radius should have few downstream dependencies.

Google chose Paxos-replicated state. Snapshots are additionally backed up to distributed filesystem to protect against all three replicas simultaneously losing their local disk — see [[cron-state-storage]].

## Lessons the chapter draws

Chapter 24 closes with three general lessons that transcend cron itself:

1. **Even a "simple" utility gets complicated when distributed.** Every classical single-machine assumption (single failure domain, ephemeral state, fire-and-forget execution) breaks.
2. **Strong consistency is the correct default for critical scheduling state.** Skipped launches are recoverable; double launches often are not. Paxos is the natural fit.
3. **The datacenter scheduler's primitives shape what the distributed service can do.** The partial-failure resolution technique (precomputed names + launch-time in the name) depends on [[borg|Borg]]'s ability to look up job state by name.

## Cross-book framing

- [[consensus]] and [[paxos]] / [[multi-paxos]] / [[fast-paxos]] — the chapter is an applied consensus system, smaller and more specialised than [[chubby|Chubby]] but with the same Paxos-family machinery.
- [[idempotence]] — the chapter is a case study in systems where idempotency is *not* universal and must be reasoned about per-job.
- [[borg]] — the datacenter scheduler that actually runs the cron jobs; the leader's interaction with Borg is the source of partial-launch failures.
- [[managing-critical-state]] — the chapter is the applied form of Chapter 23: "schedule for job X at time T has fired" is exactly the kind of critical shared state consensus is for.
- [[reliable-replicated-datastore]] — structurally the cron service is one, specialised for scheduling rather than general key-value storage.

## Related pages

- [[cron-reliability-challenges]]
- [[cron-idempotency-and-skip-vs-double-launch]]
- [[cron-leader-follower]]
- [[cron-partial-failure-resolution]]
- [[cron-state-storage]]
- [[cron-thundering-herd]]
- [[paxos]]
- [[multi-paxos]]
- [[fast-paxos]]
- [[consensus]]
- [[managing-critical-state]]
- [[reliable-replicated-datastore]]
- [[borg]]
- [[idempotence]]
- [[site-reliability-engineering]]
