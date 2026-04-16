# Two-Phase Commit (2PC)

**Summary**: An algorithm for achieving atomic transaction commit across multiple nodes, ensuring either all nodes commit or all abort -- the most common protocol for [[distributed-transactions]], but vulnerable to blocking if the coordinator fails. Newman's blunt advice for microservices: "just say no" — use [[saga|sagas]] instead.

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## 2PC is not 2PL

Two-phase commit (2PC) and [[two-phase-locking]] (2PL) are completely different algorithms despite the similar names. 2PC provides atomic commit in distributed databases; 2PL provides serializable isolation. (source: designing-data-intensive-applications, chapter 9)

## How it works

2PC introduces a **coordinator** (transaction manager) that is not present in single-node transactions. The protocol has two phases (source: designing-data-intensive-applications, chapter 9):

**Phase 1 -- Prepare**: The coordinator sends a prepare request to each participant node, asking "can you commit?"

**Phase 2 -- Commit/Abort**: 
- If ALL participants reply "yes," the coordinator sends a commit request to all.
- If ANY participant replies "no," the coordinator sends an abort request to all.

## The system of promises

The protocol works through two irrevocable points of no return (source: designing-data-intensive-applications, chapter 9):

1. **Participant votes "yes"**: the participant promises it can definitely commit later. It has written all transaction data to disk and checked for constraint violations. It surrenders the right to abort unilaterally.
2. **Coordinator decides**: the coordinator writes its commit/abort decision to its transaction log on disk (the **commit point**). This decision is irrevocable and must be enforced regardless of subsequent failures.

Detailed flow:
1. Application requests a globally unique transaction ID from the coordinator.
2. Application performs reads/writes on each participant, attaching the transaction ID.
3. Coordinator sends prepare requests tagged with the transaction ID.
4. Participants verify they can commit (write data to disk, check constraints) and reply yes/no.
5. Coordinator writes its decision to its local transaction log (the commit point).
6. Coordinator sends commit/abort to all participants, retrying forever if needed.

## Coordinator failure

The critical weakness of 2PC: if the coordinator crashes after participants have voted "yes" but before sending the commit/abort decision, participants are stuck **in doubt** (uncertain). They cannot safely commit (another participant might have aborted) or abort (another might have committed). They must wait for the coordinator to recover. (source: designing-data-intensive-applications, chapter 9)

While in doubt, participants **hold their locks** (row-level exclusive locks, shared locks for 2PL). If the coordinator takes 20 minutes to restart, those locks are held for 20 minutes. If the coordinator's log is lost, locks may be held forever until an administrator manually resolves each transaction. (source: designing-data-intensive-applications, chapter 9)

## Three-phase commit (3PC)

An alternative called 3PC has been proposed that avoids blocking. However, 3PC assumes bounded network delays and bounded response times. In real systems with unbounded delays and process pauses, 3PC cannot guarantee atomicity. Nonblocking atomic commit requires a **perfect failure detector**, which is impossible with unbounded network delays. For this reason, 2PC continues to be used in practice. (source: designing-data-intensive-applications, chapter 9)

## 2PC as a consensus algorithm

2PC is technically a consensus algorithm, but not a fault-tolerant one: it does not satisfy the termination property because it can block indefinitely waiting for a crashed coordinator. This is why better [[consensus]] algorithms (Paxos, Raft, Zab) were developed -- they require only majority votes rather than unanimity, and include recovery mechanisms for leader/coordinator changes. (source: designing-data-intensive-applications, chapter 9)

## Newman's view from microservice migrations

Sam Newman frames 2PC as something teams reach for when extracting microservices from a monolith and discovering they've broken a transaction boundary. His advice: don't. (source: chapter-04-decomposing-the-database.md)

The main operational reasons he highlights from the microservice perspective (source: chapter-04-decomposing-the-database.md):

- **Lost isolation.** The coordinator can't make all participants commit at the same instant — there's always a window where one participant has applied the change and another hasn't. The ACID `I` is gone in any practical sense.
- **Locks held across the network.** Each participant must lock its local resource between phase 1 and phase 2. The wider the latency, the longer the locks; deadlock-management at this scale is, in Newman's words, "not pretty."
- **Failure modes that need humans.** A worker that voted "yes" then disappears can leave the system in a state that requires manual unpicking. The more participants, the more such failure modes.

Newman's recommendation, "Distributed Transactions — Just Say No": (source: chapter-04-decomposing-the-database.md)

> "If you have pieces of state that you want to manage in a truly atomic and consistent way, and you cannot work out how to sensibly get these characteristics without an ACID-style transaction, then leave that state in a single database, and leave the functionality that manages that state in a single service (or in your monolith)."

If atomicity across services really *is* required, model the operation as a [[saga]] instead — a sequence of local transactions with compensating actions, not distributed locks.

## Related pages

- [[distributed-transactions]]
- [[saga]]
- [[consensus]]
- [[two-phase-locking]]
- [[transactions]]
- [[acid]]
- [[fault-tolerance]]
- [[zookeeper]]
- [[database-decomposition]]
