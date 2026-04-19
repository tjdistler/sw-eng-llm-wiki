# Data Maturity

**Summary**: A three-stage model (starting with data, scaling with data, leading with data) that describes how an organisation's use of data evolves — and therefore how a [[data-engineer]]'s day-to-day responsibilities change. Maturity is not about company age or revenue; it is about how strongly data is leveraged as a competitive advantage. A young startup can be more data-mature than a century-old enterprise.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`

**Last updated**: 2026-04-18

---

## The model

Reis and Housley survey published maturity frameworks (Data Management Maturity / DMM and others) and conclude none is both simple and useful for data engineering, so they propose their own three-stage model (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

1. **Stage 1 — Starting with data**
2. **Stage 2 — Scaling with data**
3. **Stage 3 — Leading with data**

The shape of a data engineer's role changes at each stage.

## Stage 1 — Starting with data

Loose or absent goals, early-stage architecture, single-digit headcount data team. The data engineer is a generalist doubling as data scientist and software engineer. Reports and analyses are ad hoc (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Priorities:

- **Get executive buy-in.** Ideally find a sponsor for a data initiative.
- **Define a minimal data architecture** that serves business goals. Usually solo, without a dedicated architect.
- **Audit and identify the data** that will support key initiatives.
- **Build the foundation** that future analysts and scientists will consume. In the meantime, the engineer may have to generate the reports themselves.

Pitfalls:

- **Organisational willpower wanes** without visible wins. Quick wins buy runway — but they create technical debt; have a plan to pay it down.
- **Working in silos.** Get out of the data room; talk to business stakeholders.
- **Undifferentiated heavy lifting.** Use turnkey, off-the-shelf solutions wherever possible. Only build custom where it creates competitive advantage.
- **Premature ML.** Without a solid foundation the models won't have the data to train on or a scalable deployment path. (The authors call themselves "recovering data scientists" for this reason.)

## Stage 2 — Scaling with data

The company has moved past ad-hoc requests and has formal data practices. The challenge is scaling the architecture and preparing for a genuinely data-driven future. Data engineering specialises — people own particular slices of the [[data-engineering-lifecycle]] (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Priorities:

- Establish formal data practices.
- Create scalable, robust data architectures.
- Adopt [[devops-vs-sre|DevOps]] and [[dataops|DataOps]] practices.
- Build systems that support ML in production.
- Keep avoiding undifferentiated heavy lifting.

Pitfalls:

- **Cargo-culting Silicon Valley.** Adopting bleeding-edge tech just because big tech uses it. Technology decisions must trace back to customer value.
- **The real bottleneck is the team, not the cluster.** Optimise for team throughput — simple-to-deploy tools beat bleeding-edge ones.
- **Framing yourself as a technologist** instead of a pragmatic leader. Start teaching the rest of the organisation how to consume data.

## Stage 3 — Leading with data

Automated pipelines and self-service analytics are the default. Introducing new data sources is seamless. Proper controls and practices are in place. Data engineers specialise deeply (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Priorities:

- Automation for seamless introduction and usage of new data.
- Custom tools and systems that use data as a competitive advantage.
- "Enterprisey" aspects: data management (governance, quality), [[dataops|DataOps]], master data management.
- Data catalogs, [[data-lineage|lineage]] tools, metadata management.
- Cross-functional collaboration with software engineers, ML engineers, analysts.
- Culture where people can collaborate and speak openly regardless of role.

Pitfalls:

- **Complacency.** Stage 3 is not a steady state — organisations that stop investing slide back down.
- **Technology distractions.** Expensive hobby projects that don't deliver business value become more tempting at this stage. Custom tech only where it provides competitive advantage.

## What the stages tell a data engineer

The level of data engineering complexity in a company depends heavily on data maturity, so maturity directly shapes the day-to-day job and career progression. A generalist role at Stage 1 is a different job from a deep specialist role at Stage 3 — same title, different work (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Data maturity also correlates with the [[type-a-vs-type-b-data-engineers|Type A vs Type B]] distinction: Type A engineers (abstraction-focused) fit all stages; Type B engineers (build-focused) most commonly appear in Stages 2 and 3, or in Stage 1 companies whose initial use case is so unique it demands custom tooling from day one.

## Related pages

- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[type-a-vs-type-b-data-engineers]]
- [[dataops]]
- [[data-engineering-history]]
- [[fundamentals-of-data-engineering]]
