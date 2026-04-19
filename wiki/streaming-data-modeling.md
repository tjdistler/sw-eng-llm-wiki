# Streaming Data Modeling

**Summary**: An unsettled area. Classical batch modeling — [[kimball-model|Kimball]], [[inmon-model|Inmon]], [[data-vault]] — was designed for bounded data and scheduled ETL. Translating those patterns to unbounded streams (especially SCD Type 2 maintenance) doesn't work. The emerging practice: flexible schemas, [[nested-data|nested fields]], store recent and historical together, rely on the source system for business definitions.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Why classical modeling breaks

Reis & Housley spell it out (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> Given a stream of data, how would you continuously update a Type-2 slowly changing dimension without bringing your data warehouse to its knees?

The answer is: you can't, at least not the way batch warehouses do it. Every record in the stream potentially touches a dimension, and a Type-2 update per event is a write amplification the warehouse isn't built for.

More broadly, the constraints that made classical modeling sensible — expensive storage, on-prem hardware, slow ETL, tight compute/storage coupling — have evaporated. The old rigor doesn't buy what it used to.

## What the experts say (per Reis & Housley)

Streaming data experts told the authors three things (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **Traditional batch-oriented data modeling doesn't apply to streaming.** Full stop.
2. **[[data-vault|Data vault]] is a candidate** — its insert-only, schema-flexible design aligns with stream semantics.
3. **Anticipate schema changes and keep a flexible schema.** Source systems change fields on a whim (IoT firmware upgrades, CDC type recasts); rigid downstream schemas break.

## The practical pattern

- **No rigid schema in the analytical database.** Land streaming data in [[wide-denormalized-table|wide tables]] with [[nested-data|nested columns]]. Evolve the column set by adding flattened fields as they stabilize.
- **Trust the source system's definition.** Assume the source provides correct data with the right business definition as it exists *today*. Don't try to integrate and redefine at the warehouse layer.
- **Keep recent and historical streaming data together.** Cheap storage means you don't have to choose — optimise for comprehensive analytics over the whole span.
- **React, don't report.** "Instead of reacting to reports, why not create automation that responds to anomalies and changes in the streaming data instead?" (Chapter 8).

## The wider shift (Reis & Housley's prediction)

Chapter 8 anticipates a "sea change" in modeling paradigms. The likely direction (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Incorporate **metrics layers** and **semantic layers** (see [[metrics-layer]]).
- Merge data pipelines with traditional analytics workflows.
- Run the analytics layer **directly on top of source systems** via streaming, rather than artificially separating "source" from "analytical" data.

Chapter 11 of the book expands on this as the **live data stack**.

## Cross-book connections

- [[change-data-capture]] — CDC is the primary source of streaming data and comes with its own schema-evolution surprises.
- [[stream-joins]] — DDIA's treatment of time-dependent joins, including SCD Type 2 as the determinism technique (batch-shaped, not streaming-rate).
- [[deterministic-stream-processing]] — Bellemare's framing of reproducibility under reprocessing; relevant to any streaming modeling approach.

## Related pages

- [[streaming-queries]]
- [[data-modeling]]
- [[data-vault]]
- [[wide-denormalized-table]]
- [[nested-data]]
- [[schema-evolution]]
- [[kappa-architecture]]
- [[metrics-layer]]
