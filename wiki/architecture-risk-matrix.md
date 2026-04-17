# Architecture Risk Matrix

**Summary**: A 3×3 grid of **impact × likelihood** that turns the subjective "is this low, medium, or high risk?" question into a numeric rating of 1–9. Richards and Ford's starting tool for analysing architecture risk, and the rating scale that feeds the broader **risk assessment** report and the [[risk-storming]] practice.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-20-analyzing-architecture-risk.md`

**Last updated**: 2026-04-16
---

## The problem it solves

Every architecture has risk — availability, scalability, data integrity, security. The architect's job includes continually analysing that risk so deficiencies can be addressed before they become incidents (source: chapter-20-analyzing-architecture-risk.md). The first issue that arises when assessing architecture risk is qualifying it at all:

> Too much subjectiveness usually enters into this classification, creating confusion about which parts of the architecture are really high risk versus medium risk. (source: chapter-20-analyzing-architecture-risk.md)

Two architects looking at the same database dependency can honestly disagree about whether it's "medium" or "high" risk. Without a shared procedure, the conversation reduces to opinions. The risk matrix fixes this by decomposing one subjective question into two narrower ones, each rated on a 1–3 scale, then multiplying the answers.

## The two dimensions

Each axis has three levels: low (1), medium (2), high (3) (source: chapter-20-analyzing-architecture-risk.md).

| | | Impact → |
|---|---|---|
| **Likelihood ↓** | Low (1) | Medium (2) | High (3) |
| Low (1) | **1** (low) | **2** (low) | **3** (medium) |
| Medium (2) | **2** (low) | **4** (medium) | **6** (high) |
| High (3) | **3** (medium) | **6** (high) | **9** (high) |

Band thresholds:

- **1–2** — low risk (green)
- **3–4** — medium risk (yellow)
- **6–9** — high risk (red)

Richards and Ford recommend also shading the cells (light / medium / dark grey) so the report survives black-and-white printing and colour blindness (source: chapter-20-analyzing-architecture-risk.md).

## How to apply it

The chapter's worked example: a central database suspected of availability risk (source: chapter-20-analyzing-architecture-risk.md).

1. **Consider impact first.** If the database goes down, the whole application is unusable. That's high impact — pinning the risk to the third column (3, 6, or 9).
2. **Consider likelihood second.** The database runs on a clustered, highly available configuration. Likelihood of outage is low. Row 1, column 3 → rating of **3 (medium)**.

The order matters. Impact is typically easier to reason about (what would happen?) than likelihood (how often?), and pinning the impact first narrows the matrix to one column before the harder conversation begins.

### The unknown-technology exception

One situation where the matrix cannot be used directly: a technology no team member knows. During [[risk-storming]] consensus, if a participant identifies a component as high risk purely because they don't know what it is, that's not a matrix judgement — the participant couldn't have rated impact or likelihood. Richards and Ford's rule:

> For unproven or unknown technologies, always assign the highest risk rating (9) since the risk matrix cannot be used for this dimension. (source: chapter-20-analyzing-architecture-risk.md)

This rule is why bringing developers into risk-storming sessions is valuable — a developer not recognising a named technology is itself information about architectural risk.

## Risk assessment reports

The matrix gives a rating per concern. A **risk assessment** is the summary report built from many such ratings organised by assessment criteria (rows) and services or domain areas (columns) (source: chapter-20-analyzing-architecture-risk.md).

### Basic layout

|  | Customer Registration | Catalog Checkout | Order Fulfillment | **Total** |
|---|---|---|---|---|
| Availability | 3 | 4 | 3 | **10** |
| Elasticity | 6 | 6 | 3 | **15** |
| Security | 2 | 3 | 2 | **7** |
| Performance | 3 | 6 | 3 | **12** |
| Data Integrity | 6 | 6 | 6 | **17** |
| **Total** | **20** | **25** | **17** | |

Cells are colour-coded by band. Totals accumulate along both axes, letting the architect see which *criterion* is riskiest (data integrity, at 17) and which *domain area* carries the most risk (catalog checkout, at 25). Tracking these totals over time shows whether risk is improving or degrading.

### Filtering for audience

Presenting the full matrix to a stakeholder meeting is rarely useful. For a meeting about high-risk areas, filter to the red cells only (source: chapter-20-analyzing-architecture-risk.md). Signal-to-noise ratio of the communication matters as much as completeness of the data — Richards and Ford explicitly separate the full assessment (architect's working artefact) from the filtered view (stakeholder-meeting artefact).

### Showing direction of risk

A snapshot doesn't say whether things are getting better or worse. Arrows don't work — the chapter reports that "almost 50% of people asked said that the up arrow meant things were progressively getting worse, whereas almost 50% said an up arrow indicated things were getting better" (source: chapter-20-analyzing-architecture-risk.md). Even with a key on the same page, confusion returns once the reader scrolls past it.

Two techniques Richards and Ford recommend:

1. **Plus and minus signs** appended to the rating:
   - `4−` (red minus) — medium risk, trending worse
   - `6+` (green plus) — high risk, trending better
   - `3` (no sign) — medium risk, stable
2. **Arrows with target numbers**: a red down-arrow to `6` means trending up to high risk; a green arrow to `2` means trending down to low risk. No key required because the direction is explicit in the target.

The direction signal has to come from somewhere. Richards and Ford point to continuous measurements via [[architecture-fitness-function|fitness functions]]:

> The direction of risk can be determined by using continuous measurements through fitness functions described earlier in the book. By objectively analyzing each risk criteria, trends can be observed, providing the direction of each risk criteria. (source: chapter-20-analyzing-architecture-risk.md)

This is the Chapter 20 tie-back to Chapter 6: a fitness function measuring a characteristic (say, p95 latency against a budget) is the mechanism that produces the directional arrow on the performance row of the risk assessment.

## When to use the matrix

The matrix is the rating scale underneath three separate practices:

- **Solo risk review** — an architect walking a diagram with it in mind.
- **Risk assessment reports** — the grid-form summary described above.
- **[[risk-storming]]** — the collaborative session where multiple participants independently apply the matrix to the same diagram and then consolidate.

It also generalises outside architecture. The chapter notes that user stories in an Agile iteration can be rated the same way: impact = what happens if the story doesn't make the iteration; likelihood = probability it slips (source: chapter-20-analyzing-architecture-risk.md). High-risk stories then get prioritisation and closer tracking.

## Relationship to the wiki's other risk vocabulary

- [[reversible-vs-irreversible-decisions]] — impact is higher for irreversible decisions (Bezos's one-way doors); the matrix gives a rating scale for that intuition.
- [[cost-of-change]] — the downstream cost an architectural decision incurs; feeds impact.
- [[architecture-fitness-function|fitness functions]] — the mechanism that gives the direction arrows their objective basis.
- [[architecture-decision-record]] — the Consequences section of an ADR is the natural place to record the matrix rating when an architecturally-significant decision introduces risk.
- [[risk-storming]] — the collaborative application of this matrix on a diagram with multiple participants.

## Related pages

- [[risk-storming]]
- [[architecture-fitness-function]]
- [[architecture-decision-record]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[unknown-unknowns]]
- [[architecture-governance]]
- [[architecture-vitality]]
- [[fundamentals-of-software-architecture]]
