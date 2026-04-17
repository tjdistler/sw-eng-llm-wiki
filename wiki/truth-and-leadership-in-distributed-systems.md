# Truth and Leadership in Distributed Systems

**Summary**: A node in a distributed system cannot trust its own judgment -- truth is determined by quorum vote, and any node that believes it is "the chosen one" (leader, lock holder) must have that belief confirmed by the majority to act safely.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## A node cannot trust itself

A node in a network can only make guesses based on the messages it receives (or doesn't receive). It cannot know the true state of another node -- problems in the network are indistinguishable from problems at a node. (source: designing-data-intensive-applications, chapter 8)

Three scenarios illustrate why a node cannot rely on its own perception (source: designing-data-intensive-applications, chapter 8):

1. **Asymmetric network fault**: a node receives all messages but its outgoing messages are dropped. It is working perfectly, but other nodes declare it dead because they hear nothing back. The node cannot do anything about it.
2. **Semi-disconnection**: a node may notice its messages are not being acknowledged and realize there is a fault, but it is still wrongly declared dead by others.
3. **GC pause**: a node's threads are paused for a minute by garbage collection. Other nodes declare it dead. When GC finishes, the node resumes and doesn't realize it was ever paused.

## Quorum-based truth

A distributed system cannot rely on a single node, because that node may fail at any time. Instead, many distributed algorithms rely on a **[[quorums|quorum]]**: decisions require a minimum number of votes from several nodes. (source: designing-data-intensive-applications, chapter 8)

If a quorum declares a node dead, it must be considered dead, even if the node still feels alive. The individual node must abide by the quorum decision and step down. Most commonly, the quorum is an **absolute majority** (more than half the nodes). A majority allows the system to continue working with individual node failures, and there can only be one majority -- preventing conflicting decisions. (source: designing-data-intensive-applications, chapter 8)

## The leader and the lock

Many systems require there to be only one of something (source: designing-data-intensive-applications, chapter 8):

- Only one node is the leader for a database partition (to avoid split brain)
- Only one transaction or client holds the lock for a particular resource
- Only one user has registered a particular username

Even if a node believes it is "the chosen one," that doesn't mean a [[quorums|quorum]] agrees. A node may have formerly been the leader, but if other nodes declared it dead during a [[process-pauses|GC pause]] or network interruption, it may have been demoted without knowing it. If it continues acting as the leader, it can corrupt data. (source: designing-data-intensive-applications, chapter 8)

**Example (real-world HBase bug)**: a client obtains a lease/lock to get exclusive access to a file. The client is paused (e.g., GC). The lease expires. Another client obtains the lease and starts writing. The first client resumes, believes it still has the lease, and also writes. The file is corrupted. (source: designing-data-intensive-applications, chapter 8)

The solution to this problem is [[fencing-tokens]]. (source: designing-data-intensive-applications, chapter 8)

## Applied form at the container level

Burns's Chapter 9 on [[ownership-election-pattern|ownership election]] surfaces the same problem in the pattern idiom of containers and Kubernetes: "imagine that the original lock holder becomes so overwhelmed that its processor stops running for minutes at a time. This can happen on extremely overscheduled machines. In such a case, the lock will time out and some other replica will own the lock. Now the processor frees up the replica that was the original lock holder. Obviously, the handleLockLost() function will quickly be called, but there will be a brief period where the replica still believes it holds the lock." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

His mitigations — client-side self-check using `0.75 * ttl`, server-side owner validation at every worker request, and per-request resource versions — are the applied container-level form of the fencing-token solution. See [[distributed-locks-on-kv-stores]] for the construction and [[renewable-leases]] for the long-running ownership case.

## Related pages

- [[quorums]]
- [[fencing-tokens]]
- [[process-pauses]]
- [[partial-failures]]
- [[failover]]
- [[byzantine-faults]]
- [[ownership-election-pattern]]
- [[distributed-locks-on-kv-stores]]
- [[renewable-leases]]
