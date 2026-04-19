# Managed Connector

**Summary**: A third-party-operated data-ingestion connector that abstracts the plumbing of pulling data from a specific source (database, SaaS API, file system) and landing it in a specific target (warehouse, lake). Fivetran, Airbyte, Matillion, and Stitch are the canonical examples. Reis and Housley's recommendation is blunt: "the creation and management of data connectors is largely undifferentiated heavy lifting these days and should be outsourced whenever possible."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The pitch

A managed connector provides, out of the box (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- A library of pre-built connectors to common sources (databases, SaaS APIs).
- Configuration for target, source, ingestion mode (CDC, replication, truncate-and-reload), permissions, credentials, and update frequency.
- Ongoing operation: the vendor or cloud manages and monitors data syncs; failures raise alerts with logged error information.
- Frameworks for building **custom** connectors when a needed source isn't pre-built.

The promise: set it up once, and the nitty-gritty details of connection management become someone else's problem.

## Why Reis and Housley recommend them

Ch 7's argument is an application of the broader FoDE theme — focus on high-value work, use managed services for everything that is undifferentiated (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Writing and maintaining API connectors is "plumbing" — important but not strategically differentiating.
- External data sources change constantly (APIs, schemas, auth), and the maintenance cost falls on the engineer writing the connector.
- Vendors and OSS projects "typically have hundreds of prebuilt connector options and can easily create custom connectors."
- Even custom API connectors are increasingly supported inside managed services — sometimes as declarative YAML, sometimes as code that runs in a serverless function framework (AWS Lambda) with scheduling and sync handled by the service.

"While a managed service might look like an expensive option, consider the value of your time and the opportunity cost of building API connectors when you could be spending your time on higher-value work" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## When to still write your own

Ch 7 is not absolutist — some APIs are not well supported, and custom connection work will always exist. "Reserve your custom connection work for APIs that aren't well supported by existing frameworks; you will find that there are still plenty of these to work on" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

For custom connector work, the book's two-part guidance:

1. **Software development practices.** Version control, continuous delivery, automated testing. A connector is production code.
2. **Ops practices.** Use an orchestration framework (Airflow, Dagster, Prefect) to "dramatically streamline the operational burden" — scheduling, dependency management, retries, observability.

## Fit with the broader ingestion picture

Managed connectors sit alongside the other ways to ingest data enumerated in Ch 7:

- **Direct DB connection** (JDBC/ODBC) — a managed connector often wraps this under the hood.
- **[[change-data-capture|CDC]]** — most managed connectors support batch and log-based CDC modes.
- **APIs** — the main value proposition for SaaS data ingestion.
- **[[message-brokers|Message queues and event streams]]** — often outside the managed-connector scope; streaming ingestion is typically a separate managed service (Kinesis, Pub/Sub, managed Kafka).
- **[[data-sharing]]** — increasingly the alternative when the source supports it; no connector needed.

## Chapter 11 — connectors as a growth driver

Chapter 11 revisits managed connectors as a key force driving the decline of complexity. Reis and Housley note that "API connectors will be an outsourced problem so that data engineers can focus on the unique issues that drive their businesses" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). The intersection of red-hot competition in data-tooling with a growing number of engineers means these tools will continue decreasing in complexity while gaining functionality — which, in turn, grows the practice of data engineering rather than shrinking it.

## Connection to the modern data stack

Managed connectors are one of the defining components of the [[modern-data-stack]]. Ch 4 already positioned Fivetran et al. as canonical MDS tools; Ch 7 is the operational argument for why they belong there.

## Related pages

- [[data-ingestion]]
- [[modern-data-stack]]
- [[etl-vs-elt]]
- [[change-data-capture]]
- [[orchestration]]
- [[build-vs-buy]]
- [[third-party-api-integration]]
- [[data-sharing]]
- [[software-engineering-for-data]]
- [[future-of-data-engineering]]
- [[cloud-data-os]]
