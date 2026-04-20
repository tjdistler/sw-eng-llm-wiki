# MOC: Events and Streaming

**Summary**: Entry point for questions about *using events as the integration substrate between services* — brokers as the load-bearing infrastructure, event design and contracts, the data-liberation pattern that feeds the broker from legacy systems, choreography vs orchestration, sagas in their event-driven form, outbox as publication mechanism, event-driven microservices end to end, and the supportive tooling that keeps an event-first architecture liveable. Start here when the question is "how should these services talk via events?" rather than "how do I tune this stream processor?" (that's [[moc-data-processing]]) or "what correctness guarantee does this give me?" (that's [[moc-consistency-and-transactions]]).

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You're designing how a system communicates, and events are (or might be) the substrate. Maybe the team is picking between request-response and async pub/sub. Maybe you've adopted Kafka and now need to figure out event shape, ownership, and schema evolution. Maybe the workflow is "order placed → payment → inventory → shipping" and you're staring at a whiteboard deciding whether to orchestrate or choreograph it.

The canonical shape of a question that lands here: *"Should this be a synchronous call or an event?"*, *"How do I model this event — as a fact, a command, or an entity snapshot?"*, *"Orchestration or choreography for this workflow?"*, *"How do we publish events atomically with our database writes?"*, *"How does the request-response UI read state that's built from streams?"*, *"We're adopting EDM — what tooling do we actually need before we can call it production?"*

Jurisdictional rule for this MOC:

- **This MOC** owns events as *architectural integration substrate*. Brokers, topologies (broker vs mediator; choreography vs orchestration), event design, data contracts, data liberation from legacy stores, event-driven microservice architecture end-to-end, outbox as publication, and the platform tooling around all of it.
- [[moc-data-processing]] owns *execution mechanics* of stream processing — batch vs stream engines, windows, watermarks, stateful-streaming internals, checkpointing, CDC as source-capture. This MOC cites [[stream-processing]], [[log-based-message-brokers]], and [[change-data-capture]] under an *architectural integration* lens; the processing MOC owns them under an *execution mechanics* lens.
- [[moc-consistency-and-transactions]] owns *correctness-across-stores* — the saga taxonomy, compensations, outbox-as-correctness-bridge. This MOC cites [[saga]] and [[outbox-table-pattern]] under a *publication and integration* lens; the consistency MOC owns them under a *correctness bridge* lens. Expect to land on both for any non-trivial event-driven workflow question.
- [[moc-distributed-systems]] owns the *mechanisms* a broker and its clients are built on — replication, partitioning, consensus. This MOC treats those as given; that MOC owns what they cost and how they fail.
- [[moc-microservices]] owns the *organisational frame* around event-driven services — single-writer principle as a team discipline, service boundaries, reuse patterns. This MOC owns the communication substrate; that MOC owns how the team lives with it.

Shared pages (CDC, Kafka / log-based brokers, outbox, saga, single-writer principle) are linked here with a framing sentence about their *architectural-integration* lens. Follow the sibling MOCs for the other lenses.

## Request-based vs event-based — the framing

The decision to use events as the primary integration pattern is load-bearing. Start with the frame.

- [[event-driven-architecture]] — Richards and Ford's Ch 14 treatment of event-driven as an *architecture style*. Five-star on performance, scalability, elasticity, fault tolerance; weak on simplicity and testability. The canonical reference for the request-based vs event-based distinction and for the two topologies below.
- [[event-driven-microservices]] — Bellemare's four properties: loose coupling, durable events, asynchronous processing, single source of truth. The practitioner's framing — what an EDM is and how it differs from a synchronous-microservice fleet or a traditional ESB.
- [[synchronous-microservices]] — the baseline EDM contrasts against. The coupling and availability costs of request-response as the *only* communication pattern. Worth reading to understand *what* events buy you.
- [[serverless-vs-event-driven]] — Burns's clarification: serverless and event-driven are independent axes. FaaS combines both; products exist on each axis independently; know which benefit you actually want.
- [[communication-structures]] — Bellemare's reframing of [[conways-law]] in the EDM context. Business, implementation, and *data* communication structures as three layers that can be evolved independently. The organisational theory under EDM's longevity argument.
- [[event-as-single-source-of-truth]] — the organisational commitment that makes the architecture cohere. Without it, the broker is just another message queue.

Deeper reading: [[fundamentals-of-software-architecture#chapter-14-event-driven-architecture-style]] for the style-catalogue framing; [[building-event-driven-microservices#chapter-1-why-event-driven-microservices]] for the practitioner framing.

## The broker — event-driven infrastructure

The broker is the most load-bearing piece of infrastructure in an event-driven stack. Pick it, operate it, and treat its schema as a public contract.

- [[event-broker]] — Bellemare's name for the durable, partitioned, replayable log-based broker at the centre of an EDM platform. Kafka is the canonical example; Pulsar is the common alternative. Scale, durability, availability, performance properties.
- [[log-based-message-brokers]] — the DDIA framing: partitioned append-only logs with consumer offsets, replay, and multi-consumer fan-out. Read this page for the mechanism; read [[event-broker]] for the architectural stance built on top.
- [[message-brokers]] — the broader family. Traditional brokers (RabbitMQ, ActiveMQ) *don't* retain events; log-based brokers do. Bellemare's argument: the distinction matters, because EDM's consumer-independence and replay properties depend on retention.
- [[event-streams]] — what events are; producers, consumers, topics; delivery mechanisms. The primitive all the patterns below build on.
- [[broker-topology]] — Richards and Ford Ch 14's no-central-mediator shape: events flow peer-to-peer through the broker, processors advertise what they did, others react if interested. The choreographed shape.
- [[mediator-topology]] — Ch 14's central-mediator shape: a workflow coordinator accepts the initiating event and issues commands to processors. The orchestrated shape. Better control and error handling; lower throughput; mediator as scaling bottleneck.

The first decision in any event-driven design is where on the broker-vs-mediator axis each workflow sits. Expect "mostly broker, with mediator pockets for the critical workflows that need central tracking" in mature systems.

Deeper reading: [[fundamentals-of-software-architecture#chapter-14-event-driven-architecture-style]]; [[building-event-driven-microservices#chapter-2-event-driven-microservice-fundamentals]].

## Event design and contracts

The event on the broker is a public API. Treat it with at least as much rigour as a REST contract; prefer more.

### Event shape and types

- [[event-structure]] — key + value + metadata + timestamp. The envelope every event is a specialisation of.
- [[unkeyed-event]] — no key; for append-only facts that need no co-location; round-robin partitioned. The simplest shape; useful for logging, metrics, and pure-fact streams.
- [[keyed-event]] — key but no full-entity snapshot; co-location and partial updates. The shape for most transactional streams.
- [[entity-event]] — key plus full entity state in every event; the compacted-stream payload. The shape that enables [[log-compaction]] to serve the stream as a durable key-value store. Favoured wherever downstream consumers need "current state of entity X" as a simple stream-read.
- [[tombstone]] — null-valued event signalling deletion; how entity streams represent "gone" under compaction.
- [[log-compaction]] — broker-side retention by key. Keep the latest value per key forever. The mechanism that turns an infinite log into a durable snapshot; prerequisite for entity streams as a source of truth.
- [[table-stream-duality]] — Kreps's observation: every stream implies a table (the result of replaying it through a fold), every table implies a stream (its changelog). The theoretical core; once you internalise it, most event-driven design decisions become obvious.
- [[single-writer-principle]] — one service, one stream. The write-ownership rule that keeps event sources unambiguous and compacted streams durable. Here under the architectural/integration lens; [[moc-microservices]] owns the organisational lens.

### Contracts and schema

- [[data-contract]] — the event stream as an inter-team contract. Treat schema changes with the rigour of API versioning. The discipline that separates EDM-that-works from EDM-that-becomes-a-swamp.
- [[schema-registry]] — Confluent-style centralised schema store; compatibility enforcement (backward, forward, full). The broker's "schema gate" that stops incompatible producers from shipping.
- [[schema-evolution]] — backward, forward, and full compatibility. What a schema change actually means to producers, consumers, and downstream state stores.
- [[explicit-vs-implicit-schemas]] — Avro/Protobuf/Thrift (explicit) vs JSON (implicit). The up-front cost of explicit schemas pays back in every downstream consumer that ever has to parse the stream.
- [[avro]] — the specific encoding Kafka+Registry defaults to.
- [[protocol-buffers]] — Google's comparable binary schema; appears in gRPC, internal Google storage, and cross-company contract flows.
- [[code-generation]] — generating producer/consumer types from the registry; how teams actually consume the contract in practice.
- [[event-design-guidelines]] — Bellemare's practical ruleset for what to put on the broker. One event type per stream. Meaning before mechanism. No implicit schemas. Etc.
- [[single-purpose-events]] — one event type per stream, one meaning per event. The rule that keeps downstream consumers simple.
- [[singular-event-definition-per-stream]] — why polymorphic streams cause pain. The "order-event" stream that carries Created, Updated, and Deleted events in one topic becomes the thing every consumer has to special-case forever.
- [[consumer-driven-contracts]] — Pact-style consumer-written specifications. The testing discipline that pairs with schema registry for cross-service contract integrity.

Deeper reading: [[building-event-driven-microservices#chapter-3-communication-and-data-contracts]].

## Data liberation — feeding the broker from legacy systems

Most organisations don't start greenfield. The data they need on the broker currently lives in monolithic OLTP databases, SaaS products, and legacy services. *Data liberation* is the discipline of getting it out.

- [[data-liberation]] — Bellemare's framing: extract data from siloed systems into event streams so downstream consumers (EDM, lakes, warehouses) can use it. The umbrella concept under the techniques below.
- [[data-liberation-framework]] — the organisational capability and tooling for sustained liberation across many sources. Schema registry, monitoring, per-source instrumentation.
- [[eventification]] — the act of turning a request-response API or legacy data source into a first-class stream. The umbrella above CDC when the source isn't a database.

CDC — the same mechanism as in [[moc-data-processing]], here under its *integration substrate* lens:

- [[change-data-capture]] — making one database the leader for all derived systems via binlog/WAL parsing. The mechanism behind every modern data-integration pipeline that isn't a nightly snapshot. In this MOC, CDC is the bridge that lets the event-driven stack consume events sourced from a database the EDM team doesn't own.
- [[query-based-cdc]] — periodic polling of timestamp columns. Simple but lossy; load-bearing on the database; the form most teams should leave behind once the broker is in place.
- [[cdc-triggers]] — trigger-based CDC inserting into a change table. Precise but intrusive; DBAs refuse on principle; occasionally worth the principle-violation.
- [[outbox-table-pattern]] — atomic write of business state plus a pending-event row; a poller streams it out. The CDC variant that emits *application semantics* rather than raw row events. **The single most load-bearing pattern in event-driven architecture** — it's what makes the "write to DB and publish event" dual-write problem disappear without requiring 2PC. Here under the *publication pattern* lens; [[moc-consistency-and-transactions]] owns the *correctness bridge* lens; [[moc-data-processing]] owns the *source-capture* lens.

The reverse direction — getting events back into legacy systems:

- [[event-sinking]] — writing events back into downstream databases for query. Reverse ETL at event-driven granularity.

Deeper reading: [[building-event-driven-microservices#chapter-4-integrating-event-driven-architectures-with-existing-systems]] is the full treatment and the single most referenced chapter in any EDM migration.

## Choreography vs orchestration — the coordination axis

Once services talk via events, the coordination question is how a multi-step workflow is composed across them. This is the same axis the [[saga]] family splits on; the terminology converges across books.

- [[choreography]] — no central coordinator; services react to events and emit their own. Peer-to-peer; flexible; scalable; hard to track overall progress.
- [[workflow-choreography]] — Hard Parts Ch 11 framing of the same thing.
- [[orchestration]] — central coordinator sequencing the workflow; easy to observe and debug; mediator is the scaling bottleneck. Called [[mediator-topology]] in the EDA style context and [[workflow-orchestration]] in the Hard Parts framing.
- [[workflow-orchestration]] — Hard Parts Ch 11 framing.
- [[distributed-workflow-patterns]] — the Hard Parts four-force rubric for picking between them (workflow control, error handling, observability, state tracking).
- [[workflows-in-edm]] — Bellemare's Chapter 8 framing: how event-driven microservices actually implement workflows.

The full saga taxonomy — follow the sibling MOC for the correctness depth:

- [[saga]] — the pattern hub; the main alternative to 2PC; compensations instead of locks. Follow [[moc-consistency-and-transactions]] end-to-end for the saga family in depth; this MOC links it under the "what shape is this event-driven workflow?" lens.
- [[anthology-saga]] — `async + eventual + choreographed`. **The native form of event-driven architecture.** Most mature EDM fleets converge here. If you're on any other Hard Parts saga corner in an EDM system, have a clear reason.
- [[parallel-saga]] — `async + eventual + orchestrated`. The mediator-topology EDM variant; common when a workflow needs state tracking.
- [[compensation-workflow]] — Bellemare's event-driven compensation pattern: failures emit explicit failure events; downstream services consume and reverse their state. The event-native version of [[compensating-update|compensating transactions]].

Deeper reading: [[building-event-driven-microservices#chapter-8-building-workflows-with-microservices]]; [[fundamentals-of-software-architecture#chapter-14-event-driven-architecture-style]] for the broker-vs-mediator framing.

## EDM implementation styles

Bellemare's catalogue of how an event-driven microservice actually gets built. Each has a niche; large organisations usually run all four.

- [[basic-producer-consumer-microservice]] — the simplest shape: consume, process per event, produce. No framework. The default starting point.
- [[gating-pattern]] — a guard consumer that admits events to a downstream stream only when a condition is met. The event-driven "lock."
- [[hybrid-bpc-stream-processing]] — BPC plus a state store. The common next step up from pure BPC when you need a small aggregate or join.
- [[functions-as-a-service]] — FaaS as an EDM implementation. Per-invocation, autoscaled compute. Event-driven by design; covered in depth in [[moc-container-and-serving-patterns]].
- [[faas-triggers]] — event-based, schedule-based, HTTP-based triggers.
- [[faas-offset-management]] — the subtle correctness problem unique to FaaS consumers of a log-based broker.
- [[event-stream-listener]] — the component pulling events and dispatching to the function.
- [[heavyweight-framework-microservice]] — Flink/Spark-style stream processors; cluster-resident; heavy state and checkpointing. Mechanics owned by [[moc-data-processing]].
- [[lightweight-framework-microservice]] — Kafka-Streams-style: library embedded in the service; broker handles shuffle via repartition topics. Bellemare's preferred shape for most stateful-streaming work.
- [[broker-as-shuffle-service]] — the trick behind lightweight frameworks: use the broker's partitioning for repartitioning between stream-processing steps.

## Integrating EDM with request-response — the UI and external APIs

EDM is rarely the whole world. Users still hit HTTP endpoints; third-party APIs are still synchronous. Chapter 13 of Bellemare's book is the honest admission plus the pattern catalogue.

- [[event-driven-request-response-integration]] — the hub: how synchronous clients, external APIs, and UIs plug into an event-driven backbone.
- [[external-events-ingestion]] — accepting events from outside the organisation (webhooks, partner feeds); validation and trust boundaries.
- [[webhooks]] — reverse APIs: the source pushes to the consumer's endpoint. The ingestion mechanism for most SaaS integrations.
- [[third-party-api-integration]] — wrapping external synchronous APIs so the EDM sees events instead of RPC.
- [[serving-state-from-edm]] — exposing read APIs backed by materialised state built from streams. The pattern behind "the UI reads state derived from the event log."
- [[smart-load-balancer]] — partition-aware routing sending requests to the instance already hosting the relevant state. The infrastructure that makes "serving state from EDM" fast.
- [[request-as-event]] — modelling a synchronous request as an event with a reply-to stream; turning RPC into async.
- [[asynchronous-ui]] — UIs that display eventual-consistency state and subscribe to events rather than poll.
- [[micro-frontends]] — UI-level counterpart to microservices; event-driven variant.

Deeper reading: [[building-event-driven-microservices#chapter-13-integrating-event-driven-and-request-response-microservices]].

## Supportive tooling — the platform tax EDM pays to stay liveable

The [[microservice-tax]] is only affordable if the platform team has built the right tooling around the broker. Chapter 14 is the minimum-viable-platform checklist.

- [[edm-supportive-tooling]] — the hub: the platform services every mature EDM org builds around its broker.
- [[microservice-to-team-assignment]] — the registry mapping services and streams to owning teams. The on-call prerequisite.
- [[event-stream-metadata]] — per-stream documentation: owner, schema, retention, purpose, SLAs.
- [[event-broker-quotas]] — per-client throughput and storage limits; noisy-neighbour defence at the broker.
- [[event-stream-acls]] — who can produce to and consume from each stream; authorisation at the broker.
- [[schema-change-notifications]] — alerting downstream consumers *before* an upstream schema break lands.
- [[application-reset-tool]] — operational tooling to wipe state and rewind offsets so a service can reprocess from scratch. The operational cousin of [[reprocessing-event-streams]].
- [[consumer-lag-monitoring]] — tracking how far behind each consumer group is. The single most important EDM runtime health metric.
- [[microservice-creation-workflow]] — the paved road: scaffolding, repo, CI/CD, topic ACLs, dashboards created in one step.
- [[cluster-creation-and-management]] — provisioning and operating broker clusters.
- [[cross-cluster-replication]] — MirrorMaker-style replication across regions; DR and data-locality.
- [[dependency-tracking-and-topology-visualization]] — tools rendering the live graph of streams and services.
- [[data-lineage]] — end-to-end tracking of how an event flows from source to every derived dataset.
- [[orphaned-streams]] — streams with no active consumers. The EDM analogue of dead code. Part of the platform team's regular audit.

Deeper reading: [[building-event-driven-microservices#chapter-14-supportive-tooling]].

## Testing EDM

Testing event-driven systems breaks a lot of instincts from synchronous testing. Bellemare's tiered approach:

- [[unit-testing-topology-functions]] — testing pure per-event functions in isolation; the fastest tier.
- [[topology-testing]] — driving a whole processor topology with fixtures in-process; verifying emitted events.
- [[local-integration-testing]] — running a real broker locally (Testcontainers); asserting end-to-end behaviour.
- [[remote-integration-testing]] — running against a shared remote staging; per-test isolation via topic namespacing.
- [[hosted-service-mocks]] — fake implementations of third-party APIs you integrate with.
- [[test-data-strategies]] — synthetic, sampled, captured-from-prod fixtures; privacy and reproducibility.

Deeper reading: [[building-event-driven-microservices#chapter-15-testing-event-driven-microservices]].

## Deploying EDM

Deploying an event-driven service is different from deploying a REST service. Schema compatibility and consumer-group rebalances dominate the concerns.

- [[edm-deployment-principles]] — the ground rules: reversibility, compatibility, observability, blast-radius control.
- [[edm-deployment-patterns]] — the canonical deployment patterns and when each applies.
- [[continuous-integration-delivery-deployment]] — CI/CD pipeline shape for EDM services; schema checks and topic provisioning.
- [[basic-full-stop-deployment]] — stop all instances, deploy, start. Simplest and most disruptive.
- [[rolling-update-pattern]] — replace instances one-by-one while consumer-group rebalance handles partition handoff. The usual default.
- [[blue-green-deployment]] — two full parallel deployments with traffic cutover; safe rollback at the cost of double capacity.
- [[breaking-schema-deployment]] — coordinating a producer-consumer schema break across the fleet; dual-write and dual-read phases. The only pattern that handles an incompatible schema change cleanly.

Deeper reading: [[building-event-driven-microservices#chapter-16-deploying-event-driven-microservices]].

## Patterns in nearby architectures — FaaS event pipelines and event-driven batch

Event-driven ideas appear in adjacent architectures too. These connect, especially when a team is picking between FaaS event pipelines, event-driven microservices, and batch workflows.

- [[event-pipeline-pattern]] — Burns Ch 8: directed graph of functions connected by webhooks. FaaS-granularity event-driven; non-software participants (humans, external SaaS) compose naturally.
- [[faas-decorator-pattern]] — Burns Ch 8: request/response transformation in front of a backend; the adapter-vs-FaaS-decorator decision.
- [[event-driven-batch-pattern]] — Burns Ch 11: chains [[work-queue-pattern]] instances into DAGs via named linking patterns (copier, filter, splitter, sharder, merger). Pub/sub as transport. Batch granularity of the same idea.
- [[publisher-subscriber-infrastructure]] — Burns Ch 11's transport substrate; Kafka/EventGrid/SQS as interchangeable implementations.

Deeper reading: [[designing-distributed-systems#chapter-8-functions-and-event-driven-processing]]; [[designing-distributed-systems#chapter-11-event-driven-batch-processing]].

## Sibling MOCs

- [[moc-data-processing]] — owns execution mechanics of stream processing (engines, windows, watermarks, stateful-streaming internals). This MOC shares [[change-data-capture]], [[log-based-message-brokers]], [[outbox-table-pattern]], [[single-writer-principle]], [[reprocessing-event-streams]] with that one. Split responsibilities: this MOC owns the *architectural integration* lens; the processing MOC owns the *execution mechanics* lens.
- [[moc-consistency-and-transactions]] — owns the full saga taxonomy and outbox-as-correctness-bridge. This MOC shares [[saga]], [[outbox-table-pattern]], [[compensation-workflow]], [[workflow-orchestration]], [[workflow-choreography]], and the eight Hard Parts saga variants with that one. Split responsibilities: this MOC owns the *publication and integration* lens; the consistency MOC owns the *correctness across stores* lens. For any non-trivial event-driven workflow question, expect to land on both.
- [[moc-distributed-systems]] — owns replication, partitioning, and consensus as the primitives a log-based broker is built on. This MOC treats them as given; that MOC owns what they cost.
- [[moc-microservices]] — owns the organisational frame around event-driven services. Single-writer principle, service boundaries, reuse, the platform tax. This MOC owns the substrate; that MOC owns how the team lives with it.
- [[moc-architecture-styles]] — owns the style-catalogue placement of event-driven architecture and the comparison against layered, microservices, space-based, pipeline, and service-based. This MOC goes deeper on the style.
- [[moc-container-and-serving-patterns]] — owns FaaS as a serving pattern. This MOC cites FaaS as an EDM implementation style; the container MOC owns the FaaS pattern's depth.

## Related pages

- [[index]]
- [[building-event-driven-microservices]]
- [[fundamentals-of-software-architecture]]
- [[designing-data-intensive-applications]]
- [[event-driven-architecture]]
- [[event-driven-microservices]]
- [[event-broker]]
- [[log-based-message-brokers]]
- [[message-brokers]]
- [[event-streams]]
- [[broker-topology]]
- [[mediator-topology]]
- [[event-structure]]
- [[entity-event]]
- [[log-compaction]]
- [[table-stream-duality]]
- [[single-writer-principle]]
- [[data-contract]]
- [[schema-registry]]
- [[schema-evolution]]
- [[event-design-guidelines]]
- [[data-liberation]]
- [[change-data-capture]]
- [[outbox-table-pattern]]
- [[eventification]]
- [[saga]]
- [[anthology-saga]]
- [[compensation-workflow]]
- [[choreography]]
- [[workflow-orchestration]]
- [[workflows-in-edm]]
- [[basic-producer-consumer-microservice]]
- [[lightweight-framework-microservice]]
- [[event-driven-request-response-integration]]
- [[serving-state-from-edm]]
- [[edm-supportive-tooling]]
- [[consumer-lag-monitoring]]
- [[edm-deployment-patterns]]
- [[event-pipeline-pattern]]
- [[event-driven-batch-pattern]]
