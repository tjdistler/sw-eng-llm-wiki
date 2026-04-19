# Software Engineering for Data

**Summary**: The sixth [[data-engineering-lifecycle|lifecycle]] **undercurrent** — the application of general software-engineering practices (version control, testing, CI/CD, infrastructure-as-code, pipelines-as-code, general-purpose problem solving) to data code. Chapter 2 argues that despite decades of rising abstraction over low-level data plumbing, software engineering remains **central** to data engineering.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Why software engineering is still central

Early modern data engineers (2000–2010) wrote MapReduce jobs in C, C++, and Java at a low level. The mid-2010s brought frameworks that abstracted those details away; that abstraction continues today — cloud data warehouses with SQL semantics, Spark's user-friendly DataFrame API, and managed services of all kinds. Yet software engineering remains critical (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 2 enumerates several areas where software engineering still matters.

## Core data-processing code

Even at higher levels of abstraction, core data-processing code must still be written across ingestion, transformation, and serving. Data engineers "need to be highly proficient and productive in frameworks and languages such as Spark, SQL, or Beam." The authors assert: "we reject the notion that SQL is not code" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Engineers must know proper **code-testing methodologies**: unit, regression, integration, end-to-end, and smoke tests.

## Open-source framework development

Many data engineers contribute to open-source frameworks. In the big-data era, the Hadoop ecosystem saw a "Cambrian explosion" of data-processing frameworks focused on transform-and-serve stages.

The current emphasis has shifted **up the ladder of abstraction, away from direct data processing**. New tools assist with managing, enhancing, connecting, optimising, and monitoring data. Airflow dominated orchestration from 2015 to the early 2020s; Prefect, Dagster, and Metaflow sprung up to address its limitations in metadata handling, portability, and dependency management (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 2's practical advice: before building new internal tools, survey the landscape of publicly available tools. Consider total cost of ownership (TCO) and opportunity cost. An open-source project likely already exists.

## Streaming software engineering

Stream processing is inherently more complicated than batch, and the tools and paradigms are less mature. Streaming joins become more complex than their batch equivalents; engineers must write code to apply **[[windowing]] methods** to calculate trailing statistics.

Available frameworks (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Function platforms** — OpenFaaS, AWS Lambda, Google Cloud Functions — for handling individual events.
- **Dedicated stream processors** — Spark (Structured Streaming), Beam, Flink, Pulsar — for analysing streams to support reporting and real-time actions.

## Infrastructure as code

Infrastructure-as-code (IaC) applies software-engineering practices to the configuration and management of infrastructure. See [[infrastructure-as-code]].

The infrastructure-management burden of the big-data era has decreased as companies migrated to managed systems (Databricks, Amazon EMR, cloud data warehouses). When engineers still have to manage cloud infrastructure, they increasingly do it through IaC frameworks rather than spinning up instances manually.

IaC also extends to containers and Kubernetes via tools like Helm. These practices are core to DevOps and to [[dataops|DataOps]] (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Pipelines as code

Pipelines-as-code is the core concept of present-day [[orchestration]] systems. Engineers use code (typically Python) to declare data tasks and dependencies; the orchestration engine interprets the code to run steps on available resources (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## General-purpose problem solving

Regardless of the high-level tools adopted, data engineers will encounter **corner cases** that require writing custom code — data sources without connectors in Fivetran/Airbyte/Singer, odd APIs, unusual formats. Engineers must be proficient at understanding APIs, pulling and transforming data, handling exceptions (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Cross-book connections

- [[continuous-integration-delivery-deployment]] — the DevOps CI/CD pipeline this page inherits.
- [[dataops]] — the cultural-operational layer that software engineering enables.
- [[infrastructure-as-code]] — its own page.
- [[data-processing-pipelines]] (SRE Ch 25) — operational complement covering large-scale pipeline failure modes.

## Related pages

- [[data-engineering-lifecycle]]
- [[dataops]]
- [[orchestration]]
- [[infrastructure-as-code]]
- [[continuous-integration-delivery-deployment]]
- [[windowing]]
- [[stream-processing]]
- [[testing-for-reliability]]
