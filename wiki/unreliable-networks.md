# Unreliable Networks

**Summary**: The distributed systems in this book are shared-nothing systems that communicate over asynchronous packet networks, which provide no guarantees about message delivery or timing -- creating fundamental ambiguity about remote node state.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## Shared-nothing architecture

The distributed systems discussed here are **shared-nothing**: each machine has its own memory and disk, and the network is the only way machines can communicate. This approach dominates internet services because it is cheap (commodity hardware), leverages cloud computing, and achieves high [[reliability]] through geographic redundancy. (source: designing-data-intensive-applications, chapter 8)

## Asynchronous packet networks

The internet and most datacenter networks (Ethernet) are **asynchronous packet networks**. A node can send a packet to another node, but the network gives no guarantees about when -- or whether -- it will arrive. (source: designing-data-intensive-applications, chapter 8)

When you send a request and expect a response, many things can go wrong (source: designing-data-intensive-applications, chapter 8):

1. The request may have been lost (e.g., unplugged cable)
2. The request may be queued and delivered later (network or recipient overloaded)
3. The remote node may have failed (crashed or powered down)
4. The remote node may have temporarily stopped responding (e.g., GC pause) but will respond later
5. The remote node processed the request but the response was lost
6. The remote node processed the request but the response is delayed

**These cases are indistinguishable from the sender's perspective.** The only information you have is that you haven't received a response yet. The usual handling is a [[timeouts|timeout]]: after some time, give up waiting and assume the response won't arrive. But even after a timeout, you don't know whether the remote node processed your request. (source: designing-data-intensive-applications, chapter 8)

## Synchronous vs asynchronous networks

Traditional telephone networks are **synchronous**: they establish a circuit with a fixed, guaranteed amount of bandwidth, resulting in bounded delays and no queueing. (source: designing-data-intensive-applications, chapter 8)

Datacenter networks use **packet switching** instead because it is optimized for **bursty traffic**. A circuit is good for constant-bandwidth uses like audio calls, but requesting a web page or transferring a file has no particular bandwidth requirement -- you just want it done as quickly as possible. Packet switching dynamically adapts to available capacity, maximizing wire utilization at the cost of variable delays. (source: designing-data-intensive-applications, chapter 8)

Variable delays are a consequence of **dynamic resource partitioning**: bandwidth is shared among all senders rather than statically allocated. This is cheaper but means delays are unbounded. Quality of service (QoS) and admission control can emulate circuit switching on packet networks, but this is not currently enabled in multi-tenant datacenters or the public internet. (source: designing-data-intensive-applications, chapter 8)

## Network congestion and queueing

The variability of packet delays is most often due to queueing (source: designing-data-intensive-applications, chapter 8):

- **Switch queues**: multiple nodes sending to the same destination causes packets to queue at the network switch. If the queue fills, packets are dropped.
- **OS receive queues**: when all CPU cores are busy, incoming packets are queued by the OS until the application can handle them.
- **VM scheduling**: in virtualized environments, a VM may be paused while another uses the CPU, causing incoming data to be buffered by the virtual machine monitor.
- **TCP flow control**: TCP limits sending rate to avoid overloading the network or receiver, causing additional queueing at the sender.
- **TCP retransmission**: lost packets are retransmitted after a timeout, adding to observed delay even though the application doesn't see the packet loss directly.

Queueing delays have an especially wide range when a system is near maximum capacity. In shared environments (public clouds, multi-tenant datacenters), noisy neighbors can cause highly variable delays. (source: designing-data-intensive-applications, chapter 8)

## TCP vs UDP

Some latency-sensitive applications (videoconferencing, VoIP) use UDP instead of TCP. UDP does not perform flow control or retransmit lost packets, avoiding some sources of variable delay. This is a tradeoff: reliability vs delay variability. UDP is appropriate when delayed data is worthless -- e.g., in a phone call, there isn't time to retransmit a lost audio packet before it would have been played. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[partial-failures]]
- [[network-faults]]
- [[timeouts]]
- [[fault-tolerance]]
- [[process-pauses]]
