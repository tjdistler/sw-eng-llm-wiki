# Dynamic Worker Scaling

**Summary**: Burns's treatment of how many workers a [[work-queue-pattern|work queue]] should run at any given moment. The unbounded-parallelism default (spin up a worker per item as fast as items arrive) causes bursty cluster load and wastes resources during slack periods. The bounded-parallelism fix (a hard worker cap) flattens load but risks falling permanently behind under sustained high load. The stable middle ground is a simple autoscaler driven by two metrics: the **interarrival time** of new items and the **per-item processing time**.

**Sources**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`

**Last updated**: 2026-04-16

---

## The three regimes

Burns introduces the scaling problem by walking through three regimes (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

### Regime 1: uncapped workers

The queue manager spawns one worker per pending item as soon as the item appears. This is the fastest way to drain the queue — wall-clock latency per item is minimized — but it produces **bursty resource load** on the orchestrator cluster. If your cluster has enough varied workloads that their bursts don't align, it works fine; if not, the cluster must be provisioned for the peak and sits idle the rest of the time (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

### Regime 2: hard worker cap

Limit the number of Job objects the queue-manager is willing to create concurrently. This smooths the load but trades latency for smoothness: under heavy load, items wait in the queue longer. For **bursty** workloads this is acceptable — slack periods let the manager catch up. For **sustained** high-load workloads it is not — the queue grows monotonically and the per-item latency trends toward infinity (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

### Regime 3: dynamic scaling

The right answer is to adjust the worker count dynamically based on observed load. The scaling rule falls out of a simple queueing argument.

## The interarrival-time math

Burns's analysis rests on two measured quantities (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

- **Interarrival time**: average time between new items arriving at the queue, measured as `# work items / 24 hours` (or whatever window you choose).
- **Processing time**: average wall-clock time to process one item once work begins (not counting queue wait).

For a stable queue, the **effective per-item processing time must be less than the interarrival time**. "Effective" here is the processing time divided by the parallelism (number of workers), since workers process items concurrently.

Burns works three concrete numbers:

| Arrival rate | Processing time | Verdict |
|---|---|---|
| 1 item/min | 30 s each | Processes 2-for-1; catches up from any backlog |
| 1 item/min | 1 min each | Perfectly balanced; no slack for variance |
| 1 item/min | 2 min each | Falls behind without bound; user-visible latency grows |

The balanced case is a warning, not a target. Production systems need **safety margin** — slack to absorb variance, growth, and occasional slowdowns (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

### The rule

Given parallelism `P`, the steady-state condition is:

```
(processing_time / P) < interarrival_time
```

Rearranged, the minimum stable parallelism is:

```
P > processing_time / interarrival_time
```

Burns's worked example: one-minute items and one-every-16-seconds arrivals need parallelism of at least 4 (60s / 16s = 3.75, so 4). At parallelism 4 the effective processing time is 15s, comfortably under the 16s interarrival time.

## Building an autoscaler from the rule

Scaling **up** is mechanical: if observed `processing_time / P >= interarrival_time` (the queue is not draining), increase `P` until the inequality holds with margin.

Scaling **down** is trickier because removing workers while items are in flight risks stranding them. Burns recommends the same formula plus a spare-capacity heuristic: "you can reduce the parallelism until the processing time for an item is 90% of the interarrival time for new items" (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). This keeps a 10% safety margin and smooths out the scale-down decision.

## Relationship to wiki concepts

### Scaling approaches

This is a concrete application of [[scaling-approaches]] — horizontal, elastic scaling of stateless worker replicas. The queue makes scaling elastic because each worker is ephemeral (runs one item and exits), so reducing `P` just means "stop launching new workers"; no in-flight state is lost.

### Hot sharding as a cousin

Burns's earlier [[hot-sharding]] (Chapter 6) is a parallel instinct applied to **serving** rather than batch: autoscale each shard's replica count in response to organic traffic skew. Both patterns use observed load metrics to push resource usage toward the load's actual shape. The batch case is cleaner because there's only one dimension (queue depth) and no per-shard skew to reason about.

### Response-time percentiles

The "perfectly balanced" warning ties back to [[response-time-percentiles]] — the mean arrival and processing rates hide the variance that determines tail latency. A queue whose mean is at capacity will have p95/p99 latencies that blow up in practice, because any burst above the mean pushes items into a queue that never drains.

### Scalability

The work queue is a textbook [[scalability]] problem: the system must keep up with a workload whose rate may change by orders of magnitude day-to-day. Dynamic worker scaling is the lever.

### Message-broker consumer scaling

The same math applies to [[message-brokers|message broker]] consumer pools and to stream-processing job parallelism: if consumer processing rate is slower than producer arrival rate, lag grows without bound. Burns's framing — in terms of container orchestrator Jobs and Kubernetes autoscaling — is the container-level form of that classic result.

## Related pages

- [[work-queue-pattern]]
- [[worker-container-interface]]
- [[scaling-approaches]]
- [[scalability]]
- [[hot-sharding]]
- [[response-time-percentiles]]
- [[message-brokers]]
- [[stream-processing]]
- [[designing-distributed-systems]]
