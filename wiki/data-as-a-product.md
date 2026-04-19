# Data as a Product

**Summary**: The organisational stance that treats published datasets as first-class products — with identified consumers, documented SLAs, versioning, and a product manager — rather than as byproducts of application operations. One of Zhamak Dehghani's four pillars of the [[data-mesh]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`, `raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md`

**Last updated**: 2026-04-19

---

## The idea

Chapter 3 names "data as a product" as the second of the four [[data-mesh|data mesh]] principles (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). The underlying move:

- A traditional dataset is a **byproduct** — it exists because some operational system generated it, and downstream consumers take what they can get.
- A **data product** has deliberate consumers, a stable contract, documented quality, a discoverable catalogue entry, and a team that owns supporting it.

The posture is borrowed directly from software product management and applied to data assets.

## Qualities of a data product

Chapter 3 does not enumerate these exhaustively; the working list from Dehghani's *Data Mesh* and industry practice:

- **Discoverable** — listed in a [[data-catalog]] with enough [[metadata]] for a consumer to find it
- **Addressable** — a stable name/URL/schema the consumer can bind against
- **Trustworthy** — measurable [[data-quality]]; observability into freshness and completeness
- **Self-describing semantics** — consumer can understand what the fields mean
- **Interoperable** — uses shared schemas/types/identifiers where they exist
- **Secure** — access-controlled; see [[data-security]], [[data-governance]]

These properties echo the qualities a software product team would ship against.

## Hard Parts Ch 14 — the architectural consequence

*Software Architecture: The Hard Parts* Ch 14 (co-authored by Dehghani) restates the principle and names its **architectural consequence**: treating data as a product in a decentralised architecture introduces a new [[architectural-quantum|architecture quantum]] — the [[data-product-quantum]] — "to maintain and serve discoverable, understandable, timely, secure, and high-quality data to the consumers" (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md).

Ch 14's product qualities for a mesh DPQ:

- **Discoverable** — findable across the mesh via platform search and browsing.
- **Understandable** — self-describing semantics; the consumer can read and interpret the data.
- **Timely** — freshness meets consumer SLAs.
- **Secure** — federated governance policies enforced as embedded code on every access.
- **High-quality** — observed, tested, and supported.

The point the architect takes away: the product is not a dataset. It is a deployable unit — a DPQ — that delivers on those qualities as a matter of *operational* architecture, not just documentation.

## Relationship to the engineer

The data engineer becomes responsible for:

- Treating downstream analysts, ML engineers, and other domain teams as **customers**
- Running the data product like a product team runs a feature — backlog, roadmap, on-call
- Publishing a [[data-contract]] that is stable enough for consumers to depend on

This aligns with [[dataops]]'s framing of data outputs as products rather than one-off reports.

## Chapter 9 — the product-design sibling

Chapter 9 adds a parallel concept: **[[data-product|data product]]** — DJ Patil's definition of "a product that facilitates an end goal through the use of data." Where *data as a product* (this page) is the organisational stance that every dataset is a first-class product, *data product* is the user-facing artifact that embodies that stance — a dashboard, a scored lead list, a recommendation feed. Chapter 9's product-design questions apply at the artifact level: jobs to be done, positive feedback loops, internal vs external users, ROI (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

See [[data-product]] for the full Chapter 9 treatment.

## Reverse ETL and data as a product

[[reverse-etl]] — pushing analytical data back into operational systems — is one of the drivers behind treating data as a product. Once a warehouse table is feeding Salesforce or the marketing automation system, downtime becomes an operational incident, not a reporting inconvenience. Product-grade reliability becomes mandatory (source framing: chapter-03-designing-good-data-architecture.md).

## Related pages

- [[data-product]]
- [[data-mesh]]
- [[dataops]]
- [[data-quality]]
- [[data-contract]]
- [[data-catalog]]
- [[data-governance]]
- [[reverse-etl]]
- [[data-serving]]
- [[trust-in-data]]
- [[data-product-quantum]]
- [[architectural-quantum]]
- [[software-architecture-the-hard-parts]]
