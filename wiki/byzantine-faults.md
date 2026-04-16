# Byzantine Faults

**Summary**: A class of fault where a node may "lie" -- sending arbitrary, faulty, or corrupted responses -- making consensus far harder to achieve. Relevant in adversarial environments (blockchains, aerospace), but generally not a concern in typical datacenter systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## Definition

A Byzantine fault occurs when a node sends arbitrary faulty or corrupted responses -- it may claim to have received a message it didn't, or send contradictory information to different nodes. This is distinct from the more common **crash faults** where a node simply stops responding. (source: designing-data-intensive-applications, chapter 8)

The problem of reaching consensus in an environment where nodes may lie is known as the **Byzantine Generals Problem**. It is a generalization of the Two Generals Problem (two armies coordinating over an unreliable channel), extended to include traitors among the generals who may send fake or contradictory messages. (source: designing-data-intensive-applications, chapter 8)

A system is **Byzantine fault-tolerant** if it continues to operate correctly even when some nodes are malfunctioning or malicious attackers are interfering. (source: designing-data-intensive-applications, chapter 8)

## Where Byzantine fault tolerance matters

- **Aerospace**: radiation can corrupt memory or CPU registers, causing a computer to respond unpredictably. Flight control systems must tolerate this because failure is catastrophic.
- **Multi-organization systems**: where participants may attempt to cheat or defraud others. Peer-to-peer networks like Bitcoin use Byzantine fault tolerance to reach agreement without a central authority.

## Where it doesn't matter (most server-side systems)

In typical datacenter systems, all nodes are controlled by one organization and can be trusted. Radiation levels are low enough that memory corruption is not a major concern. Byzantine fault-tolerant protocols are complex and expensive, making them impractical for most server-side data systems. (source: designing-data-intensive-applications, chapter 8)

Web applications must expect arbitrary client behavior, but this is handled by input validation, sanitization, and making the server the authority -- not by Byzantine fault-tolerant protocols. (source: designing-data-intensive-applications, chapter 8)

## Limitations

Most Byzantine fault-tolerant algorithms require a **supermajority of more than two-thirds** of nodes to be functioning correctly (e.g., at most 1 of 4 nodes may malfunction). (source: designing-data-intensive-applications, chapter 8)

Against software bugs, this only helps if you have multiple independent implementations of the same software -- unlikely in practice. Against security compromises, if an attacker compromises one node, they can probably compromise all nodes running the same software. Traditional security mechanisms (authentication, access control, encryption, firewalls) remain the primary defense. (source: designing-data-intensive-applications, chapter 8)

## Weak forms of lying

Even without full Byzantine fault tolerance, it is worth guarding against weak forms of incorrect messages (source: designing-data-intensive-applications, chapter 8):

- **Network corruption**: packets sometimes evade TCP/UDP checksums. Application-level checksums provide additional protection.
- **Input validation**: publicly accessible services must sanitize user input (range checks, size limits) to prevent denial of service.
- **Multiple NTP servers**: NTP clients contact multiple servers and exclude outliers, making synchronization robust against individual misconfigured servers.

## Assumptions in this book

The book assumes **non-Byzantine faults**: nodes are unreliable but honest. They may be slow, unresponsive, or outdated, but if they respond, they tell the truth to the best of their knowledge. [[fencing-tokens]] can detect nodes inadvertently acting in error (e.g., not knowing their lease expired), but they cannot stop a deliberately malicious node. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[fencing-tokens]]
- [[truth-and-leadership-in-distributed-systems]]
- [[partial-failures]]
- [[system-models]]
- [[fault-tolerance]]
