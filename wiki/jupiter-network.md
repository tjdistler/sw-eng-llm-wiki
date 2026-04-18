# Jupiter Network

**Summary**: Google's intra-datacenter network fabric — a Clos network of hundreds of Google-built switches acting together as one very fast virtual switch with tens of thousands of ports. At its largest, Jupiter supports 1.3 Pbps of bisection bandwidth among servers.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## The problem

Machines within a Google datacenter need to communicate with each other at very high aggregate bandwidth. No single commodity switch has enough ports, so Google constructs an equivalent using many smaller switches wired together as a **Clos network fabric** (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## The solution

Jupiter is the name of the resulting fabric (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- Built from hundreds of Google-designed switches.
- Acts as a single virtual switch with tens of thousands of ports.
- Supplies up to 1.3 Pbps of bisection bandwidth in its largest configuration.

The design choice pairs with [[software-defined-networking]]: Jupiter's switches are comparatively simple ("dumb" switching components), while centralised controllers pre-compute best paths. The expensive routing decisions are moved off the switch hardware.

## Relationship to B4

Jupiter handles traffic **inside** a datacenter. The [[b4-network|B4]] backbone handles traffic **between** datacenters. The two are the intra- and inter-datacenter halves of Google's network stack (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Related pages

- [[b4-network]]
- [[software-defined-networking]]
- [[google-datacenter-topology]]
- [[site-reliability-engineering]]
