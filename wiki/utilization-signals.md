# Utilization Signals

**Summary**: SRE Chapter 21's per-task overload-protection input: a numeric signal, local to each backend task, that the task uses to decide whether to accept or reject incoming requests. Utilisation is typically CPU-based (current CPU rate divided by reserved CPUs), but the framework accepts any signal a backend needs, and can combine multiple. Google's most generally useful signal is the **executor load average** — a smoothed count of threads that are running or ready to run, compared to processor count. As utilisation approaches configured thresholds the task starts rejecting requests, with higher thresholds for higher [[request-criticality|criticalities]] so that critical traffic survives when sheddable traffic is already being dropped.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## The role

Chapter 21 positions utilisation signals as the input to per-task [[load-shedding]] (source: chapter-21-handling-overload.md):

> Our implementation of task-level overload protection is based on the notion of utilization. In many cases, the utilization is just a measurement of the CPU rate (i.e., the current CPU rate divided by the total CPUs reserved for the task), but in some cases we also factor in measurements such as the portion of the memory reserved that is currently being used. As utilization approaches configured thresholds, we start rejecting requests based on their criticality (higher thresholds for higher criticalities).

A task has three pieces of information it combines into a shed-or-serve decision:

- Its current utilisation (this page).
- The request's [[request-criticality|criticality]].
- Configured per-criticality thresholds (e.g., shed `SHEDDABLE` at 70% utilisation, shed `CRITICAL_PLUS` only at 95%).

When utilisation crosses the threshold for the incoming request's criticality, the task rejects it. This is what makes a task self-defending: even if the [[per-customer-quotas|quota system]] is not yet aware of a new load spike, and even if the [[weighted-round-robin|load balancer]] has over-subscribed this particular task, the task has a local defence.

## The executor load average

Chapter 21's preferred signal (source: chapter-21-handling-overload.md):

> The most generally useful signal is based on the "load" in the process, which is determined using a system we call executor load average. To find the executor load average, we count the number of active threads in the process. In this case, "active" refers to threads that are currently running or ready to run and waiting for a free processor. We smooth this value with exponential decay and begin rejecting requests as the number of active threads grows beyond the number of processors available to the task.

Three design choices worth naming:

- **"Active" means running or ready, not merely existing.** A thread blocked in I/O doesn't count; a thread in `RUNNABLE` state on the scheduler run-queue does.
- **Exponential smoothing.** Raw instantaneous counts are too noisy — a fan-out request that schedules a burst of short-lived operations would cause a spurious spike. The smoothed value filters those out while still tracking sustained load.
- **Comparison is against processor count.** If `smoothed_active_threads > processors_available`, the task is saturated by construction: there's no more CPU for an incoming request to run on. This is the natural threshold.

The name **executor load average** deliberately echoes Unix's `loadavg` — same underlying idea (smoothed count of ready work relative to capacity), applied at the process rather than the OS level. The advantage of reimplementing it per-process: the signal is scoped to the task's own resource allocation, so "1.0 load" means "this task is fully using its allocated CPU," not "this machine is fully using its physical CPU."

### Why smoothing matters

The example Chapter 21 gives (source: chapter-21-handling-overload.md):

> An incoming request that has a very large fan-out (i.e., one that schedules a burst of a very large number of short-lived operations) will cause the load to spike very briefly, but the smoothing will mostly swallow that spike. However, if the operations are not short-lived (i.e., the load increases and remains high for a significant amount of time), the task will start rejecting requests.

The distinction matters because transient bursts are normal and should not trigger shedding — they are what the system is designed to handle. Sustained elevated load is the actual overload signal. Smoothing separates the two.

## Other signals

The executor load average is the default but not the only option (source: chapter-21-handling-overload.md):

> While the executor load average has proven to be a very useful signal, our system can plug in any utilization signal that a particular backend may need. For example, we might use memory pressure — which indicates whether the memory usage in a backend task has grown beyond normal operational parameters — as another possible utilization signal. The system can also be configured to combine multiple signals and reject requests that would surpass the combined (or individual) target utilization thresholds.

Examples of signals a service might compose in:

- **Memory pressure.** For a service with a large working set, memory-used / memory-reserved approaching 1.0 predicts imminent GC pause or OOM.
- **Disk I/O queue depth.** For a service bottlenecked on storage I/O.
- **Downstream-specific signals.** A service whose bottleneck is a downstream quota might expose its downstream-quota consumption as a utilisation signal.

Chapter 21 doesn't prescribe which signals to combine — that is a per-service decision — but the framework supports the pattern.

## The threshold-per-criticality interaction

The key insight that makes utilisation signals work well is that the threshold depends on the request's criticality (source: chapter-21-handling-overload.md, [[request-criticality]]):

> We start rejecting requests based on their criticality (higher thresholds for higher criticalities).

Sketch of the policy:

| Criticality | Reject when utilisation exceeds |
|---|---|
| SHEDDABLE | 70% (indicative numbers, not from chapter) |
| SHEDDABLE_PLUS | 80% |
| CRITICAL | 90% |
| CRITICAL_PLUS | 95% |

The effect: at 75% utilisation, `SHEDDABLE` traffic is being dropped but everything else flows; at 92%, all sheddable traffic is dropped and `CRITICAL` is starting to be dropped but `CRITICAL_PLUS` is still fully served. The task degrades gracefully across four bands rather than a single cliff.

The actual Google numbers aren't in the chapter; the shape is.

## Relationship to existing wiki concepts

### Utilisation signals and [[weighted-round-robin]]

Both Chapter 20's Weighted Round Robin and Chapter 21's utilisation signals use the same underlying measurement (typically CPU utilisation) for different decisions:

- **Weighted Round Robin (client-side).** Backend reports utilisation in every response; clients weight routing so all backends converge to similar utilisation.
- **Utilisation signals (server-side).** Backend measures its own utilisation; rejects requests based on a per-criticality threshold.

They are complementary: Weighted Round Robin tries to keep utilisation even across the fleet, and utilisation signals ensure that even if Weighted Round Robin over-shoots on one task (or the task is unusually slow), that task can protect itself. The same measurement drives both; the policies are independent.

### Utilisation signals and [[four-golden-signals]]

**Saturation** is one of the four golden signals from Chapter 6. Chapter 21's utilisation signal is saturation operationalised: a numeric measure of "how full is the service right now" used not just for monitoring but for active request-admission control. Saturation monitoring alerts humans; utilisation signals drive automated per-request shedding. The two live on top of the same measurement.

### Utilisation signals and executor-load-average

The executor load average is specifically Google's preferred implementation of the general "how loaded is this process" idea. It is to a process what Unix's `loadavg` is to a machine: a smoothed count of ready-to-run threads relative to CPU capacity. The design lesson travels: if you need a process-local saturation signal, count ready threads and smooth.

### Utilisation signals and [[operational-overload]]

[[operational-overload]] is Chapter 11's concept of an on-call rotation being given more work than it can sustain. Chapter 21's utilisation signals are the software analogue: a task that cannot process as many requests as it is receiving needs a way to recognise and respond to the condition. The response in both cases is to shed lower-priority work and preserve capacity for the most important tasks.

### Utilisation signals and [[circuit-breaker]]

A [[circuit-breaker]] protects a *caller* from a failing callee; utilisation signals protect a *callee* from being overwhelmed. Both feed off a local observation and cause requests to fail fast, but the roles are different. Chapter 21's overall design is a composition: clients use [[adaptive-throttling]] (caller-side), backends use utilisation-driven shedding (callee-side), and the pairing catches cases neither can handle alone.

## Related pages

- [[handling-overload]]
- [[load-shedding]]
- [[request-criticality]]
- [[weighted-round-robin]]
- [[adaptive-throttling]]
- [[four-golden-signals]]
- [[operational-overload]]
- [[circuit-breaker]]
- [[site-reliability-engineering]]
