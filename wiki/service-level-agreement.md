# Service Level Agreement

**Summary**: An SLA is an explicit or implicit *contract* with users that specifies the consequences of meeting or missing the [[service-level-objective|SLOs]] it contains. The easy test for distinguishing SLA from SLO: "what happens if the SLOs aren't met?" — if there is no explicit consequence, it is an SLO, not an SLA (source: chapter-04-service-level-objectives.md).

**Sources**: `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Definition

> SLAs are service level agreements: an explicit or implicit contract with your users that includes consequences of meeting (or missing) the SLOs they contain. (source: chapter-04-service-level-objectives.md)

Consequences are most easily recognised when they are **financial** — a rebate or a penalty — but they can take other forms.

## The SLA vs SLO test

Most people mean SLO when they say "SLA." The book's footnote makes this explicit: a talk of an "SLA violation" is almost always a missed SLO; a real SLA violation might trigger a court case for breach of contract (source: chapter-04-service-level-objectives.md). Keeping the two terms distinct helps prevent engineering discussions from being framed as legal ones.

## Where SRE fits

SRE doesn't typically construct SLAs — SLAs are closely tied to business and product decisions, and require legal input on consequences and penalties. But SRE does get involved in two places (source: chapter-04-service-level-objectives.md):

1. **Helping avoid triggering the consequences** of missed SLOs — the whole point of the error-budget machinery is preventing SLO breaches, which in turn prevents SLA breaches.
2. **Defining the [[service-level-indicator|SLIs]]** behind the SLA — there must be an objective way to measure every SLO in the agreement, or disagreements will arise.

## Implicit SLAs

Even services without a written SLA have consequences for unavailability. Google Search is the chapter's example: there is no signed contract with the whole world, but an outage still damages reputation and drops advertising revenue (source: chapter-04-service-level-objectives.md). Google for Work, on the other hand, has explicit SLAs with its enterprise customers.

## Be conservative in what you advertise

The broader the constituency, the harder it is to change or delete SLAs that turn out to be unwise. Chapter 4's guidance: **be conservative in SLAs you publish**, and apply the same discipline as with SLOs — pick only what you can defend, start loose and tighten later (source: chapter-04-service-level-objectives.md). See [[service-level-objective]] for the underlying target-picking discipline.

## Consequences beyond money

The chapter's framing is that consequences are "most easily recognised" as financial, but can take other forms. Non-financial consequences include contractual early-termination rights, credit hours, prioritised support escalations, or a seat on a customer advisory board. The SLA constructs the channel through which service-level misses translate into business-level pain for the provider.

## Relationship to SLO and SLI

- [[service-level-indicator|SLI]] — the metric.
- [[service-level-objective|SLO]] — the target on the metric.
- **SLA** — the contract around the target, with teeth.

Whether or not a service has an SLA, it is still valuable to define SLIs and SLOs and use them to manage the service (source: chapter-04-service-level-objectives.md).

## Related pages

- [[service-level-indicator]]
- [[service-level-objective]]
- [[error-budget]]
- [[risk-tolerance]]
- [[availability-measurement]]
