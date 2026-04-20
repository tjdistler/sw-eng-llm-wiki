# Request Criticality

**Summary**: SRE Chapter 21's four-valued priority attached to every RPC request: `CRITICAL_PLUS` (user-visible impact if it fails), `CRITICAL` (default for production requests), `SHEDDABLE_PLUS` (partial unavailability expected — default for batch), and `SHEDDABLE` (frequent partial unavailability and occasional full unavailability expected). Criticality is a first-class property of Google's RPC system, propagated automatically down call chains, set as close to the browser or mobile client as possible, and consumed by every overload-handling mechanism — [[per-customer-quotas|quotas]], [[adaptive-throttling|client throttling]], [[utilization-signals|local shedding]] — so that when a service is overloaded, it can reject low-criticality work first and preserve capacity for what matters.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## The four values

Chapter 21 defines exactly four criticality levels (source: chapter-21-handling-overload.md):

| Value | Meaning |
|---|---|
| **CRITICAL_PLUS** | Reserved for the most critical requests, those that will result in *serious* user-visible impact if they fail. |
| **CRITICAL** | The default for requests sent from production jobs. Failures result in user-visible impact but less severe than CRITICAL_PLUS. Services are expected to **provision enough capacity for all expected CRITICAL and CRITICAL_PLUS traffic**. |
| **SHEDDABLE_PLUS** | Traffic for which partial unavailability is expected. Default for batch jobs (which can retry minutes or hours later). |
| **SHEDDABLE** | Traffic for which frequent partial unavailability and occasional full unavailability is expected. |

The chapter addresses the obvious "why not more levels" question (source: chapter-21-handling-overload.md):

> We've had various discussions on proposals to add more values, because doing so would allow us to classify requests more finely. However, defining additional values would require more resources to operate various criticality-aware systems.

Four is a deliberate compromise between expressiveness and operational cost.

## How criticality is used

Chapter 21 weaves criticality into every overload-handling mechanism (source: chapter-21-handling-overload.md):

- **Per-customer quotas can be set per criticality.** A customer might have a high `CRITICAL_PLUS` quota and a small `SHEDDABLE` quota, reflecting the different cost the provider is willing to absorb for each class. When a customer runs out of quota at a given criticality, the backend only rejects that criticality's requests if it's already rejecting everything below.
- **Local overload shedding is criticality-aware.** When a task is itself overloaded, [[utilization-signals|higher thresholds]] apply to higher criticalities — a task rejects `SHEDDABLE` at lower utilisation than `CRITICAL_PLUS`.
- **Adaptive throttling tracks stats per criticality.** This keeps sheddable-stream rejection from throttling critical-stream sending (see [[adaptive-throttling]]).

The net effect: when any part of the system is under pressure, load is shed from the low-criticality traffic first, while high-criticality traffic continues to flow. Gmail search suggestions (`SHEDDABLE` — it's fine if they disappear) drop before Gmail message send (`CRITICAL_PLUS` — users notice immediately).

## Criticality is orthogonal to latency

Chapter 21 is explicit that criticality is not the same as QoS (source: chapter-21-handling-overload.md):

> The criticality of a request is orthogonal to its latency requirements and thus to the underlying network quality of service (QoS) used. For example, when a system displays search results or suggestions while the user is typing a search query, the underlying requests are highly sheddable (if the system is overloaded, it's acceptable to not display these results), but tend to have stringent latency requirements.

Sheddable-and-fast (search-as-you-type suggestions), sheddable-and-slow (batch jobs), critical-and-fast (message send), critical-and-slow (a long-running report): all four combinations exist. The RPC stack treats them as independent dimensions.

## Propagation: set at the edge, flow automatically

Chapter 21's operational rule (source: chapter-21-handling-overload.md):

> We've also significantly extended our RPC system to propagate criticality automatically. If a backend receives request A and, as part of executing that request, issues outgoing request B and request C to other backends, request B and request C will use the same criticality as request A by default.

The rationale is defence-in-depth: if the end user's request is `CRITICAL_PLUS`, every downstream RPC in its dependency tree inherits that criticality, so an overloaded service ten hops down the stack still sheds the right traffic first. Without automatic propagation, each service would independently classify its outgoing calls, and classification drift would break the end-to-end guarantee.

The set-it-once point:

> Our practice is thus to set the criticality as close as possible to the browsers or mobile clients — typically in the HTTP frontends that produce the HTML to be returned — and only override the criticality in specific cases where it makes sense at specific points in the stack.

This is structurally the same design as correlation IDs: attach a property at the entry point, let it flow with the request through every hop, and override only where the semantics genuinely differ.

## Why standardisation matters

Chapter 21 flags that before criticality was standardised in the RPC framework, it wasn't absent — it was just fragmented (source: chapter-21-handling-overload.md):

> In the past, many systems at Google had evolved their own ad hoc notions of criticality that were often incompatible across services. By standardizing and propagating criticality as a part of our RPC system, we are now able to consistently set the criticality at specific points. This means we can be confident that overloaded dependencies will abide by the desired high-level criticality as they reject traffic, regardless of how deep down the RPC stack they are.

The pattern — **promote a cross-cutting property into framework-level infrastructure** — is the same move that [[backend-task-states|three-state backend models]] and [[weighted-round-robin|weighted round robin]] embody. Put it in Stubby, and every service gets it for free; leave it as a per-team convention, and inconsistencies compound across the call graph.

## Relationship to existing wiki concepts

### Criticality and [[bulkhead]]

Criticality is a soft bulkhead across *priority classes*: overloaded resources preferentially serve the high-criticality class, so a flood of low-priority traffic can't starve high-priority traffic even though both share the same physical resources. Unlike a hard bulkhead (separate thread pools per tenant), the boundary is probabilistic and per-request rather than structural. The trade-off is less rigid isolation in exchange for better utilisation: without criticality-based shedding, the service would need separate deployments per priority, which is wasteful when the priorities mostly don't peak at the same time.

### Criticality and [[correlation-ids]]

Criticality and correlation IDs share the same propagation pattern — set at the entry point, attached to the RPC envelope, carried through every hop automatically. The difference is what the downstream does with it: correlation IDs are for observability (tie together log lines, trace spans), criticality is for policy (decide whether to serve). Both live in the same RPC metadata and ride for free on every request.

### Criticality vs classical [[circuit-breaker|circuit breaking]]

A classical circuit breaker operates on a single dependency with no notion of what the call is *for*. Criticality turns the decision into a prioritised one: if the downstream is struggling, cut the sheddable calls first. This is particularly important for services that have both user-facing and batch load paths that share a dependency — a blind circuit breaker that opens when batch floods the shared dependency will also fail user-facing calls, while a criticality-aware shedding decision keeps user-facing flowing until the very last moment.

### Criticality and [[load-shedding]]

[[load-shedding]] is the action (reject this request now); criticality is the *input* that determines which requests are shed first. Chapter 21 is structured so that criticality is the data and shedding is the policy; keeping them separate means the policy can be changed without re-labelling every call site.

## Related pages

- [[handling-overload]]
- [[per-customer-quotas]]
- [[adaptive-throttling]]
- [[utilization-signals]]
- [[load-shedding]]
- [[correlation-ids]]
- [[bulkhead]]
- [[circuit-breaker]]
- [[site-reliability-engineering]]
