# Cross-Cluster Event Data Replication

**Summary**: Moving event data between [[event-broker]] clusters — across regions, across business units, or between prod/test — to support disaster recovery, cross-cluster consumption, and programmatically generated environments. The choice of replication tool is load-bearing; its characteristics (exactness, latency, scale, stream lifecycle handling) determine what the downstream architecture can rely on.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`, `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why replicate across clusters

Three driving use cases (source: chapter-14-supportive-tooling.md):

- **Disaster recovery** — a secondary cluster holds a copy of production data so that the organization can fail over if the primary is lost.
- **Routine cross-cluster communication** — when data produced in one region must be consumed in another, or when a business unit in one cluster needs data from another.
- **Programmatic test/integration environments** — spin up a new cluster for testing and seed it from a replica of production data.

## The questions to ask of a replication tool

Bellemare's checklist when selecting a replicator (source: chapter-14-supportive-tooling.md):

- **Newly-added streams** — does replication pick them up automatically, or must each new stream be explicitly registered?
- **Deleted / modified streams** — what happens on the destination when the source stream changes lifecycle?
- **Exactness** — is the replicated data byte-identical with the **same offsets, partitions, and timestamps**, or is it an approximate copy with different offsets?
- **Latency** — what is the end-to-end lag from source to replica? Is it acceptable for the business purpose?
- **Performance / scalability** — does the tool scale to the organization's throughput requirements?

The offset-exactness question is the one with the most downstream consequences: if offsets don't match, failing over a consumer to the replica cluster requires a separate offset-translation step and consumers cannot resume mid-stream cleanly.

## Not covered by the book

Bellemare explicitly defers multicluster service and data-management strategy to other sources — the details depend too heavily on the broker, the replicator, and the prevention/recovery strategy in use. The chapter's contribution is the checklist above; the implementation is left to the reader (source: chapter-14-supportive-tooling.md). Capital One is cited as a real-world case where custom libraries were built on top of Kafka specifically because financial-event loss was unacceptable.

## Seeding integration-test environments

Chapter 15 names this tool as the load-bearing mechanism for populating a [[remote-integration-testing|programmatically-created test environment]] with realistic data. Spin up a dedicated cluster per test run, use the replicator to copy the relevant production streams in, run the tests, tear the cluster down. Production [[event-broker-quotas|quotas]] must be configured so the copy process doesn't starve real consumers (source: chapter-15-testing-event-driven-microservices.md). See [[test-data-strategies]] for how replication compares to curated fixtures and schema-driven mock events.

## Relationship to existing wiki coverage

- **[[cluster-creation-and-management]]** — the broader cluster-lifecycle story; replication is the data plane.
- **[[event-broker]]** — replication is usually broker-native (Kafka MirrorMaker 2, Confluent Replicator) or a third-party tool riding on top.
- **[[replication]] / [[leader-based-replication]] / [[multi-leader-replication]]** — general-purpose replication primitives; cross-cluster event replication is a specialized case.
- **[[consumer-offset]]** — the offset-exactness question is why this page references offsets at all.

## Related pages

- [[edm-supportive-tooling]]
- [[event-broker]]
- [[cluster-creation-and-management]]
- [[replication]]
- [[consumer-offset]]
- [[remote-integration-testing]]
- [[test-data-strategies]]
