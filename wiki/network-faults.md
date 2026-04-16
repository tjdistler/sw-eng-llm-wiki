# Network Faults

**Summary**: Network problems are surprisingly common even in controlled datacenter environments, and software must be designed to handle them -- whether by tolerating faults or by showing clear error messages until recovery.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## Prevalence in practice

Despite decades of building computer networks, network faults remain common (source: designing-data-intensive-applications, chapter 8):

- One study of a medium-sized datacenter found about 12 network faults per month: half disconnected a single machine, half disconnected an entire rack.
- Another study found that adding redundant networking gear doesn't reduce faults as much as expected, because **human error** (e.g., misconfigured switches) is a major cause of outages.
- Public cloud services like EC2 are notorious for frequent transient network glitches.
- A software upgrade for a switch can trigger a network topology reconfiguration, delaying packets for more than a minute.
- Sharks have bitten undersea cables and damaged them.
- A network interface may drop all inbound packets while sending outbound packets successfully -- a link working in one direction doesn't guarantee the reverse.

## Network partitions

When one part of the network is cut off from the rest due to a network fault, it is called a **network partition** (or netsplit). The book uses the more general term "network fault" to avoid confusion with partitions (shards) of a storage system. (source: designing-data-intensive-applications, chapter 8)

## Detecting faults

Many systems need to automatically detect faulty nodes -- load balancers need to remove dead nodes from rotation, and [[leader-based-replication]] systems need to trigger [[failover]] when the leader fails. The uncertainty of the network makes this difficult. (source: designing-data-intensive-applications, chapter 8)

Some specific feedback mechanisms exist:

- **TCP RST/FIN**: if the node's OS is running but no process is listening, the OS sends a reset or close packet. But if the node crashed mid-request, you don't know what was processed.
- **Process crash notification**: if the OS is still running, a script can notify other nodes immediately (e.g., HBase does this).
- **Hardware-level link detection**: network switch management interfaces can detect link failures, but only if accessible.
- **ICMP Destination Unreachable**: a router may report unreachability, but routers are subject to the same network limitations.

None of these are reliable in general. Even TCP acknowledgment only means the packet was delivered, not that the application handled it. If you want certainty, you need a **positive response from the application itself**. In the general case, you must fall back to [[timeouts]]. (source: designing-data-intensive-applications, chapter 8)

## Handling network faults

Handling faults doesn't necessarily mean tolerating them. If the network is normally reliable, showing an error message to users during problems may be a valid approach. But you must know how your software reacts and ensure it can recover. (source: designing-data-intensive-applications, chapter 8)

If error handling is not defined and tested, arbitrarily bad things can happen: deadlocks, permanent inability to serve requests, or even data deletion. Deliberate fault injection (as in Chaos Monkey) is recommended to verify behavior. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[unreliable-networks]]
- [[timeouts]]
- [[partial-failures]]
- [[fault-tolerance]]
- [[failover]]
- [[leader-based-replication]]
