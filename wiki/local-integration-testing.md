# Local Integration Testing

**Summary**: Running a developer-controllable replica of the production environment — [[event-broker]], [[schema-registry]], state stores, framework, microservice — on the developer's own machine to exercise a whole [[event-driven-microservices|EDM]] under controlled failure modes, adverse conditions, and varying capacity. Two implementation styles: **embed** the dependencies in the test runtime itself, or run them as a separate (usually containerized) environment that the test code talks to.

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why local integration testing

[[unit-testing-topology-functions|Unit]] and [[topology-testing]] cover business logic inside a single topology. Local integration testing is what ensures the microservice *as a deployable unit* behaves correctly when the surrounding systems misbehave (source: chapter-15-testing-event-driven-microservices.md):

- Control each component independently — broker, registry, stores, framework, microservice.
- Programmatically reproduce production failure scenarios: intermittent failures, [[out-of-order-events]], loss of network access, broker outages.
- Test request-response access in the same workflows as event ingestion — "think of the request-response API as just another source of events."
- Exercise [[stream-processing-scaling-strategies|horizontal scaling]] behavior: rebalancing, [[copartitioning]], [[state-store]] restore from [[changelog-stream]] or [[checkpointing-stream-processing|checkpoint]], data locality.

## Per-component knobs the test controls

Bellemare's enumeration of what the test environment should let you drive (source: chapter-15-testing-event-driven-microservices.md):

**Event broker:** create/delete streams, apply selective event ordering across partitions, modify partition counts, induce broker and stream-availability failures and recovery.

**Schema registry:** publish evolutionarily-compatible schemas (see [[schema-evolution]]), induce failures and recovery.

**Data stores:** schema changes to existing tables, stored-procedure changes, [[state-store-rebuilding-vs-migrating|rebuild internal state]] as instance counts change, induce failures and recovery.

**Processing framework (if applicable):** shuffling via [[broker-as-shuffle-service|internal streams]] or [[external-shuffle-service]] to exercise [[copartitioning]]; [[checkpointing-stream-processing|checkpoint]] and recovery; induce worker-instance failure for heavyweight frameworks.

**Application:** scale instance count dynamically to verify rebalancing, state restore, preserved data locality, and uninterrupted external state / request-response access.

## Two implementation styles

### Embedded: temporary environment inside the test runtime

Test code starts the broker, registry, and microservice instances *in the same process* as itself. Pseudocode from the book:

```
broker.start(...);
schemaRegistry.start(...);
topologyOne.start(...);  // first instance of the microservice
topologyTwo.start(...);  // second instance of the same microservice
producer.publish(inputStreamOne, ...);
producer.publish(inputStreamTwo, ...);
Thread.sleep(5000);
topologyOne.stop();       // mimic a failure
event = consumer.consume(outputTopic, ...);
topologyTwo.stop();
schemaRegistry.stop();
broker.stop();
// assert on event
```

Advantages: full programmatic control, deterministic cleanup on termination, no external infrastructure to manage.

Limitations: this is essentially a **JVM-only technique** at the time of writing. Kafka, the Confluent schema registry, Kafka Streams, and most heavyweight frameworks are JVM-based; programmatically starting them in-process requires a JVM test runner. Non-JVM stacks can work around it, but not cleanly (source: chapter-15-testing-event-driven-microservices.md).

### External: temporary environment outside the test runtime

Install the broker, registry, and other dependencies locally (or in a container) and point the test code at them. Installing locally per developer is low-overhead at first but becomes expensive and version-skew-prone across a team.

The recommended form is a **single shared container image** that bundles broker + registry + any required infrastructure. Teams consume it as an internal open-source artifact; improvements flow back for everyone. The microservice runs *outside* the container and points its test config at the container's addresses. Language-agnostic, easy to keep aligned with production versions.

For a lightweight framework: broker, schema registry, and topics live inside the container; the microservice runs locally (illustrated in Figure 15-1 of the source).

For a [[heavyweight-framework-microservice|heavyweight framework]]: the container also runs the master and worker instances of the framework, and the microservice submits its job to the master (Figure 15-2). FaaS uses a similar pattern with the provider's local testing library (Cloud Functions, Lambda, Azure Functions, OpenWhisk, OpenFaaS, Kubeless).

## Hosted services with no local option

Some production components are closed-source hosted services with no open-source implementation. See [[hosted-service-mocks]] for what to do when emulators exist (Google PubSub, LocalStack for Kinesis/etc., FaaS local-test libraries) and what to do when they don't (Azure Event Hubs at the time of writing — fall back to the Apache Kafka compatibility shim or to [[remote-integration-testing]]).

## What local integration testing cannot cover

Local environments are always sized well below production. They cannot answer:

- Performance, load, throughput, and scaling at production-scale capacity.
- Realistic data distributions and [[hot-spots|data skew]].
- Long-lived [[state-store]] behavior over production-scale histories.

Those belong to [[remote-integration-testing]].

## Related pages

- [[unit-testing-topology-functions]]
- [[topology-testing]]
- [[remote-integration-testing]]
- [[hosted-service-mocks]]
- [[test-data-strategies]]
- [[event-broker]]
- [[schema-registry]]
- [[stream-processing-cluster]]
- [[functions-as-a-service]]
- [[checkpointing-stream-processing]]
