# Partial Failures

**Summary**: In a distributed system, some parts may be broken while others work fine, creating nondeterministic failures that are fundamentally different from the all-or-nothing behavior of a single computer.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## The single-computer model vs distributed reality

A single computer with good software is usually either fully functional or entirely broken. This is a deliberate design choice: if an internal fault occurs, the computer crashes completely rather than returning wrong results, because wrong results are difficult to deal with. CPUs, memory, and disk present an idealized model of mathematical perfection on top of fuzzy physical reality. (source: designing-data-intensive-applications, chapter 8)

In a distributed system, this idealized model breaks down. Some parts of the system may be broken in unpredictable ways while other parts work fine. This is a **partial failure**. The difficulty is that partial failures are **nondeterministic**: the same operation may work sometimes and fail other times. You may not even know whether something succeeded, because network message delivery times are themselves nondeterministic. (source: designing-data-intensive-applications, chapter 8)

## Cloud computing vs supercomputing

There is a spectrum of approaches to handling faults in large-scale systems (source: designing-data-intensive-applications, chapter 8):

- **Supercomputers (HPC)**: deal with partial failure by escalating it into total failure. The entire cluster is stopped, the faulty node is repaired, and computation restarts from the last checkpoint. This is viable because HPC jobs are offline batch workloads.
- **Cloud computing / internet services**: must handle partial failures gracefully because they serve users online with low latency requirements. Making the service unavailable for repair is not acceptable.
- **Traditional enterprise datacenters**: lie somewhere between these extremes.

Key differences that make internet services harder (source: designing-data-intensive-applications, chapter 8):

- Nodes are commodity hardware with higher failure rates
- Networks are IP/Ethernet (packet-switched, not circuit-switched)
- In a system with thousands of nodes, something is always broken
- Geographically distributed deployments must use the unreliable internet
- Rolling upgrades require the system to tolerate node-level failures

## The engineering response

If we want distributed systems to work, we must accept partial failures and build [[fault-tolerance]] mechanisms into the software. We need to build reliable systems from unreliable components. (source: designing-data-intensive-applications, chapter 8)

This is an old idea in computing: IP is unreliable, but TCP provides reliable transport on top of it. Error-correcting codes transmit data accurately over noisy channels. The more reliable higher-level system is not perfect, but it handles tricky low-level faults so the remaining faults are easier to reason about. (source: designing-data-intensive-applications, chapter 8)

There is always a limit to how much more reliable the system can be than its parts. TCP can hide packet loss but cannot remove network delays. The goal is to make the system reliable *enough* for its purpose. (source: designing-data-intensive-applications, chapter 8)

## Suspicion, pessimism, and paranoia

Even in small systems, it is important to consider a wide range of possible faults and to artificially create them in testing environments. It would be unwise to assume faults are rare and simply hope for the best. In distributed systems, suspicion, pessimism, and paranoia pay off. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[fault-tolerance]]
- [[reliability]]
- [[unreliable-networks]]
- [[unreliable-clocks]]
- [[process-pauses]]
- [[system-models]]
