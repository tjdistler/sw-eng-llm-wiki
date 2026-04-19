# NoSQL

**Summary**: NoSQL is an umbrella term for non-relational databases that emerged in the 2010s, driven by scalability needs and developer frustration with relational schemas — not a single technology but a set of trade-offs that complement, rather than replace, the relational model.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## Origin

"NoSQL" started as a Twitter hashtag for a 2009 meetup on open source, distributed, non-relational databases. It was never a formal name for a technology — it was retroactively reinterpreted as "Not Only SQL." The name stuck despite being imprecise. (source: chapter-02-data-models-and-query-languages.md)

## Driving forces

Four main reasons drove NoSQL adoption:

1. **Scalability** — need for larger datasets or higher write throughput than relational databases easily support
2. **Open source preference** — avoiding commercial database licensing costs
3. **Specialized queries** — operations not well-served by the relational model
4. **Schema flexibility** — frustration with rigid relational schemas and desire for more dynamic data models

## Two main directions

NoSQL datastores diverged into two families:

- **[[document-model]] databases** (MongoDB, CouchDB, RethinkDB) — target use cases where data is self-contained and relationships between records are rare
- **[[graph-data-models]] databases** (Neo4j, Datomic) — target use cases where everything is potentially related to everything else

The relational model sits in the middle, handling many-to-many relationships that neither extreme handles as naturally.

## Polyglot persistence

The practical conclusion of the NoSQL movement: different data stores for different use cases within the same system. A single application might use:
- A relational database for transactional records
- A document store for user-generated content
- A graph database for social connections
- A search index for full-text queries

This is called **polyglot persistence** — picking the right tool for each problem rather than forcing everything into one model. (source: chapter-02-data-models-and-query-languages.md)

## What NoSQL didn't replace

Relational databases have proved remarkably general-purpose. Much of the web runs on relational stores (publishing, social networking, e-commerce, SaaS). The prediction that NoSQL would displace SQL has not materialized; instead, both approaches coexist, and the two are converging — relational databases now support JSON natively, and document databases have added joins and aggregation pipelines. (source: chapter-02-data-models-and-query-languages.md)

## The six NoSQL families (Reis & Housley)

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* organizes NoSQL into six families a data engineer will regularly encounter as source systems (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

| Family | Page | Typical use |
|---|---|---|
| Key-value | [[key-value-store]] | Caches, session stores, high-volume persistent KV (DynamoDB) |
| Document | [[document-model]] | Application backends with self-contained nested records |
| Wide-column | [[wide-column-database]] | Massive scale, sub-10ms lookups, single-index (Bigtable, Cassandra) |
| Graph | [[graph-data-models]] | Relationship-heavy data; social, knowledge graphs |
| Search | [[search-database]] | Text search, log analysis (Elasticsearch, Solr) |
| Time-series | [[time-series-database]] | IoT, metrics, time-indexed workloads |

Reis and Housley stress that each family "abandons various RDBMS characteristics, such as strong consistency, joins, or a fixed schema" in exchange for specific scale or flexibility benefits. "Data innovation is constant" — new shapes will keep emerging, and the data engineer must be able to evaluate a new NoSQL family against the same considerations framework used for existing ones (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

The typical operational advice for all six: many lack full ACID and rich query features, so **analytics workloads cannot run directly against them at scale**. Extraction is either a full scan (slow, expensive, potentially disruptive) or a [[change-data-capture|CDC]]-style event stream (preferred when available).

The relational-store-as-default instinct still dies hard. Reis and Housley: "we often see that people start with a relational database under the impression it's a universal appliance and shoehorn in a ton of use cases and workloads. As data and query requirements morph, the relational database collapses under its weight. At that point, you'll want to use a database that's appropriate for the specific workload under pressure" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Related pages

- [[data-models]]
- [[document-model]]
- [[graph-data-models]]
- [[relational-model]]
- [[schema-on-read-vs-write]]
- [[key-value-store]]
- [[wide-column-database]]
- [[search-database]]
- [[time-series-database]]
- [[source-systems]]
