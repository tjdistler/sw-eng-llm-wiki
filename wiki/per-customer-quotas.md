# Per-Customer Quotas

**Summary**: SRE Chapter 21's first line of defence against global overload: each customer of a backend service is allocated a CPU-denominated quota based on negotiated usage, and when global overload occurs the backend only rejects requests from customers that are over their quota. Per-customer limits may sum to more than the total provisioned capacity, relying on the statistical unlikelihood that all customers hit their limits simultaneously. Real-time global usage is aggregated from all backend tasks and pushed as effective limits to each task.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## The problem quotas solve

Chapter 21's framing is pragmatic (source: chapter-21-handling-overload.md):

> In a perfect world, where teams coordinate their launches carefully with the owners of their backend dependencies, global overload never happens and backend services always have enough capacity to serve their customers. Unfortunately, we don't live in a perfect world. Here in reality, global overload occurs quite frequently (especially for internal services that tend to have many clients run by many teams).

Without per-customer quotas, a single misbehaving customer (a launch gone wrong, a runaway batch job, a new feature with a bug) consumes capacity that belongs to every other customer. The service provider has no structural defence.

The design goal stated in the chapter:

> When global overload does occur, it's vital that the service only delivers error responses to misbehaving customers, while other customers remain unaffected.

## The mechanism

Chapter 21's worked example (source: chapter-21-handling-overload.md):

> If a backend service has 10,000 CPUs allocated worldwide (over various datacenters), their per-customer limits might look something like the following:
>
> - Gmail is allowed to consume up to 4,000 CPU seconds per second.
> - Calendar is allowed to consume up to 4,000 CPU seconds per second.
> - Android is allowed to consume up to 3,000 CPU seconds per second.
> - Google+ is allowed to consume up to 2,000 CPU seconds per second.
> - Every other user is allowed to consume up to 500 CPU seconds per second.
>
> Note that these numbers may add up to more than the 10,000 CPUs allocated to the backend service. The service owner is relying on the fact that it's unlikely for all of their customers to hit their resource limits simultaneously.

Two things are worth pulling out:

### The unit is CPU, not QPS

Quotas are expressed in **CPU seconds per second** — effectively "how many CPUs this customer is allowed to keep busy on average." This is the direct consequence of Chapter 21's [[queries-per-second-pitfalls|argument against QPS as a capacity metric]]. A CPU-denominated quota is stable as the customer's query mix evolves; a QPS-denominated quota would need to be re-tuned every time the customer shipped a new feature.

### Over-subscription is intentional

The customer limits (4,000 + 4,000 + 3,000 + 2,000 + 500 + others) sum to more than the 10,000 actually provisioned. This is deliberate. The service owner is betting on **non-correlated peaks**: Gmail and Calendar and Android are unlikely to all spike simultaneously, and the unused headroom lets every customer's burst capacity be larger than it could be under strict partitioning. This is the quota-system equivalent of memory over-commit.

The cost of over-subscription is that simultaneous peaks can still cause global overload, which is why the rest of Chapter 21's mechanisms ([[utilization-signals|local shedding]], [[adaptive-throttling|client throttling]], [[retry-budget|retry budgets]]) exist as fallbacks.

## Implementation: real-time global aggregation

Chapter 21 describes the mechanism at a high level (source: chapter-21-handling-overload.md):

> We aggregate global usage information in real time from all backend tasks, and use that data to push effective limits to individual backend tasks.

The chapter's scope doesn't cover the details ("a closer look at the system that implements this logic is outside of the scope of this discussion") but flags that Google has written "significant code" for this and that computing per-request CPU consumption in real time is itself non-trivial, especially for non-thread-per-request servers.

The conceptual pattern: each backend task observes local usage per customer, a global aggregator combines these, and the aggregator pushes per-task effective limits (which may be less than the global limit divided by the task count, to account for uneven client distribution). A task rejects a request from a customer whose current task-local usage exceeds the pushed limit.

## What quotas alone don't solve

The chapter's transition to the next mechanism makes clear that per-customer quotas are necessary but not sufficient (source: chapter-21-handling-overload.md):

- **Rejecting a request still costs resources.** For simple RAM-lookup services where rejection cost ≈ processing cost, a backend can saturate its CPU purely on rejecting traffic.
- **Clients have no awareness of their quota state.** Without client-side coordination, an over-quota customer keeps sending requests until every one is rejected, wasting network and backend CPU on the rejection path.

The first is why per-customer quotas pair with per-task [[utilization-signals|local overload protection]]; the second is why they pair with [[adaptive-throttling|client-side adaptive throttling]].

## Quotas per criticality

Chapter 21 flags a later refinement: per-customer limits can be **set per [[request-criticality|criticality]]**. A customer might have a high quota for `CRITICAL_PLUS` traffic and a much lower quota for `SHEDDABLE` traffic, reflecting the different cost the provider is willing to absorb for each. This composes with the shedding policy: even within a customer's budget, lower-criticality requests are dropped first.

## Relationship to existing wiki concepts

### Quotas and [[rate-limiting]]

Newman's [[rate-limiting]] page describes edge-tier rate limiting by client identity, IP, or path, typically measured in requests per unit time. Per-customer quotas are the internal-service equivalent, with two differences that matter at Google scale:

- **CPU, not QPS.** Quotas are measured in the resource actually being contended for.
- **Global, not per-instance.** The limit is enforced against aggregated cross-datacenter usage, not per-replica. This requires the real-time aggregation infrastructure the edge rate limiter usually doesn't need.

Rate limiting on a public API protects against misbehaving outside clients; per-customer quotas protect against misbehaving *internal* clients that the service provider cannot control. The patterns are structurally the same; the implementation differs because of the trust boundary.

### Quotas and [[bulkhead]]

A per-customer quota is a bulkhead across customers: one customer's over-use cannot consume another's share. [[bulkhead]] is the general pattern; per-customer quotas are the specific realisation for a multi-tenant backend where the tenants are other internal services. The bulkhead here is a logical CPU budget rather than a physical thread pool, but the isolation goal is identical.

### Quotas and [[event-broker-quotas]]

Bellemare's [[event-broker-quotas]] describes per-producer/per-consumer throughput and storage limits on the event broker. The intent is the same as per-customer quotas here — isolate each tenant from the noisy-neighbour effect of others — realised on the event-log side rather than the RPC side.

### Quotas and the cross-book rate-limit stack

Layering quotas together:

- Public-facing edge: [[rate-limiting]] by IP, user, or path.
- Internal RPC: per-customer quotas (this page).
- Per-task local defence: [[utilization-signals]] plus [[load-shedding]].
- Event-log layer: [[event-broker-quotas]].

No single layer is sufficient; each catches the cases the others don't.

## Related pages

- [[handling-overload]]
- [[adaptive-throttling]]
- [[request-criticality]]
- [[utilization-signals]]
- [[queries-per-second-pitfalls]]
- [[load-shedding]]
- [[rate-limiting]]
- [[bulkhead]]
- [[event-broker-quotas]]
- [[site-reliability-engineering]]
