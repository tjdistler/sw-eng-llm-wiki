# Database Type Selection

**Summary**: Once a monolithic database is broken into [[data-domain|data domains]], each domain can be re-hosted on the database type best suited to its workload — [[polyglot-persistence]]. Ford, Richards, and Sadalage's Chapter 6 surveys eight families (relational, key-value, document, column-family, graph, NewSQL, cloud-native, time-series) and rates each on an eight-axis star-rating matrix. This page is the summary of the matrix.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## Why this is a whole chapter

The Paradox of Choice. Beginning around 2005, a revolution in database technology produced dozens of products, each optimised for a different set of trade-offs. The architect's job isn't to memorise every database — it's to match the **workload shape** of a data domain to the **family** whose trade-offs fit best (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

The book proposes eight characteristics for evaluating any database family.

## The eight characteristics

| Characteristic | Question it answers |
|---|---|
| **Ease of learning curve** | How hard is it for a developer/DBA/modeller to pick up? |
| **Ease of data modelling** | Does the modelling approach match many use cases, and is it easy to change later? |
| **Scalability / throughput** | Can it scale horizontally or vertically? How easily? |
| **Availability / partition tolerance** | Does it support HA configs, network-partition tolerance, tunable quorums? |
| **Consistency** | ACID vs BASE vs tunable-consistency; support for "always consistent" writes. |
| **Language support, maturity, SQL, community** | How many programming languages, how mature the product, how many developers know it? |
| **Read/write priority** | Does the engine favour reads, writes, or balance them? |

Higher star rating = more of that quality. The book's whole framing: **no database gets five stars on everything** — every database trades something for something else, and the architect picks the database that trades things they can afford to lose (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

## The eight families at a glance

Summarising the chapter's per-family ratings into a single comparison table. Ratings are on a 1–5 scale per the book's figures.

| Family | Learning | Modelling | Scale | Availability | Consistency | Community | R/W |
|---|---|---|---|---|---|---|---|
| [[relational-model\|Relational]] | 5 | 4 | 3 | 3 | 5 (ACID) | 5 | balanced |
| [[key-value-store\|Key-value]] | 4 | 4 | 5 | 5 (tunable) | 3 (tunable) | 4 | read-biased |
| [[document-model\|Document]] | 4 | 4 | 4 | 4 | 3 (some ACID) | 5 | read-biased |
| [[wide-column-database\|Column family]] | 2 | 2 | 5 | 5 | 3 (tunable) | 4 | write-biased |
| [[graph-data-models\|Graph]] | 2 | 2 | 3 | 3 | 4 (ACID some) | 4 | read-biased |
| [[newsql-database\|NewSQL]] | 4 | 4 | 5 | 5 | 5 (ACID) | 3 | balanced |
| [[cloud-native-database\|Cloud-native]] | varies | varies | 5 | 5 | varies | 2–3 | varies |
| [[time-series-database\|Time-series]] | 4 | 3 | 4 | 4 | tunable | 3 | read-biased |

(Exact figure values are from the chapter's per-family rating charts — Figures 6-25 through 6-33.)

## Family-by-family notes

### Relational

The default for 40+ years. Strong on ACID, SQL ubiquity, developer familiarity, and read/write flexibility (the same DB can be tuned for either). Weak on horizontal scaling — vertical-first, and replication setup is complex. MySQL, PostgreSQL, Oracle, SQL Server. See [[relational-model]].

### Key-value

Values are opaque blobs; only the key is queryable. Extreme scale, tunable consistency (quorum-based), aggregate-oriented. Reference data, session storage, user preferences are canonical fits. DynamoDB, Riak, Redis, Memcached, Aerospike. See [[key-value-store]].

### Document

Key-value where the value is a queryable, indexable JSON/XML document. Developer-friendly (aggregates map to domain objects), reasonably scalable, tunable consistency. MongoDB, CouchDB, Couchbase. See [[document-model]].

### Column family (wide-column)

Rows with varying columns, clustered by row key. **Extreme write throughput** and horizontal scale. Steep learning curve — row-key design dominates performance. Cassandra, Scylla, HBase, Bigtable. CQL has made the SQL surface more approachable. See [[wide-column-database]].

### Graph

Vertices, edges, properties; relationships are first-class objects. Great for traversal-heavy queries, steep learning curve for modelling (nodes vs relations vs properties). Scaling writes is constrained — graphs don't shard easily. Neo4j, Neptune, JanusGraph, TigerGraph. See [[graph-data-models]].

### NewSQL

Relational + ACID + SQL, with horizontal scaling built in. The "have-your-cake-and-eat-it" family. Multiple active nodes (vs relational's single leader + followers), ACID transactions, geographic distribution. CockroachDB, VoltDB, Spanner, YugabyteDB. See [[newsql-database]].

### Cloud-native

Cloud-only databases with DBaaS operational models. Some (Redshift, Snowflake, Cosmos DB) are warehouse-like; others (Datomic) use totally different paradigms (immutable atomic facts, EAVT indexing). Scaling is easy (just pay more); community depth varies by product. See [[cloud-native-database]].

### Time-series

Append-only, timestamp-tagged, no updates. Write-heavy, optimised for range scans by time. IoT, metrics, observability. InfluxDB, TimescaleDB, kdb+. See [[time-series-database]].

## Aggregate orientation

A concept that cross-cuts most NoSQL families: the **aggregate** is a chunk of related data that is stored, queried, and transferred as a unit (Evans's DDD term). Key-value, document, and column-family databases are all **aggregate-oriented** — they store whole trees of data co-located, which:

- Enables easy distribution across a cluster (copy the aggregate to another node).
- Improves read and write performance (fewer joins).
- Reduces impedance mismatch between application objects and storage.
- Makes it difficult to analyse *across* aggregates (no cheap cross-aggregate joins).
- Makes aggregate-boundary changes expensive (rewriting data).

(source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md)

The Sysops Squad survey example in the chapter shows the **single aggregate vs multiple aggregates with references** trade-off for a document store. Embedding the survey's questions inside the survey document is fast to read and easy to copy, but makes question-centric queries awkward. Splitting the survey and questions into separate documents with references enables per-question queries at the cost of client-side join logic. Neither is wrong; the workload picks the winner.

## Selecting for a data domain

The book's practical recipe (derivable from the chapter):

1. **Describe the workload.** Reads vs writes, query shape, scale envelope, consistency needs, relationship density.
2. **Identify which of the eight characteristics are hard constraints.** e.g., "must be strongly consistent", "must handle 1M writes/s", "must have 24/7 availability under partition".
3. **Eliminate families that fail the hard constraints.** A read-heavy reporting domain with <1k writes/s eliminates column-family; a ACID-required financial ledger eliminates key-value with eventual consistency.
4. **Score remaining families on the soft criteria.** Developer familiarity, community size, product maturity, cost.
5. **Pilot before committing.** The book's recurring warning — "picking a new database is a team skills investment, not just a technical choice."

## Polyglot persistence

The payoff of [[database-decomposition]]: different data domains can live on different database types. The Sysops Squad's Survey domain (flexible schema, nested structure, read-mostly) becomes a document store; the Ticketing domain (transactional, relational) stays on an RDBMS; reference data (country codes, product codes) moves to a key-value store. See [[polyglot-persistence]].

## Related pages

- [[database-decomposition]]
- [[data-domain]]
- [[data-decomposition-drivers-and-integrators]]
- [[polyglot-persistence]]
- [[relational-model]]
- [[key-value-store]]
- [[document-model]]
- [[wide-column-database]]
- [[graph-data-models]]
- [[newsql-database]]
- [[cloud-native-database]]
- [[time-series-database]]
- [[nosql]]
- [[acid]]
- [[cap-theorem]]
- [[software-architecture-the-hard-parts]]
