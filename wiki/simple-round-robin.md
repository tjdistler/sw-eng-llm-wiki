# Simple Round Robin

**Summary**: The baseline [[load-balancing-policies|load-balancing policy]] from SRE Chapter 20: each client sends requests in round-robin order to each healthy, non-[[lame-duck-state|lame-duck]] backend in its [[subsetting|subset]]. Dead simple, significantly better than random, and Google's most common policy for years. But in practice it produces **up to 2x spread in CPU consumption** between the least- and most-loaded tasks because of four compounding factors: small subsetting, varying query cost, machine diversity, and unpredictable performance factors like antagonistic neighbours and task restarts. The rest of the Chapter 20 policy ladder ([[least-loaded-round-robin|Least-Loaded]] and [[weighted-round-robin|Weighted]]) exists to address these.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The policy

The algorithm is one sentence long: rotate through the client's subset, skipping anything not currently healthy, sending each new request to the next backend in the rotation (source: chapter-20-load-balancing-in-the-datacenter.md).

Properties:

- **No backend information.** The client doesn't track per-backend load or latency.
- **No coordination between clients.** Each client rotates independently.
- **Deterministic within a client.** Given the same start and the same healthy set, the output is identical.

Chapter 20's honest framing: *"For many years, this was our most common approach, and it's still used by many services"* (source: chapter-20-load-balancing-in-the-datacenter.md).

## Why it's not enough: the four failure modes

Chapter 20 attributes the 2x CPU spread to four compounding causes (source: chapter-20-load-balancing-in-the-datacenter.md).

### 1. Small subsetting

All clients don't issue requests at the same rate. Different processes sharing the same backend service have different request patterns. If client A sends twice as much traffic as client B, the backends in A's subset are twice as loaded as the backends only in B's subset — even with perfect round-robin within each client. Small [[subsetting|subsets]] make this worse because each client's traffic is concentrated in a smaller backend slice.

### 2. Varying query costs

Many Google services have request cost that varies by **1000x or more** between the cheapest and most expensive request. A query like *"return all emails received by user XYZ in the last day"* is cheap for a user with little email and catastrophic for a power user. Round Robin distributes requests uniformly, but *cost* distributes very non-uniformly.

Chapter 20's example: one Java backend averages 15 ms of CPU per query, but a single outlier query can take up to 10 seconds. Even with multiple reserved CPU cores to parallelise work, a backend hit by one of these spikes runs at elevated load for seconds, and latency for other requests on that backend rises due to resource competition.

The partial fix Chapter 20 discusses is *capping the work per request* — introducing pagination so *"return the most recent 100 emails"* becomes the unit, not the full day. But this requires changing the service interface and its consistency story (a pagination walk can miss or repeat messages when the underlying data changes), which is often impractical. Many services thus live with the 100-to-10,000x cost variance and accept the imbalance it causes.

### 3. Machine diversity

Datacenters are not homogeneous; machines have CPUs of different performance. The same request takes different CPU time on different machines. Dealing with this *without* requiring strict fleet homogeneity was a multi-year challenge at Google (source: chapter-20-load-balancing-in-the-datacenter.md).

The solution outline: scale CPU reservations by machine type so that 2 CPU units on a "slow" machine is equivalent to 0.8 CPU units on a "fast" one; the scheduler adjusts reservations based on the machine it schedules the process on. Google introduced the **GCU (Google Compute Unit)** as a virtual CPU-rate unit that abstracts the mapping from physical CPU architectures to a normalised scale.

GCU makes the scheduler's accounting correct; it does not make Simple Round Robin correct. Even with matched reservations, the same request still takes more wall-clock CPU time on the slower machine, so a round-robin client sending the same request rate to a slow and a fast machine will load them unequally.

### 4. Unpredictable performance factors

The largest failure mode, per Chapter 20, and the one that cannot be addressed by any static policy.

**Antagonistic neighbours.** Other processes sharing a machine — often unrelated, run by different teams — can degrade your process's performance by **up to 20%**, mostly through competition for shared resources (memory caches, network bandwidth). The effect compounds: a backend whose outgoing network latency rises because of neighbour competition accumulates more active requests, which triggers more garbage collection, which makes it slower still.

**Task restarts.** A freshly restarted task needs more resources for a few minutes — dynamic optimisation on JVM, cold caches, JIT warm-up. Chapter 20 mentions Google specifically added prewarming logic: tasks stay in [[lame-duck-state|lame duck]] for a period after start so they can trigger their optimisations against internal traffic before being considered healthy. Across many servers updated every day, the fraction of the fleet in the post-restart warm-up regime is non-trivial.

Simple Round Robin sends the warming-up backend just as many requests as a steady-state backend, which degrades the warmer further and may cascade — the opposite of what the ideal policy would do.

## The takeaway

The 2x spread is not a subtle statistical artefact; it's a direct consequence of these four structural factors. A policy that does not *observe* backend state cannot adapt to any of them. Chapter 20's progression adds exactly that observation — first active-request count ([[least-loaded-round-robin]]), then backend-reported utilisation ([[weighted-round-robin]]) — and the spread shrinks accordingly.

## Why it's still widely used

Simple Round Robin is *appropriate* when (the chapter doesn't list these explicitly but they follow from its analysis):

- Query cost variance is narrow.
- The machine fleet is homogeneous.
- The service is not CPU-bound, so small imbalances don't matter.
- The operational cost of implementing something more complex is not justified.

Many Google services continue to use it for exactly these reasons. The lesson is not "never use Simple Round Robin"; the lesson is "know what it costs you and choose deliberately."

## Relationship to existing wiki concepts

### Simple Round Robin and Burns's default

Burns's [[replicated-load-balanced-service]] mentions round-robin as the default load-balancer behaviour. Chapter 20's assessment is what happens when that default is put under real-world pressure.

### Simple Round Robin and GCU

The Google Compute Unit (GCU) is mentioned only in this subsection of Chapter 20 and a few other places in the SRE book. It is an infrastructure detail: a virtual CPU-rate unit used for capacity accounting across heterogeneous machines. See [[capacity-planning]] and [[intent-based-capacity-planning]] for where GCU lives in the broader plan.

### Simple Round Robin and queueing-theory-style policies

There is a large academic literature on richer policies (join-the-shortest-queue, power-of-two-choices, least-response-time). Chapter 20 does not engage with it directly; its pragmatic stance is that active-request count plus backend-reported utilisation captures most of the benefit at a fraction of the implementation cost.

## Related pages

- [[load-balancing-policies]]
- [[least-loaded-round-robin]]
- [[weighted-round-robin]]
- [[datacenter-load-balancing]]
- [[subsetting]]
- [[lame-duck-state]]
- [[replicated-load-balanced-service]]
- [[capacity-planning]]
- [[site-reliability-engineering]]
