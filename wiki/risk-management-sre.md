# Risk Management (SRE)

**Summary**: SRE manages service reliability largely by managing *risk*, treated as a continuum rather than a binary. The practice is to pick the appropriate point on that continuum for each service — reliable enough, but no more — so the availability target acts as both a minimum *and* a maximum.

**Sources**: `raw/site-reliability-engineering/chapter-03-embracing-risk.md`

**Last updated**: 2026-04-17

---

## Why risk, not reliability

The obvious goal for a service is maximum uptime. Chapter 3 opens by rejecting that framing:

> Past a certain point, increasing reliability is worse for a service (and its users) rather than better.

Extreme reliability has a real cost: it limits how fast new features ship, dramatically raises the cost of operating the service, and reduces the number of features the team can afford to build. And users usually cannot tell the difference — a user on a 99% reliable smartphone cannot distinguish 99.99% service reliability from 99.999% (source: chapter-03-embracing-risk.md). SRE reframes the goal as **balancing risk against rapid innovation and efficient operations** so overall user happiness is optimised.

## Two dimensions of cost

Cost does not scale linearly with reliability — an incremental improvement may cost 100x more than the previous increment (source: chapter-03-embracing-risk.md). The book names two distinct cost dimensions:

1. **Cost of redundant machine/compute resources** — the hardware needed to take systems offline for maintenance, provide data-durability parity blocks, or handle unplanned failures.
2. **Opportunity cost** — the engineering time spent on risk-reduction work is engineering time *not* spent on features users can see. Engineers building more redundancy are engineers not building new products.

Both costs matter, and both compound as the target tightens.

## Risk as a continuum

Chapter 3 treats risk as a smooth continuum rather than a yes/no property. Every service sits somewhere on that continuum, and Google's practice is to *place* each service explicitly based on a cost/benefit analysis:

> We give equal importance to figuring out how to engineer greater reliability into Google systems and identifying the appropriate level of tolerance for the services we run.

Search, Ads, Gmail, and Photos sit at different points on the continuum, not because Google gave up on some of them, but because each has a different business case. The explicit framing "this service has a 99.9% target; that one has 99.99%" replaces the implicit "reliability is always better".

## The target as both minimum *and* maximum

The most counterintuitive Chapter 3 idea:

> When we set an availability target of 99.99%, we want to exceed it, but not by much: that would waste opportunities to add features to the system, clean up technical debt, or reduce its operational costs. In a sense, we view the availability target as both a minimum and a maximum.

Beating the target substantially is a *signal of waste*, not a victory. It means the team spent engineering effort on reliability the business did not need and did not ask for. That effort should have gone into launches, debt reduction, or operational efficiency. This framing is what makes the [[error-budget]] a two-sided constraint: you cannot overspend it, and you should not leave it entirely unspent either.

## Explicit, thoughtful risk-taking

The overall payoff of the risk-management framing is that it **unlocks explicit, thoughtful risk-taking**. Without it, teams either overspend on reliability (nobody ever got fired for more nines) or underspend under launch pressure. With risk on the table as a measurable quantity, both the investment and the spending become legible, negotiable, and defensible.

The rest of Chapter 3 develops the two machinery pieces that make this practical:

- [[availability-measurement]] — how to turn risk into a number (request success rate, usually).
- [[risk-tolerance]] — how to pick the right number for a given service (consumer vs infrastructure cases).
- [[error-budget]] — how to spend the number against change velocity.

## Related pages

- [[error-budget]]
- [[service-level-objective]]
- [[availability-measurement]]
- [[risk-tolerance]]
- [[reliability]]
- [[sre-tenets]]
