# Resource Exhaustion

**Summary**: The mechanism by which [[server-overload|overload]] causes [[cascading-failure|cascading failure]]. SRE Chapter 22 catalogues the four primary exhaustible resources — CPU, memory, threads, file descriptors — and the secondary effects each produces when it runs out. Many of these effects feed each other (CPU starvation → slower requests → more in-flight requests → more memory use → more GC → less CPU), making the root cause hard to identify during an outage. Running out of a resource is often a *desired* effect (something has to give under overload) but the specific failure shape — degrade, crash, or misbehave — decides whether the system cascades or merely slows down.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Running out of a resource can result in higher latency, elevated error rates, or the substitution of lower-quality results. These are in fact desired effects of running out of resources: something eventually needs to give as the load increases beyond what a server can handle.

The word *desired* is important. The goal is not to avoid exhaustion — that's impossible — but to engineer the exhaustion to manifest as **rejection** (caught by [[load-shedding]]) or **degradation** (caught by [[graceful-degradation]]) rather than as a **crash** or **wedge** (the two failure modes that cause cascades).

## CPU exhaustion

Chapter 22's CPU list (source: chapter-22-addressing-cascading-failures.md):

- **Increased number of in-flight requests.** Slower requests accumulate. This affects almost every other resource: memory, active threads, file descriptors, backend resources.
- **Excessively long queue lengths.** If capacity is insufficient at steady state, queues saturate. Latency grows because requests spend time waiting in the queue; memory grows because queues hold request state. See [[queue-management]].
- **Thread starvation.** A thread blocked on a lock may cause health checks to fail if the health-check endpoint can't get served in time.
- **CPU or request starvation.** Internal watchdogs detect that the server isn't making progress and kill it.
- **Missed RPC deadlines.** Responses arrive after clients have given up. The server's work is wasted; clients retry, amplifying load. See [[latency-and-deadlines]].
- **Reduced CPU caching benefits.** More CPU cores used means more cache misses and lower effective throughput.

CPU is the most entangled resource. Almost every other failure mode either causes or is caused by CPU saturation.

## Memory exhaustion

Chapter 22's memory list (source: chapter-22-addressing-cascading-failures.md):

- **Dying tasks.** Container managers kill tasks that exceed their memory limit. Application code crashes when allocation fails.
- **Increased GC rate in Java** — resulting in increased CPU use. This is the [[gc-death-spiral]]: less CPU → slower requests → more concurrent requests → more RAM → more GC → even less CPU.
- **Reduction in cache hit rates.** Less RAM means smaller in-memory caches, meaning more backend RPCs, meaning potential backend overload.

The GC death spiral is the canonical example of *feedback between resources*: memory and CPU exhaustion become the same failure.

## Thread exhaustion

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Thread starvation can directly cause errors or lead to health check failures. If the server adds threads as needed, thread overhead can use too much RAM. In extreme cases, thread starvation can also cause you to run out of process IDs.

Thread pools are one of the most common hard-coded limits in server code, and thread exhaustion converts a slow downstream call into a service-wide failure. See the [[bulkhead]] pattern for the isolation mechanism designed to prevent this.

## File descriptor exhaustion

The most unglamorous failure mode (source: chapter-22-addressing-cascading-failures.md):

> Running out of file descriptors can lead to the inability to initialize network connections, which in turn can cause health checks to fail.

Every network connection consumes a file descriptor. Servers with many idle connections (WebSockets, long polling, keepalive pools) are particularly vulnerable. See [[connection-level-load]] for the closely related problem of connection overhead.

## Dependencies among resources

The chapter's most important observation is that these failure modes feed each other, and in a real outage the observable symptoms rarely name the root cause (source: chapter-22-addressing-cascading-failures.md):

> Note that many of these resource exhaustion scenarios feed from one another — a service experiencing overload often has a host of secondary symptoms that can look like the root cause, making debugging difficult.

The chapter's nine-step worked scenario:

1. A Java frontend has poorly tuned GC parameters.
2. Under high but expected load, the frontend runs out of CPU due to GC.
3. CPU exhaustion slows request completion.
4. More in-progress requests increase RAM use.
5. Memory pressure reduces RAM available for caching.
6. Smaller cache means more cache misses.
7. More cache misses means more backend RPCs.
8. Backend runs out of CPU or threads.
9. Backend health checks fail. Cascading failure.

The tunable parameter (GC settings) is step 1; the visible failure is at step 9. The debugging distance between symptom and cause is what makes these outages hard to diagnose during the incident. It may not be obvious that the backend crash was caused by a cache-hit-rate drop in the frontend, especially if the two components have different owners.

## Design implications

Building a server that exhausts resources *safely* requires specific choices:

- **Short, bounded queues** rather than unbounded (see [[queue-management]]).
- **[[load-shedding|Shed]] at a threshold well below hard resource limits** so rejection is controlled rather than collapse.
- **Watchdogs that kill hung tasks** rather than letting them consume resources indefinitely.
- **Cheap rejection paths** so shedding itself doesn't saturate CPU.
- **RPC deadlines that propagate** so servers don't do work whose results will be ignored (see [[deadline-propagation]]).
- **Connection and thread pools sized to real traffic** — too small causes starvation, too large causes unbounded consumption.
- **Memory limits** that kill the task rather than letting it drag the whole machine down (container-level resource limits).

Each choice converts a resource-exhaustion failure from an uncontrolled crash into a controlled rejection.

## Relationship to other wiki concepts

### Resource exhaustion and [[utilization-signals]]

Chapter 21's [[utilization-signals]] are Google's runtime measurement of resource state — specifically, the executor load average (smoothed count of ready threads vs processor count). This is the *sensor* that feeds [[load-shedding|shedding decisions]]. Chapter 22's resource-exhaustion catalogue is the *failure-mode taxonomy* that the utilisation signal is trying to prevent the system from reaching.

### Resource exhaustion and [[bulkhead]]

The [[bulkhead]] pattern isolates resources so exhaustion in one pool doesn't affect another. Per-dependency thread pools, per-tenant process isolation, and per-service cell deployments are all direct responses to the resource-exhaustion failure modes above.

### Resource exhaustion and [[stream-processing-fault-tolerance]]

Stream processors have their own resource-exhaustion modes — checkpoint state growing unbounded, consumer lag consuming broker disk, state-store compaction backlogs — but the failure mechanics are the same. The lessons transfer directly.

### Resource exhaustion and the Chapter 22 scenario

The nine-step scenario above is worth keeping in mind whenever a production outage starts. The visible symptom (backend health check failures) is almost never the root cause (Java GC parameters). Resource-exhaustion cascades teach that you debug from the *top* of the causal chain, not from the bottom — and often the top is a component whose owner is not in the incident call.

## Related pages

- [[cascading-failure]]
- [[server-overload]]
- [[gc-death-spiral]]
- [[queue-management]]
- [[connection-level-load]]
- [[utilization-signals]]
- [[load-shedding]]
- [[bulkhead]]
- [[deadline-propagation]]
- [[latency-and-deadlines]]
- [[site-reliability-engineering]]
