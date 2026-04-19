# Data Catalog

**Summary**: A system for making data discoverable by cataloguing what exists, what it means, who owns it, and where it came from. A concrete implementation of [[metadata|metadata management]] and the engine of [[data-governance|discoverability]]. Chapter 2 notes "we're seeing a proliferation of data catalogs, data-lineage tracking systems, and metadata management tools" as part of the data-management maturation of the discipline.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## What a data catalog holds

A catalog is where both auto-generated and human-generated [[metadata|metadata]] collects. From Chapter 2's framing of metadata (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Business metadata** — what a "customer" means for the business, how fields are defined, who owns which tables.
- **Technical metadata** — schemas, lineage, field mappings, pipeline workflows.
- **Operational metadata** — job runs, error rates, SLAs.
- **Reference metadata** — lookup data (internal codes, geographic codes, units).

The data engineer uses the catalog as a **design input** — it becomes "a foundation for designing pipelines and managing data throughout the lifecycle," not just documentation generated after the fact (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Auto vs human-generated

Chapter 2 emphasises both modes (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Auto-generated** — tools crawl databases for relationships, monitor pipelines to track data flow. Example: crawling and cataloging tables and columns across every DB in the organisation.
- **Human-generated** — owners, consumers, domain experts, anecdotes. The social element of data. Airbnb's **Dataportal** concept is cited as the canonical human-oriented system.

"Documentation and internal wiki tools provide a key foundation for metadata management, but these tools should also integrate with automated data cataloging. For example, data-scanning tools can generate wiki pages with links to relevant data objects."

## The interoperability problem

Chapter 2 is honest about the current state: "interoperability and standards are still lacking. Metadata tools are only as good as their connectors to data systems and their ability to share metadata" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). The engineer evaluating a catalog must look hard at what it can actually talk to.

## Ch 6 — catalogs across the storage layers

Chapter 6 positions the catalog as infrastructure that spans every storage abstraction (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> Strictly speaking, a data catalog is not a top-level data storage abstraction, but it integrates with various systems and abstractions. Data catalogs typically work across operational and analytics data sources, integrate data lineage and presentation of data relationships, and allow user editing of data descriptions.

Three concrete Chapter 6 points:

- **Catalog application integration.** Ideally, data applications are designed to call catalog APIs directly to publish and update their metadata. As catalogs become widely adopted, this pattern is more achievable.
- **Automated scanning.** In practice, catalogs rely on scanners that crawl databases, lakes, and warehouses to collect metadata. Scanners can also *infer* metadata — relationships between tables, presence of sensitive data — that owners never explicitly recorded.
- **Data portal and social layer.** A web UI for search and relationship browsing, plus wiki-style annotations from users. Airbnb's Dataportal is the canonical reference.

## Ch 6 — catalogs as a lakehouse ingredient

Chapter 6 gives the catalog a specific structural role in the [[data-lakehouse|lakehouse]] (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> Data catalogs make metadata easily available to systems. For instance, a data catalog is a key ingredient of the data lakehouse, allowing table discoverability for queries.

Lakehouse systems like Databricks Unity Catalog, AWS Glue, Hive Metastore, and Iceberg REST catalogs are the operational plumbing that lets the same object-storage bucket present tables to multiple query engines. Without a catalog, the [[lakehouse-table-formats|table format]] metadata is just files on disk that each engine has to find separately.

## Related pages

- [[metadata]]
- [[data-governance]]
- [[data-management]]
- [[data-lineage]]
- [[schema-registry]]
- [[data-engineering-lifecycle]]
- [[data-lakehouse]]
- [[lakehouse-table-formats]]
- [[schema-on-read-vs-write]]
