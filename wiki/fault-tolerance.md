# Fault Tolerance

**Summary**: Fault tolerance is the property of a system that allows it to continue operating correctly when one or more of its components fail, by isolating faults before they become failures.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`, `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/site-reliability-engineering/chapter-21-handling-overload.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`, `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`

**Last updated**: 2026-04-19

---

## Fault vs failure

A **fault** is one component deviating from its specification. A **failure** is the system as a whole stopping service to users. The engineering goal is to build systems where faults are inevitable but failures are rare — fault-tolerant systems absorb component-level faults without visible impact to users. (source: chapter-01)

Fault probability cannot be reduced to zero, so the design must assume faults will occur and handle them gracefully rather than relying on prevention alone.

## Hardware redundancy

The traditional approach to hardware faults is redundancy:

- **RAID** for disk arrays
- Dual power supplies and hot-swappable CPUs for servers
- Backup batteries and diesel generators for datacenters

This can keep a single machine running uninterrupted for years. However, as applications run on larger fleets — and especially on cloud platforms like AWS where VM instances can disappear without warning — hardware redundancy alone is insufficient. Software-level fault tolerance is increasingly necessary. (source: chapter-01)

A benefit of software fault tolerance: systems can be patched via **rolling upgrades**, rebooting one node at a time, with no system-wide downtime.

## Chaos engineering and deliberate fault injection

Counterintuitively, increasing fault rates deliberately improves fault tolerance. By randomly killing processes or inducing failures in a controlled way, teams force their fault-tolerance mechanisms to be continually exercised.

**Netflix's Chaos Monkey** is the canonical example: it randomly terminates production processes to ensure the system handles the loss gracefully. Many critical bugs are due to error-handling code that is never executed under normal conditions — deliberate fault injection exposes these latent bugs before they appear under real conditions. (source: chapter-01)

## Fault tolerance vs fault prevention

For most failure modes, tolerating faults is preferable to preventing them. **Security** is the main exception: once an attacker has exfiltrated sensitive data, no fault-tolerance mechanism can undo the breach. Prevention is the only option. (source: chapter-01)

## Systematic software faults

Unlike hardware faults (random and uncorrelated), software faults tend to be **systematic and correlated** — the same bug can affect all instances simultaneously. This makes them harder to tolerate with simple redundancy. They often lie dormant until triggered by an unusual combination of circumstances.

Mitigations: careful reasoning about system assumptions, thorough testing, process isolation, crash-and-restart design, and runtime self-checks (e.g. asserting that messages consumed equals messages produced). (source: chapter-01)

## Building reliable systems from unreliable components

It may seem that a system can only be as reliable as its weakest link, but this is not the case. It is an old idea in computing to construct a more reliable system from a less reliable base (source: designing-data-intensive-applications, chapter 8):

- **Error-correcting codes** allow accurate digital data transmission over channels that occasionally corrupt bits.
- **IP** is unreliable (may drop, delay, duplicate, or reorder packets), but **TCP** provides reliable transport on top of it by retransmitting lost packets, eliminating duplicates, and reassembling order.

There is always a limit to how much more reliable the system can be than its parts. Error-correcting codes fail under overwhelming interference; TCP cannot remove network delays. But the more reliable higher-level system handles tricky low-level faults, making remaining faults easier to reason about. (source: designing-data-intensive-applications, chapter 8)

## Fault tolerance in distributed systems

In distributed systems, [[partial-failures]] are the defining challenge: some parts of the system may be broken while others work fine, and these failures are nondeterministic. The engineering goal is to tolerate these partial failures so the system as a whole continues functioning. (source: designing-data-intensive-applications, chapter 8)

Key fault categories in distributed systems:

- **[[unreliable-networks]]**: packets may be lost, delayed, duplicated, or reordered; responses may never arrive
- **[[unreliable-clocks]]**: clocks drift, jump, and disagree between nodes; relying on synchronized clocks can cause silent data loss
- **[[process-pauses]]**: GC pauses, VM suspension, and OS scheduling can cause a node to be unresponsive for arbitrary periods, during which other nodes may declare it dead

Detecting faults is itself hard: most systems rely on [[timeouts]], which cannot distinguish network failures from node failures, and may falsely declare healthy-but-slow nodes as dead. Once detected, making the system tolerate a fault requires coordination among nodes via [[quorums]] and consensus protocols, since there is no shared memory or global state. (source: designing-data-intensive-applications, chapter 8)

## Consensus as the foundation of fault-tolerant coordination

Chapter 9 identifies [[consensus]] as the key general-purpose abstraction for building fault-tolerant distributed systems. Just as [[transactions]] allow applications to pretend crashes and concurrency don't exist, consensus allows applications to pretend nodes always agree. (source: designing-data-intensive-applications, chapter 9)

Fault-tolerant consensus algorithms (Paxos, Raft, Zab) guarantee safety properties (agreement, integrity, validity) even during total failure, and make progress (termination) as long as a majority of nodes are functioning. They require at least a majority quorum, so a system of 3 nodes tolerates 1 failure, and 5 nodes tolerates 2. (source: designing-data-intensive-applications, chapter 9)

Many critical problems reduce to consensus: [[linearizability|linearizable compare-and-set]], atomic commit, [[total-order-broadcast]], lock acquisition, membership services, and uniqueness constraints. Rather than implementing consensus from scratch (which has a poor success record), applications should use dedicated coordination services like [[zookeeper]] or etcd. (source: designing-data-intensive-applications, chapter 9)

Not every system needs consensus: [[leaderless-replication]] and [[multi-leader-replication]] deliberately forgo global consensus in exchange for better availability and performance, accepting the conflicts that result. (source: designing-data-intensive-applications, chapter 9)

## Fault tolerance in stream processing

[[stream-processing]] introduces distinct fault tolerance challenges compared to both single-node systems and [[batch-processing]]. A stream is infinite, so you cannot restart from the beginning after a crash, and output is produced continuously, so you cannot wait for the task to finish before revealing output (source: chapter-11-stream-processing.md).

Techniques for achieving **exactly-once** (effectively-once) semantics in stream processing include (source: chapter-11-stream-processing.md):

- **Microbatching**: Break the stream into small blocks (~1 second) and treat each as a miniature batch (Spark Streaming)
- **Checkpointing**: Periodically snapshot operator state to durable storage and restart from the last checkpoint on failure (Apache Flink)
- **Atomic commit**: Ensure all outputs and side effects of processing an event happen atomically (Google Cloud Dataflow, VoltDB)
- **Idempotent writes**: Make operations safe to retry by including deduplication metadata (e.g., Kafka message offsets stored alongside database writes)

See [[stream-processing-fault-tolerance]] for full details.

## Trust, but verify: auditing for data integrity

Chapter 12 argues that system models traditionally take a binary approach to faults (some things can happen, others never do), but reality is probabilistic. Data can corrupt on disk even when untouched. Random bit-flips in memory happen at scale. Software bugs corrupt data despite battle-tested databases (MySQL uniqueness constraint failures, PostgreSQL write skew under serializable isolation) (source: chapter-12-the-future-of-data-systems.md).

**Self-auditing systems** should continually check their own integrity rather than relying on blind trust:

- Large storage systems (HDFS, Amazon S3) run background processes that read back files, compare replicas, and move data from suspect disks.
- Backups should be periodically tested by restoring from them.
- [[derived-data|Derived data]] pipelines can be checked end-to-end by rerunning the derivation and comparing results.
- Event-based systems ([[event-sourcing]]) provide better auditability: deterministic derivation from an immutable event log means the provenance of every piece of data is explicit and reproducible.

Cryptographic tools (Merkle trees, as used in certificate transparency and distributed ledgers) offer promise for efficient end-to-end integrity checking, though making them scale without performance penalties remains an open problem (source: chapter-12-the-future-of-data-systems.md).

See [[end-to-end-argument]] for the broader principle that integrity checks must be end-to-end to catch all sources of corruption.

## Data integrity as a defence-in-depth discipline (Chapter 26)

SRE Chapter 26 specialises the fault-tolerance framing to **data integrity at scale** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). The key move: treat user-visible data loss as a fault class that needs its own cooperating stack of tolerance mechanisms, not a single mechanism. Chapter 26 catalogues 24 distinct failure modes (6 root causes × 2 scopes × 2 rates — see [[data-integrity-failure-modes]]) and argues that no single defence covers all 24; the response is a three-layer [[defense-in-depth-data|defence in depth]]:

- **Layer 1: [[soft-deletion]]** — primary defence against accidental user/developer/hijacker deletion; data is marked deleted but recoverable by admin paths within a grace window.
- **Layer 2: [[tiered-backup-strategy|backups]]** — multi-tier copies at progressively diverse storage technologies (local snapshots → distributed filesystem → offsite tape), each protecting against failure modes the previous tier shares with live data.
- **Layer 3: [[data-validation-pipelines|out-of-band validators]]** — MapReduce/Hadoop pipelines that continuously check cross-datastore invariants and catch low-grade corruption before it propagates beyond recovery.

Chapter 26 also explicitly strengthens Kleppmann's "trust but verify" framing with an operational rule: [[recovery-testing|continuously test the recovery process]] in normal operations and alert on missing success heartbeats. The only way to know backups are backups (not archives) is to actually restore from them, repeatedly. See [[data-integrity-sre]] for the hub and [[data-integrity-principles]] for the five principles Ch 26 closes with.

The 2011 [[gmail-gtape-restore|Gmail GTape restore]] and 2012 [[google-music-runaway-deletion|Google Music runaway-deletion]] case studies in Chapter 26 are the worked examples of the three-layer discipline paying off at Google scale.

## Overload as a fault class

SRE Chapter 21 treats **overload** as a fault class that deserves its own tolerance machinery (source: chapter-21-handling-overload.md). The failure mode: the serving system receives more requests than it can process, queues pile up, memory fills, latency spikes, and eventually the task crashes — taking all in-flight work with it. The engineering goal is the same as for any other fault: the system as a whole remains useful even when the "we're not provisioned for this much load" fault occurs.

Chapter 21's cooperating mechanisms together form a textbook fault-tolerance pattern for serving systems:

- [[per-customer-quotas]] — contain the blast radius of a misbehaving customer to their own budget.
- [[adaptive-throttling]] — client-side self-regulation so rejections don't become the load.
- [[utilization-signals]] + [[load-shedding]] — per-task self-defence: reject what cannot be served so the rest can be.
- [[request-criticality]] — preferentially shed low-priority traffic under pressure.
- [[graceful-degradation]] — serve a cheaper response when the full response would fail.
- [[retry-budget]] — cap retry amplification so a small overload doesn't cascade into a large one.

The operating principle — **partial degradation beats total failure** — is the same principle that motivates [[replicated-load-balanced-service|replication]], [[health-probes|health-probe-based deregistration]], and [[stream-processing-fault-tolerance|effectively-once semantics]]. Overload is the load-shaped fault; the Chapter 21 stack is how serving systems tolerate it.

See [[handling-overload]] for the hub page covering all eight mechanisms and how they compose.

## Cascading failure: when fault tolerance produces positive feedback

SRE Chapter 22 identifies a specific hazard in fault-tolerant systems: the very mechanisms that absorb faults in the steady state can *amplify* faults under overload, producing positive feedback (source: chapter-22-addressing-cascading-failures.md). A fault-tolerant system has load balancing to shift traffic off failing tasks; but shifted traffic arrives at peers that may also be near capacity, overloads them, and the failure spreads. Retries improve success rates when one task is briefly slow; but retries amplify load when the whole fleet is overloaded. Automatic failover reduces MTTR; but failover health-checks can death-loop a recovering fleet.

Chapter 22's closing argument (source: chapter-22-addressing-cascading-failures.md):

> Retrying on failures, shifting load around from unhealthy servers, killing unhealthy servers, adding caches to improve performance or reduce latency: all of these might be implemented to improve the normal case, but can improve the chance of causing a large-scale failure. Be careful when evaluating changes to ensure that one outage is not being traded for another.

The fault-tolerance pattern applies with a warning: evaluate each mechanism not just for its steady-state benefit but for its behaviour under overload. See [[cascading-failure]] for the full treatment, including the specific failure modes ([[gc-death-spiral]], [[retry-amplification]], [[bimodal-latency]], [[slow-startup-and-cold-caching]]) and the mitigations ([[queue-management]], [[deadline-propagation]], [[intra-layer-communication]] discipline, and [[testing-for-cascading-failures]]).

## Fault tolerance via architectural modularity (Hard Parts Ch 3)

Chapter 3 of *Software Architecture: The Hard Parts* gives fault tolerance a narrower, architecture-decomposition-focused definition (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> the ability for some parts of the system to remain responsive and available as other parts of the system fail.

The canonical illustration: a fatal out-of-memory error in the payment-processing portion of a retail application should not prevent users from searching or placing orders. Ford and Richards argue that monolithic systems fundamentally cannot deliver this — even with multiple load-balanced instances, a programming bug that triggers the fault will exist in every instance. Redundancy without isolation is theatre.

Architectural modularity is the structural answer: breaking the system into independently-deployed units means catastrophic failure is contained within the unit that fails. This is the [[bulkhead]] pattern applied at deployment-unit granularity — the failure of one bulkhead does not flood the others. See [[architectural-modularity]] for the five-driver rubric this fault-tolerance argument is part of.

The chapter's critical caveat: **synchronous coupling defeats this**. If Service A synchronously depends on Service B, and B fails, A fails too. The chapter's prescription — asynchronous communication between services — is the same conclusion Newman's [[robustness-and-resiliency-at-scale]] reaches, and the same conclusion the [[architectural-quantum]] framing produces when applied to services with different availability targets.

The granularity trade-off also applies: domain-level fault tolerance (service-based architecture) isolates failures to one domain service; function-level fault tolerance (microservices) isolates failures to one small service. Finer grain gives finer-grained fault isolation — but only if the communication between services is decoupled enough that failures don't propagate.

## Related pages

- [[reliability]]
- [[maintainability]]
- [[scaling-approaches]]
- [[partial-failures]]
- [[unreliable-networks]]
- [[unreliable-clocks]]
- [[process-pauses]]
- [[timeouts]]
- [[system-models]]
- [[consensus]]
- [[zookeeper]]
- [[two-phase-commit]]
- [[linearizability]]
- [[stream-processing]]
- [[stream-processing-fault-tolerance]]
- [[batch-processing]]
- [[end-to-end-argument]]
- [[derived-data]]
- [[event-sourcing]]
- [[timeliness-and-integrity]]
- [[replicated-load-balanced-service]]
- [[health-probes]]
- [[mttr-and-mttf]]
- [[emergency-response]]
- [[site-reliability-engineering]]
- [[handling-overload]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[adaptive-throttling]]
- [[retry-budget]]
- [[cascading-failure]]
- [[server-overload]]
- [[resource-exhaustion]]
- [[gc-death-spiral]]
- [[retry-amplification]]
- [[queue-management]]
- [[latency-and-deadlines]]
- [[deadline-propagation]]
- [[bimodal-latency]]
- [[slow-startup-and-cold-caching]]
- [[intra-layer-communication]]
- [[testing-for-cascading-failures]]
- [[addressing-ongoing-cascading-failure]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[data-integrity-failure-modes]]
- [[soft-deletion]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[data-integrity-principles]]
- [[architectural-modularity]]
- [[bulkhead]]
