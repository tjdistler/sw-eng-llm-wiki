# DataOps

**Summary**: The application of Agile, [[devops-vs-sre|DevOps]], and statistical-process-control culture to data pipelines and analytics. One of the six "undercurrents" of the [[data-engineering-lifecycle]] — fundamentally a cultural movement about collaboration, automation, observability, and rapid feedback across data producers, engineers, and consumers, not a specific tool stack. Chapter 2 names **three core technical pillars: automation, monitoring/observability, and incident response**.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What it is

DataOps is a counterpart to DevOps for data work. Chapter 1 places it as one of the six undercurrents that span every stage of the [[data-engineering-lifecycle]] — alongside security, data management, data architecture, orchestration, and software engineering (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Reis and Housley stress repeatedly that **DataOps is fundamentally cultural**, not a technology choice:

> Agile, DevOps, and DataOps are fundamentally cultural, requiring buy-in across the organization. (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md)

Many technologists mistakenly believe these practices can be solved by adopting a tool. The authors call this "dangerously wrong."

## Data products vs software products

Chapter 2 makes a specific distinction between data products and software products (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Software products** provide specific functionality and technical features for end users.
- **Data products** are built around **sound business logic and metrics** whose users make decisions or build models that perform automated actions.

A data engineer must understand both the technical aspects of building software products and the business logic, quality, and metrics that make excellent data products.

## Relation to Agile, DevOps, SPC

DataOps inherits from three older disciplines (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Agile** — iterative delivery, short feedback loops, collaboration with stakeholders.
- **[[devops-vs-sre|DevOps]]** — software engineers own operational responsibilities; heavy automation; blameless culture.
- **Statistical process control (SPC)** — watching process metrics against expected bounds; deciding which deviations are signal and which are noise.

Like DevOps, DataOps borrows from **lean manufacturing and supply-chain management** — mixing people, processes, and technology to reduce time to value.

## The DataKitchen definition

Chapter 2 quotes Data Kitchen's definition (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

> DataOps is a collection of technical practices, workflows, cultural norms, and architectural patterns that enable:
> - Rapid innovation and experimentation delivering new insights to customers with increasing velocity
> - Extremely high data quality and very low error rates
> - Collaboration across complex arrays of people, technology, and environments
> - Clear measurement, monitoring, and transparency of results

## Where to start

Chapter 2's practical advice for adopting DataOps into an existing organisation (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Greenfield** — if the company has no preexisting data infrastructure, bake DataOps in from day one.
- **Brownfield with no DataOps** — start by adding **observability and monitoring** to get a window into system performance; then **automation**; then **incident response**.
- **Mature DataOps team** — work alongside them to improve the lifecycle.

## The three core technical pillars

Chapter 2 names three pillars (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

### 1. Automation

Reliability and consistency; quick deployment of new product features and improvements. DataOps automation has a similar framework to DevOps: **change management (environment, code, and data version control), CI/CD, and configuration as code**. See [[infrastructure-as-code]]. DataOps adds specific dimensions: data quality, data/model drift detection, metadata integrity.

Chapter 2's hypothetical maturity arc:

- **Low maturity** — stages scheduled by cron jobs on a cloud instance. Works for a while, but jobs stop unexpectedly, long-running jobs cause subsequent failures, and the team learns of failures from analysts whose reports are stale.
- **Mid maturity** — adopt an [[orchestration]] framework (Airflow, Dagster). Dependencies are checked before jobs run. More jobs fit into a given time because each starts when its inputs are ready.
- **Higher maturity** — after a data scientist deploys a broken DAG and brings down the orchestrator, the team blocks manual DAG deployments. They adopt automated DAG deployment with testing, monitoring of new-DAG startup, and blocking of unvalidated Python dependency changes.

"Embrace change" — from the DataOps Manifesto — is the underlying tenet: not change for its own sake, but goal-oriented change.

### 2. Monitoring and observability

See [[data-observability]] and [[monitoring-and-observability]]. "Data is a silent killer" — bad data lingers in reports for months without detection unless you are explicitly looking for it (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 2 cites Andy Petrella's **Data Observability Driven Development (DODD)** — the data analogue of TDD — as a framework for treating observability as a first-class lifecycle concern.

### 3. Incident response

Mistakes happen; a high-functioning DataOps team **expects them and prepares**. Incident response uses automation and observability to rapidly identify root causes and resolve them. It is technical **and** cultural: "open and blameless communication, both on the data engineering team and across the organization" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 2 quotes Werner Vogels: "Everything breaks all the time." Engineers should proactively find issues before the business reports them — trust takes a long time to build and can be lost in minutes.

## DataOps summary (Chapter 2's own)

"At this point, DataOps is still a work in progress." Practitioners have adapted DevOps principles to data reasonably well; the DataOps Manifesto is the initial cultural-principles document. "Many data engineering tools, especially legacy monoliths, are not automation-first." Adoption of automation best practices across the lifecycle is a recent but growing movement; Airflow "paved the way" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Why it matters for data engineering

The chapter frames DataOps adoption as a Stage 2 ([[data-maturity|scaling with data]]) inflection point. Stage 1 companies are still getting anything working; Stage 2 is where the engineer starts formalising practices and adopting [[devops-vs-sre|DevOps]] and DataOps; Stage 3 is where "enterprisey" data management (governance, quality, [[data-lineage|lineage]]) sits atop a mature DataOps foundation (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## DataOps in technology selection (Chapter 4)

Chapter 4 treats DataOps as one of the undercurrents a selected technology must support. Two selection questions Chapter 4 calls out (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Deployment control and alerting.** For OSS you self-host, you own monitoring, hosting, deployment, incident response. For managed offerings, much of the operational responsibility shifts to the vendor — weigh the vendor's SLA, alerting channels, transparency, and ETA to fix.
- **Automation surface.** If the technology is not automation-first (many legacy monoliths aren't), the team will pay a cost over its lifetime that's easy to underestimate at the evaluation stage.

This is the undercurrent lens on the same pattern Chapter 4 applies throughout: "whatever technology you choose, be sure to understand how it supports the undercurrents of the data engineering lifecycle."

## Connections to existing wiki concepts

DataOps as practised touches several concepts the wiki already covers from other sources:

- **Pipeline observability** — [[data-observability]], [[pipeline-monitoring-problems]], [[monitoring-and-observability]].
- **Data quality and validation** — [[data-validation-pipelines]], [[data-integrity-principles]], [[data-quality]].
- **Reliable pipeline operation** — [[data-processing-pipelines]], [[google-workflow]] (SRE Ch 25).
- **Release and change management** — [[continuous-integration-delivery-deployment]], [[infrastructure-as-code]], [[blue-green-deployment]].
- **Incident response for data** — [[blameless-postmortem]], [[incident-management-framework]].

The data-engineering literature is converging on the same reliability/operational principles that SRE named a decade earlier — DataOps is the name for that convergence applied to data systems.

## Related pages

- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-maturity]]
- [[devops-vs-sre]]
- [[sre-discipline]]
- [[data-observability]]
- [[data-validation-pipelines]]
- [[data-quality]]
- [[data-lineage]]
- [[orchestration]]
- [[infrastructure-as-code]]
- [[fundamentals-of-data-engineering]]
- [[technology-selection]]
