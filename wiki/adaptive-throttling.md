# Adaptive Throttling

**Summary**: SRE Chapter 21's client-side throttling mechanism. Each client task tracks, over the last two minutes, the number of requests it attempted (**requests**) and the number the backend accepted (**accepts**). When requests exceed `K × accepts`, new requests are rejected locally with probability `max(0, (requests − K × accepts) / (requests + 1))`. Typical `K = 2`. The policy is entirely local to each client — no coordination, no extra latency — and caps the waste of backend resources on rejecting out-of-quota traffic. In the worst case the backend still rejects roughly one request for every request it serves, which is deliberate: the throttle errs on the side of more information rather than tightest-possible regulation.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## The problem

[[per-customer-quotas]] let a backend reject traffic from customers that are over their budget. But rejecting a request is not free:

- For a service that does simple RAM lookups, rejection can cost nearly as much as serving.
- Even for expensive services, if rejected requests are a large fraction of the total, the aggregate cost of rejecting saturates the backend's CPU (source: chapter-21-handling-overload.md):
  > In such cases, the backend can become overloaded even though the vast majority of its CPU is spent just rejecting requests!

Client-side throttling is Chapter 21's fix: detect when a large fraction of requests are being rejected and stop sending them in the first place.

## The formula

Each client task keeps a rolling two-minute window of two counters (source: chapter-21-handling-overload.md):

- **requests** — the number of requests *attempted by the application layer* (counted before the throttle, including requests the throttle itself later rejects).
- **accepts** — the number of requests the backend accepted (i.e., did not reject with an out-of-quota error).

Under normal operation, `requests == accepts`. As the backend starts rejecting, `accepts < requests`.

The client begins self-regulating once `requests > K × accepts`. Once self-regulating, each new request is dropped locally with probability:

```
P(reject) = max(0, (requests − K × accepts) / (requests + 1))
```

(Equation 21-1 in the chapter.)

`K = 2` is the default. The client is tolerant of up to double the rejection rate before starting to drop; once past that threshold, the drop probability grows linearly with the excess.

## Why rejected-locally requests still count in `requests`

A counter-intuitive but deliberate design choice (source: chapter-21-handling-overload.md):

> As the client itself starts rejecting requests, requests will continue to exceed accepts. While it may seem counterintuitive, given that locally rejected requests aren't actually propagated to the backend, this is the preferred behavior.

The reason: if `requests` only counted what was sent, then as soon as the client started self-throttling `requests` would fall toward `accepts` and the throttle would relax, causing oscillation. By counting everything the application *tried to send*, the throttle's signal reflects actual demand and remains stable under load.

## Tuning K

Chapter 21 gives the tuning rule explicitly (source: chapter-21-handling-overload.md):

- **Reducing K** (e.g., to 1.1) makes adaptive throttling more aggressive — fewer requests reach the backend to be rejected. Concrete effect: one rejection per ten accepts instead of one per accept.
- **Increasing K** makes it less aggressive.
- **The default is K = 2.**

The trade-off is between backend CPU wasted on rejections (lower K is better) and speed of state propagation back to clients (higher K is better, because more rejected requests means clients see changes faster). Chapter 21's reasoning for the default:

> By allowing more requests to reach the backend than are expected to actually be allowed, we waste more resources at the backend, but we also speed up the propagation of state from the backend to the clients. For example, if the backend decides to stop rejecting traffic from the client tasks, the delay until all client tasks have detected this change in state is shorter.

So K = 2 is a deliberate choice to trade some rejection CPU for faster recovery when conditions improve. For services where rejection is expensive, the chapter suggests K = 1.1 or similar.

## Worst-case behaviour

The chapter states the worst-case property:

> Even in large overload situations, backends end up rejecting one request for each request they actually process.

With K = 2, the steady state under heavy overload is that the backend sees roughly 2x the traffic it accepts — one rejection per success. This is by design: it keeps the `accepts` signal fresh enough for the throttle to track changing conditions, and caps the backend's wasted work at 50% regardless of how hard the application is trying to send.

## When it doesn't work

Chapter 21 flags one pathology (source: chapter-21-handling-overload.md):

> Client-side throttling may not work well with clients that only very sporadically send requests to their backends. In this case, the view that each client has of the state of the backend is reduced drastically, and approaches to increment this visibility tend to be expensive.

A client that makes one request per minute has a two-minute window with ~2 samples — not enough signal to discriminate "accepting normally" from "rejecting all of mine specifically." The throttle either never triggers (small sample size, no learned reject rate) or triggers inappropriately. This is the client-side analogue of the hot-key problem in statistics: the mechanism needs enough data to produce a reliable estimate, and low-rate clients don't generate enough.

Low-rate clients need a different mechanism — typically a central coordination service (the chapter cites Doorman as an open-source example in its footnote).

## Interaction with [[request-criticality]]

Chapter 21 mentions that the throttling system keeps **separate stats per criticality**. The rationale: `SHEDDABLE` traffic might be rejected at a high rate while `CRITICAL_PLUS` is all accepted; averaging the two would either fail to throttle sheddable traffic (because critical is still flowing) or over-throttle critical traffic (because sheddable is failing). Per-criticality counters give each class its own adaptive budget.

## Relationship to existing wiki concepts

### Adaptive throttling and [[circuit-breaker]]

The classical [[circuit-breaker]] is a binary state machine: closed → open → half-open → closed. Adaptive throttling is the *probabilistic* analogue of the same idea:

- **Binary breaker.** All calls rejected while open, one probe call at half-open, back to closed after a probe success.
- **Adaptive throttle.** Fraction of calls rejected grows with the observed rejection rate; the fraction decays automatically when acceptance returns.

Both are client-side policies that cap waste on a failing backend; adaptive throttling is more graceful (no sharp transitions) but relies on a steady request stream to stay calibrated. Newman's circuit breakers and Cuervo's adaptive throttling are different tools for the same job, with different trade-offs between responsiveness and smoothness.

### Adaptive throttling and [[rate-limiting]]

[[rate-limiting]] is an inbound server-side cap on request rate. Adaptive throttling is an *outbound client-side* cap on request rate, driven by observed rejection. The two are cooperative: server rate limits exist so that clients have something to observe, and client adaptive throttling exists so that the server doesn't have to burn CPU enforcing those limits on every over-quota request.

### Adaptive throttling and [[load-shedding]]

[[load-shedding]] is what the backend does when it cannot serve; adaptive throttling is what the client does in response to observing that shedding. Together they form a two-layer defence: the backend sheds to protect itself, and the client adapts so the backend spends less CPU on shedding.

### Adaptive throttling vs TCP congestion control

The policy is structurally similar to TCP's response to packet loss: observe a signal that indicates downstream congestion, reduce send rate proportionally, grow back when the signal clears. The K parameter serves the role of the slow-start / congestion-avoidance factor. The difference is that TCP operates on bytes and connections; adaptive throttling operates on request-response pairs and decisions. Both are local-information closed-loop controllers that compose into a globally stable system.

## Related pages

- [[handling-overload]]
- [[per-customer-quotas]]
- [[request-criticality]]
- [[load-shedding]]
- [[circuit-breaker]]
- [[rate-limiting]]
- [[retry-budget]]
- [[site-reliability-engineering]]
