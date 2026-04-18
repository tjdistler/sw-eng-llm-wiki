# Cron Leader and Follower

**Summary**: The core architecture of Google's distributed cron service: a [[paxos|Paxos]]-replicated group in which a single **leader** replica holds a mutual-exclusion-grade right to launch jobs and follower replicas track every state change synchronously via Paxos so they can take over on leader failure. The leader launches each job only after a quorum of followers has acknowledged the about-to-launch record; on loss of leadership the leader must immediately stop interacting with the datacenter scheduler.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## Why there's a leader

Running N replicas of a scheduler without coordination would produce N launches of each scheduled job. The leader is the mutual-exclusion mechanism: only the leader may launch, and only one replica may be the leader at a time (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

Chapter 24 uses [[fast-paxos|Fast Paxos]], whose variant internally elects a leader replica as a performance optimisation. The cron service reuses that same Paxos leader as its own service leader — one election, two uses.

## The leader's job

The leader replica is the only replica that actively launches cron jobs. Its loop (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. Maintain an **internal scheduler** much like single-machine `crond`: a list of cron jobs ordered by next-scheduled-launch time.
2. Wait until the scheduled time of the next-due job.
3. **Synchronously replicate an "about to launch" record via Paxos** — identifying the cron job *and* its scheduled launch time. This launch-time field matters: in case of high-frequency jobs (e.g., every minute), the job ID alone would be ambiguous across consecutive launches.
4. Compute the next scheduled launch time and update local state.
5. Issue the actual launch — one or more RPCs to the datacenter scheduler ([[borg|Borg]]).
6. **Synchronously replicate a "launch completed" record via Paxos** — regardless of whether the launch itself succeeded or failed for external reasons. The system is tracking *that the scheduler attempted the launch at this scheduled time*, not whether the job itself worked.

The two bracketing Paxos records — pre-launch and post-launch — are what let a new leader resolve partial failures on takeover. See [[cron-partial-failure-resolution]].

## Why the Paxos writes must be synchronous

Chapter 24 is pointed about synchronicity: "Not performing this task synchronously could mean that the entire cron job launch happens on the leader without informing the follower replicas. In case of failover, the follower replicas might attempt to perform the very same launch again because they aren't aware that the launch already occurred" (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The cost is latency per launch. The benefit is that **no launch happens without the follower quorum knowing**, which means a new leader can always pick up state consistent with what actually happened.

## The follower's job

Followers (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- Maintain the same list of cron jobs as the leader, kept consistent via Paxos.
- On every "about to launch" record from the leader, **update their local next-scheduled-launch time** for that job. This keeps all replicas' schedules identical so no replica is "behind" in its view.
- Track **open launches** — launches that started but have not been marked complete. On leader failover, the new leader must resolve these.
- Stand ready to take over as leader on any of the usual failure modes: leader crash, network partition, rescheduling.

## The mutual-exclusion guarantee on the datacenter scheduler

One of the chapter's sharpest points: "as soon as [the leader] loses its leadership for any reason, it must immediately stop interacting with the datacenter scheduler. Holding the leadership should guarantee mutual exclusion of access to the datacenter scheduler. In the absence of this condition of mutual exclusion, the old and new leaders might perform conflicting actions on the datacenter scheduler" (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

This is exactly the scenario [[fencing-tokens]] is designed for in general distributed systems. A stale leader that thinks it still holds leadership but has actually been deposed could send a launch RPC to [[borg|Borg]], and the new leader — which thinks that same launch was never issued — could send another. Without explicit mutual exclusion at the datacenter scheduler level, the cron service would double-launch.

The service enforces this at the Paxos level (leadership ends the moment a new view is established and the process internally stops sending RPCs), and in practice the fast reaction time of Fast Paxos health checks — "within seconds" — keeps the window short. See [[multi-paxos]] on the general stable-leader pattern and its assumptions.

## Failover timing

Chapter 24's operational target: **under one minute** from leader loss to a new leader taking over (source: chapter-24-distributed-periodic-scheduling-with-cron.md). The reason is the cron scheduling granularity — one minute is the smallest scheduling interval crontab supports, so a failover longer than that would skip launches.

The Paxos group health-checking detects leader loss within seconds; a new leader is elected quickly because the other cron replicas are already running (not cold-started). The new leader then runs a **leader-election protocol specific to the cron service** — taking over all unfinished work from the previous leader. This cron-service-specific election is layered on top of the Paxos leader election: the same replica is both the Paxos leader and the cron-service leader, but the cron-service role has additional takeover responsibilities beyond what Paxos itself does.

## Why Fast Paxos specifically

The chapter doesn't dwell on why Fast Paxos rather than Multi-Paxos (source: chapter-24-distributed-periodic-scheduling-with-cron.md). The structural point is simply that Fast Paxos uses a leader replica internally, and the cron service reuses it. The [[fast-paxos|Fast Paxos]] page captures the general trade-offs (client-to-acceptor direct sends, batching difficulties, latency-tail sensitivity). Cron's workload — a small internal scheduler, low-volume state changes — is benign enough that Fast Paxos's batching disadvantage is not binding.

## Why this architecture is the right shape

Several alternative designs are rejected implicitly:

- **Multi-master launching** without consensus — would produce double launches.
- **Single-master without replication** — no failure tolerance; same as single-machine `crond`.
- **External state in a distributed filesystem** — dependency explosion; see [[cron-state-storage]].
- **Consensus outside the process** (e.g., calling into [[chubby|Chubby]]) — another dependency, and the state volume is small enough that in-process Paxos is cheap.

The leader-plus-Paxos shape is the minimum machinery that gets mutual-exclusion on launches, cross-replica consistency, and fast failover. It is also the generic shape of many Google internal control-plane services — cron is just one instance.

## Related pages

- [[distributed-cron]]
- [[cron-partial-failure-resolution]]
- [[cron-state-storage]]
- [[paxos]]
- [[multi-paxos]]
- [[fast-paxos]]
- [[stable-leader]]
- [[fencing-tokens]]
- [[replicated-state-machine]]
- [[failover]]
- [[borg]]
