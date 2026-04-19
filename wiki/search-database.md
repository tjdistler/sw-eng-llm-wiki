# Search Database

**Summary**: A non-relational database optimized for searching data by complex and approximate semantic or structural criteria. Search databases cover two distinct use cases — **text search** (find documents matching a query) and **log analysis** (find patterns in operational data) — and show up both as product-backing systems and as upstream sources for analytics.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The two primary use cases

Reis and Housley separate the workload by intent (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Text search.** Finding keywords or phrases in a body of text, supporting exact, fuzzy, or semantically similar matches. Archetypal examples: e-commerce product search, internal documentation search.
- **Log analysis.** Anomaly detection, real-time monitoring, security analytics, operational analytics. Data is ingested continuously; queries are investigative. This is the workload most [[log-aggregation|log-aggregation]] platforms serve.

Both workloads share a common implementation property: **indexes are the whole story**. Queries are optimized by building per-token, per-field, per-phrase indexes at ingest time, so read performance is fast at the cost of write amplification and index-rebuild latency.

## Common implementations

- **Elasticsearch** — the dominant open-source search database; also the centerpiece of the ELK/Elastic Stack for log analysis.
- **Apache Solr / Lucene** — the engine underneath Elasticsearch (Lucene) and its independent server distribution (Solr).
- **Algolia** — a hosted search product focused on product search with low-latency requirements.
- **OpenSearch** — a fork of Elasticsearch maintained by AWS.

## As a source system

Two patterns a data engineer sees with search databases:

- **Search DB as product-backing source.** An ecommerce site's product catalog is stored in Elasticsearch to power fuzzy search. Downstream analytics (KPI reports, sales dashboards) pull from the search DB as an upstream. Reis and Housley: "you might be expected to bring data from a search database (such as Elasticsearch, Apache Solr or Lucene, or Algolia) into downstream KPI reports or something similar" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).
- **Search DB as log-analysis platform.** Ops teams ingest logs into Elasticsearch; the data engineer may need to lift events from the index into the warehouse for longer-term analysis. Note that the ELK setup is typically a *destination* rather than a source, but the engineer is occasionally on the reverse side.

## Extraction considerations

- **Search-DB queries are not SQL.** You extract by writing search-DB-specific queries (Elasticsearch DSL, Solr query syntax). Off-the-shelf connectors help but often hit limits.
- **Full-scan extracts are expensive.** Search DBs are tuned for query latency, not for bulk export. Iterating the full dataset requires the search DB's scrolling API (Elasticsearch) and can impact cluster performance.
- **Index schema can drift.** Because documents are typed per field and per index, a mapping change on the source breaks downstream extraction schema just as sharply as a relational ALTER TABLE.

## Cross-book connections

- [[nosql]] — search is one of the NoSQL families Reis and Housley enumerate.
- [[log-aggregation]] — when the search DB is the destination for logs, understanding how logs land there (and can be extracted) is the upstream problem.
- [[indexes]] (DDIA) — the underlying technique: inverted indexes on text and field tokens.

## Related pages

- [[nosql]]
- [[log-aggregation]]
- [[log]]
- [[indexes]]
- [[source-systems]]
- [[analytics]]
