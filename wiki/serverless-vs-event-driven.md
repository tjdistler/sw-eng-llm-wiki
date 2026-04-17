# Serverless vs Event-Driven

**Summary**: Burns's explicit terminological distinction at the opening of Chapter 8. "Serverless" and "event-driven" are two separate axes that FaaS happens to combine; products can sit on either axis without the other, and picking the right tool requires knowing which axis you actually need.

**Sources**: `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Last updated**: 2026-04-16

---

## The two axes

Burns opens Chapter 8 on this point because FaaS products are often described as "serverless" as if the two terms were synonymous, and they are not (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- **Serverless** — you don't see the servers. The platform provisions, scales, patches, and retires them. The developer deploys code, not infrastructure.
- **Event-driven** — execution is triggered by discrete events rather than handled by a long-running process. Functions are instantiated per event; there is no continuous serving loop.

FaaS products like AWS Lambda, Google Cloud Functions, and Azure Functions sit on both axes — serverless and event-driven. But there are meaningful products at every corner of the matrix.

## The four corners

|  | Event-driven | Not event-driven |
|---|---|---|
| **Serverless** | Managed FaaS (Lambda, Cloud Functions) | Multi-tenant container-as-a-service (Cloud Run, Fargate) |
| **Not serverless** | Self-hosted FaaS on your own cluster (Kubeless, OpenFaaS on Kubernetes) | Traditional servers on hardware you operate |

Burns calls out the two off-diagonal corners explicitly (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- **Serverless but not event-driven**: "a multi-tenant container orchestrator (container-as-a-service) is serverless but not event-driven." You get "someone else operates the servers" without the per-event lifecycle.
- **Event-driven but not serverless**: "an open-source FaaS running on a cluster of physical machines that you own and administer is event-driven but not serverless." You get the function-per-event programming model without giving up control of the underlying cluster.

## Why the distinction matters

Because the two axes produce different benefits, picking the wrong one wastes effort or leaves benefits on the table (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

- The **developer-productivity** and **operational-simplification** benefits of [[functions-as-a-service]] — "no artefact to create or push," automatic scaling, automatic fault recovery — come mostly from **serverlessness**.
- The **architectural constraints** of FaaS — short runtimes, stateless instances, pay-per-request billing, cold starts — come mostly from **event-drivenness**.

A team that wants the programming model but not the operational model can run an open-source FaaS on its own cluster, keeping the event-driven authoring style while paying VM prices. This is the escape hatch Burns recommends when request volume grows enough that per-request billing stops pencilling out: "one ideal way to scale FaaS is to run an open source FaaS that runs on a container orchestrator like Kubernetes."

Conversely, a team that wants the operations model but not the event-driven constraints — because its workload is long-running, stateful, or steady-state — should look at serverless container platforms, not FaaS.

## Practical implications

### Pricing

Serverless products generally bill per request or per resource-second of actual use. Non-serverless FaaS (open-source on your cluster) pays VM costs directly, which is cheaper at steady-state load but loses the "scales to zero" benefit.

### Limits

Event-driven platforms usually impose hard runtime limits, memory ceilings, and cold-start windows. Non-event-driven serverless platforms (Cloud Run-style) relax these — processes can be long-lived, hold memory, and serve many requests per instance.

### Observability

Both non-serverless options (self-hosted FaaS, traditional servers) give more direct access to the underlying nodes for debugging and profiling. Serverless platforms force reliance on whatever telemetry the platform exposes — which, as Burns notes elsewhere in the chapter, is a genuine operational challenge for distributed FaaS systems.

## Relationship to other patterns

[[functions-as-a-service]] is the pattern that sits in the serverless-AND-event-driven corner. [[running-too-many-things]] (Newman) argues the serverless axis is what makes FaaS attractive as a default choice on the public cloud. [[desired-state-management]] is delivered for free by both serverless corners of the matrix.

For teams on physical hardware, the event-driven-but-not-serverless corner — Kubeless, OpenFaaS, Knative on their own Kubernetes cluster — is the way to get FaaS's programming model without ceding operation of the cluster. Burns uses Kubeless for the Chapter 8 worked examples precisely because it lets readers reproduce the patterns on a local cluster.

## Related pages

- [[functions-as-a-service]]
- [[faas-decorator-pattern]]
- [[event-pipeline-pattern]]
- [[running-too-many-things]]
- [[desired-state-management]]
- [[designing-distributed-systems]]
