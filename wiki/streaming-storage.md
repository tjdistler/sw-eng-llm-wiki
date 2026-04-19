# Streaming Storage

**Summary**: The storage-layer view of distributed streaming systems. Classic message queues treated stored data as **temporary** — delete after consumption. Modern streaming frameworks like **Apache Kafka**, **Apache Pulsar**, **Amazon Kinesis**, and **Google Cloud Pub/Sub** treat the log as **durable storage** with long retention, tiered storage, and [[log-based-message-brokers|replay]] as the primary retrieval mechanism. The line between "streaming system" and "storage system" has collapsed.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Two storage regimes for streams

Chapter 6 draws a clear split (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Message queues (classic).** Data is transient. A message lives until all consumers acknowledge it; then it is deleted. Retention is measured in minutes or hours. RabbitMQ, ActiveMQ, classical JMS.
- **Distributed scalable streaming (modern).** Data is durable. Retention is measured in days, weeks, or indefinitely. Old messages are pushed to cheap tiers rather than deleted. Kafka, Pulsar, Kinesis, Pub/Sub.

The modern regime blurs the streaming/storage boundary. A Kafka topic with indefinite retention *is* a database — specifically, a distributed, partitioned, append-only log of events that can be queried by [[log-based-message-brokers|replay from any offset]].

## Indefinite retention and tiered storage

Chapter 6 specifically calls out **tiered storage** as the mechanism that makes indefinite retention economical (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md): "Kafka supports indefinite data retention by pushing old, infrequently accessed messages down to object storage."

The architecture is straightforward:

- **Hot tier.** Recent data on local SSDs attached to broker nodes. Low-latency access for live consumers.
- **Cold tier.** Older data offloaded to [[object-storage|object storage]] (S3, GCS). Higher latency but near-zero storage cost.

Consumers are oblivious to the split: the broker fetches from whichever tier holds the requested offset. The same pattern applies to Kinesis (long-term retention), Pulsar (via BookKeeper and tiered storage), and Pub/Sub.

This is the same economic logic as [[data-temperature|hot/warm/cold]] applied inside a streaming system: most reads hit recent data; old data is cheap insurance.

## Replay as the retrieval primitive

"Replay is the standard data-retrieval mechanism for streaming storage systems" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Two major uses:

- **Reprocessing in a streaming pipeline.** A bug is found in a transformation; redeploy the fixed code and replay from an earlier offset to regenerate downstream state.
- **Batch queries over a time range.** Run analytical queries over historical windows by scanning the retained log.

[[log-based-message-brokers]] covers the mechanism in depth: reading is a read-only operation, consumer offsets are under the consumer's control, a new consumer can start from any offset. This is what gives streaming-as-storage the same "experiment safely, reprocess freely" property that makes [[batch-processing]] tractable.

## Streaming-native query engines

Chapter 6 mentions the emergence of query engines over streams — "streaming buffers" that expose the live stream as a queryable table (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **ksqlDB** — SQL queries over Kafka topics; supports windowing and stream-table joins.
- **BigQuery streaming buffer** — rows ingested via the streaming API land in a short-term buffer that is transparently queryable alongside object-storage-backed columnar data. The buffer eventually reserialises into columnar format.

These collapse the classical split between "data in motion" (stream) and "data at rest" (warehouse) into a single query surface. See [[stream-to-batch-storage]] for the broader architectural pattern.

## Trade-offs vs. other storage

| Aspect | Streaming storage | [[data-warehousing|Warehouse]] | [[object-storage]] |
|---|---|---|---|
| Write shape | Append-only events | Bulk batches or inserts | Whole-object writes |
| Ordering | Per-partition total order | None | None |
| Retention | Days to indefinite with tiering | Years | Indefinite |
| Read pattern | Offset-based replay + tail | SQL scan/aggregate | Key lookup + range |
| Cost profile | Higher per-byte than object storage; lower than warehouse for raw | Highest | Lowest |
| Update model | Log compaction (per-key latest); [[tombstone|tombstones]] | UPDATE/DELETE | Rewrite whole object |

Streaming storage is uniquely good at **event-shaped workloads** — CDC streams, telemetry, user actions — where the access pattern is "tail the latest" plus "occasionally reprocess history." It is a poor fit for "aggregate 5 years of sales by region" queries; dump those to a warehouse or object store via the [[stream-to-batch-storage|stream-to-batch]] pattern.

## Cross-book connections

- [[log-based-message-brokers]] (DDIA, Bellemare) — the fuller treatment of Kafka-style brokers, including partitioning, consumer offsets, and log compaction.
- [[event-streams]] — FoDE Ch 5's source-systems framing of streams.
- [[event-sourcing]] — the architectural pattern that leans hardest on streaming storage as the source of truth.
- [[change-data-capture]] — streams as database-replication substrate.

## Related pages

- [[log-based-message-brokers]]
- [[event-streams]]
- [[object-storage]]
- [[data-temperature]]
- [[stream-to-batch-storage]]
- [[event-sourcing]]
- [[change-data-capture]]
- [[stream-processing]]
- [[kappa-architecture]]
- [[lambda-architecture]]
- [[data-storage-stage]]
