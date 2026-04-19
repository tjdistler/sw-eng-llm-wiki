# Data Platform

**Summary**: A data platform is a vendor-curated **ecosystem of interoperable tools** tightly integrated around a core storage layer — object storage, warehouse, lake, or lakehouse. Reis and Housley treat the platform as a genuine category alongside warehouse/lake/lakehouse: Snowflake, Databricks, BigQuery, AWS, Azure, and Google Cloud are competing to build the **walled garden of data tools** that the next generation of data engineers will select as a whole.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## What a data platform is

Chapter 6 admits the term is fresh and not yet settled: "the notion of the data platform frankly has yet to be fully fleshed out" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The working definition:

- A **core storage layer** (typically object-storage-backed).
- A **constellation of integrated tools** — ingestion, transformation, orchestration, catalog, access control, ML — that share authentication, metadata, and compute.
- **Tight integration** sufficient to reduce operational overhead compared to assembling equivalent best-of-breed tools.

Tools outside the platform can still interoperate with extra "data overhead for data interchange" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md), but with more friction.

## Why vendors push the platform framing

"The race is on to create a walled garden of data tools, both simplifying the work of data engineering and generating significant vendor lock-in" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The motivation is symmetric: customers get one bill, one set of credentials, one vendor to call when something breaks; vendors get retention and cross-sell.

This is a **rerun of the earlier warehouse-vendor pattern** at a higher level of abstraction. Teradata, Oracle, and IBM built tool stacks around their warehouses in the 1990s. Snowflake, Databricks, and the hyperscalers are doing the same on top of object storage in the 2020s — with the difference that open table formats (see [[lakehouse-table-formats]]) prevent the lock-in from being total.

## Platform vs. modular stack

The platform pitch stands in contrast to the [[modern-data-stack]], which emphasises **independent best-of-breed tools** connected via standard interfaces (SQL, Iceberg/Delta tables, dbt, Airflow). Chapter 4's [[technology-selection]] framing applies directly:

- **Platform advantages.** Less integration work; consistent security; single support vendor; metadata and lineage shared automatically.
- **Modular stack advantages.** Best tool per category; substitutability; no lock-in; easier to negotiate pricing.
- **Platform risks.** [[total-opportunity-cost-of-ownership|TOCO]] — what escape plans look like if the platform under-delivers or prices escalate.

Reis and Housley's guidance tracks the nine [[principles-of-good-data-architecture|architecture principles]]: favour reversibility, favour loose coupling, favour common components. A platform can embody all three — *if* the pieces speak open standards at the edges.

## The class leaders

Chapter 6 enumerates (implicitly and explicitly) the current class leaders (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **AWS, Azure, Google Cloud** — the hyperscaler platforms. Broadest tool span; tightest integration with the rest of cloud infrastructure (IAM, networking, ML).
- **Snowflake** — the warehouse-turned-platform. Added data sharing, marketplace, and Snowpark (Python/Java processing) to its core SQL warehouse.
- **Databricks** — the lake-turned-platform. Delta Lake as the storage layer; Spark, MLflow, Databricks SQL, Unity Catalog on top.

Chapter 3 describes the convergence narrative: warehouses and lakes are evolving toward each other, and the platforms are the commercial realisation of that convergence. See [[data-lakehouse]] and [[storage-compute-separation]].

## What a data engineer evaluates

Chapter 6's practical advice (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Does the platform's tool set cover the required lifecycle stages?** Missing stages mean integration work — and potentially re-introducing the problems the platform was supposed to solve.
- **How does the platform handle unstructured data?** Platforms now emphasise close integration with object storage for non-tabular use cases; this is where lakehouse-style capabilities matter.
- **How easily can non-platform tools integrate?** Open table formats, REST APIs, and metastore integrations are the escape hatches.

## Related pages

- [[data-lakehouse]]
- [[data-warehousing]]
- [[data-lake]]
- [[storage-compute-separation]]
- [[lakehouse-table-formats]]
- [[modern-data-stack]]
- [[proprietary-walled-garden]]
- [[total-opportunity-cost-of-ownership]]
- [[principles-of-good-data-architecture]]
- [[data-sharing]]
