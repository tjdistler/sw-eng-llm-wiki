# Test Data Strategies for EDM

**Summary**: Three ways to populate an [[event-broker]]'s input streams for [[remote-integration-testing]] of an [[event-driven-microservices|EDM]]: copy events from **production**, load **curated** event sets from a durable store, or **programmatically generate** events from the registered [[schema-registry|schema]]. Each trades realism for isolation, maintenance cost, and coverage of corner cases.

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why this is its own decision

EDMs almost always source their input from event streams (source: chapter-15-testing-event-driven-microservices.md). A newly-created test environment is empty; populating it is a distinct engineering problem from bringing the environment up. The choice affects test fidelity, maintenance burden, and risk of leaking sensitive production data.

## Option 1: Replicate from production

Use the same [[cross-cluster-replication]] tooling that supports disaster recovery to copy specific production streams into the test cluster.

**Advantages** (source: chapter-15-testing-event-driven-microservices.md):

- Accurately reflects production data — same distributions, same volumes, same edge cases.
- Granular: copy as many or as few events as required.
- The isolated environment prevents other tests from interfering.

**Disadvantages:**

- Copying can affect production broker performance unless [[event-broker-quotas|broker quotas]] are set up.
- Can require copying substantial amounts of data, especially for long-lived entity streams.
- Sensitive data on some streams must be handled carefully — both legally and technically.
- Requires significant tooling investment to make the copy process low-friction.
- Risks exposing sensitive production events to developer environments.

## Option 2: Curated test data sets

Store carefully-crafted event fixtures in a durable store and load them into the test streams on demand. Common in shared staging environments ([[remote-integration-testing]]).

**Advantages** (source: chapter-15-testing-event-driven-microservices.md):

- Small, focused data sets — fast to load, cheap to hold.
- Curator controls specific values, relationships, and corner cases.
- No impact on production, no risk of leaking sensitive data.

**Disadvantages:**

- Significant ongoing maintenance burden.
- Data goes stale; new event streams must be added by hand; schema changes force updates to fixtures.
- Lesser-used streams tend to be forgotten.
- Without discipline, the curated set follows the typical organizational fate of documentation: well-intentioned, perpetually out of date, perpetually lower priority than other work.

## Option 3: Programmatic mock events from schemas

Read a schema from the [[schema-registry]] and generate events that conform to it. Older schema versions can be used too, to exercise [[schema-evolution]] compatibility paths. Tools like Confluent's Avro tooling support this.

**Advantages** (source: chapter-15-testing-event-driven-microservices.md):

- No dependency on production data; no performance or privacy blast radius.
- Fuzz-style generators can exercise boundary conditions, malformed fields, and corner cases that real production data doesn't contain.
- Third-party tooling automates most of it.

**Disadvantages:**

- Realism requires deliberate attention: valid joins need matching primary/foreign keys across streams, aggregations need distributions that exercise the aggregation logic.
- Even careful mocks miss production's volume and skew characteristics — [[hot-spots|key-distribution skew]] that dominates production load may be entirely absent from mock data.
- Fields that are "just strings" in the schema may have structural conventions (embedded IDs, formatted timestamps) that business logic depends on; mocks can parse correctly in test and fail on a subset of real production strings.

## Summary table

| Strategy | Realism | Isolation from prod | Maintenance | Corner cases |
|---|---|---|---|---|
| Replicate from production | highest | isolated cluster | moderate (tooling-heavy) | only those present in prod |
| Curated fixtures | low–medium | full | high (ongoing) | the ones you curated |
| Schema-driven mocks | medium | full | low | whatever the fuzzer covers |

No one strategy dominates; real test suites typically mix curated fixtures for hand-designed scenarios with schema-driven fuzzing for breadth, and fall back on production replication when realism is indispensable.

## Related pages

- [[remote-integration-testing]]
- [[local-integration-testing]]
- [[cross-cluster-replication]]
- [[schema-registry]]
- [[schema-evolution]]
- [[event-broker-quotas]]
- [[hot-spots]]
