# Timeouts

**Summary**: The primary mechanism for detecting faults in distributed systems, but choosing the right timeout value is a fundamental tradeoff between fast fault detection and the risk of falsely declaring healthy nodes dead.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The timeout dilemma

A timeout is often the only sure way of detecting a fault in a distributed system, since [[unreliable-networks]] make it impossible to distinguish a dead node from a slow one. But there is no simple answer for how long a timeout should be. (source: designing-data-intensive-applications, chapter 8)

- **Long timeout**: slow to declare a node dead. Users may see errors or wait for extended periods during genuine failures.
- **Short timeout**: detects faults faster, but carries a higher risk of **falsely declaring a node dead** when it has only suffered a temporary slowdown (load spike, network congestion).

## Dangers of premature declaration of death

Prematurely declaring a node dead is problematic (source: designing-data-intensive-applications, chapter 8):

- If the node is alive and performing an action (e.g., sending an email), and another node takes over, the action may be performed twice.
- The "dead" node's responsibilities must be transferred to other nodes, adding load. If the system is already under high load, this can trigger a **cascading failure** -- nodes declare each other dead due to slowness caused by transferred load, and everything stops.

## Why fixed timeouts don't work

In an ideal system with bounded network delay *d* and bounded processing time *r*, a timeout of **2d + r** would be correct. But real systems have neither guarantee (source: designing-data-intensive-applications, chapter 8):

- Asynchronous networks have **unbounded delays** -- there is no upper limit on packet delivery time.
- Most servers cannot guarantee bounded request processing time (see [[process-pauses]]).
- For failure detection, being fast *most of the time* is not sufficient -- a transient spike in round-trip times can throw the system off balance.

## Adaptive timeouts

Rather than using configured constant timeouts, systems can continually measure response times and their variability (jitter), and automatically adjust timeouts to the observed distribution. (source: designing-data-intensive-applications, chapter 8)

The **Phi Accrual failure detector** is one such approach, used in Akka and Cassandra. It outputs a suspicion level rather than a binary alive/dead judgment. TCP retransmission timeouts work similarly, adapting to observed round-trip times. (source: designing-data-intensive-applications, chapter 8)

In practice, timeouts should be determined experimentally by measuring the distribution of network round-trip times over an extended period across many machines, then choosing a tradeoff between detection delay and premature-timeout risk appropriate for the application. (source: designing-data-intensive-applications, chapter 8)

## Deadlines: the server-side counterpart

SRE Chapter 22 develops the complementary notion of an RPC **deadline** (source: chapter-22-addressing-cascading-failures.md): an absolute wall-clock time by which the request must be answered, propagated from the top of the request tree through every downstream call. Where a timeout is the client's maximum wait, a deadline is the collective budget the whole call tree shares.

Deadline-based frameworks (gRPC, Stubby) have two advantages over timeout-based frameworks for cascading-failure prevention:

- **Propagation.** The deadline flows through every RPC in the subtree. A deep backend with a 19-second remaining budget knows exactly how long it has, so it can short-circuit work that won't complete in time.
- **Cancellation.** When any call in the tree is cancelled (by deadline expiry or client disconnect), the cancellation propagates across the tree, stopping in-flight work that would otherwise continue until its own local deadline.

Chapter 22 treats deadlines as a cascading-failure defence: servers that do work whose results are thrown away consume resources for no benefit, and under load this wasted work becomes the difference between surviving and cascading. See [[latency-and-deadlines]] for the picking-a-deadline discussion, [[deadline-propagation]] for the mechanic, and [[bimodal-latency]] for the specific failure mode where too-long deadlines amplify a small unavailability into a large one.

## Related pages

- [[unreliable-networks]]
- [[network-faults]]
- [[partial-failures]]
- [[failover]]
- [[process-pauses]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[latency-and-deadlines]]
- [[deadline-propagation]]
- [[bimodal-latency]]
- [[cascading-failure]]
