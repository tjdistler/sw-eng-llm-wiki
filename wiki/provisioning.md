# Provisioning

**Summary**: The act of bringing new capacity online — new instances, new locations, the associated configuration and load-balancer changes, and validation that it works. Combines [[change-management-sre|change management]] and [[capacity-planning]]; must be done quickly, only when necessary, and correctly.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`

**Last updated**: 2026-04-17

---

## Where provisioning sits

Chapter 1 identifies provisioning as the intersection of two other tenets (source: chapter-01-introduction.md):

- [[capacity-planning]] says *how much* capacity to bring up and *when*.
- [[change-management-sre]] says *how to do it safely*.
- Provisioning is the execution that combines the two.

## The SRE stance: quickly, and only when necessary

Two competing pressures shape the SRE approach (source: chapter-01-introduction.md):

- **Quickly** — capacity that arrives late is useless. If the forecast said November and you provision in January, you've already failed.
- **Only when necessary** — capacity is expensive. Over-provisioning is a real cost, both in direct spend and in the maintenance overhead of running more machines than the service actually needs.

The *and correctly* is non-negotiable: capacity that's wrongly configured doesn't work when called on, which is worse than not having it.

## Why it's riskier than load shifting

Chapter 1 is explicit that provisioning is more dangerous than routine operational work (source: chapter-01-introduction.md):

> Adding new capacity often involves spinning up a new instance or location, making significant modification to existing systems (configuration files, load balancers, networking), and validating that the new capacity performs and delivers correct results. Thus, it is a riskier operation than load shifting, which is often done multiple times per hour, and must be treated with a corresponding degree of extra caution.

Load shifting is rebalancing within existing capacity; provisioning adds new capacity and therefore touches more moving parts. Every modification is an opportunity to break something.

## Validation as part of provisioning

A point easy to miss: provisioning is not complete until the new capacity has been *validated* — it performs and delivers correct results. A new instance that's up but silently returning wrong answers is worse than no new instance at all. This is one of the places the [[change-management-sre|three automation practices]] apply within provisioning itself: progressive rollout (route a little traffic first), detection (does it respond correctly?), rollback (remove it if not).

## Related pages

- [[capacity-planning]]
- [[change-management-sre]]
- [[sre-tenets]]
- [[sre-efficiency]]
- [[scaling-approaches]]
