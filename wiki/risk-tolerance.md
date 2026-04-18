# Risk Tolerance of Services

**Summary**: Every service has a different appropriate point on the risk continuum. Chapter 3 walks through how SREs identify that point — for consumer services (work with a product owner and weigh availability, failure shape, cost, and non-availability metrics) and for infrastructure services (partition by explicit service level so clients choose the reliability tier they need).

**Sources**: `raw/site-reliability-engineering/chapter-03-embracing-risk.md`

**Last updated**: 2026-04-17

---

## Why this is hard at Google

In safety-critical or formal environments, risk tolerance is baked into the product definition. At Google it usually isn't — so SREs must **work with product owners to turn business goals into explicit reliability objectives** that can actually be engineered against (source: chapter-03-embracing-risk.md).

Consumer services typically have a product team. Infrastructure services often do not, so the SRE team and the engineers building the system end up playing the product-owner role.

## Consumer service risk tolerance

For a consumer service, Chapter 3 names four factors to weigh:

### 1. Target level of availability

The appropriate target depends on the service's function and market position. Questions to ask (source: chapter-03-embracing-risk.md):

- What level of service will users expect?
- Does this tie directly to revenue — ours or our customers'?
- Is the service paid or free?
- What do competitors offer?
- Is it consumer-facing or enterprise-facing?

Two worked examples:

- **Google Apps for Work** — enterprise customers depend on Gmail/Calendar/Drive/Docs to run their businesses. An outage is an outage for every customer. Quarterly target: 99.9% externally, a stronger internal target, a contract with penalties for failing the external one.
- **YouTube (post-2006 acquisition)** — consumer-facing, growing rapidly, with a very different business lifecycle than Google's. The team set a **lower** availability target than Google's enterprise products because rapid feature development mattered correspondingly more.

The lesson: the right target is specific to the product's phase of life, not a corporate standard.

### 2. Types of failures

Absolute error count does not determine impact; the *shape* of the failure does. Chapter 3's illustrative examples:

- Contact-management service — intermittent profile-picture render failures versus a bug that shows one user's private contacts to another. Same error count can be catastrophically different; in the second case, **taking the service entirely down** during debug/clean-up is appropriate because private-data exposure destroys trust.
- Ads Frontend — used primarily during business hours, so occasional **scheduled maintenance windows** were acceptable and counted as *planned* downtime, not unplanned.

Two different questions the failure shape answers: how resilient is the business to full-site outages vs. constant low-rate failures? And are there failure classes so damaging that the right response is a deliberate takedown?

### 3. Cost

Cost is often the deciding factor. Ads is a good case because request successes and failures map directly to revenue:

> If we were to build and operate these systems at one more nine of availability, what would our incremental increase in revenue be? Does this additional revenue offset the cost of reaching that level of reliability?

Worked example from the chapter:

- Proposed improvement: 99.9% → 99.99%
- Increase in availability: 0.09%
- Service revenue: $1M
- Value of improved availability: $1M × 0.0009 = **$900**

If the cost to reach the extra nine is less than $900, do it. Otherwise don't.

When the revenue mapping isn't clean, a useful heuristic: **compare to the background error rate of ISPs on the Internet**, which Google measured at 0.01%–1% depending on ISP and protocol (source: chapter-03-embracing-risk.md). Once service errors drop below ISP background noise, further improvement is invisible to users.

### 4. Other service metrics

Availability is not the only dimension with a tolerance. Examining other metrics often reveals degrees of freedom for thoughtful risk-taking. The chapter's worked example is Ads latency:

- **AdWords** (ads next to search results) — latency invariant: ads must not slow down the search experience. This has driven engineering goals across every generation of AdWords.
- **AdSense** (contextual ads on publisher pages) — latency goal: don't slow down the publisher's page rendering. Because a given publisher's page already takes some hundreds of milliseconds to render, AdSense ads can be served **hundreds of milliseconds slower than AdWords ads**.

The looser AdSense latency requirement enabled smart provisioning trade-offs (fewer geographic locations, lower operational overhead, substantial cost savings). Identifying which metrics *don't* need to be tight is often as valuable as identifying which do.

## Infrastructure service risk tolerance

Infrastructure components differ fundamentally: **by definition they have multiple clients with different needs** (source: chapter-03-embracing-risk.md). The worked example in Chapter 3 is [[bigtable]]:

- Some consumer services serve user requests directly out of Bigtable — they need **low latency and high reliability**.
- Other teams use Bigtable as the data source for MapReduce-style offline analysis — they care more about **throughput** than either of the above.

The temptation is to engineer all infrastructure services to be ultra-reliable. Given the massive resource footprint of infrastructure, that's "far too expensive in practice" (source: chapter-03-embracing-risk.md).

### Observing the difference via request queues

A concrete lens on the conflict: the desired state of Bigtable's request queues.

- The low-latency user wants queues **(almost always) empty** so requests process immediately on arrival. Inefficient queuing is often the cause of high tail latency.
- The throughput user wants queues **never empty** so the system never idles waiting for work.

Success for one is failure for the other.

### Partition by service level

The resolution is to **partition the infrastructure and offer it at multiple independent levels of service** (source: chapter-03-embracing-risk.md). For Bigtable:

- **Low-latency clusters** — substantial slack capacity, short queues, strict client isolation, more redundancy.
- **Throughput clusters** — run hot, less redundancy, optimise throughput over latency. Cost can be as little as **10–50% of a low-latency cluster** at the same capacity.

Critically, this can be done with **identical hardware and software**; the differentiation is in resource quantity, redundancy, geographic provisioning, and infrastructure-software configuration.

### Externalising cost to the client

Explicitly delineated service levels let clients make their own cost/reliability trade-offs. Google+ might put user-privacy data in a high-availability globally consistent store ([[spanner]]) and put optional UX-enhancing data in a cheaper, eventually consistent store ([[bigtable]]). Exposing cost to the client is the mechanism that motivates them to pick the lowest-cost tier that still meets their needs.

### Frontend infrastructure

Not all infrastructure is storage. Google's frontend infrastructure (reverse proxies, load balancers near the network edge; see [[google-frontend]]) is engineered for extremely high reliability because **a request that never reaches the application frontend is simply lost** — there is no backend to gracefully handle the failure.

## The common thread

Consumer and infrastructure cases share a single principle: **the appropriate risk tolerance is discovered, not assumed**. For consumer services, you discover it by working with the product team. For infrastructure services, you discover it by cataloguing your clients' use cases and offering service tiers that match them.

Once discovered, the tolerance becomes an [[service-level-objective|SLO]], and the [[error-budget]] falls out of it.

## Related pages

- [[service-level-objective]]
- [[error-budget]]
- [[risk-management-sre]]
- [[availability-measurement]]
- [[reliability]]
- [[bigtable]]
- [[spanner]]
- [[google-frontend]]
