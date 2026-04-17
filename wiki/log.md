# Wiki Log

Append-only record of all operations.

---

## 2026-04-17 — Building Event-Driven Microservices, Chapter 1
- Created: [[event-driven-microservices]], [[communication-structures]], [[synchronous-microservices]]
- Updated: [[conways-law]] (added Bellemare's three-substructure refinement), [[domain-driven-design]] (added Bellemare's concise domain/subdomain/model/bounded-context definitions), [[bounded-context]] (added business-vs-technical alignment section with Bellemare's tip), [[event-streams]] (added events-are-the-data, single-source-of-truth, consumer-does-own-modeling framings), [[coupling]] (added coupling-on-domain-data-not-APIs section)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 2
- Created: [[microservice-topology]], [[business-topology]], [[event-structure]], [[unkeyed-event]], [[entity-event]], [[keyed-event]], [[table-stream-duality]], [[tombstone]], [[log-compaction]], [[event-broker]], [[single-writer-principle]], [[consumer-offset]], [[consumer-group]], [[microservice-tax]], [[container-management-system]]
- Updated: [[event-driven-microservices]] (added Chapter 2 producer/consumer framing, two-topologies section, events-and-state section, single-writer principle, platform-and-tax section), [[event-streams]] (added event-broker storage requirements, three event types), [[message-brokers]] (added Bellemare's event-broker vs message-broker comparison), [[log-based-message-brokers]] (added EDM-substrate framing with consumer groups, lag, queue-mode consumption)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 3
- Created: [[data-contract]], [[explicit-vs-implicit-schemas]], [[schema-registry]], [[code-generation]], [[event-design-guidelines]], [[single-purpose-events]], [[singular-event-definition-per-stream]], [[event-as-single-source-of-truth]]
- Updated: [[schema-evolution]] (added Bellemare's forward/backward/full compatibility types, full-compatibility default, EDM framing), [[backward-forward-compatibility]] (added full-compatibility as EDM default, JSON caveat), [[breaking-changes]] (added Bellemare's entity-vs-event accommodation strategies, communicate-early rule), [[encoding-formats]] (added EDM format selection with Avro/Thrift/Protobuf recommendation and JSON discouragement), [[event-structure]] (added schema-definition-comments and narrowest-data-types guidance)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 4
- Created: [[data-liberation]], [[query-based-cdc]], [[outbox-table-pattern]], [[cdc-triggers]], [[event-sinking]], [[eventification]], [[data-liberation-framework]]
- Updated: [[change-data-capture]] (added Bellemare's three-pattern taxonomy, log-based benefits/drawbacks, bootstrapping, Debezium/Maxwell tooling, bootstrap-not-destination warning), [[event-as-single-source-of-truth]] (added publish-first vs unidirectional-liberation compromise for legacy integration)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 5
- Created: [[stateless-stream-processing]], [[event-transformations]], [[stream-branching-and-merging]], [[repartitioning]], [[copartitioning]], [[partition-assignor]]
- Updated: [[microservice-topology]] (added Chapter 5 stateless-case elaboration and links to transformations/branching/repartitioning/copartitioning), [[consumer-group]] (added partition-assignor mechanics, reassignment suspension, and copartitioning-constraint references)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 6
- Created: [[deterministic-stream-processing]], [[event-timestamps]], [[event-scheduling]], [[watermarks]], [[stream-time]], [[out-of-order-events]], [[late-arriving-events]], [[reprocessing-event-streams]]
- Updated: [[windowing]] (added Bellemare's tumbling/sliding/session framing, event-time-preferred guidance, late-event policy dependency, links to watermarks/stream-time/reprocessing)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 7
- Created: [[stateful-stream-processing]], [[materialized-state]], [[state-store]], [[internal-state-store]], [[external-state-store]], [[global-state-store]], [[changelog-stream]], [[hot-replicas]], [[state-store-rebuilding-vs-migrating]], [[effectively-once-processing]]
- Updated: [[stateless-stream-processing]] (linked to stateful counterpart), [[table-stream-duality]] (linked to state-store/changelog pages), [[stream-processing-fault-tolerance]] (added BEDM framing section with effectively-once terminology, changelog, hot replicas, client-broker transactions), [[idempotence]] (added BEDM dedup-ID treatment)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 8
- Created: [[workflows-in-edm]], [[compensation-workflow]]
- Updated: [[saga]] (added Bellemare EDM framing — idempotence for forward and reverse actions, single-writer asymmetry in choreographed sagas, orchestrator signals beyond success/failure, compensation-as-third-option), [[distributed-transactions]] (added Bellemare avoid-or-compensate perspective), [[event-driven-microservices]] (added composing-services-into-workflows section linking to workflows-in-edm and compensation-workflow)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 9
- Created: [[event-stream-listener]], [[faas-triggers]], [[faas-offset-management]], [[cold-start-warm-start]], [[faas-batch-processing]], [[faas-function-composition]]
- Updated: [[functions-as-a-service]] (added Bellemare EDM framing — four-component model, design disciplines, provider choice with 7-day broker retention caveat, trigger/batch/composition links, EDM fit criteria), [[workflows-in-edm]] (added FaaS realization note mapping event-driven and direct-call orchestration onto Chapter 9 function-composition patterns)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 10
- Created: [[basic-producer-consumer-microservice]], [[gating-pattern]], [[hybrid-bpc-stream-processing]]
- Updated: [[sidecar-pattern]] (added EDM framing — BPC sidecar upserting event-stream data into a legacy frontend's data store, same single-deployable discipline as Burns), [[event-driven-microservices]] (linked new BPC/gating/hybrid pages)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 11
- Created: [[heavyweight-framework-microservice]], [[stream-processing-cluster]], [[application-submission-modes]], [[checkpointing-stream-processing]], [[external-shuffle-service]], [[stream-processing-scaling-strategies]], [[multitenancy-in-streaming-clusters]]
- Updated: [[stateful-stream-processing]] (linked to checkpointing as heavyweight-framework durability analogue), [[hybrid-bpc-stream-processing]] (clarified Chapter 11 heavyweight vs Chapter 12 lightweight escape hatch), [[dataflow-engines]] (added BEDM heavyweight-streaming-descendant section linking to cluster/submission/checkpoint/ESS/multitenancy pages), [[event-driven-microservices]] (linked new heavyweight page), [[stream-processing-fault-tolerance]] (added checkpoint operator/key-state framing and heavyweight cross-link), [[basic-producer-consumer-microservice]] (corrected EDM-family table — Chapter 11 is heavyweight, Chapter 12 is lightweight)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 12
- Created: [[lightweight-framework-microservice]], [[broker-as-shuffle-service]], [[stream-table-table-join]]
- Updated: [[heavyweight-framework-microservice]] (EDM-family table linked to lightweight page; added cross-links), [[external-shuffle-service]] (strengthened lightweight-twist section with broker-as-shuffle-service cross-link), [[stream-processing-scaling-strategies]] (added lightweight-frameworks-collapse-the-strategies section), [[hot-replicas]] (added seamless-scale-up workflow for lightweight deployments), [[changelog-stream]] (reframed Kafka Streams / Samza embedded as lightweight-framework durability substrate; added checkpoint analogue cross-link), [[basic-producer-consumer-microservice]] (linked lightweight-framework page in EDM-family table), [[event-driven-microservices]] (linked new lightweight page)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 13
- Created: [[event-driven-request-response-integration]], [[external-events-ingestion]], [[third-party-api-integration]], [[serving-state-from-edm]], [[smart-load-balancer]], [[request-as-event]], [[asynchronous-ui]], [[micro-frontends]]
- Updated: [[synchronous-microservices]] (linked Chapter 13 integration hub and sub-pages), [[event-driven-microservices]] (expanded sync-vs-async section with Chapter 13 integration seams), [[materialized-state]] (added serving-over-RR-API section with smart-load-balancer and internal/external routing), [[internal-state-store]] (added request-response serving section with 1/N hit-rate and smart-load-balancer reference), [[external-state-store]] (added request-response serving section with all-in-one vs separate-microservice patterns), [[ui-composition]] (contrasted Newman's migration framing with Bellemare's steady-state framing; added [[micro-frontends]] cross-link)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 14
- Created: [[edm-supportive-tooling]], [[microservice-to-team-assignment]], [[event-stream-metadata]], [[event-broker-quotas]], [[event-stream-acls]], [[schema-change-notifications]], [[application-reset-tool]], [[consumer-lag-monitoring]], [[microservice-creation-workflow]], [[cluster-creation-and-management]], [[cross-cluster-replication]], [[dependency-tracking-and-topology-visualization]], [[data-lineage]], [[orphaned-streams]]
- Updated: [[event-driven-microservices]] (linked Chapter 14 tooling hub), [[single-writer-principle]] (added ACL enforcement concretization), [[schema-registry]] (added change-notifications section), [[consumer-offset]] (added lag-monitoring and offset-management-as-tool sections), [[business-topology]] (added concrete-tool section), [[container-management-system]] (added self-serve-controls section with autoscaling/cluster-bringup links)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 15
- Created: [[unit-testing-topology-functions]], [[topology-testing]], [[local-integration-testing]], [[remote-integration-testing]], [[hosted-service-mocks]], [[test-data-strategies]]
- Updated: [[event-driven-microservices]] (added testability section and Chapter 15 cross-links), [[end-to-end-testing]] (added Bellemare EDM framing with push-verification-left-and-right convergence point), [[schema-evolution]] (added CI-time compatibility-checking section as a fitness-function candidate), [[cross-cluster-replication]] (added seeding-integration-test-environments section)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 16
- Created: [[edm-deployment-principles]], [[edm-deployment-patterns]], [[continuous-integration-delivery-deployment]], [[basic-full-stop-deployment]], [[rolling-update-pattern]], [[blue-green-deployment]], [[breaking-schema-deployment]]
- Updated: [[breaking-changes]] (added deployment-mechanics section pointing to breaking-schema-deployment), [[application-reset-tool]] (added link to basic-full-stop-deployment as primary consumer), [[progressive-delivery]] (added links to edm-deployment-patterns and blue-green-deployment)

## 2026-04-17 — Building Event-Driven Microservices, Chapter 17
- Updated: [[event-driven-microservices]] (added Ch 17 closing framings: ownership-vs-access decoupling, failure-mode decoupling, composition-over-integration, large-services-OK rule, avoid-technical-alignment, Bellemare's final one-liner), [[communication-structures]] (added Ch 17 one-liner: decouples ownership and production from access and consumption), [[data-liberation]] (added sequencing-by-business-value and composition-payoff section), [[service-granularity]] (added Bellemare's three principles for running larger services and keeping future decomposition options open), [[microservice-tax]] (added Ch 17 incremental-payment-and-outsourcing framing), [[edm-deployment-principles]] (added four-way deployment trade-off and design-over-tooling thin-serving-layer alternative to blue/green)
