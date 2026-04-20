# MOC: Consistency and Transactions

**Summary**: Entry point for questions about *correctness under concurrency and partial failure* — what a transaction guarantees, what each isolation level allows, what you lose when data spans stores, and how sagas, compensations, and outbox patterns rebuild a useful correctness story on top of per-service local transactions. Start here when the question is "what promise can I make about this operation?" rather than "what's the mechanism under that promise?" (the mechanism MOC is [[moc-distributed-systems]]).

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have an operation — a user checkout, a transfer, a workflow across services — and you need to know what will happen to it under concurrency, retry, partial failure, or replication lag. You might be choosing an isolation level. You might be weighing saga variants. You might be staring at a cross-service step that used to be a single database transaction and wondering what you just gave up.

The canonical shape of a question that lands here: *"Can I downgrade from Serializable to Snapshot Isolation?"*, *"What happens if step 3 of this 5-step saga fails?"*, *"Is eventual consistency acceptable for this flow?"*, *"Do I need 2PC or a saga?"*, *"What isolation anomaly is this bug?"*, *"How do I ship an event atomically with a database write?"*

Jurisdictional rule for this MOC:

- **This MOC** owns the *guarantees* a user, application, or workflow can rely on. Isolation, atomicity, linearizability vs causal vs eventual, saga variants, compensations, outbox as a correctness bridge, idempotence as the building block for effectively-once.
- [[moc-distributed-systems]] owns the *mechanisms* that produce the guarantees. Consensus, quorums, replication protocols, fencing tokens. Linearizability and CAP appear in both MOCs: this one owns the promise, that one owns the cost of keeping it.
- [[moc-data-processing]] owns the *pipeline-execution correctness* story — effectively-once processing, checkpointing, Google Workflow's structural mechanisms. This MOC cites those from the cross-store-correctness angle; the processing MOC owns the engine-internal treatment.
- [[moc-events-and-streaming]] owns the *publication* side of outbox — how an event-driven system hands off events atomically with business state. This MOC owns outbox as the *correctness bridge across a saga step*; both MOCs link the same page under different framings.
- [[moc-data-models-and-storage]] owns *how the store implements* ACID — MVCC, WAL, 2PL internals. This MOC owns the semantics they expose; the storage MOC owns the storage-engine side.

## Transactions — the building block

Before any distributed-correctness story, get single-node transactions right. Most cross-service correctness bugs are actually single-node isolation bugs dressed up.

- [[transactions]] — grouping reads and writes into an all-or-nothing logical unit. The discipline that lets application code ignore concurrency and partial failure *inside the boundary* and reason about it only at the edges. Start here.
- [[acid]] — Atomicity, Consistency, Isolation, Durability. The four guarantees, with deliberate nuance on how each is weaker-than-you-think in real databases. Consistency is the weakest member of the acronym; Isolation is the one that hides the most variation.
- [[base-properties]] — Basically Available, Soft state, Eventual consistency. The ACID complement for cross-service systems. Not a replacement — a trade-off explicitly made when ACID across services would cost too much.

Deeper reading: [[designing-data-intensive-applications#chapter-7-transactions]]. If there's one chapter to read end-to-end from DDIA, this is the one for application engineers.

## Isolation levels — the spectrum

Every database gives you a spectrum from weakest (cheap, many anomalies) to strongest (expensive, no anomalies). Know where your database's default sits and what the next step up or down costs and permits.

- [[isolation-levels]] — the spectrum hub: Read Uncommitted, Read Committed, Snapshot Isolation / Repeatable Read, Serializable. Vendor names differ; the guarantees don't always match the names.
- [[read-committed]] — no dirty reads, no dirty writes. The most basic *useful* level. Postgres's default; still permits read skew and lost updates. Know what it does and doesn't protect.
- [[snapshot-isolation]] — MVCC-based consistent snapshots. Each transaction sees a view of the database as of its start. Great for long reads (analytics, backups); vulnerable to [[write-skew]] because writes are made against a snapshot that may be stale by commit.
- [[mvcc]] — multi-version concurrency control. Multiple committed versions per row, garbage-collected later; the mechanism under both snapshot isolation and Postgres's general read path. The reason "readers don't block writers, writers don't block readers" became the expected default.
- [[serializability]] — the strongest level: the result is equivalent to *some* serial execution. Three implementation routes follow.
- [[serializable-snapshot-isolation]] — SSI, 2008; optimistic serializability on top of snapshot isolation. Tracks read/write dependencies and aborts at commit time if a cycle would form. Postgres's `SERIALIZABLE`. The best general-purpose answer for most OLTP systems that need true serializability without the locking cost.
- [[two-phase-locking]] — pessimistic serializability: shared/exclusive locks acquired incrementally, released at commit. Readers and writers block each other. The historical default; widely deprecated for hot workloads because of the latency and deadlock footprint.
- [[actual-serial-execution]] — single-threaded stored-procedure execution (VoltDB, Redis). Feasible when working sets fit in memory and transactions are short. The niche-but-elegant answer.

### The anomalies each level permits

Know the anomalies by name — every production bug in this area is one of these with the label torn off.

- [[dirty-reads-and-dirty-writes]] — reading or overwriting uncommitted data. Read Committed prevents both.
- [[read-skew]] — seeing the database at two different points in time across two reads (nonrepeatable read). Snapshot Isolation prevents it.
- [[lost-updates]] — two concurrent read-modify-write cycles silently overwrite each other. Prevented by atomic `UPDATE … SET x = x + 1`, by `SELECT FOR UPDATE`, by application-side compare-and-set, or by Serializable.
- [[write-skew]] — two transactions read the same data and write different objects, violating a cross-object invariant (the on-call-rotation bug; the doctor-shift bug). Snapshot Isolation *does not* prevent this — only Serializable does.
- [[phantoms]] — one transaction's write changes another's earlier range query. Predicate locks and index-range locks in 2PL; dependency tracking in SSI.

Deeper reading: [[designing-data-intensive-applications#chapter-7-transactions]] for the end-to-end treatment with worked examples.

## Consistency models — the cross-node guarantees

Once the data spans nodes, the isolation-level vocabulary isn't enough. You need a separate axis for what *readers across replicas* are promised.

- [[linearizability]] — the strongest single-object guarantee: atomic recency, single-copy illusion, every read returns the last successful write. Expensive: requires consensus on every write or every read. Reach for it for critical infrastructure (distributed locks, leader election, coordination) and not much else.
- [[causal-consistency]] — preserves happens-before without requiring a total order. The strongest guarantee achievable without global coordination. The sweet spot: more than eventual, cheaper than linearizable.
- [[consistent-prefix-reads]] — causally related writes appear in order. The replication-lag anomaly to be aware of if you're going to downgrade from linearizability.
- [[monotonic-reads]] — reads never go backwards in time for a given user. Stickiness as the usual implementation.
- [[read-after-write-consistency]] — users see their own writes. The per-user consistency most applications care about; often the *only* linearisability an application truly needs.
- [[eventual-consistency]] — the weakest useful guarantee: convergence with no time bound. Fine for view-layer data; dangerous when treated as the default without naming the reconciliation strategy.
- [[cap-theorem]] — the partition-time forced choice between linearizability and availability. Historically framed as "pick two of C, A, P" — that framing was never quite right; read the page for what Brewer actually proved and why "AP vs CP" stickers hide more than they reveal.
- [[timeliness-and-integrity]] — Kleppmann's disentangling of "consistency" into two independent requirements: reads are up-to-date (timeliness) and data is correct (integrity). Most applications need integrity always; timeliness only sometimes.
- [[coordination-avoidance]] — maintain integrity without synchronous coordination whenever possible. The design principle behind the last two decades of scalable systems.

Deeper reading: [[designing-data-intensive-applications#chapter-9-consistency-and-consensus]] for the theory; [[designing-data-intensive-applications#chapter-12-the-future-of-data-systems]] for Kleppmann's synthesis of timeliness-vs-integrity and the coordination-avoidance argument.

## Cross-store correctness — why the single-transaction story doesn't extend

Once an operation touches two stores — two databases, or a database and a message broker — you've left ACID behind. You have two choices: give up atomicity and compensate, or try to hold atomicity across stores and pay a high operational cost. Almost every production system picks the first.

- [[distributed-transactions]] — transactions spanning multiple nodes or stores. XA, heterogeneous 2PC, the operational cliff: any coordinator-down moment blocks every participant indefinitely. Why most shops gave up on 2PC and picked sagas instead.
- [[two-phase-commit]] — the protocol: prepare, commit/abort. Not fault-tolerant without a replicated coordinator. The in-doubt window is where stores sit holding locks with no idea whether to commit. Newman's standing recommendation: "just say no."
- [[dynamic-coupling]] — Ford and Richards's three-axis taxonomy of runtime coupling: **communication** (sync vs async) × **consistency** (atomic vs eventual) × **coordination** (orchestrated vs choreographed). Eight corners; each is one of the sagas below. This single page is the conceptual key for the whole cross-store-correctness discussion.

### The saga family

Sagas are the main alternative to 2PC. The original 1987 paper framed them for long-lived single-database transactions; microservices repurposed the idea for cross-service workflows. The Hard Parts taxonomy names all eight corners of the dynamic-coupling cube as specific saga shapes.

Start with the pattern itself:

- [[saga]] — the hub. A business process as a sequence of local ACID transactions across services; [[compensating-update|compensations]] instead of locks; backward and forward recovery; orchestrated vs choreographed at the coordination axis. The vocabulary under every saga variant below.
- [[compensating-update]] — semantic rollback: an explicit "undo" action for each saga step. The core building block. Rarely a perfect inverse — "refund the payment" is not "the payment never happened" — which is why parallel-run, reconciliation, and manual-intervention channels are part of every real saga.
- [[compensation-workflow]] — Bellemare's event-driven framing of compensations: failures emit explicit failure events; downstream services consume them and reverse their own state.
- [[distributed-workflow-patterns]] — the hub for the Hard Parts Ch 11 orchestration-vs-choreography trade-off matrix and the four-force rubric (workflow control, error handling, observability, state tracking) used to pick between them.
- [[workflow-orchestration]] — mediator coordinates the workflow; central state tracking; easy to observe and debug; scales worse than choreography because every step fans through the mediator. Named [[mediator-topology]] in event-driven-architecture framing.
- [[workflow-choreography]] — peer-to-peer events; no central coordinator; responsive and scalable; hard to track overall state. Named [[broker-topology]] in event-driven-architecture framing.
- [[choreography]] — the top-level hub; cross-links the same concept across DDD, EDM, and Hard Parts.
- [[workflows-in-edm]] — Bellemare's event-driven framing of the choice.

The eight Hard Parts saga variants — read these end-to-end if the question is "which shape for this workflow?":

- [[epic-saga]] — `sync + atomic + orchestrated`. The traditional distributed-transaction shape. Rarely advisable; pays all three costs at once.
- [[phone-tag-saga]] — `sync + atomic + choreographed`. Worst of both worlds. Avoid.
- [[fairy-tale-saga]] — `sync + eventual + orchestrated`. The common real-world default for request-response microservice workflows.
- [[time-travel-saga]] — `sync + eventual + choreographed`. Choreographed variant of fairy-tale.
- [[fantasy-fiction-saga]] — `async + atomic + orchestrated`. Rarely viable — atomicity is what async gives up in the first place.
- [[horror-story-saga]] — `async + atomic + choreographed`. Avoid. Named for good reason.
- [[parallel-saga]] — `async + eventual + orchestrated`. Very common, a strong default when you need async + state tracking.
- [[anthology-saga]] — `async + eventual + choreographed`. The native form of event-driven architecture; the shape most mature event-driven microservice fleets converge to.

The Hard Parts Ch 9 and 10 Data-Ownership patterns that sit alongside saga choices:

- [[distributed-data-access]] — the four-pattern hub for reading data a service doesn't own.
- [[interservice-communication-pattern]] — remote call; three latencies (network, processing, security); tight runtime coupling; the baseline to compare against.
- [[column-schema-replication-pattern]] — copy columns into the reader's DB; async sync; staleness trade.
- [[replicated-caching-pattern]] — Hazelcast-style in-memory replicated cache; ~500 MB ceiling.
- [[data-domain-pattern]] — shared schema across services; explicit re-entry of shared-DB tension for a specific reason.
- [[event-based-consistency-pattern]] — the default eventual-consistency pattern via events (Ch 9).
- [[orchestrated-request-based-pattern]] — synchronous orchestrated workflow; atomic-ish consistency across services (Ch 9).
- [[background-synchronization-pattern]] — background reconciler for eventual consistency (Ch 9).
- [[data-ownership]] — the writer-owns rule; sole vs common vs joint ownership. The decision prior to any of the access patterns.
- [[joint-ownership-techniques]] — four legit ways to let multiple services write one table; table split, data domain, delegate, service consolidation.

Deeper reading: [[monolith-to-microservices#chapter-4-decomposing-the-database]] for Newman's migration-focused saga framing; [[building-event-driven-microservices#chapter-8-building-workflows-with-microservices]] for the event-driven variant.

## Outbox — the correctness bridge

The outbox is the single most load-bearing pattern in cross-service correctness. It appears in three MOCs; here it's the bridge across a saga step.

- [[outbox-table-pattern]] — within a single transaction, write business state AND an "event-to-publish" row to an outbox table. A separate process streams the outbox to the broker. Guarantees *at-least-once* publication of the event for every successful state change, with no distributed transaction. The foundation under every event-driven saga that claims to be correct under failure.

The lens in each MOC:

- This MOC owns outbox as the *correctness bridge* between an atomic local transaction and a cross-service workflow. "The saga needs to know step 1 happened; outbox guarantees the event announcing step 1 is durable and will be published."
- [[moc-events-and-streaming]] owns outbox as a *publication pattern* — atomic event emission for an event-driven microservice, treated as the canonical integration seam.
- [[moc-data-processing]] owns outbox as a *source-capture mechanism* — an application-layer CDC variant that gives you semantic events instead of raw row events.

Alternatives to outbox, with their failure modes:

- **Dual write without outbox** — write the DB, then publish the event. Two-phase failure modes: DB committed but broker publish failed; broker published but DB commit failed (if the order is reversed). Never correct without an outbox, 2PC, or at-least-once retry with idempotence.
- [[change-data-capture]] — CDC over the binlog/WAL as an outbox alternative. Gives you row-level change events, not application-semantic events; the decision is about whether downstream wants domain events or row deltas.
- [[query-based-cdc]] — periodic polling of timestamp columns. Simple and lossy; acceptable only for low-stakes synchronisation.

Deeper reading: [[building-event-driven-microservices#chapter-4-integrating-event-driven-architectures-with-existing-systems]] for the outbox + CDC + eventification treatment.

## Effectively-once semantics and idempotence

"Exactly once" is a thing users want and a thing production systems rarely honestly deliver. The practical target is *effectively once* — at-least-once delivery plus idempotent operations plus transactional offset commits, with operation IDs carrying the deduplication story end to end.

- [[exactly-once-semantics]] — DDIA's framing: exactly-once is achievable *as a visible outcome*, via idempotence + end-to-end operation identifiers, not via transport guarantees.
- [[end-to-end-argument]] — Saltzer/Reed/Clark's principle: infrastructure-level guarantees are insufficient; the application must carry operation IDs end to end. The reason "the broker promises exactly once" is never actually enough.
- [[idempotence]] — operations safe to retry without changing the result. The building block: design operations around idempotence and most failure recovery becomes "retry and move on."
- [[effectively-once-processing]] — the stream-processing version of the above. Idempotent writes + transactional offset commits + deterministic processing yields the same user-visible result as exactly-once, with none of the theoretical impossibility.
- [[workflow-correctness-guarantees]] — Google Workflow's four structural mechanisms (configuration tasks as barriers, lease-bound commits, unique output filenames, server-token validation). Exactly-once *without* requiring idempotent payloads — a rare and illuminating counterpoint.

Deeper reading: [[designing-data-intensive-applications#chapter-12-the-future-of-data-systems]] for the end-to-end-argument framing; [[building-event-driven-microservices#chapter-7-stateful-streaming]] for effectively-once in a stream processor.

## When eventual consistency is enough (and when it isn't)

Eventual consistency is the default of distributed systems; the discipline is to *know* where you're using it, *name* the reconciliation strategy, and *bound* the window.

- [[eventual-consistency]] — the guarantee; the user-facing implications; why "eventually" without a bound is an admission rather than a design.
- [[background-synchronization-pattern]] — the reconciliation path: a background job that compares stores, detects drift, and heals it. The honest answer to "what happens when they diverge?" for eventual-consistency patterns.
- [[data-availability-vs-integrity]] — SRE Ch 26's framing: integrity is the means, availability is the goal. Users can't distinguish loss, corruption, and extended unavailability. The lens that forces you to name what "consistent enough" means.
- [[defense-in-depth-data]] — soft deletion + backups + validators. The structural answer for when eventual-consistency + bugs can silently destroy user data.

## Sibling MOCs

- [[moc-distributed-systems]] — owns the mechanisms behind every guarantee in this MOC. Consensus, quorums, replication, fencing. This MOC is "what promise do I get?"; that MOC is "what does it cost and how does it work?"
- *moc-events-and-streaming* (companion) — owns the architectural use of events. This MOC shares [[saga]], [[outbox-table-pattern]], [[compensation-workflow]], and the orchestration-vs-choreography axis with that one under a *publication and integration* framing; this MOC owns the *correctness-across-stores* framing.
- [[moc-data-processing]] — owns effectively-once in a stream processor, Google Workflow's structural correctness mechanisms, and pipeline-execution correctness. Cited here under the cross-store-correctness lens; the processing MOC owns the engine-internal side.
- [[moc-data-models-and-storage]] — owns MVCC, WAL, storage-engine internals. This MOC cites those as the implementation of isolation; the storage MOC owns the engine view.
- [[moc-decomposition]] — owns the extraction playbook. This MOC owns the correctness you lose the moment you split a database. Read [[saga]], [[outbox-table-pattern]], [[two-phase-commit]] end to end before any non-trivial split, especially in money or safety-critical domains; [[parallel-run-pattern]] from the decomposition MOC is the verification discipline that pairs with them.
- [[moc-microservices]] — owns the organisational frame around services that live with these correctness constraints. Single-writer principle, service data ownership, and the discipline of not sharing databases are the operational consequences of everything here.

## Related pages

- [[index]]
- [[designing-data-intensive-applications]]
- [[monolith-to-microservices]]
- [[building-event-driven-microservices]]
- [[software-architecture-the-hard-parts]]
- [[transactions]]
- [[acid]]
- [[base-properties]]
- [[isolation-levels]]
- [[snapshot-isolation]]
- [[serializability]]
- [[serializable-snapshot-isolation]]
- [[two-phase-locking]]
- [[write-skew]]
- [[lost-updates]]
- [[phantoms]]
- [[linearizability]]
- [[causal-consistency]]
- [[eventual-consistency]]
- [[cap-theorem]]
- [[coordination-avoidance]]
- [[timeliness-and-integrity]]
- [[distributed-transactions]]
- [[two-phase-commit]]
- [[saga]]
- [[compensating-update]]
- [[dynamic-coupling]]
- [[epic-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
- [[outbox-table-pattern]]
- [[change-data-capture]]
- [[idempotence]]
- [[exactly-once-semantics]]
- [[effectively-once-processing]]
- [[end-to-end-argument]]
- [[workflow-correctness-guarantees]]
- [[distributed-workflow-patterns]]
- [[workflow-orchestration]]
- [[workflow-choreography]]
