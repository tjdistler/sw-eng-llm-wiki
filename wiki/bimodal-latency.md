# Bimodal Latency

**Summary**: A failure mode where a small fraction of requests consume far more capacity than their share because they hit the deadline rather than completing quickly — converting a small percentage of unavailable work into a large percentage of failed requests. SRE Chapter 22's canonical example: a frontend of 10 servers × 100 threads (1,000 total), normally at 1,000 QPS × 100ms = 100 threads busy. If 5% of requests hit a 100-second deadline instead of completing, those 50 QPS occupy 5,000 threads' worth of capacity — more than the 1,000 available. Only ~20% of requests can be handled, resulting in **80% error rate** instead of the underlying 5%.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's worked example

Chapter 22 develops the arithmetic carefully (source: chapter-22-addressing-cascading-failures.md):

> Suppose that the frontend from the preceding example consists of 10 servers, each with 100 worker threads. This means that the frontend has a total of 1,000 threads of capacity. During usual operation, the frontends perform 1,000 QPS and requests complete in 100 ms. This means that the frontends usually have 100 worker threads occupied out of the 1,000 configured worker threads (1,000 QPS * 0.1 seconds).
>
> Suppose an event causes 5% of the requests to never complete. This could be the result of the unavailability of some Bigtable row ranges, which renders the requests corresponding to that Bigtable keyspace unservable. As a result, 5% of the requests hit the deadline, while the remaining 95% of the requests take the usual 100 ms. With a 100-second deadline, 5% of requests would consume 5,000 threads (50 QPS * 100 seconds), but the frontend doesn't have that many threads available.

The calculation:

- **Healthy baseline.** 1,000 QPS × 100 ms = 100 threads occupied. Comfortable headroom.
- **Bad state.** 50 QPS × 100s (the deadline) = **5,000** thread-seconds per second of stuck work. That exceeds the 1,000-thread capacity by a factor of 5.
- **Result.** The frontend can handle only 1,000 threads' worth of concurrent work, so only 19.6% of total request work (1,000 / (5,000 + 95)) gets attention. **80.4% error rate**.

The punchline: the underlying failure was 5% of requests being unservable. The observed failure is an 80% error rate. The deadline length is the amplifier.

## Why it's called "bimodal"

The name comes from the shape of the latency distribution. Normal operation produces a single peak around the mean response time (100 ms in the example). The failure mode produces two peaks: one at the mean, and one at the deadline. The distribution is *bimodal* — two modes, not one — and averaging the two produces a mean that looks reasonable but hides the disaster in the tail.

The chapter's first detection guideline names this explicitly (source: chapter-22-addressing-cascading-failures.md):

> Detecting this problem can be very hard. In particular, it may not be clear that bimodal latency is the cause of an outage when you are looking at mean latency. When you see a latency increase, try to look at the distribution of latencies in addition to the averages.

A 95/5 split with one peak at 100ms and one at 100s has a mean somewhere around 5 seconds. Neither peak is at 5 seconds. The mean is a lie.

## The four prescriptions

Chapter 22 lists four responses (source: chapter-22-addressing-cascading-failures.md):

### 1. Look at distributions, not averages

The detection discipline. See [[long-tail-latency]] for the more general case — the Chapter 6 argument that histograms beat means is the precondition for noticing bimodal distributions.

### 2. Return errors early

> This problem can be avoided if the requests that don't complete return with an error early, rather than waiting the full deadline. For example, if a backend is unavailable, it's usually best to immediately return an error for that backend, rather than consuming resources until it the backend available. If your RPC layer supports a fail-fast option, use it.

The failure mode is about stuck requests consuming capacity for the *duration of the deadline*. If unavailable backends return errors immediately instead of hanging, the deadline never gets burned. This is the fail-fast principle applied specifically to the bimodal case.

### 3. Match deadline to mean latency

> Having deadlines several orders of magnitude longer than the mean request latency is usually bad. In the preceding example, a small number of requests initially hit the deadline, but the deadline was three orders of magnitude larger than the normal mean latency, leading to thread exhaustion.

100ms mean × 1,000 = 100s deadline. The ratio is the amplifier. Shrinking the deadline to (say) 1s × 5% = 50 thread-seconds — well within the 1,000-thread budget. The same underlying failure (5% stuck) becomes a 5% error rate instead of 80%.

### 4. Limit in-flight requests by keyspace

> When using shared resources that can be exhausted by some keyspace, consider either limiting in-flight requests by that keyspace or using other kinds of abuse tracking.

If the stuck work is all for one keyspace (one customer, one tenant, one Bigtable range), a per-keyspace concurrency limit prevents it from occupying more than its share of capacity. The chapter's example:

> Suppose your backend processes requests for different clients that have wildly different performance and request characteristics. You might consider only allowing 25% of your threads to be occupied by any one client in order to provide fairness in the face of heavy load by any single client misbehaving.

This is the [[bulkhead]] pattern applied to concurrent-request limits rather than thread pools.

## Relationship to other wiki concepts

### Bimodal latency and [[latency-and-deadlines]]

Bimodal latency is the extreme case that motivates the "short deadline" side of the picking-a-deadline trade-off in [[latency-and-deadlines]]. A deadline orders of magnitude larger than the mean is what makes the amplification severe; a deadline close to the p99.9 keeps the amplification bounded.

### Bimodal latency and [[deadline-propagation]]

Deadline propagation is partly what makes bimodal latency tolerable: when a stuck request's deadline expires upstream, cancellation flows downstream and the expensive stuck work stops. Without propagation, the downstream can keep burning resources even after the upstream has given up.

### Bimodal latency and [[long-tail-latency]]

Chapter 6's [[long-tail-latency]] is the general discipline of measuring tail-focused percentiles instead of means. Bimodal latency is the specific shape that makes tail-focused measurement necessary: the mean is actively misleading. If you only look at mean latency, you miss the pattern entirely; if you look at p99, the two peaks are separated and the failure is visible.

### Bimodal latency and [[tail-latency-amplification]]

Burns's [[tail-latency-amplification]] argument — that a backend's p99 becomes a scatter-gather system's p50 at modest fan-out — is the scatter-gather cousin of bimodal latency. Both are failure modes where the *tail* of the latency distribution, not the mean, dominates the failure behaviour. Both require histogram-level observation to detect and both need fail-fast discipline to mitigate.

### Bimodal latency and [[bulkhead]]

The per-keyspace concurrency limit the chapter suggests is a [[bulkhead]] at the admission-control layer: each tenant gets at most 25% of the capacity so one misbehaving tenant can't starve the others. This is the granularity of bulkhead that matters specifically for bimodal latency — thread-pool bulkheads across dependencies won't help if the stuck work is all the same dependency.

### Bimodal latency and [[hot-spots]]

Kleppmann's [[hot-spots]] discussion covers the partitioning-level cause (some keys are disproportionately popular); bimodal latency is one of the downstream effects when those hot keys are also slow. Preventing hot spots by better partitioning reduces the base rate of stuck requests; bulkheading by keyspace caps the damage when they do occur.

## Related pages

- [[cascading-failure]]
- [[latency-and-deadlines]]
- [[deadline-propagation]]
- [[long-tail-latency]]
- [[tail-latency-amplification]]
- [[response-time-percentiles]]
- [[bulkhead]]
- [[hot-spots]]
- [[site-reliability-engineering]]
