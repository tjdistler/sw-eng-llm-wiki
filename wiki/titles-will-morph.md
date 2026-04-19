# Titles and Responsibilities Will Morph

**Summary**: Reis and Housley's prediction that the boundaries between [[data-engineer|data engineer]], [[software-engineering-for-data|software engineer]], data scientist, and ML engineer — already fuzzy — will continue to blur. Two specific forecasts: a new ML-focused engineer who lives between DE and MLE, and a deeper fusion of SWE and DE around [[data-application-fusion|data applications]]. The "throw it over the wall" model dies.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The core claim

The [[data-engineering-lifecycle]] isn't going away, but the titles of the people who execute it will (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). Reis and Housley already see this happening — many data scientists organically morph into data engineers when they lack the data-engineering support they need. They frame it as a pattern, not an accident.

## Driver: simplification

As tooling climbs the stack, (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Data scientists** spend less time gathering and munging data.
- **Data engineers** spend less time on low-level tasks (managing servers, configuration) and more time on [[enterprisey-data-engineering|"enterprisey"]] concerns.
- **ML engineers** shift from ad-hoc exploration to an operational discipline.
- **Software engineers** can't avoid streaming, pipelines, modeling, and quality.

Everyone moves up. Old responsibilities don't disappear; they get absorbed into simpler tools, leaving higher-value work for humans.

## Prediction 1: The ML-focused engineer

Between ML engineering and data engineering, Reis and Housley predict a new hybrid role (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- Knows algorithms, ML techniques, model optimisation, model monitoring, and data monitoring.
- Primary role: build or operate systems that **automatically train models, monitor performance, and operationalise the full ML process** for well-understood model types.
- Monitors data pipelines and quality — overlapping DE territory.

Research ML — novel model types — stays specialised. But for standard ML at standard scale, the role converges with DE.

See [[feature-store]] and [[model-drift]] — the tooling that makes this role possible.

## Prediction 2: SWE ↔ DE fusion around data applications

As [[data-application-fusion|data applications]] become standard — applications that blend traditional software with real-time analytics and ML — the boundary between software engineering and data engineering dissolves (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- Software engineers develop expertise in streaming, pipelines, modeling, data quality.
- Data engineers get integrated into application-development teams.
- "The boundaries that exist between application backend systems and data engineering tools will be lowered as well, with deep integration through streaming and event-driven architectures."

The end of "throw it over the wall." Today's producer/consumer wall between the application team and the data team becomes a tight collaboration.

## Why this matters for the lifecycle

The [[data-engineering-lifecycle]] doesn't care about titles. It cares about who does the work. The work doesn't disappear — it redistributes. Reis and Housley's broader point in Chapter 11 is that **the work-up-the-stack pattern holds across all four adjacent roles**: DE, DS, MLE, SWE. Everyone's scope changes, nobody's scope evaporates.

## The cultural pattern

This prediction echoes the same pattern that produced DevOps and SRE — specialist silos that industry learned to break down, reconstituting the work in cross-functional teams. Reis and Housley's forecast is that data roles follow the same arc.

See [[devops-vs-sre]] for the SWE/ops precedent, [[dataops]] for the data-flavoured culture that makes it possible, and [[type-a-vs-type-b-data-engineers]] for an orthogonal split that will still apply whatever the job title is.

## Related pages

- [[future-of-data-engineering]]
- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-application-fusion]]
- [[feature-store]]
- [[model-drift]]
- [[enterprisey-data-engineering]]
- [[software-engineering-for-data]]
- [[dataops]]
- [[devops-vs-sre]]
- [[type-a-vs-type-b-data-engineers]]
