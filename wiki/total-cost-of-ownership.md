# Total Cost of Ownership (TCO)

**Summary**: The total estimated cost of an initiative including direct and indirect costs of products and services utilized. Reis and Housley's first cost lens on [[technology-selection|technology selection]], alongside [[total-opportunity-cost-of-ownership|TOCO]] and [[finops|FinOps]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Direct vs indirect costs

Chapter 4 splits costs two ways (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Direct costs** — attributable to the initiative. Examples: salaries of a team working on the initiative; the AWS bill for services consumed by this project.
- **Indirect costs (overhead)** — independent of the initiative; paid regardless.

## Capex vs opex

Orthogonal to direct/indirect is how the expense is purchased (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md). See [[opex-vs-capex]].

- **Capital expenses (capex)** — up-front investment, treated as an asset that depreciates. Before the cloud, data systems required multi-million-dollar hardware-and-software contracts, server rooms, data centres.
- **Operational expenses (opex)** — gradual, spread over time. Pay-as-you-go. Short-term focused, more flexible, closer to a direct cost and easier to attribute to a data project.

## Why cloud pushes opex-first

Before the cloud, opex wasn't an option for large data projects. The cloud changed that: data platform services let engineers pay on a consumption-based model. Reis and Housley's advice is explicit (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Given the upside for flexibility and low initial costs, we urge data engineers to take an opex-first approach centered on the cloud and flexible, pay-as-you-go technologies.

The argument is partly about direct dollars, partly about pace of change — "the data landscape is changing too quickly to invest in long-term hardware that inevitably goes stale."

## What TCO misses

TCO counts the dollars a choice will cost you. It does not count the dollars the choice will cause you to *forgo* — that's [[total-opportunity-cost-of-ownership|TOCO]]. Chapter 4 is clear that treating TCO as the only cost lens is a blind spot.

## Cross-book framing

- [[finops]] is the operational discipline that makes cloud TCO visible day-to-day.
- [[data-temperature]] (hot/warm/cold storage tiers) is a concrete TCO-vs-access-pattern trade-off.
- Burns's [[scaling-approaches]] and [[dynamic-worker-scaling]] are cost-shaping levers inside the TCO equation.

## Related pages

- [[technology-selection]]
- [[total-opportunity-cost-of-ownership]]
- [[opex-vs-capex]]
- [[finops]]
- [[principles-of-good-data-architecture]]
- [[data-architecture]]
- [[cloud]]
