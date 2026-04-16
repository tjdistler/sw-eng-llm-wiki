# Leader-Based Replication

**Summary**: A replication architecture where one node (the leader) accepts all writes and propagates changes to followers; also called master–slave or active/passive replication.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## How it works

1. One replica is designated the **leader** (master, primary). All writes go here first.
2. The leader writes the change to its local storage and sends it to all **followers** (replicas, secondaries, slaves, hot standbys) via a replication log or change stream.
3. Each follower applies changes in the same order the leader processed them.
4. Reads can be served by the leader or any follower; writes are leader-only.

This is the default model in PostgreSQL (≥9.0), MySQL, Oracle Data Guard, SQL Server AlwaysOn, MongoDB, RethinkDB, Kafka, and RabbitMQ highly-available queues.

## Synchronous vs asynchronous replication

**Synchronous**: the leader waits for the follower to acknowledge before reporting success to the client.
- Advantage: the follower is guaranteed to have consistent data; if the leader fails, the data is still on the follower.
- Disadvantage: if the follower is slow or unavailable, *all* writes are blocked.

**Semi-synchronous**: one follower is synchronous, the rest asynchronous. Guarantees at least two up-to-date copies (leader + one follower). The standard practical compromise.

**Fully asynchronous**: the leader doesn't wait for any follower. Writes are never blocked, but if the leader fails before replication completes, those writes are lost — even if acknowledged to the client.

## Replication log methods

Four approaches for propagating changes from leader to followers:

**Statement-based replication**: the leader forwards every SQL statement (`INSERT`, `UPDATE`, `DELETE`) to followers, which re-execute it. Simple and compact, but breaks with nondeterministic functions (`NOW()`, `RAND()`), autoincrement, or triggers. Used in early MySQL; mostly superseded.

**WAL shipping**: the leader ships its write-ahead log to followers, which build an identical storage structure. Used in PostgreSQL and Oracle. Disadvantage: the log is storage-engine-specific — different versions of the database cannot run on leader and follower simultaneously, requiring downtime for upgrades.

**Logical (row-based) log replication**: a separate log format, decoupled from the storage engine, recording changes at the row level (new values for inserts, primary key + new values for updates, primary key for deletes). Used in MySQL binlog row mode. Allows leader and follower to run different software versions; also enables **change data capture** for streaming data to external systems.

**Trigger-based replication**: application-level replication using database triggers to write changes to a separate table, read by an external process. More flexible (subset replication, cross-database replication) but higher overhead, more error-prone.

## Setting up new followers

Followers can be added without downtime using a snapshot-and-catch-up process:
1. Take a consistent snapshot of the leader (without locking, if possible).
2. Copy the snapshot to the new follower.
3. The follower requests all changes since the snapshot's position in the replication log (PostgreSQL calls this the *log sequence number*; MySQL calls it *binlog coordinates*).
4. Once the follower has caught up, it processes the live change stream.

## Handling node outages

**Follower failure**: each follower keeps a log of changes received. On restart, it reconnects to the leader and requests any changes it missed since its last processed position.

**Leader failure**: requires [[failover]]. One follower must be promoted to leader, clients reconfigured, and other followers pointed at the new leader.

## Linearizability and consensus

Single-leader replication is **potentially linearizable**: if reads go to the leader or synchronously updated followers, the system can provide [[linearizability]]. However, this is not guaranteed -- snapshot isolation or concurrency bugs can violate it, and a node that incorrectly believes it is the leader will serve stale data. Asynchronous replication means [[failover]] may lose committed writes, violating both durability and linearizability. (source: designing-data-intensive-applications, chapter 9)

The replication log in single-leader replication effectively implements [[total-order-broadcast]] -- all followers process the same writes in the same order ([[state-machine-replication]]). However, choosing and maintaining the leader requires [[consensus]]. If the leader is manually configured, the system cannot make progress automatically when the leader fails. Automatic leader election requires a consensus algorithm (Raft, Zab, Paxos), typically provided by tools like [[zookeeper]] or etcd. (source: designing-data-intensive-applications, chapter 9)

Partitioning a single-leader database (one leader per partition) does not affect linearizability, since linearizability is a single-object guarantee. Cross-partition consistency requires [[distributed-transactions]]. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[replication]]
- [[failover]]
- [[replication-lag]]
- [[multi-leader-replication]]
- [[linearizability]]
- [[consensus]]
- [[total-order-broadcast]]
- [[state-machine-replication]]
- [[zookeeper]]
