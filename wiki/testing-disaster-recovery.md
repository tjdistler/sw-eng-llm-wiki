# Testing Disaster Recovery

**Summary**: Chapter 17 splits disaster-recovery tooling into two categories with sharply different testing profiles: **offline tools** that compute a checkpoint, push it, and trigger a clean start are straightforward to test (constrained shape, excellent coverage); **online repair tools** operate outside the mainstream API and interact with the eventual-consistency behaviour of a live system, making them significantly harder to test with confidence.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`, `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## Offline disaster-recovery tools

Chapter 17's tractable category (source: chapter-17-testing-for-reliability.md):

> Many disaster recovery tools can be carefully designed to operate offline. Such tools do the following:
> - Compute a checkpoint state that is equivalent to cleanly stopping the service
> - Push the checkpoint state to be loadable by existing nondisaster validation tools
> - Support the usual release barrier tools, which trigger the clean start procedure

When the tool respects these constraints — **offline, checkpoint-producing, loadable, barrier-supporting, clean-start-triggering** — the associated tests are easy to write and offer excellent coverage. The checkpoint is a comparable artifact; the load step is idempotent; the start is the existing healthy-start procedure.

## When any constraint breaks

> If any of the constraints (offline, checkpoint, loadable, barrier, or clean start) must be broken, it's much harder to show confidence that the associated tool implementation will work at any time on short notice. (source: chapter-17-testing-for-reliability.md)

The shape of the problem: the constraints define a small, well-understood subset of the system's state space that a test can cover. Breaking any one of them pushes the tool into the full state space, where coverage becomes exponentially harder.

## Online repair tools

> Online repair tools inherently operate outside the mainstream API and therefore become more interesting to test. One challenge you face in a distributed system is determining if normal behavior, which may be eventually consistent by nature, will interact badly with the repair. (source: chapter-17-testing-for-reliability.md)

Two forces combine to make testing online repair hard:

- **Outside the mainstream API**. The tool isn't covered by the normal service's tests; it has its own assumptions about state that the service doesn't enforce.
- **Eventual consistency**. The state the tool reads may not reflect the state as any other actor sees it. A repair that's correct against one consistent view can be wrong against another.

Chapter 17's concrete example: a race condition that the analysis tries to study with offline tools. Offline tools are typically written to expect instant consistency (easier to reason about and test), but the actual system is eventually consistent. The result:

> This situation becomes complicated because the repair binary is generally built separately from the serving production binary that it's racing against. Consequently, you might need to build a unified instrumented binary to run within these tests so that the tools can observe transactions. (source: chapter-17-testing-for-reliability.md)

The test architecture ends up needing a **merged binary** instrumented so the repair and serving paths share a transaction view. That's expensive engineering, and the chapter flags it as the realistic cost of testing online repair honestly.

## Chapter 26's continuous-recovery-testing requirement

Chapter 17 covers the testing economics; Chapter 26 makes the operational demand explicit for data-recovery tools specifically (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Continuously test the recovery process as part of your normal operations. Set up alerts that fire when a recovery process fails to provide a heartbeat indication of its success.

If recovery tests are manual staged events, they become drudgery that isn't performed deeply or frequently enough to earn confidence. **Automate them and run them continuously.** See [[recovery-testing]] for the full discipline. The two Chapter 26 case studies ([[gmail-gtape-restore]] and [[google-music-runaway-deletion]]) both explicitly credit prior DiRT-tested recovery tooling with making their actual recoveries tractable. The recovery tools were in Ch 17's **offline** category (the tractable one), which is why they were testable enough to be tested continuously, which is why they worked when needed.

The composition: Ch 17 tells you which recovery tools are structurally testable; Ch 26 tells you how often you must exercise them.

## DiRT in the cross-industry catalogue (Chapter 33)

Chapter 33 places DiRT inside a much older family of preparedness practices (source: chapter-33-lessons-learned-from-other-industries.md):

> Google's Disaster Recovery tests have a lot in common with the simulations and live drills that are a key focus of many of the established industries we researched. The potential consequences of a system outage determine whether using a simulation or a live drill is appropriate.

The relevant cross-industry analogues:

- **US nuclear Navy live drills** — 2-3 days per week, *"actually breaking real stuff but with control parameters."* The cadence is calibrated to the failure cost (catastrophic) and the consequence of forgetting the response (you have to keep practicing or the muscle dies)
- **Aviation simulators** — the *can't test in production* extreme: simulators with live data feeds, control rooms modeled to the smallest detail, because passengers can't be put at risk
- **Lifeguard mystery-shopper drownings** — staged to be indistinguishable from the real thing; lifeguards can't differentiate real and staged, so the practice transfers directly
- **Telecom weather drills** — surviving hurricanes and other weather emergencies; led to weatherproof facilities with on-site generators sized to outlast a storm

DiRT sits in the *live-drill* half of this taxonomy (real production systems, real failures induced) rather than the *simulation* half (which is occupied by [[disaster-role-playing|Wheel of Misfortune]]). Both are needed because they expose different failure-mode classes; see [[preparedness-and-disaster-testing]] for the full Chapter 33 framing.

## Cross-book connections

- [[failover]] (Kleppmann) — Kleppmann's catalogue of failover failure modes is the space online repair tools have to navigate; the operational response is online repair tooling
- [[eventual-consistency]] (Kleppmann) — the property that makes online repair hard to test; Chapter 17 surfaces the cost from the testing side
- [[mysql-on-borg]] (Ch 7) — Decider is an example of the opposite choice: replace a human operator with an automated system whose repairs are mostly checkpoint-and-promote style (offline-ish), not online repair
- [[process-induced-emergency]] (Ch 13) — the Diskerase three-day phased manual rebuild is a production-scale demonstration of why online repair at fleet scale is structurally hard; Ch 17 explains the testing reason
- [[data-integrity-sre]] (Ch 26) — the data-recovery tools Chapter 17 categorises must themselves be exercised continuously; Chapter 26 makes that the default discipline

## Related pages

- [[testing-for-reliability]]
- [[testing-scalable-tools]]
- [[testing-automation-tools]]
- [[statistical-testing-techniques]]
- [[recovery-testing]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[tiered-backup-strategy]]
- [[gmail-gtape-restore]]
- [[google-music-runaway-deletion]]
- [[lessons-from-other-industries]]
- [[preparedness-and-disaster-testing]]
