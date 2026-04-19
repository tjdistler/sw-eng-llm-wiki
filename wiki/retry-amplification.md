# Retry Amplification

**Summary**: The failure mode where naïve client retries turn a transient overload into a sustained cascading failure. SRE Chapter 22 develops the mechanism: a backend rejects 100 QPS as overload, the client retries the 100 failed requests, which arrive on top of the normal 10,000 QPS — and next second's retries add to *those* failures, and so on. Retry volume grows geometrically until the backend melts down or the retry traffic stabilises at a multiple of the real load that the backend cannot sustain. Even restoring the incoming rate to pre-failure levels doesn't help: the retry loop remains, and the backend stays overloaded. Chapter 22 prescribes randomised exponential backoff, per-request and per-client retry budgets, clear error classification, and the "retry at only one level of the stack" rule that prevents combinatorial explosion.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's worked example

Chapter 22's opening scenario (source: chapter-22-addressing-cascading-failures.md):

1. A backend has a known limit of 10,000 QPS per task.
2. The frontend calls at 10,100 QPS, overloading the backend by 100 QPS. The backend rejects the 100.
3. Those 100 QPS of failures are retried every 1,000 ms.
4. Next second, the backend sees 10,200 QPS — 10,000 original + 100 new failures + 100 retries.
5. 200 QPS fail. Those 200 are retried.
6. Next second: 10,300 QPS. 300 fail. Retries grow.
7. Retry volume grows without bound. The backend eventually melts down under the sheer weight of requests and retries.

The failure is positive feedback: the response to overload (retries) *increases* the load on the backend that was already overloaded.

## Why even restoring the original rate doesn't help

From the chapter (source: chapter-22-addressing-cascading-failures.md):

> Even if the rate of calls to MakeRequest decreases to pre-meltdown levels (9,000 QPS, for example), depending on how much returning a failure costs the backend, the problem might not go away.

Two reasons:

1. **Rejection costs resources.** If the backend spends significant resources processing requests that will fail — parsing them, authenticating, checking quotas — then the retry volume keeps CPU saturated even without successful work. See [[adaptive-throttling]] for the client-side mechanism that pushes rejection decisions to the client to avoid this.
2. **Backend instability.** A backend that has started crashing under overload may not stabilise simply because traffic drops; it needs time to recover, and retry traffic prevents that time from accumulating.

The consequence: dropping the load rate alone doesn't fix the cascade. The retry loop must be broken, either by the backend signalling "overloaded; don't retry" or by the client-side retry budget exhausting.

## Chapter 22's retry guidelines

The chapter's seven-point list for automatic retries (source: chapter-22-addressing-cascading-failures.md):

### 1. Apply the broader overload defences

> Most of the backend protection strategies described in "Preventing Server Overload" apply. In particular, testing the system can highlight problems, and graceful degradation can reduce the effect of the retries on the backend.

Retry amplification is one face of the broader overload problem; the broader defences apply.

### 2. Randomised exponential backoff

> Always use randomized exponential backoff when scheduling retries... If retries aren't randomly distributed over the retry window, a small perturbation (e.g., a network blip) can cause retry ripples to schedule at the same time, which can then amplify themselves.

The chapter opens with the Dan Sandler quote:

> If at first you don't succeed, back off exponentially.

And the follow-up from Ade Oshineye:

> Why do people always forget that you need to add a little jitter?

Exponential alone is insufficient — without jitter, all clients retry at the same moment and produce a synchronised spike. The jitter spreads retries over a window.

### 3. Cap retries per request

> Limit retries per request. Don't retry a given request indefinitely.

This is what [[retry-budget]]'s per-request budget (three attempts) implements in the Chapter 21 framework.

### 4. Per-process retry budget

> Consider having a server-wide retry budget. For example, only allow 60 retries per minute in a process, and if the retry budget is exceeded, don't retry; just fail the request. This strategy can contain the retry effect and be the difference between a capacity planning failure that leads to some dropped queries and a global cascading failure.

The [[retry-budget]]'s 10% per-client retry ratio is the Chapter 21 realisation of this.

### 5. The combinatorial-retry rule

> Think about the service holistically and decide if you really need to perform retries at a given level. In particular, avoid amplifying retries by issuing retries at multiple levels: a single request at the highest layer may produce a number of attempts as large as the product of the number of attempts at each layer to the lowest layer.

The chapter's math:

> If the database can't service requests because it's overloaded, and the backend, frontend, and JavaScript layers all issue 3 retries (4 attempts), then a single user action may create 64 attempts (43) on the database.

Retries at every layer produce multiplicative amplification. Retry at **one** layer — the layer best positioned to know whether the request type is retryable and whether the remote call is likely to succeed this time — and let failures propagate up.

### 6. Clear response codes

> Use clear response codes and consider how different failure modes should be handled. For example, separate retriable and nonretriable error conditions. Don't retry permanent errors or malformed requests in a client, because neither will ever succeed. Return a specific status when overloaded so that clients and other layers back off and do not retry.

4xx client errors should almost never be retried; 5xx transient errors are candidates; "overloaded; don't retry" is the Chapter 21 signal that removes even transient-5xx retries when widespread overload is detected.

## Detection during incidents

The chapter warns about the diagnostic difficulty (source: chapter-22-addressing-cascading-failures.md):

> In an emergency, it may not be obvious that an outage is due to bad retry behavior. Graphs of retry rates can be an indication of bad retry behavior, but may be confused as a symptom instead of a compounding cause.

Retry spikes look like a symptom of backend failure; they are *also* a cause. The ambiguity makes debugging hard, which is why Chapter 22 emphasises prevention over reaction: once the retry storm is in progress, mitigation requires code changes, dramatic load reduction, or cutting requests off entirely — none of which is fast during an incident.

## Where retry amplification appears

The pattern has several faces (source: chapter-22-addressing-cascading-failures.md):

> This pattern has contributed to several cascading failures, whether the frontends and backends communicate via RPC messages, the "frontend" is client JavaScript code issuing XmlHttpRequest calls to an endpoint and retries on failure, or the retries originate from an offline sync protocol that retries aggressively when it encounters a failure.

Any layer that retries on failure can amplify — application code, HTTP libraries with default retry behaviour, mobile sync protocols, service-mesh sidecars, and so on. The prevention discipline applies everywhere retries happen.

## Relationship to existing wiki concepts

### Retry amplification and [[retry-budget]]

[[retry-budget]] is the Chapter 21 mechanism that implements Chapter 22's guidelines as a built-in RPC-framework feature. The per-request budget (3 attempts), per-client ratio (10%), retry-count metadata, and "overloaded; don't retry" response are direct answers to the Chapter 22 amplification problem. Chapter 22 is the *why*; Chapter 21 is the *how*.

### Retry amplification and [[adaptive-throttling]]

[[adaptive-throttling]] doesn't cap retries — it caps *first* attempts when the backend is rejecting too many. But the combined effect with retry budgets is what keeps backends stable under widespread overload: throttling bounds new requests, retry budget bounds retries on top of them.

### Retry amplification and [[circuit-breaker]]

A [[circuit-breaker]] is the alternative to retry budgets for capping retry amplification. Once the breaker is open, no retries pass through — a binary version of what the retry budget does probabilistically. Both mechanisms solve the same problem, with different trade-offs around responsiveness and smoothness.

### Retry amplification and [[idempotence]]

Retries are only safe for [[idempotence|idempotent]] operations. Applications with non-idempotent RPCs (bank transfers, order placement) need explicit duplicate-detection (e.g., operation IDs) before retrying. Chapter 22's retry guidelines assume idempotence; pairing them with the right application-level discipline is on the caller.

### Retry amplification and thundering herd

A thundering herd is retry amplification with an additional temporal synchronisation: a cache expiry, a service restart, or a deployment causes many clients to retry *at the same moment*, producing a spike that overwhelms even a healthy backend. Randomised exponential backoff is the defence against both the steady-state retry storm (Chapter 22's primary concern) and the synchronised spike.

## Chapter 27 client-side view

SRE Chapter 27 reaches the same retry-amplification concern from the launch-coordination side: [[abusive-client-behavior|client behaviour]] that misjudges update rates or retries aggressively can threaten a service's stability on launch day. The chapter's action-item answer is the same as Chapter 22's: exponential backoff with jitter, careful error classification (don't retry 4xx), and server-controlled client configuration so a misbehaving client fleet can be slowed remotely. The Chapter 27 framing adds two things:

- A standing [[launch-checklist-themes|launch-checklist question]] — "Do you have auto-save / auto-complete / heartbeat functionality?" — that surfaces these risks before launch
- The [[abusive-client-behavior|dormant-functionality pattern]] as a structural safety valve: new client behaviour is shipped inactive and activated server-side, so a retry or sync-rate misconfiguration can be disabled without pushing a new client version

## Related pages

- [[cascading-failure]]
- [[server-overload]]
- [[retry-budget]]
- [[adaptive-throttling]]
- [[circuit-breaker]]
- [[idempotence]]
- [[latency-and-deadlines]]
- [[addressing-ongoing-cascading-failure]]
- [[site-reliability-engineering]]
