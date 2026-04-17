# Topology Testing

**Summary**: The middle layer of the [[event-driven-microservices|EDM]] testing pyramid — exercising a whole [[microservice-topology]] as a single complex function, without standing up a real [[event-broker]] or framework cluster. Built-in or third-party drivers (Kafka Streams' `TopologyTestDriver`, Spark's `MemoryStream` + `StreamingSuiteBase` / `spark-fast-tests`, Flink's and Beam's own testing utilities) let tests drive input events in, inspect output events, and control timing and ordering precisely.

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why unit tests alone are not enough

A topology is more than the sum of its [[unit-testing-topology-functions|leaf functions]]. Given:

```
myInputStream
  .map(myMapFunction)
  .groupByKey()
  .reduce(myReduceFunction)
```

you can unit-test `myMapFunction` and `myReduceFunction` in isolation, but `map`, `groupByKey`, and `reduce` are **framework operations** — their behavior is not in your code and cannot easily be re-created by hand (source: chapter-15-testing-event-driven-microservices.md). Time-based aggregations, [[event-scheduling]], and stateful operators emerge from the framework's interaction with your business logic, and only a topology test exercises that interaction.

## What a topology test driver gives you

Topology testing drivers let you treat the whole topology as "a single, large, complex function with many moving parts" (source: chapter-15-testing-event-driven-microservices.md) while still keeping the test hermetic:

- **Drive input precisely** — produce events with specific values, specific keys, specific timestamps, at specific points in wall-clock or [[stream-time]].
- **Generate adversarial input** — [[out-of-order-events]], events with invalid timestamps, events with invalid payloads, events that trigger corner-case branches.
- **Inspect output** — events written to output streams, [[materialized-state]], [[changelog-stream|changelog records]].
- **No broker, no cluster** — none of the setup cost or flakiness of a real [[event-broker]] or [[stream-processing-cluster]].

## Framework support varies

Choice of framework matters here. Bellemare's examples (source: chapter-15-testing-event-driven-microservices.md):

- **[[lightweight-framework-microservice|Kafka Streams]]** ships with `TopologyTestDriver` — it mocks the broker's behavior and lets you drive a full topology from a unit test.
- **Apache Spark** has `MemoryStream` built in for fine-grained stream input control, plus two third-party projects — `StreamingSuiteBase` and `spark-fast-tests` — for topology testing.
- **Apache Flink** and **Apache Beam** provide their own topology-testing utilities.

Bellemare treats this as a criterion when choosing a framework: "the community of users and contributors may have created a third-party option ... this is another reason to choose a framework with a strong community." If your framework has no topology-testing story, you are left to either build one or jump straight to [[local-integration-testing]].

## What topology testing cannot cover

Topology testing deliberately mocks the framework. It does not exercise:

- Real [[event-broker]] behavior (partition rebalancing, broker failures, quota enforcement).
- Real [[schema-registry]] compatibility checks — see [[schema-evolution]] for testing those separately at submission time.
- Multi-instance coordination, [[copartitioning]] across worker instances, [[checkpointing-stream-processing|checkpoint]]/recovery.
- Integration with request-response APIs, external data stores, or hosted services.

For those, you move up to [[local-integration-testing]].

## Related pages

- [[unit-testing-topology-functions]]
- [[local-integration-testing]]
- [[microservice-topology]]
- [[lightweight-framework-microservice]]
- [[heavyweight-framework-microservice]]
- [[event-scheduling]]
- [[out-of-order-events]]
- [[stream-time]]
- [[windowing]]
