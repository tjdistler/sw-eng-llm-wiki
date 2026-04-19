# Data Serving

**Summary**: The fifth and final stage of the [[data-engineering-lifecycle|data engineering lifecycle]] — delivering data to consumers in useful form. Reis and Housley call serving "perhaps the most exciting part of the lifecycle — this is where the magic happens," and warn against **data vanity projects** where data is carefully collected but never actually used. Serving breaks down into three main consumers: [[analytics]], machine learning, and [[reverse-etl]]. Chapter 9 is the full deep-dive into the stage; this page collects the hub concepts.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Why serving is the point

"Data has value when it's used for practical purposes. Data that is not consumed or queried is simply inert." Chapter 2 warns against **data vanity projects** — massive [[data-lake|data lakes]] during the big-data era that were never consumed meaningfully, and a new wave of cloud-era vanity projects on warehouses and streaming platforms. The cure: data projects must be *intentional* across the lifecycle, always pointed at a business purpose (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 9's general considerations

Before any specific serving decision, Chapter 9 enumerates five general considerations that apply across analytics / ML / reverse ETL (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **[[trust-in-data|Trust]]** — "the root consideration." Sophisticated architectures are worthless if stakeholders don't trust the numbers.
2. **Use case and user** — what action will the data trigger, and who will take it? Can it be automated?
3. **[[data-product|Data products]]** — what "job to be done" is the user hiring this product for? What's the expected outcome and ROI?
4. **[[self-service-analytics|Self-service or not?]]** — mostly aspirational; succeeds only with specific audiences.
5. **[[data-definitions-and-logic|Data definitions and logic]]** — encoded in the [[data-catalog|catalog]] and in [[semantic-layer|semantic]] / [[metrics-layer|metrics layers]], not carried as tribal knowledge.
6. **[[data-mesh]]** — changes serving fundamentally from central-team-to-consumers to peer-to-peer domain serving.

## Ways to serve for analytics and ML

Chapter 9 lists concrete serving mechanisms (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **[[file-exchange-serving|File exchange]]** — ubiquitous, oldest, often unavoidable.
- **Databases** — OLAP queries from warehouses / lakes; SQL editors; fine-grained access controls.
- **Streaming systems** — emitted metrics and operational-analytics databases that blend OLAP and stream processing; see [[streaming-queries]].
- **[[federated-query|Query federation]]** — pull from multiple sources (OLTP, OLAP, APIs, files) without centralising.
- **[[data-sharing]]** — multitenant cloud sharing; consumer runs the query; security and access-control become the central serving problem.
- **[[semantic-layer|Semantic]] / [[metrics-layer|metrics layers]]** — consolidate business definitions and logic above the warehouse.
- **[[serving-in-notebooks|Serving data in notebooks]]** — the data-scientist interface; credentials, scale, and the path off the laptop.

## Three consumption modes

The chapter splits serving into three broad categories (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

### 1. Analytics

Covers three sub-varieties:

- **Business intelligence (BI)** — dashboards and reports describing the business's past and current state. Historically the default meaning of "analytics." Often uses a **logic-on-read** model where a BI tool maintains a repository of business logic and applies it at query time against clean-but-raw warehouse data.
- **Operational analytics** — fine-grained, real-time views: live inventory, website-health dashboards, things that trigger immediate operator action. Consumed directly from source systems or streaming pipelines; concerned with the present, not historical trends.
- **Embedded / customer-facing analytics** — analytics presented *to the SaaS platform's customers* rather than internal users. Request rates go up dramatically; access control becomes significantly more complicated because customers must see their data and only their data. A data leak here is a massive trust breach, not an internal procedural issue.

See [[analytics]] for more.

Embedded analytics ties to the **multitenancy** problem: many storage and analytics systems support multitenancy for efficient shared compute, but data engineers "must understand the minutiae of multitenancy in the systems they deploy to ensure absolute data security and isolation" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

### 2. Machine learning

Once an organisation reaches sufficient [[data-maturity|data maturity]], it can identify ML-amenable problems and build a practice around them. The boundaries between data engineering, ML engineering, and analytics engineering can be fuzzy — a data engineer may own Spark clusters that serve both ML training and analytics, orchestrate cross-team tasks, and maintain metadata/cataloging systems that track data history and lineage (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The [[feature-store]] is called out as a recent tool that straddles data engineering and ML engineering: it maintains feature history and versions, enables feature sharing, and provides operational capabilities like backfilling.

ML-specific questions at the serving stage (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- Is data quality good enough for reliable feature engineering?
- Is data discoverable by data scientists and ML engineers?
- Where are the technical and organisational boundaries between DE and MLE? A consequential architectural question.
- Does the dataset represent ground truth? Is it unfairly biased? (See [[data-ethics]].)

Reis and Housley's caution: **companies often prematurely dive into ML.** Build the data foundation first; develop competence in analytics before ML.

### 3. Reverse ETL

See [[reverse-etl]]. Taking processed data from the output side of the lifecycle and feeding it back into source and SaaS systems — e.g., pushing warehouse-calculated bids back into Google Ads, pushing customer segments into a CRM.

## Cross-book connections

- [[serving-state-from-edm]] (Bellemare) is the event-driven-microservices view of the same stage: services derive their own local materialised state from producer event streams rather than querying a central serving DB.
- [[oltp-vs-olap]] — the workload split that motivated the warehouse in the first place.
- [[data-ethics]], [[data-security]] — embedded analytics and reverse ETL both sharpen these concerns dramatically.

## Undercurrents at the serving stage

Chapter 9's closing undercurrents commentary (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **[[data-security|Security]]** — serving presents the "largest security surface" of any lifecycle stage. [[least-privilege|Least privilege]] for people and systems; read-only by default; fine-grained access; filtered views for multitenant sharing; kill unused data products to shrink the attack surface.
- **[[data-management]]** — [[trust-in-data|trust]] and quality; data-obfuscation techniques (synthetic, scrambled, anonymised) for serving sensitive data; semantic/metrics layers as single source of truth.
- **[[dataops]]** — monitor data health, downtime, latency, quality, security, and versions of data and models being served.
- **[[data-architecture]]** — fast feedback loops; collaborative dev/test/prod environments; move data scientists off laptops.
- **[[orchestration]]** — the serving stage coordinates data flow across many teams. Centralised vs decentralised orchestration is a key organisational call.
- **[[software-engineering-for-data|Software engineering]]** — translate data-scientist notebook code into production; understand how programmatic SQL (LookML, dbt/Jinja, ORMs) performs; build CI/CD for the data team.

## Related pages

- [[data-engineering-lifecycle]]
- [[analytics]]
- [[business-analytics]]
- [[operational-analytics]]
- [[embedded-analytics]]
- [[reverse-etl]]
- [[trust-in-data]]
- [[data-product]]
- [[self-service-analytics]]
- [[data-definitions-and-logic]]
- [[semantic-layer]]
- [[metrics-layer]]
- [[file-exchange-serving]]
- [[serving-in-notebooks]]
- [[feature-store]]
- [[feature-engineering]]
- [[model-drift]]
- [[training-test-sets]]
- [[data-warehousing]]
- [[data-maturity]]
- [[data-ethics]]
- [[data-quality]]
- [[data-mesh]]
- [[data-as-a-product]]
- [[serving-state-from-edm]]
