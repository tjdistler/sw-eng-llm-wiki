# Inmon Model

**Summary**: Bill Inmon's 1990 approach to data warehousing: a **subject-oriented, integrated, nonvolatile, time-variant** collection of data, highly normalized (typically 3NF), ingested via rigorous ETL from every key source system, and exposed to business via department-specific [[data-mart|data marts]] downstream. The more rigorous half of the Inmon-vs-Kimball debate.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The definition

Inmon's definition of a data warehouse (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> A data warehouse is a subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions.

The four adjectives carry specific meaning:

- **Subject-oriented.** Focused on a business subject area (sales, marketing). The logical model organises around the subject, not around the shape of a particular source system.
- **Integrated.** Data from disparate sources is consolidated and normalized into a single physical corporate image. "Of all the aspects of a data warehouse, integration is the most important" (Inmon, quoted in Chapter 8).
- **Nonvolatile.** Once stored, data doesn't change. The warehouse retains history.
- **Time-variant.** Data is queryable across varying time ranges; the warehouse isn't a point-in-time snapshot.

## The architecture

1. Data is extracted from every key operational source system.
2. ETL integrates, converts, reformats, resequences, and summarizes it.
3. The result is loaded into the data warehouse as **highly normalized (3NF)** relational tables — the schema often mirrors the source systems' normalization structure, with as little duplication as possible.
4. **Business and department-specific [[data-mart|data marts]]** sit downstream, typically denormalized (often as [[star-schema|star schemas]] despite this being a "Kimball" construct).

The data warehouse is the **single source of truth**; the marts are the consumption-shaped projection.

## Design characteristics

Reis & Housley (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Relentless emphasis on ETL.** Data is cleaned and integrated *before* landing in the warehouse (not after, as in modern ELT).
- **Ingested incrementally**, starting with highest-priority business areas.
- **Strict normalization** (~3NF) minimises duplication and therefore minimises downstream analytical errors from divergent representations.
- Marts may be denormalized because they serve specific reporting needs.

## Inmon vs Kimball in one sentence

Inmon is **top-down**: integrate everything at the warehouse first (3NF), then project into department marts. [[kimball-model|Kimball]] is **bottom-up**: model department-facing business analytics (facts + dimensions, [[star-schema|star schemas]]) directly in the warehouse from the start, accepting duplication and denormalization.

Inmon himself: "a data mart is never a substitute for a data warehouse." He argues Kimball's bottom-up approach skews the definition of "data warehouse."

## Where it still applies

The Inmon model was defined when storage was expensive and compute was coupled to storage. Those constraints have relaxed — cheap cloud storage and [[storage-compute-separation|separated compute]] mean the cost of denormalization has fallen dramatically. That has softened the Inmon-Kimball debate and pushed some teams toward hybrid approaches (start with [[data-vault]] for integration, then project a Kimball-style star schema for analytics).

That said, the Inmon emphasis on **integration as the central act** remains a strong organising idea, especially when a business needs a single source of truth across many source systems.

## Canonical references

- Inmon, *Building the Data Warehouse* (Wiley).
- Inmon, *Corporate Information Factory*.
- Inmon, *The Unified Star Schema* (Technics Publications).

## Cross-book connections

- [[data-warehousing]] — DDIA's treatment of the warehouse pattern; the star/snowflake schema discussion there sits inside the *Kimball* tradition that most warehouses (and Inmon-model marts) actually use.

## Related pages

- [[data-warehousing]]
- [[kimball-model]]
- [[data-vault]]
- [[data-mart]]
- [[normalization-levels]]
- [[conceptual-logical-physical-models]]
- [[etl-vs-elt]]
- [[master-data-management]]
