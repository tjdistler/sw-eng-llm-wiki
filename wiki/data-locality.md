# Data Locality

**Summary**: Storage locality — keeping related data physically adjacent — speeds up reads that need the full record, but creates write overhead and wastes I/O when only part of the data is needed.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

---

## The concept

**Locality** refers to how closely related data is stored together. When data that is frequently read together is physically adjacent on disk (or in memory), reads are faster — fewer disk seeks, fewer I/O operations, better cache utilization.

In the [[document-model]], a document is stored as a single continuous byte string (JSON, XML, or a binary variant like BSON). Fetching the entire document — a common operation, e.g. rendering a user profile — requires one read. In the [[relational-model]], the same data split across multiple tables requires multiple index lookups and joins. (source: chapter-02-data-models-and-query-languages.md)

## The trade-off

The locality advantage is real but conditional:

**Locality helps when**: the application needs most or all of the document at once.

**Locality hurts when**:
- The application only needs a small part of a large document — the database still loads the entire document, wasting I/O
- The document is updated — the entire document typically needs to be rewritten, even for a small change; updates that increase a document's encoded size are especially costly

Practical implication: **keep documents small** and avoid writes that grow them. Large documents significantly erode the locality advantage. (source: chapter-02-data-models-and-query-languages.md)

## Locality is not unique to document databases

Several systems bring locality to other data models:

- **Google Spanner** — relational model, but allows schema declarations that interleave (nest) child table rows within parent rows
- **Oracle multi-table index cluster tables** — similar interleaving
- **Cassandra and HBase column families** — the Bigtable column-family concept groups related columns together for locality

Locality is a storage-layer concern that can be applied to multiple data models. (source: chapter-02-data-models-and-query-languages.md)

## Related pages

- [[document-model]]
- [[relational-model]]
- [[data-models]]
