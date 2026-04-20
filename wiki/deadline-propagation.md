# Deadline Propagation

**Summary**: The discipline of attaching a deadline to the top of a request tree and having it flow through every downstream RPC, so that every server in the subtree shares the same absolute deadline rather than inventing fresh ones. SRE Chapter 22 develops this as a cascading-failure defence: without propagation, deep backends may have deadlines longer than the root's remaining budget, and will do work that the top of the stack has already given up on. **Cancellation propagation** is the companion: when the top-level call is cancelled or times out, the cancellation flows down the tree so in-flight work can stop early rather than running to completion.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The mechanic

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> With deadline propagation, a deadline is set high in the stack (e.g., in the frontend). The tree of RPCs emanating from an initial request will all have the same absolute deadline. For example, if server A selects a 30-second deadline, and processes the request for 7 seconds before sending an RPC to server B, the RPC from A to B will have a 23-second deadline. If server B takes 4 seconds to handle the request and sends an RPC to server C, the RPC from B to C will have a 19-second deadline, and so on. Ideally, each server in the request tree implements deadline propagation.

The pattern:

- A single absolute deadline (wall-clock time by which the root must have an answer) is set once at the top.
- Every outgoing RPC carries the *remaining* budget at the moment of dispatch.
- Each server handling the RPC knows how much time it has.
- Requests whose deadline has already passed can be short-circuited immediately.

## Why it matters

Without propagation, each layer of the stack invents its own deadline based on local assumptions — which may be wildly inappropriate given what has already happened upstream. Chapter 22's worked example (source: chapter-22-addressing-cascading-failures.md):

1. Server A sends an RPC to server B with a 10-second deadline.
2. Server B takes 8 seconds to start processing, then needs to call server C.
3. **With propagation**: B sets a 2-second deadline on the RPC to C, matching what actually remains.
4. **Without propagation**: B uses a hardcoded 20-second deadline for the RPC to C.
5. Server C pulls the request off its queue after 5 seconds.
6. **With propagation**: C immediately gives up — its 2-second budget is already gone.
7. **Without propagation**: C processes the request thinking it has 15 seconds, doing work that A will never credit because the A→B RPC has already timed out.

Step 7 is wasted capacity that a healthy service cannot afford to give up. Under cascading-failure conditions, where many requests are doing exactly this, the wasted capacity is the difference between recovering and collapsing.

## Implementation details

Chapter 22 adds a pair of practical refinements (source: chapter-22-addressing-cascading-failures.md):

> You may want to reduce the outgoing deadline a bit (e.g., a few hundred milliseconds) to account for network transit times and post-processing in the client.

Each hop adds its own latency — network transit, deserialization, handling. Passing the full remaining budget means the *callee* experiences a deadline slightly later than the caller expected, and its own deadline checks will show more time remaining than really exists. A small safety margin per hop (a hundred milliseconds, say) accounts for this.

> Also consider setting an upper bound for outgoing deadlines. You may want to limit how long the server waits for outgoing RPCs to noncritical backends, or for RPCs to backends that typically complete in a short duration.

The propagated deadline might be generous because the root allowed plenty of time. But for a noncritical backend that should complete quickly, holding a long deadline open keeps resources consumed long after it should be given up. Capping the outgoing deadline at some lower ceiling preserves the server's ability to free resources fast for noncritical calls even when the root's deadline is long.

The chapter adds a cautionary note:

> However, be sure to understand your traffic mix, because you might otherwise inadvertently make particular types of requests fail all the time (e.g., requests with large payloads, or requests that require responding to a lot of computation).

Hard-capping outgoing deadlines can starve legitimate slow requests. The right answer is workload-aware.

## Exceptions

Most servers should honour the deadline, but the chapter notes one exception (source: chapter-22-addressing-cascading-failures.md):

> There are some exceptions for which servers may wish to continue processing a request after the deadline has elapsed. For example, if a server receives a request that involves performing some expensive catchup operation and periodically checkpoints the progress of the catchup, it would be a good idea to check the deadline only after writing the checkpoint, instead of after the expensive operation.

The general pattern: if the work has side effects that preserve progress (checkpoints, commits, atomic state updates), finish the current step before checking the deadline. Otherwise, check before doing expensive work.

## Cancellation propagation

The companion mechanism (source: chapter-22-addressing-cascading-failures.md):

> Propagating cancellations avoids the potential RPC leakage that occurs if an initial RPC has a long deadline, but RPCs between deeper layers of the stack have short deadlines and time out. Using simple deadline propagation, the initial RPC continues to use server resources until it eventually times out, despite being unable to make progress.

Deadline propagation alone doesn't cover the case where an early-stack call has a short deadline and fails before the outer call's deadline. Cancellation propagation closes this gap: when any call in the tree is cancelled (by deadline expiry, explicit cancellation, or client disconnect), the cancellation is propagated up and down. In-flight work further down the tree can then stop immediately rather than continuing until the deadline it holds.

Modern RPC frameworks (gRPC, Stubby) implement both: deadlines propagate down the tree, cancellations propagate across the tree.

## Relationship to other wiki concepts

### Deadline propagation and [[latency-and-deadlines]]

[[latency-and-deadlines]] is the Chapter 22 hub for the broader discussion of why deadlines matter. Deadline propagation is the specific discipline that makes deadlines work correctly in multi-layer RPC trees.

### Deadline propagation and the RPC framework

Google's internal RPC framework (open-sourced as gRPC) has deadlines as a first-class envelope field. Every RPC call carries an absolute deadline; the deadline is automatically propagated by the framework when the server opens an outgoing call in the context of the incoming one. This is one of the ways gRPC materially differs from libraries that require manual threading of the deadline.

### Deadline propagation and [[correlation-ids]]

The propagation mechanism for deadlines is the same mechanism used for [[correlation-ids]]: a field in the RPC envelope that travels with the call. Both are examples of request-context metadata that must be plumbed through every hop. The RPC framework is the natural place to implement both.

### Deadline propagation and [[queue-management]]

A queued request whose propagated deadline has expired should be dropped when dequeued rather than served. The check is a simple test of "is the propagated deadline in the past?" at the moment of dequeue. See [[queue-management]] for the broader policy of deadline-aware queueing.

### Deadline propagation and [[bimodal-latency]]

The [[bimodal-latency]] failure mode is specifically what happens when a fraction of requests exhaust their deadline without completing. Deadline propagation ensures the exhausted deadline propagates to downstream calls rather than being silently extended — which makes the failure mode shorter-lived than it would be otherwise.

### Deadline propagation and distributed tracing

[[distributed-tracing]] systems carry trace context through every RPC hop, and the same infrastructure typically carries the deadline. The implementation overlap is convenient: a service instrumented for distributed tracing is almost certainly already plumbing a context object through every call, and adding deadline propagation is low-cost marginal work.

## Related pages

- [[latency-and-deadlines]]
- [[cascading-failure]]
- [[bimodal-latency]]
- [[queue-management]]
- [[correlation-ids]]
- [[distributed-tracing]]
- [[retry-budget]]
- [[site-reliability-engineering]]
