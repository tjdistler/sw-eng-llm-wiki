# Consumer Lag Monitoring

**Summary**: Periodic measurement of [[consumer-offset|consumer lag]] per consumer group as the **primary autoscaling and health signal** for event-driven microservices. Thresholded lag triggers scale-up; sustained low lag triggers scale-down. Historical-deviation-based measurements (e.g. Burrow) are preferred to raw thresholds for spiky workloads.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## What lag means here

**Consumer lag** = most-recent offset on the partition − last-processed offset for the consumer group (source: chapter-14-supportive-tooling.md). The definition is broker-independent; the measurement mechanism varies.

See [[consumer-offset]] for the deeper mechanics.

## The basic autoscaling loop

The textbook policy (source: chapter-14-supportive-tooling.md):

- If lag > **N** events for more than **M** minutes → double the consumer-processor count and rebalance.
- If lag is resolved and running processors exceed the configured minimum → scale down.

**Hysteresis** — a tolerance band — is essential. Without it a workload that oscillates near the threshold flaps up and down continuously. Modern cloud autoscalers (AWS CloudWatch, Google Cloud Operations) have hysteresis primitives built in.

## Historical-deviation monitoring (Burrow)

Threshold rules mislead on high-rate streams. If events arrive in bursts such that lag is only momentarily zero between bursts, a naive threshold will flag the consumer as perpetually lagging even when it's keeping up fine (source: chapter-14-supportive-tooling.md).

Burrow (for Apache Kafka) instead tracks the **history of lag** and compares current behavior against that history. "Unhealthy" becomes *"deviation from established norms"* rather than *"above a fixed number"*. This is the right model for spiky production workloads.

## Why lag is the right scaling signal for EDM

Unlike CPU- or memory-based autoscaling, lag is:

- **Workload-proportional** — it grows when work is arriving faster than it's processed, which is exactly what scale-up should respond to.
- **Consumer-centric** — it ignores the producer side, so upstream rate changes don't noise up the signal.
- **Already in the broker** — no extra metrics pipeline is needed.

This is why lag-based scaling is the default in [[faas-triggers|FaaS-on-EDM]] triggers, [[stream-processing-scaling-strategies|stream-processing scaling strategies]], and [[container-management-system|CMS]] autoscalers driven by lag metrics.

## Relationship to existing wiki coverage

- **[[consumer-offset]]** — the lag signal this tool monitors.
- **[[stream-processing-scaling-strategies]]** — Chapter 11's elasticity framework; consumer lag is one of its inputs.
- **[[faas-triggers]]** — FaaS invocations driven by lag > 0.
- **[[functions-as-a-service]]** — scale-to-zero behaves naturally because lag = 0 ⟹ no invocation.

## Related pages

- [[edm-supportive-tooling]]
- [[consumer-offset]]
- [[consumer-group]]
- [[stream-processing-scaling-strategies]]
- [[container-management-system]]
- [[faas-triggers]]
