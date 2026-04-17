# Message Brokers and Async Message Passing

**Summary**: Message brokers sit between services, storing messages temporarily and delivering them asynchronously. They decouple producers from consumers in time, space, and identity — providing reliability, buffering, and fan-out that direct [[rpc|RPC]] calls cannot. The actor model extends this pattern to concurrency within and across nodes.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`, `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`, `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`, `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## Async Message Passing vs RPC and Databases

Async message passing sits between [[rpc|RPC]] and databases:
- Like RPC: messages are delivered with low latency.
- Like databases: messages pass through an intermediary (the broker) rather than a direct connection, and the sender does not wait for a response.

## What a Message Broker Does

A producer sends a message to a **named queue or topic**. The broker stores the message and delivers it to one or more consumers subscribed to that queue or topic. Examples: RabbitMQ, ActiveMQ, Apache Kafka, NATS, HornetQ; historically TIBCO and IBM WebSphere.

Key properties:
- **Buffering**: if a consumer is slow or temporarily unavailable, the broker queues messages rather than dropping them or failing the producer.
- **Automatic redelivery**: if a consumer crashes after receiving but before processing a message, the broker can redeliver to another instance.
- **Location decoupling**: producers don't need to know the IP address or port of consumers. Particularly useful in cloud environments where virtual machines come and go.
- **Fan-out**: one message can be delivered to multiple consumers (pub/sub model).
- **Logical decoupling**: producers and consumers can be deployed, scaled, and evolved independently.

## One-Way Communication

Unlike RPC, message passing is normally **one-way**. Producers publish and forget. If a consumer needs to send a response, it publishes to a separate reply queue (which the original producer may subscribe to). This is the request-response pattern over messaging, but it requires the original sender to maintain state about outstanding requests.

Producers are **asynchronous**: they don't block waiting for delivery or processing.

## Schema Compatibility in Message Brokers

Brokers typically treat messages as opaque byte sequences with metadata — they don't enforce any data model. This means the encoding format is the producer's and consumer's responsibility.

The same [[backward-forward-compatibility]] rules apply as with databases and RPC. Because producers and consumers are deployed independently, the message format must support rolling upgrades:

- If you use a format with explicit compatibility rules ([[schema-evolution]] — Thrift, Protocol Buffers, Avro), you can change producers and consumers independently.
- If a consumer re-publishes messages to another topic (chaining), it must **preserve unknown fields** — otherwise it may silently strip data that a downstream consumer needs. This is the same problem as [[data-outlives-code]] in databases: a node that doesn't understand a field must not erase it.

## Message Brokers vs Databases

Message brokers are similar to databases in some ways (both store data, both can participate in [[two-phase-commit]] via XA/JTA), but there are important practical differences (source: chapter-11-stream-processing.md):

| Aspect | Databases | Message brokers |
|---|---|---|
| Retention | Keep data until explicitly deleted | Auto-delete after successful delivery |
| Working set | Large, on disk | Small, in memory (performance degrades if queues spill to disk) |
| Data access | Secondary indexes, arbitrary queries | Subscribe to topics matching a pattern |
| Query model | Point-in-time snapshot; client must re-query to see changes | No arbitrary queries, but clients are notified when new data arrives |

## Multiple Consumer Patterns

When multiple consumers read from the same topic, two patterns apply (source: chapter-11-stream-processing.md):

- **Load balancing**: each message goes to *one* consumer, sharing the work. In AMQP, multiple clients consume from the same queue; in JMS, this is a shared subscription.
- **Fan-out**: each message goes to *all* consumers. In JMS, via topic subscriptions; in AMQP, via exchange bindings.

These patterns can be combined: multiple consumer groups each receive all messages, but within each group only one node gets each message (source: chapter-11-stream-processing.md).

## Acknowledgments and Redelivery

Consumers may crash before finishing processing. Brokers use **acknowledgments**: a consumer must explicitly tell the broker it has finished processing a message. If the connection closes without an acknowledgment, the broker redelivers the message to another consumer (source: chapter-11-stream-processing.md).

Redelivery combined with load balancing can break message ordering: if consumer 2 crashes while processing message m3, and consumer 1 is processing m4, then m3 is redelivered to consumer 1, which processes m4 before m3. Messages that are independent of each other are unaffected, but causal dependencies can be violated. To avoid this, use a separate queue per consumer (source: chapter-11-stream-processing.md).

## Message broker vs event broker (Bellemare)

Adam Bellemare's Chapter 2 of *Building Event-Driven Microservices* argues that message brokers and [[event-broker|event brokers]] solve **different problems**, and that an event broker can replace a message broker but a message broker cannot substitute for an event broker (source: raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md).

Two specific deficiencies make a message broker insufficient as an EDM substrate:

- **Shared-queue consumption.** Multiple applications consuming from the same queue each receive only a **subset** of messages — the queue load-balances across them. No single consumer ever sees the full stream. This makes it "impossible to correctly communicate state via events" because no consumer gets a full copy.
- **Delete-after-acknowledge.** Messages are removed from the broker once acknowledged. This precludes indefinite retention, global access, and replay — three properties a durable event log depends on.

Bellemare stresses that queue-shaped access patterns are still valid inside EDM architectures for specific use cases — message brokers "still have a role" — but they are not sufficient as the primary substrate of the architecture (source: chapter-02-event-driven-microservice-fundamentals.md). See [[event-broker]] for the corresponding concept page.

## Log-Based Message Brokers

Traditional message brokers treat messaging as transient (messages are deleted after acknowledgment). [[log-based-message-brokers]] combine the durable storage of databases with the low-latency notification of messaging, using append-only partitioned logs. Apache Kafka, Amazon Kinesis, and Twitter DistributedLog are examples. See [[log-based-message-brokers]] for details (source: chapter-11-stream-processing.md).

## The Actor Model

The **actor model** is a concurrency programming model in which:
- Logic is encapsulated in **actors** — each actor has private local state and communicates only by sending and receiving asynchronous messages.
- Actors process one message at a time, so there are no threads, no locks, and no race conditions within a single actor.
- Message delivery is not guaranteed — actors must be designed to tolerate lost messages.

This is a natural fit for distributed systems: the same message-passing mechanism works whether sender and recipient are on the same node or different nodes. The actor model does not pretend that remote calls behave like local calls (unlike RPC) — it acknowledges from the start that message delivery may fail. This makes **location transparency** more honest than in RPC.

### Distributed Actor Frameworks

**Distributed actor frameworks** integrate a message broker with the actor programming model:

| Framework | Default encoding | Rolling upgrade support |
|---|---|---|
| **Akka** | Java serialization (poor compatibility) | Replace with Protocol Buffers for rolling upgrades |
| **Orleans** | Custom format (no rolling upgrade support by default) | Requires blue/green cluster deployment |
| **Erlang OTP** | Native term format | Rolling upgrades are possible but require careful planning |

All three can support rolling upgrades with the right encoding, but it requires explicit attention — the framework doesn't do it for you.

## Brokers as a work-queue source

Burns's [[work-queue-pattern|Chapter 10 work queue]] treats a broker topic as one of several interchangeable work-item sources: an application-specific [[source-container-interface|source ambassador]] fronting a Kafka or Redis queue turns the broker into a pull-style item list that the generic queue-manager can consume (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The queue-manager never learns that the backing store is a broker — it issues `GET /api/v1/items` calls against `localhost`, the ambassador drains the broker and responds.

Two differences from a classic broker-consumer loop:

- Completion tracking lives in Kubernetes Job annotations, not in broker acks or Kafka consumer offsets. Work-item identity is the Job's name.
- The queue-manager is generic across source shapes — a filesystem listing, a cloud-storage bucket, or a broker all look the same behind the source-ambassador interface.

This makes the work queue a useful bridge between broker-shaped ingress and container-based batch processing.

## Brokers as the workflow transport

Burns's [[event-driven-batch-pattern|Chapter 11 event-driven batch pattern]] uses a pub/sub broker as the **transport layer** that wires together multi-stage batch workflows (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Each output stream of each workflow stage is a topic; linking containers ([[copier-pattern|copiers]], [[filter-pattern|filters]], [[splitter-pattern|splitters]], [[sharder-pattern|sharders]], [[merger-pattern|mergers]]) publish and subscribe to topics to build the workflow DAG. Burns treats Apache Kafka, Azure EventGrid, and Amazon SQS as interchangeable substrates at the pattern level. See [[publisher-subscriber-infrastructure]] for the Kafka-on-Kubernetes-via-Helm walkthrough and the topic-per-output-shard convention.

## Brokers as the substrate of an architecture style

Richards and Ford's [[event-driven-architecture]] (Chapter 14) treats the message broker as the **structural substrate of a whole architecture style**, not just an inter-service detail (source: raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md). Two topologies use the broker in materially different ways:

- **[[broker-topology]]** — events are **past-tense facts** broadcast to **pub/sub topics**. No central coordinator. Extensibility is the killer feature: new processors plug into existing event feeds without upstream changes. Federated brokers (one cluster per domain) are the common deployment.
- **[[mediator-topology]]** — a central mediator sends **commands** to **dedicated point-to-point queues**. Each queue has exactly one intended consumer. The broker is still the transport, but the vocabulary is imperative rather than declarative.

Data-loss prevention in event-driven architecture relies on the standard broker features already described above — **persistent queues + synchronous send** (producer → broker), **client acknowledge mode** (broker → consumer), and **ACID + last participant support** (consumer → database). The Chapter 14 treatment names these as the baseline for any production event-driven system.

The **request-reply** pattern in event-driven architecture is implemented over brokers using either a **correlation ID** in the message header (filter the reply queue by correlation ID) or a **temporary queue** per request. The correlation-ID variant is preferred at volume; the temporary-queue variant is simpler but stresses the broker's queue-creation path at scale (source: raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md).

## FaaS as a broker consumer

Burns's Chapter 8 ([[functions-as-a-service]]) positions FaaS as a compute substrate for broker-driven event handlers: a function fires per message, runs a small stateless handler, and returns. This is a clean fit for the broker model because brokers already provide buffering and fan-out — the FaaS platform adds automatic scaling and scale-to-zero (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md). Multiple FaaS handlers chained through a broker form Burns's [[event-pipeline-pattern]].

## Related pages

- [[rpc]]
- [[backward-forward-compatibility]]
- [[encoding-formats]]
- [[schema-evolution]]
- [[data-outlives-code]]
- [[log-based-message-brokers]]
- [[stream-processing]]
- [[event-streams]]
- [[change-data-capture]]
- [[two-phase-commit]]
- [[functions-as-a-service]]
- [[event-pipeline-pattern]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[event-driven-batch-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[event-driven-architecture]]
- [[broker-topology]]
- [[mediator-topology]]
- [[correlation-ids]]
- [[event-broker]]
- [[event-driven-microservices]]
