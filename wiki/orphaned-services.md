# Orphaned Services

**Summary**: Microservices that have been running for months or years without changes, where no team currently takes ownership. They're often working fine — until they aren't, and nobody knows what to do. The remedy is a service registry (or equivalent) and disciplined re-assignment of ownership when orphans are discovered.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The shape of the problem

As microservices become more focused, more of them happily run for long stretches without changes. That's actually one of the goals — [[independent-deployability]] is appealing partly because the rest of the system stays stable when one part doesn't need to change (source: chapter-05-growing-pains.md).

The downside: with no changes comes no ownership, no recent context, no working knowledge. Newman:

> "I refer to these services as orphaned services, as fundamentally no one in the company is taking ownership or responsibility for them." (source: chapter-05-growing-pains.md)

The fundamental problem is that when an orphaned service *does* break, or does need to change, no one knows what to do.

## The "walled-up servers" anecdote

Newman recounts hearing (perhaps apocryphal) stories of old servers being discovered walled up in old offices — still running, still doing whatever they did, but no one remembered why. Microservices can exhibit the same thing. He's spoken to teams that didn't even know where the source code for an orphaned service lived (source: chapter-05-growing-pains.md).

## When this happens

Typically in organisations that have been running microservices for a long time — long enough that collective memory has faded. The original implementers have forgotten the details or left the company (source: chapter-05-growing-pains.md).

## Mitigations

### Practise collective ownership

Newman offers an *untested hypothesis* (source: chapter-05-growing-pains.md): organisations practising [[code-ownership-models|collective ownership]] may be less prone to orphan problems, because they've already had to invest in mechanisms that let any developer move between services and make changes. Restricted language and technology choices, common tooling for build/test/deploy — all reduce the cost of picking up an unfamiliar service.

The caveat: if those common practices have *changed* since the orphan was last touched, even collective ownership may not save you.

### Build a service registry

Several companies Newman has spoken to created in-house registries to collate metadata about their services (source: chapter-05-growing-pains.md). Some crawl source-code repositories looking for metadata files; the resulting catalogue can be merged with real runtime data from systems like consul or etcd to build a richer picture.

### The Financial Times Biz Ops example

The most developed example Newman cites (source: chapter-05-growing-pains.md). FT has hundreds of services across teams worldwide. **Biz Ops** — built on a graph database for flexibility — gives them one place to find information about microservices, networks, file servers, and other infrastructure.

Biz Ops goes further than most: it computes a **System Operability Score** for each service. The score reflects whether the service has provided correct registry information, has proper health checks, and so on. Teams can see at a glance what needs fixing. It's a feedback loop that incentivises keeping a service "well-tended" — and surfaces the ones that aren't.

### Re-assign ownership when orphans are discovered

If your orphans predate your registry, the registry won't have caught them. The remedy is to bring the discovered orphan into line with how other services are managed (source: chapter-05-growing-pains.md):

- Under **strong ownership**: assign the orphan to an existing team.
- Under **collective ownership**: raise work items for the service to be improved to whatever current standards are.

## Why this is more than tidiness

An orphan that "just works" today is a latent risk — when it breaks, the team responding to the incident has no priors. Combined with the slow loss of organisational memory, this is how systems quietly become unmaintainable. The Chapter 5 framing is that microservices reward stability with neglect, and you need explicit mechanisms to push back against that.

## Connection to other Chapter 5 topics

- **[[code-ownership-models]]** — Newman's hypothesis is that the model influences orphan-likelihood.
- **[[desired-state-management]]** — runtime visibility platforms like Kubernetes provide one source of "what's currently running" data that registries can pull from.
- **[[monitoring-and-observability]]** — observability tools see the calls into orphaned services even when humans don't; useful as an additional data source.

## Related pages

- [[code-ownership-models]]
- [[independent-deployability]]
- [[desired-state-management]]
- [[service-discovery]]
- [[monitoring-and-observability]]
