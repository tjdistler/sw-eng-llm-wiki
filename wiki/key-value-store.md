# Key-Value Store

**Summary**: A [[nosql]] database that retrieves records by a single key, functioning as a large-scale, persistent hash map. Key-value stores are the simplest of the NoSQL families — they trade join support, secondary indexing, and query expressiveness for operational simplicity and extreme scale.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The shape

A key-value database "retrieves records using a key that uniquely identifies each record. This is similar to hash map or dictionary data structures presented in many programming languages but potentially more scalable" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

Two broad deployment shapes:

- **In-memory.** Redis, Memcached. Extremely fast; storage is typically temporary — "if the database shuts down, the data disappears." Popular for caching session data and for web/mobile applications needing "ultra-fast lookup and high concurrency" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).
- **Persistent, disk-backed.** DynamoDB, FoundationDB, Riak, Aerospike. Durable across restarts, replicated across nodes, suitable for application state that must survive.

Reis and Housley's canonical example of a persistent KV use case: an ecommerce application where every user click, cart change, and checkout must be durably stored and retrievable (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## As an umbrella

"Key-value stores encompass several NoSQL database types — for example, document stores and wide column databases" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). In that sense [[document-model|document databases]] and [[wide-column-database|wide-column databases]] are specialised descendants of the KV pattern with extra structure on the value side.

## Source-system implications

For a data engineer pulling from a key-value store as a source:

- **No query engine.** There are no joins, no secondary indexes by default. Extraction typically means scanning the full key space or tailing a [[change-data-capture|change-data stream]].
- **Change streams are often first-class.** DynamoDB Streams, Redis Pub/Sub, Aerospike XDR — these change-data interfaces are the recommended extraction path.
- **Consistency varies.** In-memory caches are often eventually consistent or best-effort; durable KV stores may offer strong consistency per-key (DynamoDB) or eventual consistency across replicas (Riak, Cassandra's KV shape).
- **Hot keys are dangerous.** A key-value store partitions by key, so a disproportionately-accessed key creates a hotspot. Both the application and the extractor must avoid hammering a single key.

## Cross-book connections

- [[hash-indexes]] (DDIA) — the in-memory-hash implementation strategy underlies many KV stores.
- [[bigtable]] (SRE book / DDIA) — Google Bigtable is the archetypal wide-column KV descendant.
- [[distributed-locks-on-kv-stores]] — KV stores are a common substrate for distributed locking.
- [[document-model]] / [[wide-column-database]] — the two structured variants on the value side.

## Hard Parts ratings and positioning

Chapter 6 of *Software Architecture: The Hard Parts* rates key-value stores on its eight-characteristic matrix (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — easy.** Simple `get`, `put`, `delete` API. The hard part is *aggregate design* — because values are opaque, any change to the shape of the value means rewriting every stored value. Moving from a relational mindset to a KV mindset takes unlearning: you can't say "give me all the keys."
- **Data modelling — aggregate-oriented.** Values are memory structures (arrays, maps, blobs). Queries are by key only, so the **key design dominates**. Good keys: `session_id`, `user_id`, `order_id` — things the client already has.
- **Scalability — very high.** Key-based indexing means no joins, no `ORDER BY`, no cross-record queries. Lookups are O(1) and horizontally-shardable.
- **Availability / partition tolerance — tunable.** Riak and similar stores offer per-operation quorum levels (`all`, `one`, `quorum`, `default`) — treat KV stores as configurable per-operation, not as a single personality.
- **Consistency — tunable.** Quorum-based. Higher consistency costs latency (more nodes must acknowledge). Majority quorum is the common trade-off.
- **Community — good.** Many open source options; most expose HTTP REST APIs, which eases integration.
- **Read/write priority — read-biased.** Geared toward fast get-by-key; session stores, caches, user-preferences caches are canonical fits.

### Positioning in Hard Parts' decomposition recipe

The [[database-decomposition]] chapter names key-value stores specifically as the better home for **reference data** (country codes, product codes, warehouse codes) that has no real relational structure and only ever gets queried by key. Extracting such tables from a monolithic RDBMS into a KV store is a canonical [[polyglot-persistence]] move (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

## Related pages

- [[nosql]]
- [[document-model]]
- [[wide-column-database]]
- [[hash-indexes]]
- [[bigtable]]
- [[source-systems]]
- [[change-data-capture]]
- [[database-type-selection]]
- [[polyglot-persistence]]
