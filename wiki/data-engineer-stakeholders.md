# Data Engineer Stakeholders

**Summary**: A map of the roles a [[data-engineer]] works with. Upstream stakeholders (data architects, software engineers, DevOps/SREs) produce the data the engineer consumes; downstream stakeholders (data scientists, analysts, ML engineers, business leadership) consume what the engineer produces. The data engineer sits at the hub between the two.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The hub position

A data engineer is a **hub** between data producers and data consumers (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **Producers (upstream)** — software engineers, data architects, DevOps / [[sre-discipline|SREs]].
- **Consumers (downstream)** — data analysts, data scientists, ML engineers, business leadership, AI researchers.

The role is therefore partly technical and partly organisational: the data engineer is a translator across function and across abstraction levels.

## Upstream stakeholders

### Data architects

Architects design the blueprint for organisational data management — processes, overall architecture, systems. They are a **bridge between technical and nontechnical sides** of the organisation, often with "battle scars" from hands-on engineering (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

The cloud has shifted the boundary between data architect and data engineer: cloud architectures are far more fluid than on-prem, so decisions that once required long lead times and hardware contracts now happen during implementation. The architect's role has become more strategic and visionary; the engineer picks up more tactical architectural work. In small organisations the same person plays both roles (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

### Software engineers

Software engineers build the business's applications, which generate the operational data the engineer consumes — application event data and logs in particular. In well-run organisations, software engineers and data engineers coordinate **from the inception** of a new project so application data is designed for downstream consumption (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

This maps directly to the [[data-contract]] / [[data-liberation]] ideas from Bellemare's *Building Event-Driven Microservices*: application producers owe their consumers a stable, well-designed data interface.

### DevOps and SREs

DevOps and [[sre-discipline|SRE]] teams **produce data via operational monitoring** — metrics, traces, logs. They sit upstream in that sense, but are frequently downstream too: data engineers build dashboards and data products that DevOps/SREs consume, and the two coordinate on operating data systems (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

See [[monitoring-and-observability]] and [[sre-monitoring-outputs]] for the operational-data side.

## Downstream stakeholders

### Data scientists

Build forward-looking models for predictions and recommendations. Industry folklore says they spend 70–80% of their time collecting, cleaning, and preparing data; Reis and Housley argue this is **a symptom of immature data engineering practice**, not an inherent property of the role. Good data engineering frees scientists to focus on modelling rather than plumbing (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

See [[data-science-hierarchy-of-needs]] for the Rogati framing of this relationship.

### Data analysts / business analysts

Focus on past and present (scientists focus on the future). Run SQL queries against warehouses/lakes, use BI tools (Power BI, Looker, Tableau), and are **domain experts** in the data they work with. Their subject-matter expertise is invaluable to the engineer for improving data quality (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

### ML engineers and AI researchers

**ML engineers** train and deploy models in production, maintain scaled ML infrastructure, and use PyTorch/TensorFlow heavily. The role blurs into data engineering (DevOps responsibilities over ML systems) and into data science (designing advanced ML processes). MLOps mirrors DataOps as a set of practices layered on top (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

**AI researchers** work on new ML techniques at big tech, specialised labs (OpenAI, DeepMind), or academia. Problems span immediate practical applications and abstract demonstrations (AlphaGo, GPT-3/4). Researchers in well-funded organisations have supporting engineering teams; in academia they rely on graduate students and postdocs (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Business leadership (C-suite)

Data engineers increasingly participate in strategic planning (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **CEO** — sets the data vision in collaboration with technical leadership; relies on engineers for the "what's possible" map.
- **CIO** — internal-facing IT leadership; directs major initiatives (ERP, CRM, cloud migration). Collaborates with data engineering leadership in mature organisations, shapes data culture in immature ones.
- **CTO** — external-facing technology leadership. Owns mobile/web/IoT — all critical data sources for engineers. Data engineers often report (directly or indirectly) through the CTO.
- **CDO (Chief Data Officer)** — responsible for data assets and strategy. The role was created at Capital One in 2002.
- **CAO (Chief Analytics Officer)** — responsible for analytics strategy and decision-making. Often oversees data science and ML.
- **CAO-2 (Chief Algorithms Officer)** — a recent addition focused specifically on data science and ML; typically a highly technical leader with an ML-research background.

## Project and product managers

- **Project managers** — coordinate large, often multi-year initiatives (cloud migrations, greenfield platforms). Most work Agile/Scrum, occasionally Waterfall. They prioritise a backlog of business requests and keep delivery on track.
- **Product managers** — oversee **data products** either built from scratch or iteratively improved. Like project managers, they balance tech-team cadence against business needs; as companies become more data-centric, the data-engineer / product-manager interaction becomes more frequent.

Data engineers interact with these managers through one of two team models (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **Centralised service team** — serves incoming requests from the rest of the org.
- **Cross-functional / embedded team** — engineers assigned to a particular product or project team.

## Source-system stakeholders (Chapter 5 refinement)

Reis and Housley return to upstream stakeholders in Chapter 5 and split them into two categories specific to source systems (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Systems stakeholders.** Build and maintain the source system itself. Software engineers, application developers, third-party SaaS providers.
- **Data stakeholders.** Own and control access to the data the source system produces. Typically IT, a data governance group, or third parties.

These categories often overlap but are distinct. A source system's operational reliability is a systems-stakeholder concern; a source dataset's schema, retention, and access permissions are a data-stakeholder concern. For any given pipeline, the data engineer needs to know both sides.

Chapter 5 adds two operational practices the engineer should own for this relationship:

- **A feedback loop.** "Create awareness of how data is consumed and used." When the source changes — schema, server, database, anything — the data engineer must be made aware of the impact it will have on their pipelines. Reis and Housley call this "among the single most overlooked areas where data engineers can get a lot of value" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).
- **A [[data-contract]] and [[service-level-agreement|SLA]]/[[service-level-objective|SLO]].** Written expectations of what the source will provide and when. If a formal contract feels too heavy, verbally set expectations and write them down somewhere retrievable.

## Related pages

- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-maturity]]
- [[data-science-hierarchy-of-needs]]
- [[data-contract]]
- [[data-liberation]]
- [[building-event-driven-microservices]]
- [[sre-discipline]]
- [[monitoring-and-observability]]
- [[fundamentals-of-data-engineering]]
