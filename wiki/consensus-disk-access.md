# Consensus Disk Access

**Summary**: One of the two physical constraints on [[consensus]] system performance (the other being network RTT): every commitment an acceptor makes must be logged to persistent storage before the acceptor acknowledges. Chapter 23's operational numbers: a small random disk write is ~10 ms, bounding a single naive consensus operation at ~100 per minute at the tight latency envelope. The chapter's two mitigations: **combine the consensus log and the RSM transaction log into one log** (avoid seek alternation) and **batch multiple client operations** (amortise both disk and network costs).

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why disk writes are mandatory

Logging to persistent storage is required so that a node, having crashed and returned to the cluster, honours its previous commitments. In Paxos, acceptors cannot agree to a proposal when they have already agreed to a proposal with a higher sequence number. If those agreements aren't logged, a crash and restart will cause the acceptor to violate the protocol (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## Where in the protocol the writes happen

For [[multi-paxos|Multi-Paxos]], a disk write must happen whenever a process makes a commitment it must honour. In the performance-critical second phase (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Before an acceptor sends Accepted** — it has promised to accept the proposal.
- **Before the proposer sends Accept** — this Accept message is also an implicit Accepted from the proposer itself.

So a single consensus round involves:

1. One disk write on the proposer.
2. Parallel messages to the acceptors.
3. Parallel disk writes at the acceptors.
4. Return messages.

## A variant that parallelises proposer and acceptor writes

There is a version of Multi-Paxos where the proposer's Accept is **not** treated as an implicit Accepted. The proposer writes to disk **in parallel with** the acceptors and sends an explicit Accept. The latency is then proportional to two message hops plus a quorum of synchronous disk writes executed in parallel (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## The arithmetic

Chapter 23's numbers: if the latency for a small random write to disk is on the order of 10 milliseconds, and network RTTs are negligible in this analysis, the rate of consensus operations is limited to approximately **100 per minute** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). That's wall-clock floor, not throughput — throughput can be much higher with batching and pipelining.

The quoted 10 ms depends heavily on hardware: SSDs, NVMe, and battery-backed RAID all change the number. The shape of the argument survives the specific figure.

## The key optimisation: combine the logs

An RSM needs a transaction log for recovery purposes — the same log-writing discipline any database uses. Chapter 23's observation: the RSM's transaction log and the consensus algorithm's log can be **combined into a single log**. This avoids "constantly alternating between writing to two different physical locations on disk," reducing seek time. The disks can sustain more operations per second, and the system performs more transactions (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## State vs log

In a datastore, disks serve two purposes: maintaining logs and holding system state. Log writes must be flushed directly to disk. **Writes for state changes can be written to a memory cache and flushed to disk later**, reordered to use the most efficient schedule (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This is standard database discipline ported to the consensus-backed datastore.

## Batching for disk cost amortisation

Another possible optimisation: **batch multiple client operations together into one operation at the proposer**. This amortises the fixed costs of disk logging and network latency over a larger number of operations, increasing throughput (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). This connects back to why [[multi-paxos]]'s single-proposer design dominates [[fast-paxos]] on throughput — batching at a single point is structurally straightforward, batching across independently-proposing clients is not.

See [[consensus-performance]] for the broader performance discussion.

## Cross-book framing

- [[b-trees]] / [[sstables-and-lsm-trees]] (Kleppmann) — the same log-flush discipline applies to any durable storage engine; the RSM-plus-consensus logging story is a special case of database WAL-plus-state discipline
- [[write-amplification]] (Kleppmann) — the same "one logical write causing multiple physical writes" concern applies in a consensus-backed datastore
- [[event-sourcing]] (Kleppmann) — the log-as-source-of-truth pattern; the unified RSM-plus-consensus log is an event-sourced view of the consensus operation stream

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[consensus-performance]]
- [[multi-paxos]]
- [[paxos]]
- [[replicated-state-machine]]
- [[reliable-replicated-datastore]]
