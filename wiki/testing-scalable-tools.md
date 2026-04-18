# Testing Scalable Tools

**Summary**: SRE-developed tools are themselves software and need their own testing. Chapter 17 identifies two subclasses — general SRE tools (metric collection, capacity prediction, replica-data refactors, file edits) and automation tools (index selection, datacenter load balancing, log shuffling) — with shared characteristics that constrain how their tests are structured.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Examples of SRE tools

Chapter 17 lists representative SRE-developed tools (source: chapter-17-testing-for-reliability.md):

- Retrieving and propagating database performance metrics
- Predicting usage metrics to plan for capacity risks
- Refactoring data within a service replica that isn't user accessible
- Changing files on a server

Their shared characteristics:

- Side effects remain within the tested mainstream API.
- They are isolated from user-facing production by an existing validation and release barrier.

The second property is load-bearing. SRE tools typically don't interact with production directly — they go through the same release pipeline, canary, and rollout gates as user-facing software. Their testing can therefore mostly follow the traditional pattern: unit, integration, system tests in hermetic environments.

## The exception: automation tools

Automation tools are different. Examples (source: chapter-17-testing-for-reliability.md):

- Database index selection
- Load balancing between datacenters
- Shuffling relay logs for fast remastering

Their shared characteristics:

- The actual operation performed is against a robust, predictable, well-tested API.
- The purpose of the operation is a **side effect that is an invisible discontinuity to another API client**.

That second property is where testing gets subtle. See [[testing-automation-tools]] for the full treatment.

## Barrier defenses for risky software

Some SRE tools deliberately bypass the normal, heavily-tested API — for example, a batch update utility that temporarily disables database transactions to shorten a maintenance window. Running such a tool against a live user-facing replica could cause havoc. The chapter's design defense is the **barrier pattern**, which keeps risky tools away from healthy replicas by construction. See [[barrier-defenses]].

## Disaster-recovery tools

Disaster recovery tools are a third subclass with their own testing discipline. Offline tools (checkpoint, push, trigger clean start) have reasonable test paths; online repair tools operate outside the mainstream API and are harder to test, especially under eventual consistency. See [[testing-disaster-recovery]].

## Scope note

Chapter 17 explicitly scopes out non-scalable SRE tools — tools that don't need to be scalable have a risk footprint similar to user-facing applications, and the same testing strategies apply. The chapter focuses on the scalable ones because their testing needs are distinctive (source: chapter-17-testing-for-reliability.md).

## Related pages

- [[testing-for-reliability]]
- [[testing-automation-tools]]
- [[barrier-defenses]]
- [[testing-disaster-recovery]]
- [[statistical-testing-techniques]]
