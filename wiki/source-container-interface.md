# Source Container Interface

**Summary**: The producer side of Burns's [[work-queue-pattern]]. A **source container** is the application-specific ambassador that exposes the work-queue's items to the generic queue-manager container over an HTTP REST API on `localhost`. The source hides the concrete backing store (a cloud-storage bucket, a network-filesystem directory, a Kafka/Redis topic) behind a uniform interface; the queue-manager stays reusable across applications.

**Sources**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## Where it sits

Every work queue needs a collection of items to process, but the sources vary wildly — objects in a cloud-storage bucket, files on an NFS share, messages in a pub/sub topic, rows in a database (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). Burns's move is to factor that source-specific logic into its own container and let the generic work-queue manager speak to it through a narrow, uniform API.

This is the [[ambassador-pattern]] applied to batch ingest (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

- The generic **work-queue manager** is the primary application container.
- The application-specific **source container** is the ambassador that proxies the manager's "give me the list of items" requests out to the concrete real-world source.

Both containers run in the same [[pod]], sharing the network namespace, so the manager connects to `localhost:8080` (or wherever the source ambassador listens) and never learns what the backing store actually is.

## The API

Burns defines the source interface as an HTTP REST API with two endpoints (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

```
GET http://localhost/api/v1/items
GET http://localhost/api/v1/items/<item-name>
```

The collection endpoint returns a list of item names:

```json
{
  "kind": "ItemList",
  "apiVersion": "v1",
  "items": ["item-1", "item-2", ...]
}
```

The item endpoint returns the details for a single item:

```json
{
  "kind": "Item",
  "apiVersion": "v1",
  "data": { "some": "json", "object": "here" }
}
```

The `data` field is passed through to the worker for processing (see [[worker-container-interface]]).

### Version the API from day one

Burns flags the `v1` in the URL explicitly: "It may not seem logical, but it costs very little to version your API when you initially define it. Refactoring versioning onto an API without it, on the other hand, is very expensive. Consequently, it is a best practice to always add versions to your APIs even if you're not sure they will ever change" (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). This mirrors the general API-evolution discipline from [[breaking-changes]] and [[backward-forward-compatibility]].

### What the API deliberately omits

The source API has **no endpoint for marking an item as processed**. Burns makes this choice deliberately to keep the source container as dumb as possible: "the goal of this effort is to place as much of the generic implementation inside of the generic work queue manager as possible. To that end, the work queue manager itself is responsible for tracking which items have been processed and which items remain to be processed" (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

In Burns's [[work-queue-pattern|implementation]], that tracking lives in Kubernetes Job annotations rather than in the source or in a sidecar database. The source only has to answer "what items exist right now?" — nothing more.

## Implementation patterns

Although each application's source is bespoke in principle, Burns notes that a small number of generic source containers cover most real cases (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

- A source that lists objects in a cloud-storage bucket.
- A source that lists files in a network-filesystem directory.
- A source that drains a Kafka topic or Redis pub/sub queue.

Users pick the source that matches their backing store and configure it; most never have to write one. This is the [[modular-reusable-containers]] discipline applied to work-queue ingest: parameterize the source, define the API surface, document it.

### Worked example: NFS directory listing

The chapter's video-thumbnailer example uses a directory listing on an NFS share (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The source is a ~30-line Node program that reads a `MEDIA_PATH` environment variable, lists `*.mp4` files in that directory, and returns them as the `items` response. That is the entire application-specific code for this pipeline; everything else — fetching, scheduling, retrying — comes from the generic queue-manager and the off-the-shelf `ffmpeg` worker container.

## Relationship to other wiki concepts

### Ambassador pattern

This is a textbook [[ambassador-pattern]] use: brokering the queue manager's outbound request for "items to process" into whatever protocol the backing store speaks. Burns's recurring client-side/server-side trade-off applies — for very widely shared sources (a company-standard Kafka topic), the source could equally well be a shared service in front of the broker rather than a per-pod ambassador.

### Work-queue pattern

See [[work-queue-pattern]] for the full pattern. This page covers the producer-side interface; [[worker-container-interface]] covers the consumer-side interface.

### Message brokers

A source container fronting a broker topic makes a [[message-brokers|message broker]] look like a pull-style item list. This is a useful glue: existing broker-based pipelines can feed a work queue without the queue manager needing to speak AMQP or Kafka directly.

### Source ambassadors as filter primitives

Burns's [[event-driven-batch-pattern|Chapter 11 event-driven batch pattern]] stacks source ambassadors to build the [[filter-pattern|filter pattern]]: a filter container wraps an existing source ambassador, applies a predicate, and returns the shorter list to the queue-manager (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). This is ambassador-on-ambassador composition — the downstream queue is unchanged, the upstream source is unchanged, and the filter is a drop-in wrapper. The same shape underlies the [[merger-pattern]], which adapts multiple source ambassadors into one.

## Related pages

- [[work-queue-pattern]]
- [[worker-container-interface]]
- [[ambassador-pattern]]
- [[modular-reusable-containers]]
- [[pod]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[backward-forward-compatibility]]
- [[breaking-changes]]
- [[event-driven-batch-pattern]]
- [[filter-pattern]]
- [[merger-pattern]]
- [[designing-distributed-systems]]
