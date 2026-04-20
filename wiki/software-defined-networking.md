# Software-Defined Networking (SDN)

**Summary**: An architecture that moves routing decisions off the switching hardware and into centralised controllers. Switches become "dumb" high-throughput forwarders; controllers (often duplicated for availability) pre-compute paths and push them down. OpenFlow is the open standard Google uses for this. SDN underpins both Google's intra-datacenter Clos fabric and its inter-datacenter backbone.

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
2. **Traffic engineering**. Problems that are hard to solve via distributed routing (elastic bandwidth allocation across a WAN backbone, for example) are tractable when a single controller sees the whole graph.

## Where it shows up at Google

- SDN inside the datacenter (a Clos-fabric intra-datacenter switch).
- SDN across datacenters (the inter-datacenter software-defined backbone).
- **Bandwidth Enforcer (BwE)** — the per-task bandwidth quota system, analogous to [[borg]] for compute.

## Related pages

- [[google-datacenter-topology]]
- [[site-reliability-engineering]]
