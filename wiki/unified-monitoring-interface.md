# Unified Monitoring Interface

**Summary**: The first of Burns's three canonical applications of the [[adapter-pattern]]: presenting every application in a fleet through a single, well-understood metrics interface so that one monitoring tool can automatically discover and scrape them all. Worked example: a Prometheus exporter adapter running alongside a Redis container.

**Sources**: `raw/designing-distributed-systems/chapter-04-adapters.md`

**Last updated**: 2026-04-16

---

## The problem

Automated monitoring of a distributed system assumes that every application exposes metrics through one interface — so that "a single solution … can automatically discover and monitor any application that is deployed into your environment" (source: raw/designing-distributed-systems/chapter-04-adapters.md).

Reality doesn't cooperate. Burns lists examples of widespread-but-incompatible monitoring interfaces: syslog, Windows Event Tracing (ETW), JMX for Java applications, and many more protocols with different communication styles (notably **push vs pull**). An application fleet assembled from first-party code, vendor software, and open-source components inherits this zoo of interfaces, and the single-tool assumption quickly breaks (source: raw/designing-distributed-systems/chapter-04-adapters.md).

## The adapter solution

Rather than modify each application to emit the standard metrics format, run an **adapter container** alongside it. The application container keeps its native interface; the adapter reads that interface and re-exposes the data in the shape the monitoring system expects (source: raw/designing-distributed-systems/chapter-04-adapters.md).

Burns lists the advantages of this decomposition:

- **Decoupled rollouts.** New application versions don't require adapter redeploys and vice versa.
- **Reuse across the fleet.** One Redis-to-Prometheus adapter works for every Redis deployment.
- **Third-party authorship.** The monitoring team (or the wider open-source community) can supply the adapter; the application team doesn't need to touch it.
- **Isolated resources.** The adapter has its own CPU/memory quota — a misbehaving monitoring adapter "cannot cause problems with a user-facing service."

## Hands-on: Redis with Prometheus

The chapter's worked example (source: raw/designing-distributed-systems/chapter-04-adapters.md):

**The problem.** Prometheus expects every container to expose a specific pull-style metrics API. Redis does not.

**The adapter.** The open-source `oliver006/redis_exporter` is a small HTTP server that speaks Redis's own protocol to the sibling Redis container and re-exposes the data as Prometheus-formatted metrics.

**The pod.** Starting from a vanilla Redis pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example
  namespace: default
spec:
  containers:
  - image: redis
    name: redis
```

Add the adapter container alongside:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example
  namespace: default
spec:
  containers:
  - image: redis
    name: redis
  # Provide an adapter that implements the Prometheus interface
  - image: oliver006/redis_exporter
    name: adapter
```

The Redis container is unchanged. The exporter uses the pod's shared network namespace to talk to Redis on `localhost:6379` and serves Prometheus metrics on its own HTTP port. Prometheus scrapes the pod and gets metrics in the format it understands.

Burns flags the composite lesson: "the value of the adapter pattern for ensuring a consistent interface, but also the value of container patterns in general for modular container reuse" (source: raw/designing-distributed-systems/chapter-04-adapters.md). The deployment combines an existing Redis image with an existing Prometheus exporter with near-zero custom work — the alternative (embedding Prometheus instrumentation into a fork of Redis) would be "significantly more custom work" and would inherit a perpetual rebase burden.

## Why pull-style makes the pattern elegant

Prometheus is pull-based: the monitoring system calls into each application on a standard endpoint. That dovetails naturally with the adapter pattern because the adapter can be a passive HTTP server that translates on demand. Push-based systems (like StatsD or Fluent-forwarding) need the adapter to drive outbound connections instead, which is more stateful but structurally similar.

## Relationship to existing wiki concepts

### Unified monitoring and observability

Newman's [[monitoring-and-observability]] chapter makes the case that microservices break monolith-era monitoring. This page is the container-level mechanism for satisfying that requirement without rewriting every application. Service-level metrics — request rate, error rate, latency — can be supplied by a [[service-mesh]] automatically for services that speak HTTP/gRPC. Application-specific internal metrics (Redis hit rate, MySQL query timings) need an adapter per app type.

### Unified monitoring and modular reusable containers

The Redis exporter is a textbook [[modular-reusable-containers]] artefact: narrow scope, parameterised over endpoint and credentials, authored once and reused anywhere Redis is deployed. The pattern and the discipline are mutually reinforcing.

### Unified monitoring and the adapter pattern

This is the first of three canonical adapter applications in Chapter 4; the other two are [[log-normalization]] and the [[health-check-adapter]]. All three share the adapter-pattern structure: the application's native interface faces inward; the fleet-standard interface faces outward.

## Related pages

- [[adapter-pattern]]
- [[log-normalization]]
- [[health-check-adapter]]
- [[monitoring-and-observability]]
- [[sidecar-pattern]]
- [[modular-reusable-containers]]
- [[pod]]
- [[service-mesh]]
- [[designing-distributed-systems]]
