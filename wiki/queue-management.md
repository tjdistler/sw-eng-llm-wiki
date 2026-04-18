# Queue Management

**Summary**: Thread-per-request servers queue incoming work in front of a worker pool. SRE Chapter 22's thesis on queue sizing: for services with fairly steady traffic, **keep queues small** (50% of the thread-pool size or less) and reject excess work early, rather than buffering it. A long queue looks like it smooths bursts, but mostly it inflates tail latency and consumes memory — and under sustained overload, a queue full of stale requests is work the server is committed to but will complete too late to matter. Gmail famously uses **queueless** servers; on the other end, bursty-load services may size queues dynamically based on current thread usage.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Most thread-per-request servers use a queue in front of a thread pool to handle requests. Requests come in, they sit on a queue, and then threads pick requests off the queue and perform the actual work... Usually, if the queue is full, the server will reject new requests.

The core question is how big the queue should be. Chapter 22's answer depends on traffic shape.

## The steady-state argument

For steady-state traffic, queues are an unnecessary capacity tax (source: chapter-22-addressing-cascading-failures.md):

> If the request rate and latency of a given task is constant, there is no reason to queue requests: a constant number of threads should be occupied. Under this idealized scenario, requests will only be queued if the steady state rate of incoming requests exceeds the rate at which the server can process requests, which results in saturation of both the thread pool and the queue.

If throughput matches demand, there's no reason for requests to queue. The *only* time a queue fills is when demand exceeds throughput — which is the condition the server should be shedding, not buffering.

The chapter's concrete sizing rule:

> For a system with fairly steady traffic over time, it is usually better to have small queue lengths relative to the thread pool size (e.g., 50% or less), which results in the server rejecting requests early when it can't sustain the rate of incoming requests.

A small queue does two things: it gives a tiny bit of buffer for micro-bursts that resolve quickly, and it ensures that once the server is sustainedly overloaded, it starts rejecting instead of queueing.

## The queue-latency math

Chapter 22 works the numbers (source: chapter-22-addressing-cascading-failures.md):

> For example, if the queue size is 10x the number of threads, the time to handle the request on a thread is 100 milliseconds. If the queue is full, then a request will take 1.1 seconds to handle, most of which time is spent on the queue.

A 10x queue doesn't buy 10x more throughput; it buys 10x more latency for requests that arrive when it's full. From the user's perspective, the server becomes progressively slower as overload continues — which is almost always worse than fast rejection.

## Gmail's queueless approach

The chapter cites Gmail as an example of the extreme (source: chapter-22-addressing-cascading-failures.md):

> For example, Gmail often uses queueless servers, relying instead on failover to other server tasks when the threads are full.

With no queue, a request that finds every thread busy fails immediately. The load balancer or RPC retry logic directs the client to a different task, which likely has capacity. This approach:

- Minimises tail latency — no request ever waits in a queue.
- Pushes the buffering work to the load-balancing layer, which has global information about capacity.
- Depends on the existence of spare capacity elsewhere; it only works if the fleet is provisioned such that individual tasks saturating is the exception.

This is the aggressive end of the spectrum.

## Bursty traffic: dynamic queue sizing

The other end (source: chapter-22-addressing-cascading-failures.md):

> On the other end of the spectrum, systems with "bursty" load for which traffic patterns fluctuate drastically may do better with a queue size based on the current number of threads in use, processing time for each request, and the size and frequency of bursts.

For services where bursts are the norm — short sharp traffic spikes that resolve in seconds — a dynamic queue sized to absorb the burst without overflowing is useful. The parameters the chapter names:

- Current thread pool occupancy.
- Per-request processing time.
- Burst size and frequency.

The rough heuristic: size the queue to cover a single expected burst at full thread occupancy, plus margin. Anything larger just adds latency to requests arriving after the burst has exceeded what the thread pool can sustain.

## Queue-ordering policies

Chapter 22's [[load-shedding]] section names queue-ordering as a complementary discipline (source: chapter-22-addressing-cascading-failures.md):

> Changing the queuing method from the standard first-in, first-out (FIFO) to last-in, first-out (LIFO) or using the controlled delay (CoDel) algorithm or similar approaches can reduce load by removing requests that are unlikely to be worth processing.

The intuition: under overload, the *oldest* queued request is the one most likely to have already exceeded its deadline. Serving it is wasted work — the client has probably already retried or given up. Serving fresher requests first gives more useful work per unit of capacity.

- **FIFO** — fair, but serves stale requests when overloaded.
- **LIFO** — discards the oldest requests; under overload, keeps the most recent work.
- **CoDel** (Controlled Delay, Nichols et al. 2012) — estimates queueing delay and drops packets (or requests) when it exceeds a target. The preferred modern approach.

CoDel is particularly effective because it targets the *condition* (sustained queueing delay) rather than a proxy (queue length).

## Deadlines complement queue management

From the chapter (source: chapter-22-addressing-cascading-failures.md):

> This strategy works well when combined with propagating RPC deadlines throughout the stack.

The queue should check each request's remaining deadline when dequeuing; if the deadline has passed, drop the request rather than serve it. See [[deadline-propagation]] for how deadlines flow through a stack of servers, and [[latency-and-deadlines]] for the broader discussion.

## Relationship to other wiki concepts

### Queue management and [[load-shedding]]

Queue management is one realisation of [[load-shedding]]: when the queue is full, reject. The chapter explicitly lists "limiting queue length" as a form of shedding. The shedding decision combines queue state with [[utilization-signals|utilisation]] and [[request-criticality|criticality]].

### Queue management and [[bulkhead]]

Per-dependency thread pools (one of the [[bulkhead]] forms) imply per-dependency queues. Sizing each queue independently per dependency, based on each dependency's traffic shape, is the fine-grained version of the Chapter 22 advice.

### Queue management and [[connection-level-load]]

Chapter 21's [[connection-level-load]] section discusses the related problem of *connection* queueing — maintaining idle connections is itself work, and a fan-in of many slow clients can dominate the thread pool's capacity even if request queues are tiny. Queue management is one piece of the admission-control picture; connection-level admission is another.

### Queue management and the batch-proxy pattern

Chapter 21's [[connection-level-load|batch-proxy fuse]] is a case where queue sizing really matters: batch clients generate bursty connection storms that would overflow any reasonable request queue. Putting the batch traffic behind its own proxy with its own queue (sized for the burst) bulkheads the interactive-traffic queue from batch-client noise.

### Queue management and Kleppmann's queueing chapters

Kleppmann's performance-and-percentile material ([[response-time-percentiles]], [[tail-latency-amplification]]) is the theoretical substrate. M/M/1 queueing theory says wait time grows unbounded as utilisation approaches 1; what Chapter 22 prescribes is how server design choices avoid realising the asymptote.

## Related pages

- [[cascading-failure]]
- [[resource-exhaustion]]
- [[load-shedding]]
- [[deadline-propagation]]
- [[latency-and-deadlines]]
- [[connection-level-load]]
- [[bulkhead]]
- [[response-time-percentiles]]
- [[tail-latency-amplification]]
- [[site-reliability-engineering]]
