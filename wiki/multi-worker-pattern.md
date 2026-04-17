# Multi-Worker Pattern

**Summary**: A refinement of Burns's [[work-queue-pattern|work queue]] in which a single worker slot is implemented as a **composition of several smaller worker containers** rather than one bespoke image. An aggregator container implements the standard [[worker-container-interface]] outward and dispatches to a series of reusable processing containers inward. Burns treats this as a specialization of the [[adapter-pattern]]: the aggregator adapts a group of heterogeneous workers into the single worker interface the queue-manager expects.

**Sources**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## The motivating example

Burns's illustration is an image pipeline with three distinct steps (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

1. Detect faces in the image.
2. Tag each face with identities.
3. Blur the faces.

The naive implementation is a single bespoke worker container that does all three. The cost is that the container is **not reusable** — if next month you want to detect *cars* and blur them, you must build a second bespoke worker that duplicates the blurring logic.

The multi-worker fix: build each processing step as its own narrow container (face detector, identity tagger, face blurrer), and compose them behind an **aggregator** container that presents a single worker interface to the queue-manager (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). Reusing the blurring container for a different detector is now a composition change, not a rewrite.

## The aggregator shape

The aggregator container runs coresident with a collection of processing containers in the same worker pod:

- The aggregator receives the work item via the [[worker-container-interface|file-based worker interface]] from the queue-manager.
- The aggregator invokes each processing container in sequence (or in a configured DAG), passing intermediate outputs between them.
- The aggregator reports success/failure outward as a single unit.

Structurally, the worker pod becomes a miniature processing pipeline — one aggregator plus N processing containers — that looks like a single worker from the queue-manager's perspective (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

## Why Burns calls this a specialization of the adapter pattern

Burns's framing: "the multiworker pattern transforms a collection of different worker containers into a single unified container that implements the worker interface, yet delegates the actual work to a collection of different, reusable containers" (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

That is the [[adapter-pattern]] shape — the aggregator takes a heterogeneous inward interface (several different processing containers, each with its own native API) and presents a standard outward interface (the one-shot, file-based [[worker-container-interface]] the queue-manager expects). The inward complexity is hidden; the outward shape is uniform.

Compare with the Part I adapter uses:

| Adapter use | Inward | Outward |
|---|---|---|
| [[unified-monitoring-interface]] | Redis INFO, MySQL status, JMX, syslog | One Prometheus endpoint |
| [[log-normalization]] | Per-application log formats | One fluentd/stdout stream |
| [[health-check-adapter]] | Application-specific diagnostics | One HTTP health probe |
| Multi-worker aggregator (this page) | Several processing containers with their own APIs | One worker-interface file-based invocation |

The mechanical shape is the same; what's adapted differs.

## Why the code reuse matters

Burns's broader argument throughout the book is that containers are the new unit of library reuse: a well-designed container with a documented API can be dropped into many deployments the way a function library is imported into many programs (see [[modular-reusable-containers]]). The multi-worker pattern applies that discipline specifically to batch pipelines — each processing step becomes a published container with a known interface, and composing a new pipeline is a deployment-description change rather than a code change (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

This is particularly valuable for the image/video/audio processing space the chapter draws from, because:

- The component operations (detect, classify, extract, transform, encode) are genuinely reusable across many applications.
- They are often implemented by community-maintained tools (OpenCV, ffmpeg, TensorFlow image models).
- Wrapping each as a narrow container means the contributor does not need to know what pipeline it will be used in.

## Relationship to wiki concepts

### Adapter pattern

See [[adapter-pattern]] for the general pattern. The multi-worker is one specific application — the "adapted" thing is a **set** of containers rather than a single application's heterogeneous interface, but the transformation is the same shape.

### Sidecar and ambassador in the worker pod

The aggregator and processing containers sit inside one [[pod]], using the same shared-namespace substrate that underlies [[sidecar-pattern]] and [[ambassador-pattern]]. Depending on how data flows, each processing container might look like a sidecar (augmenting the aggregator's behaviour) or an ambassador (proxying the aggregator's outbound calls to a model-serving endpoint). The multi-worker pattern is less about which Part I pattern applies inside and more about what the worker pod looks like from outside — a single worker, per the [[worker-container-interface]].

### Dataflow engines

The multi-worker pod is structurally a very small [[dataflow-engines|dataflow DAG]] — a chain of processing operators with an orchestrator. For fine-grained compositions across huge data the right answer is a real dataflow engine (Spark, Flink); for coarse-grained, per-item pipelines where each item is independent, the multi-worker pod is lighter-weight and operationally simpler.

### MapReduce

A [[mapreduce]] pipeline's map-side composition (chaining several per-record transformations before the shuffle) is conceptually equivalent to the multi-worker pattern. Burns's contribution is to express the same idea at container granularity with a clear interface contract.

### Merger pattern (Chapter 11)

Burns's [[merger-pattern]] from Chapter 11 applies the same multi-source adapter shape to the *source* side of the work queue rather than the worker side (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Where the multi-worker aggregator composes many **processing** containers behind one worker interface, the merger composes many **source** containers behind one source interface. Structurally they are mirror images — compose-multiple-inward, present-one-outward — and Burns names both as adapter-pattern specialisations.

### FaaS event pipelines

The [[event-pipeline-pattern]] solves a similar composition problem on FaaS substrate — a directed graph of functions connected by webhooks. The multi-worker pattern is the container-based, per-work-item equivalent: one worker pod contains the whole chain for one item. The event pipeline is better when each step is bursty and event-shaped; the multi-worker is better when all steps process every item and resource profiles are predictable.

## Related pages

- [[work-queue-pattern]]
- [[worker-container-interface]]
- [[adapter-pattern]]
- [[modular-reusable-containers]]
- [[pod]]
- [[dataflow-engines]]
- [[mapreduce]]
- [[event-pipeline-pattern]]
- [[event-driven-batch-pattern]]
- [[merger-pattern]]
- [[designing-distributed-systems]]
