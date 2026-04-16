# Log-Based Message Brokers

**Summary**: Log-based message brokers (Apache Kafka, Amazon Kinesis, Twitter DistributedLog) combine the durable, replayable storage of databases with the low-latency notification of [[message-brokers]], using append-only partitioned logs with consumer offsets to track progress.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-15

---

## Motivation

Traditional AMQP/JMS-style [[message-brokers]] treat messaging as transient: messages are deleted after acknowledgment, so you cannot replay them. Databases store data permanently but lack low-latency notification. Log-based brokers are a hybrid: they provide durable, replayable storage with real-time notification of new messages (source: chapter-11-stream-processing.md).

This hybrid is important because it enables the same repeatable-processing property that makes [[batch-processing]] powerful: you can experiment with processing logic, fix bugs, and rerun without damaging input data (source: chapter-11-stream-processing.md).

## Using logs for message storage

A log is an append-only sequence of records on disk (the same structure used in [[sstables-and-lsm-trees|log-structured storage engines]], write-ahead logs in [[b-trees]], and [[replication]] logs). A producer appends a message to the log; a consumer reads sequentially. When the consumer reaches the end, it waits for notification of new messages -- similar to `tail -f` in Unix (source: chapter-11-stream-processing.md).

## Partitioning

To scale beyond a single disk's throughput, the log is [[partitioning|partitioned]]. Different partitions are hosted on different machines, each functioning as an independent log. A **topic** is defined as a group of partitions carrying messages of the same type (source: chapter-11-stream-processing.md).

Within each partition, the broker assigns a **monotonically increasing sequence number (offset)** to every message. Messages within a partition are **totally ordered**; there is no ordering guarantee across partitions (source: chapter-11-stream-processing.md).

Implementations: Apache Kafka, Amazon Kinesis Streams, Twitter DistributedLog. Google Cloud Pub/Sub is architecturally similar but exposes a JMS-style API (source: chapter-11-stream-processing.md).

## Logs compared to traditional messaging

| Aspect | Traditional (AMQP/JMS) | Log-based (Kafka) |
|---|---|---|
| Fan-out | Via topic subscriptions/exchange bindings | Trivially supported -- reading doesn't delete |
| Load balancing | Per-message assignment to consumers | Per-partition assignment to consumers |
| Parallelism ceiling | Unlimited consumers | At most one consumer per partition |
| Message ordering | May be broken by redelivery | Preserved within each partition |
| Slow message handling | Blocks only that consumer's queue | Blocks processing of subsequent messages in that partition (head-of-line blocking) |

The log-based approach is preferable when message throughput is high, each message is fast to process, and ordering matters. The JMS/AMQP style is preferable when messages are expensive to process, per-message parallelism is needed, and ordering is less important (source: chapter-11-stream-processing.md).

## Consumer offsets

Because consumers read a partition sequentially, tracking progress is simple: all messages with offset less than the consumer's current offset have been processed; all with greater offset have not. The broker only needs to periodically record consumer offsets, rather than tracking per-message acknowledgments (source: chapter-11-stream-processing.md).

This offset mechanism is very similar to the **log sequence number** in [[leader-based-replication]]: the message broker behaves like a leader database, and the consumer like a follower. If a consumer fails, another node resumes from the last recorded offset (source: chapter-11-stream-processing.md).

## Disk space management

Logs are divided into **segments**. Old segments are periodically deleted or archived. If a slow consumer falls so far behind that its offset points to a deleted segment, it will miss messages. The log implements a bounded-size buffer (circular/ring buffer) on disk (source: chapter-11-stream-processing.md).

In practice, this buffer is very large. A 6 TB disk with 150 MB/s sequential write throughput can buffer approximately 11 hours of messages at maximum write rate. Real deployments typically retain several days or weeks. Throughput remains constant regardless of retention length, unlike in-memory brokers that degrade when queues spill to disk (source: chapter-11-stream-processing.md).

## When consumers can't keep up

If a consumer falls behind, the log-based approach buffers messages on disk. Only the slow consumer is affected -- it does not disrupt other consumers. You can monitor the gap between a consumer's offset and the head of the log and alert if it grows too large. This operational isolation is a major advantage: you can safely run experimental consumers against a production log without risking the production service (source: chapter-11-stream-processing.md).

Contrast this with traditional brokers where an unconsumed queue continues accumulating messages and consuming memory from other active consumers (source: chapter-11-stream-processing.md).

## Replaying old messages

In a log-based broker, consuming messages is a **read-only** operation -- it does not change the log. The consumer offset is under the consumer's control and can be manipulated: you can start a new consumer with yesterday's offsets, write output to a different location, and reprocess a day's messages. This makes log-based messaging similar to [[batch-processing]], where derived data is clearly separated from input data (source: chapter-11-stream-processing.md).

## Log compaction

Log compaction (the same technique used in [[hash-indexes]] and [[sstables-and-lsm-trees|log-structured storage engines]]) periodically discards older records for the same key, keeping only the most recent update. A **tombstone** (null value) indicates a deleted key (source: chapter-11-stream-processing.md).

With log compaction, a new consumer can start from offset 0 and obtain a full copy of the database contents by scanning the entire compacted log. This eliminates the need for periodic snapshots when setting up new derived systems. Apache Kafka supports this feature, effectively allowing the message broker to serve as **durable storage**, not just transient messaging (source: chapter-11-stream-processing.md).

See [[change-data-capture]] for how log compaction interacts with CDC, and [[event-sourcing]] for why log compaction works differently with event-sourced systems.

## Related pages

- [[stream-processing]]
- [[event-streams]]
- [[message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[partitioning]]
- [[replication]]
- [[leader-based-replication]]
- [[batch-processing]]
- [[hash-indexes]]
- [[sstables-and-lsm-trees]]
