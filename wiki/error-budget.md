# Error Budget

**Summary**: The error budget is the quantified amount of permitted unavailability implied by a service's [[service-level-objective|SLO]] — if the target is 99.99%, the budget is 0.01%. SRE reframes that budget as a resource to be *spent* on velocity (launches, experiments, risky changes), which resolves the structural dev-vs-ops conflict the [[sysadmin-approach]] trench-warfares over.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-03-embracing-risk.md`, `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## The reframing

The error budget is SRE's resolution of the conflict the [[sysadmin-approach]] cannot resolve. Product development wants launches; operations wants stability; both are right, and both sets of goals are genuinely in tension because most outages are caused by change (source: chapter-01-introduction.md).

SRE's move: *stop arguing about whether to change things and start measuring how much unreliability you can afford*. Once you have an [[service-level-objective|SLO]], its complement is an explicit budget for unreliability — and you can agree to spend it on whatever you want, including the velocity the development team wants.

## 100% is the wrong reliability target

The budget starts from the observation that **100% is the wrong reliability target for basically everything** (pacemakers and anti-lock brakes being notable exceptions) (source: chapter-01-introduction.md). No user can tell the difference between 100% and 99.999% availability: there are many other systems between user and service (their laptop, their home WiFi, their ISP, the power grid) and these collectively are far less than 99.999% available. The marginal 0.001% gets lost in the noise of everything else, and nobody benefits from the enormous effort it takes to reach it.

## Picking the target is a product question, not a technical one

If 100% is wrong, what is right? Not a technical question. The business or product owner must set the target based on (source: chapter-01-introduction.md):

- What level of availability will users be **happy with**, given how they use the product?
- What **alternatives** are available to users who are dissatisfied?
- What happens to users' **usage** of the product at different availability levels?

The SRE team does not unilaterally pick the SLO. Once the SLO is set, however, the error budget derives from it mechanically: `error_budget = 1 - availability_target`.

## Spending the budget

> We can spend the budget on anything we want, as long as we don't overspend it. (source: chapter-01-introduction.md)

The development team wants to launch features and attract new users. Ideally, SRE spends the error budget taking risks on launches in order to ship them quickly. That simple framing changes downstream behaviour:

- **[[progressive-delivery|Phased rollouts]] and 1% experiments** become ways of *freeing up* budget — if you can roll out without consuming much of the budget, you can launch more often.
- **Outages stop being "bad"** — they are an expected part of innovation and a planned expenditure. Both sides *manage* them rather than fearing them.
- **SRE's goal is no longer "zero outages"** — it is spending the error budget efficiently in the service of feature velocity.

## The enforcement lever

When the budget is depleted, launches stop for the remainder of the period. This is the lever that makes the agreement real, not just rhetorical. Treynor Sloss is explicit that **this kind of decision requires strong management support** — the product development team will not embrace a launch freeze unless the chain of command backs it (source: chapter-01-introduction.md). Without executive backing, the budget degrades into another piece of ops theatre.

## Why the conflict dissolves

The pre-SRE conversation is qualitative and zero-sum:

- Dev: *launch more*.
- Ops: *break less*.

The error-budget conversation is quantitative and positive-sum:

- Both: *here is the budget; how do we spend it to maximise value?*

Reliability and velocity stop being arguments about each other's legitimacy and become the two axes of a shared optimisation problem. See [[sysadmin-approach]] for the pre-SRE failure mode this replaces.

## Chapter 3: motivation and mechanics

Chapter 3 ("Embracing Risk") develops the error budget as an explicit arbitration mechanism between product development and SRE. Both teams are evaluated on different (and partly opposing) metrics — product dev on velocity, SRE on reliability — and **information asymmetry amplifies the tension**: product dev sees the effort of writing/releasing code; SRE sees the state of production (source: chapter-03-embracing-risk.md).

Typical tensions that the error budget exists to arbitrate:

- **Software fault tolerance** — how hardened to make the code against unexpected events (brittleness vs shipping-friction).
- **Testing** — not enough causes outages; too much loses the market.
- **Push frequency** — every push is risky; how much effort to spend reducing that risk?
- **Canary duration and size** — how long and how big a slice for pre-launch canary testing?

Without a budget, teams work out an **informal balance** that's really a function of the negotiating skills of the engineers involved, not data. Chapter 3 quotes Google SRE's unofficial motto — *"Hope is not a strategy"* — and calls for an objective agreed-upon metric instead.

## Forming the budget

Chapter 3 spells out the mechanics:

1. **Product Management defines an [[service-level-objective|SLO]]** setting the expectation of uptime per quarter.
2. **Actual uptime is measured by a neutral third party** — the monitoring system.
3. **The difference between the two is the budget** of unreliability remaining for the quarter.
4. **As long as measured uptime is above the SLO**, new releases can be pushed.

Worked example: SLO = 99.999% of queries per quarter → error budget = 0.001% failure rate per quarter. A problem causing 0.0002% of queries to fail spends **20% of the quarterly error budget** (source: chapter-03-embracing-risk.md).

See [[availability-measurement]] for the success-rate framing of "uptime" that makes this quarterly-tracking computable.

## Budget-as-control-loop

The common pattern is to **manage release velocity** with the budget:

- Budget remaining → releases continue.
- Budget depleted → releases halt while the team invests in testing, resilience, and performance work.

This is a simple on/off control — the chapter calls it **"bang/bang" control** with a footnote to the cybernetics term. More nuanced approaches exist: *slow* releases as the budget nears depletion, or roll back automatically. Either way, the budget is the signal.

## Self-policing via budget awareness

When both sides see the budget:

- If product dev wants to skimp on testing or push faster and SRE resists, the budget guides the call.
- When the budget is fat, devs take more risks.
- When it is nearly drained, **product dev themselves push for more testing or slower releases** — they don't want to stall a launch.

The product development team becomes self-policing. This outcome **relies on SRE having the authority to actually stop launches** if the SLO is broken (source: chapter-03-embracing-risk.md) — the lever that Chapter 1 already named as requiring strong management backing.

## Externalities eat the budget too

A network outage or datacenter failure reduces measured availability just like a bad push does. That also consumes error budget, and the number of new pushes may be reduced for the rest of the quarter. The entire team supports the reduction because **everyone shares responsibility for uptime** (source: chapter-03-embracing-risk.md) — not just the team whose change caused the incident.

## Budget as evidence against over-reliability

The budget also surfaces the cost of **over-reliable targets**. If the team can't get launches out the door, they may elect to *loosen* the SLO (which increases the budget) to raise innovation capacity (source: chapter-03-embracing-risk.md). This is the operational expression of Chapter 3's "target as both minimum and maximum" framing — beating the target consistently is a signal to consider whether the target is too strict.

## Chapter 3 key insights

The chapter closes with three takeaways:

- Managing service reliability is largely about managing [[risk-management-sre|risk]], and managing risk can be costly.
- **100% is probably never the right reliability target** — not only impossible but usually more reliability than users want or notice. Match the service profile to the risk the business is willing to take.
- An error budget **aligns incentives and emphasises joint ownership** between SRE and product development, makes release-rate decisions easier, defuses outage discussions with stakeholders, and lets multiple teams reach the same conclusion about production risk without rancor.

## Chapter 4: "an SLO for meeting other SLOs"

Chapter 4 ("Service Level Objectives") restates the budget idea compactly: it is unrealistic and undesirable to insist that SLOs be met 100% of the time — doing so reduces innovation and deployment velocity and requires expensive, overly conservative solutions. So **allow an error budget — a rate at which SLOs can be missed** — and track it daily, weekly, with a monthly or quarterly assessment on top. The chapter's one-liner: *an error budget is just an SLO for meeting other SLOs* (source: chapter-04-service-level-objectives.md).

The SLO violation rate itself is a useful indicator of user-perceived health, and the gap between violation rate and budget feeds back into release-pacing decisions — see [[change-management-sre]].

## Connection to the rest of the wiki

- [[reliability]] — the technical substrate. Error budgets presuppose you can measure availability, which presupposes the fault-vs-failure framing.
- [[monitoring-and-observability]] — you need real data on availability to know how much budget you have left.
- [[progressive-delivery]] — the mechanism for launching inside an error budget; canary releases, feature flags, and 1% experiments all reduce the expected budget cost of a launch.
- [[change-management-sre]] — progressive rollouts, fast detection, and safe rollback all minimise the budget cost of a change going wrong.

## Related pages

- [[service-level-objective]]
- [[risk-management-sre]]
- [[risk-tolerance]]
- [[availability-measurement]]
- [[sre-discipline]]
- [[sysadmin-approach]]
- [[sre-tenets]]
- [[progressive-delivery]]
- [[change-management-sre]]
- [[reliability]]
