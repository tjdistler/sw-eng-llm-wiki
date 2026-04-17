# Building Event-Driven Microservices

**Summary**: Adam Bellemare's practitioner's guide to building, operating, and scaling microservices that communicate through durable event streams. Where most microservice books treat messaging as a detail, this book treats the event broker as the central nervous system of the organization — the single source of truth that services produce to, consume from, and are modelled around.

**Sources**: `raw/building-event-driven-microservices/`

**Last updated**: 2026-04-17

---

## About the book

*Building Event-Driven Microservices: Leveraging Organizational Data at Scale* (O'Reilly, 2020) by Adam Bellemare is organised around a simple thesis: in a world where every team needs access to the same data to do their job, the cheapest and most scalable way to share that data is to publish it as events on a durable log and let every team build its own derived view. The book uses Kafka as its reference broker throughout but the patterns are broker-agnostic.

The book stitches together four concerns that are usually covered separately:

1. **Organisational data architecture** — why [[communication-structures]] precede software structures; why the [[event-broker]] becomes the contract between teams; [[event-as-single-source-of-truth]] as the governing idea
2. **Stream-processing mechanics** — stateless vs stateful; deterministic processing of out-of-order data; the relationship between [[table-stream-duality|tables and streams]]
3. **Microservice implementation choices** — [[basic-producer-consumer-microservice|BPC]] vs [[heavyweight-framework-microservice|heavyweight]] vs [[lightweight-framework-microservice|lightweight]] vs [[functions-as-a-service|FaaS]] — with honest trade-offs for each
4. **The operational envelope** — tooling, testing, and deployment patterns that make event-driven microservices safe at organisational scale

The recurring payoff: the event broker is an *infrastructure-level* commitment. Once you make it, the rest of the book's patterns — [[data-liberation]], [[single-writer-principle]], [[schema-registry]], [[effectively-once-processing]], [[blue-green-deployment|blue-green]] rollouts — follow as natural consequences.

## Ingestion status

| Chapter | Title | Status |
|---|---|---|
| 1 | Why Event-Driven Microservices | Ingested 2026-04-17 |
| 2 | Event-Driven Microservice Fundamentals | Ingested 2026-04-17 |
| 3 | Communication and Data Contracts | Ingested 2026-04-17 |
| 4 | Integrating Event-Driven Architectures with Existing Systems | Ingested 2026-04-17 |
| 5 | Event-Driven Processing Basics | Ingested 2026-04-17 |
| 6 | Deterministic Stream Processing | Ingested 2026-04-17 |
| 7 | Stateful Streaming | Ingested 2026-04-17 |
| 8 | Building Workflows with Microservices | Ingested 2026-04-17 |
| 9 | Microservices Using Function-as-a-Service | Ingested 2026-04-17 |
| 10 | Basic Producer and Consumer Microservices | Ingested 2026-04-17 |
| 11 | Heavyweight Framework Microservices | Ingested 2026-04-17 |
| 12 | Lightweight Framework Microservices | Ingested 2026-04-17 |
| 13 | Integrating Event-Driven and Request-Response Microservices | Ingested 2026-04-17 |
| 14 | Supportive Tooling | Ingested 2026-04-17 |
| 15 | Testing Event-Driven Microservices | Ingested 2026-04-17 |
| 16 | Deploying Event-Driven Microservices | Ingested 2026-04-17 |
| 17 | Conclusion | Ingested 2026-04-17 |

## Foundations (Chapters 1–2)

The first two chapters establish what an event-driven microservice *is* and why it differs from a [[synchronous-microservices|synchronous microservice]]. Bellemare's framing: services talk through durable event streams rather than point-to-point RPC, and the [[event-broker]] becomes the organisation's load-bearing piece of infrastructure.

Hub pages:

- [[event-driven-microservices]] — the umbrella concept; the four properties (loose coupling, durable events, asynchronous processing, single source of truth)
- [[communication-structures]] — Bellemare's reframing of [[conways-law]]: business structure, implementation structure, and *data* communication structure as three independent layers
- [[microservice-topology]] and [[business-topology]] — how single services compose into a domain-aligned graph
- [[microservice-tax]] — the baseline operational cost of running a microservice; the threshold that makes or breaks the architecture
- [[container-management-system]] — Kubernetes and friends as the substrate that keeps the tax affordable

The event broker and the log:

- [[event-broker]] — the durable, partitioned, replayable log at the centre of the architecture
- [[event-structure]] — the anatomy of an event: key, value, timestamp, headers
- [[unkeyed-event]], [[keyed-event]], [[entity-event]] — the three event archetypes and when to use each
- [[table-stream-duality]] — Jay Kreps's observation that a changelog *is* a table; the foundation for every stateful pattern in the book
- [[tombstone]] — the null-value delete marker that makes log-based state usable
- [[log-compaction]] — retain the latest value per key; the mechanism that turns an infinite log into a snapshot
- [[consumer-offset]] and [[consumer-group]] — position tracking and horizontal scaling within a topic
- [[single-writer-principle]] — exactly one service owns writes to a given stream; the discipline that makes [[event-as-single-source-of-truth]] workable

## Communication and data contracts (Chapter 3)

Chapter 3 is where event-driven architecture meets the hard problem of inter-team coordination. Bellemare's stance: the schema on the broker is a public API, and must be treated with the same rigour as any other published contract.

- [[data-contract]] — the event stream as the inter-team contract
- [[schema-registry]] — Confluent-style centralised schema store; compatibility enforcement
- [[code-generation]] — generating producer/consumer types from the registry; how teams actually consume the contract
- [[explicit-vs-implicit-schemas]] — the cost of implicit JSON versus the up-front cost of Avro/Protobuf
- [[event-design-guidelines]] — the practical ruleset for what to put on the broker
- [[single-purpose-events]] — one event type per stream, one meaning per event
- [[singular-event-definition-per-stream]] — why polymorphic streams cause pain
- [[event-as-single-source-of-truth]] — the organisational commitment that makes the whole architecture cohere

## Integrating with existing systems (Chapter 4)

Most organisations cannot start greenfield. Chapter 4 is the pattern catalogue for getting data *out* of the monolithic databases and legacy systems that currently hold it.

- [[data-liberation]] — the hub concept; liberate data from silos and publish it to the broker
- [[query-based-cdc]] — polling with a timestamp column; the simplest (and flakiest) approach
- [[outbox-table-pattern]] — transactional outbox writes; [[change-data-capture|CDC]] reads the outbox, not the primary tables
- [[cdc-triggers]] — database triggers feeding a dedicated CDC table
- [[event-sinking]] — the reverse flow: materialising broker state back into a legacy system
- [[eventification]] — refactoring an existing service to publish domain events alongside (or instead of) its DB writes
- [[data-liberation-framework]] — Bellemare's generic framework combining the above with a [[schema-registry]] and monitoring

## Processing basics (Chapter 5)

Chapter 5 covers what services actually *do* with events once they arrive. This is the stateless half of stream processing; stateful work is deferred to Chapter 7.

- [[stateless-stream-processing]] — transformations, filters, routing; no memory between events
- [[event-transformations]] — map, filter, flatMap as the basic primitives
- [[stream-branching-and-merging]] — one input to many outputs; many inputs to one
- [[repartitioning]] — change the partitioning key; triggers a shuffle through the broker
- [[copartitioning]] — align two streams on the same key so joins can happen locally
- [[partition-assignor]] — how consumers in a group divide partitions among themselves

## Determinism (Chapter 6)

Chapter 6 addresses the subtlest problem in stream processing: producing the same answer twice from the same inputs, even when events arrive late or out of order. Without determinism, [[reprocessing-event-streams|reprocessing]] from the start of time produces different results than the original run — and most of the book's operational patterns depend on being able to reprocess.

- [[deterministic-stream-processing]] — the hub concept and why it matters
- [[event-timestamps]] — event time vs processing time; why timestamps are attached at produce time
- [[event-scheduling]] — choosing which event to process next across multiple partitions
- [[watermarks]] — the mechanism that lets you close a window despite uncertainty
- [[stream-time]] — the monotonic, data-driven clock that replaces wall-clock time
- [[out-of-order-events]] — the default, not the exception
- [[late-arriving-events]] — arriving after the watermark; handling policies
- [[reprocessing-event-streams]] — the operational payoff of determinism; rewind the offset, run again

## Stateful streaming (Chapter 7)

Chapter 7 is where stream processing becomes interesting. Real applications need aggregates, joins, and materialised views — which means keeping state across events, surviving restarts, and scaling horizontally.

- [[stateful-stream-processing]] — the umbrella; when statelessness is insufficient
- [[materialized-state]] — deriving a queryable view from an event stream; the read-side pattern
- [[state-store]] — the abstract concept of per-service state
- [[internal-state-store]] — an embedded KV store (RocksDB); fast but tied to the instance
- [[external-state-store]] — Cassandra, Redis, etc.; slower but independent of the compute
- [[global-state-store]] — every instance has a full copy; for small reference data
- [[changelog-stream]] — the state store's writes are themselves an event stream; the durability mechanism
- [[hot-replicas]] — standby instances with pre-warmed state; recovery without full replay
- [[state-store-rebuilding-vs-migrating]] — the operational decision during deployments
- [[effectively-once-processing]] — Bellemare's pragmatic alternative to "exactly once": idempotence plus transactional writes (see also [[exactly-once-semantics]])

## Workflows (Chapter 8)

Chapter 8 is short but important: how do you implement a multi-step business process in a world where every step is a separately deployed microservice?

- [[workflows-in-edm]] — choreography vs orchestration in an event-driven world
- [[compensation-workflow]] — the event-driven counterpart to the [[saga]]; undoing in-flight work when a step fails

## Microservice implementation styles (Chapters 9–12)

Chapters 9–12 form the book's pattern catalogue for the *implementation* of an event-driven microservice. Bellemare's core point: there is no single right answer. Each style has a niche, and large organisations usually run all four.

### FaaS (Chapter 9)

- [[functions-as-a-service]] — the hub; per-invocation, autoscaled compute
- [[event-stream-listener]] — the component that pulls events and dispatches them to the function
- [[faas-triggers]] — event-based, schedule-based, HTTP-based
- [[faas-offset-management]] — the subtle correctness problem unique to FaaS
- [[cold-start-warm-start]] — the latency tax and how to amortise it
- [[faas-batch-processing]] — amortise invocation overhead across many events
- [[faas-function-composition]] — chaining functions via streams; avoiding direct invocation

### Basic producer/consumer (Chapter 10)

- [[basic-producer-consumer-microservice]] — the simplest shape: a loop that consumes, processes, and produces
- [[gating-pattern]] — single-consumer coordination via an auxiliary stream; the event-driven lock
- [[hybrid-bpc-stream-processing]] — BPC plus a state store when you need both simplicity and memory

### Heavyweight frameworks (Chapter 11)

- [[heavyweight-framework-microservice]] — Spark Streaming, Flink, Storm; cluster-resident stream processing
- [[stream-processing-cluster]] — the shared compute substrate that services submit jobs to
- [[application-submission-modes]] — client-mode, cluster-mode, session-mode
- [[checkpointing-stream-processing]] — the framework's fault-tolerance mechanism
- [[external-shuffle-service]] — repartitioning that survives executor death
- [[stream-processing-scaling-strategies]] — horizontal, vertical, and partition-count trade-offs
- [[multitenancy-in-streaming-clusters]] — isolation, resource quotas, the noisy-neighbour problem

### Lightweight frameworks (Chapter 12)

- [[lightweight-framework-microservice]] — Kafka Streams, Samza; the library-not-cluster model
- [[broker-as-shuffle-service]] — the trick that lets a library do what a heavyweight cluster needs its own shuffle service for
- [[stream-table-table-join]] — the three-way join enabled by co-partitioning plus materialised state

## Request-response integration (Chapter 13)

Chapter 13 is the honest admission that event-driven is not the whole world. Users still hit HTTP endpoints; third-party APIs are still synchronous. Bellemare catalogues the patterns for bridging the two worlds.

- [[event-driven-request-response-integration]] — the hub page
- [[external-events-ingestion]] — turning incoming HTTP requests into events on the broker
- [[third-party-api-integration]] — calling out to synchronous services from within a stream processor
- [[serving-state-from-edm]] — how a stream processor exposes its materialised view to a HTTP-speaking client
- [[smart-load-balancer]] — routing read requests to the instance that holds the relevant partition's state
- [[request-as-event]] — encoding a synchronous request as a request/response pair on two streams
- [[asynchronous-ui]] — UIs that subscribe to events rather than poll
- [[micro-frontends]] — UI-level counterpart to microservices; an event-driven variant

## Supportive tooling (Chapter 14)

Chapter 14 is the operational reality check: the [[microservice-tax]] is only affordable if the platform team has built the right tooling.

- [[edm-supportive-tooling]] — the hub; an organisation's minimum viable platform
- [[microservice-to-team-assignment]] — the ownership registry; the prerequisite for on-call
- [[event-stream-metadata]] — owner, SLA, retention, compatibility policy per stream
- [[event-broker-quotas]] — per-team resource limits on the shared broker
- [[event-stream-acls]] — who can produce, who can consume
- [[schema-change-notifications]] — downstream consumers need to know *before* a breaking change lands
- [[application-reset-tool]] — reset offsets, wipe state, start over; the operational cousin of [[reprocessing-event-streams]]
- [[consumer-lag-monitoring]] — the single most important runtime health signal
- [[microservice-creation-workflow]] — the paved road that makes "spin up a new service" a 10-minute task
- [[cluster-creation-and-management]] — brokers, connect workers, processing clusters
- [[cross-cluster-replication]] — MirrorMaker and friends; geo-distribution and disaster recovery
- [[dependency-tracking-and-topology-visualization]] — who produces what, who consumes what
- [[data-lineage]] — end-to-end provenance; the audit and debugging story
- [[orphaned-streams]] — streams with no producer or no consumer; the counterpart to [[orphaned-services]]

## Testing (Chapter 15)

- [[unit-testing-topology-functions]] — testing individual transformations in isolation
- [[topology-testing]] — testing the full stream-processing graph without a real broker
- [[local-integration-testing]] — Testcontainers-style brokers run locally
- [[remote-integration-testing]] — shared test clusters; when local isn't enough
- [[hosted-service-mocks]] — wiremocks and service virtualisation for third-party calls
- [[test-data-strategies]] — production snapshots, synthetic data, property-based generation

## Deployment (Chapter 16)

Chapter 16 closes the book with the mechanics of rolling out event-driven microservices safely. The key twist: deployment is not just "swap the binary" — it interacts with partitions, state stores, and schema compatibility.

- [[edm-deployment-principles]] — the three principles: independent deployability, reproducibility, rollback-ability
- [[edm-deployment-patterns]] — the hub for the patterns below
- [[continuous-integration-delivery-deployment]] — the CI/CD spine; tests, schema checks, canaries
- [[basic-full-stop-deployment]] — the simplest pattern; acceptable downtime
- [[rolling-update-pattern]] — partition-by-partition rollover; state-store considerations
- [[blue-green-deployment]] — two full copies; offset cutover; the safest pattern when state is involved
- [[breaking-schema-deployment]] — the multi-stage dance required when a schema must change incompatibly

## Related pages

- [[event-driven-microservices]]
- [[event-broker]]
- [[communication-structures]]
- [[single-writer-principle]]
- [[event-as-single-source-of-truth]]
- [[table-stream-duality]]
- [[log-compaction]]
- [[data-contract]]
- [[schema-registry]]
- [[event-design-guidelines]]
- [[data-liberation]]
- [[outbox-table-pattern]]
- [[change-data-capture]]
- [[stateless-stream-processing]]
- [[stateful-stream-processing]]
- [[deterministic-stream-processing]]
- [[reprocessing-event-streams]]
- [[materialized-state]]
- [[effectively-once-processing]]
- [[workflows-in-edm]]
- [[compensation-workflow]]
- [[functions-as-a-service]]
- [[basic-producer-consumer-microservice]]
- [[heavyweight-framework-microservice]]
- [[lightweight-framework-microservice]]
- [[event-driven-request-response-integration]]
- [[edm-supportive-tooling]]
- [[consumer-lag-monitoring]]
- [[edm-deployment-principles]]
- [[blue-green-deployment]]
- [[breaking-schema-deployment]]
