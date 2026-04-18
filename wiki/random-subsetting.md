# Random Subsetting

**Summary**: SRE Chapter 20's *rejected* [[subsetting]] algorithm: each client shuffles the backend list once and picks the first *subset_size* entries. It handles restarts and failures robustly (the shuffle is stable per client) but spreads connection load very unevenly — with a 30% subset, the least-loaded backend sees 63% of the average load and the most-loaded sees 121%; smaller subsets are worse. The chapter concludes that random subsetting needs subsets of ≥75% of the fleet to balance decently, which defeats the point of subsetting at all. Google uses [[deterministic-subsetting]] instead.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The naive algorithm

Random subsetting is exactly what it sounds like (source: chapter-20-load-balancing-in-the-datacenter.md):

1. Each client takes the global list of backends.
2. Shuffles it (client-specific seed, so each client gets a different permutation).
3. Picks the first *subset_size* resolvable/healthy entries.

The shuffle is done *once*, at client start, and the resulting subset is stable for the life of the client. This gives desirable behaviour on failure: when a backend disappears, the client replaces it from the remainder of its shuffled list, which minimises the churn in its subset.

So far so good on the resilience requirements. The problem is distribution.

## Why it distributes load badly

The expected number of clients that include a given backend in their subset is `clients × (subset_size / total_backends)`. That's the mean; the variance is large. Chapter 20 walks through two concrete simulations (source: chapter-20-load-balancing-in-the-datacenter.md):

### 300 clients, 300 backends, 30% subset (90 backends per client)

- Expected connections per backend: **90** (mean)
- Least-loaded backend observed: **57** (63% of mean)
- Most-loaded backend observed: **109** (121% of mean)

Figure 20-3 shows the distribution for this case.

### 300 clients, 300 backends, 10% subset (30 backends per client)

- Expected connections per backend: **30** (mean)
- Least-loaded backend observed: **15** (50% of mean)
- Most-loaded backend observed: **45** (150% of mean)

Figure 20-4 shows this worse case.

The pattern gets *worse* as subset size shrinks — exactly the regime where subsetting is most useful. And 30% is already a larger subset than most deployments would actually want.

## What this means for capacity

Load non-uniformity translates directly into overprovisioning. If the most-loaded backend runs at 121% of average, then to prevent it hitting its ceiling the whole fleet has to be overprovisioned by 21% — the 21% above the average is reserved but unused (source: chapter-20-load-balancing-in-the-datacenter.md's [[datacenter-load-balancing|ideal-case]] framing). The 150% worst-case in the 10% simulation means 50% overprovisioning.

At Google's cost structure this is unacceptable, and Chapter 20 concludes plainly: "for random subsetting to spread the load relatively evenly across all available tasks, we would need subset sizes as large as 75%. A subset that large is simply impractical; the variance in the number of clients connecting to a task is just too large to consider random subsetting a good subset selection policy at scale" (source: chapter-20-load-balancing-in-the-datacenter.md).

## The underlying statistics

The variance comes from each client independently choosing backends without coordination with other clients. On any given draw, a backend has probability `p = subset_size / total_backends` of being chosen by a client; across `C` clients the connection count is binomial with mean `Cp` and variance `Cp(1-p)`. For the 300 × 300 × 30% case this gives a standard deviation of about 8 on a mean of 90, which is consistent with the simulation's 63%–121% spread when extreme values are sampled across 300 backends.

The fundamental fix is to have clients *coordinate* their choices so that the aggregate covers the backends uniformly. That is exactly what [[deterministic-subsetting]] does.

## Why it still gets airtime

Even though Google rejects random subsetting, it's worth understanding for two reasons:

1. **It is what most systems do by default.** Libraries that offer "pick N backends from a pool" typically do it randomly. Understanding the failure mode is necessary to recognise when the library's default is not good enough.
2. **The desirable properties of deterministic subsetting are defined in contrast to random.** Chapter 20's requirements list (uniform load, low churn, graceful resizes) is a checklist of what random does well and what it does badly.

## Relationship to existing wiki concepts

### Random subsetting vs consistent hashing

[[consistent-hashing]] also provides low churn on fleet changes. If clients each *hashed* their IDs to positions on a ring and picked the next `subset_size` backends going clockwise, the per-client subset would be stable and the aggregate would be uniform modulo the usual consistent-hashing variance. This is closer to [[deterministic-subsetting]] in spirit than to random subsetting, and it is what several non-Google systems use (Finagle's P2C-with-deterministic-aperture variant, for example). Chapter 20 doesn't cite consistent hashing in the subsetting context, but the CDN-side discussion in [[network-load-balancer|Ch 19]] is structurally the same mechanism applied to packets instead of connections.

### Random subsetting and the three requirements

Using Chapter 20's checklist:

- **Uniform load:** random subsetting *fails*.
- **Low churn on failure:** random subsetting *passes*, because the shuffle is stable.
- **Graceful resizes:** random subsetting mostly passes — the shuffle is independent of fleet size, so growing or shrinking the backend list doesn't invalidate existing subsets. But the non-uniform distribution baseline makes this less valuable in practice.

The deterministic alternative's contribution is passing all three simultaneously.

## Related pages

- [[subsetting]]
- [[deterministic-subsetting]]
- [[datacenter-load-balancing]]
- [[consistent-hashing]]
- [[site-reliability-engineering]]
