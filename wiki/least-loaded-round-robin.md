# Least-Loaded Round Robin

**Summary**: The middle rung of SRE Chapter 20's [[load-balancing-policies|policy ladder]]: each client tracks the number of active requests per backend and round-robins among backends tied for the minimum. The intuition is sound — loaded tasks have higher latency, so active-request count is a proxy for load — but the policy has a dangerous failure mode called **sinkholing traffic**, where a backend serving fast errors appears to have a light load and attracts *more* traffic. Fixing this requires counting recent errors as though they were active requests. Even with the fix, Least-Loaded leaves about a 2x spread in large services because active-request count is a poor proxy for capability and each client sees only its own view.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The policy

For each new request (source: chapter-20-load-balancing-in-the-datacenter.md):

1. Filter the [[subsetting|subset]] down to backends with the *minimum* active-request count.
2. Round-robin among that filtered set.

Chapter 20's worked example: a client's subset is `t0..t9`; current active-request counts are some mix; the minimum is 0 and the tied set is `{t2, t3, t5, t7, t8}`; the client picks one of those via round-robin. After four more requests (still assuming none complete), the tied set shrinks; if a request against `t4` completes, its count drops back to 0 and it re-enters the tied set.

The Round Robin part matters: without the round-robin among tied backends, the policy might not spread requests well enough to exercise all available capacity — it might keep picking the same "least-loaded" backend repeatedly.

## Sinkholing traffic: the dangerous pitfall

Chapter 20's own phrasing: *"if a task is seriously unhealthy, it might start serving 100% errors. Depending on the nature of those errors, they may have very low latency; it's frequently significantly faster to just return an 'I'm unhealthy!' error than to actually process a request"* (source: chapter-20-load-balancing-in-the-datacenter.md).

The cascade:

1. The unhealthy backend serves fast errors.
2. Its active-request count stays very low.
3. The Least-Loaded filter preferentially picks it.
4. *More* traffic flows to the broken backend, compounding the damage.

The chapter names this behaviour **sinkholing**: the bad backend acts like a sinkhole, sucking traffic in.

### The fix: count errors as active requests

*"Modify the policy to count recent errors as if they were active requests"* (source: chapter-20-load-balancing-in-the-datacenter.md). An error-flooding backend now looks *more* loaded, not less, and the policy routes around it. The fix is cheap — errors are already observed by the client — and standard in Google's implementation.

This is the classic lesson that **any load signal you use for routing will be gamed by failure modes that produce that signal without load**. The mitigation is to treat the proxy signal as a composite: active requests plus recent errors plus, eventually, backend-reported utilisation ([[weighted-round-robin]]).

## Residual limitations

Even with the error-counting fix, Least-Loaded has two structural weaknesses (source: chapter-20-load-balancing-in-the-datacenter.md):

### Active-request count is a poor proxy for capability

Many requests spend most of their life waiting on downstream I/O (other backends, databases, caches), not consuming CPU. A backend with a CPU twice as fast as its peers can process twice as many requests, but the *latency* of those requests is dominated by the network wait, so the fast backend's active-request count per unit time looks similar to the slow one's. Least-Loaded treats them as equally loaded and sends them equal traffic — under-utilising the fast backend.

This is a subtle but serious problem in a heterogeneous fleet. A policy that actually measured backend capability (e.g. CPU utilisation) could give the fast backend more traffic; active-request count can't.

### Each client sees only its own view

A client's active-request count includes only *its own* outstanding requests to the backend, not anyone else's. So a backend heavily loaded by other clients looks "idle" to a client that isn't sending much to it, and the client happily sends more. With many clients doing this independently, backends can still be wildly uneven.

Chapter 20's bottom line: *"large services using Least-Loaded Round Robin will see their most loaded backend task using twice as much CPU as the least loaded, performing about as poorly as Round Robin"* (source: chapter-20-load-balancing-in-the-datacenter.md).

Both limitations are what [[weighted-round-robin]] fixes: its capability score comes from the *backend itself* via utilisation reports, so it reflects *actual* backend capability and *total* backend load, not what any one client sees.

## When it's still an improvement

Least-Loaded outperforms [[simple-round-robin]] in two regimes:

- **Backends with very different latencies.** A slow backend accumulates active requests faster than a fast one, so its tied-set membership drops away and the policy avoids it. This is the simplest case Least-Loaded was designed for.
- **Detecting soft degradation.** Even without backend-reported utilisation, a backend that starts handling requests 2x slower will quickly accumulate twice the active requests and be de-prioritised.

Chapter 20 does not dismiss Least-Loaded; it places it as a useful step up from Simple. The move from Least-Loaded to Weighted is the final lift.

## Relationship to existing wiki concepts

### Least-Loaded and the three backend states

The [[backend-task-states|three explicit states]] catch backends that are clearly down (refusing connections) or intentionally draining ([[lame-duck-state|lame duck]]). The sinkholing problem lives in a gap: a backend that is *up, listening, and answering*, but answering wrong. The explicit states don't catch it; the error-count fix is what does.

### Least-Loaded and circuit breakers

[[circuit-breaker|Circuit breakers]] (Newman / Nygard) react to error rates by short-circuiting calls to a dependency. Least-Loaded with error counting is essentially a soft circuit breaker: errors make the backend look more loaded, so less traffic goes to it, so the blast radius shrinks without the binary open/closed decision. Both techniques are adapting to error signals; the mechanism differs.

### Least-Loaded and the power-of-two-choices

Academic-literature alternative: rather than picking the globally-least-loaded backend, pick two at random and choose the less loaded of the two. The P2C variant is simpler to implement in distributed settings because it avoids the tie-set filtering step and has known convergence properties. Chapter 20 doesn't cite P2C by name, but the engineering rationale for Least-Loaded in the chapter (cheap local state, responds to latency) applies equally.

### Least-Loaded and Weighted: the step up

The Chapter 20 progression is explicit: Least-Loaded's residual problems (proxy mismatch, partial view) are solved by *asking the backend how loaded it is*. Weighted Round Robin is the policy that actually does that, and Figure 20-6's before/after CPU distribution is Chapter 20's most convincing quantitative argument.

## Related pages

- [[load-balancing-policies]]
- [[simple-round-robin]]
- [[weighted-round-robin]]
- [[datacenter-load-balancing]]
- [[backend-task-states]]
- [[circuit-breaker]]
- [[subsetting]]
- [[site-reliability-engineering]]
