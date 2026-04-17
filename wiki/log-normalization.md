# Log Normalization

**Summary**: The second canonical application of the [[adapter-pattern]]: using an adapter container to convert the heterogeneous log output of an application into a consistent, structured, timestamped stream that a fleet log aggregator can index uniformly. Worked example: `fluentd` with `fluent-plugin-redis-slowlog` to surface Redis's `SLOWLOG` command output as a time-series of queryable events.

**Sources**: `raw/designing-distributed-systems/chapter-04-adapters.md`

**Last updated**: 2026-04-16

---

## The problem

Applications log in wildly different ways (source: raw/designing-distributed-systems/chapter-04-adapters.md):

- Some split output across files by level (debug/info/warning/error); others write everything to stdout and stderr.
- Different logging libraries (Java's built-in logger vs Go's `glog`, etc.) emit different structured representations of fields like timestamp and severity.
- Some information you care about isn't in a log file at all — it's behind an API, a shell command, or a stats endpoint.

Meanwhile, container platforms have conventions: stdout is what `docker logs` and `kubectl logs` expose; downstream [[log-aggregation]] pipelines expect a consistent structured shape so they can parse and index events.

## The adapter solution

An adapter container sits alongside the application and normalises its logging. Typical transformations (source: raw/designing-distributed-systems/chapter-04-adapters.md):

- **Redirect files to stdout** so `kubectl logs` and the log aggregator see them.
- **Parse heterogeneous formats** into a single structured representation (JSON, for example) with consistent field names.
- **Ensure timestamps** are present and normalised.
- **Pull data from non-log sources** — shell commands, HTTP APIs, database queries — and format it as log events.

As with the [[unified-monitoring-interface]] adapter, the application itself is unchanged. Burns's succinct framing: "the adapter is taking a heterogeneous world of applications and creating a homogenous world of common interfaces" (source: raw/designing-distributed-systems/chapter-04-adapters.md).

## Hands-on: fluentd + Redis SLOWLOG

Redis exposes a `SLOWLOG` command that lists recent queries exceeding a configured time threshold — extremely useful for diagnosing performance problems. The catch: it's only available as an interactive command on the running server. If nobody is looking when a problem occurs, the information is lost after the buffer rolls over (source: raw/designing-distributed-systems/chapter-04-adapters.md).

The chapter's solution is a `fluentd` adapter container deployed in the same pod as the Redis container, running the community plugin `fluent-plugin-redis-slowlog` to continuously poll `SLOWLOG` and emit each entry as a structured log event:

```
<source>
type redis_slowlog
host localhost
port 6379
tag redis.slowlog
</source>
```

Because the two containers share the pod's network namespace, the plugin simply configures `localhost` and the Redis default port. The adapter produces a persistent, queryable time series of slow queries, turning a transient interactive command into a retrospectively-debuggable log stream.

## Hands-on: fluentd + Apache Storm

The same structural pattern works for Apache Storm, which exposes internal status via a RESTful API (source: raw/designing-distributed-systems/chapter-04-adapters.md). A fluentd adapter container with `fluent-plugin-storm` polls Storm's local HTTP endpoint and converts it into a log stream:

```
<source>
type storm
tag storm
url http://localhost:8080
window 600
sys 0
</source>
```

Again, `localhost` works because of shared pod networking. The Storm process itself is untouched; the adapter turns "data that exists only if you happen to be looking" into "data that persists and can be queried later."

## Why not modify the application?

Burns raises and answers the obvious objection: "why not simply modify the application container itself?" If you own the application, modifying it is defensible. In practice you often don't — Redis, Storm, and most other long-lived infrastructure you operate come as third-party images. Deriving "a slightly modified image that we have to maintain (patch, rebase, etc.) is significantly more expensive than developing an adapter container that can run alongside the other party's image." Separating the adapter also enables reuse across deployments and contribution by the broader community (source: raw/designing-distributed-systems/chapter-04-adapters.md).

## Relationship to existing wiki concepts

### Normalization vs aggregation

This page is about *producing* structured logs; [[log-aggregation]] is about *collecting and querying* them. The two compose: adapter-normalised logs are dramatically easier to aggregate because the downstream parser doesn't have to cope with per-application format drift. Newman's "do this first" recommendation for log aggregation implicitly assumes consistent logs — the adapter pattern is the container-level mechanism that gets you there.

### Normalization and correlation IDs

Normalised structured logs are a prerequisite for [[correlation-ids]] to work across services. If service A logs `requestId` and service B logs `trace-id`, the fact that the same UUID appears in both won't help a query — the shared field name has to be there. An adapter is a natural place to normalise field names across heterogeneous emitters.

### Normalization and the adapter pattern

This is the second of three canonical adapter applications in Chapter 4. See also [[unified-monitoring-interface]] and the [[health-check-adapter]].

### Normalization and legacy modernization

Forcing uniform logging out of a legacy application is a common [[legacy-modernization]] task. An adapter is the least invasive way to do it — no source change, no rebuild, no fork of the upstream image.

## Related pages

- [[adapter-pattern]]
- [[unified-monitoring-interface]]
- [[health-check-adapter]]
- [[log-aggregation]]
- [[correlation-ids]]
- [[monitoring-and-observability]]
- [[modular-reusable-containers]]
- [[legacy-modernization]]
- [[pod]]
- [[designing-distributed-systems]]
