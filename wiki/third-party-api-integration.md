# Third-Party API Integration

**Summary**: Calling a synchronous request-response API from inside an event-driven workflow. The microservice consumes an input event, composes an HTTP request, blocks for the reply, parses it into an event, and produces it to an output stream. Simple in shape but loaded with non-obvious hazards: nondeterminism on reprocessing, brittle external contracts, and surge-induced rate-limit collisions.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## The pattern

An EDM often needs to call a third-party API — a payment processor, an email sender, a geocoding service. The request-response call slots into the event loop as a remote function call (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

```
while (true):
  events = consumer.consume("input-stream")
  for event in events:
    request = generateRequest(event, ...)
    response = RequestService.makeBlockingRequest(request, timeout, retries, ...)
    if response.code == 200:
      parsed = parseResponseToObject(response)
      outEvent = applyBusinessLogic(parsed, event, ...)
      producer.produce("output-stream", outEvent)
    else:
      // decide: retry, fail, log, skip
  consumer.commitOffsets()
```

The reply is treated as any other input — parsed, schema-validated, combined with the originating event, emitted to an output stream.

## When to capture the response as an event

The decision depends on whether downstream business logic needs the reply's detail (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- **Fire-and-forget** — sending advertisement emails via a third-party service. An HTTP 202 is enough; you don't need to materialize the response.
- **Response is essential** — a payment processor's reply specifying success/failure, error messages, and a traceable transaction ID. Downstream accounting services need to reconcile against these, so the reply absolutely becomes an event.

## Parallelism

Parallel processing is valid **only for queue-style streams** where ordering does not matter (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Nonblocking requests can be issued in parallel; wait for all of them before committing offsets. For ordered streams, stick to sequential blocking calls.

## The hazards

### Nondeterminism on reprocessing

Making an external call introduces a nondeterministic element into the workflow. [[reprocessing-event-streams|Reprocessing]] a failed batch — or a bug-fix replay — may return different results than the original call (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Downstream consumers reading the resulting output stream will see a different "history" than they did originally.

See [[deterministic-stream-processing]] for why this matters; third-party API calls are one of the canonical violations.

### External contract breakage

When the API is controlled by someone outside your organization, they can change the request shape, response format, or semantic meaning at will. Your microservice can fail without warning (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Usual defenses — contract testing, versioned endpoints, fail-fast on schema violation — apply.

### Surge on reprocessing

EDMs consume and process as fast as they can execute (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Rewinding the input stream for reprocessing can cause a massive surge of requests to the external API — quickly exceeding quotas, triggering IP-level blocks, or burning through paid-usage budgets in minutes.

Mitigations:

- **Quotas** on your consumer — rate-limit the consumption itself.
- **Client-side throttling** at the microservice. This is often your responsibility when the external API does not enforce it cleanly, particularly for services that burst but charge disproportionately above baseline (some logging and metrics providers fit this profile).
- Being aware of the cost math before hitting "replay" on a large topic.

## FoDE framing: APIs as a source-system category

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* frames APIs not as the EDM-shaped outbound call Bellemare focuses on, but as a **source-system category** — a way the data engineer **receives** data from somebody else's system (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). "APIs are now a standard and pervasive way of exchanging data in the cloud, for SaaS platforms, and between internal company systems." The chapter catalogues the HTTP-based paradigms a data engineer meets:

- **REST.** The dominant paradigm, built around HTTP verbs and stateless interactions. Critics point out REST "is in no way a full specification" — the data engineer must acquire significant domain knowledge per API. The variation in API abstraction is wide: some APIs are thin wrappers that barely protect the internals; others are "masterpieces of engineering" that prepare data for analytics use cases (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). See [[rpc]] for the DDIA treatment.
- **[[graphql|GraphQL]].** Facebook's alternative; multiple data models per request; client-specified query shapes. Encountered often, but with worse caching characteristics than REST.
- **[[rpc|gRPC]].** HTTP/2-based, Protocol-Buffers-encoded, efficient bidirectional. "Many Google services... offer gRPC APIs." Common inside organizations; rare across company boundaries.
- **[[webhooks|Webhooks]].** The reverse direction — source pushes to consumer. Often used alongside a message queue to make delivery durable.

### Operational practices that reduce API plumbing

Reis and Housley point to two developments that have simplified API-shaped ingestion (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Client libraries** — many API providers ship language-specific client libraries (especially Python) that handle authentication, pagination, retries, and error-mapping. The engineer's undifferentiated plumbing work drops.
- **Off-the-shelf SaaS/OSS connectors** — services and open-source libraries that manage data synchronization for common APIs. "Engineers would do well to reduce undifferentiated heavy lifting by using off-the-shelf tools."

But: "there are numerous data APIs without client libraries or out-of-the-box connector support." At large companies, the engineer will still write custom code for long-tail APIs — understanding their data structure, extraction logic, and synchronization strategy from first principles.

## Related pages

- [[event-driven-request-response-integration]]
- [[external-events-ingestion]]
- [[rpc]]
- [[reprocessing-event-streams]]
- [[deterministic-stream-processing]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[idempotence]]
- [[effectively-once-processing]]
- [[graphql]]
- [[webhooks]]
- [[source-systems]]
- [[data-sharing]]
