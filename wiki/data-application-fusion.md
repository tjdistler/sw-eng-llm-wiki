# Data-Application Fusion

**Summary**: Reis and Housley's prediction that the application layer and the data layer will merge — "application stacks will be data stacks, and vice versa." In the [[live-data-stack]] world, applications emit real-time events, streaming pipelines react, ML models respond, and the results flow back into the application. The result: much shorter feedback loops between users, data, and intelligent behaviour.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The prediction

Chapter 11 calls this "the next revolution" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

> Right now, applications sit in one area, and the MDS sits in another. To make matters worse, data is created with no regard for how it will be used for analytics. Consequently, lots of duct tape is needed to make systems talk with one another. This patchwork, siloed setup is awkward and ungainly. Soon, application stacks will be data stacks, and vice versa.

Applications will integrate real-time automation and decision-making powered by streaming pipelines and ML. The [[data-engineering-lifecycle]] stages don't disappear; the time between them collapses.

## What changes technically

Three specific technical shifts the chapter highlights (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Mixed OLTP/OLAP databases** — a new class of database designed to serve application transactions and analytical workloads against the same storage. Chapter 11 flags this as "emerging database technologies designed to address the mix of OLTP and OLAP use cases."
- **[[feature-store|Feature stores]]** — the analogous substrate for ML use cases, making real-time features available both to training and to live inference.
- **Streaming pipelines embedded in application architecture** — see [[stream-processing]], [[event-driven-architecture]].

## What changes organisationally

- The "throw it over the wall" pattern between application teams and data teams dies. See [[titles-will-morph]].
- [[software-engineering-for-data|Software engineers]] learn streaming, pipelines, modeling, and quality.
- [[data-engineer|Data engineers]] embed into application teams instead of sitting in a parallel org.
- Events become a first-class design artifact, not an afterthought.

## The tight application/ML feedback loop

The chapter pairs data-application fusion with a second, closely related prediction: the **tight feedback loop between applications and ML** (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

> ML is well-suited for scenarios where data is generated at such a high rate and volume that humans cannot feasibly process it by hand. As data sizes and velocity grow, this applies to every scenario. As data feedback loops become shorter, we expect most applications to integrate ML.

The sequence: application emits events → stream processors transform → models infer in real time → application uses inference to shape the next interaction → the user generates more events. Each turn of the loop sharpens the model and improves the experience. This is what makes TikTok, Uber, and DoorDash feel like magic.

## Why it's the logical end of the MDS decoupling

The [[modern-data-stack]] is fundamentally about **decoupling**: separate the application DB from the warehouse, separate ingestion from transformation, separate analytics from operations. Data-application fusion is the re-coupling of those layers — not as a regression, but because streaming makes it possible to re-couple without losing independence (the glue is an event log, not a synchronous call graph). See [[loose-coupling]] for the underlying principle.

## Cross-book resonance

- **[[unbundling-databases]]** (DDIA Ch 12) — Kleppmann's vision of decomposing the database into event logs, derived indexes, and stream operators. Data-application fusion is the organisational face of this technical decomposition.
- **[[event-driven-architecture]]** — the general pattern. Data-application fusion is EDA with ML and analytics bolted in.
- **[[event-driven-microservices]]** (Bellemare) — the microservices version of the same vision. In data-application fusion, streams are the integration layer not only between microservices but between services and analytical/ML subsystems.
- **Reads as events** (DDIA Ch 12, see [[stream-processing]]) — Kleppmann's related prediction that even read queries can be represented as events, which would collapse the last remaining wall between applications and the data plane.

## Related pages

- [[future-of-data-engineering]]
- [[live-data-stack]]
- [[titles-will-morph]]
- [[stream-transform-load]]
- [[real-time-olap]]
- [[feature-store]]
- [[model-drift]]
- [[stream-processing]]
- [[event-driven-architecture]]
- [[event-driven-microservices]]
- [[unbundling-databases]]
- [[modern-data-stack]]
- [[loose-coupling]]
- [[software-engineering-for-data]]
