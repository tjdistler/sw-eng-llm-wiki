# External State Store

**Summary**: A [[state-store]] that **lives outside the microservice's container** — a separate, network-accessible data service. External stores trade the raw throughput and operational simplicity of an [[internal-state-store]] for query flexibility, elastic cost, and access to a tech stack the team already understands. Each microservice owns its own logically-isolated dataset, even when that dataset sits on a shared database cluster.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`, `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Shape

The external store is any networked data service the team chooses: RDBMS, document DB, Lucene-backed geospatial search, distributed KV, or a hosted cloud database (source: chapter-07-stateful-streaming.md). Each microservice *instance* still consumes its own assigned partitions and writes through to the shared external store.

The shared-tech part is where teams get into trouble. Bellemare's rule: even if the underlying technology is shared, **the data set must remain logically isolated** per service. Sharing a materialized dataset across microservices is an anti-pattern that reintroduces all the coupling EDM exists to eliminate (source: chapter-07-stateful-streaming.md). See also [[shared-database-antipattern]].

## Advantages

**Full data locality.** Because every instance sees all the data, cross-partition queries — foreign-key joins, geospatial range queries, full-text search across the whole set — become trivial. Internal state stores can't do this without [[global-state-store|global materialization]] (source: chapter-07-stateful-streaming.md).

**Read-after-write strong consistency is available** via most RDBMS and many modern distributed databases. This eliminates one class of multi-instance anomaly that internal stores can't easily address (source: chapter-07-stateful-streaming.md).

**Use what the org already knows.** A team fluent in PostgreSQL can reach production faster if its microservice's state store is PostgreSQL. Basic producer/consumer patterns (Chapter 10) and [[functions-as-a-service|Function-as-a-Service]] solutions (Chapter 9) are especially good fits for external stores (source: chapter-07-stateful-streaming.md).

## Drawbacks

**Management of multiple technologies.** Each team running an external store must handle its own resource allocation, scaling policies, monitoring, and backup strategies. Bellemare's guidance: the platform team should curate "a list of acceptable external data services with guides on how to properly manage and scale them," rather than letting each team rediscover the same operational lessons (source: chapter-07-stateful-streaming.md). **Do not** delegate store operation to a separate team — that reintroduces the cross-team technical dependency microservices were meant to kill.

**Network latency.** Every lookup is a network hop. Caching and parallelization can help, but many stream-processing patterns require the processing thread to block on the reply — there is no parallelism to exploit (source: chapter-07-stateful-streaming.md). The 1 ms → 16x-throughput-loss math from [[internal-state-store]] applies here with full force.

**Financial cost.** Hosted external state stores charge by transactions, data size, and retention. Bursty workloads may require over-provisioning. Internal state on local disk is typically cheaper per byte at steady state (source: chapter-07-stateful-streaming.md).

**Full data locality is also a hazard.** Since the shared dataset is written to by multiple instances that each have their own [[stream-time|stream time]], race conditions and nondeterminism creep in. "One instance may attempt to join an event on a foreign key that has not yet been populated by a separate instance. Reprocessing the same data at a later time may execute the join" — producing different results on replay (source: chapter-07-stateful-streaming.md). Reasoning about any single instance's contribution to the collective state is hard.

## Recovery options

External-store recovery is not one-size-fits-all; the chapter identifies three generalizable techniques (source: chapter-07-stateful-streaming.md):

- **From the source streams.** Reset consumer offsets to 0 and rebuild the whole store from scratch. Longest downtime; reproduces any output events the service is supposed to emit. The full-reset option.
- **From a changelog.** External stores *can* use broker changelogs, though it's less common. Same shape as internal-store recovery, but slower — every changelog event lands behind a network hop.
- **From snapshots.** The most common choice. Many hosted DBs provide one-click backup/restore. If state is idempotent, set consumer offsets to a few minutes before the snapshot was taken (at-least-once). If not idempotent, store consumer offsets *inside the snapshot* alongside the data so offsets and state commit together.

Bellemare's warning: rebuilding a large external store from the broker can be prohibitively slow due to network latency — verify SLA feasibility before committing to this strategy.

## Serving reads over a request-response API

Because every instance can see the whole dataset, exposing a synchronous read API is straightforward — no [[smart-load-balancer]] or in-service redirect is needed (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Two deployment shapes:

- **All-in-one microservice** — one binary processes events, materializes state, and serves the API. Simplest to deploy. Instance count can exceed partition count; extra instances serve requests and act as failover capacity.
- **Separate event-processor and API microservices** — split into two deployables within the same bounded context, sharing the external store. Lets you pick different stacks per concern and isolates processing failures from serving. Cost: more deployment coordination and a soft violation of the "single deployable per bounded context" principle.

See [[serving-state-from-edm]] for the full discussion.

## Consistency via offsets-in-the-data-store

When exactly-once semantics matter and the broker doesn't offer transactions, a powerful trick is to **move offset management into the external state store itself**, atomically updating state and offsets in one local transaction. See [[effectively-once-processing]] for the mechanics.

This gives effectively-once *processing* but not effectively-once *production* — output events still follow at-least-once semantics unless paired with an [[outbox-table-pattern]] or a broker-level transaction.

## Related pages

- [[state-store]]
- [[internal-state-store]]
- [[global-state-store]]
- [[stateful-stream-processing]]
- [[effectively-once-processing]]
- [[outbox-table-pattern]]
- [[shared-database-antipattern]]
- [[functions-as-a-service]]
- [[changelog-stream]]
- [[stream-time]]
- [[serving-state-from-edm]]
