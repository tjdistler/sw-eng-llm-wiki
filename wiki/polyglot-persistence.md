# Polyglot Persistence

**Summary**: The practice of using **multiple database types within a single system**, each matched to the data domain it serves best. A term popularised by Sadalage and Fowler's *NoSQL Distilled*, and the natural endpoint of the [[database-decomposition]] pattern — once data is split into domains, each domain can move to its best-fit database type.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The term

Polyglot persistence is the data-tier analogue of **polyglot programming**: just as a system may use Java for one service, Python for another, and Go for a third, a polyglot-persistence system uses a relational database for one data domain, a document database for another, and a key-value store for a third (source: raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md).

A single application might use:

- A [[relational-model|relational database]] for transactional records
- A [[document-model|document store]] for user-generated content
- A [[graph-data-models|graph database]] for social connections
- A search index for full-text queries
- A [[key-value-store|key-value store]] for session state
- A [[time-series-database|time-series database]] for metrics

Each store is picked because it's the best fit for that data shape, not because it's "the company database."

## Why it became feasible

The [[nosql]] movement (late 2000s) produced specialised database types that were each better than a general-purpose RDBMS at specific workloads. Simultaneously, the [[microservices]] architecture style broke applications into small services that owned their own data — making it natural for each service to pick its own store (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

Before per-service databases, the cost of operating multiple database types fell on a central DB team, who reasonably pushed back on "one more technology to support." Once the service team owns its data, the team can own the database type too.

## The Hard Parts framing

*Software Architecture: The Hard Parts* Chapter 6 names **database type optimisation** as one of the six [[data-decomposition-drivers-and-integrators|data disintegrators]] (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md). When a monolithic relational database stores application state, reference data, graph-shaped relationships, and time-series events all in the same tables, the relational model serves every use case mediocrely. Splitting the database enables moving each category to its best-fit family — see [[database-type-selection]] for the eight-family comparison.

The Sysops Squad worked example in the chapter picks a document store for the **Survey** domain (nested schema, read-mostly, flexible question shapes) while keeping Ticketing on a relational store. That's polyglot persistence in action.

## Trade-offs

Polyglot persistence is not free:

- **Operational surface area.** Every database type is another monitoring integration, another backup procedure, another set of client libraries, another on-call rotation.
- **Team skills.** Hiring a DBA who knows Cassandra *and* PostgreSQL *and* Neo4j is harder than hiring one who knows just PostgreSQL.
- **Cross-domain analytics.** Reports that need data from multiple domains can no longer use a single SQL query — they need an ETL pipeline or an analytical store.
- **Distributed transactions.** ACID across stores isn't possible the way it is within one store — see [[saga]] for the distributed-transaction alternative.

The decision to go polyglot is the same shape as the [[data-decomposition-drivers-and-integrators|decomposition decision]]: enumerate the benefits on the disintegrator side, enumerate the costs on the integrator side, and pick the least-worst combination for the specific system.

## Related pages

- [[database-decomposition]]
- [[database-type-selection]]
- [[data-domain]]
- [[nosql]]
- [[relational-model]]
- [[document-model]]
- [[key-value-store]]
- [[graph-data-models]]
- [[wide-column-database]]
- [[time-series-database]]
- [[data-sovereignty]]
- [[microservices]]
- [[software-architecture-the-hard-parts]]
