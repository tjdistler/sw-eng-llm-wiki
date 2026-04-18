# Consensus Performance

**Summary**: Chapter 23's treatment of how distributed [[consensus]] systems are actually made fast enough for production, against the folk wisdom that they are "too slow and costly." The chapter catalogues the techniques — [[stable-leader]]s, batching, pipelining, [[quorum-leases]], [[mencius-epaxos|leaderless protocols]], managing [[consensus-disk-access]], scaling reads via replicas — and argues performance depends on matching the technique to the workload and deployment.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The folk wisdom is wrong

Conventional wisdom has generally held that consensus algorithms are too slow and costly to use for systems requiring high throughput and low latency. Chapter 23 pushes back: "This conception is simply not true — while implementations can be slow, there are a number of tricks that can improve performance. Distributed consensus algorithms are at the core of many of Google's critical systems and they have proven extremely effective in practice" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Google's scale is a disadvantage, not an advantage, for this claim: large datasets × several replicas multiply storage cost, and large geographical distances multiply latency. The techniques still work.

## No single best algorithm

Chapter 23 is explicit that "there is no one 'best' distributed consensus and state machine replication algorithm for performance, because performance is dependent on a number of factors relating to workload, the system's performance objectives, and how the system is to be deployed" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). [[fast-paxos]] is the canonical example — faster than Classic Paxos on some topologies, slower on others.

## The workload axes

Chapter 23 names the axes any workload should be characterised on before choosing or tuning a consensus system (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Throughput** — proposals per unit of time at peak load
- **Type of requests** — proportion of operations that change state
- **Consistency semantics required for reads** — determines whether replica reads, quorum leases, or full consensus reads are needed
- **Request sizes** — variable-size payloads interact poorly with the stable-leader bandwidth bottleneck

## The deployment axes

And the corresponding deployment choices (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- Local-area vs wide-area deployment
- Quorum composition and where the majority of processes live — see [[quorum-composition]]
- Sharding, pipelining, batching

## The techniques

The chapter catalogues these optimisations, each covered on its own page:

| Technique | What it does | Page |
|---|---|---|
| Stable leader | Skip Phase 1 on subsequent proposals; collapse to one RTT + quorum | [[stable-leader]] |
| Multi-Paxos | The canonical stable-leader protocol | [[multi-paxos]] |
| Quorum leases | Grant read leases so local replicas can serve strongly-consistent reads without consensus | [[quorum-leases]] |
| Read optimisations | Read from leader, quorum lease, or stale replica depending on needs | [[consensus-read-optimisations]] |
| Rotating leader | Mencius: preassign slots to replicas to avoid the leader bottleneck | [[mencius-epaxos]] |
| Leaderless | EPaxos: no leader; better for geographically distributed clients | [[mencius-epaxos]] |
| Batching | Multiple client operations into a single proposal | (covered below) |
| Pipelining | Multiple proposals in-flight at once via sliding window | (covered below) |
| Disk access optimisation | Combine RSM and consensus logs; batch log writes | [[consensus-disk-access]] |
| Proxies | Persistent TCP connections from regional proxies to acceptors; avoids per-client connection setup | (covered below) |

## Batching

Batching increases throughput by amortising the fixed per-consensus costs (disk logging, network latency) over a larger number of operations (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This is why the [[multi-paxos|stable-leader]] architecture dominates over [[fast-paxos]]: proposals are consolidated at a single point (the proposer) so they can be batched consistently.

The technique is specifically called out as easy when there's a single proposer and hard when clients propose directly to acceptors — the latter is why Fast Paxos loses throughput to Classic Paxos under load.

## Pipelining

Batching still leaves replicas idle while awaiting replies. **Pipelining** allows multiple proposals to be in-flight at once — similar to TCP's sliding-window approach keeping the pipe full. Pipelining is normally used in combination with batching. The pipelined batches are still globally ordered by view number and transaction number, so the [[replicated-state-machine|RSM]] global-ordering property holds (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## Network considerations

Network RTTs vary enormously by distance. Within a datacenter: ~1ms. Across the US: ~45ms. New York to London: ~70ms (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Consensus performance over a LAN can be comparable to asynchronous leader-follower replication; over a WAN, the replica latency dominates.

TCP/IP adds a one-round-trip three-way handshake plus slow start (initial window 4–15 KB). Persistent connections between the consensus group members avoid this overhead internally. For systems with very many clients — sharded consensus clusters with thousands of replicas and larger numbers of clients — a **pool of regional proxies** that hold persistent TCP/IP connections to the consensus group is the Chapter 23 mitigation (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Proxies also encapsulate sharding, load balancing, and cluster-membership discovery.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[multi-paxos]]
- [[fast-paxos]]
- [[stable-leader]]
- [[quorum-leases]]
- [[consensus-read-optimisations]]
- [[mencius-epaxos]]
- [[consensus-disk-access]]
- [[consensus-replica-count]]
- [[consensus-replica-placement]]
- [[quorum-composition]]
