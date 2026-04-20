# SRE Product Adoption

**Summary**: Chapter 18's playbook for turning an SRE-built internal tool into a tool that's actually used across the organisation. Technical excellence is necessary but insufficient — adoption requires sustained socialisation, customer advocacy, targeted early-customer selection, and active customer service.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## Adoption is work

Don't underestimate the effort required to raise awareness and interest in an internal software product — **a single presentation or email announcement is not enough** (source: chapter-18-software-engineering-in-sre.md). Adoption requires all of:

- A consistent, coherent message repeated over time
- User advocacy (early adopters who speak on behalf of the tool to their peers)
- Sponsorship from senior engineers and management — leaders you've convinced of the tool's utility

Internal users tolerate more rough edges than external users, but they are also **busy**: if the tool is too difficult or confusing, they will write their own. Documentation matters even for a technical audience.

## Setting expectations

The tension is between **aspirational goals** (what the product will eventually do) and **minimum success criteria** / MVP (what it does right now) (source: chapter-18-software-engineering-in-sre.md):

- Promise too much, too soon: lose credibility when delivery slips.
- Promise too little: can't overcome activation energy to get teams to try something new.

The Auxon team's balance — a **long-term roadmap alongside short-term fixes**:

- Immediate benefit promised: onboarding and configuration effort would alleviate manual short-term resource-request bin-packing pain.
- Long-term benefit promised: the same configuration files would carry over and unlock broader cost savings as features shipped.
- **Demonstrate steady, incremental progress** through small releases — each release raises user confidence in the team's ability to deliver.

A published roadmap also lets teams quickly decide whether the early versions cover their use case; they can wait, or they can engage and influence priorities.

## Identify the right first customers

A one-size solution rarely fits all. Many larger teams already have passable home-grown solutions; they've already paid the configuration cost and have little incentive to adopt an alpha tool with rough edges (source: chapter-18-software-engineering-in-sre.md).

The Auxon team's strategy: **target teams that had no existing capacity-planning process**. They would have to invest configuration effort regardless, so the marginal cost of adopting Auxon was zero relative to the home-grown alternative.

The flywheel:

1. Early customers onboard because they have no alternative
2. Early customers become advocates
3. One Business Area wrote a **case study** comparing before-and-after results — time savings and toil reduction quantified
4. The case study creates the incentive that pulls later adopters across the threshold

## Customer service

Any sufficiently innovative software presents a **learning curve**. Chapter 18 is explicit: don't be afraid to provide **white-glove customer support** for early adopters to help them through onboarding (source: chapter-18-software-engineering-in-sre.md).

Automation carries emotional baggage too — fear that a shell script is replacing someone's job. Chapter 18's framing: working one-on-one with early users lets you address those fears directly and reframe the work — the team moves from owning the toil of a tedious task to **owning the configurations, processes, and results** of their technical work.

Google's SRE teams are globally distributed, so **early-adopter advocates double as local experts** for neighbouring teams considering the tool. One engaged early customer can unlock adoption across a region.

## Design at the right level

**Agnosticism** — design the software to accept many data sources as input, so customers don't have to commit to one upstream tool to use the framework (source: chapter-18-software-engineering-in-sre.md).

This was key for Auxon: customers brought their own forecasting, performance-data, and rollout tools. The messaging to potential users was "come as you are; we'll work with what you've got."

The payoff: broad adoption across a divergent set of use cases, with a low barrier to entry for new services.

The pitfall to avoid at the other extreme: **don't define success as 100% adoption**. Diminishing returns close out the last mile — the long tail of services rarely justifies the work to cover every edge case. Chapter 18 names this restraint explicitly.

## Cross-book connections

- [[team-autonomy]] (Newman) — agnostic design is a form of consumer-side autonomy: teams don't have to change their upstream choices to get value
- [[consumer-driven-contracts]] (Newman) — CDCs work similarly on the protocol axis: the producer accommodates consumer expectations without forcing migration
- [[migration-pattern-selection]] (Newman) — the incentive analysis ("teams with existing solutions won't move until the pain of not moving exceeds the cost of moving") applies to microservice extraction too
- [[evolutionary-architecture]] (Richards & Ford) — steady incremental progress via small releases is the incremental-change affordance Richards and Ford argue for at the architecture level
- [[architectural-thinking]] (Richards & Ford) — "don't define success as 100% adoption" is the trade-off-analysis stance: chasing the last 5% costs more than it returns

## Related pages

- [[software-engineering-in-sre]]
- [[sre-software-development-lessons]]
- [[fostering-software-engineering-in-sre]]
- [[introducing-sre-software-development]]
