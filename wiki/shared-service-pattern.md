# Shared Service Pattern

**Summary**: A [[reuse-patterns|code-reuse pattern]] that places shared functionality in a separately deployed service rather than a library. Composition, not inheritance: callers invoke the service over the network. Trades compile-time [[static-coupling|static coupling]] for [[dynamic-coupling|runtime dynamic coupling]] — gaining language-independence and instant rollout, paying with latency, scalability tax, fault-tolerance risk, and trickier versioning.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19

---

## The pattern

Common functionality lives in its own deployable service. Other services call it at runtime — typically via REST, gRPC, or messaging — instead of importing a library (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

A defining property: the shared code is consumed via **composition**, not inheritance. The architectural composition-vs-inheritance question matters here in a way it doesn't always matter in code: a shared service can only be composed into a workflow, never extended by it.

## What changes vs a shared library

| | [[shared-library-pattern|Shared library]] | Shared service |
|---|---|---|
| Binding | Compile time | Runtime |
| Coupling axis | [[static-coupling|Static]] | [[dynamic-coupling|Dynamic]] |
| Change rollout | Each service rebuilds and redeploys | Deploy once; effective immediately for all callers |
| Polyglot fit | One library per language | One service serves all languages |
| Failure mode of "simple" change | Caught at compile / test time per consumer | Can break every caller in production at once |

The chapter's framing: changes in a shared service feel agile (one redeploy, every caller benefits) until they break the entire system at runtime. **A "simple" change can take down everything that depends on it.**

## Change risk and runtime versioning

Versioning is the obvious answer. The obvious mechanism is API endpoint versioning (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

```
app/1.0/discountcalc?orderid=123
app/1.1/discountcalc?orderid=123
app/1.2/discountcalc?orderid=123
app/1.3/discountcalc?orderid=123
latest -> app/1.4/discountcalc?orderid=123
```

The problems:

- **Callers must change** to point to the new version. The "no rebuild needed" benefit erodes with every breaking version.
- **When does a new endpoint warrant a new version?** Error-message change? New calculation? The line is subjective.
- **Multi-protocol access** — if some callers use REST, others gRPC, others messaging, version coordination across protocols is hard.

Net: shared-service versioning is *more complex* to apply and manage than shared-library versioning, even though both nominally exist for the same reason.

## Performance, scalability, fault tolerance

These are the operational costs the [[shared-library-pattern]] avoids by binding at compile time. The shared service introduces all three (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

### Performance

Every use of shared functionality becomes an inter-service call. Network latency + security latency add up. Mitigations:

- **gRPC** instead of REST.
- **Asynchronous messaging** with request/reply queues and correlation IDs, so callers can do other work while waiting.

### Scalability

The shared service must scale alongside its callers. With many concurrent consumers this becomes its own capacity-planning headache. A shared library has no equivalent issue — the shared code scales with each service automatically.

### Fault tolerance

If the shared service is unavailable, every dependent service is rendered non-operational for that capability. Multiple instances mitigate but do not eliminate the risk. A shared library has no equivalent issue — the shared code lives inside the consumer.

## Trade-offs

| Pro | Con |
|---|---|
| Polyglot-friendly — one service serves all languages | Inter-service calls add latency (network + security) |
| Changes deploy without redeploying consumers | Runtime change risk — a "simple" bug breaks every caller |
| Preserves bounded context — no shared compile-time artifact | Shared service must scale with consumers |
| Fast rollout for high-churn shared logic | Adds a fault-tolerance dependency |
| | Versioning is harder than for libraries; multi-protocol coordination painful |

## When to use

Two conditions favour the shared service over a shared library (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

1. **Polyglot environment** — the cost of maintaining a parallel library per language outweighs the runtime cost of a shared service.
2. **Frequently-changing shared functionality** — the agility of one redeploy reaching all callers outweighs the runtime risk.

In other situations, prefer [[shared-library-pattern|shared library]] (homogeneous stack, low churn) or [[code-replication-pattern]] (trivial static code).

## Not the same as a sidecar / service mesh

A [[sidecar-pattern|sidecar]] also moves shared concerns out of the service code, but for *operational / cross-cutting* capabilities (monitoring, mTLS, tracing, circuit breakers). A shared service holds *domain* logic that callers compose into business workflows. Use a sidecar for orthogonal concerns ([[orthogonal-coupling]]); use a shared service for domain capabilities polyglot teams need to share.

## Cross-link to component decomposition

[[gather-common-domain-components-pattern]] (Chapter 5) finds shared *domain* components in a monolith. The Chapter 8 follow-up — "should this consolidated component become a shared library or a shared service?" — is what this page answers from the service side.

## Related pages

- [[reuse-patterns]]
- [[shared-library-pattern]]
- [[code-replication-pattern]]
- [[sidecar-pattern]]
- [[orthogonal-coupling]]
- [[dynamic-coupling]]
- [[gather-common-domain-components-pattern]]
- [[shared-database-antipattern]]
- [[software-architecture-the-hard-parts]]
