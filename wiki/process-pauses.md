# Process Pauses

**Summary**: A node in a distributed system can be paused for an arbitrary length of time -- due to garbage collection, VM suspension, disk I/O, or OS scheduling -- without realizing it, creating a dangerous window during which other nodes may take over its responsibilities.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## The lease problem

Consider a database partition leader that holds a **lease** (a lock with a timeout) to prove it is still the leader. The leader must periodically renew the lease. The danger: if the leader's thread is paused for longer than the lease duration, the lease expires, another node becomes leader, but the paused node resumes and still believes it holds the lease. It may then process requests unsafely, corrupting data. (source: designing-data-intensive-applications, chapter 8)

There is nothing to tell the paused thread how long it was paused. From its perspective, hardly any time has passed. This is why relying on local time checks between obtaining a lease and using it is unsafe -- the pause can happen at any point. (source: designing-data-intensive-applications, chapter 8)

## Causes of process pauses

Burns's *Designing Distributed Systems* Chapter 9 adds one more concrete scenario that matters at the container level: "imagine that the original lock holder becomes so overwhelmed that its processor stops running for minutes at a time. This can happen on extremely overscheduled machines." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md) CPU starvation on a noisy-neighbour node produces the same indistinguishable-from-dead effect as a GC pause, and it is the failure mode ownership-election mitigations (resource versions, server-side owner validation) are tuned for. See [[ownership-election-pattern]] and [[distributed-locks-on-kv-stores]].

All of these can preempt a running thread at any point and resume it later without the thread noticing (source: designing-data-intensive-applications, chapter 8):

- **Garbage collection (GC)**: "stop-the-world" GC pauses can last several minutes. Even "concurrent" collectors like HotSpot JVM's CMS must stop the world occasionally.
- **Virtual machine suspension**: a VM can be suspended (state saved to disk) and resumed at any time, for arbitrary durations. This is used for live migration between hosts.
- **Laptop suspend/resume**: execution may be paused when a user closes the laptop lid.
- **OS context switching**: when the OS or hypervisor switches to another thread or VM, the current thread is paused. Under heavy load, it may take a long time before the paused thread runs again. Time spent in other VMs is called **steal time**.
- **Synchronous disk I/O**: a thread may block on a slow disk operation. In Java, class loading can trigger unexpected disk access at any time. If the disk is a network filesystem (e.g., Amazon EBS), I/O latency includes [[unreliable-networks|network delay variability]].
- **Memory paging (swap)**: if the OS swaps to disk, a memory access may trigger a page fault requiring slow disk I/O. Under memory pressure, excessive paging (**thrashing**) can stall the system. Server machines often disable swap to avoid this.
- **Unix signals**: SIGSTOP pauses a process until SIGCONT is received. An accidental Ctrl-Z by an operator can pause a critical process.

## Analogy to thread safety

The problem is similar to multi-threaded programming on a single machine: you cannot assume anything about timing because arbitrary context switches may occur. However, the tools for single-machine thread safety (mutexes, semaphores, atomic counters, lock-free data structures) do not translate to distributed systems, which have no shared memory -- only messages over an [[unreliable-networks|unreliable network]]. (source: designing-data-intensive-applications, chapter 8)

A node must assume its execution can be paused for a significant length of time at any point. During the pause, other nodes may declare it dead and reassign its responsibilities. When the node resumes, it may not realize it was paused until it checks its clock. (source: designing-data-intensive-applications, chapter 8)

## Real-time systems

Some systems (aircraft, rockets, cars) have **hard real-time** requirements: the software must respond within a specified deadline or the entire system fails. Providing real-time guarantees requires (source: designing-data-intensive-applications, chapter 8):

- A real-time operating system (RTOS) with guaranteed CPU time allocation
- Library functions with documented worst-case execution times
- Restricted or no dynamic memory allocation
- Extensive testing and measurement

Real-time systems are very expensive to develop and may have lower throughput. For most server-side data processing, real-time guarantees are not economical. (source: designing-data-intensive-applications, chapter 8)

## Mitigating GC pauses

Without full real-time guarantees, GC impact can be reduced (source: designing-data-intensive-applications, chapter 8):

- **Treat GC pauses as planned outages**: when a node needs GC, stop sending it requests, let it drain, perform GC, then resume. Some financial trading systems use this.
- **Use GC only for short-lived objects** and periodically restart processes before they accumulate enough long-lived objects to require a full GC. Restart nodes one at a time, shifting traffic away first (like a rolling upgrade).

These measures reduce but do not eliminate the impact of pauses.

## Related pages

- [[partial-failures]]
- [[unreliable-clocks]]
- [[unreliable-networks]]
- [[timeouts]]
- [[fencing-tokens]]
- [[failover]]
