# Postmortems at Google Working Group

**Summary**: A company-wide working group that coordinates postmortem practice across Google — pulling together templates, automating postmortem creation from incident tooling, and enabling cross-product trend analysis. Chapter 15 names it as the mechanism behind Google's continuous investment in postmortem culture and the vehicle for the chapter's forward-looking work (ML-assisted prediction, real-time investigation, duplicate detection).

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## The group's charter

Chapter 15's closing section describes the working group's remit (source: chapter-15-postmortem-culture-learning-from-failure.md):

> Our "Postmortems at Google" working group is one example of our commitment to the culture of blameless postmortems. This group coordinates postmortem efforts across the company: pulling together postmortem templates, automating postmortem creation with data from tools used during an incident, and helping automate data extraction from postmortems so we can perform trend analysis.

Three active workstreams:

1. **Template stewardship.** The [[postmortem-template|postmortem template]] (Appendix D) isn't static — the group owns its evolution, adds metadata fields, and ensures template changes propagate consistently across the company.
2. **Incident-tool integration.** Automating postmortem creation by ingesting data from the tools used during the incident itself — the [[live-incident-state-document|live incident document]], the [[recognized-command-post|command-post chat log]], monitoring dashboards, alert records. This reduces the toil portion of authoring and makes postmortems more complete by default.
3. **Automated data extraction.** Pulling structured data back *out* of finished postmortems so trend analysis becomes possible across products.

## Why cross-product matters

Chapter 15 names the products the working group has collaborated across (source: chapter-15-postmortem-culture-learning-from-failure.md):

> We've been able to collaborate on best practices from products as disparate as YouTube, Google Fiber, Gmail, Google Cloud, AdWords, and Google Maps. While these products are quite diverse, they all conduct postmortems with the universal goal of learning from our darkest hours.

The diversity of products is the point. A single product's postmortem corpus reveals that product's failure modes. The *union* of postmortem corpora across products reveals Google-wide failure modes that no single team would have spotted — shared infrastructure weaknesses, common response-pattern gaps, recurring architecture anti-patterns.

This is the argument for company-level coordination over team-level autonomy in postmortem practice. Teams can customise [[postmortem-triggers|triggers]] and choose their own root-cause techniques; they should not customise the template so aggressively that cross-product aggregation breaks.

## Trend analysis

Chapter 15 notes (source: chapter-15-postmortem-culture-learning-from-failure.md):

> With a large number of postmortems produced each month across Google, tools to aggregate postmortems are becoming more and more useful. These tools help us identify common themes and areas for improvement across product boundaries.

The **volume argument** is doing real work here. A single team producing ~10 postmortems per year can't reliably spot themes; Google-wide production of hundreds per month can. At that scale, aggregated analysis is a different genre of insight than any single postmortem review can provide.

## The metadata-enrichment push

The chapter explicitly connects the working group to [[postmortem-template|template metadata enrichment]] (source: chapter-15-postmortem-culture-learning-from-failure.md):

> To facilitate comprehension and automated analysis, we have recently enhanced our postmortem template (see Appendix D) with additional metadata fields.

Metadata fields are the structured handles the aggregation tools consume. A well-chosen metadata field turns a prose postmortem into a queryable record — "how many incidents this quarter had root causes in configuration changes?" becomes a database query rather than a manual survey.

## Future work: ML-assisted postmortem tooling

Chapter 15 closes with a forward-looking paragraph (source: chapter-15-postmortem-culture-learning-from-failure.md):

> Future work in this domain includes machine learning to help predict our weaknesses, facilitate real-time incident investigation, and reduce duplicate incidents.

Three distinct applications:

- **Weakness prediction.** Given aggregate postmortem data, flag systems that exhibit the structural risk factors of past major incidents.
- **Real-time incident investigation.** During an active incident, match the unfolding pattern against past postmortems and surface the relevant ones to responders. This turns the archive from passive memory into active assistance.
- **Duplicate detection.** Prevent the same root-cause investigation from being redone twice, and surface the recurrence signal early when a new incident is actually "the same one again."

The chapter frames this as **future work**, not current practice — but the direction of travel is clear.

## Connection to the feedback surveys

The working group's tooling priorities are shaped by the [[postmortem-feedback-surveys|surveys]] SREs fill in. "What kinds of tools would you like to see developed?" is the direct feeder question. The working group is the institutional locus where that feedback turns into product.

## Related pages

- [[postmortem-philosophy]]
- [[postmortem-template]]
- [[postmortem-review-process]]
- [[postmortem-feedback-surveys]]
- [[postmortem-culture-activities]]
- [[live-incident-state-document]]
- [[recognized-command-post]]
- [[learning-from-outages]]
