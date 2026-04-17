# Unit Testing Topology Functions

**Summary**: The innermost layer of the [[event-driven-microservices|EDM]] testing pyramid: exercising the individual transformation, aggregation, mapping, filter, and reduction functions that sit inside a [[microservice-topology]]. Stateless functions are trivial to test; stateful functions require a mocked or locally-available state store for the duration of the test.

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why topology functions are good unit-test targets

Event-driven topologies overwhelmingly consist of small, purpose-built transform / aggregate / map / filter / reduce functions applied to events. These are exactly the shape that unit tests are best at: small, composable, with well-defined inputs and outputs (source: chapter-15-testing-event-driven-microservices.md).

Bellemare's standing tip: **test boundary conditions** — null, maximum, malformed — for each function, not just the happy path (source: chapter-15-testing-event-driven-microservices.md).

## Stateless functions

Stateless functions keep no state between calls. Given the same inputs they produce the same outputs. A typical lightweight-framework topology exposes them directly:

```
myInputStream
  .filter(myFilterFunction)
  .map(myMapFunction)
  .to(outputStream)
```

`myFilterFunction` and `myMapFunction` are pure functions. They can be pulled out of the topology and unit-tested independently without any framework machinery at all (source: chapter-15-testing-event-driven-microservices.md).

## Stateful functions

Stateful functions — typical of a [[basic-producer-consumer-microservice]] aggregation, or any [[stateful-stream-processing]] operator — depend on a [[state-store]] that varies with time and prior events. They need more care:

- **Cover the stateful edge cases.** State evolves with both time and input ordering, so the test matrix is larger than for a stateless function.
- **Make the state store available for the test.** Either mock the store's endpoint, or spin up a local instance of it.

Bellemare's example is an aggregation function that reads a running sum, adds the incoming value, and writes the sum back:

```java
public Long addValueToAggregation(String key, Long eventValue) {
    Long storedValue = datastore.getOrElse(key, 0L);
    Long sum = storedValue + eventValue;
    datastore.upsert(key, sum);
    return sum;
}
```

### Mock vs local store

- **Mocking the store** keeps the unit test fast and cheap — no bringup cost, no process boundary. Mocking tends to work well here because "it allows for very high-performance unit testing that isn't burdened by the overhead of spinning up a full implementation of the data store" (source: chapter-15-testing-event-driven-microservices.md).
- **A locally running instance of the store** is more faithful but shades into [[local-integration-testing]] territory.

In either case, think carefully about what the store's behavior needs to be to exercise the function correctly — missing keys, stale reads, write failures.

## What unit tests cannot cover

Unit tests on individual functions do not exercise:

- The framework-level operations themselves (`map`, `groupByKey`, `reduce`, `windowing`, `joins`).
- Copartitioning, shuffling, scaling, rebalancing.
- Ordering between events arriving on different partitions or different streams.

For those you need [[topology-testing]] and [[local-integration-testing]].

## Related pages

- [[topology-testing]]
- [[local-integration-testing]]
- [[microservice-topology]]
- [[stateful-stream-processing]]
- [[stateless-stream-processing]]
- [[state-store]]
- [[basic-producer-consumer-microservice]]
- [[lightweight-framework-microservice]]
- [[heavyweight-framework-microservice]]
