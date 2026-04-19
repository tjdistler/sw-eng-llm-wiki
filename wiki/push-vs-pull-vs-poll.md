# Push vs Pull vs Poll

**Summary**: The three directional patterns for moving data between a source and an [[data-ingestion|ingestion system]]. **Push** means the source writes to the target. **Pull** means the target reads from the source. **Poll** is a pull-flavoured pattern in which the target periodically checks the source for new data and pulls when it sees change. Reis and Housley note the lines are blurry — many real pipelines mix all three at different stages.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The three patterns

| Pattern | Who initiates | Typical example |
|---|---|---|
| **Push** | Source system | [[webhooks|Webhook]] from a SaaS platform; a source application publishes to a message queue; file-based export dropped into object storage |
| **Pull** | Target ingestion system | [[etl-vs-elt|ETL]] extract; [[query-based-cdc|timestamp-based batch CDC]]; a scheduled reader pulls via JDBC/ODBC |
| **Poll** | Target ingestion system, periodically | An ingestion tool checks a source API or file location for change on a schedule; when change is detected, it pulls |

(source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md; raw/fundamentals-of-data-engineering/chapter-07-ingestion.md)

## Why the distinction matters

The pattern determines:

- **Who bears the load of deciding when to move data.** Push: the source; pull/poll: the target.
- **Latency.** Push is typically lower-latency — the source fires immediately. Poll adds up to one poll-interval of delay. Pull can be either, depending on schedule.
- **Coupling.** Push can couple a source to a target's endpoint availability (webhook retries get lossy if the target is down). Pull leaves the source unaware of who is reading.
- **Load on the source.** Pull requires querying; aggressive pull can overload the source. Push offloads the trigger cost to the source's natural write path.
- **Security surface.** Pull requires the ingestion system to authenticate inward against the source. Push requires the source to authenticate outward to a consumer endpoint.

## The lines blur

Chapter 2 emphasizes that push/pull is **not binary** (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Real pipelines mix both, often within a single CDC implementation:

| Mechanism | Direction | Notes |
|---|---|---|
| **ETL extract** | Pull | Queries a snapshot of the source on a fixed schedule |
| **Trigger-based [[cdc-triggers|CDC]]** | Push (at the trigger), then pull (on the queue) | Trigger fires on row change; message is pushed to a queue; ingestion system picks it up |
| **[[change-data-capture\|Log-based CDC]]** | Push (from the DB) | DB appends to binlog/WAL; ingestion reads the log |
| **[[query-based-cdc\|Timestamp-based batch CDC]]** | Pull | Target periodically queries for rows changed since last read |
| **IoT event ingestion** | Push | Devices write directly to ingestion endpoint / streaming platform |
| **[[webhooks]]** | Push | Source POSTs to a consumer-hosted HTTP endpoint |
| **Message queues and event streams** | Consumer pulls from the broker in most systems | See [[consumer-offset]]; the broker already holds what the source pushed |

(source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md; raw/fundamentals-of-data-engineering/chapter-07-ingestion.md)

## File-based export as push

Ch 7 explicitly labels [[file-based-ingestion|file-based export]] as a push-based pattern: "data export and preparation work is done on the source system side." Once the files are ready, they are handed off via object storage, SFTP, EDI, or SCP (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Consumer pull vs push for streams

Inside the stream-ingestion space, the same vocabulary shows up **between broker and consumer**. Ch 7 notes (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Kafka and Kinesis support only pull subscriptions.** Subscribers read messages from the topic and confirm when they have been processed.
- **Pub/Sub and RabbitMQ support both pull and push subscriptions.** Push allows the broker to write messages to a listener endpoint.

Reis and Housley's default recommendation: "pull subscriptions are the default choice for most data engineering applications, but you may want to consider push capabilities for specialized applications." A pull-only system can still push by adding an extra layer that reads and then writes outward.

## Design implications

- **Favour push when the source is willing to initiate** — it usually yields lower latency and less source load.
- **Favour pull when you cannot trust the source to initiate reliably** — or when the target needs explicit control of timing.
- **Polling is a compromise** — useful when neither side supports push natively but some change signal exists (modification time, autoincrementing id, `updated_at`).

## Related pages

- [[data-ingestion]]
- [[change-data-capture]]
- [[query-based-cdc]]
- [[cdc-triggers]]
- [[outbox-table-pattern]]
- [[webhooks]]
- [[file-based-ingestion]]
- [[message-brokers]]
- [[event-streams]]
- [[consumer-offset]]
