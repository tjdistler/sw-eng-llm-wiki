# Normalization

**Summary**: Normalization removes duplication by storing human-meaningful information once and referencing it by ID everywhere else — keeping data consistent and reducing update anomalies, at the cost of requiring joins.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

---

## The core idea

When the same piece of information appears in multiple places, updating it requires changing every copy. If any copy is missed, the data becomes inconsistent. **Normalization** solves this by storing each fact exactly once and referencing it by ID.

A simple example: instead of storing the string "Greater Seattle Area" in every user record, store a `region_id` that points to a single regions table. When the region name changes, only one row needs updating. (source: chapter-02-data-models-and-query-languages.md)

## Why IDs rather than text?

IDs have no intrinsic meaning to humans — they never need to change even if the underlying information does. Human-meaningful text *does* change (city names, company names, job titles), so duplicating it creates ongoing maintenance burden and inconsistency risk.

The trade-off: IDs require a join to resolve to human-readable values. (source: chapter-02-data-models-and-query-languages.md)

## Benefits of normalized data

- **Consistency** — one update changes the value everywhere
- **No ambiguity** — standardized lists prevent variant spellings or naming
- **Localization** — a single lookup table can be translated once
- **Better search** — structured relationships enable richer queries (e.g., find users in Washington state via a region hierarchy, not just string matching)

## Normalization vs the document model

Normalization depends on joins. The [[document-model]] has weak join support, which means either:

1. **Denormalize** — duplicate data, accepting update overhead and inconsistency risk
2. **Emulate joins in application code** — make multiple database requests and merge results in memory (slower; moves complexity into the application)

This tension is a fundamental limitation of document databases for applications with many-to-many relationships. (source: chapter-02-data-models-and-query-languages.md)

## Denormalization trade-offs

Denormalization (deliberately duplicating data for read performance) is sometimes the right call — particularly for read-heavy workloads where update consistency is manageable. But it requires the application to maintain consistency across duplicated copies. See also the broader discussion in the book's Part III on caching and derived data.

## Related pages

- [[relational-model]]
- [[document-model]]
- [[data-models]]
