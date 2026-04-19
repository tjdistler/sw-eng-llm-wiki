# Stream-to-Batch Storage

**Summary**: A pattern where a **streaming topic fans out to multiple consumers**, one of which writes the stream to durable batch storage for long-term retention and analytical queries. The streaming system handles live event flow; the batch storage handles historical queries. Architecturally close to the [[lambda-architecture]] but often less explicit about the "speed vs batch" split — in modern cloud warehouses the split is nearly invisible.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The shape

Chapter 6 describes a simple topology (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

```
                  ┌──► real-time consumer (dashboards, alerts)
topic ──► fan-out ┤
                  └──► batch-storage writer (object storage / warehouse)
```

Every event in the topic goes both places. Real-time consumers compute live statistics over the stream; the batch-storage writer accumulates events into durable columnar files for retrospective analysis.

Chapter 6's canonical examples:

- **AWS Kinesis Firehose.** Reads from a Kinesis stream, batches events by time-window or size, writes Parquet/JSON/CSV files to S3 on configurable triggers.
- **BigQuery streaming buffer.** Rows ingested via the streaming API land in a short-term in-memory buffer. The query engine seamlessly unions the buffer with the table's columnar object-storage backing. The buffer is **automatically reserialised to columnar object storage** in the background.

The BigQuery example collapses the "stream storage" and "batch storage" distinction into something a user cannot tell apart: a query over `today's data` scans the streaming buffer and any already-flushed files in one pass.

## Relationship to Lambda

Chapter 6: "The stream-to-batch storage architecture has many similarities to the Lambda architecture, though some might quibble over the technical details" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

[[lambda-architecture|Lambda]] is the older, more explicit framing: a **batch layer** stores the immutable full history, a **speed layer** computes approximate real-time views, and a **serving layer** merges them. Stream-to-batch storage is a less opinionated realisation of the same basic idea: fan out to both a real-time path and a batch path.

Where Lambda required two full processing pipelines (one batch, one streaming), modern stream-to-batch can be as simple as a single stream + a Firehose-style sink. The real-time "computation" may be a single consumer writing summaries; the batch side is a query engine reading the object-storage files.

[[kappa-architecture]] is the other alternative: do everything as streaming, scrap the batch layer, rely on replay for historical queries. Kappa is elegant but places heavy demands on the streaming engine for long-running retrospective computations.

## Why the pattern persists

Stream-to-batch storage persists because the **access patterns are genuinely different** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Live consumers** need sub-second access to recent events. Stream-native storage (Kafka, Kinesis) excels here.
- **Analytical queries** need to aggregate billions of rows across years. Columnar object storage with warehouse or lakehouse query engines excels here.

Attempting a single storage system for both hurts both. Attempting two entirely separate systems (without a shared source) risks inconsistency between the real-time and historical views. Stream-to-batch, where the same event feed drives both, guarantees the historical store is a faithful copy of the streaming source.

## Tradeoffs

- **Ingestion latency vs. cost.** Firehose with a 60-second batch trigger writes many small files; engineers often compact them via a periodic background job.
- **Schema drift.** The streaming schema must stay compatible with the batch writer's expectations; a schema change on the producer can break the batch sink. See [[schema-evolution]].
- **Exactly-once vs. at-least-once.** Duplicate events in the batch store can throw off aggregates. Batch writers typically rely on idempotent outputs and deterministic partitioning.

## Related pages

- [[streaming-storage]]
- [[lambda-architecture]]
- [[kappa-architecture]]
- [[log-based-message-brokers]]
- [[object-storage]]
- [[data-lakehouse]]
- [[stream-processing]]
- [[data-storage-stage]]
- [[data-warehousing]]
- [[event-sinking]]
