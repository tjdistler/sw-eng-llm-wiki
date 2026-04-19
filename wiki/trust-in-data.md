# Trust in Data

**Summary**: Reis & Housley's Chapter 9 declares trust "the root consideration in serving data." The fanciest architecture is irrelevant if end users don't believe the data represents their business. Trust takes 20 years to build and five minutes to lose; once lost, the data project is on a silent countdown to cancellation.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Why trust is the prime consideration

Chapter 9 opens the serving discussion with Warren Buffett's line — "it takes 20 years to build a reputation and five minutes to ruin it" — and frames that as the first law of data serving. A loss of trust is "often a silent death knell for a data project, even if the project isn't officially canceled until months or years later" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The failure mode the authors see repeatedly: data teams fixate on *pushing out data* without asking whether stakeholders trust it in the first place. The business underperforms with data, and the data team loses credibility and — eventually — its headcount.

## Two dimensions of trust

Chapter 9 separates trust into two axes (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **Trust in data quality.** Does the data accurately represent financial, customer, or operational reality? Built via [[data-quality|data validation]] and [[data-observability]], plus visually confirming validity with stakeholders.
2. **Trust in SLAs and SLOs.** High-quality data is of little value if it is not available when a business decision must be made. Users come to depend on data being there on time and up-to-date per the commitments data engineers made.

A [[data-contract|data contract]] — formal or informal — encodes both axes.

## Practical moves for building trust

- Apply [[data-validation-pipelines|data validation]] throughout the lifecycle, not only at serving.
- Run [[data-observability]] so problems are detected proactively, not by a stakeholder seeing a wrong number.
- Negotiate an [[service-level-agreement|SLA]] stating what the data product will do, and [[service-level-objective|SLOs]] that measure performance against it. Chapter 9's example: "Data will be reliably available and of high quality" (SLA); "pipelines will have 99% uptime with 95% of data free of defects" (SLO).
- Keep communication channels open about possible SLA/SLO issues; have a remediation and improvement process.
- Visually confirm with stakeholders — numbers can be technically correct and still be wrong because the definition doesn't match what the business means. See [[data-definitions-and-logic]].

## The silent-killer connection

Trust ties directly into the [[dataops|DataOps]] mantra "data is a silent killer" — bad data lingers in reports for months without detection unless observability is explicit. When the silent killer finally surfaces, it's trust that dies first (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Cross-book connections

- **[[service-level-agreement]] / [[service-level-objective]]** — SRE's vocabulary for the same commitment mechanism Chapter 9 applies to data products.
- **[[blameless-postmortem]]** — once trust is damaged, only a credible, open, learning-oriented response rebuilds it; Google's SRE postmortem culture is a model.
- **[[truth-and-leadership-in-distributed-systems]]** — the general problem of a system staying a trusted source of truth under failure.

## Related pages

- [[data-serving]]
- [[data-quality]]
- [[data-observability]]
- [[data-contract]]
- [[data-definitions-and-logic]]
- [[service-level-agreement]]
- [[dataops]]
- [[data-as-a-product]]
