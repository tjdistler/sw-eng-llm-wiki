# Data Management

**Summary**: The second of the six [[data-engineering-lifecycle|lifecycle]] **undercurrents**. An umbrella discipline covering [[data-governance|governance]], [[data-modeling|modeling]], [[data-lineage|lineage]], storage and operations, integration and interoperability, [[data-lifecycle-management|lifecycle management]], advanced analytics/ML data systems, and ethics/privacy. The DAMA DMBOK defines it as "the development, execution, and supervision of plans, policies, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their lifecycle."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Why data management is on the list

Reis and Housley observe that old-school data management — long dismissed as "corporate" and relevant only to huge enterprises — is now filtering into companies of all sizes. As data tools become simpler and less complex to manage, the data engineer moves up the value chain toward practices like governance, master data management, data-quality management, and metadata management. "Data engineering is becoming enterprisey," they write, and they frame it as a good thing (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The authors quote the DAMA DMBOK definition of data management:

> "Data management is the development, execution, and supervision of plans, policies, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their lifecycle." (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md)

Without such a framework, "data engineers are simply technicians operating in a vacuum."

## Why it matters

Chapter 2 argues that data management demonstrates that data is as vital to daily operations as financial resources, finished goods, or real estate. A cohesive data-management framework lets the organisation get value from data and handle it appropriately (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## The facets

Chapter 2 names these facets (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

| Facet | Wiki page |
|---|---|
| Data governance (discoverability, accountability, security) | [[data-governance]] |
| Data modeling and design | [[data-modeling]] |
| Data lineage | [[data-lineage]] |
| Storage and operations | [[data-storage-stage]] |
| Data integration and interoperability | [[data-integration]] |
| Data lifecycle management (archival, destruction, retention) | [[data-lifecycle-management]] |
| Data systems for advanced analytics and ML | [[analytics]], [[feature-store]] |
| Ethics and privacy | [[data-ethics]] |

## Master data management

An additional pillar the chapter highlights: [[master-data-management|MDM]] — building consistent entity definitions ("golden records") for business entities like employees, customers, products, and locations. Often owned by a dedicated cross-organisation team rather than data engineering, but the data engineer collaborates heavily (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Related pages

- [[data-engineering-lifecycle]]
- [[data-governance]]
- [[data-modeling]]
- [[data-lineage]]
- [[data-quality]]
- [[metadata]]
- [[master-data-management]]
- [[data-integration]]
- [[data-lifecycle-management]]
- [[data-ethics]]
