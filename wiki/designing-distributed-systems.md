# Designing Distributed Systems

**Summary**: Brendan Burns's pattern catalogue for building reliable distributed systems out of containers and container orchestrators. The book argues that just as the "Gang of Four" formalized object-oriented design patterns, containers and orchestrators (Kubernetes in particular) have made it possible to formalize reusable, language-agnostic patterns for distributed systems.

**Sources**: `raw/designing-distributed-systems/`

**Last updated**: 2026-04-16
---

## About the book

Brendan Burns is a co-founder of Kubernetes and a Corporate Vice President at Microsoft. *Designing Distributed Systems* (O'Reilly, 2018) presents distributed systems as collections of reusable patterns implemented as containers connected via HTTP-style interfaces, the way OOP made it possible to ship Gang-of-Four patterns as language libraries.

The book is organized into three parts:

1. **Single-Node Patterns** — tight multi-container groupings (Kubernetes pods) running on one machine: sidecar, ambassador, adapter.
2. **Serving Patterns** — long-lived multi-node serving systems: replicated load-balanced services, sharded services, scatter/gather, functions / event-driven (FaaS), ownership election.
3. **Batch Computational Patterns** — finite computations over large inputs: work queues, event-driven batch pipelines, coordinated batch processing (join, reduce, coordinator).

The emphasis throughout is on *pattern vocabulary* and *container-level composition*: every pattern is a blueprint that can be implemented with off-the-shelf containers and reused across languages. Container orchestrators — Kubernetes is the running example — are the substrate that makes these patterns operationally real.

Across the three parts the recurring payoff is the same: naming a pattern turns opaque deployments into readable blueprints and turns bespoke glue code into a composition of reusable containers. The book closes (Chapter 13) by reiterating that the pattern catalogue is deliberately open-ended — a starting vocabulary for a new era of distributed systems engineering rather than a finished canon.

## Ingestion status

| Chapter | Title | Status |
|---|---|---|
| 1 | Introduction | Skipped (introductory front matter) |
| 2 | The Sidecar Pattern | Ingested 2026-04-16 |
| 3 | Ambassadors | Ingested 2026-04-16 |
| 4 | Adapters | Ingested 2026-04-16 |
| 5 | Replicated Load-Balanced Services | Ingested 2026-04-16 |
| 6 | Sharded Services | Ingested 2026-04-16 |
| 7 | Scatter/Gather | Ingested 2026-04-16 |
| 8 | Functions and Event-Driven Processing | Ingested 2026-04-16 |
| 9 | Ownership Election | Ingested 2026-04-16 |
| 10 | Work Queue Systems | Ingested 2026-04-16 |
| 11 | Event-Driven Batch Processing | Ingested 2026-04-16 |
| 12 | Coordinated Batch Processing | Ingested 2026-04-16 |
| 13 | Conclusion: A New Beginning | Skipped (conclusion) |

## Chapter 2 concepts

Chapter 2 introduces the **sidecar pattern** as the first of the single-node patterns. Its thesis: two coscheduled containers — an application container plus a sidecar — can add capability to an application through a separate deployable unit instead of through source changes. That opens two doors: adapting legacy applications that are too expensive to modify, and building reusable utility containers (introspection, TLS termination, config sync, git-pull-based PaaS) that any application can compose with. The chapter closes with a design discipline for sidecars to be truly reusable: parameterize, define the API surface, document.

Pages created from this chapter:

- [[sidecar-pattern]] — the two-container pattern itself; shared namespaces; four worked examples (HTTPS, config sync, `topz`, git-PaaS); motivations
- [[pod]] — atomic container group with shared namespaces; the substrate that makes sidecars work
- [[modular-reusable-containers]] — the three-part discipline: parameterize, API surface, document; subtle breaking changes
- [[legacy-modernization]] — using sidecars to extend legacy applications without changing their source

Existing pages augmented: [[service-mesh]] (positioned as a large-scale sidecar deployment), [[information-hiding]] (sidecars as deployment-layer information hiding).

## Chapter 3 concepts

Chapter 3 introduces the **ambassador pattern**, the second of Burns's single-node patterns. An ambassador container brokers the *outbound* connections of the application container — taking sharding, service discovery, and request-splitting logic out of the application process and into a coresident proxy. The application connects to what it believes is a single backend on `localhost`; the ambassador applies whatever outward-facing logic the deployment needs. Like the sidecar, the pattern pays off in modularity and reuse: twemproxy fronting sharded Redis, nginx splitting 10% of traffic to an experiment, and off-the-shelf service brokers can be dropped in front of any application. Burns recurrently flags the client-side ambassador vs server-side proxy-tier trade-off: either is valid, and the right answer depends on how longstanding the logic is and where team boundaries fall.

Pages created from this chapter:

- [[ambassador-pattern]] — the core pattern; three canonical uses (sharding, service brokering, request splitting); the client-side / server-side trade-off; relationship to sidecars and service mesh
- [[client-side-sharding]] — using an ambassador to proxy to a sharded backend; the twemproxy/Redis/ketama worked example; relationship to DDIA's request-routing options
- [[service-brokering]] — ambassador as service-discovery client; the MySQL-across-environments example; relationship to service mesh
- [[request-splitting]] — ambassador for canary, dark launch, and tee/parallel-run traffic; the 10%-experiment nginx worked example

Existing pages augmented: [[sidecar-pattern]] (ambassador cross-reference and distinction), [[pod]], [[modular-reusable-containers]] (ambassadors share the discipline), [[service-mesh]] (ambassador as the outbound primitive), [[service-discovery]], [[request-routing]], [[consistent-hashing]] (ketama), [[partitioning]], [[parallel-run-pattern]], [[progressive-delivery]].

## Chapter 4 concepts

Chapter 4 completes the Part I trilogy with the **adapter pattern**: a coresident container that transforms the interface an application container exposes so it matches a uniform standard that fleet tooling expects (monitoring, logging, health checks). The thesis is the heterogeneity argument: real-world deployments assemble code written in-house, by vendors, and off-the-shelf open source in many languages with many conventions; a single tool for monitoring, logging, or health probing presupposes a single interface; the adapter container provides that translation without modifying the application image. Burns's three canonical applications — a Prometheus exporter for Redis, a fluentd adapter normalising logs from Redis and Storm, and a Go adapter running representative SQL against MySQL — are all structurally the same: application's native interface inward, fleet-standard interface outward. The closing note in the chapter is unusually broad: adapters are structurally friendly to community contribution, and the pattern becomes a mechanism for packaging and sharing operational expertise.

Pages created from this chapter:

- [[adapter-pattern]] — the core pattern; the heterogeneity problem; why not just modify the application; full trilogy comparison with sidecar and ambassador
- [[unified-monitoring-interface]] — adapter applied to monitoring; the Redis + `redis_exporter` + Prometheus worked example; pull-style fit
- [[log-normalization]] — adapter applied to logging; fluentd + `fluent-plugin-redis-slowlog` and `fluent-plugin-storm` worked examples; converting ephemeral server state into queryable logs
- [[health-check-adapter]] — adapter applied to orchestrator health probes; the Go + MySQL worked example; modularity argument against forking the upstream image

Existing pages augmented: [[sidecar-pattern]] and [[ambassador-pattern]] (adapter sibling cross-reference, trilogy table), [[pod]] (adapter to Related), [[modular-reusable-containers]] (adapters apply too), [[monitoring-and-observability]] (adapter pattern as container-level mechanism), [[log-aggregation]] (adapter as the normalisation step), [[service-mesh]] (adapter role within the mesh story), [[information-hiding]] (adapters as deployment-layer information hiding), [[legacy-modernization]] (adapters complement sidecars for observability).

## Chapter 5 concepts

Chapter 5 opens Part II of the book — the Serving Patterns — with the **replicated load-balanced service**, the simplest multi-node pattern and the foundation all the other serving patterns build on. Its thesis: a stateless service replicated behind a load balancer is horizontally scalable and highly available by default, provided you also deploy the machinery that makes the load balancer behave correctly — especially a **readiness probe** that keeps unfinished replicas out of the pool. From there, the chapter develops two refinements of the base pattern: **session tracking** (when per-user affinity is needed, implemented via IP hash inside the cluster and via cookies/headers across NAT or upstream proxies, with consistent hashing to minimise disruption during scaling) and **application-layer replicated tiers** (stacking replicated load-balanced services on top of each other — a caching tier in front of the app, an SSL-terminating tier in front of the cache — to add capability without changing either the inner or outer tier).

The chapter also draws a sharp operational line between liveness and readiness probes (the orchestrator restarts on liveness failure; the load balancer deregisters on readiness failure), discusses why cache tiers should be few-and-large rather than many-and-small, flags the subtle interaction between caching and IP-based session affinity, and treats rate limiting and SSL termination as pluggable features of the edge tier.

Pages created from this chapter:

- [[replicated-load-balanced-service]] — the core pattern; stateless replicas behind a load balancer; the two-replica-minimum SLA argument; composition into stacked tiers
- [[health-probes]] — liveness vs readiness; why they answer different questions; Kubernetes implementation; relation to the Chapter 4 health-check adapter
- [[session-tracked-services]] — sticky sessions via IP hash and via cookies/headers; why NAT and upstream proxies break IP affinity; why consistent hashing is the default
- [[caching-layer]] — Varnish as a replicated HTTP cache tier; the few-large-replicas sizing rule; why cache-as-sidecar is usually wrong; the cache + session-tracking interaction
- [[rate-limiting]] — DoS defence at the edge; 429 and X-RateLimit-Remaining; anonymous vs authenticated quotas
- [[ssl-termination]] — the nginx edge tier; per-layer certificates for independent rollouts; the full three-tier stack

Existing pages augmented: [[scaling-approaches]] (horizontal stateless scaling as the textbook case), [[consistent-hashing]] (session affinity as another CDN-style use), [[sidecar-pattern]] (cache-as-sidecar as a worked when-not-to-use example), [[service-mesh]] (mesh proxies as the fleet-wide implementation of session affinity and edge TLS), [[health-check-adapter]] (readiness-vs-liveness framing added), [[fault-tolerance]] (readiness probes as graceful-degradation substrate).

## Chapter 6 concepts

Chapter 6 is the second serving pattern — the **sharded service**. Where the Chapter 5 [[replicated-load-balanced-service]] had identical stateless replicas sitting behind a round-robin load balancer, a sharded service's replicas each hold a disjoint subset of state, and a **root** examines each request and routes it to the shard that owns it. The thesis: when state outgrows a single machine — Burns's canonical example is a cache whose working set exceeds any one replica's memory — the replicated pattern wastes most of the memory you paid for, and sharding is the answer. Each shard stores unique data, so aggregate cache size grows linearly with shard count.

Burns builds almost the entire chapter around the sharded-cache example because it crystallises every design question at once: the memory-utilisation argument, the hit-rate-as-capacity-multiplier arithmetic, the failure-mode analysis (what happens when a shard dies), the choice of sharding function, the choice of shard key, and the operational penalties of re-sharding a production cache. The chapter then generalises: any stateful service with too-large state — a multiplayer game world partitioned by player location — can be built with the same pattern, just with a different shard key.

Two refinements are treated substantively: the **replicated sharded service** (replace each shard with a Chapter 5-style replicated sub-service for reliability and safe rollouts) and **hot sharding** (autoscale each shard's replica count in response to organic traffic skew — the service-level answer to celebrity-key hot spots). A short section on shard-key selection makes the point that picking what to hash is the interesting design decision, not picking the hash function itself. The chapter's two hands-on deployments (per-pod twemproxy ambassador vs shared shard-routing service) reprise the client-side/server-side trade-off from Chapter 3.

The chapter connects tightly to existing wiki coverage of database partitioning from DDIA: all the DDIA mechanics apply at the service layer, and Burns's chapter contributes the distinct **operational and deployment** perspective — how you build a sharded cache in Kubernetes, what shard rollouts cost, what hot-sharding looks like in practice.

Pages created from this chapter:

- [[sharded-service-pattern]] — the core Chapter 6 pattern; root + shards; comparison with replicated pattern; DDIA-partitioning vocabulary mapping
- [[sharded-cache]] — the chapter's deep-dive worked example; memory-utilisation math; hit-rate as capacity multiplier; criticality analysis
- [[replicated-sharded-service]] — combining Chapter 5 and Chapter 6; failure resilience, safe rollouts, per-shard scaling
- [[hot-sharding]] — autoscaling per-shard replica count in response to organic traffic skew; the service-level hot-spot response
- [[shard-key-selection]] — the "too general / too specific / just right" discussion; `shard(country(request.ip), request.path)` as the worked example

Existing pages augmented: [[partitioning]] (stateful-serving-tier section linking to the Chapter 6 pages), [[consistent-hashing]] (re-sharding-as-cache-flush argument + the nginx `hash $request_uri consistent` example), [[hot-spots]] (hot-sharding as service-level response), [[rebalancing-partitions]] (Burns's naive-`hash % N` warning and per-shard replica rebalancing), [[request-routing]] (the "root" concept and shared-shard-router deployment option), [[client-side-sharding]] (Chapter 6 cross-reference and per-pod vs shared trade-off), [[caching-layer]] (sharded-vs-replicated fork), [[ambassador-pattern]] (Chapter 6 revisits ambassador as sharded-service root), [[replicated-load-balanced-service]] (composition with sharding noted).

## Chapter 7 concepts

Chapter 7 is the third serving pattern — **scatter/gather** — the final piece of the serving-pattern trilogy. Where the [[replicated-load-balanced-service]] replicates for request throughput and the [[sharded-service-pattern]] shards for state size, scatter/gather replicates for **time**: it fans a single request out to many leaves in parallel and combines their partial results, shrinking wall-clock latency by running lots of mostly independent work concurrently. Burns's thesis in the chapter is compact but architecturally important. He walks through two variants (homogeneous leaves with root-distributed work; data-sharded leaves with full fan-out per query), the distributed-document-search worked example for each, and a careful treatment of why increasing the leaf count yields asymptotic rather than linear speedup — per-request overhead scales with leaf count, and the straggler problem means the p99 of the leaf tier becomes the p50 of the user-facing system at modest fan-out. The chapter closes with the standard reliability mitigation: replicate each leaf, so leaf failures degrade performance instead of breaking the gather step.

The chapter is short because the concept is compact, but it ties together several deep threads already in the wiki: DDIA's framing of document-partitioned secondary indexes as scatter/gather reads, MPP parallel query execution, tail-latency amplification in any fan-out system, and the compositional logic of nesting the earlier serving patterns inside each other. Burns's contribution is to name the pattern as a named, standalone architectural element at the serving tier and to surface its load-bearing performance concern (tail amplification) as a first-class design input.

Pages created from this chapter:

- [[scatter-gather-pattern]] — the core pattern; root + leaves + combine step; the two variants (root-distributed work vs leaf-sharded data); the cat-and-dog worked example for both; leaf-count as a design knob; reliability via leaf replication
- [[tail-latency-amplification]] — Burns's 99th-percentile math worked through; straggler framing; availability amplification; mitigations (hedged requests, bounded leaf count, leaf replication, approximate gather); relationship to DDIA's original coverage on [[response-time-percentiles]]

Existing pages augmented: [[response-time-percentiles]] (cross-linked the new tail-latency-amplification page and the serving pattern), [[partitioning-secondary-indexes]] (scatter/gather read path now named as an instance of the scatter-gather pattern), [[partitioning]] (MPP parallel query execution linked to scatter/gather; scatter/gather pages added to Related), [[sharded-service-pattern]] (relationship-to-scatter/gather section expanded and linked bidirectionally), [[replicated-sharded-service]] (replicate-each-leaf fix for scatter/gather reliability noted), [[replicated-load-balanced-service]] (composing with scatter/gather section added), [[hadoop-vs-mpp-databases]] (MPP query execution as scatter/gather at the analytics layer).

## Chapter 8 concepts

Chapter 8 closes the serving-pattern part of the book with **functions-as-a-service** — the fourth and structurally distinct serving pattern. Where the previous three patterns ([[replicated-load-balanced-service]], [[sharded-service-pattern]], [[scatter-gather-pattern]]) all assume long-running server processes, FaaS inverts that assumption: functions come into existence per event, run briefly, and disappear, with the platform handling lifecycle and scaling. Burns's chapter is unusually balanced — about half the space is spent on *when FaaS is a good fit and when it isn't*, which is arguably the more useful content than the patterns themselves.

Burns opens with a terminological clarification that matters for design: **serverless and event-driven are two separate axes**. FaaS happens to combine both, but products exist in all four corners of the matrix, and the benefits you want might sit on only one axis. The benefits of FaaS (no artefacts, no fleet to manage, automatic scaling, automatic fault recovery) come from the serverless axis; the constraints (short runtimes, no in-memory state, pay-per-request billing, hard-to-reason-about distributed behaviour) come from the event-driven axis. Teams that want the programming model without giving up cluster control can run open-source FaaS on their own Kubernetes — Burns's preferred escape hatch when pay-per-request pricing stops pencilling out at high request volumes.

The chapter's fit/no-fit discussion lands on four disqualifiers: long-running background work, services needing warm in-memory state, sustained high-volume request serving, and systems whose cross-function dependencies are hard to reason about (Burns's pathology of a cyclic function chain that runs up arbitrarily large bills is memorable). The fit cases are the mirror image: stateless, short-lived, event-shaped, bursty work — especially the asynchronous augmentations that hang off request-driven systems (welcome emails, two-factor SMS, upload notifications).

Two composition patterns appear: the **FaaS decorator**, a stateless request/response transformer that sits in front of a backend API (Python-decorator analogy; worked example is JSON default-filling for a REST API), and the **event pipeline**, a directed graph of functions connected by webhooks (worked examples: a CI pipeline with human approval in Jira; a new-user signup flow with required and optional handlers). Burns is explicit that the FaaS decorator overlaps with the Chapter 4 [[adapter-pattern]] and handles the overlap head-on: use an adapter container when the transformation should scale with the backend pod; use a FaaS decorator when it should scale on its own axis. The event-pipeline pattern's distinguishing feature versus microservices is the ability to include non-software participants — humans approving tickets, external SaaS firing webhooks.

Pages created from this chapter:

- [[functions-as-a-service]] — the core FaaS pattern; serverless-vs-event-driven distinction; four operational/architectural/economic challenges; the fit/no-fit matrix; relationship to the other three serving patterns; relationship to message brokers, event sourcing, and CDC as event sources; relationship to Newman's serverless-first framing
- [[serverless-vs-event-driven]] — the terminological distinction Burns opens the chapter with; the four corners of the matrix; why the two benefits come from different axes; how to pick the right product
- [[faas-decorator-pattern]] — request/response transformation; the Python-decorator analogy; defaulting worked example (Kubeless); explicit comparison against the [[adapter-pattern]]; other common applications (validation, shimming, backward-compat)
- [[event-pipeline-pattern]] — directed graph of functions connected by webhooks; two worked examples (CI-with-human-approval; new-user signup with required/optional handlers); relationship to microservices, message-brokers, stream-processing, and the saga pattern

Existing pages augmented: [[running-too-many-things]] (Burns's catalogue of FaaS limits now cited as the complement to Newman's serverless-first default), [[desired-state-management]] (Burns's Chapter 8 treatment of FaaS as a serving pattern in its own right now linked), [[decorating-collaborator-pattern]] (FaaS decorator as a natural implementation substrate for Newman's migration pattern), [[adapter-pattern]] (adapter-vs-FaaS-decorator comparison section added), [[event-streams]] (FaaS as an event consumer), [[message-brokers]] (FaaS as a broker consumer; broker+FaaS as the substrate for event pipelines).

## Chapter 9 concepts

Chapter 9 closes the serving-pattern part of the book with **ownership election** — the final multi-node serving pattern and the one that scales **assignment** rather than requests, state, or time. Burns's thesis: when a task must have exactly one owner across a replicated service, don't implement Paxos or Raft yourself; outsource consensus to etcd, [[zookeeper]], or Consul and build the lock/lease/ownership abstractions you need on top of their compare-and-swap + TTL + resource-version primitives.

The chapter's most distinctive contributions are (a) an unusually honest opening argument that **most services don't need master election at all** — a singleton running under Kubernetes is three-to-four nines out of the box and is a serious option; (b) a derive-from-first-principles construction of a distributed lock on etcd that walks readers through the subtle bugs (no TTL = stuck on crash; TTL without version = stale unlock after pause; neither = split ownership undetectable at the worker); and (c) the naming of the **operator** pattern — an application-specific controller running inside Kubernetes, worked through with the CoreOS etcd operator installed via Helm. The chapter's applied defences against the "both replicas think they're master" window (client-side self-check, server-side owner validation, per-request resource versions) are the container-level form of DDIA's [[fencing-tokens]] mechanism, derived from scratch rather than cited as such.

This chapter connects tightly to existing DDIA coverage — [[consensus]], [[zookeeper]], [[fencing-tokens]], [[truth-and-leadership-in-distributed-systems]], [[process-pauses]], [[failover]] — and Burns's perspective complements rather than duplicates it. Where DDIA explains why the problem is hard and why consensus is the right solution, Burns shows how to actually build the thing with commodity containers.

Pages created from this chapter:

- [[ownership-election-pattern]] — the core Chapter 9 pattern; scales assignment; master election + handoff; the do-you-even-need-it test; Burns's two-replicas-briefly-both-master scenario; defences (client self-check, server-side validation, resource versions); relationship to the full DDIA theory stack
- [[singleton-pattern]] — the cheaper alternative Burns opens with; orchestrator-backed single replica; three-to-four-nines uptime arithmetic; the upgrade-window constraint as the binding SLA ceiling; when it's the right call (background async work) and when it isn't
- [[distributed-locks-on-kv-stores]] — the applied construction: CAS + TTL + resource versions; naive-lock-then-fix-the-bugs derivation; watchdog timers; connection to DDIA's [[fencing-tokens]] and [[linearizability]]
- [[renewable-leases]] — long-running ownership; short TTL refreshed every `ttl/2` from a background thread; terminate-and-let-orchestrator-restart as the `handleLockLost` implementation; Kubernetes scheduler as the canonical example
- [[operator-pattern]] — CoreOS's pattern; an online program inside the orchestrator whose job is to manage one application via a custom desired-state API; the etcd-operator-via-Helm worked example; relationship to [[desired-state-management]] and packaging of operational expertise

Existing pages augmented: [[zookeeper]] (container-level perspective; Burns's interchangeability framing; pointer to the lock construction), [[fencing-tokens]] (Burns's applied resource-version-per-request mechanism; the delayed-R1 scenario walk-through), [[truth-and-leadership-in-distributed-systems]] (container-level form of the mitigations), [[failover]] (container-level prescription: decide if you need it, outsource consensus, use renewable leases), [[consensus]] (Burns's "don't implement this yourself" blunt statement), [[process-pauses]] (CPU starvation on overscheduled machines as a concrete scenario), [[desired-state-management]] (operator pattern as the application-specific specialisation), [[health-probes]] (liveness probe as load-bearing for the singleton pattern).

## Chapter 10 concepts

Chapter 10 opens Part III of the book — the **Batch Computational Patterns** — with the **work queue**, the simplest batch pattern. Burns's thesis: when work items are wholly independent of one another (the embarrassingly parallel case), the machinery around them — fetching items, scheduling workers, tracking completion, handling failure — is almost entirely generic. Package it once as a reusable library container and the application-specific parts collapse to two narrow interfaces. The **source container** (an [[ambassador-pattern]] instance) produces items via a simple HTTP REST API on `localhost`; the **worker container** processes one item via a file-based API and exits. Between the two, a generic queue-manager loop plus Kubernetes **Job objects with annotations** provides reliable execution and durable state — the queue-manager itself stores nothing.

The chapter's other substantial contributions are (a) a queueing-theory-flavoured argument for **dynamic worker scaling** based on observed interarrival time and processing time, with the concrete rule that parallelism must exceed `processing_time / interarrival_time` for a stable queue; and (b) the **multi-worker pattern** — a specialisation of the [[adapter-pattern]] in which a single worker-interface slot is implemented by a composition of reusable processing containers (face-detect + identity-tag + blur) behind an aggregator.

This chapter connects tightly to the DDIA-sourced batch coverage already in the wiki ([[batch-processing]], [[mapreduce]], [[dataflow-engines]], [[message-brokers]]) and sits below them in the stack: the work queue is the dispatch-one-item-per-worker primitive that MapReduce composes with partitioning, and that dataflow engines generalise into arbitrary DAGs. Burns's container-level view complements DDIA's algorithmic treatment.

Pages created from this chapter:

- [[work-queue-pattern]] — the core Chapter 10 pattern; generic queue-manager; reusable-container thesis; the two interface split; Kubernetes Jobs as durable state; video-thumbnailer worked example; relationship to MapReduce, message brokers, and FaaS
- [[source-container-interface]] — the ambassador-shaped producer interface; two-endpoint HTTP REST API; deliberate omission of "mark processed"; API versioning discipline; implementation patterns (cloud storage, NFS, Kafka/Redis)
- [[worker-container-interface]] — the file-based, one-shot consumer interface; `WORK_ITEM_FILE` env var and ConfigMap mount; Kubernetes Job as the reliability substrate; idempotence requirement; ffmpeg thumbnailer worked example
- [[dynamic-worker-scaling]] — the three regimes (uncapped, capped, dynamic); interarrival vs processing time math; the `P > processing_time / interarrival_time` rule; the 90%-of-interarrival heuristic for scaling down
- [[multi-worker-pattern]] — adapter-pattern specialisation; aggregator container presenting the standard worker interface outward while delegating inward to reusable processing containers; the face-detect-tag-blur worked example

Existing pages augmented: [[ambassador-pattern]] (work-queue source as a new canonical ambassador use; batch-ingest cross-reference), [[adapter-pattern]] (multi-worker as adapter applied to batch worker composition; adapter-uses table extended), [[batch-processing]] (container-level perspective linked; Burns's work queue positioned as the dispatch primitive below MapReduce), [[message-brokers]] (work queue as a broker-consumer alternative; source-ambassador fronting a topic).

## Chapter 11 concepts

Chapter 11 is the second of Burns's batch computational patterns: **event-driven batch processing**. Its thesis: when a single-transformation [[work-queue-pattern|Chapter 10 work queue]] isn't enough, chain multiple work queues into a **directed acyclic workflow graph** where the output of each stage becomes the input to the next, and the completion of a worker is itself the event that triggers downstream stages. The shape is the same as [[event-pipeline-pattern|Chapter 8's FaaS event pipelines]] — Burns draws the parallel explicitly — but at batch-stage granularity, wired over a pub/sub broker rather than per-event webhooks.

The chapter's load-bearing contribution is a small named vocabulary of **five linking patterns** for composing work queues into workflows. Each is a narrow adapter or ambassador at the seam between queues, and together they cover the recurring topologies that workflow systems need: fan-out (copier), reduction (filter), conditional routing (splitter), even distribution (sharder), and fan-in (merger). Naming them turns opaque graphs into readable blueprints — exactly the payoff Burns highlights, since "without an overall blueprint for how the different event queues relate to each other, it can be hard to fully understand how the system is operating."

The second substantive contribution is pub/sub as the transport layer. Each output stream of each workflow stage is a **topic**; linking-pattern containers publish to and subscribe from topics; the broker handles durability, partitioning, and fan-out. Burns walks through Kafka on Kubernetes via Helm, with `--replication-factor` and `--partitions` as the two load-bearing parameters (which correspond directly to DDIA's [[replication]] and [[partitioning]] mechanics). Azure EventGrid, AWS SQS, and Google Pub/Sub are interchangeable substrates at the pattern level.

The chapter's worked example — the new-user signup workflow — composes sharder, copier, and splitter patterns across two distinct workflow phases (verification-email sharded across failure zones; then post-verification copier fanning to welcome-email + notification-setup, with a splitter routing notifications to email/text/both/neither).

Pages created from this chapter:

- [[event-driven-batch-pattern]] — the hub page; chains [[work-queue-pattern]] instances into DAGs via named linking patterns; pub/sub as transport; the workflow-as-specification payoff; relationship to [[event-pipeline-pattern]] (cousin at FaaS granularity) and [[dataflow-engines]] (cousin at operator granularity)
- [[copier-pattern]] — the fan-out primitive; 1 → N identical streams; video-transcoding worked example; Unix `tee` analogy; relationship to splitter and merger
- [[filter-pattern]] — drop items that don't meet a criterion; ambassador-on-ambassador composition in front of an upstream [[source-container-interface]]; opt-in-user worked example; Unix `grep` analogy
- [[splitter-pattern]] — the routing primitive; items divided across branches by criterion; shipping-notification worked example; subsumes copier (when item goes to multiple branches) and filter (when item goes to no branch); equivalence with copier + two filters
- [[sharder-pattern]] — hash-based even distribution; motivated by reliability (staged rollouts, failure-zone spreading) rather than semantic routing; dynamically routes around unhealthy shards; container-level echo of [[sharded-service-pattern]] and DDIA [[partitioning]]
- [[merger-pattern]] — the fan-in primitive; combines N upstream sources into one; multi-source adapter (mirror image of [[multi-worker-pattern]]); CI-across-many-repos worked example
- [[publisher-subscriber-infrastructure]] — the transport substrate for event-driven batch workflows; Kafka/EventGrid/SQS as interchangeable implementations; Kafka-on-Kubernetes-via-Helm walkthrough; topic-per-output-shard convention; `replication-factor` and `partitions` parameters linked to DDIA replication and partitioning

Existing pages augmented: [[work-queue-pattern]] (composed-workflow section; Related extended; Chapter 11 added to Sources), [[event-pipeline-pattern]] (Chapter 11 batch cousin section added explicitly naming the same topology-as-specification payoff), [[batch-processing]] (Chapter 11 extension after the work-queue section, positioning the pattern as the container-level analogue of dataflow DAGs and workflow schedulers like Airflow / Argo / Prefect), [[dataflow-engines]] (container-level-counterpart section with side-by-side comparison table; Chapter 11 added to Sources), [[message-brokers]] (brokers-as-workflow-transport section; Chapter 11 linking patterns added to Related), [[source-container-interface]] (source ambassador composed as filter pattern; merger mention), [[multi-worker-pattern]] (merger as the mirror-image multi-source adapter), [[adapter-pattern]] (every Chapter 11 linking pattern is an adapter at the seam between queues), [[ambassador-pattern]] (filter as ambassador-on-ambassador composition).

## Chapter 12 concepts

Chapter 12 closes Burns's batch-pattern trilogy with **coordinated batch processing** — the aggregation side of the batch pipeline, pulling parallel workflow outputs back together into a single result. Burns's thesis: Chapter 11's linking patterns are good at splitting and chaining, but they offer no primitive for guaranteeing completeness or combining values, and the [[merger-pattern|merger]] alone is not enough — "it does not ensure that a complete dataset is present prior to the beginning of processing." Chapter 12 supplies two distinct coordination primitives to fill that gap.

The first is the **join pattern** — barrier synchronization, explicitly named after thread-join in concurrent programming. All parallel work happens concurrently, but no item is released downstream until every parallel worker has completed. The join's completeness guarantee is what makes correctness-critical downstream steps possible: destructive operations (Burns's worked example deletes the original images only after the join releases), global aggregates, and cross-phase fences. The cost is straggler-bound latency: the workflow waits for the slowest path.

The second is the **reduce pattern** — the container-level naming of MapReduce's reduce step. A reduce container combines two (or more) parallel outputs into a single output of the same shape, repeatedly, until one aggregate remains. The operation is associative, so reduce steps can be arbitrarily stacked and parallelised. Crucially, unlike the join, the reduce can *start before the upstream phase has finished* — as soon as two outputs exist, a reduce worker can combine them. That pipelining is what makes MapReduce's reduce tractable at scale and what makes Burns's reduce-pattern more desirable than the join whenever the aggregation can be expressed associatively. Burns works through three reductions in increasing complexity — count, sum, and population-weighted histogram — to make the point that what makes a reducer correct is the algebraic structure of the combine, not the pattern's container shape.

The chapter's unifying observation is the identity between MapReduce and Burns's patterns: map = [[sharder-pattern|sharder]] + [[work-queue-pattern|work queue]]; reduce = reduce-pattern; MapReduce's implicit "wait for every mapper before any reducer starts" barrier = join-pattern. This closes the loop between Burns's container trilogy (Chapters 10–12) and DDIA's batch-processing theory, and lets readers see the same pattern-level choice about "barrier vs pipelined reduce" that [[dataflow-engines|Spark/Flink/Tez]] make at the operator level.

The chapter's chapter-length worked example — an image-tagging pipeline — composes every batch pattern in the book: [[sharder-pattern|sharders]] spreading work, [[multi-worker-pattern|multi-worker]] pods (blur-detector + blurrer; vehicle-detector + color-detector) for component reuse, a [[join-pattern|join]] fencing the destructive deletion of original images after blurring, a [[copier-pattern|copier]] fanning the post-join stream to deletion and detection, another [[sharder-pattern|sharder]] spreading detection work, and finally a [[reduce-pattern|reduce]] aggregating the per-image JSON counts into the final vehicle and color totals.

Pages created from this chapter:

- [[coordinated-batch-pattern]] — the hub page; the two coordination primitives; the three-way comparison table (merger vs join vs reduce); the image-tagging worked example composing every batch pattern; MapReduce identity table; relationship to DDIA batch coverage
- [[join-pattern]] — barrier synchronization; contrast with merger (completeness guarantee); cost (straggler latency); when the guarantee is load-bearing (destructive steps, global aggregates, phase fences); relationship to MapReduce's map-to-reduce barrier and to DDIA's differently-named [[sort-merge-joins]]
- [[reduce-pattern]] — associative pairwise combine; explicit identity with MapReduce's reduce step; Burns's three worked examples (count, sum, weighted histogram); the three defining properties (associative/repeatable, parallel, pipelined with upstream); comparison with join and merger; relationship to [[scatter-gather-pattern]]'s gather step and to dataflow engines' reduce operators

Existing pages augmented: [[mapreduce]] (new container-level perspective section with the four-row identity table: work-queue + sharder = map; join + reduce-pattern = reduce; Chapter 12 added to Sources), [[sort-merge-joins]] (note on the two distinct senses of "join" — DDIA's relational-operator join vs Burns's barrier-synchronization join; Chapter 12 added to Sources), [[merger-pattern]] (Chapter 12's explicit distinction between merger and join; three-way table cross-reference; Chapter 12 added to Sources), [[event-driven-batch-pattern]] (Chapter 12 closes-the-loop section; Chapter 12 added to Sources), [[work-queue-pattern]] (Chapter 12 as the third part of the trilogy; Chapter 12 added to Sources), [[batch-processing]] (Chapter 12 paragraph in the Burns container-level section; Chapter 12 added to Sources), [[dataflow-engines]] (pattern-level echo of the barrier-vs-pipelined-reduce operator-level choice; Chapter 12 added to Sources).

## Related pages

- [[designing-data-intensive-applications]]
- [[monolith-to-microservices]]
- [[sidecar-pattern]]
- [[pod]]
- [[modular-reusable-containers]]
- [[legacy-modernization]]
- [[ambassador-pattern]]
- [[client-side-sharding]]
- [[service-brokering]]
- [[request-splitting]]
- [[adapter-pattern]]
- [[unified-monitoring-interface]]
- [[log-normalization]]
- [[health-check-adapter]]
- [[replicated-load-balanced-service]]
- [[health-probes]]
- [[session-tracked-services]]
- [[caching-layer]]
- [[rate-limiting]]
- [[ssl-termination]]
- [[sharded-service-pattern]]
- [[sharded-cache]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
- [[shard-key-selection]]
- [[scatter-gather-pattern]]
- [[tail-latency-amplification]]
- [[functions-as-a-service]]
- [[serverless-vs-event-driven]]
- [[faas-decorator-pattern]]
- [[event-pipeline-pattern]]
- [[ownership-election-pattern]]
- [[singleton-pattern]]
- [[distributed-locks-on-kv-stores]]
- [[renewable-leases]]
- [[operator-pattern]]
- [[work-queue-pattern]]
- [[source-container-interface]]
- [[worker-container-interface]]
- [[dynamic-worker-scaling]]
- [[multi-worker-pattern]]
- [[event-driven-batch-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[merger-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
