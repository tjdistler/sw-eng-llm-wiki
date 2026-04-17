# Singleton Pattern

**Summary**: The simplest form of ownership — run exactly one replica of the service and let the container orchestrator restart it on failure. Cheaper than master election and good enough for three to four nines of uptime, but bounded by upgrade windows and machine-failure detection time.

**Sources**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## The argument

Burns opens his chapter on [[ownership-election-pattern|ownership election]] with an unusually honest "do you even need this?" section. The simplest form of ownership is a single replica. Since there is only one instance running, it implicitly owns everything without any election protocol (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

The singleton's advantage is simplicity of application code and deployment. The cost is downtime during failures and during upgrades. Whether that trade-off is acceptable depends on the SLA.

## What an orchestrator gives you for free

A singleton running under Kubernetes (or an equivalent orchestrator) inherits three automatic recovery behaviours (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. If the container crashes, it is automatically restarted
2. If the container hangs and you implement a health check (see [[health-probes]]), it is automatically restarted
3. If the machine fails, the container is moved to a different machine

The orchestrator is, in effect, acting as a degenerate lock service — it guarantees at most one replica at a time and restarts the replica on failure. For many workloads that is sufficient.

## Burns's uptime arithmetic

Assuming one container crash per day and a roughly two-second restart time, a singleton achieves about 99.99% uptime — four nines (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). Less frequent crashes push it higher.

Machine failure is the worse case. Kubernetes takes roughly five minutes to decide a machine is gone and reschedule. If every machine in the cluster failed once a day, the singleton would achieve two nines — but as Burns notes, "if every machine in your cluster fails every day, then you have way worse problems than the uptime of your master-elected service." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

Note that the ~5 minute figure is the default *node death detection* window — the orchestrator waiting on missed heartbeats before declaring the node dead and rescheduling its pods. By contrast, a [[renewable-leases]]-based ownership handoff runs at TTL granularity (typically 10–15 seconds), because a failed lease-holder's lease simply expires and a standby grabs it. This is precisely why [[ownership-election-pattern]] is preferred over the singleton when fast failover matters: the orchestrator's node-health loop is far too coarse to provide sub-minute failover on its own.

## The upgrade window is the real constraint

Rollouts are the binding constraint on singleton uptime. A singleton cannot run old and new versions concurrently: the old must be stopped before the new starts. If an upgrade takes two minutes and you deploy daily, your theoretical ceiling is two nines. Hourly deploys push you below one nine (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

Burns acknowledges that image pre-pulling and similar tricks can reduce the upgrade window to seconds, but the added complexity undercuts the simplicity argument that motivated the singleton in the first place (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

## When the singleton is the right call

Burns's canonical example is background asynchronous processing — daily report generation, off-hours batch work, non-interactive telemetry aggregation. These workloads tolerate minutes of unavailability and do not benefit from the architectural cost of proper leader election (source: raw/designing-distributed-systems/chapter-09-ownership-election.md).

The thesis generalises: "One of the key components of designing a distributed system is deciding when the 'distributed' part is actually unnecessarily complex." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

## When it isn't enough

Four-plus nines of availability, or an SLA that cannot accept multi-minute upgrade gaps, push you toward running multiple replicas with only one actively owning the work at any moment. That is the [[ownership-election-pattern]] proper, built on [[distributed-locks-on-kv-stores]] and [[renewable-leases]].

## Relationship to existing patterns

- [[health-probes]] — the readiness/liveness probes that let the orchestrator make its restart decisions correctly
- [[desired-state-management]] — the orchestrator's declarative-spec-plus-reconciliation model is what makes the singleton's implicit recovery work
- [[replicated-load-balanced-service]] — the N-replica counterpart when every replica can handle any request; singleton is the degenerate N=1 case *with* the constraint that it must be exactly 1

## Related pages

- [[ownership-election-pattern]]
- [[health-probes]]
- [[desired-state-management]]
- [[replicated-load-balanced-service]]
- [[reliability]]
- [[designing-distributed-systems]]
