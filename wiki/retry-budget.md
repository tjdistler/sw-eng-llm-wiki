# Retry Budget

**Summary**: SRE Chapter 21's two-layer cap on request retries, designed to prevent retries from amplifying a transient overload into a sustained one. **Per-request budget**: at most three attempts, then propagate the failure. **Per-client budget**: the ratio of retries to original requests over a recent window is capped at 10%. A third refinement carries a retry counter in the request metadata; the backend inspects recent-history histograms of these counters and, if it sees many already-retried requests, returns **"overloaded; don't retry"** so that further retry attempts stop at the current layer rather than propagating. And the governing rule: **retries happen only at the layer immediately above the one rejecting**, otherwise a stack of N layers produces 3^N retries.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The problem retries cause

Chapter 21's framing (source: chapter-21-handling-overload.md):

> In the case of overload errors, we distinguish between two possible situations.
>
> **A large subset of backend tasks in the datacenter are overloaded.** If the cross-datacenter load balancing system is working perfectly (i.e., it can propagate state and react instantaneously to shifts in traffic), this condition will not occur.
>
> **A small subset of backend tasks in the datacenter are overloaded.** This situation is typically caused by imperfections in the load balancing inside the datacenter. For example, a task may have very recently received a very expensive request. In this case, it is very likely that the datacenter has remaining capacity in other tasks to handle the request.

Retries help in the second case — retry usually lands on a different backend with spare capacity — but make the first case catastrophic, because the datacenter is already overloaded and retrying multiplies the load. The retry budget is the cap that keeps the helpful case viable without triggering the catastrophic one.

## Per-request budget: three attempts

Chapter 21's first mechanism (source: chapter-21-handling-overload.md):

> First, we implement a per-request retry budget of up to three attempts. If a request has already failed three times, we let the failure bubble up to the caller. The rationale is that if a request has already landed on overloaded tasks three times, it's relatively unlikely that attempting it again will help because the whole datacenter is likely overloaded.

The reasoning is probabilistic: if backend tasks are randomly over-subscribed, the probability of landing on *three* overloaded tasks in a row is a strong signal that overload is widespread rather than a one-task accident. Past three, further retries don't help and only add load.

## Per-client budget: 10% retry ratio

The second mechanism (source: chapter-21-handling-overload.md):

> Secondly, we implement a per-client retry budget. Each client keeps track of the ratio of requests that correspond to retries. A request will only be retried as long as this ratio is below 10%. The rationale is that if only a small subset of tasks are overloaded, there will be relatively little need to retry.

The math Chapter 21 works through:

> As a concrete example (of the worst-case scenario), let's assume a datacenter is accepting a small amount of requests and rejecting a large portion of requests. Let X be the total rate of requests attempted against the datacenter according to the client-side logic. Due to the number of retries that will occur, the number of requests will grow significantly, to somewhere just below 3X.

Without the per-client budget, the three-attempt per-request budget means each rejected request is attempted up to three times, so datacenter traffic can grow up to 3x. For a datacenter already struggling, a 3x amplification is catastrophic.

Layering the per-client 10% retry budget on top:

> However, layering on the per-client retry budget (a 10% retry ratio) reduces the growth to just 1.1x in the general case — a significant improvement.

The per-client budget is the dominant constraint under realistic conditions. Three-attempts is the per-event cap; 10% is the aggregate cap.

## The retry-counter histogram and "overloaded; don't retry"

The third mechanism is subtler and more interesting (source: chapter-21-handling-overload.md):

> A third approach has clients include a counter of how many times the request has already been tried in the request metadata. For instance, the counter starts at 0 in the first attempt and is incremented on every retry until it reaches 2, at which point the per-request budget causes it to stop being retried. Backends keep histograms of these values in recent history. When a backend needs to reject a request, it consults these histograms to determine the likelihood that other backend tasks are also overloaded. If these histograms reveal a significant amount of retries (indicating that other backend tasks are likely also overloaded), they return an "overloaded; don't retry" error response instead of the standard "task overloaded" error that triggers retries.

The mechanism:

1. Every request carries a `retry-count` field in its metadata. 0 = first attempt, 1 = first retry, 2 = second retry.
2. Each backend observes the distribution of `retry-count` in its recent traffic. A healthy datacenter should see mostly zeros.
3. When the backend has to reject, it looks at the recent histogram. If it is rejecting a lot of `retry-count` > 0 requests, other backends are also rejecting — the overload is widespread.
4. In that case, the backend returns **"overloaded; don't retry"** instead of the standard "task overloaded" response.
5. The client sees the stronger signal and stops retrying immediately.

This is the backend telling the client "the problem is bigger than me; escalating won't help." Without it, the client has only its own per-request and per-client budgets to work with — both of which allow *some* retries, which is dangerous when the whole datacenter is overloaded.

## The combinatorial-retry-explosion rule

Chapter 21 states the retry-stack rule explicitly (source: chapter-21-handling-overload.md):

> Our larger services tend to be deep stacks of systems, which may in turn have dependencies on each other. In this architecture, **requests should only be retried at the layer immediately above the layer that is rejecting them**. When we decide that a given request can't be served and shouldn't be retried, we use an "overloaded; don't retry" error and thus avoid a combinatorial retry explosion.

The worked example in the chapter: Frontend → Backend A → Backend B → DB Frontend. If DB Frontend is overloaded:

- Backend B retries up to three times.
- When Backend B gives up, it returns "overloaded; don't retry" to Backend A.
- Backend A *does not retry* on top of Backend B's retries — it either degrades (produces a partial response using what it has) or propagates "overloaded; don't retry" to Frontend.

If every layer retried, each layer's three attempts multiplied by the layers below would produce 3^N amplification — a stack of 4 layers would turn one rejection into 81 attempts at the bottom. The "retry only at the immediately-above layer" rule is what keeps deep stacks tractable.

## Retries and load balancing

Chapter 21 makes an interesting observation about retries and load balancing (source: chapter-21-handling-overload.md):

> From the point of view of our load balancing policies, retries of requests are indistinguishable from new requests. That is, we don't use any explicit logic to ensure that a retry actually goes to a different backend task; we just rely on the likely probability that the retry will land on a different backend task simply by virtue of the number of participating backends in the subset. Ensuring that all retries actually go to a different task would incur more complexity in our APIs than is worthwhile.
>
> Even if a backend is only slightly overloaded, a client request is often better served if the backend rejects retry and new requests equally and quickly. These requests can then be retried immediately on a different backend task that may have spare resources. The consequence of treating retries and new requests identically at the backend is that retrying requests in different tasks becomes a form of organic load balancing: it redirects load to tasks that may be better suited for those requests.

The retry is itself a form of load balancing, probabilistically moving work off overloaded tasks onto peers. This only works because of the subsetting and policy work described in [[datacenter-load-balancing|Chapter 20]] — enough backends in a subset that "a different task" is the likely outcome of a retry.

## Relationship to existing wiki concepts

### Retry budget and [[circuit-breaker]]

A classical [[circuit-breaker]] caps retries to a failing downstream by opening the breaker; once open, no retries pass through until the probe succeeds. The retry budget here is a more graduated approach: retries are allowed but bounded, and the "overloaded; don't retry" signal is the backend's version of asking the caller to treat the breaker as open for this specific request.

The Chapter 21 machinery is what a finely-tuned retry discipline looks like when built into the RPC framework. Circuit breakers are the coarse-grained alternative in environments where fine-grained per-request metadata isn't available.

### Retry budget and [[adaptive-throttling]]

Both mechanisms cap retry amplification but at different points:

- **Adaptive throttling** stops the client from *sending* requests when it observes high rejection.
- **Retry budget** stops the client from *retrying* when it observes high retry ratio.

They compose: adaptive throttling bounds first-attempts, retry budget bounds retries on top of first-attempts. Without both, either first-attempts or retries could individually flood the backend.

### Retry budget and [[fault-tolerance]]

Naïve retry-on-failure is the classic "helpful idea that makes incidents worse" in distributed systems. Every practitioner discovers this eventually; Chapter 21 is the fully worked-out fix. The general pattern — **observe success/failure rates, cap retries against them, propagate "don't retry" signals upstream** — is applicable to any retry-capable system.

### Retry budget and [[request-criticality]]

Chapter 21 doesn't explicitly tie retries to criticality, but the two compose naturally: `SHEDDABLE` traffic should arguably have a smaller retry budget than `CRITICAL_PLUS`, since retrying sheddable-class traffic is exactly the amplification the criticality label is trying to prevent.

### Retry budget as cascade defence (Chapter 22)

Chapter 22's [[retry-amplification]] section develops the failure mode that the retry budget is specifically designed to prevent: a backend rejecting a small overload, clients retrying the rejections, retries adding to load, load growing geometrically, service collapsing. The chapter's seven-point retry-guidelines list is the general form; Chapter 21's retry budget is the Stubby-framework realisation (source: chapter-22-addressing-cascading-failures.md). The budget's three-attempt cap implements "limit retries per request"; the 10% per-client ratio implements "consider having a server-wide retry budget"; the "overloaded; don't retry" response implements "return a specific status when overloaded so that clients and other layers back off."

The combinatorial-retry rule — "requests should only be retried at the layer immediately above the layer that is rejecting them" — is a Chapter 22 principle that the retry budget's architectural design already assumes. Retries are framework-level (the RPC client, not the application), and the framework propagates the "don't retry" signal upward rather than retrying at every layer.

### Retry budget and [[idempotence]]

Retries are only safe for [[idempotence|idempotent]] operations. Chapter 21 treats the retry budget as a given and doesn't discuss the idempotence precondition, but it is implicit: the RPC framework retries requests the application has marked retryable, and the application takes responsibility for the requests being safe to retry. The retry budget caps *allowed* retries, not *correct* retries — both are required.

## Related pages

- [[handling-overload]]
- [[adaptive-throttling]]
- [[load-shedding]]
- [[request-criticality]]
- [[circuit-breaker]]
- [[fault-tolerance]]
- [[idempotence]]
- [[datacenter-load-balancing]]
- [[retry-amplification]]
- [[cascading-failure]]
- [[site-reliability-engineering]]
