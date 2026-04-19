# Data Engineer

**Summary**: The role that develops, implements, and maintains the systems and processes that turn raw data into high-quality, consistent information for downstream use cases like analytics and machine learning. A data engineer manages the [[data-engineering-lifecycle]] end to end — from source-system generation through serving — and sits at the intersection of software engineering, security, data management, [[dataops]], data architecture, and orchestration.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## Definition

Reis and Housley define **data engineering** as:

> the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning

and **a data engineer** as the person who manages the [[data-engineering-lifecycle]], beginning with getting data from source systems and ending with serving data to consumers (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

This definition deliberately sits at the intersection of six disciplines — security, data management, [[dataops]], data architecture, orchestration, and software engineering — rather than equating data engineering with any single tool or storage format.

## What a data engineer is not

A data engineer typically does *not* (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- Build ML models.
- Create reports or dashboards.
- Perform data analysis.
- Build KPIs.
- Develop end-user software applications.

They should understand each of these well enough to serve the stakeholders who do them. The role is a hub, not a one-person pipeline.

## The balancing act

A data engineer constantly optimizes along six axes (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- Cost
- Agility
- Scalability
- Simplicity
- Reuse
- Interoperability

These axes trade off against each other — echoing the same "everything is a trade-off" framing captured in [[laws-of-software-architecture]] and [[trade-off-analysis]] at the software-architecture level.

## Business responsibilities

The chapter lists the macro, non-technical skills every data engineer needs (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **Communication** with both technical and nontechnical stakeholders. Most data-team failures are communication failures, not technology failures.
- **Scoping and gathering requirements** — knowing *what* to build before choosing *how*.
- **Cultural fluency in Agile, [[devops-vs-sre|DevOps]], and [[dataops]]** — these are cultural movements, not tool stacks.
- **Cost control** — time-to-value, total cost of ownership, opportunity cost; monitor costs to avoid surprises.
- **Continuous learning** — the tooling changes constantly; the durable skill is filtering fads from real developments.

## Technical responsibilities

At the technical level, the data engineer must be able to (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- Design architectures that balance performance and cost using prepackaged or homegrown components.
- Execute the five stages of the [[data-engineering-lifecycle]] (generation, storage, ingestion, transformation, serving).
- Apply the lifecycle's undercurrents (security, data management, [[dataops]], data architecture, software engineering).
- Write production-grade code. "A data engineer who can't write production-grade code will be severely hindered."

### Primary languages

- **SQL** — the lingua franca; briefly sidelined by MapReduce, now reemerged via Spark SQL, BigQuery, Snowflake, Hive, Flink, and [[stream-processing|streaming]] SQL.
- **Python** — the "second-best language at everything"; glue for pandas, NumPy, Airflow, PySpark, sci-kit learn, PyTorch.
- **JVM languages (Java / Scala)** — for deep work with Spark, Hive, Druid, Beam.
- **bash** — CLI productivity; still used for pipeline file processing and orchestration hooks.

Secondary languages appear where the company ecosystem demands them: R, JavaScript, Go, Rust, C/C++, C#, Julia.

### The unreasonable effectiveness of SQL

MapReduce briefly pushed SQL aside; declarative set-theoretic SQL then reemerged on top of Spark, BigQuery, Snowflake, Hive, Flink, Beam, and Kafka. The chapter treats SQL proficiency as table stakes, while also warning that a good data engineer recognises when SQL is the wrong tool — e.g., an NLP tokenisation pipeline is far better written in native Spark than in a masochistic SQL query (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Generalist vs specialist by data maturity

The day-to-day shape of the role depends on [[data-maturity]] (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **Stage 1 (starting with data)** — one generalist wearing many hats: part data scientist, part software engineer, part architect.
- **Stage 2 (scaling with data)** — specialists emerge, each focused on one slice of the lifecycle.
- **Stage 3 (leading with data)** — deep specialists plus a shift toward "enterprisey" concerns: governance, quality, [[data-lineage|lineage]], cataloguing.

See also [[type-a-vs-type-b-data-engineers]] for an orthogonal split — abstraction-focused vs build-focused engineers.

## Internal-facing vs external-facing

A data engineer faces one of two directions, or a blend (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- **External-facing** — aligns with users of social media apps, IoT, ecommerce. Must handle high query concurrency, per-user infrastructure limits, and the security complications of multi-tenant data.
- **Internal-facing** — BI dashboards, reports, ML models, internal process pipelines.

In practice internal-facing data is usually a prerequisite for external-facing data, so most data engineers span both.

## The role's trajectory (Chapter 11)

Chapter 11 revisits the role and predicts where it's going (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **The [[data-engineering-lifecycle]] isn't going away.** Claims that simpler tools will eliminate the role are "shallow, lazy, and shortsighted." As organisations use data in new ways, new foundations and workflows are needed — and data engineers are at the centre of designing them.
- **Move up the value chain.** Easier tooling means the engineer stops wrangling servers and pipes and moves to higher-level work: architecture, governance, quality, streaming integration, application embedding.
- **Enterprisey concerns return.** See [[enterprisey-data-engineering]] — data management, governance, quality, and DataOps become the engineer's day-to-day as the technology hard parts get abstracted away.
- **Titles blur.** See [[titles-will-morph]] — boundaries between DE, SWE, DS, and MLE collapse around data applications and operational ML.
- **Streaming-first competence.** The predicted [[live-data-stack]] expects engineers fluent in [[stream-processing]], [[stream-transform-load|STL]], [[real-time-olap|real-time OLAP]], and [[streaming-data-modeling|streaming modeling]].

The mobile-developer analogy: iOS and Android getting more sophisticated didn't eliminate app developers; it freed them to build better apps. Reis and Housley expect the same arc for data engineers as the [[cloud-data-os|cloud data OS]] matures.

## Relation to data science

Data engineering sits **upstream** from data science and analytics. Data engineers produce the inputs the scientists and analysts consume. The [[data-science-hierarchy-of-needs]] (Rogati) makes this explicit: ML sits at the top of a pyramid whose bottom three layers (collection, movement/storage, exploration) are data engineering work. Data scientists are estimated to spend 70–80% of their time on those bottom layers when they lack data-engineering support — a sign of immature data practice, not of data science being inherently drudgery (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Related pages

- [[data-engineering-lifecycle]]
- [[data-maturity]]
- [[type-a-vs-type-b-data-engineers]]
- [[dataops]]
- [[data-engineer-stakeholders]]
- [[data-science-hierarchy-of-needs]]
- [[data-engineering-history]]
- [[fundamentals-of-data-engineering]]
- [[devops-vs-sre]]
- [[data-ethics]]
- [[data-lineage]]
- [[future-of-data-engineering]]
- [[live-data-stack]]
- [[enterprisey-data-engineering]]
- [[titles-will-morph]]
