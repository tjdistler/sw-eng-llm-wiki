# Capacity Planning

**Summary**: Ensuring there is sufficient capacity and redundancy to serve projected future demand with the required availability. Nothing conceptually exotic — but a surprising number of teams skip it. SRE owns capacity planning because availability depends on it.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The idea

Capacity planning is the discipline of making sure capacity arrives *before* demand does. Chapter 1's dry observation: *there's nothing particularly special about these concepts, except that a surprising number of services and teams don't take the steps necessary to ensure that the required capacity is in place by the time it is needed* (source: chapter-01-introduction.md).

## Organic vs inorganic demand

Demand comes from two sources, and capacity planning has to account for both (source: chapter-01-introduction.md):

- **Organic growth** — natural product adoption and usage increase by customers. Smooth, extrapolatable from history.
- **Inorganic growth** — feature launches, marketing campaigns, business-driven events. Lumpy, specific to planned events, known only to the product side.

Miss either and your forecast is wrong. Organic forecasts alone leave you unprepared for a big launch; inorganic-only planning misses the slow-creeping baseline that eats capacity while nobody's watching.

## The mandatory steps

Chapter 1 lists three steps as non-negotiable (source: chapter-01-introduction.md):

1. **An accurate organic demand forecast** that extends beyond the lead time required for acquiring capacity.
2. **An accurate incorporation of inorganic demand sources** into the forecast.
3. **Regular load testing** of the system to correlate raw capacity (servers, disks, and so on) to service capacity.

The third is often the forgotten one. Raw capacity (machines) and service capacity (requests-per-second the service can handle) are not the same quantity — the translation is system-specific and changes as the code changes. Only load testing gives you the current conversion factor.

## Why SRE owns it

> Because capacity is critical to availability, it naturally follows that the SRE team must be in charge of capacity planning, which means they also must be in charge of provisioning. (source: chapter-01-introduction.md)

The logic is that accountability for availability cannot be separated from control over the resources that determine it. If capacity runs short, availability suffers; if SRE is on the hook for availability but capacity is decided elsewhere, the incentives are misaligned.

## Relationship to neighbouring tenets

- [[provisioning]] — the execution side: once the plan says "add capacity", someone has to spin up the instances and wire them in. SRE owns both ends.
- [[sre-efficiency]] — efficiency and capacity are two sides of the same coin. A more efficient service needs less capacity for the same load, so SRE's control of provisioning gives them the lever to chase efficiency.
- [[error-budget]] — capacity shortfalls burn error budget. Planning protects the budget.

## Two approaches: traditional vs intent-based

Chapter 18 develops the *how* of capacity planning at industrial scale. It names two approaches and argues forcefully for one of them (source: chapter-18-software-engineering-in-sre.md):

- [[traditional-capacity-planning]] — the demand-driven, spreadsheet-assisted cycle that industry had settled on as of the book's writing. Brittle to change, laborious, imprecise, and loses the requester's intent by the time a planner tries to map demands into supply.
- [[intent-based-capacity-planning]] — Chapter 18's proposed replacement. Programmatically encode the service's intent (dependencies, performance metrics, prioritisation) and let a solver produce the allocation plan. Regenerable on any change; reaches near-optimal solutions; surfaces unsatisfied requirements explicitly.

The industrial-strength implementation is a mixed-integer linear programming solver that plans the use of many millions of dollars of machine resources across several major divisions.

## Capacity planning and cascading failure (Chapter 22)

SRE Chapter 22 names capacity planning as a cascading-failure defence and, critically, as **insufficient on its own** (source: chapter-22-addressing-cascading-failures.md):

> Capacity planning reduces the probability of triggering a cascading failure, but it is not sufficient to protect the service from cascading failures. When you lose major parts of your infrastructure during a planned or unplanned event, no amount of capacity planning may be sufficient to prevent cascading failures. Load balancing problems, network partitions, or unexpected traffic increases can create pockets of high load beyond what was planned.

The chapter's example — a service with a 5,000 QPS per-cluster breaking point and a 19,000 QPS peak needs six clusters for N+2 — is a concrete realisation of the Chapter 1 mandatory-step #3 (correlate raw capacity to service capacity via load testing). And Chapter 22's [[testing-for-cascading-failures|load-testing discipline]] is the mechanism for keeping that correlation current: the breaking point changes with code, traffic mix, and underlying hardware, so the capacity plan is only as good as its last measured breaking point.

Organic-growth triggers (see [[cascading-failure-triggers]]) are the slowest but most common way services end up undercapacity: peak traffic grows 10-15% per quarter while the capacity plan stays fixed, and eventually a minor perturbation lands the service past its breaking point. A capacity plan that isn't routinely re-measured against the current breaking point is a plan aging toward its own failure.

## Capacity planning at launch time (Chapter 27)

SRE Chapter 27 adds the **launch-specific** capacity-planning discipline as a distinct concern (source: chapter-27-reliable-product-launches-at-scale.md). New features exhibit a temporary traffic spike that subsides within days, with a workload mix potentially very different from steady state. The consequences:

- **Launch spikes can reach 15x the initial estimate.** Public interest is notoriously hard to predict, and some Google products experienced this.
- **Launch-mix load-test results may not predict launch-mix behaviour.** Steady-state load tests have calibrated the service for a mix that the launch traffic won't match.
- **Regional launches build confidence.** Launching one region or country at a time reduces the downside of an underestimate.
- **Redundancy multiplies the plan.** Three replicated deployments at 100% peak means maintaining four or five to absorb maintenance plus an unexpected malfunction (see [[n-plus-2-redundancy]]).
- **Compute-resource lead times matter.** Datacenter and network resources have long lead times and need to be requested early.

The [[launch-checklist-themes|launch checklist]] encodes this as three standing questions: whether the launch ties to promotion, the expected traffic and growth rate, and whether compute resources have been obtained. See also [[overload-behavior-launches]] for why load tests are mandatory for most launches — first-principles prediction of overload behaviour is unreliable, so the measured breaking point is the only honest input to the plan.

## Cross-book connection

- Newman's [[scalability]] and Burns's [[sharded-service-pattern]] cover the mechanics of *how* to scale. SRE's capacity-planning tenet is the upstream discipline: *when* to scale, by how much, and on whose authority.
- Burns's [[dynamic-worker-scaling]] math (`P > processing_time / interarrival_time`) is capacity planning at the worker-pool granularity.
- [[desired-state-management]] (Newman) — an intent-based capacity plan is a declarative desired state; enacting automation is the reconciler. Intent-based capacity planning is the declarative-desired-state pattern applied to capacity rather than service composition.

## Related pages

- [[intent-based-capacity-planning]]
- [[traditional-capacity-planning]]
- [[software-engineering-in-sre]]
- [[sre-tenets]]
- [[provisioning]]
- [[sre-efficiency]]
- [[scalability]]
- [[scaling-approaches]]
- [[error-budget]]
- [[cascading-failure]]
- [[testing-for-cascading-failures]]
- [[cascading-failure-triggers]]
- [[reliable-product-launches]]
- [[launch-checklist-themes]]
- [[overload-behavior-launches]]
- [[n-plus-2-redundancy]]
