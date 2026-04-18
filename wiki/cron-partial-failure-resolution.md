# Cron Partial Failure Resolution

**Summary**: Chapter 24's technique for correctly handling the case where a cron leader dies mid-launch — between "about to launch" and "launch completed" in the Paxos log. The launcher's multi-RPC interaction with the datacenter scheduler must be recoverable: either every RPC is **idempotent** (safe to reissue) or the new leader must be able to **look up** the state of each operation. Google's chosen mechanism: **precompute the datacenter-scheduler job name** before issuing any RPCs, and include the **scheduled launch time** in that name so state lookups are unambiguous.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## The problem

The cron leader brackets every logical launch with two synchronous Paxos records: **about-to-launch** and **launch-completed** (see [[cron-leader-follower]]). Between those records, the leader may issue one or more RPCs to the datacenter scheduler. If the leader dies after the first record but before the second, the new leader sees an **open launch** — the about-to-launch is in the log, the launch-completed is not (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The new leader must now decide: did the launch happen? Should it be re-issued?

## The two sufficient conditions

Chapter 24 states the abstract requirement: for the new leader to safely make this decision, one of the following must hold (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. **All operations on external systems that might need to be continued are idempotent.** Reissuing them is safe because re-execution has the same effect as single execution. See [[idempotence]].
2. **We can look up the state of all operations on external systems** to unambiguously determine whether they completed.

Either is sufficient; both are hard. Neither is sufficient without one of the two. Without at least one, partial failures lead to **missed launches or double launches**.

## Google's chosen mechanism: precomputed job names

Chapter 24's concrete design uses the **lookup-based** approach rather than general idempotency. The key observation: "Most infrastructure that launches logical jobs in datacenters (Mesos, for example) provides naming for those datacenter jobs, making it possible to look up the state of jobs, stop the jobs, or perform other maintenance" (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

So the cron service:

1. **Constructs the datacenter-scheduler job names ahead of time**, before any mutating operation. Name construction itself is a pure computation; it does not mutate [[borg|Borg]]'s state.
2. **Distributes those precomputed names to all Paxos replicas** as part of the about-to-launch record.
3. **Uses those names as the identity** under which [[borg|Borg]] tracks the launched jobs.

On leader failover, the new leader reads the Paxos log and for every open launch it knows the precomputed name. It queries [[borg|Borg]] for each name:

- **Name exists** → the RPC succeeded before the previous leader died. Log the launch-completed record in Paxos; done.
- **Name does not exist** → the RPC was never sent (or was sent but rejected). Issue it now.

No double launches, no missed launches.

## Why the launch time must be in the name

Chapter 24 goes further: **the scheduled launch time must be part of the name** (or otherwise retrievable from it). The motivating example is a short-lived, frequently-run cron job (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. The previous leader launches the job — the datacenter scheduler accepts the RPC and runs the job.
2. Before the launch-completed Paxos entry is written, the leader crashes.
3. Failover takes unusually long.
4. In the meantime, the launched job *completes* on [[borg|Borg]] and its name is reaped.
5. The new leader takes over. Its lookup for the job name returns "not found."
6. Without launch-time in the name, the new leader assumes the job never ran and re-launches it.
7. With launch-time in the name, the new leader sees "job X for launch time T was completed in the time window between my predecessor's death and now" — in one of [[borg|Borg]]'s completion records — and does not re-launch.

The launch time is the unique disambiguator that makes state lookup **safe under long failovers and successful-then-reaped jobs**, not just safe under "did the RPC get sent."

## Relationship to the general idempotence framing

This design is a specific instance of the general technique described on [[idempotence]] — attach a unique operation ID (here: the constructed name + scheduled launch time) to every logical operation, carry it end-to-end, and use it for dedup at the receiver.

What makes cron's version distinctive:

- The "operation ID" is generated from the **scheduled time**, not from a random UUID. This means every replica independently computes the same ID for the same launch — no need to replicate an ID separately from the rest of the state.
- The receiver (Borg) provides the lookup API, so cron doesn't need to maintain its own dedup table of operation IDs.
- Because the lookup API covers both *running* and *recently-completed* jobs, the identity is durable across the entire lifecycle of a launch.

## What the actual implementation looks like

Chapter 24 notes that "the actual implementation has a more complicated system for state lookup, driven by the implementation details of the underlying infrastructure. However, the preceding description covers the implementation-independent requirements of any such system" (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The general recipe for any distributed scheduler interacting with a job-naming datacenter scheduler:

1. Precompute the unique name of any launch before mutating the scheduler.
2. Synchronously record the name (and scheduled time) in a consensus log.
3. Include the scheduled time as part of the name so state lookup is unambiguous even after natural job lifecycle completion.
4. On failover, look up each name in the downstream scheduler; retry missing ones; record completion for found ones.

## The trade-off the architect cannot escape

Chapter 24 closes this section with a pragmatic note: "Depending on the available infrastructure, you may also need to consider the trade-off between risking a double launch and risking skipping a launch" (source: chapter-24-distributed-periodic-scheduling-with-cron.md). If your datacenter scheduler doesn't provide reliable completion-record lookup, or if your RPCs aren't naturally idempotent, you still have a design decision — and per [[cron-idempotency-and-skip-vs-double-launch]], the safer default is to skip.

## Related pages

- [[distributed-cron]]
- [[cron-leader-follower]]
- [[cron-idempotency-and-skip-vs-double-launch]]
- [[cron-state-storage]]
- [[idempotence]]
- [[borg]]
- [[fencing-tokens]]
- [[partial-failures]]
- [[exactly-once-semantics]]
