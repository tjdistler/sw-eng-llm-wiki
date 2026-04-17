# Distributed Locks on KV Stores

**Summary**: Burns's applied recipe for building a correct distributed mutex on top of a consensus-backed key-value store (etcd, ZooKeeper, Consul) using three primitives: atomic compare-and-swap, key TTL, and per-write resource versions.

**Sources**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## Why build locks yourself?

The underlying stores — etcd, [[zookeeper]], Consul — already implement [[consensus]] correctly. What they don't provide out of the box is the full lock abstraction: acquire-or-block, ownership renewal, safe unlock, and protection against the stale-owner writing after timeout. Burns constructs each of these, layer by layer, to show where the subtle bugs live (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

This page captures the construction. The concepts overlap heavily with DDIA's theoretical coverage on [[consensus]], [[linearizability]], [[fencing-tokens]], and [[truth-and-leadership-in-distributed-systems]]; this page is the applied container-level companion.

## The two primitives you need from the store

Every KV store that can back a distributed lock exposes two operations (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. **Atomic compare-and-swap (CAS)** on a key: write `nextValue` only if the current value equals `expectedValue`. Return `false` otherwise. This is a [[linearizability|linearizable]] operation in the theoretical sense.
2. **Time-to-live (TTL)** on a key: once the TTL expires, the key is cleared.

Everything — locks, leases, ownership, fencing — derives from those two.

## Naive lock — simple and broken

Start with a key whose value is `"0"` (unlocked) or `"1"` (held). To acquire:

```
func (Lock l) simpleLock() boolean {
    locked, _ = compareAndSwap(l.lockName, "1", "0")
    return locked
}
```

To handle the case where the lock key doesn't exist yet, try a second CAS against nil. Then block the caller in a polling loop (or, better, a change-watch) until `simpleLock` returns true (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

This works right up until a holder crashes before calling `unlock`. The key stays `"1"` forever and the lock becomes permanently stuck.

## Adding TTL — still broken

Write every CAS with a TTL so the lock self-releases if the holder disappears. Now a crashed holder stops blocking the world. But a new bug has appeared (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. Process-1 acquires the lock with TTL t.
2. Process-1 runs slowly (overload, GC, etc.) for longer than t.
3. The lock expires.
4. Process-2 acquires the lock.
5. Process-1 finishes and calls `unlock` — which CAS-swaps the value back to `"0"`, releasing a lock it no longer holds.
6. Process-3 acquires the lock.

Now Process-2 and Process-3 both believe they own it.

This is the same pathology DDIA describes in [[process-pauses]] and [[truth-and-leadership-in-distributed-systems]]: a paused node cannot know it has been demoted.

## Adding resource versions — now safe under TTL

The fix: the KV store returns a monotonically increasing **resource version** with every write. Store the version returned when you acquired the lock, and include it in the `unlock` CAS as an additional precondition (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

```
func (Lock l) simpleLock() boolean {
    locked, l.version, error = compareAndSwap(l.lockName, "1", "0", l.ttl)
    if error != null {
        locked, l.version, _ = compareAndSwap(l.lockName, "1", null, l.ttl)
    }
    return locked
}

func (Lock l) unlock() {
    compareAndSwap(l.lockName, "0", "1", l.version)
}
```

Now `unlock` fails cleanly if TTL expiry has already caused the lock to change hands. The resource version is structurally a [[fencing-tokens|fencing token]] — Burns derives it from first principles without naming it as such. In ZooKeeper this role is played by the **zxid** or **cversion**; in etcd by the mod revision.

## Watchdog timers

Even with correct unlock semantics, the guarded code can over-run its TTL. Burns recommends a **watchdog timer**: a separate timer set at lock-acquisition time that crashes the process if TTL elapses before the critical section finishes and calls `unlock` (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). Crashing is the safe move because the orchestrator will restart the process, and in the meantime some other replica will have acquired the lock.

## Beyond locks: leases and ownership

A lock is transient: acquire, work, release, done. Many real roles (Kubernetes active scheduler, active replica in a hot-standby pair) need ownership for the lifetime of the process — see [[renewable-leases]]. The construction is the same lock plus a periodic `renew()` that re-CAS-es the key with a refreshed TTL.

## Beyond locks: validating the owner at the resource

Even a correct lock construction permits brief "both think they're master" windows when the old master is paused past TTL but not yet crashed. Burns's mitigation is **server-side owner validation** at the worker: the lock's current holder name (plus resource version) is sent with every request; the worker verifies both against the KV store before executing. A request carrying a stale version is rejected even if the key's current value is somehow equal by coincidence. See [[ownership-election-pattern]] for the full scenario walk-through (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

This pattern is the applied version of what DDIA names [[fencing-tokens]].

## Hands-on with etcdctl

The chapter demonstrates the whole construction on the command line with `etcdctl`'s `--swap-with-value` (for CAS) and `--ttl` (for TTL) flags, and `mk` (for create-if-absent) (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). Any real implementation would use one of the etcd client libraries in a programming language rather than `etcdctl`.

## Relationship to the theoretical coverage

- [[consensus]] — the KV store's CAS is made [[linearizability|linearizable]] by the store's internal consensus protocol; you are consuming consensus, not implementing it
- [[zookeeper]] — the same construction with ZooKeeper-specific primitives (ephemeral nodes, zxid, watches); ZooKeeper's ephemeral nodes automate the TTL-on-crash story
- [[fencing-tokens]] — Burns's resource-version-on-every-write is the applied form of the DDIA concept
- [[process-pauses]] — why the TTL-without-version version is broken
- [[truth-and-leadership-in-distributed-systems]] — why a lock holder cannot trust its own belief that it still holds the lock

## Related pages

- [[ownership-election-pattern]]
- [[renewable-leases]]
- [[zookeeper]]
- [[consensus]]
- [[fencing-tokens]]
- [[truth-and-leadership-in-distributed-systems]]
- [[process-pauses]]
- [[linearizability]]
- [[designing-distributed-systems]]
