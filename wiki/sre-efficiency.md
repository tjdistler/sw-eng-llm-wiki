# SRE Efficiency and Performance

**Summary**: Resource use is a function of demand, capacity, and software efficiency. SRE controls the first two (via capacity planning and provisioning) and can modify the third (as software engineers), which makes efficiency one of the team's most consequential levers on total service cost.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`

**Last updated**: 2026-04-17

---

## The lever

> Paying close attention to the provisioning strategy for a service, and therefore its utilization, provides a very, very big lever on the service's total costs. (source: chapter-01-introduction.md)

Efficient use of resources matters any time the service cares about money. Because SRE owns [[provisioning]], SRE is necessarily involved in any work on utilisation — utilisation is a function of *how the service works* and *how it is provisioned* (source: chapter-01-introduction.md).

## The three factors

Resource use is a function of three things (source: chapter-01-introduction.md):

1. **Demand** (load) — forecast and managed through [[capacity-planning]].
2. **Capacity** — provisioned to meet demand at an acceptable response time. See [[provisioning]].
3. **Software efficiency** — how much work the service can do per unit of capacity. SRE can modify this, because SREs are software engineers.

These three factors are a large part of a service's efficiency (though not the entirety — the chapter is careful to hedge on this).

## Performance and capacity are linked

A subtle point Chapter 1 makes (source: chapter-01-introduction.md):

> Software systems become slower as load is added to them. A slowdown in a service equates to a loss of capacity. At some point, a slowing system stops serving, which corresponds to infinite slowness.

Because SREs provision to meet a capacity target *at a specific response speed*, they are keenly interested in performance. A regression that adds 20ms of latency is not just a UX issue; it's a capacity issue, because the service now serves fewer concurrent requests at the same response-time target.

## The dev-SRE collaboration

Performance work is inherently cross-functional. SREs *and* product developers should monitor and modify a service to improve its performance, *thus adding capacity and improving efficiency* (source: chapter-01-introduction.md). This is another place the shared intellectual background of [[sre-discipline|SRE's hiring model]] pays off — both groups can read the same code and propose the same kind of change.

## Related pages

- [[sre-tenets]]
- [[capacity-planning]]
- [[provisioning]]
- [[scaling-approaches]]
- [[response-time-percentiles]]
