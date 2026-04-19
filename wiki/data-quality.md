# Data Quality

**Summary**: "The optimisation of data toward the desired state," answering the question *"what do you get compared with what you expect?"* A sub-facet of [[data-governance]] and a core responsibility of the data engineer. Chapter 2 names **three primary characteristics — accuracy, completeness, timeliness** — and frames quality as a problem that sits across the boundary of human and technical systems.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The framing question

Chapter 2 opens the topic with a human question: *"Can I trust this data?"* — a question every business person eventually asks.

Data quality is the optimisation of data toward the desired state. It orbits the question: **"What do you get compared with what you expect?"** Data should conform to expectations in the [[metadata|business metadata]] — does it match the definition the business agreed upon? (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md)

Data engineers ensure data quality across the entire lifecycle: running data-quality tests, ensuring conformance to schema expectations, completeness, and precision.

## Three primary characteristics

From *Data Governance: The Definitive Guide*, cited in Chapter 2 (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

### Accuracy

Is the collected data factually correct? Are there duplicate values? Are numeric values correct?

### Completeness

Are the records complete? Do all required fields contain valid values?

### Timeliness

Are records available in a timely fashion?

## Where these get nuanced

Each dimension has subtle failure modes that purely technical checks cannot solve.

**Accuracy and bots.** For web-event data, accuracy depends on distinguishing humans from bots and scrapers. Misclassification in either direction corrupts downstream analysis of the customer journey. This is a process-and-definition problem as much as a technical one (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

**Completeness, timeliness, and late-arriving data.** Chapter 2 cites the Google Dataflow paper's canonical example: an offline video platform downloads videos and ads while connected, plays them while offline, and uploads ad-view data once reconnected. The ad-view data arrives **well after** the ads were actually watched. How does the platform bill for the ads? No purely technical answer suffices — engineers must set standards for late-arriving data and enforce them uniformly. See [[late-arriving-events]] and [[windowing]] (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Human + technical problem

Data quality "sits across the boundary of human and technology problems" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). The engineer needs:

- **Robust processes** to collect actionable human feedback on quality issues.
- **Technology tools** to detect quality problems preemptively, before downstream users ever see them.

## Connection to other concepts

- Data quality is where [[data-validation-pipelines|validation pipelines]] plug in.
- Quality defects often show up first in **[[monitoring-and-observability|observability]]** signals — which is why [[dataops]] bundles them together.
- Accountability for quality is a governance topic — see [[data-governance]].
- Bellemare's [[data-contract|data contracts]] and [[schema-registry]] are the EDM enforcement mechanism for schema-shaped quality issues; they prevent producers from publishing data that doesn't conform.

## Related pages

- [[data-governance]]
- [[data-management]]
- [[data-validation-pipelines]]
- [[data-integrity-principles]]
- [[late-arriving-events]]
- [[windowing]]
- [[dataops]]
- [[data-lineage]]
