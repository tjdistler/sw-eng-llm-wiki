# Ownership Election Pattern

**Summary**: Burns's fifth and final serving pattern: when a task must have exactly one owner across a replicated service, use a distributed key-value store (etcd, ZooKeeper, Consul) to elect a master and hand off ownership safely when that master fails.

**Sources**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## What the pattern scales

The previous serving patterns all distributed something different: [[replicated-load-balanced-service]] distributes *requests per second*, [[sharded-service-pattern]] distributes *state*, [[scatter-gather-pattern]] distributes *time to process a request*, [[functions-as-a-service]] distributes *events*. Ownership election is the pattern for distributing **assignment** — the problem of deciding which replica owns a particular task at a particular time (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

Burns frames the problem like this. On a single machine, in-process mutexes are enough to guarantee that only one actor owns a given task at a time. But a single-process owner is neither scalable (the task can't be replicated) nor reliable (if the process fails, the task is unavailable until it restarts). When ownership is genuinely required in a distributed system, you need a distributed protocol for establishing and transferring it. "Often, establishing distributed ownership is both the most complicated and most important part of designing a reliable distributed system." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

## The diagram the chapter opens with

Three replicas are eligible to own some task. Replica 1 is the initial master. Replica 1 fails. Replica 3 takes over. Replica 1 eventually recovers and rejoins the group — but replica 3 remains master. A new master is not chosen merely because the old one came back. (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

That last point matters operationally: the pattern does not oscillate, and a returning former-leader becomes a passive secondary waiting for the next handoff.

## First: do you actually need it?

Burns spends the opening section making an unusually honest argument that **most systems don't need master election at all** (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). See [[singleton-pattern]] — a single replica running under a container orchestrator already gets:

- automatic restart on crash or health-check failure
- automatic machine-level failover (slower, but still bounded)
- roughly three to four nines of uptime if the container crashes once a day

The complexity of master election is warranted only when you need four or more nines *and* cannot accept the singleton-pattern upgrade window (during a rollout, the old singleton must be stopped before the new one starts). This is a real architectural decision, not a default. Background asynchronous processing is Burns's canonical example of a workload where a singleton is fine.

## How election is actually built

Two paths exist in principle (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. **Implement a consensus algorithm** (Paxos, Raft, Zab) yourself. Burns flatly discourages this: "akin to implementing locks on top of assembly code compare-and-swap instructions. It's an interesting exercise for an undergraduate computer science course, but it is not something that is generally worth doing in practice."
2. **Outsource consensus** to a distributed key-value store — etcd, [[zookeeper]], or Consul — that has already implemented a fault-tolerant [[consensus]] algorithm and exposes two primitives sufficient for election:
   - atomic compare-and-swap on a key
   - time-to-live (TTL) on a key, so values clear themselves if the owner disappears

Everything else — locks, leases, ownership, fencing — is built on top of those two primitives. See [[distributed-locks-on-kv-stores]] for the construction.

## Ownership vs locks: the lease

Burns distinguishes two scopes (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

- **Locks** are transient: grab, work, release. Reasonable TTL is a few seconds to a few minutes.
- **Ownership** is persistent: hold the role for as long as the process is running. A Kubernetes active scheduler holds ownership for days at a time.

You don't solve ownership by making the TTL very long — that would mean a week-long outage if the owner died. Instead you use a [[renewable-leases|renewable lease]]: a short TTL that the owner refreshes every `ttl/2` from a background thread. If refresh fails, the owner voluntarily terminates and lets the orchestrator restart it; in the meantime, some other replica has already grabbed the lease. "This is safe, because some other replica has grabbed the lock in the interim, and when the restarted application comes back online it will become a secondary listener waiting for the lock to become free." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

## Two replicas can briefly both believe they are master

Even correctly implemented leases can produce a window — usually very brief — where the old and new master both think they hold ownership. Burns's scenario (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. The machine holding the lease is so overloaded its OS stops scheduling the process.
2. The lease expires; another replica acquires it.
3. The original process finally resumes scheduling and runs its work, still believing it is master.

This is the same pathology DDIA covers under [[process-pauses]] and [[truth-and-leadership-in-distributed-systems]]: a node cannot tell whether it has been paused and demoted. Burns's applied mitigations combine three defences (see [[fencing-tokens]] for the DDIA-native treatment):

1. **Client-side self-check** before any action: call `isLocked()` comparing the local lock-acquired time against `0.75 * ttl`. Reduces but does not eliminate the race.
2. **Server-side owner validation**: the workers the master sends requests to check with the KV store that the requester is the current owner before executing (Burns's Figure 9-2).
3. **Resource versions on every request**: the master includes the KV-store's per-write resource version with each outbound request; the worker rejects any request whose version is not the current one. This closes the subtle "obtained, lost, re-obtained, delayed message arrives" window.

The resource-version mechanism is structurally identical to DDIA's [[fencing-tokens]] (the zxid or cversion in ZooKeeper). Burns derives it from first principles rather than naming it as such.

## Hands-on: etcd on Kubernetes

The chapter's worked deployment uses Helm and the CoreOS etcd [[operator-pattern|operator]] to stand up a three-replica etcd cluster in Kubernetes, then uses `etcdctl` with the `--swap-with-value` and `--ttl` flags to demonstrate a lock with and without a lease (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). The operator owns the cluster's lifecycle — creation, scaling, upgrade — and is itself an application of [[desired-state-management]].

## Relationship to the other serving patterns

Where [[sharded-service-pattern]] partitions state and [[hot-sharding]] rebalances replicas, ownership election decides **which** replica is currently authoritative for a given shard when only one can be. The two patterns compose: a sharded service may elect a master per shard via etcd so that shard rebalancing, compaction, or write coordination has a well-defined owner. Burns gestures at this in his opening paragraph — "we have previously seen this in the context of sharded and hot-sharded systems" — without expanding the intersection (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

Ownership election is also what makes other serving patterns fault-tolerant at the control plane: the active Kubernetes scheduler is a singleton elected from a pool, which is the book's canonical long-running-ownership example (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

## Relationship to DDIA coverage

The DDIA corpus already covers the theory thoroughly:

- [[consensus]] — the underlying agreement problem; Paxos/Raft/Zab
- [[zookeeper]] — the coordination-service family Burns treats interchangeably with etcd and Consul
- [[total-order-broadcast]] — the primitive consensus provides
- [[linearizability]] — what the KV-store's compare-and-swap gives you
- [[fencing-tokens]] — the resource-version mechanism Burns reinvents applied
- [[truth-and-leadership-in-distributed-systems]] — why a node can't trust its own judgment
- [[failover]] — leader promotion and its many edge cases
- [[process-pauses]] — why the "both-masters" window exists

Burns's contribution is the **container-level implementation recipe**: which store to deploy, what the lock/lease/owner abstractions look like when you build them, what the defences against pause-induced split ownership look like in practice, and how it all sits inside a Kubernetes cluster.

## Related pages

- [[singleton-pattern]]
- [[distributed-locks-on-kv-stores]]
- [[renewable-leases]]
- [[operator-pattern]]
- [[consensus]]
- [[zookeeper]]
- [[fencing-tokens]]
- [[truth-and-leadership-in-distributed-systems]]
- [[failover]]
- [[process-pauses]]
- [[linearizability]]
- [[desired-state-management]]
- [[sharded-service-pattern]]
- [[designing-distributed-systems]]
