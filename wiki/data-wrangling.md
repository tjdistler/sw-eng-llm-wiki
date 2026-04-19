# Data Wrangling

**Summary**: The batch-transformation activity of converting messy, malformed data into clean, usable data. The classic ETL developer pain. Reis & Housley describe **data-wrangling tools** as "IDEs for malformed data" — visual environments that accelerate the parse-inspect-fix loop that otherwise consumes disproportionate engineer time.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The activity

Data wrangling takes messy, malformed data and turns it into useful clean data (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). Generally a batch activity.

The classic example: [[edi|EDI]] data from a partner business — a mix of structured data and text, variably malformed. The typical process:

1. Ingest the data as a single-text-field table (entire row as one field) because it's too broken to parse on entry.
2. Write queries to parse and break it apart.
3. Discover anomalies and edge cases.
4. Iterate until data is in rough shape.
5. Only *then* can actual downstream transformation begin.

Data wrangling has "long been a major source of pain and job security for ETL developers."

## Data-wrangling tools

Reis & Housley push back against data engineers' suspicion of low-code tools (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> These tools often put off data engineers because they claim to be no code, which sounds unsophisticated. We prefer to think of data wrangling tools as integrated development environments (IDEs) for malformed data.

Typical features:

- **Visual sample preview** with inferred types, distributions, outliers, nulls.
- **Step-builder interface** — add steps to fix typing errors, split fields, join with lookup tables.
- **Preview-on-sample, scale-to-full** — steps run against a small sample interactively; when the full job is ready, push it to Spark or a similar system.
- **Error handling** — after a full run, errors and unhandled exceptions come back so the user can refine the recipe.

## The recommendation

The chapter suggests (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Experiment with wrangling tools — major cloud providers sell their own, many third-party options exist.
- **Train specialists** in data wrangling if your team frequently ingests from new, messy sources.
- Wrangling tools can offload parsing work from data engineers to analysts.

This aligns with Chapter 8's broader point about the democratization of data tooling — lower the barrier to entry so analysts and scientists can handle the parts that used to require engineer time.

## Related pages

- [[data-transformation]]
- [[edi]]
- [[data-quality]]
- [[schema-on-read-vs-write]]
- [[data-ingestion]]
