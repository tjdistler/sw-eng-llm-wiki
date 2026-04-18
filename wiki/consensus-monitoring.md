# Consensus Monitoring

**Summary**: Chapter 23's catalogue of what must be monitored on a consensus cluster: member health, lagging replicas, leader existence, leader-change rate, consensus transaction number, proposals seen vs agreed, and throughput/latency. Rapid leader changes mean the leader is flapping (probably a network problem); the transaction number must always increase; a decreasing view number signals a serious bug.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What must be monitored

All important production systems need monitoring to detect outages and for troubleshooting. Consensus systems have specific aspects that warrant attention (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

### Group membership and process health

- **Number of members running in each consensus group** — structural check.
- **Status of each process (healthy or not)** — a process may be *running* but unable to make progress for hardware-related or other reasons.

### Replica state

- **Persistently lagging replicas** — a healthy member may be recovering state from peers after startup, lagging behind the quorum, or participating fully (possibly as leader). Monitoring must distinguish these states.

### Leadership

For a [[stable-leader]] system like [[multi-paxos|Multi-Paxos]]:

- **Whether a leader exists** — **if the system has no leader, it is totally unavailable**. This is the single most important monitoring signal for a stable-leader consensus system.
- **Number of leader changes** — rapid leader changes impair performance, so track the rate. Consensus algorithms mark leader changes with a new **term** or **view** number.
  - Too-rapid increase signals the leader is *flapping*, typically from network connectivity issues.
  - **A decrease in the view number signals a serious bug** — view/term numbers are supposed to be monotonic.

### Progress

- **Consensus transaction number** — most consensus algorithms use an increasing transaction number to indicate progress. The number must always increase over time if the system is healthy.
- **Proposals seen** and **proposals agreed upon** — jointly indicate whether the system is operating correctly. If proposals are being seen but few are being agreed, there is a liveness problem.

### Performance

Not specific to consensus but essential regardless:

- **Throughput and latency** — what the administrators need to understand system performance.

## Performance-debugging metrics

For understanding performance issues and troubleshooting, Chapter 23 also recommends monitoring (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Latency distributions for proposal acceptance** — per-proposal latency, presented as a distribution rather than a mean, for the reasons covered on [[long-tail-latency]] and [[response-time-percentiles]].
- **Distributions of network latencies observed between parts of the system in different locations** — particularly important for wide-area consensus deployments where RTT varies by replica pair.
- **Time acceptors spend on durable logging** — the disk-write bottleneck from [[consensus-disk-access]]; directly measurable at the acceptor.
- **Overall bytes accepted per second** — throughput budget for capacity planning.

## Operational interpretation

The signals compose. A quick read of what these metrics together are saying:

- **Healthy stable-leader consensus system**: leader present, view number stable, transaction number steadily increasing, proposals-seen ≈ proposals-agreed, latency in spec.
- **Flapping leader**: view number increasing rapidly; likely network problems preventing the current leader from holding the role.
- **No leader**: system is unavailable; must page.
- **Replica lagging**: replica status shows it behind the transaction number; may be recovering, may be stuck.
- **Slow disk**: proposer latency distribution has a heavier tail than usual; acceptor durable-logging time up; disk is probably the bottleneck.
- **Quorum at risk**: member count down to bare majority; needs intervention per [[consensus-replica-count]].

## Cross-book framing

- [[four-golden-signals]] (SRE Ch 6) — latency, traffic, errors, saturation; the consensus-specific metrics here are the subset of saturation (lagging replicas, disk time) and errors (proposals-not-agreed) specialised for consensus
- [[long-tail-latency]] / [[response-time-percentiles]] — why latency must be monitored as a distribution, not a mean
- [[symptoms-vs-causes]] (SRE Ch 6) — "no leader exists" is a symptom; "view number increasing rapidly" is a cause; both should be monitored but the symptom is what pages
- [[sli-aggregation]] / [[sli-standardization]] (SRE Ch 4) — the operational framework for defining these metrics consistently
- [[consumer-lag-monitoring]] (Bellemare) — the EDM-world analogue: lagging consumer on an event stream is structurally the same failure mode as a lagging consensus replica
- [[borgmon-rules]] / [[prober]] (SRE Ch 10) — the Google-internal mechanism for implementing these monitors

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[stable-leader]]
- [[consensus-replica-count]]
- [[consensus-disk-access]]
- [[consensus-performance]]
- [[four-golden-signals]]
- [[long-tail-latency]]
- [[sli-standardization]]
