# Data Models

**Summary**: Data models are layered abstractions that shape not just how software is written but how engineers think about problems — choosing the wrong model has cascading consequences throughout the stack.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

---

## The layering abstraction

Every application is built by stacking data models on top of each other. Each layer hides the complexity of the one below it:

1. **Application layer** — real-world entities (people, orders, events) modeled as objects or data structures
2. **General-purpose data model** — those objects expressed as JSON documents, relational tables, or graph nodes/edges
3. **Storage layer** — the database's internal representation as bytes in memory or on disk
4. **Hardware layer** — bytes as electrical currents, magnetic fields, pulses of light

Each layer provides a clean interface so that different teams — application developers and database engineers, for example — can work together without needing to understand each other's internals. (source: chapter-02-data-models-and-query-languages.md)

## Why the choice matters

The data model shapes what operations are easy, which are possible at all, and which are prohibitively slow. A model that fits your application's relationship patterns makes code simple; a mismatch creates accidental complexity that compounds over time. (source: chapter-02-data-models-and-query-languages.md)

The three dominant general-purpose models each suit a different class of problem:

| Model | Optimized for | Key concept |
|---|---|---|
| [[relational-model]] | Many-to-many relationships, structured data | Tables, joins, normalization |
| [[document-model]] | Self-contained tree-structured documents | Locality, schema flexibility |
| [[graph-data-models]] | Highly interconnected data | Vertices, edges, traversal |

These models are not mutually exclusive — [[polyglot-persistence]] describes using several together in one system.

## Convergence

Relational and document databases are converging. PostgreSQL, MySQL, and DB2 now support native JSON. RethinkDB and later MongoDB added join-like operations. A hybrid model — relational storage with document flexibility — may be the long-term direction. (source: chapter-02-data-models-and-query-languages.md)

## Related pages

- [[relational-model]]
- [[document-model]]
- [[graph-data-models]]
- [[nosql]]
- [[object-relational-mismatch]]
- [[schema-on-read-vs-write]]
- [[declarative-vs-imperative-queries]]
- [[polyglot-persistence]]
