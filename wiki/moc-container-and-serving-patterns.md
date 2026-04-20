# MOC: Container and Serving Patterns

**Summary**: Entry point for questions about *how a containerised service is shaped, replicated, sharded, composed, and rolled out* — the single-node container patterns (sidecar, ambassador, adapter), the multi-node serving shapes (replicated-load-balanced, sharded, scatter/gather, FaaS, ownership-elected), the work-queue and event-driven batch patterns for asynchronous workloads, and the deployment mechanics (blue/green, canary, rolling, progressive, feature-flagged) that move new versions into production. Start here when the question is "what shape should this service be, how should its containers compose, and how do I roll new versions out safely?" rather than "what SLO should it promise and how do I observe it?" (that's [[moc-reliability-and-operations]]) or "how should services communicate via events?" (that's [[moc-events-and-streaming]]).

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have a service (or one coming) and you're making construction decisions. Maybe you're wrapping a legacy binary and wondering where TLS termination lives. Maybe you're sharding a stateful cache and staring at the rebalance story. Maybe your async workload is outgrowing "one VM with a cron loop" and you need a real work-queue shape. Maybe a release keeps causing outages and you want the deploy mechanics that would have caught it at 1% traffic instead of 100%. Maybe you're picking between a monolithic serving tier and a fan-out/gather scheme because p99 is ugly.

The canonical shape of a question that lands here: *"Where should rate limiting live — in the app or as a sidecar?"*, *"Is this workload a replicated load-balanced service, a sharded service, or scatter/gather?"*, *"Should we adopt a master-election pattern or just run a singleton?"*, *"What's the right deployment strategy for a schema change?"*, *"How do I compose legacy monitoring with Prometheus-shaped scraping?"*, *"Is this workload a FaaS or a long-running service?"*

Jurisdictional rule for this MOC:

- **This MOC** owns the *shape and lifecycle mechanics* of a service — how containers compose inside a node, how service instances are multiplied and specialised across nodes, how asynchronous work is dispatched and collected, and how a new version replaces an old one in production. Burns's *Designing Distributed Systems* is the spine of the catalogue; deployment patterns are the complementary mechanics.
- [[moc-reliability-and-operations]] owns the *operational promise* built on top — SLOs, observability, on-call, postmortems, cascading-failure dynamics, capacity planning, incident response. Deployment patterns are a shared page set: this MOC owns them as *mechanism* (what blue/green does, what a canary is); the reliability MOC owns them as *safety practice* (how to use progressive delivery to protect an error budget).
- [[moc-distributed-systems]] owns the *systems-level mechanics* under ownership election, sharding, and replication — consensus, fencing tokens, quorums, replication strategies. This MOC cites [[ownership-election-pattern]] and [[sharded-service-pattern]] under a *container-level construction* lens; the distributed-systems MOC owns them under a *mechanism and failure-mode* lens.
- [[moc-events-and-streaming]] owns events as the *integration substrate between services* — brokers, event design, choreography vs orchestration. This MOC owns FaaS, work queues, and event-driven batch as *serving shapes*; the events MOC owns the cross-service event fabric they plug into.
- [[moc-microservices]] owns the *organisational and architectural frame* around a services fleet — ownership, reuse, granularity, service mesh as platform tax. This MOC owns the container-level construction of each service; the microservices MOC owns what a team does with the result.
- [[moc-data-processing]] owns the *execution mechanics* of batch and streaming engines — Spark, Flink, scheduler internals, pipeline topologies. This MOC owns Burns's container-level batch patterns (work queue, event-driven batch, coordinated batch) as serving-tier constructions; the processing MOC owns the engine-internal treatment.

Shared pages (ownership-election, sharded-service, deployment patterns, FaaS) are linked here under their *shape-and-mechanics* lens. Follow the sibling MOCs for the other lenses.

## Containers — the primitive

Before any of the patterns, internalise why containerisation is what makes the rest of this MOC tractable. A pattern is only reusable if its implementation and interface are well-bounded; containers give you exactly that boundary.

- [[containers]] — the unit of packaging and isolation that makes the rest of the book's patterns possible. Without the container boundary, "sidecar" is an ambiguous shell-script; with it, the pattern is a precise object with a well-defined interface.
- [[pod]] — a group of containers scheduled together on one node with shared localhost and shared volumes. The substrate for every single-node pattern below; the thing sidecars attach to.
- [[modular-reusable-containers]] — the design goal the patterns deliver. Each container does one thing; interfaces are explicit; composition is cheap; swap-out is trivial. The "class library" analogy Burns uses throughout.
- [[information-hiding]] — the old idea resurfaced at the container layer. A container exposes an interface and hides its implementation; sidecars, ambassadors, and adapters are all specialisations of the same information-hiding move.
- [[legacy-modernization]] — the pragmatic case for sidecars. Wrap an old binary with a modern container that adds TLS, monitoring, config-sync, or leader election without modifying the legacy code.
- [[container-management-system]] — the orchestrator that turns a pattern declaration into running containers with rescheduling, scaling, health-checking. Kubernetes is the assumed substrate; Borg is its ancestor ([[borg]]).
- [[desired-state-management]] — the control-loop model that makes patterns declarative: "I want 5 replicas spread across 3 zones" rather than "SSH to each host and start a process." The property that lets the patterns below be described as config rather than code.

Deeper reading: [[designing-distributed-systems]] for Burns's opening framing — why patterns in distributed systems were stuck without a common packaging primitive until containers arrived.

## Single-node multi-container patterns

The first family: multiple containers scheduled together on one node, composed via shared network namespace and shared volumes. These are the patterns that let you extend or adapt a service without touching its code.

### Sidecar — extending a container

- [[sidecar-pattern]] — the canonical single-node pattern: add a helper container to an existing one to augment or improve it. Adds HTTPS termination, config reload, log tailing, or leader election *without* changing the main container. The default answer for "how do I add X to this service without forking its code."
- [[ssl-termination]] — the motivating example. A legacy HTTP server gets a nginx sidecar that terminates TLS on port 443 and forwards cleartext to the main container on localhost. The code of the main service is unchanged.
- [[health-check-adapter]] — a sidecar case where the main container's native health check is useless (always returns 200) and the sidecar runs meaningful probes (real SQL query, real cache hit) and exposes a Kubernetes-compatible `/healthz`. The bridge between a legacy app's notion of "alive" and the orchestrator's.

Deeper reading: [[designing-distributed-systems#chapter-2-the-sidecar-pattern]].

### Ambassador — proxying outbound communication

- [[ambassador-pattern]] — a sidecar specialised for *outbound* communication. The main container talks to localhost; the ambassador translates that into real-world complexity (sharding, service discovery, circuit breaking, protocol translation). The pattern that lets the main container stay ignorant of where its dependencies are and how to reach them.
- [[client-side-sharding]] — ambassadors as shard routers. The main container does `GET localhost:6379/key`; the ambassador hashes the key and routes to the correct Redis shard. Shard topology changes land in the ambassador only.
- [[service-brokering]] — ambassadors as service discovery. The main container talks to `localhost:8080`; the ambassador resolves that to a real backend, applying circuit-breakers, retries, and fallback policies. Precursor to (and a good conceptual introduction for) the service mesh.
- [[request-splitting]] — an ambassador can fan a single inbound call out to two backends (A/B, shadow, dark launch) and aggregate/pick the response. The traffic-shaping side of the pattern.

Deeper reading: [[designing-distributed-systems#chapter-3-ambassadors]].

### Adapter — normalising outbound interfaces

- [[adapter-pattern]] — a sidecar specialised for *adapting the main container's external interface* to what the rest of the system expects. The main container exposes whatever logs, metrics, or health checks it natively has; the adapter normalises them into the standard shape the platform requires.
- [[unified-monitoring-interface]] — the canonical example. Legacy app emits JMX, Prometheus, or custom text; adapter exposes `/metrics` in Prometheus text format. The main container stays unchanged; the platform sees a homogeneous metrics surface.
- [[log-normalization]] — adapter that reshapes arbitrary stdout into structured JSON with tenant, service, and trace IDs. The reason your log pipeline can be a single Fluentd config rather than N per-service ones.

Deeper reading: [[designing-distributed-systems#chapter-4-adapters]].

## Replicated serving shapes

Once you leave the single-node patterns behind, the question is how to multiply and specialise service instances across a cluster. Four shapes cover the vast majority of serving workloads.

### Replicated stateless services

The default. If your service is stateless (or can be made so by pushing state to a backing store), replicate it behind a load balancer and you're done.

- [[replicated-load-balanced-service]] — N identical stateless replicas behind a load balancer; scale horizontally with the cluster. The one pattern every web service you've ever built already uses.
- [[health-probes]] — readiness and liveness probes are the load balancer's and orchestrator's only view into whether a replica should take traffic. Get these wrong and you end up sending traffic to replicas that can't serve it, or killing replicas that are fine.
- [[session-tracked-services]] — the compromise: deterministic routing of a given session to a specific replica (usually by source-IP hashing or cookie). Cheaper than real session replication; loses the session if that replica dies. The pattern behind "sticky sessions."
- [[caching-layer]] — the replicated service's front-door optimisation. A Redis / Memcache tier in front of the stateless replicas that turns popular reads into microsecond hits. Sits naturally with [[sharded-cache]] when the working set exceeds a single node's memory.
- [[rate-limiting]] — another ubiquitous front-door responsibility. Often a sidecar or ambassador; sometimes a dedicated tier. The point where you protect the rest of the service from abusive or mis-configured clients.
- [[scaling-approaches]] — vertical (bigger machines) vs horizontal (more replicas). Replicated-load-balanced services are the argument for horizontal; stateful databases are often still the argument for vertical. Know why.

Deeper reading: [[designing-distributed-systems#chapter-5-replicated-load-balanced-services]].

### Sharded services

When a single node can't hold all your state, partition it. The shape is orthogonal to replication — you can shard without replicating, replicate without sharding, or do both.

- [[sharded-service-pattern]] — Burns's container-level take on partitioning. Requests are routed to the shard that owns the relevant key; each shard is a serving instance with its own slice of state. The container-level echo of [[partitioning]] and [[partitioning-strategies]] in the storage MOC.
- [[shard-key-selection]] — the decision that constrains everything else. Poor choice → hot spots, cross-shard queries, painful rebalancing. Good choice → even load, local queries, incremental growth.
- [[hot-sharding]] — Burns's name for celebrity-load and temporal-skew failure modes at the container level. Mitigations are the usual suspects ([[hot-spots]] from the storage MOC covers the theory): key salting, hotkey replication, adaptive sampling.
- [[sharded-cache]] — the cache version of the sharded-service pattern. Hit ratios and rebalance cost dominate; small shard-count changes can invalidate huge fractions of the cache. Read alongside [[consistent-hashing]] to understand the standard mitigation.
- [[replicated-sharded-service]] — composition: each shard is itself a replicated-load-balanced service. The production shape of almost every at-scale stateful system. Also the place where [[ownership-election-pattern]] becomes non-optional.

Deeper reading: [[designing-distributed-systems#chapter-6-sharded-services]].

### Scatter/gather — fan-out aggregation

- [[scatter-gather-pattern]] — broadcast a request to many leaf shards, each computes on its slice, the root aggregates. The shape behind search, multi-shard analytical queries, and any "map-reduce but online" pattern. Embarrassingly parallel at the leaf; latency-bound by the slowest leaf.
- [[tail-latency-amplification]] — the defining failure mode. If a single leaf's p99 is 100ms, a 100-leaf scatter/gather's p99 is dominated by the *worst* leaf of 100 — which, empirically, is much worse than 100ms. Hedged requests, backup requests, and reducing leaf-count are the usual mitigations.

Deeper reading: [[designing-distributed-systems#chapter-7-scatter-gather]].

### Ownership election — coordinated singleton scaling

When the work can't be parallelised arbitrarily (one consumer of a partition, one periodic task, one leader-of-a-replica-set), use ownership election rather than sharding or replication.

- [[ownership-election-pattern]] — scale *assignment* rather than requests or state. Elect a master among replicated instances; handle handoff; defend the brief-both-master window. The container-level construction of the same problems the distributed-systems MOC owns at the protocol level.
- [[singleton-pattern]] — the pattern Burns opens with, and the one you should reach for first. A single replica under Kubernetes is 3-to-4 nines out of the box. If that suffices, stop. Only escalate to master election if you actually need faster failover than the orchestrator provides.
- [[distributed-locks-on-kv-stores]] — the Chapter 9 construction of the lock a master-election depends on. CAS + TTL + resource-versions, arriving at the same [[fencing-tokens]] story DDIA derives from theory. Read for the subtle naive-implementation bugs.
- [[renewable-leases]] — the practical ownership-refresh scheme: short TTL, refreshed every `ttl/2` by a background thread; self-terminate-and-let-orchestrator-restart on lost lock.
- [[operator-pattern]] — application-specific controller embedded in Kubernetes; packaged operational expertise. The pattern under etcd-operator, Prometheus-operator, and most stateful-workload Helm charts.

Deeper reading: [[designing-distributed-systems#chapter-9-ownership-election]]. See also [[moc-distributed-systems]] for the consensus / fencing / leader-election theory underneath.

## Functions and event-driven serving

FaaS is a different serving shape: no long-lived container, per-request billing, the platform owns scaling. Know when it's the right answer and when it's a trap.

- [[functions-as-a-service]] — the serverless serving shape: a function is invoked in response to an event, scaled by the platform, billed per invocation. Lambda, Cloud Functions, Azure Functions. Great for spiky low-latency work; awful for long-running, stateful, or high-RPS work where container cold starts and per-call overhead dominate.
- [[serverless-vs-event-driven]] — the clarifying distinction. Serverless is a *billing and scaling* model; event-driven is an *integration pattern*. They combine in FaaS but are independent; a long-running container can be event-driven, a FaaS function can be HTTP-triggered. Know which benefit you actually want.
- [[faas-decorator-pattern]] — FaaS functions composing as chains or fan-outs with per-function middleware (auth, validation, enrichment). The FaaS-native analogue of middleware stacks in a traditional web framework.
- [[event-pipeline-pattern]] — FaaS-specific pattern: each function consumes from one queue and produces to another, forming a DAG. The serverless reshape of an ETL pipeline. See [[moc-data-processing]] for the longer-running-engine version.

Deeper reading: [[designing-distributed-systems#chapter-8-functions-and-event-driven-processing]].

## Work queues and asynchronous batch serving

Async work — *this task should eventually complete, not this request should return by now* — is a different serving shape from anything above. Burns treats it as three stacked patterns.

### Work queue — the base shape

- [[work-queue-pattern]] — the canonical async shape: a source of work items, a queue, a pool of workers. The workers are containerised; scaling is horizontal; backpressure is natural because the queue is the shock absorber. The shape behind thumbnail generation, email sending, ML-inference batches, every "do this later" workload.
- [[source-container-interface]] — the contract between the work-queue platform and whatever is producing items (HTTP source, cron source, Kafka source, etc.). Swappable source implementations let the same worker pool consume from different event types.
- [[worker-container-interface]] — the contract between the platform and the worker: how items are delivered, how completion is acknowledged, how retries are signalled. A stable interface is what lets the worker be written in any language and the platform be written once.
- [[dynamic-worker-scaling]] — autoscale on queue depth, not CPU. The correct signal for async work is backlog; CPU-based scaling reacts too late and doesn't catch queues that grow while workers are idle (e.g., slow downstream).
- [[multi-worker-pattern]] — composition: a single inbound item fans out to multiple specialised worker pools (resize image + generate thumbnail + extract EXIF + run content-safety model). A bridge from simple work-queues toward full pipeline DAGs.

Deeper reading: [[designing-distributed-systems#chapter-10-work-queue-systems]].

### Event-driven batch processing

Work queues where the item isn't independent but is shaped by per-stage transformation logic. Burns's catalogue of reusable batch-processing containers.

- [[event-driven-batch-pattern]] — the umbrella pattern: batch processing built from reusable containerised stages, wired via pub/sub infrastructure. The reason the stages below each have a container-level concept page.
- [[copier-pattern]] — duplicate every input event onto multiple downstream topics. The fan-out primitive.
- [[filter-pattern]] — emit an input only if it matches a predicate. Cheap classification and routing.
- [[splitter-pattern]] — split a single input into multiple outputs based on content (e.g., image → thumbnails-to-topic-A, metadata-to-topic-B). Decomposition primitive.
- [[sharder-pattern]] — route inputs to one of N downstream topics by hashing a key. Partitioning primitive.
- [[merger-pattern]] — combine inputs from multiple topics into one. Join primitive at the batch-stage layer.
- [[publisher-subscriber-infrastructure]] — the pub/sub substrate under all of the above. Kafka is the usual answer; the pattern works with any durable pub/sub.

Deeper reading: [[designing-distributed-systems#chapter-11-event-driven-batch-processing]]. See also [[moc-events-and-streaming]] for the same substrate viewed as cross-service integration rather than batch-stage wiring, and [[moc-data-processing]] for the stream-engine view.

### Coordinated batch processing

When stages can't be composed purely by pub/sub because they need to synchronise — join two streams by key, reduce across a window.

- [[coordinated-batch-pattern]] — patterns where stages have to coordinate, not just forward. The step up from pub/sub-wired stages into MapReduce-shaped topologies.
- [[join-pattern]] — merge two streams on a common key; the map-side-join or reduce-side-join distinction; state and watermarks.
- [[reduce-pattern]] — aggregate many inputs into one output (count, sum, top-N). The classic MapReduce reduce phase expressed as a container pattern.

Deeper reading: [[designing-distributed-systems#chapter-12-coordinated-batch-processing]]. The stream-engine version of the same problems lives in [[moc-data-processing]] — when you want these at production scale, you're usually picking between "roll your own with these patterns" and "use Flink/Spark/Beam."

## Deployment patterns

The mechanics that move a new version of a service into production. This section owns *what each mechanism is and does*; [[moc-reliability-and-operations]] owns *the operational safety discipline* — progressive delivery as an error-budget practice, canary analysis as an SLO protection mechanism. Most of these pages are linked from both MOCs with different framing sentences.

### Deployment-vs-release — the foundational distinction

- [[deployment-vs-release]] — deploying a binary and releasing its functionality are separate concerns. Dark-launched code runs in production without being exposed; feature-flag-gated code is deployed in the "off" state and released by toggling the flag. The distinction that makes every other pattern below cleaner.
- [[independent-deployability]] — a service is independently deployable if you can ship a new version of it *without* coordinating releases across other services. The defining property of a microservice; the property the rest of this section's patterns exist to protect.
- [[deployability]] — a broader architectural characteristic. The "-ility" that scores how fast and safely a system can move code to production. Fits into [[moc-architecture-fundamentals]]'s -ilities catalogue.

### In-place vs side-by-side rollouts

- [[basic-full-stop-deployment]] — stop everything, replace binaries, start everything. The mechanism that works only for low-traffic services with generous maintenance windows. Listed here mostly as the anti-pattern every other pattern improves on.
- [[rolling-update-pattern]] — replace instances a few at a time behind the load balancer; the default for replicated-load-balanced services. Breaks when the new version has a schema or wire-protocol incompatibility with the old — use blue/green instead.
- [[blue-green-deployment]] — two identical environments; deploy the new version to the idle one; switch the router; keep the old one running as the rollback. Expensive (2x capacity during transition), safe (atomic cutover, instant rollback), the right answer for schema-incompatible changes when rolling-update won't work.
- [[breaking-schema-deployment]] — the dedicated pattern for schema-incompatible rollouts: expand (additive schema change + dual-read code), migrate, contract (drop the old schema). The discipline that lets you ship schema changes without downtime. Read alongside [[moc-data-models-and-storage]]'s schema-evolution content.

### Gradual exposure — canary and progressive

- [[canary-test]] — route a small fraction (1%, 5%) of traffic to the new version; watch for SLO regressions; promote or roll back. The cheap-to-build version of what modern platforms call progressive delivery. [[moc-reliability-and-operations]] owns the SLO-budget framing; this MOC owns the traffic-routing mechanism.
- [[progressive-delivery]] — automated canary: progressively increase the percentage of traffic to the new version while a monitoring system evaluates SLI-based gates. Roll back on gate failure. The Flagger / Argo Rollouts / LaunchDarkly-style-automation story.
- [[gradual-rollout]] — the generalisation: any mechanism that exposes a change to a growing cohort of users or traffic over time. Canary is one implementation; feature-flag-based percentage rollouts are another; geographic staged rollouts are a third.

### Feature flags and decoupled release

- [[feature-toggle]] — the page for what a feature toggle *is* — a runtime switch that gates a code path without a redeploy. Four canonical types: release, experiment, ops, permission. The primitive under every "deploy Tuesday, release Thursday" story.
- [[feature-flag-framework]] — productionising feature toggles: flag registry, evaluation SDK, targeting rules, rollout-percentage support, logging, kill-switch semantics. LaunchDarkly / Split / Flagsmith productise this; in-house versions are common. The infrastructure that makes dozens or hundreds of flags manageable.

### EDM-specific deployment considerations

Event-driven microservices add their own rollout constraints — the broker's schema is a contract shared across producers and consumers; producers and consumers deploy independently but must stay compatible.

- [[edm-deployment-patterns]] — the EDM-specific catalogue. Schema evolution on the event broker; producer-first vs consumer-first rollouts; dual-write during schema transitions.
- [[edm-deployment-principles]] — the principles under the catalogue: backward compatibility by default; no breaking changes without a dual-publish window; the schema registry as a gate.

### Release engineering as discipline

The mechanisms above live inside the release-engineering discipline — how a team builds the pipeline, picks a cadence, and treats releases as a first-class engineering artifact.

- [[release-engineering]] — SRE Ch 8 hub: release engineering as a discipline distinct from both development and operations. Build configuration, automation, release protocol, rollback, postmortem feedback.
- [[release-engineering-principles]] — self-service model, high velocity, hermetic builds, enforcement of policies. The principles that scale a release pipeline from "a senior engineer pushes the button" to "any engineer can ship on any day."
- [[release-simplicity]] — the principle that releases should be small, frequent, and boring. The opposite of the quarterly-big-bang release — and the prerequisite for most of the safety mechanisms above to work.
- [[release-branching-and-cherry-picking]] — the Git workflow under release engineering: main-branch development, release branches cut on a cadence, cherry-picks for hotfixes. The mechanism under "deploy what's tested, not what's current."
- [[release-policy-enforcement]] — policy as code: what gates must pass (tests, canary, signoff) before a release is permitted. The thing that stops "I'll skip the canary this once."
- [[self-service-release-model]] — the end state the other principles build toward: any engineer can release any service at any time because the pipeline and gates are self-service infrastructure, not shared-resource bottleneck.
- [[continuous-integration-delivery-deployment]] — the three-letter-acronym spectrum: CI (merge and test often), CD-delivery (always-releasable artifact), CD-deployment (automatic release to prod on green main). The vocabulary map for "what does your deployment pipeline do."
- [[hermetic-builds]] — builds that produce byte-identical output from the same source and dependencies, regardless of host or time. The property that makes "rebuild the release tag" trustworthy and rollback-by-artifact-reuse possible.
- [[high-release-velocity]] — the argument that higher release frequency improves *safety*, not reduces it. Small changes fail less often and fail smaller; the mechanisms above are what make high velocity achievable.
- [[rapid-release-system]] — Google's release frequency — push-on-green for some services, daily for others. The existence proof for the principles above.

Deeper reading: [[site-reliability-engineering#chapter-8-release-engineering]]. See [[moc-reliability-and-operations]] for the launch-coordination, reliable-product-launch, and pre-production-review disciplines that wrap around the release mechanics above.

## Pattern selection — which shape for what workload?

The catalogue is wide; the selection rule is usually narrow. Ask these questions in order:

1. **Is it stateless and simple?** Replicated-load-balanced service. Stop here if it works.
2. **Does the state exceed one node?** Shard. Compose with replication ([[replicated-sharded-service]]) once per-shard durability matters.
3. **Does a single query need to touch many shards?** Scatter/gather. Watch for [[tail-latency-amplification]].
4. **Is the work async — "eventually complete" rather than "return by now"?** Work queue. Escalate to event-driven batch if there are multiple stages; coordinated batch if stages must synchronise.
5. **Is there exactly one thing that must run at a time?** Singleton first. Ownership election only if failover latency matters more than the orchestrator's native restart.
6. **Is load spiky and short-lived?** FaaS — after you've confirmed cold starts are acceptable and per-call billing is favourable.
7. **Does the main container need something it doesn't provide?** Sidecar (augment), ambassador (outbound proxy), adapter (interface normalisation). In that order of likelihood.

Each of these decisions is reversible but usually expensive to reverse; get it approximately right before committing. The shape you pick here constrains every operational story [[moc-reliability-and-operations]] has to build on top.

## Sibling MOCs

- [[moc-reliability-and-operations]] — owns the operational promise *on top of* the shapes in this MOC. Deployment patterns appear in both: this MOC owns what they are; the reliability MOC owns using them safely. Read end-to-end before a non-trivial rollout.
- [[moc-distributed-systems]] — owns the consensus, replication, partitioning, and fencing mechanisms under the ownership-election, sharding, and replication patterns above. This MOC builds the containers; that MOC explains why the coordination works (or fails).
- [[moc-microservices]] — owns the organisational frame around a services fleet. This MOC owns each service's shape; the microservices MOC owns how the fleet is organised, governed, and coupled.
- [[moc-events-and-streaming]] — owns events as cross-service integration substrate. This MOC's FaaS, work queue, and event-driven batch patterns plug into the broker the events MOC describes.
- [[moc-data-processing]] — owns the stream-engine and pipeline-scheduler view of batch. This MOC owns the container-level batch patterns; the processing MOC owns Spark/Flink/Beam as the industrial-strength alternative.
- [[moc-decomposition]] — owns the extraction playbook. The shapes in this MOC are the destination a decomposition targets; [[why-microservices]] and [[independent-deployability]] sit on the boundary between the two MOCs.

## Related pages

- [[index]]
- [[designing-distributed-systems]]
- [[site-reliability-engineering]]
- [[containers]]
- [[pod]]
- [[modular-reusable-containers]]
- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[replicated-load-balanced-service]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[scatter-gather-pattern]]
- [[functions-as-a-service]]
- [[ownership-election-pattern]]
- [[singleton-pattern]]
- [[work-queue-pattern]]
- [[event-driven-batch-pattern]]
- [[coordinated-batch-pattern]]
- [[blue-green-deployment]]
- [[rolling-update-pattern]]
- [[canary-test]]
- [[progressive-delivery]]
- [[feature-toggle]]
- [[feature-flag-framework]]
- [[deployment-vs-release]]
- [[independent-deployability]]
- [[release-engineering]]
- [[hermetic-builds]]
- [[continuous-integration-delivery-deployment]]
