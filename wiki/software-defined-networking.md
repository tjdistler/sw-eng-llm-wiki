# Software-Defined Networking (SDN)

**Summary**: An architecture that moves routing decisions off the switching hardware and into centralised controllers. Switches become "dumb" high-throughput forwarders; controllers (often duplicated for availability) pre-compute paths and push them down. OpenFlow is the open standard Google uses for this. SDN underpins both [[jupiter-network|Jupiter]] (intra-datacenter) and [[b4-network|B4]] (inter-datacenter).

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## The split

In a traditional network, each switch runs routing logic itself — peer with neighbours, run OSPF/BGP, compute a forwarding table locally. In an SDN, that logic is lifted out:

- **Data plane** — the switches forward packets as directed. No routing intelligence.
- **Control plane** — a central (typically duplicated) controller computes best paths across the whole network and programs the switches.

The communication between the two is done over a standardised protocol; Google uses OpenFlow (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Why Google uses it

Two reasons from the chapter (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. **Cost**. "Smart" routing hardware is expensive; centralising the computation lets Google use "less expensive 'dumb' switching components."
2. **Traffic engineering**. Problems that are hard to solve via distributed routing ([[b4-network|B4]]'s elastic bandwidth allocation being the example) are tractable when a single controller sees the whole graph.

## Where it shows up at Google

- [[jupiter-network]] — SDN inside a datacenter.
- [[b4-network]] — SDN across datacenters.
- **Bandwidth Enforcer (BwE)** — the per-task bandwidth quota system, analogous to [[borg]] for compute.

## Related pages

- [[jupiter-network]]
- [[b4-network]]
- [[google-datacenter-topology]]
- [[site-reliability-engineering]]
