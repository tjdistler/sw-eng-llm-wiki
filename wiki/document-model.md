# Document Model

**Summary**: Document databases store self-contained records (typically JSON) that map naturally to application objects and load efficiently as a unit — at the cost of weak support for joins and many-to-many relationships.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[data-models]]
- [[relational-model]]
- [[schema-on-read-vs-write]]
- [[data-locality]]
- [[object-relational-mismatch]]
- [[normalization]]
- [[nosql]]
