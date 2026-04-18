# CAP Theorem

**Summary**: A theorem (proposed by Eric Brewer in 2000) stating that when a network partition occurs, a distributed system must choose between [[linearizability]] (consistency) and availability -- historically influential but frequently misunderstood and of limited practical value for system design.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The actual trade-off

When the network is working correctly, a system can provide both consistency ([[linearizability]]) and total availability. The choice arises only during a network partition (source: designing-data-intensive-applications, chapter 9):

- **If the application requires linearizability**: replicas that cannot communicate with each other must refuse requests (becoming unavailable) rather than serve potentially stale data.
- **If the application does not require linearizability**: each replica can process requests independently, remaining available but potentially returning inconsistent results.

A better phrasing: "either Consistent or Available when Partitioned." (source: designing-data-intensive-applications, chapter 9)

## Why CAP is unhelpful

CAP is often presented as "pick 2 of 3: Consistency, Availability, Partition tolerance." This framing is misleading because network partitions are faults, not a choice -- they will happen. You are really choosing between C and A during partitions. (source: designing-data-intensive-applications, chapter 9)

Further problems with CAP as a design tool (source: designing-data-intensive-applications, chapter 9):

- The formal definition of "availability" in CAP does not match common usage. Many highly available (fault-tolerant) systems do not meet CAP's definition.
- CAP only considers one consistency model ([[linearizability]]) and one kind of fault (network partitions). It says nothing about network delays, dead nodes, or other trade-offs.
- CAP has been superseded by more precise impossibility results in distributed systems research.
- The CP/AP classification of databases is an oversimplification with many flaws.

## Historical value

Despite its limitations as a formal result, CAP was historically important for shifting database engineering culture. Before CAP, many distributed databases focused on providing linearizable semantics on shared-storage clusters. CAP encouraged exploring shared-nothing distributed designs more suitable for large-scale web services, contributing to the explosion of NoSQL technologies in the mid-2000s. (source: designing-data-intensive-applications, chapter 9)

## The real reason: performance, not fault tolerance

Most systems that forgo [[linearizability]] do so for **performance**, not because of CAP. Even multi-core CPUs drop linearizability (each core has its own cache) purely for speed. Attiya and Welch proved that linearizable operations must have response times proportional to network delay uncertainty. Weaker models like [[causal-consistency]] can be much faster and remain available during network faults. (source: designing-data-intensive-applications, chapter 9)

## Chapter 23 operational reframing (SRE book)

Laura Nolan's framing in *Site Reliability Engineering* Chapter 23 connects CAP to its practical consequence: **you cannot sacrifice correctness on critical state to achieve reliability or performance** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). A financial-transaction system is her canonical example — reliability or performance are not very valuable if the financial data is incorrect.

Her treatment is pointed about the **BASE vs ACID** dichotomy that grew out of CAP-era systems. Datastores supporting *Basically Available, Soft state, Eventual consistency* (BASE) are useful for some workloads that would be infeasible with ACID, but they impose a heavy cost on application developers. Nolan quotes Jeff Shute (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

> We find developers spend a significant fraction of their time building extremely complex and error-prone mechanisms to cope with eventual consistency and handle data that may be out of date. We think this is an unacceptable burden to place on developers and that consistency problems should be solved at the database level.

The chapter's specific warnings about BASE / [[eventual-consistency]]:

- **Multimaster replication with timestamp conflict resolution** is fragile because of clock drift — inevitable in distributed systems — and [[unreliable-networks|network partitioning]].
- **Kyle Kingsbury's Jepsen series** has produced many real-world examples of unexpected and incorrect behaviour in BASE datastores.

The punchline: systems with critical state must be able to reliably synchronise that state across processes, and [[consensus|distributed consensus]] algorithms are the mechanism. CAP is the framing; consensus is the answer.

## Related pages

- [[linearizability]]
- [[causal-consistency]]
- [[eventual-consistency]]
- [[consensus]]
- [[replication]]
- [[fault-tolerance]]
- [[managing-critical-state]]
- [[spanner]]
