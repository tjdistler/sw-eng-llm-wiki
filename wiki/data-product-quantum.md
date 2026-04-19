# Data Product Quantum

**Summary**: A **data product quantum (DPQ)** is the architectural unit of a [[data-mesh]] — a cooperative [[architectural-quantum|quantum]] that lives adjacent to a domain microservice and serves that domain's analytical data to the rest of the organisation. Coined by Zhamak Dehghani and treated in *Software Architecture: The Hard Parts* Chapter 14, the DPQ extends the quantum concept from operational services to analytical data.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md`

**Last updated**: 2026-04-19

---

## The idea

In a [[data-mesh]], analytical data is not extracted out of domains into a central warehouse or lake. Instead, each domain team publishes its analytical data as a product — discoverable, addressable, trustworthy, and interoperable. The DPQ is the *architectural* shape of that product (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md):

- A domain service (e.g. `Alpha`) contains operational code and transactional (OLTP) data.
- Alongside it, a **data product quantum** contains its own code and data, acting as the interface for Alpha's analytical and reporting needs.
- The two deploy independently but are tightly coupled contractually — they are *cooperating quanta*.

Ch 14's one-line picture: "the DPQ acts as an operationally independent but highly coupled set of behaviors and data" (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md).

## Relationship to the architectural quantum

The DPQ is an [[architectural-quantum]] in its own right. It has independent deployability, its own functional cohesion (serving analytical views of the domain), and its own dynamic-coupling characteristics. It sits at the **static-coupling** envelope of the domain service — "the DPQ and its communication implementation belong to the static coupling of an architecture quantum" — the same way a required message broker does: the service plane must be available for the architecture to function as designed (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md).

The book explicitly connects the idea to the [[sidecar-pattern]] / [[service-mesh]] lineage: analytical data is an **[[orthogonal-coupling|orthogonal concern]]** to the operational domain, and the DPQ is the data-side analogue of the sidecar — a cooperating quantum that implements the orthogonal cross-cutting concern without entangling the operational service's implementation.

## Three types of DPQ

Ch 14 catalogues the common DPQ flavours (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md):

| DPQ type | Role |
|---|---|
| **Source-aligned (native) DPQ** | Provides analytical data on behalf of the collaborating operational quantum (typically a microservice). The default. |
| **Aggregate DPQ** | Aggregates data from multiple input DPQs, either synchronously or asynchronously. |
| **Fit-for-purpose DPQ** | Custom-built for a specific requirement — analytical reporting, BI, ML training, or another supporting capability. |

An analytics/BI subsystem in a mesh architecture typically forms its own quantum that has **static quantum coupling** to the individual DPQs it draws from, with calls either synchronous or asynchronous depending on the request type (some DPQs expose a SQL interface for synchronous querying).

## Cooperative quantum semantics

The book defines **cooperative quantum** specifically to name the service-plus-DPQ pair (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md):

> An operationally separate quantum that communicates with its cooperator via asynchronous communication and eventual consistency, yet features tight contract coupling with its cooperator and generally looser contract coupling to the analytics quantum.

Key properties:

- **Operationally independent** from the domain service — different deploy cadence, different runtime characteristics, different scaling envelope.
- **Tight contract with its cooperator** — the DPQ and its domain service agree on the shape of the data flowing between them.
- **Looser contract with the analytics quantum** — consumers of the DPQ bind against its published analytical contract; the DPQ can absorb upstream churn behind that contract.
- **Asynchronous, eventually consistent** communication between service and DPQ — never transactional.

## Dynamic coupling constraint

Chapter 14 is explicit about what the DPQ's dynamic coupling must look like (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md):

> From a dynamic quantum coupling standpoint, the data sidecar should always implement one of the communication patterns that features both eventual consistency and asynchronicity: either the Parallel Saga(aeo) pattern or the Anthology Saga(aec) pattern. A data sidecar should never include a transactional requirement to keep operational and analytical data in sync, which would defeat the purpose of using a DPQ for orthogonal decoupling.

The picks are [[parallel-saga]] or [[anthology-saga]] — both async, eventual. A DPQ that requires transactional consistency with its operational cooperator has failed at its architectural job.

Communication outward to the analytics plane is also generally **asynchronous**, so that analytical workloads do not impact the operational architecture characteristics of the domain service.

## Why the DPQ exists

The DPQ is the structural answer to the failure modes of the [[data-warehousing|data warehouse]] and [[data-lake]] patterns in microservices architectures (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md):

- Warehouses and lakes separate data from its domain context, losing the very partitioning that microservices work hard to preserve.
- They rely on brittle ETL / schema pipelines that re-couple domains through the analytics layer.
- They assume a central team builds and owns the analytical assets — domain teams are second-class.

The DPQ puts analytical data back inside the domain boundary. The domain team — which already understands the semantics, the PII constraints, and the business invariants — owns the analytical product for that domain. Cross-domain analytics happens by composing DPQs, not by hauling raw data to a central lake.

## Related pages

- [[data-mesh]]
- [[architectural-quantum]]
- [[data-as-a-product]]
- [[data-product]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[orthogonal-coupling]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[parallel-saga]]
- [[anthology-saga]]
- [[cross-service-analytics]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-governance]]
- [[software-architecture-the-hard-parts]]
