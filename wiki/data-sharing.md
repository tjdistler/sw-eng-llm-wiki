# Data Sharing

**Summary**: A multitenant cloud-platform capability that lets one tenant selectively expose their data to other tenants without copying it or shipping files around. Data sharing is the cloud-era alternative to building a proper API or an SFTP feed, and it is the infrastructure underneath **data marketplaces** and increasingly underneath [[data-mesh]]-style intra-organizational data distribution.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The idea

"The core concept of cloud data sharing is that a multitenant system supports security policies for sharing data among tenants" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). Concretely, any cloud object store with a fine-grained permission system qualifies, as do all the major cloud data warehouses (Snowflake, BigQuery, Databricks).

The shared data is *not copied*. Consumer queries hit the provider's storage in place, with access governed by the platform's IAM policies. Reis and Housley observe that modern sharing platforms support **row, column, and sensitive-data filtering** so a provider can expose a subset of a dataset to a given consumer without needing to materialize that subset separately (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Data marketplaces

A data marketplace is a centralized venue built on top of data-sharing infrastructure, where data providers advertise datasets and consumers can subscribe without negotiating connectivity, data formats, or API credentials. Reis and Housley: "Data marketplaces provide a centralized location for data commerce, where data providers can advertise their offerings and sell them without worrying about the details of managing network access to data systems" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

Common venues: Snowflake Marketplace, AWS Data Exchange, Databricks Marketplace, Google Analytics Hub. These map one-to-one onto the cloud data-warehouse ecosystem.

## Two uses of data sharing

Reis and Housley call out two practical applications (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Third-party data acquisition.** Instead of paying a vendor for a data feed delivered via API or SFTP, the consumer subscribes to the provider's shared dataset and queries it directly in their own warehouse. See [[third-party-api-integration]] for the comparison point.
- **Decentralized intra-organizational data distribution.** Units of an organization manage their own data, expose subsets to other units via shared datasets, and each unit pays only for its own compute. This is the infrastructure layer that [[data-mesh]] depends on — domain-owned data products, self-serve access, federated governance.

## Alignment with principles-of-good-architecture

Reis and Housley are explicit about the architectural fit: "Data sharing and data mesh align closely with our philosophy of common architecture components. Choose common components that allow the simple and efficient interchange of data and expertise rather than embracing the most exciting and sophisticated technology" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). Data sharing is the concrete technology that realises one of the Chapter 3 [[principles-of-good-data-architecture|nine principles]] — choose common components — in practice.

## Limitations

- **Platform lock-in.** Data sharing is implemented at the platform layer; cross-platform sharing (Snowflake-to-BigQuery, for example) still requires export/import today. See [[multicloud]].
- **Governance overhead.** Selective sharing works only if the provider has the metadata and policy discipline to enforce it — see [[data-governance]].
- **Hidden cost model.** Consumer-side compute is still paid by the consumer; a shared dataset's "cheapness" can evaporate under large analytical queries.

## Ch 7 — is this actually ingestion?

Chapter 7 of *Fundamentals of Data Engineering* makes a subtle technical point about data sharing's relationship to [[data-ingestion|ingestion]]: **in the strict sense, it isn't ingestion**. "These datasets are often shared in a read-only fashion, meaning you can integrate these datasets with your own data (and other third-party datasets), but you do not own the shared dataset. In the strict sense, this isn't ingestion, where you get physical possession of the dataset. If the data provider decides to remove your access to a dataset, you'll no longer have access to it" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

This is a significant architectural property. A dataset you "ingested" via data sharing:

- Is not copied into your own storage.
- Is governed by the provider's access controls and availability.
- Can disappear without notice if the sharing relationship ends.
- Is queryable in place — your warehouse's query engine reads the provider's storage directly.

For many analytics use cases this is perfectly fine — and in fact the cost and governance advantages are real. But for use cases that require **durable access independent of the provider** (regulatory retention, disaster-recovery snapshots), data sharing is not a substitute for genuine ingestion; you would need to additionally copy the shared data into your own storage.

Ch 7 places data sharing in its enumeration of ingestion mechanisms anyway, because from the consumer's point of view it is a practical alternative to ingesting via API or SFTP. The qualifier is important for architectural planning.

## Cross-book connections

- [[data-mesh]] (Dehghani via Reis & Housley) — data sharing is the enabling infrastructure for a mesh's data-as-a-product layer.
- [[data-as-a-product]] — a shared dataset, when paired with documentation, SLAs, and a schema contract, becomes the technical realisation of a "data product."
- [[principles-of-good-data-architecture]] — choose common components; sharing is one such component.
- [[third-party-api-integration]] — data sharing is the alternative to pulling data through an external API.

## Related pages

- [[data-mesh]]
- [[data-as-a-product]]
- [[data-warehousing]]
- [[principles-of-good-data-architecture]]
- [[third-party-api-integration]]
- [[source-systems]]
- [[multicloud]]
- [[data-governance]]
- [[data-ingestion]]
