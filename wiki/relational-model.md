# Relational Model

**Summary**: The relational model organizes data into tables of rows and columns, hides storage implementation details behind a clean interface, and has dominated data storage for over 40 years — largely because its query optimizer generalizes well across wildly different use cases.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## History

Edgar Codd proposed the relational model in 1970. It was initially doubted — would it be efficient enough? By the mid-1980s, relational databases and SQL had become the default for anyone storing structured data.

Its roots are in mainframe business data processing: transaction processing (banking, airline reservations) and batch processing (payroll, invoicing). The key goal was to **hide internal storage details** behind a clean interface, freeing developers from thinking about physical data layout. (source: chapter-02-data-models-and-query-languages.md)

## Core concepts

- **Relation (table)** — an unordered collection of tuples (rows)
- **Tuple (row)** — a single record; values in each column
- **Normalization** — removing duplication by using IDs rather than repeated text; see [[normalization]]
- **Join** — combining rows from different tables at query time using a shared key
- **Foreign key** — a column in one table referencing the primary key of another

## The query optimizer insight

In the network model (CODASYL), developers had to manually specify access paths — which index to use, in what order to traverse records. The relational model moved this to an automatic **query optimizer**. The key insight: *you only need to build a query optimizer once, and every application benefits from it*. (source: chapter-02-data-models-and-query-languages.md)

This made adding new features far easier: declare a new index, and all existing queries can use it without modification.

## Strengths

- Excellent support for **many-to-many relationships** via joins
- **Normalization** keeps data consistent and avoids update anomalies
- **Schema-on-write** catches data errors early; see [[schema-on-read-vs-write]]
- Declarative query language (SQL) enables automatic optimization; see [[declarative-vs-imperative-queries]]
- General-purpose: has successfully expanded far beyond its original business data processing scope

## Weaknesses

- **[[object-relational-mismatch]]**: OOP code and relational tables don't map naturally
- Schema changes can be slow (MySQL copies the entire table on ALTER TABLE)
- Poor fit for tree-structured data where the whole tree is read at once — requires multiple joins or queries
- Less natural for highly interconnected data where [[graph-data-models]] excel

## Relationship to other models

The relational model defeated the hierarchical model (IMS) and network model (CODASYL) in the 1970s "great debate." It faces renewed competition from [[nosql]] stores and [[document-model]] databases, though the two are converging — most relational databases now support JSON natively. (source: chapter-02-data-models-and-query-languages.md)

## As a source system (Reis & Housley)

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* frames the RDBMS as the canonical [[source-systems|source system]] backing software applications (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **ACID + normalization + high transaction rate.** The combination makes relational databases "ideal for storing rapidly changing application states." Most OLTP application backends are RDBMS.
- **Challenge for the data engineer: capturing state over time.** The RDBMS will happily overwrite last year's customer address with this year's. The engineer has to decide how to preserve history — [[change-data-capture|CDC]], [[insert-only]] tables, point-in-time snapshots — at source-system design time, not after the fact.
- **Extraction primitives.** Modern relational databases expose several: full-table scan, incremental scan by primary key or `updated_at`, read replicas, log-based CDC on the binlog or WAL. See [[application-database-as-source]] for the extraction-pattern comparison.
- **Lineage of the LAMP stack.** The web era's RDBMS explosion (MySQL, PostgreSQL, MariaDB) produced the workload shape the engineer inherits — thousands of small OLTP databases each backing one application, expected to remain extractable without harm.

## Hard Parts ratings and positioning

Chapter 6 of *Software Architecture: The Hard Parts* rates relational databases on its eight-characteristic matrix. Headline scores (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — high.** SQL is ubiquitous, taught in schools, and thoroughly documented. Easier to onboard than any NoSQL family.
- **Data modelling — flexible.** Key-value, document, and graph-like shapes can all be expressed with some effort; what's hard is arbitrary-depth graph traversal.
- **Scalability — limited.** Vertical scaling by default; horizontal scaling via replicas and HA clusters is complex and coordination-heavy.
- **Availability / partition tolerance — moderate.** Relational DBs favour consistency over availability and partition tolerance (CA in CAP vocabulary — see [[cap-theorem]]).
- **Consistency — maximum.** Full ACID, the reason the family has dominated for four decades. The book credits ACID with letting application developers avoid reasoning about low-level concurrency details.
- **Community — largest.** Every major language has drivers; every tool speaks SQL; hiring is easiest here.
- **Read/write priority — balanced.** The same schema can be indexed for read efficiency or normalised for write efficiency; the same engine handles both.

**When the Hard Parts Chapter 6 framing says "not relational":** high-volume key-value-shaped reference data, tree-shaped documents where schemas vary per record, massive write-throughput time-series workloads, and graph-shaped relationship data. Each of these has a better-fit family in [[database-type-selection]]. The book's recurring caution: starting with a relational DB "under the impression it's a universal appliance" works until scale or flexibility demands force a rethink — [[polyglot-persistence]] is the escape hatch.

Popular implementations: MySQL, PostgreSQL, Oracle, Microsoft SQL Server. Also available as DBaaS on every major cloud.

## Related pages

- [[data-models]]
- [[normalization]]
- [[object-relational-mismatch]]
- [[schema-on-read-vs-write]]
- [[declarative-vs-imperative-queries]]
- [[document-model]]
- [[nosql]]
- [[source-systems]]
- [[application-database-as-source]]
- [[change-data-capture]]
- [[acid]]
- [[database-type-selection]]
- [[newsql-database]]
- [[polyglot-persistence]]
