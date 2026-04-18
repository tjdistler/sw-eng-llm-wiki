# Fast Paxos

**Summary**: A [[paxos|Paxos]] variant (Lamport, 2006) in which clients send Propose messages directly to every acceptor instead of going through a proposer — substituting one parallel client-to-acceptors send for the proposer-to-acceptors fan-out of Classic Paxos. Intuitively faster; in practice often **slower** than Classic Paxos when the slow links are on the client-to-acceptor legs, because the latency-tail effect makes a single hop across a slow link faster than a quorum of hops.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`, `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## The idea

In [[paxos|Classic Paxos]] and [[multi-paxos|Multi-Paxos]], a client sends its request to a single proposer, which fans it out to a quorum of acceptors. Fast Paxos collapses this into a single parallel client-to-acceptors send, removing the proposer hop (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- **Classic Paxos**: client → one proposer (one message across whatever link), then proposer → N acceptors (N parallel messages).
- **Fast Paxos**: client → N acceptors directly (N parallel messages).

On first principles this looks like a strict win.

## Why it can be slower

Chapter 23 is pointed: "it seems as though Fast Paxos should always be faster than Classic Paxos. However, that's not true" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The scenario where it loses: the client has a high RTT to the acceptors, but the acceptors have fast connections to each other. In that topology:

- **Fast Paxos** has N parallel messages across the slow client-to-acceptor links and must wait for a quorum of them.
- **Classic Paxos** has one message across the slow link (client to proposer) followed by N parallel messages across the fast links.

Because of the **latency tail effect** — the distribution of latencies on a slow link has a long right tail — waiting for a quorum of N messages across slow links is usually slower than one message across the slow link plus a quorum across the fast links. The quorum-of-slow-hops is bounded by the slowest few packets in the distribution; the single-slow-hop pays only one draw from that distribution.

This is the same statistical argument that motivates [[long-tail-latency]] observation in monitoring and [[tail-latency-amplification]] in scatter-gather serving: parallel slow events compound rather than cancel.

## The batching problem

Many consensus systems batch multiple operations into a single transaction at the acceptor to increase throughput. Fast Paxos makes batching much harder because proposals now arrive independently at acceptors from different clients — so acceptors cannot batch them in a consistent way across replicas (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Multi-Paxos batches naturally at the proposer; Fast Paxos does not.

## When Fast Paxos does win

Fast Paxos can be a win when:

- The client-to-acceptor RTT is comparable to or smaller than proposer-to-acceptor RTT (so the "slow link" premise doesn't hold).
- The workload is low enough that batching is not needed.
- Throughput is not the binding constraint.

For the common Google-scale case — clients across wide-area networks, high throughput, batching essential — the chapter's framing is that Multi-Paxos's stable leader plus batching beats Fast Paxos in practice.

## A production Google user: the distributed cron service

Chapter 24 names Fast Paxos as the Paxos variant used inside Google's [[distributed-cron|distributed cron service]]: "the variant of Paxos we use, Fast Paxos, uses a leader replica internally as an optimization — the Fast Paxos leader replica also acts as the cron service leader" (source: chapter-24-distributed-periodic-scheduling-with-cron.md). The cron service is a deliberately benign workload for Fast Paxos:

- **Small replica group** (three replicas) within a single datacenter → fast, homogeneous client-to-acceptor RTTs, so the "slow link" disadvantage that Chapter 23 warns about doesn't bite.
- **Low write volume** — a handful of state transitions per cron-job launch, and cron-job launches are minute-grained at worst → the batching disadvantage doesn't bite either.
- **What matters is the leader** — the cron service reuses Fast Paxos's internally-elected leader as its own application-level service leader, so Fast Paxos's internal leader machinery is doing double duty. See [[cron-leader-follower]].

This is a good illustration of Chapter 23's "no one best algorithm" claim — Fast Paxos is a reasonable fit in one production system and a worse fit in the wide-area multi-client workload the Chapter 23 analysis is built around.

## The broader lesson

Chapter 23 uses Fast Paxos as an example of why "there is no one 'best' distributed consensus and state machine replication algorithm for performance, because performance is dependent on a number of factors relating to workload, the system's performance objectives, and how the system is to be deployed" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). What looks faster on the message-count axis may be slower on the percentile-latency axis, and neither tells you about throughput under batching.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[paxos]]
- [[multi-paxos]]
- [[stable-leader]]
- [[consensus-performance]]
- [[long-tail-latency]]
- [[tail-latency-amplification]]
- [[mencius-epaxos]]
- [[distributed-cron]]
- [[cron-leader-follower]]
