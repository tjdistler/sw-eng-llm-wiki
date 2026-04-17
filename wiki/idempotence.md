# Idempotence

**Summary**: A property of an operation such that applying it N times has the same observable effect as applying it once. In distributed systems idempotence is the workhorse primitive that makes retry-based fault tolerance safe — it converts at-least-once delivery into effectively-once behaviour without requiring synchronous coordination.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/designing-data-intensive-applications/glossary.md`

**Last updated**: 2026-04-16

---

## Definition

An operation `f` is **idempotent** if `f(f(x)) == f(x)` — applying it twice produces the same state as applying it once. More generally, any number of applications (including zero retries, one retry, ten retries) converges on the same observable effect. Kleppmann's definition: "An idempotent operation is one that you can perform multiple times, and it has the same effect as if you performed it only once" (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md). The book's glossary phrases the operational consequence: "Describing an operation that can be safely retried; if it is executed more than once, it has the same effect as if it was only executed once" (source: raw/designing-data-intensive-applications/glossary.md).

The definition is about **observable effects**, not internal bookkeeping. An operation that records each retry in an audit log but leaves the externally visible state unchanged still counts as idempotent for the consumers of that state.

## Why distributed systems need it

Distributed systems assume at-least-once delivery as the default. Retries are unavoidable because (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md):

- A network call can fail in three ways the caller cannot distinguish: request lost, response lost, or server crashed after committing. Without knowing which, a prudent client retries. Kleppmann's Chapter 4 makes the same point about [[rpc|RPC]]: "If you retry a failed network request, it could happen that the requests are actually getting through, and only the responses are getting lost. In that case, retrying will cause the action to be performed multiple times, unless you build a mechanism for deduplication (idempotence) into the protocol" (source: raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md).
- Message brokers (Kafka, SQS, Pub/Sub) offer at-least-once semantics; exactly-once-over-the-wire is either impossible or carries prohibitive cost.
- [[stream-processing-fault-tolerance|Stream processors]] replay input on checkpoint recovery; [[worker-container-interface|batch workers]] get re-scheduled after node failure; [[rpc|RPC]] clients retry on timeout.

The alternative to retrying is to drop the operation and lose data. That is almost never acceptable, so duplicate execution *will* happen. Idempotence is the discipline that makes it harmless.

## Natural vs constructed idempotence

Some operations are **naturally idempotent** — the effect of repeating them is structurally the same as the effect of doing them once. Kleppmann's example: "setting a key in a key-value store to some fixed value is idempotent (writing the value again simply overwrites the value with an identical value)" (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md). Generalising:

- `SET X = 5` — writing the same value again leaves `X` at 5.
- `DELETE user WHERE id = 42` — the row is gone after the first call; subsequent calls are no-ops.
- `PUT /objects/key` to content-addressed storage — the key is the content hash, so re-uploading overwrites identical bytes with identical bytes.
- Writing a batch worker's output to an item-keyed path in a blob store (e.g., `s3://bucket/{item_id}/output.png`) — the second run overwrites the first. This is a natural pairing with Kubernetes-managed [[worker-container-interface|work queues]] that may restart a worker after a node failure.

Other operations are **not naturally idempotent** and must be made so. Kleppmann's counter-example: "incrementing a counter is not idempotent (performing the increment again means the value is incremented twice)" (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md). Generalising:

- `INCREMENT counter` — incrementing twice gives a different result than incrementing once.
- `INSERT INTO orders (...) VALUES (...)` — without a uniqueness constraint, the same order is inserted twice.
- `SEND email` — the recipient reads the same email twice.
- `CHARGE $11` — the customer pays twice. Kleppmann uses exactly this example (Example 12-1: "a standard example for transaction atomicity, it is actually not correct, and real banks do not work like this" — because a user whose `POST` times out will retry, and from the database's point of view the retry is a separate transaction) (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md).

Making these idempotent requires extra machinery, usually in the form of dedup state keyed by an **operation ID**. "Even if an operation is not naturally idempotent, it can often be made idempotent with a bit of extra metadata" (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md).

## Techniques

### Operation IDs / request IDs

Attach a unique identifier to each logical operation at the *originating* client and propagate it end-to-end. The receiver keeps a dedup table keyed by ID; duplicates are detected and the second execution is suppressed (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md).

Kleppmann's concrete recipe for Example 12-2: "you could generate a unique identifier for an operation (such as a UUID) and include it as a hidden form field in the client application, or calculate a hash of all the relevant form fields to derive the operation ID. If the web browser submits the POST request twice, the two requests will have the same operation ID" (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). The database then enforces dedup via a `UNIQUE` constraint on the `request_id` column; "Relational databases can generally maintain a uniqueness constraint correctly, even at weak isolation levels" (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md).

The ID must be generated *before* the first attempt, so retries carry the same ID. A server-assigned ID is useless for dedup because retries would each get a new one.

This is the central technique of the [[end-to-end-argument]]: only the originating client knows which calls are retries of the same logical operation. TCP, the database, and the stream processor each suppress duplicates in their own layer, but only an application-level ID covers the full user-intent-to-persisted-effect path.

A bonus observation from Example 12-2: the `requests` table "acts as a kind of event log, hinting in the direction of event sourcing. The updates to the account balances don't actually have to happen in the same transaction as the insertion of the event, since they are redundant and could be derived from the request event in a downstream consumer—as long as the event is processed exactly once, which can again be enforced using the request ID" (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). The dedup table doubles as an audit trail that downstream [[event-sourcing|event-sourced]] consumers can replay.

### Dedup tables

The receiver stores `operation_id -> result` (or at minimum `operation_id -> applied`). Before executing, it checks whether the ID has been seen. If so, it returns the cached result without re-executing (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md).

The table grows unboundedly unless entries are expired. Common approaches:

- TTL on the entry (tolerate duplicates arriving after the window).
- Scope the IDs to a partition and compact old segments.
- Rely on a uniqueness constraint on a persistent table the operation writes anyway (e.g., an `orders` table with `UNIQUE(request_id)`).

### Versioned updates / compare-and-swap

Include a version in every write. The receiver accepts the write only if the version matches the current one, then bumps the version (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). A duplicate retry carries a stale version and is rejected.

This is the mechanism behind [[fencing-tokens]] — a monotonically increasing token issued with a lease, checked by the resource on every request. Fencing tokens are the mutual-exclusion specialization: the version is the lease generation, and "duplicate" means "the previous holder speaking after its lease expired".

### Content-hash keys

When the operation writes an immutable artifact, use the hash of the content as the storage key. Two retries produce identical artifacts with identical hashes, so the second write overwrites the first harmlessly. This is how Git, IPFS, and most content-addressed storage achieve idempotence for free.

### Kafka-offset-based dedup

For stream consumers, store the offset of the most recently processed message atomically with the downstream write. Before writing, check whether the offset has already been applied. If yes, skip. Storm's Trident uses this approach (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md).

## Where the burden sits

In almost every case the **receiver** carries the dedup state, and the **sender retries freely** (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). This asymmetry is the whole point: the client does not have to distinguish lost-request from lost-response, because the server's dedup handles both the same way.

A corollary: the sender must use the *same* operation ID across retries. Generating a fresh ID per attempt breaks dedup entirely — each retry becomes a new logical operation from the server's perspective.

## Prerequisites for idempotence-based fault tolerance

Idempotence alone is not sufficient. Stream-processing fault tolerance via idempotence additionally requires (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md):

- **Deterministic replay** — failed tasks must replay the same messages in the same order. [[log-based-message-brokers]] provide this.
- **Deterministic processing** — the same input must produce the same downstream writes.
- **No concurrent writers to the same value** — otherwise a "dedup" check sees a stale state and re-applies.
- **Fencing during failover** — [[fencing-tokens]] prevent a node believed dead but actually alive from interfering.

Get any of these wrong and idempotence silently degrades into at-least-once semantics.

## Relationship to exactly-once semantics

Idempotence + end-to-end operation IDs + deterministic derivation = **effectively-once** semantics, which is what [[exactly-once-semantics]] actually delivers in practice. The "exactly once" marketing term hides the fact that duplicates still happen at the wire and framework levels; what changes is that downstream effects absorb the duplicates without visible consequence (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). Kleppmann explicitly frames idempotence as one of two alternatives to achieving this: "Distributed transactions are one way of achieving that goal, but another way is to rely on idempotence. … idempotent operations can be an effective way of achieving exactly-once semantics with only a small overhead" (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md).

This is also why heterogeneous [[distributed-transactions]] (XA) can usually be replaced with asynchronous event logs plus idempotent consumers — the same correctness property with vastly better availability characteristics. Kleppmann: "when data crosses the boundary between different technologies, I believe that an asynchronous event log with idempotent writes is a much more robust and practical approach" (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md). See [[coordination-avoidance]] for the broader argument.

## Integrity, not timeliness

A useful framing from Kleppmann's Chapter 12 is that idempotence contributes to **integrity** (absence of corruption) rather than **timeliness** (up-to-date reads). He distinguishes them: "violations of timeliness are 'eventual consistency,' whereas violations of integrity are 'perpetual inconsistency.'" And directly on our topic: "fault-tolerant message delivery and duplicate suppression (e.g., idempotent operations) are important for maintaining the integrity of a data system in the face of faults" (source: raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md).

This matters because it tells you what idempotence *doesn't* do: it does not guarantee that consumers see a write immediately (timeliness), only that when they do see it — after any number of retries — the effect is applied once. Systems that need strict read-after-write may still need linearizable reads on top of idempotent writes; systems that can tolerate async propagation get integrity for free.

## Where idempotence shows up in the wiki

- **[[stream-processing-fault-tolerance]]** — microbatching and checkpointing restore framework-internal exactly-once, but external side effects need idempotence to survive replays.
- **[[worker-container-interface]]** — Kubernetes may retry a batch worker after a machine failure; workers must write outputs to item-keyed paths so re-runs overwrite rather than duplicate.
- **[[rpc]]** — a network request can succeed with the response lost. Retrying is safe only if the server-side operation is idempotent; REST's `PUT` and `DELETE` are idempotent by convention where `POST` is not.
- **[[reduce-pattern]]** — the associativity required by reduce is closely related: an associative + idempotent combine lets the reduce tree be rebuilt in any order after partial failure without corrupting the aggregate.
- **[[exactly-once-semantics]]** — the pattern for converting at-least-once infrastructure into effectively-once application behaviour.
- **[[saga]]** — compensating actions rely on the original action and its compensation both being idempotent, so partial-retry scenarios don't double-apply either step.
- **[[change-data-capture]]** and **[[event-sourcing]]** — derived-state pipelines that replay events must produce the same state every time; idempotent writes are the mechanism.

## Summary of honest forms

The "honest" form of each idempotence technique surfaces the ID or version at the layer that knows it:

| Layer | Honest form | Dishonest form |
|---|---|---|
| Client → server | Client-generated UUID in the request body | Server-generated ID returned by the first call (useless for dedup) |
| Stream consumer | Kafka offset stored with downstream write | "Our framework provides exactly-once" (true only inside the framework) |
| Lock holder → resource | Fencing token rejected by the resource | Client checking its own lock status |
| Multi-service workflow | End-to-end request ID in every hop | Each service's internal dedup only |

In every case, the honest form pushes the identifier to the layer that can actually tell a retry from a new intent — which, per the end-to-end argument, is almost always the application.

## Related pages

- [[exactly-once-semantics]]
- [[end-to-end-argument]]
- [[fencing-tokens]]
- [[stream-processing-fault-tolerance]]
- [[worker-container-interface]]
- [[rpc]]
- [[coordination-avoidance]]
- [[distributed-transactions]]
- [[reduce-pattern]]
- [[saga]]
- [[log-based-message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
