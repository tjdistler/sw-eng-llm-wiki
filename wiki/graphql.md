# GraphQL

**Summary**: A query language for application data, created at Facebook as an alternative to REST. Where a REST endpoint returns a fixed resource shape, a GraphQL query **describes the subset of data the client wants** across potentially multiple underlying data models in a single request. From a [[source-systems|source-system]] perspective, GraphQL is one of the three HTTP-based API paradigms a data engineer regularly encounters, alongside REST and [[rpc|gRPC]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The idea

GraphQL was created at Facebook and released as an open standard. It is "a query language for application data and an alternative to generic REST APIs." The distinguishing property: "whereas REST APIs generally restrict your queries to a specific data model, GraphQL opens up the possibility of retrieving multiple data models in a single request. This allows for more flexible and expressive queries than with REST" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

GraphQL is **built around JSON and returns data in a shape resembling the JSON query** — the client specifies the fields it wants; the server returns exactly those fields nested exactly how the client asked (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Contrast with REST

| Dimension | REST | GraphQL |
|---|---|---|
| Request shape | Fixed endpoints, fixed response shapes | Client-specified query document |
| Data models per request | Typically one resource | Multiple, joined server-side |
| Over-fetching | Common — endpoints return more than needed | Rare — client asks for fields explicitly |
| Under-fetching | Common — requires multiple round trips | Rare — one query aggregates |
| Caching story | HTTP cache plays well | HTTP cache does not apply naturally — requires GraphQL-aware tooling |
| Discoverability | Informal (OpenAPI documents help) | Schema is first-class and introspectable |

"There's something of a holy war between REST and GraphQL, with some engineering teams partisans of one or the other and some using both. In reality, engineers will encounter both as they interact with source systems" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## As a source-system interface

From the data engineer's perspective:

- **Advantage: fewer round trips.** A complex cross-entity extraction can be expressed as a single GraphQL query, rather than as N REST calls stitched together on the client.
- **Advantage: explicit schema.** GraphQL schemas are machine-readable; code generation is straightforward.
- **Disadvantage: query complexity budgeting.** A GraphQL endpoint that allows arbitrary joins over an underlying relational store can be overloaded by a single deep query. Producers commonly impose depth limits, rate limits, or cost budgets.
- **Disadvantage: caching.** Unlike REST's URL-keyed cache, GraphQL responses are keyed by query document. Standard HTTP caches don't help; downstream systems often resort to their own application-level caches.
- **Disadvantage: less tooling than REST.** No off-the-shelf GraphQL-to-warehouse connector is as mature as the corresponding REST tooling.

## Relationship to other API paradigms

Chapter 5 of Reis and Housley catalogues four HTTP-based API paradigms a data engineer should recognize (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **[[rpc|REST]]** — resource-oriented, stateless, dominant in public APIs.
- **GraphQL** — query-shaped, multi-model per request, introspectable schema.
- **[[rpc|gRPC]]** — HTTP/2 + Protobuf; efficient bidirectional exchange; common inside organizations.
- **[[webhooks]]** — reverse direction; source pushes to consumer.

Each carries different implications for ingestion code, schema evolution, and the [[data-contract]] between producer and consumer.

## Cross-book connections

- [[rpc]] — the DDIA treatment of REST, gRPC, and RPC frameworks generally. GraphQL sits in the same "HTTP-based API style" category.
- [[encoding-formats]] — GraphQL rides on JSON; the textual-schemaless format caveats from DDIA still apply.
- [[data-contract]] (Bellemare) — a GraphQL schema *is* a data contract in the Bellemare sense, with the same disciplines around evolution and triggering logic.

## Related pages

- [[rpc]]
- [[source-systems]]
- [[third-party-api-integration]]
- [[webhooks]]
- [[data-contract]]
- [[encoding-formats]]
