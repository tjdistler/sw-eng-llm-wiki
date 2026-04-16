# Fencing Tokens

**Summary**: A monotonically increasing token issued with each lock or lease grant, used to prevent a node that falsely believes it holds a lock from corrupting data -- the resource rejects any write carrying a token older than one it has already seen.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## The problem

When using a lock or lease to protect a shared resource (e.g., a file in a storage service), a node may continue to act on the lock after it has expired -- for example, because of a [[process-pauses|process pause]]. Another node may have already acquired the lock and started writing. The original node, unaware its lock has expired, also writes to the resource, causing data corruption. (source: designing-data-intensive-applications, chapter 8)

This is not theoretical: HBase had this exact bug in production. (source: designing-data-intensive-applications, chapter 8)

## How fencing tokens work

Every time the lock server grants a lock or lease, it also returns a **fencing token** -- a number that increases with each grant (e.g., a simple counter). (source: designing-data-intensive-applications, chapter 8)

The protocol:

1. Client 1 acquires the lock and receives token **33**.
2. Client 1 is paused (e.g., GC). The lock expires.
3. Client 2 acquires the lock and receives token **34**.
4. Client 2 sends a write to the storage service, including token 34. The write succeeds.
5. Client 1 resumes and sends its write with token 33.
6. The storage service rejects the write because it has already processed a write with the higher token 34.

## Key requirement: server-side enforcement

The resource itself must actively check tokens and reject any write with an older token than one it has already processed. It is **not sufficient** to rely on clients checking their own lock status -- a paused client cannot know its lock has expired. (source: designing-data-intensive-applications, chapter 8)

This server-side checking is arguably a good thing: it is unwise for a service to assume that its clients will always be well behaved. (source: designing-data-intensive-applications, chapter 8)

## Implementations

If ZooKeeper is used as a lock service, the **transaction ID (zxid)** or the **node version (cversion)** can be used as fencing tokens, since both are guaranteed to be monotonically increasing. (source: designing-data-intensive-applications, chapter 8)

For resources that do not explicitly support fencing tokens, workarounds may be possible -- for example, including the token in the filename of a file storage service. But some form of check is necessary. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[truth-and-leadership-in-distributed-systems]]
- [[process-pauses]]
- [[quorums]]
- [[failover]]
- [[byzantine-faults]]
