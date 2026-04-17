# Remote Integration Testing

**Summary**: Integration testing that runs the [[event-driven-microservices|EDM]] against a full, production-scale, remote environment — necessary for performance, load, throughput, scaling, and failure-recovery tests that cannot be faithfully reproduced on a developer laptop. Three variants: a **temporary** environment spun up per test run, a **shared** staging environment used by many teams, and **production itself**. The three have very different cost and risk profiles.

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why remote

Some tests can only be done at production scale (source: chapter-15-testing-event-driven-microservices.md):

- Event-processing throughput and request-response latency under realistic load.
- Horizontal scaling of instance counts under organic traffic.
- Failure-recovery behavior when instances, brokers, or stores actually go down.
- Full-history reprocessing from the beginning of input-stream time.

The stated goal: "create an environment as close to possible as that of production, including event streams, event data volume, event schemas, and request-response patterns" (source: chapter-15-testing-event-driven-microservices.md).

## Option 1: Programmatically-created temporary environment

Leverage the same [[cluster-creation-and-management|cluster creation and management]] tooling used to bring up production brokers and compute pools. For each test run, spin up a new broker cluster and reserved compute, run the containerized microservice, and tear the whole environment down at the end.

Additional benefit: "regularly exercises the process of creating new brokers and compute environments" (source: chapter-15-testing-event-driven-microservices.md). Any bug in the bringup scripts surfaces on the next test run instead of during a disaster.

Prerequisites:

- Source event streams to create — names taken from a microservice config file or asked of the user.
- Partition counts matching production, so scaling, [[copartitioning]], and repartitioning behavior are faithful.
- Event data to populate the streams — see [[test-data-strategies]] for the three options (replication from production, curated data sets, schema-generated mock events) and their trade-offs.

The full benefit is only realized with investment in [[edm-supportive-tooling|supportive tooling]] — programmatic cluster bringup plus [[cross-cluster-replication|cross-cluster replication]] for seeding. Without that tooling, temporary environments are too expensive to build per test and organizations fall back to shared staging.

## Option 2: Shared staging environment

A single persistent testing cluster with shared event streams, used by every team. Lower-overhead to start, but subject to the **"tragedy of the commons"** (source: chapter-15-testing-event-driven-microservices.md):

- Fragmented, abandoned streams accumulate. It becomes hard to tell valid input from stale residue. Naming patterns like `stream-testing-01`, `stream-testing-02-final`, `stream-testing-02-final-v2` proliferate.
- Teams running large-scale performance tests affect each other's results.
- Incompatible events produced to another service's input stream break that service's tests.
- Event data goes stale and stops representing production.
- No isolation between services under test, since one service's output is often another service's input.

Bellemare's explicit warning: "This strategy is the worst of the options in terms of usability." Survivable with strict curation, naming conventions, write-side ACLs, and coordinated load-test scheduling, but it requires ongoing diligence.

## Option 3: Test in production

Run the microservice against the real production broker and real production event streams, but direct its **outputs** to a set of distinct, test-only output streams and state stores so it doesn't contaminate real consumers (source: chapter-15-testing-event-driven-microservices.md).

Advantages:

- Complete access to real production event data.
- Production security model enforces access protocols naturally.
- Excellent for smoke-testing.
- No separate environment to maintain.

Disadvantages:

- Risk of affecting production capacity — unsuitable for load and performance testing.
- Cleanup is essential: test output streams, consumer groups, ACLs, state stores.
- Tooling must clearly distinguish "true production" services from "services under test" so observers and deployment pipelines don't conflate them, especially during long-running tests.

This form of in-production testing is a close cousin of [[parallel-run-pattern|parallel run]] and [[progressive-delivery]] techniques — running a new implementation alongside the existing one and comparing behavior.

## Choosing a strategy

The modularity of microservices means you don't have to pick just one — different projects can use different strategies, and your methodology can evolve as requirements change (source: chapter-15-testing-event-driven-microservices.md).

Tooling investment is the determinant:

- **Low tooling** → a single shared cluster is what you will end up with, with all its pathologies. Tribal knowledge carries the day, testing fidelity suffers, and costs are high for a continuously-available staging cluster that must also hold performance data and long-retention streams.
- **High tooling** → each microservice brings up its own dedicated cluster, seeds it from production, runs tests, tears it down. Testing artifacts don't accumulate. The same tooling also unlocks multi-cluster operation and disaster recovery (Chapter 14).

Shared staging isn't categorically wrong; it's a reasonable starting point as long as source-stream reliability is owned by the team that owns the production data, naming is disciplined, and teams coordinate performance tests. Over time, migrate teams toward dynamically-created clusters as the tooling matures.

## Related pages

- [[local-integration-testing]]
- [[test-data-strategies]]
- [[end-to-end-testing]]
- [[cluster-creation-and-management]]
- [[cross-cluster-replication]]
- [[edm-supportive-tooling]]
- [[progressive-delivery]]
- [[parallel-run-pattern]]
- [[synthetic-transactions]]
