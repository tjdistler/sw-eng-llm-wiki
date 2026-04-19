# GC Death Spiral

**Summary**: A JVM-specific feedback loop where memory pressure triggers increased garbage collection, GC consumes CPU, the reduced available CPU slows request handling, slower requests means more in-flight requests, more in-flight requests means more RAM used, which triggers more GC — and the cycle accelerates until the task wedges or crashes. SRE Chapter 22 names this specifically as a cascading-failure mechanism, and Chapter 22's suggested response ("restart servers") is specifically motivated by this failure mode: a wedged Java process cannot escape on its own.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

From Chapter 22's memory-exhaustion section (source: chapter-22-addressing-cascading-failures.md):

> Increased rate of garbage collection (GC) in Java, resulting in increased CPU usage
>
> A vicious cycle can occur in this scenario: less CPU is available, resulting in slower requests, resulting in increased RAM usage, resulting in more GC, resulting in even lower availability of CPU. This is known colloquially as the "GC death spiral."

The feedback loop has four links, each feeding the next:

1. **Memory pressure → more GC.** The collector runs more often and more aggressively as the heap fills.
2. **More GC → less CPU for requests.** GC threads consume CPU that would otherwise serve requests. Stop-the-world phases halt request processing entirely.
3. **Less CPU → slower requests.** Requests take longer to complete; more are concurrent at any time.
4. **More concurrent requests → more memory.** Each in-flight request holds request/response objects and backend state in memory.

The output of step 4 is the input of step 1. The cycle is positive feedback, and once established it only accelerates.

## Why Java specifically

The death spiral is named after Java because the JVM makes this failure mode particularly visible, but variants exist in any managed-memory runtime:

- **Go** — the collector is less disruptive (concurrent, low-pause), but high allocation rates still consume CPU and slow the goroutine scheduler.
- **Python, Ruby, JavaScript** — reference-counting plus cyclic GC have their own versions.
- **C++ with garbage-collected allocators** (Boehm GC, some game engines) — same pattern.

The Java pattern is the textbook case because the early 2000s-era HotSpot collectors had long stop-the-world phases that made the spiral visible and catastrophic. Modern collectors (G1, ZGC, Shenandoah) mitigate but don't eliminate the feedback loop.

## Why the spiral can't recover on its own

The cycle is positive feedback, which means small perturbations amplify. Small perturbations could in principle damp out — but in practice the spiral is self-sustaining because:

- **Allocation pressure is driven by the request rate**, which doesn't drop. If the task is still in the load balancer's healthy pool, it keeps receiving requests, which keep allocating.
- **The heap doesn't shrink** meaningfully under sustained allocation. Once full, it stays full.
- **Watchdogs may not fire** because the task is still technically making progress, just very slowly. Health checks on ancillary endpoints may succeed while request-handling is effectively dead.

The result: the task is wedged but not dead. Load balancers may keep sending it work. The only escape is external intervention: restart the task.

## The suggested response: restart

Chapter 22's [[addressing-ongoing-cascading-failure|immediate-steps]] section names GC death spirals specifically as a restart trigger (source: chapter-22-addressing-cascading-failures.md):

> If servers are somehow wedged and not making progress, restarting them may help. Try restarting servers when:
>
> - Java servers are in a GC death spiral
> - Some in-flight requests have no deadlines but are consuming resources, leading them to block threads, for example
> - The servers are deadlocked

The caveat the chapter adds is important: **make sure you identify the source of the cascading failure before you restart your servers**, because restart may amplify the existing cascade if the root cause is cold caches or a traffic pattern the fresh task will hit just as hard.

## Prevention

Chapter 22 doesn't prescribe specific GC tuning, but the nine-step scenario earlier in the chapter opens with "a Java frontend has poorly tuned garbage collection (GC) parameters" as the root-cause step. The practical defences:

- **Tune GC for the workload.** Long-lived vs short-lived object distribution, heap size, collector choice, pause-target parameters. This is specialist work.
- **Cap the heap well below the container limit.** Leave headroom for native memory (stacks, buffers, JIT code) so the container manager doesn't kill the task for exceeding its limit before the GC even has a chance to reclaim.
- **Shed load before the heap fills.** [[utilization-signals|Memory pressure]] as a shedding signal is harder to calibrate than CPU, but both should feed the shedding decision.
- **Enforce RPC deadlines.** Requests that will never complete shouldn't be allowed to hold memory indefinitely. See [[latency-and-deadlines]].
- **Bound request-state size.** Streaming, chunking, or pagination for large payloads.
- **Periodic restarts.** Some services schedule rolling restarts specifically to bound the age of any task's heap.

## Relationship to other wiki concepts

### GC death spiral and [[resource-exhaustion]]

The death spiral is the most cited example of the "resources feed each other" phenomenon from [[resource-exhaustion|Chapter 22's resource dependency section]]. Memory and CPU exhaustion are not independent — they share a runtime layer (the GC) that couples them.

### GC death spiral and [[process-pauses]]

Kleppmann's [[process-pauses|Chapter 8 process-pauses discussion]] treats GC pauses as a source of silent failures in distributed systems: a long pause can cause a lease to expire, a failure detector to fire, or a distributed lock to be handed to another node while the original holder still believes it is healthy. The death spiral is the SRE-side complement — the same mechanism (GC) causing the same pauses, but analysed for its effect on cascading failure rather than on distributed-systems safety.

### GC death spiral and [[load-shedding]]

[[load-shedding]] is the Chapter 21 mechanism designed to prevent the conditions that trigger the spiral: reject work before the heap fills, so the task's resource consumption stays bounded. A task with aggressive shedding won't enter the spiral; a task without shedding reliably will under sustained overload.

### GC death spiral and stateful-stream-processing

Stateful stream processors with large in-memory state stores are particularly vulnerable to GC death spirals because state growth is unbounded — the processor accumulates keys over time, each holding state. Spiking input rate plus a tenured generation full of long-lived state objects is the classic Flink/Kafka Streams death-spiral trigger.

### GC death spiral and restart-as-recovery

The restart-as-recovery response captured in Chapter 22 is an industry-wide operational pattern with no good name. The SRE-book's explicit acknowledgement that "wedged" is a distinct failure mode requiring a distinct response is one of the most useful additions to the fault-tolerance vocabulary — before this naming, wedged processes were often diagnosed as "slow" or "buggy" and debugged individually rather than treated as a named failure class with a known remedy.

## Related pages

- [[cascading-failure]]
- [[resource-exhaustion]]
- [[server-overload]]
- [[process-pauses]]
- [[load-shedding]]
- [[utilization-signals]]
- [[addressing-ongoing-cascading-failure]]
- [[latency-and-deadlines]]
- [[site-reliability-engineering]]
