# MOC: Distributed Systems

**Summary**: Entry point for questions about the *fundamental problems of running computation across multiple machines* — partial failures, unreliable networks, unreliable clocks, process pauses, truth and leadership, replication, partitioning, consensus, and the coordination primitives that make the whole mess tractable. Start here when the question is "how does this actually work when machines fail, networks drop, and nodes disagree?" rather than "what does correctness look like across stores?" or "how do services talk via events?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have work spread across machines and something about it is hard. Maybe replicas disagree. Maybe a leader failed over and you're not sure what was lost. Maybe a node came back after a 90-second GC pause and proceeded to act as if nothing had changed. Maybe you're reaching for ZooKeeper or etcd and want to understand what it actually gives you. This MOC is the vocabulary for every problem that *only exists because multiple machines are involved*.

The canonical shape of a question that lands here: *"Why did our leader election go wrong?"*, *"Should we use quorum reads or a leader read?"*, *"Is our system CP or AP and does that even mean anything useful?"*, *"How many replicas do we actually need?"*, *"Why did the new leader accept a write the old leader had already committed?"*, *"What does 'exactly once' mean on an unreliable network?"*

Jurisdictional rule for this MOC:

- **This MOC** owns the *systems* layer — the machinery that lets nodes survive, agree, replicate, partition, and coordinate. Failure modes, replication strategies, partitioning strategies, consensus protocols, coordination services.
- [[moc-consistency-and-transactions]] owns the *correctness* layer built *on top* — linearizability vs causal consistency, isolation levels, ACID, two-phase commit, sagas, serializability. Those abstractions are the guarantees an application sees; this MOC is the machinery that produces the guarantees.
- [[moc-events-and-streaming]] owns the *integration* layer that sits adjacent — brokers as a distributed-systems substrate used as the communication backbone between services, choreography vs orchestration, event design.
- [[moc-data-models-and-storage]] owns the *storage-engine* side — how LSM trees and B-trees work, replication as a store property, partitioning of secondary indexes. This MOC cites replication and partitioning as distributed-systems primitives; the storage MOC owns the store-shape consequences.
- *moc-reliability-and-operations* (forthcoming) owns the operational playbook — SLOs, observability, on-call. This MOC is about what you need to reason about to write a correct distributed algorithm; the reliability MOC is about how you run the result in production.

Shared pages (replication, partitioning, quorums, consensus, ZooKeeper) are linked here under their *mechanism* lens — what they do, when they fail, what their assumptions are. Other MOCs link the same pages under a *guarantee* or *integration* lens.

## The defining problems

Before any of the mechanisms, internalise *why* distributed systems are hard. Every pattern below is a response to one of these three realities.

- [[partial-failures]] — the defining characteristic: nondeterministic, asymmetric, partial breakdowns where part of the system works and part doesn't, and often no-one has the full picture. The reason you cannot just "program as if it's one big computer."
- [[monolithic-vs-distributed]] — the first-fallacy reminder. Every call that used to be an in-memory function is now an attempt. Every microservice migration signs up for the problems catalogued below, indefinitely.
- [[fallacies-of-distributed-computing]] — the eight fallacies every distributed system pays continuously: reliable network, zero latency, infinite bandwidth, secure network, static topology, one administrator, zero transport cost, homogeneous network. Read once, remember forever.

Deeper reading: [[designing-data-intensive-applications#chapter-8-the-trouble-with-distributed-systems]] is the book-length treatment of this section. If you internalise Chapter 8, most of the rest of this MOC becomes obvious.

## Unreliable networks

Networks drop packets, reorder them, delay them arbitrarily, and partition. The only thing a sender can observe is "no response yet" — which is indistinguishable from "the recipient crashed," "the request was dropped," "the response was dropped," or "everything's fine, just slow."

- [[unreliable-networks]] — shared-nothing asynchronous networks. No delivery guarantees; queueing and congestion mean latency is a distribution, not a number. The substrate assumption under every pattern below.
- [[network-faults]] — how prevalent network problems actually are in production (more than you'd guess); partitions; how services actually detect faults; the correlation with cascading failures.
- [[timeouts]] — the only fault-detection mechanism you really have. The long-vs-short dilemma: short timeouts cause false positives and retries, long timeouts cause slow failover. Adaptive timeouts as the practical answer.
- [[retry-amplification]] — retries turn a spike into a stampede. The failure mode that converts a brief blip into an extended outage; the counterargument to "just retry."
- [[retry-budget]] — cap retries at the callsite so the retry rate stays bounded even under failure; the practical fix.
- [[circuit-breaker]] — stop calling a downstream that's failing; the per-caller back-pressure discipline that keeps retries from piling on.
- [[bulkhead]] — isolate thread pools / connection pools per dependency so one slow downstream doesn't exhaust the shared pool and bring down everything.
- [[load-shedding]] — refuse requests at the edge when the system is over capacity; the structural alternative to queueing until everything times out.

Deeper reading: [[designing-data-intensive-applications#chapter-8-the-trouble-with-distributed-systems]] for the foundational framing; [[site-reliability-engineering#chapter-22-addressing-cascading-failures]] for the production-scale failure patterns; [[site-reliability-engineering#chapter-21-handling-overload]] for the load-shedding and adaptive-throttling mechanics.

## Unreliable clocks and process pauses

Time is the other thing you can't trust. Clocks drift, get corrected, disagree between machines. Processes pause for garbage collection, VM migration, or kernel scheduling delays long enough to violate any "the leader must renew its lease every 30 seconds" assumption you thought you had.

- [[unreliable-clocks]] — time-of-day clocks (wall-clock, can jump) vs monotonic clocks (only go forward, can't compare across machines). Why using a timestamp to order events across nodes is one of the oldest and worst traps in distributed systems.
- [[clock-synchronization]] — NTP limitations (tens of milliseconds at best, sometimes much worse); GPS/PTP/atomic clocks; Google's TrueTime as the exotic answer that Spanner leans on. Why the answer is usually "don't depend on tight synchronisation."
- [[process-pauses]] — GC, VM suspension, disk I/O, kernel preemption. Unpredictable delays that can last longer than any lease or heartbeat timeout you'll reasonably set. The reason "we'll just renew the lock every 10 seconds" doesn't give you what you think it does.

The pattern that rescues you when a paused node wakes up and tries to act on stale authority:

- [[fencing-tokens]] — monotonically increasing tokens attached to every privileged operation; downstream services reject operations with a token older than the highest they've seen. The mechanism that prevents a zombie leader from corrupting state. Burns's container-level construction of the same idea appears as resource-version-per-request in [[distributed-locks-on-kv-stores]].
- [[truth-and-leadership-in-distributed-systems]] — the node cannot trust its own judgment; quorum-based truth is the only reliable answer. The conceptual prerequisite for understanding why consensus protocols are the shape they are.

Deeper reading: [[designing-data-intensive-applications#chapter-8-the-trouble-with-distributed-systems]].

## System models — what assumptions your algorithm holds under

Before you write a distributed algorithm, know which model you're targeting. Get this wrong and your proof is vacuous.

- [[system-models]] — timing models (synchronous, partially synchronous, asynchronous) and failure models (crash-stop, crash-recovery, Byzantine). The axis on which every algorithm below assumes *something*.
- [[safety-and-liveness]] — two property classes. Safety: nothing bad ever happens (no two nodes ever disagree on the commit). Liveness: something good eventually happens (the commit eventually completes). Most proof arguments separate them; most production outages are liveness failures masquerading as safety ones.
- [[flp-impossibility]] — Fischer-Lynch-Paterson, 1985. Bounded-time consensus is impossible in a fully asynchronous system with even one crash-stop failure. How production systems sidestep it (partial synchrony, randomness, failure detectors).
- [[byzantine-faults]] — nodes that actively lie. The Byzantine Generals Problem; why BFT matters in cryptocurrency, aerospace, and adversarial multi-party systems, and why most production systems assume non-Byzantine and save the 3x-replication cost.

## Replication

Once you have more than one copy of data, you have to decide who can write, how writes propagate, and what a reader sees when replication is mid-flight.

The hub:

- [[replication]] — the three architectures (single-leader, multi-leader, leaderless); synchronous vs asynchronous propagation; the fundamental tension between consistency, availability, and latency. Start here.

### Single-leader replication

- [[leader-based-replication]] — one replica accepts writes; the others apply the leader's log. WAL-based, statement-based, row-based, and trigger-based replication; each has different evolution, compatibility, and correctness trade-offs.
- [[failover]] — promoting a follower when the leader dies. Split brain, lost writes, fencing (the [[fencing-tokens]] lens from above applied at the replica level), the many ways automatic failover is harder than it looks.
- [[replication-lag]] — async replication always lags. The three user-visible anomalies (read-after-write staleness, non-monotonic reads, causality inversion) and why they matter at scale.

Anomalies the application or the client library has to paper over:

- [[read-after-write-consistency]] — users always see their own writes. Sticky-leader reads, track-client-latest-timestamp, and per-user monotonic cursors.
- [[monotonic-reads]] — reads never go backwards in time for a given user. Sticky-replica routing as the usual implementation.
- [[consistent-prefix-reads]] — causally related writes appear in order; the causality anomaly where a reply appears before the question.

### Multi-leader and leaderless

- [[multi-leader-replication]] — multiple leaders accept writes; multi-datacenter, offline-first, and collaborative editing as the three use cases. Buys availability at the cost of conflict handling.
- [[write-conflicts]] — detection and resolution: last-writer-wins (lossy), application-level merge, CRDTs, custom logic, tombstones. The central complexity of multi-leader.
- [[leaderless-replication]] — Dynamo-style; any replica accepts writes; read repair and anti-entropy as the reconciliation mechanisms; sloppy quorums when the "preferred" nodes are unreachable.
- [[quorums]] — the `w + r > n` overlap guarantee; why this gives you recency *per key* without consensus; the many edge cases (concurrent writes, sloppy quorums, node failure during the write) that break the naive promise.
- [[version-vectors]] — per-replica version numbers that distinguish happens-before from concurrent; the basis for sibling detection and merge in leaderless systems.

Deeper reading: [[designing-data-intensive-applications#chapter-5-replication]] for the foundational single/multi/leaderless treatment; [[designing-data-intensive-applications#chapter-9-consistency-and-consensus]] for linearisability's interaction with replication (the next MOC owns the guarantees, this one owns the mechanism).

## Partitioning

Replication gives you durability and availability; partitioning gives you scale. The two compose: a partition gets replicated, and the partitioning scheme has to survive the replication scheme.

- [[partitioning]] — splitting datasets across nodes for scalability; terminology (shard, partition, region, vnode) and how it varies across systems. Start here.
- [[partitioning-strategies]] — key-range vs hash. Range supports range queries and suffers hot spots on sequential keys; hash kills range queries and spreads load evenly. Most real systems hash with a prefix that preserves some locality.
- [[hot-spots]] — disproportionate load on a single partition. Celebrity writes, temporal skew, hash-key salting, sampling-and-split as mitigations.
- [[consistent-hashing]] — the CDN-origin term; why it's a misnomer when applied to databases. Virtual nodes as the generalisation most systems actually use.
- [[partitioning-secondary-indexes]] — document-partitioned (local) indexes vs term-partitioned (global) indexes. Local is cheap to write, expensive to query; global inverts the trade. The decision shapes every secondary-index read pattern.
- [[rebalancing-partitions]] — redistributing partitions when nodes are added or removed. Fixed count (Couchbase), dynamic splitting (HBase, MongoDB), proportional-to-nodes (Cassandra). Why "just rehash" is the wrong answer.
- [[request-routing]] — service discovery for partitioned databases: routing tiers, client-side awareness, ZooKeeper-coordinated metadata. The infrastructure that turns a partitioned store into a single logical service.

Container-level and service-level echoes of the same concepts:

- [[sharded-service-pattern]] — Burns's service-level pattern for partitioning state across instances; connects to the [[replicated-load-balanced-service]] pattern at the serving layer.
- [[replicated-sharded-service]] — replication plus sharding at container granularity; the composition pattern for stateful containerised services.
- [[sharded-cache]] — partition-by-key caching; hot-key and rebalance concerns that mirror the database version.

Deeper reading: [[designing-data-intensive-applications#chapter-6-partitioning]] for the theory; [[designing-distributed-systems#chapter-6-sharded-services]] for the container-level view.

## Consistency, consensus, and coordination

The agreement problems that underpin every "strong" guarantee you give your users. The algorithms are famous; the production systems that implement them are a small menu.

Start with the guarantees:

- [[linearizability]] — the strongest single-object consistency guarantee: atomic recency, no stale reads, a single-copy illusion. The most expensive guarantee you can ask for; the one you usually cannot afford at scale. [[moc-consistency-and-transactions]] owns its interaction with ACID; this MOC owns the mechanism cost.
- [[causal-consistency]] — happens-before preserved without requiring total order. The strongest guarantee achievable without global coordination; the sweet spot for systems that need more than eventual but cannot pay for linearisability.
- [[lamport-timestamps]] — sequence numbers consistent with causality; the piggyback-maximum mechanism; why they cannot detect concurrency, only order events that have one.
- [[total-order-broadcast]] — reliable, totally-ordered delivery of a single message sequence to every node. Chandra-Toueg showed it's equivalent to consensus. The abstraction every replicated state machine sits on.
- [[atomic-broadcast]] — the same idea with the "reliable + totally-ordered" guarantee named. The building block under ZooKeeper's ZAB, etcd's Raft log, and Kafka's controller protocol.
- [[cap-theorem]] — Brewer's result: during a network partition you must choose between linearizability and availability. Historically important, practically limited — most systems are not actually partitioned most of the time, and the "AP vs CP" sticker hides more than it reveals. Read the page for the nuance.
- [[coordination-avoidance]] — the design principle behind the last two decades of scalable systems: don't coordinate unless you must. Pick the weakest guarantee the application can tolerate and design for it explicitly.

The core agreement problem:

- [[consensus]] — nodes agreeing on a single value in the presence of failure. The problem FLP says is impossible in pure async; the problem Paxos, Raft, and Zab solve under partial synchrony. The foundation of every strong guarantee and every reliably replicated datastore.

Consensus algorithms and shapes:

- [[paxos]] — Lamport's 1998 protocol. Sequence numbers + majority quorums; safe but agrees on one value at a time. Notoriously difficult to implement correctly; notoriously hard to understand as written.
- [[multi-paxos]] — stable-leader Paxos: one proposer at a time, one RTT in steady state. The design most "Paxos-based" production systems actually use. Dueling-proposer livelock on re-election is the standing failure mode.
- [[fast-paxos]] — client-to-acceptor direct sends that save one RTT in the happy case and sometimes make latency worse because of tail effects. Hard to batch; used less than its designers hoped.
- [[stable-leader]] — the Multi-Paxos / Raft / Zab shared pattern: elect a leader, funnel writes through it, re-elect on failure. Three liabilities — non-local latency, leader bandwidth, leader machine capacity — that shape the operational story.
- [[mencius-epaxos]] — rotating-leader and leaderless alternatives optimised for wide-area consensus. The response to stable-leader's leader-hotspot and cross-region-RTT weaknesses.

Reducing algorithms to production systems:

- [[replicated-state-machine]] — the deliberate architectural layer above consensus. Any deterministic program applied to a totally-ordered command log stays consistent across replicas. The abstraction that turns consensus into "replicate whatever you want."
- [[state-machine-replication]] — the DDIA framing of the same idea. The conceptual bridge between consensus and every consensus-backed datastore.
- [[reliable-replicated-datastore]] — consensus in the critical path of every write. The ZooKeeper / etcd / Chubby packaging.
- [[reliable-distributed-queue]] — queue-as-RSM; lease-based task claiming; work-distribution vs publish-subscribe shapes. What ZooKeeper/etcd-backed work queues actually do under the hood.
- [[distributed-barrier]] — RSM-backed primitive that blocks a group until a condition is met. MapReduce phase boundaries as the canonical case.

Production consensus services:

- [[zookeeper]] — the Yahoo-origin coordination service. Consensus-based primitives (membership, locks, config distribution); failure detection; leader election. Burns's container-level construction uses etcd for the same role.
- [[chubby]] — Google's Paxos-backed lock service. ZooKeeper's conceptual ancestor and the service behind most Google cluster-scoped coordination.
- [[managing-critical-state]] — SRE Ch 23 hub: consensus as the answer to leader election, critical shared state, distributed locking, group membership, reliable queuing. The integration-level framing.
- [[consensus-coordination-failures]] — SRE Ch 23's opening case studies: STONITH-via-heartbeats split-brain, human-escalated failover that doesn't scale, gossip-based membership under partition. The shape of the failures that consensus exists to rule out.

Performance and operations of consensus:

- [[consensus-performance]] — workload and deployment axes; the standard optimisation menu (leaders, leases, batching, disk-log combining).
- [[consensus-disk-access]] — the durable-log bottleneck; batching to amortise disk cost; combining RSM and consensus logs.
- [[consensus-read-optimisations]] — the four ways to get a strongly-consistent read: consensus read, leader read, quorum lease, stale-replica-with-explicit-bound. Each a different latency/consistency/safety trade.
- [[quorum-leases]] — read-lease optimisation for geographically concentrated read-heavy workloads; the pattern that makes etcd/ZooKeeper affordable in read-dominated systems.
- [[consensus-replica-count]] — the `2f+1` rule: `f=1` needs 3 replicas, `f=2` needs 5. Why 3 is the floor and 5 is the practical default; why losing quorum is (in theory) unrecoverable.
- [[consensus-replica-placement]] — failure domains vs latency; the rule of thumb that your consensus group shouldn't be more geographically robust than the clients it serves.
- [[quorum-composition]] — linchpin placements across continents; the drastic latency jump on linchpin loss.
- [[hierarchical-quorums]] — majority-of-groups plus majority-of-members; the mitigation for flat-quorum linchpin weakness.
- [[consensus-monitoring]] — member health, lagging replicas, leader existence, leader-change rate, transaction number, proposals. The operational dashboard for a consensus service.

Deeper reading: [[designing-data-intensive-applications#chapter-9-consistency-and-consensus]] for the theory; [[site-reliability-engineering#chapter-23-managing-critical-state-distributed-consensus-for-reliability]] for the production-integration story.

## Ownership election and container-level coordination

Burns's book treats the same problems at the container and Kubernetes-operator level. The vocabulary converges with DDIA's; the construction is hands-on.

- [[ownership-election-pattern]] — the Chapter 9 pattern: scale *assignment* rather than requests or state. Elect a master among replicated instances; handle handoff; defend against the briefly-both-master window. The container-level equivalent of [[failover]].
- [[singleton-pattern]] — the cheaper alternative Burns opens with. A single replica under Kubernetes is 3-to-4 nines out of the box. Read before reaching for master election; often the right answer.
- [[distributed-locks-on-kv-stores]] — constructing a lock on etcd/ZooKeeper/Consul from CAS + TTL + resource versions. Walks through the subtle bugs in a naive implementation and arrives at the same [[fencing-tokens]] mechanism DDIA derives from theory.
- [[renewable-leases]] — long-running ownership via short TTLs refreshed every `ttl/2` from a background thread; terminate-and-let-orchestrator-restart as the lost-lock response.
- [[operator-pattern]] — application-specific controller running inside Kubernetes; packaged operational expertise; the CoreOS etcd-operator-via-Helm worked example.

Deeper reading: [[designing-distributed-systems#chapter-9-ownership-election]].

## Distributed scheduling

Cron, but for a datacenter. A narrow specialisation of consensus (the scheduler's state is the thing being replicated) with enough special-case engineering to warrant its own section.

- [[distributed-cron]] — SRE Ch 24 hub. Google's datacenter-wide cron service: Paxos-replicated state, Fast-Paxos leader as service leader, Borg as the backing scheduler, per-datacenter scope sharing fate with Borg.
- [[cron-reliability-challenges]] — what changes when cron goes distributed: multiple failure domains, container isolation, partial-launch failures, diverse replica placement, per-datacenter-not-global scope.
- [[cron-idempotency-and-skip-vs-double-launch]] — cron jobs span the `idempotent × skippable` matrix; the fail-closed default is skip-rather-than-double-launch, because a skipped launch is usually recoverable while a double launch often isn't.
- [[cron-leader-follower]] — Paxos leader holds mutual exclusion to the datacenter scheduler; launches bracketed by synchronous about-to-launch and launch-completed records; on lost leadership the leader must immediately stop talking to the scheduler.
- [[cron-partial-failure-resolution]] — precomputed datacenter-scheduler job names, scheduled-launch-time embedded in the name; state lookup on the downstream scheduler as the resolution mechanism. The idempotence-or-lookup rule.
- [[cron-state-storage]] — Paxos logs on local disk only (three copies); snapshots on local disk *and* distributed filesystem. The asymmetric backup strategy follows from "losing logs is bounded-time loss; losing snapshots is unrecoverable."
- [[cron-thundering-herd]] — the `?` crontab extension: "any value is acceptable," chosen by hashing the job configuration. Distributes launches stably across a window instead of synchronising everyone on midnight.

Deeper reading: [[site-reliability-engineering#chapter-24-distributed-periodic-scheduling-with-cron]]. [[moc-data-processing]] owns the pipeline-execution half of the periodic-vs-continuous argument; this MOC owns the scheduler half.

## Google production infrastructure as the concrete case

The DDIA and SRE abstractions don't live in a vacuum — they shipped inside a single, tightly-integrated production stack. Reading the actual Google components makes the rest of this MOC concrete.

- [[google-datacenter-topology]] — machine / rack / row / cluster / building / campus. The failure-domain hierarchy every other component is aware of.
- [[borg]] — the cluster OS under Google. Failure-domain-aware binpacking, priority-based preemption, quota, machine-service abstraction. Kubernetes's direct ancestor.
- [[spanner]] — globally consistent SQL-like database on top of Paxos groups per shard, backed by [[clock-synchronization|TrueTime]] to close the commit-timestamp uncertainty window. The canonical example of "what if we actually synchronise clocks well enough?"
- [[bigtable]] — sparse multidimensional sorted-map NoSQL on Colossus; eventual consistency; the "big table, small guarantee" side of the Google storage portfolio.
- [[colossus]] — cluster-wide filesystem over per-machine D fileservers; the successor to GFS. The substrate every large-scale Google computation runs on.
- [[gslb]] — Global Software Load Balancer; three-level DNS/service/RPC hierarchy over BNS addresses.
- [[chubby]] — (re-cited; listed under consensus). The lock service everything else in the stack authenticates to.
- [[life-of-a-request]] — the end-to-end Shakespeare trace: DNS → GSLB → GFE → frontend → backend → Bigtable. The single most concrete thing in the SRE book.

Deeper reading: [[site-reliability-engineering#chapter-2-the-production-environment-at-google-from-the-viewpoint-of-an-sre]].

## Sibling MOCs

- [[moc-consistency-and-transactions]] — owns the guarantees built on top of the mechanisms in this MOC. Linearizability, causal consistency, and CAP appear in both MOCs under different lenses: this MOC owns the *cost and mechanism*; the consistency MOC owns the *guarantee the application gets*.
- *moc-events-and-streaming* (companion) — owns the architectural use of events as the communication layer between services. This MOC's replication, partitioning, and consensus primitives are the substrate that log-based brokers ([[log-based-message-brokers]], [[event-broker]]) are built on; the events MOC owns the integration pattern.
- [[moc-data-models-and-storage]] — owns replication and partitioning as properties of a *store*. This MOC owns them as distributed-systems *primitives*; the storage MOC owns their consequences for schema shape, encoding, and per-service data ownership.
- [[moc-data-processing]] — owns the pipeline-execution and scheduler side of SRE Ch 25. This MOC owns the cron-at-scale side of Ch 24. Both cite [[site-reliability-engineering]] Ch 24–25; split responsibilities on the *scheduler-for-a-program* vs *program-being-scheduled* axis.
- [[moc-microservices]] — owns the organisational/architectural view of services that live in the distributed fabric this MOC describes. Sidecars, service mesh, and the platform tax are the mitigations a microservices fleet applies to the problems catalogued here.
- [[moc-decomposition]] — owns the extraction playbook. This MOC owns the failure modes the extracted service inherits the moment it becomes a network hop.
- *moc-reliability-and-operations* (forthcoming) — owns the operational playbook (SLO/SLI, observability, on-call, incident response). This MOC says "fencing tokens prevent zombie-leader corruption"; the reliability MOC says "and here's how you know in production that one is happening."

## Related pages

- [[index]]
- [[designing-data-intensive-applications]]
- [[site-reliability-engineering]]
- [[designing-distributed-systems]]
- [[partial-failures]]
- [[unreliable-networks]]
- [[unreliable-clocks]]
- [[process-pauses]]
- [[fencing-tokens]]
- [[truth-and-leadership-in-distributed-systems]]
- [[replication]]
- [[leader-based-replication]]
- [[failover]]
- [[multi-leader-replication]]
- [[leaderless-replication]]
- [[quorums]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[linearizability]]
- [[causal-consistency]]
- [[consensus]]
- [[paxos]]
- [[multi-paxos]]
- [[stable-leader]]
- [[replicated-state-machine]]
- [[zookeeper]]
- [[chubby]]
- [[managing-critical-state]]
- [[cap-theorem]]
- [[coordination-avoidance]]
- [[distributed-cron]]
- [[ownership-election-pattern]]
- [[distributed-locks-on-kv-stores]]
