# Adapter Pattern

**Summary**: A single-node multi-container pattern in which an **adapter container** transforms the interface an application container exposes so that it conforms to a predefined interface expected of all applications in the environment (monitoring, logging, health checks, etc.). The application itself is unchanged; the adapter wraps whatever heterogeneous interface the app happens to have in a homogeneous one that generic tooling can rely on.

**Sources**: `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`, `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

The adapter is the third and final single-node pattern in Burns's catalogue, completing the Part I trilogy alongside the [[sidecar-pattern]] and [[ambassador-pattern]]. All three share the same substrate: two coscheduled containers in a [[pod]], shared namespaces, `localhost` communication. They differ by intent (source: raw/designing-distributed-systems/chapter-04-adapters.md):

- **Sidecar** — augments the application's *own behaviour* (TLS termination, config reloads, introspection).
- **Ambassador** — brokers the application's *outbound* connections (sharding, service discovery, request splitting).
- **Adapter** — transforms the *interface the application presents to the outside world* so it matches a uniform standard the ecosystem expects.

Burns's framing: real systems are heterogeneous — code you wrote, code your vendors wrote, off-the-shelf open source and proprietary binaries, spread across many languages with many conventions for logging, monitoring, and health. To effectively operate this zoo, you need *common interfaces*. Rather than rewrite each application to emit the standard format, drop an adapter container in front of it that translates whatever interface the app happens to present into the one the ecosystem expects (source: raw/designing-distributed-systems/chapter-04-adapters.md).

The chapter motto, roughly: "different application containers can present many different monitoring interfaces while the adapter container adapts this heterogeneity to present a consistent interface" (source: raw/designing-distributed-systems/chapter-04-adapters.md).

## Why the pattern is valuable

Burns offers several arguments that mirror, but sharpen, the sidecar case (source: raw/designing-distributed-systems/chapter-04-adapters.md):

1. **Decoupled release cycles.** Rolling out a new version of the application doesn't require a rollout of the adapter, and vice versa. The monitoring adapter can be maintained and versioned by the monitoring team; the application team owns the application.
2. **Reuse across applications.** One adapter container — say, a Redis-to-Prometheus exporter — can be used anywhere Redis is deployed. This is the [[modular-reusable-containers]] benefit applied to the interface-conformance problem.
3. **Third-party authorship.** The adapter "may even have been supplied by the monitoring system maintainers independent of the application developers." The community can supply adapters you never have to write.
4. **Dedicated resources.** The adapter gets its own CPU and memory quota; a misbehaving monitoring adapter "cannot cause problems with a user-facing service" (source: raw/designing-distributed-systems/chapter-04-adapters.md).
5. **Avoids modifying third-party images.** Building a slightly-modified image of someone else's container (to add metrics or health checks) means inheriting the burden of patching, rebasing, and chasing upstream releases forever. The adapter pattern sidesteps this entirely.

## The three canonical applications

Chapter 4 is organised around three concrete applications of the adapter pattern, each covered in its own page.

### 1. Monitoring

Every application in a fleet should expose metrics in one format so a single tool can scrape them all. Applications in reality emit metrics in many formats — syslog, ETW, JMX, proprietary protocols, push and pull styles. An adapter container translates the app's native interface into the common one (Prometheus, in the chapter's worked example). See [[unified-monitoring-interface]].

### 2. Logging

Applications log to different files at different levels in different structured formats. The operational expectation is that all logs reach stdout in a consistent structured shape that the log aggregator can parse. An adapter redirects files to stdout and normalises the format. Worked example: `fluentd` with `fluent-plugin-redis-slowlog` to extract Redis's `SLOWLOG` command output into a queryable stream. See [[log-normalization]].

### 3. Health checking

Container orchestrators want a uniform health-check endpoint (typically an HTTP probe). Off-the-shelf database and server images don't usually expose rich, application-specific health checks. An adapter container runs arbitrary diagnostic queries against the application and exposes their result via the standard probe endpoint. Worked example: a Go adapter that runs a workload-representative SQL query against a sibling MySQL container. See [[health-check-adapter]].

All three share the same mechanical shape: the application's native, heterogeneous interface faces inward into the pod; the adapter presents the fleet-standard interface outward.

## Why not just modify the application?

Burns anticipates this question. If you own the application, modifying it to emit the standard interface is defensible — and possibly cleaner. But in practice (source: raw/designing-distributed-systems/chapter-04-adapters.md):

- You usually don't own every container in a real deployment. Redis, MySQL, nginx, Kafka — these are images someone else maintains.
- Forking third-party images to add a metrics endpoint or health check creates a maintenance debt: every upstream release forces a rebase.
- In-process code for emitting metrics or logs becomes one more piece of boilerplate duplicated in every language the fleet uses.
- Decoupling into a separate adapter container "allows for the possibility of sharing and reuse, which isn't possible when you modify the application container."

The adapter pattern trades some fit (an in-process implementation would be more tailored) for much more leverage (one container, many applications, contributed by the wider community).

## The community angle

Burns closes the chapter with an unusually broad claim: "sometimes design patterns aren't just for the developers who apply them, but lead to the development of communities that can collaborate and share solutions between members of the community as well as the broader developer ecosystem" (source: raw/designing-distributed-systems/chapter-04-adapters.md).

The adapter pattern is structurally friendly to ecosystem contribution: adapters are small, narrow, single-purpose containers with well-defined inputs (a third-party application's native interface) and outputs (the fleet-standard interface). That's exactly the shape that makes open-source contribution work — you don't need to know how to health-check MySQL to *use* a published MySQL health-check adapter. The pattern is a mechanism for embedding other people's expertise into your deployment.

## Relationship to existing wiki concepts

### Adapters and the single-node pattern trilogy

The adapter rounds out the Part I trilogy:

| Pattern | Intent | Typical content |
|---|---|---|
| [[sidecar-pattern]] | Augment the application's own behaviour | nginx HTTPS termination, config sync, `topz` introspection |
| [[ambassador-pattern]] | Broker the application's outbound / backend connections | twemproxy sharding, service-broker probes, nginx split 10% |
| Adapter (this page) | Transform the application's outward interface to match a standard | Prometheus exporter, fluentd log normalizer, HTTP health-check wrapper |

The line is not always crisp — an Envoy instance in a [[service-mesh]] does a bit of all three — but at the pattern-catalogue level the three are distinct tools for distinct problems.

### Adapters and information hiding

Adapters are [[information-hiding]] at the operations layer. The application's native interface — Redis's INFO output, MySQL's status tables, a Java server's JMX endpoint — is an implementation detail, hidden inside the pod. What the rest of the infrastructure sees is the fleet-standard interface the adapter presents. The application remains free to change its internals as long as the adapter continues to produce the standard external shape.

### Adapters and legacy modernization

[[legacy-modernization]] via sidecars (Chapter 2) and via adapters (Chapter 4) are two sides of the same coin. Sidecars commonly handle the inbound side — adding HTTPS or dynamic config. Adapters commonly handle the outbound-observation side — adding metrics, logs, health checks. Both let you bring a legacy application into a modern deployment standard without touching its source.

### Adapters and the service mesh

A [[service-mesh]]'s data-plane proxy mostly plays sidecar and ambassador roles, but the telemetry it emits — standardised request metrics, access logs, traces — has an adapter flavour: the mesh presents a common observability interface regardless of what each application does internally. In practice, a production deployment often combines a mesh proxy for traffic concerns with dedicated adapter containers for application-specific observability.

### Adapters and modular reusable containers

Because adapters are by design used across many applications (any Redis, any MySQL, any Java server exposing JMX), they benefit especially strongly from the design discipline in [[modular-reusable-containers]]: parameterize them, define their API surface (parameters, emitted format, observable files and endpoints), and document them. Most real adapter containers are configured by environment variables and command-line flags for exactly this reason.

### Adapters and batch worker composition

Burns's [[work-queue-pattern|Chapter 10]] treats the [[multi-worker-pattern]] as a specialisation of the adapter pattern: an aggregator container exposes the single [[worker-container-interface]] the queue-manager expects outward, while delegating inward to a composition of reusable processing containers (face-detect, identity-tag, blur) (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). The adapter's job is to transform a heterogeneous inward interface (several processing containers with their own APIs) into the single uniform outward interface — the same mechanical shape as the monitoring, logging, and health-check adapters, now applied to batch pipeline composition.

Chapter 11 extends the use: every [[event-driven-batch-pattern|event-driven batch]] linking pattern — [[copier-pattern|copier]], [[filter-pattern|filter]], [[splitter-pattern|splitter]], [[sharder-pattern|sharder]], [[merger-pattern|merger]] — is an adapter at the seam between work queues (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Burns is especially explicit for the merger: "the merger is another great example of the adapter pattern, though in this case, the adapter is actually adapting multiple running source containers into a single merged source." The same observation applies with variations to every other linking primitive — batch workflow wiring is adapters all the way down.

### Adapters vs FaaS decorators

Burns revisits the adapter pattern in Chapter 8 when introducing the [[faas-decorator-pattern]]: a FaaS decorator does the same structural job as an adapter container — transform a request or response without modifying the backend — but scales independently of the backend rather than being coscheduled with it (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

Burns's rule of thumb: use an **adapter container** when the transformation should scale in lockstep with the application (monitoring, logs, health checks are always one-per-pod), and a **FaaS decorator** when the transformation should scale on its own axis — especially when it is much lighter than the backend or when you want to experiment with it cheaply. See [[faas-decorator-pattern]] for the full treatment.

### Adapters, monitoring, and log aggregation

[[monitoring-and-observability]] requires that every application expose metrics in some consistent shape. The adapter pattern is the container-level mechanism for satisfying that requirement without rewriting everything. [[log-aggregation]] has the same structure: normalise log formats on the way out so the central aggregator can index them uniformly. The three chapter examples map directly onto the observability toolbox Newman describes.

## Design discipline for adapters

Like sidecars and ambassadors, adapters should be designed as reusable modules. The three-part discipline from [[modular-reusable-containers]] applies (source: raw/designing-distributed-systems/chapter-04-adapters.md implicitly via modularity arguments; explicit in Chapter 2):

1. **Parameterize** — the application's listening port, the query to run, the metrics endpoint path, credentials, etc.
2. **Define the API surface** — the inbound metrics/logs/health endpoints the adapter exposes to the rest of the fleet; the application protocol the adapter speaks inward; any shared-filesystem conventions.
3. **Document** — so others in the ecosystem can use the adapter without deep knowledge of the application it fronts.

## Related pages

- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[pod]]
- [[modular-reusable-containers]]
- [[unified-monitoring-interface]]
- [[log-normalization]]
- [[health-check-adapter]]
- [[monitoring-and-observability]]
- [[log-aggregation]]
- [[information-hiding]]
- [[legacy-modernization]]
- [[service-mesh]]
- [[faas-decorator-pattern]]
- [[functions-as-a-service]]
- [[multi-worker-pattern]]
- [[work-queue-pattern]]
- [[event-driven-batch-pattern]]
- [[merger-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[splitter-pattern]]
- [[sharder-pattern]]
- [[designing-distributed-systems]]
