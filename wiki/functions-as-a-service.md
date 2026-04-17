# Functions as a Service

**Summary**: The fourth serving pattern in Burns's catalogue. Functions-as-a-Service (FaaS) is an event-driven style of computing in which short-lived, stateless functions are instantiated in response to discrete events or requests, scaled automatically by the platform, and billed per invocation. FaaS shines for lightweight, stateless, bursty event handlers and decorators — and is a poor fit for long-running work, in-memory state, and sustained steady-state load.

**Sources**: `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`, `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The shape of the pattern

The previous three serving patterns — [[replicated-load-balanced-service]], [[sharded-service-pattern]], [[scatter-gather-pattern]] — all assume **long-running** server processes that sit waiting for traffic. FaaS inverts that assumption: the server doesn't exist until an event fires, the function runs, returns, and vanishes. The platform manages lifecycle, scaling, and placement; the developer supplies only the function body and a trigger (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

Burns frames FaaS as "a class of applications that might only need to temporarily come into existence to handle a single request, or simply need to respond to a specific event" — the class of work that is event-shaped rather than session-shaped (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

## Serverless vs event-driven

Burns spends part of the chapter opening on a terminology distinction that matters for design (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- **Serverless** means you don't see the servers — the platform operates them. A multi-tenant container-as-a-service platform is serverless but not event-driven.
- **Event-driven** means execution is triggered by discrete events rather than a long-running server loop. An open-source FaaS running on a cluster of physical machines you own and administer is event-driven but not serverless.
- **FaaS** typically sits in the intersection of the two — but they are separate axes, and understanding which axis you need helps you pick the right platform.

This matters because the benefits Burns attributes to FaaS actually come from different axes: the developer-productivity benefits are about serverlessness (no artefact to build, no fleet to manage), while the architectural constraints (short runtimes, stateless instances, request-based billing) are about event-drivenness.

See [[serverless-vs-event-driven]] for the standalone framing.

## Benefits of FaaS

Burns's benefits are primarily developer-facing (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- **Shortest path from code to running service.** No artefact to build or push — the source is the deployment unit. You can go from a browser editor to production code.
- **Automatic scaling.** The platform spins up more function instances as traffic rises and scales to zero when it falls.
- **Automatic fault recovery.** When a function fails, the platform restarts it on another machine.
- **Granular building block.** Functions are even more granular than containers. Because they are stateless by construction, systems built from FaaS are "inherently more modular and decoupled than a similar system built into a single binary."

The last benefit is also the main challenge, as Burns immediately notes: the decoupling is both a strength and a weakness.

## Challenges of FaaS

Three operational and three architectural challenges appear in the chapter (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

### Operational: hard to see the whole system

Each function is "entirely independent. The only communication is across the network, and each function instance cannot have local memory, requiring all states to be stored in a storage service." The forced decoupling accelerates development but complicates operations — it is "often quite difficult to obtain a comprehensive view of your service, determine how the various functions integrate with one another, and understand when things go wrong, and why they go wrong."

Burns's worked pathology: `functionA` calls `functionB` calls `functionC` calls back to `functionA`. An inbound request kicks off an **infinite loop that terminates only when the request times out — or when you run out of money to pay for invocations**. Because there is no real representation of dependencies between functions, this is surprisingly hard to catch at authoring time. Burns's counsel: adopt rigorous monitoring and alerting early, accepting that this friction offsets some of FaaS's deployment simplicity.

### Architectural: no background processing

Function runtime is time-bounded by the platform, which makes FaaS "usually a poor fit for situations that require [background] processing." Burns's examples: transcoding video, compressing log files, any low-priority long-running computation. Scheduled triggers can synthesise events for temporal tasks ("fire a text-message alarm at 7 AM") but don't help with genuinely long-running work. Long-running work needs a pay-per-consumption environment, not pay-per-request — work queues and batch patterns (Part III of the book) are the right answer.

### Architectural: no in-memory data

"Need to have a significant amount of data loaded into memory in order to process user requests" is the second disqualifier. A search index, a large model, a warm cache — all break the FaaS model. Because the function may be **cold-started while the user is waiting**, loading cost dominates latency. Once warm, the instance can amortise across many requests, but if the service stays warm long enough for amortisation, you are "likely overpaying for the requests you are processing" under per-request billing.

### Economic: the cost curve inverts

Per-request billing is excellent for low request rates — you pay nothing when idle. As request volume grows enough to keep a processor continuously busy, per-request pricing starts to lose to per-VM pricing, and the gap widens because VM prices decline with core count and committed use while per-request prices scale roughly linearly with calls (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

Burns's guidance: "as your service grows and evolves, it's highly likely that your use of FaaS will evolve as well." One graceful escape hatch is **open-source FaaS running on a container orchestrator like Kubernetes** (the chapter uses [Kubeless](https://kubeless.io/)) — you keep the developer experience but pay VM prices. This is the "event-driven but not serverless" corner of the matrix above.

## When FaaS is appropriate

Combining Burns's benefits and challenges, FaaS is a good fit when all of the following hold (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- Work is naturally **event-shaped** — triggered by a discrete event rather than part of a long interactive session.
- Each invocation is **stateless** or close to it — no warm caches or large in-memory data sets.
- Work completes **quickly** — well under the platform's runtime limit.
- Request volume is **bursty or low** — so pay-per-request undercuts pay-per-VM.
- The handler is **small and focused** — so the developer-productivity benefits are the headline, not a rounding error on a larger service.

## When FaaS is inappropriate

The inverse, distilled from the same source:

- **Long-running background work** — video transcoding, log compression, batch analytics. Use a [[batch-processing|batch]] or work-queue pattern instead.
- **Services that need warm in-memory state** — search indexes, ML models, large caches. A [[replicated-load-balanced-service]] or [[sharded-service-pattern]] fits better.
- **Steady-state, high-volume request serving** — the pay-per-request curve loses to VMs. Graduate to a long-running service.
- **Applications where system-wide behaviour is hard to reason about** — because debugging across deeply nested functions is weak. Limit FaaS to the composable edges, not the core.

## Events vs requests

Burns draws a distinction between requests and events that clarifies where FaaS fits even within event-shaped work (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- A **request** is part of a larger series of interactions — a session with a web app or API.
- An **event** is single-instance and asynchronous — a user signing up, a file being uploaded, a machine about to reboot — fired from a main interaction and responded to some time later.

Most systems are request-driven, and request-driven load is usually the wrong workload for FaaS (sustained, stateful, session-shaped). But the **event-driven augmentations** of request-driven systems — welcome emails, upload notifications, two-factor SMS codes — are nearly ideal FaaS candidates. They are asynchronous, stateless, independent, and the rate of events is highly variable.

Burns's worked example: implementing two-factor authentication as a FaaS invoked asynchronously from the login server. The login web server fires a webhook into a function that generates the code, registers it with the login service, and sends the SMS via Twilio. Keeping this out of the login request path means the slow SMS round-trip doesn't block the login UX (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

See [[event-streams]] and [[message-brokers]] for the data-layer counterparts of this framing — event-driven FaaS is often the compute-layer consumer of a message broker or event log.

## Composition patterns

Burns catalogues two composition patterns for FaaS, each of which has its own page:

- **[[faas-decorator-pattern]]** — a function sits between a caller and a backend, transforming the request or response. Burns uses the Python decorator analogy — stateless transformations bolted onto an existing API. Worked example: JSON default-value filling in front of a REST API.
- **[[event-pipeline-pattern]]** — a directed graph of functions connected by HTTP/webhook edges, each node a small stateless handler. Worked examples: a CI pipeline spanning build, human approval, and deployment; a new-user signup flow spanning welcome email and mailing-list subscription.

Both patterns lean on the same two FaaS strengths: near-zero deploy cost for small handlers, and forced decoupling that maps naturally to the per-function granularity.

## Relationship to other patterns

### To the single-node patterns

The FaaS decorator has a structural overlap with the [[adapter-pattern]]: both transform an inbound or outbound interface without modifying the backend. Burns anticipates the question in the chapter and gives a practical answer: the adapter runs alongside the service it adapts, so the adapter scales with the service; a FaaS decorator scales independently, which is right when the decorator is much lighter than the service (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md). Use an adapter container when you want per-service affinity and one-to-one lifecycle with the application pod; use a FaaS decorator when you want the transformation to scale on its own axis.

Similarly, the FaaS event handler overlaps with the [[sidecar-pattern]] for small cross-cutting additions and with the [[ambassador-pattern]] for front-of-service interception. The deciding question is almost always whether the extra work should scale with the application or on its own.

### To the other serving patterns

FaaS completes the serving-pattern quartet (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

| Pattern | Replicates for... | State model | Scales on... |
|---|---|---|---|
| [[replicated-load-balanced-service]] | Request throughput | Stateless | Request rate |
| [[sharded-service-pattern]] | State size | Stateful (disjoint shards) | State size and per-shard load |
| [[scatter-gather-pattern]] | Latency (time) | Stateful leaves (or stateless) | Leaf count, with tail-latency ceiling |
| FaaS (this page) | Nothing long-running | Stateless | Event rate, automatically to zero |

The other three serving patterns compose by layering. FaaS composes by **event chaining** — functions call or emit into other functions rather than being stacked into the same request path.

### To event streams and message brokers

Burns's chapter treats triggering synchronously over HTTP/webhooks, but production FaaS deployments typically sit behind [[message-brokers]] or [[log-based-message-brokers]] (Kafka, Kinesis, AWS SQS) for the same reasons as any other event consumer: buffering, fan-out, replay, and decoupling producer from consumer. [[event-streams]] is the most direct data-layer companion. The fan-in / fan-out patterns on [[event-streams]] apply directly to FaaS consumers.

### To event sourcing and CDC

[[event-sourcing]] and [[change-data-capture]] produce exactly the kind of event stream that FaaS consumes well — small, discrete, stateless-to-process events arriving at variable rate. The Burns chapter doesn't name either but the composition is natural: a CDC stream of database changes feeds a FaaS that fires notifications, computes derived views, or invokes downstream systems.

### To "serverless-first" and running-too-many-things

Newman's [[running-too-many-things]] argues that for teams on the public cloud, FaaS should be the **default choice** rather than a niche tool — "try to make use of serverless technology like FaaS as a default choice, because of the reduction in operational work" (Newman, chapter-05-growing-pains.md). Burns's more cautious Chapter 8 framing identifies the limits where that default stops applying: large in-memory state, long-running work, sustained high-volume request serving. The two treatments are complementary — Newman pushes teams toward FaaS as a starting point; Burns catalogues when to graduate away.

[[desired-state-management]] is the capability FaaS platforms deliver for free: the platform continuously reconciles invocations against demand without the developer specifying instance counts.

### To microservices

A FaaS deployment is a degenerate microservice architecture in which each "service" is a single function. This gives the [[independent-deployability]] and [[information-hiding]] benefits of microservices very cheaply, at the cost of the operational visibility problem Burns flags. For systems small enough that the pipeline fits in a person's head, FaaS can deliver the benefits of microservices without the usual platform investment. For systems that grow past that threshold, either the operational tooling has to catch up or the system has to consolidate into larger services.

## Bellemare's EDM framing

Chapter 9 of *Building Event-Driven Microservices* treats FaaS as a first-class option for implementing event-driven microservices, with a specifically EDM-shaped design discipline layered on top of Burns's pattern-level framing. Bellemare's mental model: think of a FaaS solution as "a basic consumer/producer implementation that regularly fails" — a function will always end after a predetermined amount of time, and any connections and state associated with it will go away (source: chapter-09-microservices-using-function-as-a-service.md).

### Four components of every function-based microservice

Regardless of framework, every function-based microservice has four parts (source: chapter-09-microservices-using-function-as-a-service.md):

1. **The function** itself — in whatever language the FaaS framework supports.
2. **Input event stream(s)** — subscribed via the framework or via an external connector.
3. **Triggering logic** — a function-trigger map binding events to the function. See [[faas-triggers]] for the full catalogue and [[event-stream-listener]] for the canonical EDM case.
4. **Error, scaling, and consumer policies** — consumer group (every function-based microservice gets its own), batch size, batch window, retry policy, scaling policy.

### Design disciplines

Bellemare's four FaaS design rules for EDM (source: chapter-09-microservices-using-function-as-a-service.md):

- **Strict bounded-context membership.** Functions and the internal event streams they use must belong to a single owner. Mapping of function → [[bounded-context]] can be 1:1 or n:1 (several functions per context) but not the other way around. Enforce it with private data stores, standard request/response or event interfaces at the edge, metadata, and per-context repositories.
- **Commit offsets only after processing completes.** The at-least-once discipline standard for every other microservice style. Committing on function start is a FaaS anti-pattern that risks data loss. See [[faas-offset-management]].
- **Less is more.** Avoid "write one function, reuse it in five services" — ownership becomes ambiguous, change risk opaque, versioning overhead compounds. Fewer functions per bounded context is easier to test, debug, and manage than many granular ones.
- **Clean up on termination.** Intermittent functions should close broker connections and relinquish partition assignments at end-of-life. Near-always-on functions can leave them open. See [[cold-start-warm-start]].

### Choosing a provider

Open-source options include OpenWhisk, OpenFaaS, Kubeless, and Apache Pulsar's built-in FaaS. Cloud providers (AWS, GCP, Azure) offer proprietary FaaS tightly integrated with their own event brokers — attractive if you are already a subscriber, but with an important caveat Bellemare flags: all three cloud-provider brokers limit event retention to seven days, which is a tight constraint for an EDM substrate that depends on indefinite replay. Kafka Connect and similar bridges can integrate the proprietary FaaS with open-source brokers at additional setup cost (source: chapter-09-microservices-using-function-as-a-service.md).

### Triggers, batching, and composition — linked pages

The chapter's remaining material splits cleanly along four axes that each get their own page:

- **[[faas-triggers]]** — five trigger categories: event-stream listener, consumer-group lag, schedule, webhook, resource events.
- **[[event-stream-listener]]** — the canonical EDM trigger, with batch size, batch window, sync vs async dispatch, and integrated-vs-external listener variants.
- **[[cold-start-warm-start]]** — the function lifecycle and its interaction with consumer-group rebalancing.
- **[[faas-batch-processing]]** — tuning batch size, execution time, and resource allocation to avoid the fail-retry-fail-again loop; automatic batch halving.
- **[[faas-offset-management]]** — the before-vs-after commit decision and its effect on data loss.
- **[[faas-function-composition]]** — event-driven communication vs direct call (sync / async), and how each maps onto [[workflows-in-edm|choreography and orchestration]].

### When FaaS fits EDM

Bellemare's summary of where FaaS shines aligns with Burns's list but adds EDM-specific framing (source: chapter-09-microservices-using-function-as-a-service.md):

- Simple topologies and [[stateless-stream-processing|stateless]] or lightly stateful processing.
- Workloads that do not require deterministic processing across multiple event streams (no [[event-scheduling|event scheduling]]).
- Wide-fan queue-based processing where ordering doesn't matter.
- Highly variable volumes where scale-to-zero pays off.

Determinism and copartitioned processing are the main limits — same constraint as the [[stateful-stream-processing|stateful-stream]] heavyweight frameworks, and for the same reason: only one function can process a given partition at a time.

## Related pages

- [[serverless-vs-event-driven]]
- [[faas-decorator-pattern]]
- [[event-pipeline-pattern]]
- [[faas-triggers]]
- [[event-stream-listener]]
- [[faas-offset-management]]
- [[faas-batch-processing]]
- [[cold-start-warm-start]]
- [[faas-function-composition]]
- [[event-driven-microservices]]
- [[workflows-in-edm]]
- [[replicated-load-balanced-service]]
- [[sharded-service-pattern]]
- [[scatter-gather-pattern]]
- [[adapter-pattern]]
- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[event-streams]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[event-sourcing]]
- [[change-data-capture]]
- [[stream-processing]]
- [[running-too-many-things]]
- [[desired-state-management]]
- [[microservices]]
- [[independent-deployability]]
- [[coupling]]
- [[cohesion]]
- [[designing-distributed-systems]]
