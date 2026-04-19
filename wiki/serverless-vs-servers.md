# Serverless vs Servers

**Summary**: Chapter 4's framing of the compute-deployment trade-off for data systems. **Serverless** (FaaS, serverless OLAP, container-as-a-service) removes infrastructure operations but gets expensive at steady-state scale. **Servers** — including containers on orchestrators — give customisation, power, and control. Use serverless first; move to servers-with-containers when you outgrow it.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What serverless is, in Chapter 4's framing

Chapter 4 (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Serverless provides a quick time to value for the right use cases.

Many flavours exist:

- **[[functions-as-a-service|Function as a Service (FaaS)]]** — AWS Lambda (2014) kicked off the current wave. Execute small chunks of code on demand, no server management.
- **Serverless query/OLAP** — Google BigQuery scales to zero and up automatically; you pay for data consumed per query plus a small storage cost.
- **Container-as-a-service** — AWS Fargate, Google Cloud Run, Google App Engine run containers without managing a compute cluster.

The payment model — **pay for consumption and storage** — is spreading across cloud services.

## When serverless makes sense

Chapter 4 lists the tests (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Workload size and complexity.** Simple, discrete tasks. Not suitable for many moving parts or heavy compute/memory needs.
- **Execution frequency and duration.** Cloud serverless platforms have limits on frequency, concurrency, and duration.
- **Requests and networking.** Serverless platforms use simplified networking; may not support all VPC/firewall features.
- **Language.** Serverless runtimes support specific languages. Outside the list, look at containers.
- **Runtime limitations.** Not a full OS abstraction — a specific runtime image.
- **Cost.** Convenient but potentially expensive at scale.

## The cost warning

Chapter 4's most concrete advice on serverless economics (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Serverless functions suffer from an inherent overhead inefficiency. Handling one event per function call at a high event rate can be catastrophically expensive.

The discipline: **monitor cost per event** in a real-world environment, then **model worst-case scenarios** (bot swarms, DDoS) that drive the bill.

## When to run your own servers

Chapter 4 names three broad reasons (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Cost.** At a certain scale, the economics of serverless diminish and running servers is cheaper.
- **Customisation, power, control.** Serverless frameworks can be underpowered or limited.
- **Workload shape.** Long-running, stateful, or steady-state workloads don't fit the event-per-invocation model.

### If you run your own servers, Chapter 4's rules

- **Expect servers to fail.** Don't create "special snowflake" servers. Treat them as ephemeral — boot scripts or images + CI/CD for code delivery.
- **Use clusters and autoscaling.** Take advantage of cloud ability to scale compute on demand.
- **Treat infrastructure as code.** Terraform, CloudFormation, Deployment Manager.
- **Use [[containers|containers]].** For sophisticated workloads with complex dependencies.

## [[containers|Containers]] as the middle path

Chapter 4 describes containers as "one of the most powerful trending operational technologies" (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- Lightweight VMs — wrap isolated user space (filesystem, processes) but share the host kernel.
- Dependency and code isolation without full-VM overhead.
- Many containers on a single host with fine-grained resource allocation.
- Partial solution to the [[distributed-monolith]] problem — each job can have its own isolated dependencies (Hadoop now supports this).

**Kubernetes** is "a kind of serverless environment" in that developers and ops deploy microservices without worrying about the underlying machines. Kubernetes is widely available as a managed service.

### Container security caveat

Chapter 4 is explicit (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Container clusters do not provide the same security and isolation that full VMs offer. Container escape — broadly, a class of exploits whereby code in a container gains privileges outside the container at the OS level — is common enough to be considered a risk for multitenancy.

EC2 is a truly multitenant VM environment. A Kubernetes cluster should host code only within **an environment of mutual trust** — e.g., inside one company's walls. Code review and vulnerability scanning are critical.

Hybrid offerings exist: **containerised function platforms** run containers as ephemeral units triggered by events (Lambda-style but with container flexibility). **AWS Fargate, Google App Engine** run containers without cluster management and provide isolation against multitenancy risks.

## Chapter 4's advice

> In the end, abstraction tends to win. We suggest looking at using serverless first and then servers — with containers and orchestration if possible — once you've outgrown serverless options. (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md)

Progression:

1. **Start serverless.** Fastest to first deploy, lowest operational burden.
2. **Move to containers on a managed orchestrator** when workloads outgrow serverless limits.
3. **Own the cluster** only when you need the control and have the operational depth.

## Cross-book framing

- [[functions-as-a-service]] (Burns) — the full pattern; cold starts, decorator patterns, offset management, batch.
- [[serverless-vs-event-driven]] (Burns) — the two axes FaaS combines that Chapter 4 does not explicitly separate.
- [[container-management-system]] (Google/Borg/Kubernetes lineage) — the operational substrate for container-based serverless.
- [[elasticity]] — what serverless automates.

## Related pages

- [[functions-as-a-service]]
- [[serverless-vs-event-driven]]
- [[containers]]
- [[container-management-system]]
- [[distributed-monolith]]
- [[monolith-vs-modular-data]]
- [[infrastructure-as-code]]
- [[elasticity]]
- [[finops]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
