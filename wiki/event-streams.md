# Event Streams

**Summary**: An event stream is a sequence of immutable, timestamped records (events) that are incrementally produced over time and consumed by one or more subscribers. Events are the fundamental unit of data in [[stream-processing]] systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Last updated**: 2026-04-16

---

## What is an event?

An event is a small, self-contained, immutable object containing the details of something that happened at some point in time. It typically includes a timestamp indicating when it occurred. Examples include (source: chapter-11-stream-processing.md):

- A user action (viewing a page, making a purchase)
- A machine measurement (temperature sensor reading, CPU utilization metric)
- A database write (a row inserted or updated)

Events can be encoded as text strings, JSON, or binary formats (see [[encoding-formats]]). This encoding allows them to be stored (appended to a file, inserted into a database) or sent over a network.

## Producers and consumers

An event is generated once by a **producer** (also called publisher or sender) and potentially processed by multiple **consumers** (subscribers or recipients). This is analogous to batch processing where a file is written once and read by multiple jobs (source: chapter-11-stream-processing.md).

Related events are grouped into a **topic** or **stream**, analogous to a filename identifying a set of related records in a filesystem.

## Delivery mechanisms

### Polling vs notification

A file or database could connect producers and consumers: producers write events, consumers periodically poll for new ones. But polling becomes expensive as frequency increases -- most requests return no new data. It is better for consumers to be **notified** when new events appear. Databases have traditionally not supported this well (triggers are limited). Specialized [[message-brokers]] and [[log-based-message-brokers]] were developed for this purpose (source: chapter-11-stream-processing.md).

### Direct messaging

Some systems use direct producer-to-consumer communication without intermediaries (source: chapter-11-stream-processing.md):

- **UDP multicast** -- used in financial trading for low-latency stock feeds
- **Brokerless messaging** (ZeroMQ, nanomsg) -- publish/subscribe over TCP or IP multicast
- **StatsD/Brubeck** -- unreliable UDP for metrics collection
- **Webhooks** -- a consumer registers a callback URL; the producer makes HTTP/RPC requests when events occur

These systems work well for specific use cases but generally require application code to handle message loss. They assume producers and consumers are constantly online (source: chapter-11-stream-processing.md).

### Message brokers

For more robust delivery, events are sent through [[message-brokers]] or [[log-based-message-brokers]], which provide buffering, durability, and fan-out capabilities.

## Multiple consumer patterns

When multiple consumers read from the same topic, two patterns are used (source: chapter-11-stream-processing.md):

- **Load balancing**: each message is delivered to *one* consumer. Consumers share the work. Useful when messages are expensive to process. (AMQP: multiple clients on same queue; JMS: shared subscription.)
- **Fan-out**: each message is delivered to *all* consumers. Independent consumers each get the full broadcast. (JMS: topic subscriptions; AMQP: exchange bindings.)

These patterns can be combined: two separate consumer groups each receive all messages, but within each group, only one node receives each message (source: chapter-11-stream-processing.md).

## Immutability of events

Events are immutable records of things that happened. This property is powerful for several reasons (source: chapter-11-stream-processing.md):

- **Auditability** -- like accounting ledgers, incorrect entries are corrected by adding compensating entries, not by erasing. The original record remains for audit purposes.
- **Richer information** -- a customer adding an item to their cart and then removing it captures intent that would be lost in a mutable database that simply deletes the row.
- **Bug recovery** -- if buggy code writes bad data, an immutable event log makes it easier to diagnose and recover than a database where data has been destructively overwritten.
- **Multiple views** -- the same event log can feed multiple derived read-optimized representations (search indexes, analytics databases, caches). See [[change-data-capture]] and [[event-sourcing]].

For the relationship between mutable state and immutable event logs, see [[event-sourcing]].

## FaaS as an event consumer

Burns's Chapter 8 treatment of [[functions-as-a-service|FaaS]] positions event-driven functions as natural consumers of event streams: small, stateless, asynchronous handlers that fire once per event and scale automatically with event rate (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md). The broker-and-FaaS combination is common in practice — the broker provides buffering, fan-out, and replay; the FaaS provides compute that scales to zero when no events arrive. Burns's [[event-pipeline-pattern]] arranges multiple such functions into a directed graph; [[faas-decorator-pattern]] is the inbound request variant.

## Related pages

- [[stream-processing]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[encoding-formats]]
- [[windowing]]
- [[functions-as-a-service]]
- [[event-pipeline-pattern]]
