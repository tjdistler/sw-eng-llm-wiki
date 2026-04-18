# Testing Automation Tools

**Summary**: Automation tools (database index selection, cross-datacenter load balancing, log shuffling for remastering) perform operations against well-tested APIs, but their **purpose is a side effect invisible to another API client**. Testing them means demonstrating the *other* layer's desired behaviour both before and after the change — and managing the circular dependency that arises when one automation tool changes the environment of another.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Two defining characteristics

Chapter 17's framing of automation tools (source: chapter-17-testing-for-reliability.md):

- The actual operation performed is against a **robust, predictable, well-tested API**.
- The purpose of the operation is a **side effect that is an invisible discontinuity to another API client**.

The database's read path still returns correct answers; the user query still succeeds. What the automation changed — a new index, a new leader, a drained replica — only matters to the *other* layer (the query planner's choice, the replication topology) and only across the discontinuity of the automation's action.

## What testing must show

> Testing can demonstrate the desired behavior of the other service layer, both before and after the change. It's often possible to test whether internal state, as seen through the API, is constant across the operation. For example, databases pursue correct answers, even if a suitable index isn't available for the query. (source: chapter-17-testing-for-reliability.md)

The assertion shape: **pre-condition from the other client's point of view + post-condition from the other client's point of view + invariant spanning the automation's action**.

## When documented invariants don't hold across the change

Not every documented API invariant survives an automation tool's action (source: chapter-17-testing-for-reliability.md):

> Some documented API invariants (such as a DNS cache holding until the TTL) may not hold across the operation. For example, if a runlevel change replaces a local nameserver with a caching proxy, both choices can promise to retain completed lookups for many seconds. It's unlikely that the cache state is handed over from one to the other.

The tests need to enumerate these transients and verify the system recovers from them. Adjacent binaries may themselves need additional release tests to handle environmental transients the automation introduces.

## The circular-dependency problem

> After all, the automation for shuffling containers to improve usage is likely to try to shuffle itself at some point if it also runs in a container. It would be embarrassing if a new release of its internal algorithm yielded dirty memory pages so quickly that the network bandwidth of the associated mirroring ended up preventing the code from finalizing the live migration. (source: chapter-17-testing-for-reliability.md)

Automation tools that act on the environment they run in can produce interaction failures that integration tests won't see at a realistic scale (container counts, intercontinental bandwidth). Worse:

> One automation tool might be changing the environment in which another automation tool runs. Or both tools might be changing the environment of the other automation tool simultaneously! (source: chapter-17-testing-for-reliability.md)

The fleet-upgrade tool consumes the most resources while pushing upgrades; the container rebalancer is therefore tempted to move it; the rebalancer itself needs upgrading. The circular dependency is fine **if** (source: chapter-17-testing-for-reliability.md):

- Associated APIs have restart semantics.
- Someone remembered to implement test coverage for those semantics.
- Checkpoint health is assured independently.

Three conditions, any of which being missed can produce a production surprise.

## Cross-book connections

- [[automation-at-google]] / [[autonomous-systems]] (Ch 7) — Ch 17 is the testing counterpart of Ch 7's automation hierarchy; tools at the autonomous end need the strongest testing because their feedback loops run without human gates
- [[automation-gone-wrong]] (Ch 7) — the Diskerase incident is a canonical example of an automation tool whose inputs were not adequately tested against environmental transients
- [[idempotence]] — the "restart semantics" precondition; idempotence at the workflow level is what makes the circular-dependency case testable
- [[prodtest]] (Ch 7) — an early SRE automation-test pattern that applied unit-test discipline to cluster state; Chapter 17 generalises the idea

## Related pages

- [[testing-for-reliability]]
- [[testing-scalable-tools]]
- [[barrier-defenses]]
- [[automation-at-google]]
- [[automation-gone-wrong]]
- [[idempotence]]
