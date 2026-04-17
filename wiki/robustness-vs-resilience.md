# Robustness vs Resilience

**Summary**: A distinction from David Woods's resilience engineering (via John Allspaw): robustness is reacting to expected variations; resilience is adapting to the unforeseen. Microservices can enable robustness, but resilience is an organisational property — not something an architecture grants you.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The distinction

> *Robustness* is the ability to have a system that is able to react to expected variations.
>
> *Resilience* is having an organisation capable of adapting to things that haven't been thought of, which could well include creating a culture of experimentation through things like chaos engineering.
>
> — John Allspaw, paraphrased (source: chapter-02-planning-a-migration.md)

The framing is from David Woods's resilience engineering literature, which separates how systems handle **known** sources of failure from how they handle **unknown** ones.

## A worked example

Knowing that a specific machine could die, you load-balance instances behind a proxy. That is **robustness** — addressing a known failure mode (source: chapter-02-planning-a-migration.md).

Preparing the organisation for the fact that it cannot anticipate every potential problem — running game days, exercising recovery procedures, fostering a culture where engineers practise their response under failure — is **resilience**.

## Microservices give you neither for free

A common confusion is to assume that breaking a system into services magically makes it more reliable. Newman pushes back hard (source: chapter-02-planning-a-migration.md):

- Microservices **open up opportunities** to design for tolerance of network partitions, service outages, and the like.
- They **do not guarantee** improved robustness. Spreading functionality across processes and machines just as easily *increases* the failure surface.

Robustness has to be designed in. Resilience has to be built into the organisation's culture and practices — it cannot be a property of the deployment topology alone.

## Cheaper alternatives for robustness

Before concluding microservices are required for robustness, consider (source: chapter-02-planning-a-migration.md):

- Run multiple copies of the [[monolith]] behind a load balancer or queue.
- Distribute instances across **failure planes** (different racks, different data centres).
- Invest in more reliable hardware and software.
- Audit existing causes of outages — Newman has seen many production issues caused by manual processes or "people not following protocol". The British Airways 2017 outage that grounded all Heathrow and Gatwick flights was reportedly triggered by a single individual's actions during a power-related procedure.

> "If the robustness of your application relies on human beings never making a mistake, you're in for a rocky ride." (source: chapter-02-planning-a-migration.md)

## Operationalising the distinction at scale

Chapter 5 returns to this theme in the [[robustness-and-resiliency-at-scale|robustness and resiliency]] section. The robustness side gets concrete patterns — time-outs, circuit breakers, isolation, multiple instances, [[desired-state-management]]. The resilience side stays organisational (source: chapter-05-growing-pains.md):

> "It's about a whole way of working — building an organization that not only is ready to handle the unforeseeable problems that will inevitably crop up, but also evolves working practices as necessary."

Newman highlights one specific resilience habit: **document production issues when they arise and keep a record of what you learned**. Organisations move on too quickly after the immediate problem is solved, only to encounter the same issue months later (source: chapter-05-growing-pains.md).

## Connection to existing concepts

The robustness/resilience distinction layers cleanly on top of [[fault-tolerance|fault tolerance]] from Kleppmann: techniques like redundancy, replication, and quorums are robustness mechanisms. The organisational practices that surround them — chaos engineering, blameless post-mortems, runbook rehearsals — are resilience mechanisms.

## Related pages

- [[why-microservices]]
- [[fault-tolerance]]
- [[reliability]]
- [[microservices]]
- [[robustness-and-resiliency-at-scale]]
- [[desired-state-management]]
- [[circuit-breaker]]
- [[bulkhead]]
