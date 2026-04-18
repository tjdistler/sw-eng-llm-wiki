# Barrier Defenses

**Summary**: A design pattern for safely running risky SRE-developed software that must bypass the normal heavily-tested API (for example, batch updates that temporarily disable database transactions). A separately-managed barrier in the replication configuration makes selected replicas fail health checks; risky software is configured to operate **only** on unhealthy replicas; a separately-managed validating tool removes the barrier once the work is done.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The failure mode being defended against

> Software that bypasses the usual heavily tested API (even if it does so for a good cause) could wreak havoc on a live service. For example, a database engine implementation might allow administrators to temporarily turn off transactions in order to shorten maintenance windows. If the implementation is used by batch update software, user-facing isolation may be lost if that utility is ever accidentally launched against a user-facing replica. (source: chapter-17-testing-for-reliability.md)

The dangerous property: a tool that's safe against quiesced replicas but destructive against live ones, and where the runtime does not automatically tell the tool which it's looking at.

## The three-tool pattern

Chapter 17's design (source: chapter-17-testing-for-reliability.md):

1. **Use a separate tool** to place a barrier in the replication configuration so the replica cannot pass its health check. As a result, the replica isn't released to user traffic.
2. **Configure the risky software** to check for the barrier upon startup. Allow the risky software to only access unhealthy replicas.
3. **Use the replica-health-validating tool** (the same one used for black-box monitoring) to remove the barrier when the work is complete.

The **separation of concerns** is what makes this testable. Each of the three tools is simple, has a single job, and can be tested independently. The composition — barrier set, work done, barrier removed — produces the safe-by-construction behaviour.

## Why the barrier belongs in a different tool

If the risky software also manages its own barrier, a bug in its barrier logic is a bug in its destruction safety. By pinning the barrier to a **separate tool with a different release cadence and different owner**, the safety property doesn't depend on the risky software being correct.

The same logic applies at the other end: using the production health-validation tool (the one that already gates user traffic) to remove the barrier means "barrier removed" has the same meaning as "replica is healthy enough for users" — one policy, one implementation.

## Cross-book connections

- [[bulkhead]] (Newman) — the same pattern at a different scale; bulkheads keep bad actors isolated to compartments by construction
- [[blue-green-deployment]] — conceptually similar: the "blue" environment is invisible to users because a separate traffic-routing tool says so, not because the software itself knows
- [[deployment-vs-release]] (Newman) — the barrier mechanism is a deployment-vs-release separation for the risky-tool case: the replica may be deployed, but is not released to user traffic until the barrier lifts
- [[change-management-sre]] — the progressive-rollout leg of the automation trio; barrier defenses are the risky-tool-specific realisation

## Related pages

- [[testing-for-reliability]]
- [[testing-scalable-tools]]
- [[testing-automation-tools]]
- [[black-box-vs-white-box-monitoring]]
