---
name: Load Parameters
description: Quantitative metrics that describe the current load on a system, used as the basis for scalability reasoning
type: concept
---

# Load Parameters

**Summary**: Load parameters are the numbers that best describe what a system is currently doing — the foundation for any meaningful discussion of scalability or performance.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-15

---

## What load parameters are

You cannot reason about [[scalability]] without first quantifying load. Load parameters are the metrics that capture the current state of demand on a system. The right choice of parameters depends entirely on the architecture and workload. Examples:

- Requests per second to a web server
- Ratio of reads to writes in a database
- Number of simultaneously active users in a chat room
- Cache hit rate
- **Fan-out** — the number of downstream requests triggered per incoming request (see below)

The relevant parameter is whichever one dominates your bottleneck: sometimes the average case matters; sometimes a small number of extreme cases determine everything. (source: chapter-01)

## Fan-out as a load parameter

**Fan-out** is a term borrowed from electronics, where it describes the number of gate inputs attached to a single gate output. In distributed systems, it describes the number of downstream requests needed to serve one incoming request.

The Twitter home timeline problem illustrates this well. (source: chapter-01)

The key load parameter is not tweet volume (4.6k/sec average posts is manageable), but **follower distribution** — specifically how many people each user follows and is followed by. The average fan-out per tweet is ~75 followers, producing ~345k cache writes/sec. But some users have 30+ million followers, meaning a single tweet could trigger 30 million writes. That extreme tail, not the average, drives architectural decisions.

This is a general principle: identify which load parameter is the actual bottleneck driver, including its distribution, not just its mean.

## Load parameters and architectural decisions

Load parameters determine what tradeoffs make sense. A system optimized for:

- **High read volume, low write volume**: pre-compute and cache results at write time (push model)
- **High write volume, low read volume**: compute results at read time (pull/query model)
- **Balanced read/write**: hybrid approaches, often per-user or per-entity

Twitter moved from pull (approach 1) to push (approach 2) because reads outnumbered writes by roughly two orders of magnitude, making write-time fan-out the better tradeoff. Their current hybrid approach handles celebrity accounts (extreme outliers) separately. (source: chapter-01)

## Connecting load to performance

Once load is described, you can ask:

1. With resources fixed, how does performance change if load doubles?
2. To keep performance constant, how much additional resource is needed if load doubles?

Both questions require [[response-time-percentiles]] or throughput numbers as the performance side of the equation.

## Related pages

- [[scalability]]
- [[response-time-percentiles]]
- [[scaling-approaches]]
