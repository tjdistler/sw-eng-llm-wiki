# Master Data Management

**Summary**: Master data management (MDM) is the practice of building consistent entity definitions — known as **golden records** — for business entities such as employees, customers, products, and locations. An undercurrent of the [[data-engineering-lifecycle]] that sits inside [[data-management]]'s [[data-governance|governance]] area and typically involves a dedicated cross-organisation team the data engineer collaborates with.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What master data is

Master data is data **about business entities** — employees, customers, products, locations. As an organisation grows through organic expansion, acquisitions, and partnerships, maintaining a consistent picture of entities and identities becomes dramatically harder (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Golden records

MDM is the practice of harmonising entity data across the organisation into **golden records** — a single, agreed definition of each entity that is consistent across divisions and partners (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## A business-process problem with technical support

Reis and Housley are clear that MDM is "a business operations process facilitated by building and deploying technology tools." Chapter 2's example: an MDM team sets a standard format for addresses, then works with data engineers to build an API returning consistent addresses and a system that matches customer records across company divisions using that address data (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Organisational placement

MDM reaches across the full data cycle into operational databases. It may sit directly under data engineering's responsibility, but is **often the assigned responsibility of a dedicated team** that works across the organisation. Even when they don't own it outright, "data engineers must always be aware of it, as they will collaborate on MDM initiatives" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Cross-book connection

[[serving-state-from-edm]] (Bellemare) shows the event-driven counterpart: services derive their own local view of customer/product master data from the producer's entity event stream rather than querying a central MDM service, avoiding the shared-database antipattern. Both approaches aim for the same thing — consistent entity views across the organisation.

## Related pages

- [[data-management]]
- [[data-governance]]
- [[data-engineering-lifecycle]]
- [[serving-state-from-edm]]
- [[entity-event]]
- [[materialized-state]]
