# Google Datacenter Topology

**Summary**: Google's physical infrastructure hierarchy — machine, rack, row, cluster, datacenter building, campus — plus the deliberate terminology split between **machine** (hardware) and **server** (software that implements a service). The vocabulary is used throughout the SRE book.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## Machine vs server

Google deliberately separates two meanings that the industry usually conflates (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- **Machine** — a piece of hardware (or a VM).
- **Server** — a piece of software that implements a service.

Any machine can run any server; there is no dedicated "mail server machine." Allocation is handled by [[borg]]. This split is unusual but load-bearing: once tasks are fluidly bin-packed over machines, "the mail server" as a hardware entity stops making sense.

## Physical hierarchy

From smallest to largest (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

| Level | Content |
|---|---|
| Machine | Individual compute unit |
| Rack | Tens of machines |
| Row | A line of racks |
| Cluster | One or more rows |
| Datacenter building | Multiple clusters |
| Campus | Multiple nearby datacenter buildings |

A rack matters as a failure domain: the top-of-rack switch is a single point of failure for every machine in it, so [[borg]] refuses to place all of a job's tasks on one rack.

## Homogeneous hardware

Unlike typical colocation datacenters, Google-designed datacenters use **the same compute hardware across the board** (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). The chapter's footnote qualifies this ("roughly the same. Mostly. Except for the stuff that is different"), but the deliberate homogeneity is what makes [[borg]]-style fluid task placement tractable.

## Networking within and between datacenters

- Within a datacenter, machines talk through the [[jupiter-network]] — a Clos-fabric virtual switch with tens of thousands of ports, built from Google-designed switches.
- Datacenters connect to each other through the [[b4-network]] — a [[software-defined-networking|software-defined]] backbone using OpenFlow.

See those pages for the networking details.

## Related pages

- [[borg]]
- [[jupiter-network]]
- [[b4-network]]
- [[software-defined-networking]]
- [[gslb]]
- [[site-reliability-engineering]]
