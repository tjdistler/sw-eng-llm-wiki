# Chubby

**Summary**: Google's lock service — a filesystem-like API for maintaining distributed locks across datacenters. Chubby uses the Paxos protocol for asynchronous [[consensus]] and is the canonical place to store data that must be consistent across the cluster, including [[bns|BNS]] name-to-address mappings. The direct ancestor of [[zookeeper|ZooKeeper]].

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What Chubby does

Chubby provides (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- A **filesystem-like API** for maintaining locks.
- **Distributed** locks — handled across datacenter locations.
- [[consensus|Consensus]] via the Paxos protocol (asynchronous).

## Master election

Chubby's defining use case is master election. When a service has five replicas of a job running for reliability but only one replica is allowed to perform actual work, Chubby is used to select which replica may proceed (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). This is the classic [[ownership-election-pattern]] as Burns frames it at the container level.

## Storing consistent data

Beyond lock-holding, Chubby is the general home for "data that must be consistent." The chapter explicitly mentions [[bns|BNS]] storing its mapping between BNS paths and `IP:port` pairs in Chubby (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). This is the structural analogue of using [[zookeeper|ZooKeeper]] or etcd as the authoritative source of partition-to-node mappings in other systems (see [[request-routing]]).

## Relationship to ZooKeeper

[[zookeeper|ZooKeeper]] is modeled directly after Chubby — see the wiki's ZooKeeper page for the direct statement. Chubby uses Paxos; ZooKeeper uses Zab; etcd uses Raft. All three expose similar primitives: linearizable atomic operations, session-based failure detection (via ephemeral nodes), watches, and totally-ordered operations.

## The Global Chubby planned outage

Chapter 4 uses global Chubby as its canonical over-reliance case study (source: chapter-04-service-level-objectives.md). Global Chubby distributes replicas across geographic regions, and true outages are very infrequent. Over time, service owners began to add dependencies **assuming Chubby would never go down**. When the rare outage happened, those dependents couldn't function — the dependency was unreasonable but its unreasonableness had been hidden by Chubby's high actual reliability.

SRE's response was to ensure global Chubby **meets, but does not significantly exceed, its [[service-level-objective|SLO]]**. In any quarter where a true failure hasn't dropped availability below target, a **controlled outage is synthesized by intentionally taking the system down**. This flushes out unreasonable dependencies shortly after they are added and forces dependent-service owners to reckon with the reality of distributed systems.

This is the clearest real-world instance of the principle catalogued on [[slo-expectations]]: don't overachieve your SLO, because users build on what you actually deliver rather than what you say you'll deliver.

## Consensus-as-a-service (SRE Chapter 23)

Laura Nolan's Chapter 23 names Chubby directly as Google's instance of the service-rather-than-library packaging of [[consensus]]: "The Chubby service fills a similar niche at Google. Its authors point out that providing consensus primitives as a service rather than as libraries that engineers build into their applications frees application maintainers of having to deploy their systems in a way compatible with a highly available consensus service" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Structurally Chubby is a [[replicated-state-machine]] on top of Paxos whose API surface is a filesystem-like tree plus locks and watches — exactly the ZooKeeper shape. The "consistency-as-a-service" framing is why Chubby could become the universal home for "data that must be consistent" inside Google; application teams didn't have to understand Paxos, replica placement, or quorum composition to use it.

## Cross-book connections

- [[zookeeper]] — the open-source descendant.
- [[consensus]] — Paxos is the mechanism.
- [[ownership-election-pattern]] (Burns) — the container-level pattern Chubby was built for.
- [[distributed-locks-on-kv-stores]] (Burns) — Burns's derivation of distributed locks from compare-and-swap + TTL is the etcd-era version of what Chubby does natively.
- [[fencing-tokens]] (Kleppmann) — Chubby's sequence numbers play the fencing-token role for lock safety.

## Related pages

- [[zookeeper]]
- [[consensus]]
- [[ownership-election-pattern]]
- [[bns]]
- [[borg]]
- [[slo-expectations]]
- [[service-level-objective]]
- [[site-reliability-engineering]]
- [[managing-critical-state]]
- [[paxos]]
- [[multi-paxos]]
- [[replicated-state-machine]]
