# The Four Golden Signals

**Summary**: Google SRE's canonical four metrics for a user-facing system: **latency, traffic, errors, saturation**. If you can only measure four things, measure these — and page a human when any one is problematic or (for saturation) nearly so.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`

**Last updated**: 2026-04-17

---

## The four signals

Rob Ewaschuk's Chapter 6 lists them in this order (source: chapter-06-monitoring-distributed-systems.md):

### Latency

The time it takes to service a request. The crucial subtlety: **track successful latency and failed latency separately**. An HTTP 500 returned quickly after a backend-connection failure would otherwise pollute the overall latency number, making things look faster than they are. And a slow error is worse than a fast error, so you can't just filter errors out — you have to measure them separately.

See [[response-time-percentiles]] for why this signal has to be reported as a distribution, not a mean.

### Traffic

A measure of how much demand is being placed on the system, in a high-level service-specific unit:

- Web service: HTTP requests per second, broken out by request nature (static vs dynamic)
- Audio streaming: network I/O rate or concurrent sessions
- Key-value store: transactions and retrievals per second

Traffic is the independent variable the other three signals should be interpreted against.

### Errors

The rate of requests that fail. Three failure modes to cover:

- **Explicit**: HTTP 500 and equivalents
- **Implicit**: a "success" response carrying the wrong content
- **By policy**: "we committed to one-second responses; anything over one second is an error"

Where the protocol's response codes can't express all failure modes (implicit failures especially), secondary internal protocols may be needed. Catching explicit failures is cheap (load balancer logs suffice); catching wrong-content failures typically requires end-to-end tests.

### Saturation

How "full" the service is — the fraction of its most constrained resource that's currently in use. Memory-bound service: memory. I/O-bound: I/O. The key caveat is that most systems degrade well before 100% utilization, so **the utilization target matters** — you generally can't run to saturation.

Saturation has three sub-concerns:

- **Current utilization** of the bottleneck resource
- **Higher-level load measurement**: can the service handle 2x traffic? 1.1x? Less than it has now?
- **Imminent saturation predictions**: "your database fills its disk in 4 hours"

Latency increases (especially p99 over a short window like 1 minute) are often a **leading indicator** of saturation, before raw resource metrics cross their thresholds.

## Why these four

The argument is one of coverage: if you measure all four signals and page when any is problematic or nearly so, your service is *at least decently* covered. The four together span:

- User experience (latency, errors)
- Demand (traffic)
- Headroom (saturation)

You can miss serious incidents with any one of them alone; you rarely miss them with all four.

## Relationship to symptoms vs causes

The four golden signals are all [[symptoms-vs-causes|symptoms]], not causes. They describe what users experience and what the service has left to give, not why something is broken. That's deliberate: Chapter 6 is emphatic that paging should be symptom-oriented, and the four signals are the canonical symptoms for a user-facing system.

## Instrumentation discipline

Latency and saturation both require distribution-aware measurement, not averages:

- **Latency**: bucket request counts by latency range (histograms), distributing bucket boundaries approximately exponentially (e.g. factors of ~3). See [[long-tail-latency]] for why.
- **Saturation**: even something like CPU utilization can be imbalanced across nodes; mean CPU hides hotspots. The Chapter 6 recommended trick is per-second internal sampling into bucketed histograms on each server, aggregated every minute externally. See [[monitoring-resolution]].

## Cross-book connections

- [[monitoring-and-observability]] — the monitoring side of Newman's monitoring-vs-observability split; the four golden signals are the concrete "what to measure for monitoring" answer
- [[service-level-indicator]] — SLIs for user-facing services typically cover availability, latency, throughput, which map to errors/latency/traffic of the four golden signals; the fourth SLI category (saturation) appears in the SRE Chapter 4 "all service types" bucket under durability/correctness
- [[tail-latency-amplification]] (Burns) — why a backend's latency distribution, not its mean, is what propagates up the stack
- [[unified-monitoring-interface]] (Burns) — the adapter-container mechanism for exposing these four metrics consistently across heterogeneous apps

## Related pages

- [[symptoms-vs-causes]]
- [[black-box-vs-white-box-monitoring]]
- [[long-tail-latency]]
- [[monitoring-resolution]]
- [[alert-philosophy]]
- [[monitoring-and-observability]]
- [[sre-monitoring-outputs]]
- [[response-time-percentiles]]
- [[service-level-indicator]]
- [[site-reliability-engineering]]
