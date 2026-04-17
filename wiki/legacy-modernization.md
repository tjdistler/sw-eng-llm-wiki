# Legacy Modernization

**Summary**: Adapting pre-existing applications to new requirements — HTTPS, dynamic configuration, cloud-native observability — without modifying their source code. Burns presents the [[sidecar-pattern]] as a powerful technique for this: attach a separate container that augments the legacy application through shared OS namespaces, leaving the application itself untouched.

**Sources**: `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`

**Last updated**: 2026-04-16

---

## The problem

Real systems accumulate applications whose source is hard to change:

- The build system is obsolete and no longer functional.
- The original developers are gone and nobody is confident rebuilding it.
- The application works and is business-critical; opening it up to modify is expensive and risky.
- Regulatory or security requirements have changed since the application was written, and the gap between what it does and what it must now do keeps widening.

Burns's running example: a legacy web service that only speaks HTTP, in a company that now requires HTTPS everywhere. The team is stuck between resurrecting a broken build system and porting the source to a new one — both expensive (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

## The sidecar escape hatch

Rather than modify the legacy application, co-deploy a separate container alongside it in the same [[pod]]. The sidecar container augments the legacy application's behaviour using shared namespaces, so the legacy container stays exactly as it is.

Burns walks through two modernization sidecars (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

### Adding HTTPS to a plaintext service

- Bind the legacy service to `127.0.0.1` only.
- Add an nginx sidecar in the same network namespace.
- nginx terminates HTTPS on the external IP and proxies cleartext to the legacy service over loopback.
- The cleartext hop never leaves the pod, so network security is satisfied.

The legacy binary is never rebuilt. The build-system question becomes irrelevant.

### Adding dynamic configuration to a file-based application

- The legacy application reads its config from a file on disk (as it always did).
- A configuration-manager sidecar shares that directory.
- The sidecar watches a cloud configuration API; on change, it writes the new file and signals the app (via `SIGHUP`, file-watch events, or `SIGKILL` + orchestrator restart).

Again, the application is unchanged. It continues to behave as if config is a local file, because — from its point of view — it is.

## Why this matters

Burns frames this as the primary motivation many readers will expect from the sidecar pattern, and notes correctly that it is only one of several (the other main one being [[modular-reusable-containers]]). But the modernization use case is high-value because:

- It sidesteps the "we can't rebuild this" problem entirely.
- It lets organizations apply new policies (HTTPS, dynamic config, observability) uniformly across legacy and modern applications.
- It does so through orchestrator-level composition, not in-application changes, so teams with no knowledge of the legacy codebase can do the work.

## Relationship to existing wiki concepts

### Compared with Newman's monolith-migration patterns

In *Monolith to Microservices*, Sam Newman gives a catalogue of patterns for chipping functionality off a legacy monolith without rewriting it — the [[strangler-fig-pattern]], [[branch-by-abstraction]], [[parallel-run-pattern]], [[decorating-collaborator-pattern]], and so on. All share the same philosophy: extend or replace legacy behaviour from the outside, incrementally.

The sidecar is a close cousin, operating at a different level. Where strangler-fig intercepts traffic at the application edge and grows a replacement service next to the monolith, the sidecar augments the legacy process on the node itself, leaving the application wire contract intact but changing what surrounds it.

Both approaches prize the same thing: **don't change the legacy code until you have to**. See [[deployment-vs-release]] and [[incremental-migration]] for Newman's framing of the underlying discipline.

### Compared with service mesh

At scale, legacy-modernization sidecars blur into the [[service-mesh]]: the same nginx or Envoy that terminates HTTPS for one legacy service can be deployed uniformly across the fleet and centrally controlled. A service mesh is, in one reading, a legacy-modernization sidecar that has been standardized and promoted to platform infrastructure.

### Information hiding at the deployment layer

The sidecar is [[information-hiding]] in operational clothing. The legacy application's internal deficiencies — no TLS, no dynamic config, no `/topz` endpoint — are hidden behind a pod-level interface that presents the capabilities a modern deployment expects. Consumers of the pod can't tell whether the TLS, the dynamic config, or the metrics endpoint are provided by the application or by a sidecar.

### Adapters for legacy observability

Where sidecars typically handle the *inbound* side of modernization (HTTPS, dynamic config), the Chapter 4 [[adapter-pattern]] typically handles the *outward observation* side: metrics, logs, health checks (source: raw/designing-distributed-systems/chapter-04-adapters.md). A legacy MySQL image probably doesn't expose a rich HTTP health check; a [[health-check-adapter]] container adds one without a fork. A legacy Redis deployment doesn't expose Prometheus metrics; a [[unified-monitoring-interface]] adapter does. A legacy Java server with opinionated log format goes through a [[log-normalization]] adapter on its way to the aggregator. All three modernise the application's *interface to the rest of the infrastructure* without changing the application itself — the same philosophy as the sidecar legacy-modernization cases, applied to a different slice of the pod surface.

## When the sidecar is not the answer

The chapter doesn't make this explicit, but the argument implies limits:

- If the legacy application's problem is *inside* its protocol or data — for example, it exposes an insecure API semantics, not just insecure transport — a sidecar proxy does not fix it.
- If the required augmentation needs tight feedback with application internals (not just traffic), a sidecar's namespace sharing may not be enough.
- Eventually, sidecars that accumulate around a legacy application raise the question of whether the legacy application should be replaced rather than surrounded. Newman's migration patterns resume from there.

## Related pages

- [[sidecar-pattern]]
- [[adapter-pattern]]
- [[unified-monitoring-interface]]
- [[log-normalization]]
- [[health-check-adapter]]
- [[pod]]
- [[modular-reusable-containers]]
- [[service-mesh]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[incremental-migration]]
- [[deployment-vs-release]]
- [[information-hiding]]
- [[designing-distributed-systems]]
