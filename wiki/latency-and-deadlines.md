# Latency and Deadlines

**Summary**: SRE Chapter 22's framing of RPC deadlines as a cascading-failure defence. A deadline caps how long a server may consume the client's resources; without deadlines, a slow downstream holds upstream resources until both servers restart. Missed deadlines also waste work — once the client has given up, any further processing the server does is useless. Picking a good deadline is a trade-off between short (expensive requests fail consistently) and long (stale work consumes resources far longer than needed). The detailed mechanics — how deadlines travel through a request tree, and why each server must check the remaining deadline before continuing — are on [[deadline-propagation]]; the special failure mode of a small fraction of requests exhausting resources by never completing is on [[bimodal-latency]].

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## Why deadlines matter for cascading failure

Chapter 22's core statement (source: chapter-22-addressing-cascading-failures.md):

> When a frontend sends an RPC to a backend server, the frontend consumes resources waiting for a reply. RPC deadlines define how long a request can wait before the frontend gives up, limiting the time that the backend may consume the frontend's resources.

The cascading-failure consequence: without deadlines, a single slow downstream can indefinitely hold upstream thread-pool capacity, memory for in-flight request state, and open connections. The slow downstream has effectively rented a piece of every upstream service it touches. When multiple upstreams share thread pools or connection pools (see [[bulkhead]]), the slow downstream's reach extends further still — into unrelated requests that don't even touch it.

## Picking a deadline

From the chapter (source: chapter-22-addressing-cascading-failures.md):

> It's usually wise to set a deadline. Setting either no deadline or an extremely high deadline may cause short-term problems that have long since passed to continue to consume server resources until the server restarts. High deadlines can result in resource consumption in higher levels of the stack when lower levels of the stack are having problems. Short deadlines can cause some more expensive requests to fail consistently. Balancing these constraints to pick a good deadline can be something of an art.

The trade-off:

- **Very long deadline (or none).** Stale work consumes resources long after the client has given up. A slow downstream can tie up upstream capacity for minutes or hours. "Until the server restarts" is the tail latency of an unbounded deadline.
- **Very short deadline.** Requests that *could* have succeeded given more time fail. The service-specific p99 may consistently miss a deadline set at the p95.

The practical approach: measure request-latency distributions, pick a deadline somewhere in the upper tail (p99 or p99.9) with margin for the backend itself to have its own downstream deadlines and latency.

## Missed deadlines

From the chapter (source: chapter-22-addressing-cascading-failures.md):

> A common theme in many cascading outages is that servers spend resources handling requests that will exceed their deadlines on the client. As a result, resources are spent while no progress is made: you don't get credit for late assignments with RPCs.

The chapter's memorable worked example:

> Suppose an RPC has a 10-second deadline, as set by the client. The server is very overloaded, and as a result, it takes 11 seconds to move from a queue to a thread pool. At this point, the client has already given up on the request. Under most circumstances, it would be unwise for the server to attempt to handle this request, because it would be doing work for which no credit will be granted — the client doesn't care what work the server does after the deadline has passed, because it's given up on the request already.

The prescription: **check the deadline before starting work**. If a request is split into stages (parse, backend request, process), check at each stage that enough deadline remains to justify proceeding.

The chapter notes an exception: servers that write periodic checkpoints of long-running work (catchup operations, for example) may wish to continue past the deadline in order to save their progress. Here, "check after writing the checkpoint" is the right rule, not "check before starting the expensive operation."

## Deadline propagation

The mechanism by which a deadline set at the top of the stack applies to all downstream calls without being reinvented at each layer has its own page: [[deadline-propagation]]. The short version: every RPC in the subtree of an initial request should share the initial deadline. If server A sets a 30-second deadline, and processes for 7 seconds before calling B, the A→B RPC has 23 seconds. If B takes 4 seconds before calling C, the B→C RPC has 19 seconds. And so on.

Without propagation, an RPC late in the stack may have a hardcoded 20-second deadline even when only 2 seconds of the original 30-second budget remain — and C will spend up to 20 seconds doing work the root has already given up on.

## Bimodal latency

A related failure mode is when a fraction of requests never complete at all, consuming resources proportional to the full deadline while the rest complete quickly. This is covered separately on [[bimodal-latency]]. The short version: a 5% unavailable keyspace with a 100-second deadline and a 1,000-thread frontend converts into an 80% error rate, because the 5% that never complete consume far more capacity than their share.

## Relationship to other wiki concepts

### Deadlines and [[timeouts]]

Kleppmann's [[timeouts]] discussion treats the client's perspective: how long before the client gives up. Chapter 22's deadlines extend this to the server's perspective: the server shouldn't do work beyond what the client is willing to wait for. The concepts overlap but aren't identical:

- **Timeout** — the client's maximum wait before giving up.
- **Deadline** — the absolute time by which the request must be answered; deadlines are more useful in stacked RPC trees because they naturally propagate, whereas timeouts reset at each hop unless explicitly decremented.

Deadline-based RPC frameworks (gRPC, Stubby) make deadline propagation automatic. Timeout-based frameworks (many older HTTP libraries) require each hop to compute its own timeout budget from the incoming request's remaining deadline — which is error-prone.

### Deadlines and [[queue-management]]

A deadline should be checked when a request is dequeued. If the deadline has passed during the wait, the request should be dropped rather than served. This is the [[queue-management|CoDel-like]] discipline that converts stale queued requests into useful shedding.

### Deadlines and [[retry-amplification]]

Retries without deadline awareness compound the problem. A client retrying a request that has already exceeded its overall deadline wastes work at every layer — the backend will reject, the retry budget counts, and the original request has no chance of being served. The RPC framework should carry the deadline through retries so that retries whose deadline has passed are skipped entirely.

### Deadlines and [[circuit-breaker]]

Deadlines provide the failure signal that feeds a [[circuit-breaker]]: a call that exceeds its deadline counts as a failure. Without deadlines, a slow downstream might never hit the breaker's failure counter.

### Deadlines and [[stubby]]

Google's RPC framework [[stubby]] has deadlines as a first-class part of every RPC, and deadline propagation is automatic. This is one of the many ways Google's RPC infrastructure differs from a plain HTTP-based microservice stack — the fault-tolerance mechanisms are built into the transport.

## Related pages

- [[cascading-failure]]
- [[deadline-propagation]]
- [[bimodal-latency]]
- [[timeouts]]
- [[queue-management]]
- [[retry-amplification]]
- [[retry-budget]]
- [[circuit-breaker]]
- [[stubby]]
- [[site-reliability-engineering]]
