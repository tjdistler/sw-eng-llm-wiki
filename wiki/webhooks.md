# Webhooks

**Summary**: A simple event-based data-transmission pattern in which the **source** pushes an HTTP POST to a **consumer**-hosted endpoint when a specified event occurs. The connection direction is the reverse of a normal API call — hence the common label "reverse API." Webhooks are the cheap-and-cheerful alternative to setting up a full [[message-brokers|message broker]] when a third-party SaaS needs to notify a downstream system.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The shape

A webhook is registered by the consumer: "when event X happens in your system, please POST the details to this URL of mine." The source fires the HTTP request; the consumer's endpoint does whatever it wants with the payload — store it, enqueue it, trigger a downstream process (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

```
[source system] --POST event payload--> https://consumer.example.com/hook
```

Reis and Housley emphasize the direction: unlike a typical API where the consumer pulls, in a webhook the source pushes. "The connection goes from the source system to the data sink, the opposite of typical APIs. For this reason, webhooks are often called reverse APIs" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Typical producers

- **SaaS platforms** (Stripe, GitHub, Shopify) — payment events, push events, order events.
- **Application backends** — internal "something happened" notifications.
- **Mobile or web pages** — user-action events delivered via the app's backend.

## Why webhooks are attractive for ingestion

- **No broker to operate.** Just an HTTPS endpoint; let the SaaS or source system do the pushing.
- **Low latency.** Events arrive within seconds of occurrence.
- **Zero read-side load on the source.** The source decides when to send; the consumer doesn't poll.

## Why they're hard to scale

Webhooks struggle under real-world volume and reliability constraints:

- **Delivery is not durable by default.** If the consumer endpoint is down when the webhook fires, many senders will retry a few times and then give up. Some guarantee delivery; most don't.
- **Ordering is not guaranteed.** Webhooks are independent HTTP requests.
- **Rate spikes can overwhelm.** A burst of webhook POSTs against a single endpoint can exceed its capacity.
- **Idempotency is the consumer's problem.** Retries or duplicate deliveries are routine.

The Reis-and-Housley-recommended mitigation: "engineers commonly use message queues to ingest data at high velocity and volume" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). The webhook endpoint becomes a thin adapter that pushes incoming events to a message queue or event-streaming platform for durable retention and replay. See [[message-brokers]] and [[log-based-message-brokers]].

## Ch 7 — the recommended full-fat architecture

Chapter 7 of *Fundamentals of Data Engineering* explicitly calls out that webhook-based ingestion "can be brittle, difficult to maintain, and inefficient." The book's recommended robust architecture in AWS (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

```
[source] --POST--> Lambda --> Kinesis --> Flink --> S3
            (receive)    (buffer)   (stream-process)  (long-term)
```

- **Lambda (or similar FaaS)** receives the incoming HTTP POSTs. Scales elastically, decouples the endpoint from downstream.
- **Kinesis (or another managed event-streaming platform)** stores and buffers the messages, adding durability and replay.
- **Flink (or similar stream processor)** handles real-time analytics on the events.
- **S3** for long-term storage and replay archive.

Ch 7's general observation: this architecture "does much more than simply ingest the data. This underscores ingestion's entanglement with the other stages of the data engineering lifecycle; it is often impossible to define your ingestion architecture without making decisions about storage and processing" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

The takeaway for webhook ingestion specifically: **do not let the consumer endpoint be both the HTTP receiver and the processor.** Split them, and put a durable buffer between.

## Connection to the rest of the wiki

Bellemare's Chapter 4 notes that centralized [[data-liberation-framework|liberation frameworks]] and modern FaaS-based integrations frequently use webhooks as the on-ramp into the [[event-broker]] — fronting a webhook endpoint with a lightweight function that normalizes the payload and publishes to a topic. See [[faas-triggers]] for webhooks as a FaaS trigger category, and [[event-pipeline-pattern]] for the directed-graph-of-functions-plus-webhooks pattern.

The [[third-party-api-integration]] page deals with the **outbound** side of integrating with external systems; webhooks are the **inbound** side of the same broader problem — talking to services you don't own.

## Cross-book connections

- [[functions-as-a-service]] (Burns) — webhooks as a FaaS trigger; the login-to-2FA example.
- [[faas-triggers]] (Bellemare) — webhook as one of the five EDM-relevant trigger categories.
- [[event-pipeline-pattern]] (Burns) — a graph of functions connected by webhook-shaped edges.
- [[rpc]] / REST — the "forward" direction of the same HTTP substrate webhooks invert.

## Related pages

- [[source-systems]]
- [[data-ingestion]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[third-party-api-integration]]
- [[faas-triggers]]
- [[functions-as-a-service]]
- [[event-pipeline-pattern]]
- [[rpc]]
- [[push-vs-pull-vs-poll]]
- [[dead-letter-queue]]
