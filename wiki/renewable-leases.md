# Renewable Leases

**Summary**: Long-running distributed ownership built by giving a lock a short TTL and refreshing it every `ttl/2` from a background thread — so ownership lasts as long as the holder is healthy, but a dead holder is replaced within one TTL interval rather than waiting for a fixed expiry.

**Sources**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## The problem with long TTLs

A [[distributed-locks-on-kv-stores|distributed lock]] with a short TTL is appropriate for transient critical sections. But many roles need ownership for the lifetime of the process — the active Kubernetes scheduler is Burns's canonical example (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

The naive solution — setting a very long TTL, say a week — fails when the owner crashes: a replacement cannot take over until the TTL expires, which could mean days of outage. A renewable lease solves this by keeping the TTL short and letting the owner extend it repeatedly.

## The mechanism

Add a `renew()` call that CAS-updates the key's TTL while keeping the value and expected resource version the same (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

```
func (Lock l) renew() boolean {
    locked, _ = compareAndSwap(l.lockName, "1", "1", l.version, ttl)
    return locked
}
```

Run this in a background thread every `ttl/2` seconds. The `ttl/2` cadence gives two full renewal attempts per TTL window, so one dropped renewal (network hiccup, brief scheduler delay) does not cause ownership loss (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

## Losing the lease

When `renew()` returns false, the lease is gone — either TTL expired faster than expected or another replica claimed it. The owner must call `handleLockLost()` (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

Burns's recommended implementation of `handleLockLost` is to **terminate the process** and let the orchestrator restart it. This is safe for three reasons (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. Some other replica has already grabbed the lease — there is no race to resume in-place work.
2. On restart, the former owner becomes a passive secondary that waits for the lease to next become free.
3. Termination is the only way to be sure no in-flight handlers continue acting on the (now-lost) ownership.

## Hands-on with etcd

The chapter demonstrates renewable leases with `etcdctl` using `--ttl=10` for the initial `mk` (create-if-absent) and repeated `set --ttl=10 --swap-with-value alice my-lock alice` calls every few seconds to refresh. "It may seem odd that Alice is continually rewriting her own name into the lock, but this is the way the lock lease is extended beyond the 10-second TTL." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

If a refresh fails, the next holder uses `mk` to claim the vacant key.

## Why the `ttl/2` cadence matters

The renewal period is a direct trade-off (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

- Too close to TTL — one dropped or slow renewal causes the owner to lose the lease unnecessarily
- Too short — wasted load on the KV store and the owner process

`ttl/2` is the standard choice. At TTL=10s, that is a refresh every 5s, tolerating one full missed refresh before ownership is at risk.

## Combined with owner validation

Even perfectly renewed leases suffer the "both-replicas-think-they're-master" window when the owner is paused past TTL. Burns's applied mitigation is for workers to validate the owner's identity and resource version against the KV store on every request — see [[distributed-locks-on-kv-stores]] and [[ownership-election-pattern]] for the scenario walk-through. This is the applied form of [[fencing-tokens]].

## Kubernetes as the worked example

The chapter's motivating use case is Kubernetes's highly available scheduler: multiple scheduler replicas run, exactly one holds a renewable lease in etcd, and only the lease-holder makes scheduling decisions. When the active scheduler loses its lease (crash, partition, pause), another replica takes over within one TTL — typically 10–15 seconds — and the former active becomes a passive secondary on restart (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

## Related pages

- [[distributed-locks-on-kv-stores]]
- [[ownership-election-pattern]]
- [[zookeeper]]
- [[fencing-tokens]]
- [[process-pauses]]
- [[failover]]
- [[designing-distributed-systems]]
