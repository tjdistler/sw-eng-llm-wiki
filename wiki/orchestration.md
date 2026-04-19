# Orchestration

**Summary**: The fifth [[data-engineering-lifecycle|lifecycle]] **undercurrent** — coordinating many jobs to run as quickly and efficiently as possible on a scheduled cadence. An orchestration engine is not a scheduler: it knows about **job dependencies**, usually as a directed acyclic graph (DAG). Reis and Housley cite Nick Schrock: orchestration is "the center of gravity of both the data platform and the data lifecycle."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## Orchestration ≠ scheduling

A pure scheduler (cron) knows only about time. An orchestration engine layers **metadata about job dependencies** on top — usually as a directed acyclic graph (DAG). The DAG can run once or on a fixed interval (daily, hourly, every five minutes) (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 2 assumes throughout that an orchestration system stays online with high availability, so it can sense and monitor continuously without human intervention and run new jobs as they are deployed.

## What an orchestration engine does

Chapter 2 enumerates the responsibilities (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Monitor managed jobs** and kick off new tasks as DAG dependencies complete.
- **Monitor external systems** to watch for data arrival and criteria to be met.
- **Set error conditions and alert** via email/other channels when tasks go out of bounds (e.g., expected completion at 10 a.m. missed).
- **Job history, visualisation, alerting** — built-in operational dashboards.
- **Backfill** new DAGs or individual tasks as they're added.
- **Time-range dependencies** — e.g., a monthly reporting job checks that an ETL job completed for the full month before starting.

## History and current landscape

Chapter 2's brief history (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **2010s enterprises** used expensive, non-extensible workflow tools.
- **Apache Oozie** was popular in the 2010s but was designed to live inside a Hadoop cluster.
- **Facebook Dataswarm** (late 2000s) — internal use, inspired the next generation.
- **Apache Airflow** — introduced by Airbnb in 2014, open source, Python, highly extensible. The "mindshare leader for the time being."
- **Next generation:** **Prefect, Dagster** (improve portability and testability of DAGs — local dev to production), **Argo** (built around Kubernetes primitives), **Metaflow** (Netflix, aims at data-science orchestration).

## Orchestration is strictly a batch concept

Chapter 2 is specific: "orchestration is strictly a batch concept." The streaming alternative to orchestrated task DAGs is the **streaming DAG** — still hard to build and maintain, but next-generation streaming platforms like Pulsar aim to reduce the engineering and operational burden (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Airflow as Chapter 4's exemplar

Chapter 4 makes an explicit exception to its "don't discuss specific technology" rule to deep-dive on Airflow. The reasoning: orchestration is currently dominated by a single open-source technology (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md).

### Origins

- Maxime Beauchemin kicked off the Airflow project at Airbnb in 2014.
- Developed as a non-commercial open-source project from the start.
- Apache Incubator in 2016; full Apache project in 2019.

### Airflow advantages (Chapter 4)

- **Active open-source project** — high commit rate, quick response on bugs and security issues. Airflow 2 was a major refactor of the codebase.
- **Massive mindshare.** Vibrant community on Slack, Stack Overflow, GitHub — finding answers to questions is easy.
- **Commercially available** as a managed service or software distribution from GCP, AWS, Astronomer.io, and others. The [[commercial-oss|COSS]] form is well developed.

### Airflow disadvantages (Chapter 4)

- **Non-scalable core components** — the scheduler and backend database can become bottlenecks for performance, scale, and reliability.
- The scalable parts still follow a [[distributed-monolith]] pattern.
- **Lacks support for data-native constructs** — schema management, lineage, cataloging are weak.
- **Workflow development and testing is challenging.**

### Contenders

- **Prefect** and **Dagster** — rethink components of the Airflow architecture to solve the distributed-monolith and dev/test problems.

Chapter 4 is emphatic: "Will there be other orchestration frameworks and technologies not discussed here? Plan on it." Anyone choosing an orchestration technology today should study current options and watch for new entrants.

## Chapter 11 — the next generation of orchestration

Chapter 11 forecasts that orchestration will undergo significant enhancement as part of the emerging [[cloud-data-os|cloud-scale data OS]] (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Data-aware orchestration.** Integrates with data cataloging and [[data-lineage|lineage]] natively — the orchestrator understands the data it moves, not just the tasks.
- **Built-in IaC.** Terraform-style infrastructure declarations inside the pipeline. Missing Snowflake databases, Databricks clusters, Kinesis streams get provisioned automatically the first time a pipeline runs.
- **Built-in CI/CD.** GitHub-Actions-style or Jenkins-style deployment features baked into the orchestrator, so a pipeline author writes, tests, deploys, and monitors from a single code artifact.
- **Stream-pipeline orchestration.** A new generation of tools will stitch together managed stream processors (Kinesis Data Analytics, Google Cloud Dataflow, Pulsar) and monitor them as a unit. This is the streaming counterpart to Airflow's batch DAG.
- **Airflow, Dagster, Prefect continue.** Airflow will grow in capabilities on its mindshare; Dagster and Prefect will compete by rebuilding orchestration architecture from the ground up.

This is Chapter 11's operational counterpart to the [[live-data-stack]] prediction: the live data stack needs a live orchestrator.

## Relationship to the undercurrents

Orchestration is the glue binding many of the other undercurrents:

- **[[dataops|DataOps]]** — the DataOps automation story typically centres on moving cron jobs to orchestration frameworks.
- **[[software-engineering-for-data|Software engineering]]** — pipelines-as-code is the core concept of present-day orchestration: DAGs are Python code, tested and reviewed like any other software artefact.
- **[[metadata|Metadata]]** — pipeline metadata is a first-class output of orchestration; one motivator for the new generation of systems is better metadata capture.

## Cross-book connections

- [[distributed-cron]] (SRE Ch 24) covers the layer **below** orchestration — how to run cron reliably in a distributed environment.
- [[data-processing-pipelines]] (SRE Ch 25) and [[google-workflow]] name the Google-scale operational pathologies of periodic batch chains and Google's continuous-processing alternative.
- [[event-driven-batch-pattern]] (Burns) is the container-level analogue of an orchestration DAG — work queues linked by pub/sub.

## Related pages

- [[data-engineering-lifecycle]]
- [[dataops]]
- [[distributed-cron]]
- [[data-processing-pipelines]]
- [[google-workflow]]
- [[periodic-pipeline]]
- [[continuous-data-processing]]
- [[event-driven-batch-pattern]]
- [[batch-processing]]
- [[software-engineering-for-data]]
- [[distributed-monolith]]
- [[commercial-oss]]
- [[technology-selection]]
- [[cloud-data-os]]
- [[future-of-data-engineering]]
- [[live-data-stack]]
