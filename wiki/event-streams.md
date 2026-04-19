# Event Streams

**Summary**: An event stream is a sequence of immutable, timestamped records (events) that are incrementally produced over time and consumed by one or more subscribers. Events are the fundamental unit of data in [[stream-processing]] systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`, `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`, `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

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

## Events vs commands in event-driven architecture

Richards and Ford's [[event-driven-architecture]] (Chapter 14) load-bears a distinction that DDIA's and DDS's stream-processing treatments do not emphasise: the difference between an **event** and a **command** as message types (source: raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md).

- **Event** — a past-tense fact. `order-created`, `payment-applied`, `email-sent`. An event **can be ignored** — any number of processors can subscribe, and none are required to.
- **Command** — an imperative instruction. `place-order`, `send-email`, `apply-payment`. A command **must be processed** by its named target.

The distinction underpins the two [[event-driven-architecture|event-driven architecture]] topologies: the [[broker-topology]] uses events on pub/sub topics (extensibility via architectural hooks anyone can subscribe to); the [[mediator-topology]] uses commands on point-to-point queues (a coordinator names exactly who must do what). The DDIA / DDS "event stream" concept maps directly onto the broker-topology notion of an event feed — both are immutable, timestamped, broadcast-to-whoever-listens records of things that happened.

## Event streams as a data communication structure

Adam Bellemare's Chapter 1 of *Building Event-Driven Microservices* treats event streams not just as a transport between services but as the **data communication structure of the whole organization** — the third of three [[communication-structures]] alongside business and implementation (source: raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md). Three framings follow.

### Events are the data

Events are not signals that data is ready elsewhere. Nor are they a wrapper around a direct data transfer between two implementations. **Events are simultaneously data storage and a means of asynchronous communication** (source: chapter-01-why-event-driven-microservices.md). Because they persist in the stream, consumers can read and re-read at their own pace, for as long as the retention policy allows — this is the property that separates Bellemare's event-driven microservices from the older transient-message-passing style.

### Event streams as single source of truth

Each event in a stream is a statement of fact. Together they form "a continuous, canonical narrative detailing everything that has happened in the organization" — the **single source of truth** for all systems (source: chapter-01-why-event-driven-microservices.md). A data communication structure is only as good as the veracity of its information, so the organization must commit to treating the streams as authoritative. If some teams put conflicting data in other locations, the single-source-of-truth property is significantly diminished and the whole EDM story weakens.

### Consumers do their own modeling

Unlike a shared-database or overloaded-implementation communication structure, event streams **provide no querying or lookup functionality** (source: chapter-01-why-event-driven-microservices.md). All business and application logic lives in the producer and consumer of the events. Each consumer pulls the events it needs, stores its own copy, builds its own model, and runs its own joins and queries. Producers are relieved of having to supply cross-team APIs, data-transfer mechanisms, or query services on behalf of downstream teams. This is the inversion that makes EDM scalable: the burden of access shifts from the data owner to the data consumer, and access to shareable data is democratized across the business.

See [[event-driven-microservices]] for the microservice-architecture-level consequences and [[communication-structures]] for the three-structure framing.

## Structural requirements in an event broker

Bellemare's Chapter 2 of *Building Event-Driven Microservices* enumerates the minimum storage/serving features any system must have to count as an [[event-broker]] for EDM purposes (source: raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md):

- **[[partitioning|Partitioning]]** — streams split into independent substreams so that parallel consumer instances can process each substream for greater throughput.
- **Strict ordering** — within a partition, events are served in the exact order they were published.
- **Immutability** — once published, an event cannot be modified. Corrections are expressed as new events.
- **Indexing** — each event gets an index (offset) at write time; consumers specify offsets to read from, and the tail-minus-current gap is the [[consumer-offset|consumer lag]].
- **Infinite retention** — events are retainable indefinitely, which is what lets the stream carry state, not just transient signals.
- **Replayability** — any consumer can read whatever events it needs from any point in the log.

These properties are what separate an event-broker-backed stream from a traditional [[message-brokers|message broker]]'s transient queue.

## The three event types

Bellemare classifies events by their key/value shape into three types (source: raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md):

- **[[unkeyed-event]]** — no key. A standalone statement of fact (e.g. a user opened a book).
- **[[entity-event]]** — keyed on the unique ID of an entity; the value carries the entity's full current state. The latest entity event per key fully determines current state, which is what makes [[table-stream-duality]] and [[log-compaction]] work.
- **[[keyed-event]]** — keyed but not an entity description; used primarily for [[partitioning]] locality and per-key ordering, often aggregated downstream into an entity event.

See [[event-structure]] for the shape rules and [[table-stream-duality]] for how entity events become queryable local state inside a microservice.

## Streams vs message queues (Reis & Housley)

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* draws the **message queue vs event stream** distinction sharply in the context of source systems (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **A message** is a raw data unit passed from System A to System B. Once delivered and acknowledged, it is removed from the queue. Messages are "discrete and singular signals" (e.g., an IoT temperature reading that triggers a furnace controller then goes away).
- **A stream** is an **append-only log of event records**. Events accumulate in an ordered sequence over a long retention window (often weeks or months). The stream is where "you care about what happened over many events" — aggregations across events, replay to any past point, complex multi-event analyses.

A streaming platform *can* move single messages (and is often used to) but a message queue *cannot* serve as a long-retention replayable log. This mirrors the Bellemare [[message-brokers|message broker]] vs [[event-broker|event broker]] distinction from a different angle — here framed for the lifecycle generation stage rather than the EDM substrate.

## Topics, partitions, and hotspotting (Reis & Housley)

Chapter 5's Kafka-lens treatment adds three concrete mechanics (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Topic.** A collection of related events. A producer streams events to a topic; zero, one, or many consumers read from it. An event in an order-processing system might go to a topic like `web-orders`, read by one `fulfillment` subscriber and one `marketing` subscriber — the same stream serves operational and analytics consumers simultaneously.
- **Stream partitions.** A topic is split into parallel substreams, each owned by one consumer at a time. The key lever is **parallelism**: more partitions → higher throughput. Messages with the same partition key always land on the same partition, giving per-key ordering.
- **Hotspotting.** A poorly-chosen partition key creates an unbalanced distribution — Reis and Housley's canonical example is partitioning IoT messages by US state, where California, Texas, Florida, and New York overwhelm their partitions while Wyoming is idle. The engineer must design the key to distribute load uniformly.

The partition-key hotspotting warning applies to every keyed stream. See [[partitioning-strategies]] for the broader topic and [[wide-column-database]] for the same problem at the row-key layer.

## Types of time in a stream (Reis & Housley)

Time is subtle in streaming. Chapter 5 names four distinct timestamps that arise for a single event (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Event time** — when the event was generated at the source.
- **Ingestion time** — when the event was accepted by the ingestion system (queue, store, database).
- **Process time** — when the consumer began processing the event.
- **Processing time** — how long processing took.

The Reis-and-Housley advice: log timestamps at each stage so the movement of data through the pipeline can be reconstructed after the fact. Bellemare's [[event-timestamps]] page gives the deeper treatment of why only two of these (event time, broker ingestion time) can anchor deterministic processing.

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
- [[event-driven-architecture]]
- [[broker-topology]]
- [[mediator-topology]]
- [[functions-as-a-service]]
- [[event-pipeline-pattern]]
- [[event-driven-microservices]]
- [[communication-structures]]
- [[event-broker]]
- [[event-structure]]
- [[entity-event]]
- [[keyed-event]]
- [[unkeyed-event]]
- [[table-stream-duality]]
- [[log-compaction]]
- [[tombstone]]
- [[consumer-offset]]
- [[consumer-group]]
