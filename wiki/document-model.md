# Document Model

**Summary**: Document databases store self-contained records (typically JSON) that map naturally to application objects and load efficiently as a unit — at the cost of weak support for joins and many-to-many relationships.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## Core idea

A document is a self-contained unit of data — typically JSON or XML — that encodes a tree of one-to-many relationships in a single record. Examples: MongoDB, RethinkDB, CouchDB, Espresso.

A résumé is the canonical example: one person has many positions, many education entries, and many contact details. In the [[relational-model]], these require separate tables and joins. In the document model, they nest naturally inside one JSON object. (source: chapter-02-data-models-and-query-languages.md)

## Strengths

### Schema flexibility
Document databases don't enforce a schema on write. New fields can be added to new documents immediately without a migration. Old documents with missing fields are handled in application code at read time. See [[schema-on-read-vs-write]].

This is particularly valuable when:
- Items in the collection don't all have the same structure
- Data shape is controlled by external systems that can change without warning

### Data locality
A document is usually stored as a single continuous byte string. Loading it requires one read, not multiple index lookups across tables. When the application needs most or all of the document at once — rendering a profile page, for example — this is a meaningful performance advantage. See [[data-locality]].

### Simpler code for tree-structured data
When the data naturally forms a tree (one-to-many throughout), the document model matches the application's data structures directly, avoiding the [[object-relational-mismatch]].

## Weaknesses

### Poor support for joins
Document databases were designed for data that doesn't need to reference other documents. When many-to-many relationships appear, joins must be emulated in application code via multiple queries — slower, and more complex. (source: chapter-02-data-models-and-query-languages.md)

### Nested references are awkward
You cannot refer directly to a nested item within a document; you must navigate by path ("the second item in positions for user 251"). This echoes the access-path navigation of the old hierarchical model (IMS).

### Data grows interconnected over time
Applications that start with clean tree-structured data tend to accumulate relationships as features are added. An initial fit with the document model can degrade as the application evolves.

## The hierarchical model parallel

The document model is a modern revival of IBM's IMS (1968), which stored data as nested trees. IMS had the same strengths and the same weakness: great for one-to-many, poor for many-to-many. The 1970s "great debate" between the hierarchical/network models and the relational model was triggered by exactly this limitation. Document databases are relitigating it. (source: chapter-02-data-models-and-query-languages.md)

## When to use document vs relational

| Condition | Preferred model |
|---|---|
| Data is tree-structured, loaded as a whole | Document |
| Many-to-many relationships are central | Relational |
| Highly interconnected, graph-like data | [[graph-data-models]] |
| Schema varies across records | Document |
| Data consistency and join integrity matter | Relational |

The right choice depends on the *relationship patterns* in your data, not just preference. (source: chapter-02-data-models-and-query-languages.md)

## Convergence with relational

RethinkDB supports relational-like joins. MongoDB added an aggregation pipeline for declarative queries. PostgreSQL, MySQL, and DB2 support native JSON storage and querying. The models are merging. (source: chapter-02-data-models-and-query-languages.md)

## As a source system (Reis & Housley)

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* adds a data-engineer-shaped caveat to the DDIA strengths above. From the **source-system** perspective (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Collections map to tables.** Terminology bridge — a collection in a document database is roughly a table; a document is roughly a row.
- **Usually not ACID.** Unlike relational databases, document stores are "generally not ACID compliant." Many are eventually consistent; writes to different documents in different partitions may not be durable under the same semantics a relational app developer expects. The engineer "needs technical expertise in a particular document store" to reason about tuning, writes, consistency, and durability — one store's behaviour is not another's.
- **Schema flexibility is a double-edged sword.** A flexible schema lets the app evolve quickly, but "we've seen document databases become absolute nightmares to manage and query." If schema evolution is not communicated before deployment, pipelines silently break.
- **Analytics extraction is expensive.** To run analytics on a document store, engineers "generally must run a full scan to extract all data from a collection or employ a [[change-data-capture|CDC]] strategy to send events to a target stream." Full scans slow the source and, for many serverless cloud document stores, "charge a significant fee for each full scan." Indexes help, but only for lookup, not for bulk extraction.
- **Joins are not native.** "Data cannot be easily normalized... Applications can still join manually. Code can look up a document, extract a property, and then retrieve another document." The engineer extracting from a document source must either denormalize in the pipeline or accept slow programmatic joins.

## Hard Parts ratings and positioning

Chapter 6 of *Software Architecture: The Hard Parts* rates document databases on its eight-characteristic matrix (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — easy.** Documents are human-readable; enterprises already deal with JSON/XML as API payloads and frontend data.
- **Data modelling — aggregate-oriented, forgiving.** Model orders, tickets, or other domain objects as aggregates. Document databases are *more* forgiving than key-value stores because parts of the aggregate are queryable and indexable.
- **Scalability — good.** Aggregate-oriented design distributes naturally; complex indexing reduces scalability; past a certain data size, sharding becomes necessary and the sharding-key choice becomes architectural.
- **Availability / partition tolerance — good.** Configurable; replicated clusters for sharded collections are complex to operate, though cloud providers are smoothing this.
- **Consistency — tunable.** Some stores now support ACID **within a single collection**, though edge cases persist. Quorum-based tunable consistency lets each read or write pick its own trade-off.
- **Community — largest of the NoSQL families.** MongoDB leads; active user community, many tutorials, many language drivers.
- **Read/write priority — read-biased.** Aggregate orientation plus secondary indexes make document stores favour read workloads.

### Document-store design for the Sysops Squad survey

The chapter's worked example for polyglot-persistence migration is the Sysops Squad's **Survey** data domain moving from relational to a document store (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md). The key modelling choice is whether to use a **single aggregate with embedded questions** or **separate aggregates with references**:

- **Embedded questions.** One read gets the whole survey + its questions. Fast, simple, ideal when the survey is always consumed as a unit. Cost: question-centric queries are awkward; changing questions requires rewriting the survey document.
- **Referenced questions.** Survey and Question are separate aggregates; the survey holds question IDs. Per-question queries are easy; client-side joins are required when the full survey is needed.

Neither is wrong; the workload picks the winner. This is the aggregate-design trade-off the book flags for all aggregate-oriented NoSQL families.

## Related pages

- [[data-models]]
- [[relational-model]]
- [[schema-on-read-vs-write]]
- [[data-locality]]
- [[object-relational-mismatch]]
- [[normalization]]
- [[nosql]]
- [[source-systems]]
- [[change-data-capture]]
- [[database-type-selection]]
- [[polyglot-persistence]]
