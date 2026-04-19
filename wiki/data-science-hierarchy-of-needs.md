# Data Science Hierarchy of Needs

**Summary**: Monica Rogati's 2017 pyramid arguing that AI and ML sit at the top of a stack whose lower layers (data collection, movement/storage, exploration/transformation, aggregation/labelling, learning/optimisation) must exist first. In Reis and Housley's framing: the lower layers are [[data-engineer|data engineering]] work; the top layers are data-science work; companies that jump to ML without a data foundation get stuck.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`

**Last updated**: 2026-04-18

---

## The pyramid

Rogati published the hierarchy in a 2017 article (*"The AI Hierarchy of Needs"*). It answers: what has to be in place for AI/ML work to succeed? (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md)

From bottom to top:

1. **Collect** — instrumentation, source systems producing data.
2. **Move / store** — ingestion pipelines, reliable storage.
3. **Explore / transform** — cleaning, anomaly detection, prep.
4. **Aggregate / label** — feature engineering, labelled training sets.
5. **Learn / optimise** — A/B testing, experimentation, simple ML.
6. **AI, deep learning** — at the very top.

Reis and Housley use this as their core argument for why data engineering is a first-class discipline: the bottom three layers of the pyramid are where data scientists report spending 70–80% of their time, and that number is a **symptom of immature data engineering**, not an inherent property of data-science work. With good data engineering support, scientists should spend >90% of their time on the top layers (analytics, experimentation, ML).

## Implications

Chapter 1 draws several conclusions from the hierarchy (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **Don't skip to ML.** Companies without a solid data foundation (the bottom three layers) lack both the training data and the deployment path to make models succeed in production.
- **Data scientists aren't trained to engineer production-grade data systems.** Left to do it themselves, they do it haphazardly — slow, fragile, un-automated.
- **Data engineering is equal in importance to data science.** The engineer's job is to build the bottom of the pyramid so the scientist can focus on the top.
- **Data engineering sits upstream from data science.** Engineers provide inputs; scientists convert them into value.

## Maps directly onto the lifecycle

The Rogati hierarchy and the [[data-engineering-lifecycle]] describe overlapping territory (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

| Hierarchy layer | Lifecycle stage |
|---|---|
| Collect | Generation |
| Move / store | Ingestion + Storage |
| Explore / transform | Transformation |
| Aggregate / label | Transformation → Serving |
| Learn / optimise, AI | Serving → downstream consumers |

The hierarchy frames it from the ML-product side; the lifecycle frames it from the platform/pipeline side. They are two views of the same territory.

## Related pages

- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-engineer-stakeholders]]
- [[data-maturity]]
- [[fundamentals-of-data-engineering]]
