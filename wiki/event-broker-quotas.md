# Event Broker Quotas

**Summary**: Per-producer and per-consumer limits on the CPU, network, and I/O that any single client can consume on an [[event-broker]] cluster. Quotas prevent a chatty producer or an aggressive parallelized consumer group from causing accidental denial-of-service for the rest of the cluster.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Why universal quotas exist

A single misbehaving client can saturate a shared broker: a producer burst, a consumer group starting at offset 0 on a very large stream, or a parallelized reprocessing job. A universal quota — "no one client may consume more than 20% of CPU" — ensures that cluster capacity is not exhausted by one tenant (source: chapter-14-supportive-tooling.md). The broker throttles the offender by delaying its responses.

## Per-client quotas

Granular quotas override the universal default for specific producers or consumers. Use cases (source: chapter-14-supportive-tooling.md):

- **Surge-tolerant producers** — a service that has legitimate short bursts gets a higher ceiling.
- **Guaranteed-minimum consumers** — a steady-state consumer gets a reserved share so it never falls behind due to noisy neighbors.
- **External-source producers** — a producer whose inbound rate is dictated by a third party should not be throttled, because throttling would cause dropped data or crashes on the external side. Remove the quota or set it above the expected peak.

## What can go wrong without quotas

- One consumer group resets to offset 0 on a 500 GB stream → the broker's CPU and network saturate → every other tenant's latency spikes.
- A runaway producer retries aggressively after a deserialization bug → message flood → cluster outage.
- A poorly tuned [[stream-processing-cluster]] scales to many parallel consumers against a hot partition → storms the broker.

## Where quotas sit in the tooling catalog

Quotas are set by the broker ops team, but the **self-serve tool** lets owning teams inspect their services' current throughput and negotiate changes when they legitimately need more headroom. Identity comes from [[event-stream-acls]], and the request/approval path goes through the [[microservice-to-team-assignment]] system.

## Related pages

- [[edm-supportive-tooling]]
- [[event-broker]]
- [[event-stream-acls]]
- [[rate-limiting]]
- [[stream-processing-cluster]]
