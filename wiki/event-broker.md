# Event Broker

**Summary**: Adam Bellemare's name for the **central infrastructure component** of an event-driven microservice platform — a distributed, durable, partitioned, replayable, append-only log system that is the single source of truth for all inter-service data. Apache Kafka is the canonical example. Event brokers generalize [[message-brokers|message brokers]] by retaining events indefinitely and serving them to many independent consumers at their own pace; Bellemare argues this generalization is strictly required for event-driven microservices and that traditional message brokers cannot substitute.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## Role in EDM

The event broker sits "at the heart of every production-ready event-driven microservice platform" (source: chapter-02-event-driven-microservice-fundamentals.md). It is the system that receives events, stores them in a queue or partitioned event stream, and serves them for consumption by other processes. Events are typically grouped into different streams by logical meaning — similar to how a database has many tables, each containing a specific type of data.

The event broker is the substrate that realizes the **data [[communication-structures|communication structure]]** in an EDM organization. It is the piece that makes events be simultaneously storage and communication.

## Cluster model and operational properties

Production-grade event broker platforms all follow the same general model: **multiple distributed broker nodes cooperate in a cluster** to provide production, consumption, and storage capacity (source: chapter-02-event-driven-microservice-fundamentals.md). Four essential operational properties follow from this model:

- **Scalability** — adding broker nodes increases cluster throughput and storage capacity.
- **Durability** — event data is **replicated between nodes**; a single broker failure does not lose data.
- **High availability** — clients reconnect to other nodes when a broker fails; uptime survives individual broker failures.
- **High performance** — the cluster distributes load; each broker must also serve hundreds of thousands of reads or writes per second.

## Minimum required storage/serving features

Bellemare lists the **minimum requirements** a system must satisfy to count as an event broker for EDM purposes (source: chapter-02-event-driven-microservice-fundamentals.md):

- **[[partitioning|Partitioning]].** Streams split into independent substreams so that consumer instances can process partitions in parallel for greater throughput. Queues are optional for this — stream topics require it.
- **Strict ordering.** Within a partition, data is served in the exact order it was originally published.
- **Immutability.** Once published, an event cannot be modified. Corrections are expressed as new events.
- **Indexing.** Each event is assigned an index (offset) at write time; consumers specify offsets to read from. [[consumer-offset|Consumer lag]] is derived from the difference between the consumer's offset and the tail.
- **Infinite retention.** Events must be retainable indefinitely — foundational for maintaining state from the stream.
- **Replayability.** Any consumer must be able to read whatever data it requires from any point in the log — foundational for the single-source-of-truth story and for bootstrapping new consumers.

## Selection factors

Beyond the minimum features, Bellemare lists additional factors that drive event broker selection (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Support tooling.** Browsing events and schemas; quotas, access control, and topic management; monitoring, throughput, and lag measurements.
- **Hosted services.** Does a managed offering exist? Will the team self-host? Does the hosted option couple you to a single provider? Is professional support available?
- **Client libraries and processing frameworks.** Coverage of the languages and frameworks you use. Are you using mainstream frameworks or rolling your own?
- **Community support.** Mature, production-ready, widely used, attractive to new hires. Apache Kafka is the chapter's exemplar of strong community support.
- **Long-term and tiered storage.** Older segments may roll to cheaper backing stores (S3, GCS, Azure Storage). Can data roll up and down tiers automatically? Can it be retrieved seamlessly?

## Event broker vs message broker

Bellemare explicitly contrasts the two, arguing that an event broker **can replace** a message broker but not vice versa (source: chapter-02-event-driven-microservice-fundamentals.md):

| Aspect | [[message-brokers|Message broker]] | Event broker |
|---|---|---|
| Retention | Deletes messages after acknowledgment | Retains events indefinitely |
| Shape | Queues | Partitioned, append-only log |
| Multiple consumers | Each consumer sees **a subset** of messages from a shared queue | Each consumer sees **all** events via its own offset |
| Replay | Not possible — consumed messages are gone | First-class — consumer picks up from any offset |
| Suited for | Task distribution, work queues, transient signals | Durable ordered log of facts; state communication; single source of truth |

Two deficiencies make a message broker inadequate for EDM specifically (source: chapter-02-event-driven-microservice-fundamentals.md):

1. The shared-queue model means no individual consumer gets a **full copy** of all events — so state cannot be correctly communicated via events.
2. Messages are **deleted after acknowledgment**, preventing indefinite storage, global access, and replay.

Message broker patterns are still useful inside EDM architectures for specific access patterns that map awkwardly onto partitioned streams. But the substrate of the architecture must be an event broker.

## Consumption modes

An event broker's append-only log can be consumed in two modes (source: chapter-02-event-driven-microservice-fundamentals.md):

- **As a stream.** Each consumer maintains its own offset (see [[consumer-offset]]); multiple consumers read independently; [[consumer-group|consumer groups]] support horizontal scaling with partition-level assignment.
- **As a queue.** Each event is consumed by exactly one consumer; once consumed it is marked and not re-delivered. Order is *not* preserved under parallel queue consumption. Not all brokers support this mode — Apache Pulsar does, Apache Kafka does not.

See [[consumer-offset]] and [[consumer-group]] for the mechanics.

## Single source of truth

Because the broker is durable, immutable, ordered, and replayable, it is positioned as "the only location in which services consume and produce data" — every consumer is guaranteed to receive an identical copy of the data (source: chapter-02-event-driven-microservice-fundamentals.md). Adopting this posture requires a **cultural shift**: teams previously running direct SQL queries against a monolith's database must now publish that data to the event broker, and they become accountable for any divergence between the streams and the underlying database.

See [[communication-structures]] and [[event-driven-microservices]] for the organizational ramifications.

## Relationship to existing wiki coverage

- **[[log-based-message-brokers]]** — the DDIA-level treatment of the same category of system (Kafka, Kinesis, DistributedLog). Bellemare's "event broker" is the EDM-centric name for the same thing, with stricter framing around being the organization's single source of truth.
- **[[message-brokers]]** — the traditional AMQP/JMS-style system; insufficient as an EDM substrate.
- **[[single-writer-principle]]** — Bellemare's convention for managing write ownership on top of an event broker.

## Related pages

- [[log-based-message-brokers]]
- [[message-brokers]]
- [[event-streams]]
- [[event-driven-microservices]]
- [[communication-structures]]
- [[partitioning]]
- [[consumer-offset]]
- [[consumer-group]]
- [[log-compaction]]
- [[single-writer-principle]]
- [[schema-evolution]]
