# B4 Network

**Summary**: Google's globe-spanning backbone network connecting its datacenters. B4 is a [[software-defined-networking|software-defined]] architecture using the OpenFlow open-standard protocol. It supplies massive bandwidth to a modest number of sites and uses **elastic bandwidth allocation** to maximise average bandwidth.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## What B4 does

B4 is the wide-area network that connects Google datacenters to each other. Three defining properties (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- **Software-defined** — routing decisions are made by centralised controllers, not by the switches themselves.
- **OpenFlow-based** — uses the open-standard communications protocol between controllers and forwarding hardware.
- **Elastic bandwidth allocation** — capacity is reallocated across flows to maximise average utilisation, rather than statically partitioned.

## Why centralisation works here

A modest number of sites (datacenters) and very high bandwidth between them is a regime where central planning beats distributed routing. The chapter is explicit: "centralized traffic engineering has been shown to solve a number of problems that are traditionally extremely difficult to solve through a combination of distributed routing and traffic engineering" (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## BwE: the enforcement companion

Inside any given flow, Google enforces a per-task bandwidth budget with the **Bandwidth Enforcer (BwE)**, analogous to [[borg]]'s compute-quota enforcement but for network bandwidth. BwE manages available bandwidth to maximise average availability (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Relationship to Jupiter

B4 is the inter-datacenter counterpart of the intra-datacenter [[jupiter-network]]. Together they form Google's two-tier network: Jupiter inside each building; B4 between them (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Related pages

- [[jupiter-network]]
- [[software-defined-networking]]
- [[google-datacenter-topology]]
- [[site-reliability-engineering]]
