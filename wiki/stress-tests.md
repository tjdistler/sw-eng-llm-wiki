# Stress Tests

**Summary**: A production test whose job is to **find the limits** of a system and its components. Unlike [[performance-tests]], which guard against gradual degradation, stress tests deliberately push a component past its safe operating point to discover where it breaks — because in many cases components don't degrade gracefully, they fail catastrophically.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> In order to safely operate a system, SREs need to understand the limits of both the system and its components. In many cases, individual components don't gracefully degrade beyond a certain point — instead, they catastrophically fail. Engineers use stress tests to find the limits on a web service. (source: chapter-17-testing-for-reliability.md)

Example questions stress tests answer (source: chapter-17-testing-for-reliability.md):

- How full can a database get before writes start to fail?
- How many queries per second can be sent to an application server before it becomes overloaded?

## Why "catastrophic failure" matters

A system with graceful degradation gives operators time — saturation metrics climb, latency rises, pages fire, humans intervene. A system with catastrophic failure gives them no warning: operating well, operating well, falling off a cliff. Stress tests are the mechanism by which the cliff is located before production finds it.

## Cross-book connections

- [[capacity-planning]] — stress tests produce the capacity ceilings capacity planning uses as its operational constraint
- [[four-golden-signals]] — the *saturation* signal is the one stress tests most directly calibrate; leading-indicator tail latency gets its thresholds from stress-test data
- [[operational-overload]] (Ch 11) — when stress-test data doesn't inform capacity planning, teams discover their limits by living through them on-call

## Related pages

- [[testing-for-reliability]]
- [[performance-tests]]
- [[canary-test]]
- [[capacity-planning]]
- [[four-golden-signals]]
