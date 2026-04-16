# System Models

**Summary**: Formal abstractions that describe what faults a distributed algorithm may assume can occur -- combining timing assumptions (synchronous, partially synchronous, asynchronous) with node failure models (crash-stop, crash-recovery, Byzantine) to enable correctness proofs.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## Why system models exist

Distributed algorithms need to tolerate the faults described throughout Chapter 8 ([[unreliable-networks]], [[unreliable-clocks]], [[process-pauses]]). To be useful, algorithms must not depend heavily on specific hardware or software configurations. System models formalize the kinds of faults that can occur, enabling algorithms to be proved correct under those assumptions. (source: designing-data-intensive-applications, chapter 8)

## Timing models

Three system models describe timing assumptions (source: designing-data-intensive-applications, chapter 8):

### Synchronous model

Assumes **bounded** network delay, process pauses, and clock error. You know that delays will never exceed some fixed upper bound. This does not mean zero delay or perfect synchronization -- just known limits. **Not realistic for most practical systems**, because unbounded delays and pauses do occur.

### Partially synchronous model

The system behaves like a synchronous system **most of the time**, but sometimes exceeds the bounds for network delay, process pauses, and clock drift. When this happens, delay and error may become arbitrarily large. **This is the most realistic model for most systems**: things usually work well, but any timing assumption can occasionally be violated.

### Asynchronous model

The algorithm cannot make **any** timing assumptions -- it doesn't even have a clock, so it cannot use [[timeouts]]. Very restrictive; some algorithms can be designed for it, but most practical systems do not operate under this model.

## Node failure models

Three models describe how nodes can fail (source: designing-data-intensive-applications, chapter 8):

### Crash-stop faults

A node can only fail by crashing. Once it stops responding, it is gone forever and never comes back.

### Crash-recovery faults

Nodes may crash and later start responding again after some unknown time. Nodes have **stable storage** (disk) that survives crashes, but in-memory state is lost. **Most practical systems use this model.**

### Byzantine (arbitrary) faults

Nodes may do absolutely anything, including lying, sending contradictory messages, or actively trying to subvert the system. See [[byzantine-faults]].

## The most useful combination

For modeling real systems, the **partially synchronous model with crash-recovery faults** is generally the most useful. (source: designing-data-intensive-applications, chapter 8)

## Correctness of algorithms

An algorithm is correct in a system model if it always satisfies its properties in all situations the model assumes may occur. Properties are described formally. For example, a fencing token algorithm might require (source: designing-data-intensive-applications, chapter 8):

- **Uniqueness**: no two requests return the same token value
- **Monotonic sequence**: if request x completes before request y begins, x's token is less than y's
- **Availability**: a non-crashed node that requests a token eventually receives a response

See [[safety-and-liveness]] for how these properties are classified.

## Mapping models to reality

System models are simplified abstractions. Real implementations must handle cases the model assumes away (source: designing-data-intensive-applications, chapter 8):

- Crash-recovery models assume stable storage survives crashes, but disk data can be corrupted, wiped by hardware errors, or lost to firmware bugs.
- [[quorums]] rely on nodes remembering stored data. If a node suffers amnesia (data loss), the quorum condition breaks.
- Even when an algorithm is proven correct, its implementation may need code for "impossible" cases -- sometimes just logging an error and exiting for a human to handle.

Theoretical analysis and empirical testing are equally important. Proofs uncover problems that might remain hidden in real systems for a long time, surfacing only when timing assumptions are violated under unusual circumstances. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[safety-and-liveness]]
- [[partial-failures]]
- [[byzantine-faults]]
- [[unreliable-networks]]
- [[unreliable-clocks]]
- [[process-pauses]]
- [[quorums]]
- [[fault-tolerance]]
