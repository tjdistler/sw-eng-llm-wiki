# Event Pipeline Pattern

**Summary**: Burns's second canonical FaaS composition pattern. A directed graph of stateless functions is connected by HTTP webhooks or other network calls — events flow from node to node, each function doing a small piece of work and emitting an event for the next. Event pipelines suit flows that are naturally asynchronous, span heterogeneous participants (including humans), and would be awkward to express as either a monolith or a set of long-running microservices.

**Sources**: `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

An event pipeline is a **directed graph of event sinks** (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- **Nodes** are functions or webhooks — each a [[functions-as-a-service|FaaS]] handler or an external system that accepts webhooks.
- **Edges** are HTTP (or other network) calls that deliver events from one node to the next.
- There is generally **no shared state** between pieces of the pipeline, but "there may be a context or other reference point that can be used to look up information in shared storage."

Burns compares the topology to the flowcharts of old: a business process expressed as a graph where each node is a small responsibility and each edge is a handoff.

## Why it's distinct from microservices

Burns draws two specific differences between event pipelines and a conventional microservices architecture (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

1. **Event-driven vs long-running.** An event pipeline is event-driven by construction — each node runs only when an event arrives. A microservices architecture is a collection of long-running services.
2. **Heterogeneous participants.** "Event-driven pipelines may be highly asynchronous and diverse in the things that they connect together. For example, while it is difficult to see how a human approving a ticket in a ticketing system like Jira could be integrated into a microservices application, it's quite easy to see how that event could be incorporated into a event-driven pipeline."

This second point is the load-bearing one. Event pipelines admit **non-software nodes** — a human approving a Jira ticket, an external SaaS firing a webhook, a build job in CI. Microservices architectures, by contrast, are built on the assumption that all participants are co-operative long-running services speaking the same protocols.

## Worked example: CI pipeline with human approval

Burns's chapter example (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

1. Developer commits code to source control → triggers a build event.
2. Build completes (minutes later) → fires a build-analysis event.
3. Build-analysis function branches:
   - **Success** → create a Jira ticket for a human to approve production deploy.
   - **Failure** → file a bug and terminate the pipeline.
4. Human closes the approval ticket → fires an event that triggers the production deploy.

The pipeline spans source control, a build system, a FaaS, Jira, a human, and a deploy system. No single "coordinator" owns it; each stage fires the next by emitting an event. Burns's point: this flow is easy to draw as a graph and awkward to express as a microservices architecture because half the nodes aren't services.

## Worked example: new-user signup

A simpler pipeline from the chapter's second worked example. When a user signs up, the pipeline must send a welcome email, and optionally subscribe the user to a mailing list (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

The monolithic alternative puts all the logic in one user-creation server, owned by one team, deployed as one unit. Burns's factoring instead makes the user-creation function a dispatcher that just fires webhooks:

```python
def create_user(context):
    # Required handlers always called
    for key, value in required.items():
        call_function(value.webhook, context.json)
    # Optional handlers called conditionally
    for key, value in optional.items():
        if context.json.get(key, None) is not None:
            call_function(value.webhook, context.json)
```

Each handler is itself a FaaS:

```python
def email_user(context):
    user = context.json['username']
    msg = 'Hello {} thanks for joining my awesome service!'.format(user)
    send_email(msg, context.json['email'])

def subscribe_user(context):
    email = context.json['email']
    subscribe_user(email)
```

Two payoffs Burns calls out (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

1. **Each FaaS is tiny and focused** — a few lines, one responsibility. Writing, testing, and evolving each piece is straightforward.
2. **The pipeline graph itself is the high-level design.** "By visualizing our user-creation flow as an event-driven pipeline, it is also straightforward to have a high-level understanding of what exactly happens on user login, simply by following the flow of the context through the various functions in the pipeline."

The second payoff is unusual: the pipeline topology is **both the wiring and the specification**. Reading the graph tells you what happens on signup, because the graph is what happens on signup.

## When event pipelines fit

The pattern is a strong fit when (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md and natural extensions):

- Work is naturally asynchronous — no single caller is waiting synchronously for the end-to-end result.
- Steps are independent — each node can be reasoned about on its own inputs.
- Heterogeneous participants — humans, external SaaS, CI/CD systems, or third-party APIs must participate.
- Steps evolve at different rates — new optional handlers are added frequently, old ones deprecated.
- Handlers are small enough that the per-function deployment overhead of FaaS is negligible.

## When event pipelines don't fit

- **Synchronous end-to-end latency matters** — event chaining adds network hops, and each FaaS invocation can cold-start. A long-running service is faster.
- **Large in-memory state is needed** — same as the general FaaS limitation; long-running data-loaded services fit better.
- **The graph becomes too big to follow by reading it** — Burns's pathology of circular function chains becomes a real risk at scale. Without dependency visualisation, the graph-as-spec benefit collapses.
- **Strong transactional semantics across the pipeline** — event pipelines are naturally eventually consistent; if the flow needs cross-step atomicity, a [[saga]] with explicit compensation is a better frame than ad hoc webhooks.

## Relationship to event streams and message brokers

Burns's chapter shows pipelines wired over HTTP webhooks, but the same topology is routinely built on [[message-brokers]] or [[log-based-message-brokers]] (Kafka, Kinesis, AWS EventBridge, Google Pub/Sub). The broker-based form gives buffering, replay, and fan-out for free — important once the pipeline grows beyond a handful of handlers. [[event-streams]] provides the vocabulary.

The broker-mediated pipeline also avoids one of the failure modes of the webhook form: if a downstream FaaS is temporarily unreachable, a synchronous webhook either blocks or drops the event, whereas a broker queues it for retry. Burns doesn't dwell on this in Chapter 8 because his focus is the shape of the pattern, not the transport.

## Relationship to stream processing

[[stream-processing]] operators arranged in a DAG are structurally the same pattern, one level down the stack: instead of FaaS nodes wired by HTTP, stream operators are wired by partitioned logs with exactly-once (or effectively-once — see [[exactly-once-semantics]]) delivery guarantees. For high-throughput pipelines the stream-processing form wins on throughput, fault tolerance, and ordering. For low-throughput, evolutionarily-volatile pipelines with heterogeneous participants, the FaaS form wins on development speed and participant diversity.

## Relationship to the saga pattern

A [[saga]] is an event pipeline that happens to need compensation semantics for multi-step distributed transactions. The topology is similar; the difference is that sagas carefully model success and failure branches so that partial completion can be rolled back. Burns's CI pipeline is already close to a choreographed saga without the compensation machinery.

## Relationship to CDC and event sourcing

[[change-data-capture]] and [[event-sourcing]] are common *sources* of the events that drive pipelines. A database commit becomes a CDC event, which becomes the trigger for a FaaS pipeline that emails customers, updates search indexes, and notifies downstream systems. Burns doesn't name the CDC/event-sourcing connection in Chapter 8, but it is the natural integration point on the data side.

## Relationship to event-driven batch (Chapter 11)

Burns's [[event-driven-batch-pattern|Chapter 11 event-driven batch pattern]] is the same idea at batch-workflow granularity: instead of per-event FaaS handlers wired by webhooks, entire [[work-queue-pattern|work queues]] are wired by pub/sub topics. Burns draws the parallel explicitly: "the operation of an event-driven batch processor is similar to event-driven FaaS" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Both share the *topology-as-specification* payoff — the diagram of nodes and edges is both the design document and the system. Both share the named-linking-patterns discipline: Chapter 11 gives the batch workflow its vocabulary ([[copier-pattern|copier]], [[filter-pattern|filter]], [[splitter-pattern|splitter]], [[sharder-pattern|sharder]], [[merger-pattern|merger]]) for readability, in exactly the spirit that Chapter 8's FaaS event pipelines benefit from named handlers.

The choice between the two is substrate. FaaS-wired pipelines suit low-volume, interactive, heterogeneous workflows (humans approving Jira tickets, external SaaS firing webhooks). Batch-wired workflows suit throughput-oriented bulk processing (transcoding videos into four formats, running builds across thousands of repos). The pattern shape is shared.

## Coupling and cohesion

The event pipeline pattern trades one kind of coupling for another. Pipeline nodes are loosely coupled at the **implementation** level — each function is small, stateless, independently deployable. But they are tightly coupled at the **contract** level — if the context payload changes shape, every downstream node can break. Schema evolution discipline ([[backward-forward-compatibility]], [[schema-evolution]]) applies to webhook payloads just as much as to message-broker messages. See [[message-brokers]] for the schema-compatibility discussion in the async-messaging context.

## Related pages

- [[functions-as-a-service]]
- [[faas-decorator-pattern]]
- [[serverless-vs-event-driven]]
- [[event-driven-batch-pattern]]
- [[event-streams]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[stream-processing]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[saga]]
- [[microservices]]
- [[independent-deployability]]
- [[coupling]]
- [[cohesion]]
- [[backward-forward-compatibility]]
- [[designing-distributed-systems]]
