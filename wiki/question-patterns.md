# Question Patterns

**Summary**: A router from real expert-level questions to the MOCs and concept pages most likely to ground a high-quality answer. When a complex multi-cluster question arrives, find the closest archetype here, read every MOC the pattern names, then follow the listed concept pages and raw chapter sections before drafting.

**Sources**: (meta-page; aggregates MOCs and concept pages)

**Last updated**: 2026-04-19

---

## How to use this page

Most expert questions in this wiki are *multi-cluster* — they touch decomposition, data, consistency, organisation, and operations simultaneously. A single keyword match against `index.md` will find the closest-shaped concept page and miss the five other clusters that compose to a complete answer. This page is the router that prevents that.

Match the question to the closest pattern below. Fuzzy matches are fine — patterns are deliberately broad, and real questions usually hit more than one. Read **every MOC** each pattern lists, in full, before drafting. Each MOC tells you which concept pages apply and how to frame them; follow into the concept pages as each MOC guides. Cite raw book chapter sections (listed at the bottom of each MOC and again here per pattern) when the distilled concept-page treatment is too terse for the depth the question requires.

If the question doesn't fit any pattern here, read `index.md` for the MOC catalogue and compose a pattern yourself. If the shape recurs, add it as a new pattern — the list is meant to grow as the wiki is exercised.

## Pattern: Extract a service from a monolith

*Examples*: "We need to split the payments backend out of our Django monolith so we can scale 10x"; "Pull the notification system into its own service"; "How do we get the fulfilment domain out of the shared Postgres?"

This is the canonical multi-cluster question. It touches decomposition (the patterns for getting the code out), data (the new service's target schema and the split of the shared DB), consistency (what correctness you lose and how to rebuild it with sagas and outbox), microservices (what it means to *run* the new service), distributed systems (the failure modes the monolith didn't have), and reliability (the SLOs, observability, and on-call the new service needs before cutover). Skipping any one cluster produces a plan that stalls halfway through — typically at the database or at the first production incident.

Read: [[moc-decomposition]], [[moc-data-models-and-storage]], [[moc-consistency-and-transactions]], [[moc-microservices]], [[moc-distributed-systems]], [[moc-reliability-and-operations]].

Key concept pages: [[why-microservices]], [[modular-monolith]], [[independent-deployability]], [[extraction-prioritization]], [[architectural-quantum]], [[bounded-context]], [[aggregate]], [[coupling]], [[cohesion]], [[event-storming]], [[strangler-fig-pattern]], [[branch-by-abstraction]], [[parallel-run-pattern]], [[change-data-capture]], [[outbox-table-pattern]], [[saga]], [[shared-database-antipattern]], [[database-as-a-service-interface]], [[database-view-pattern]], [[split-the-database-first]], [[conways-law]], [[service-level-objective]], [[error-budget]], [[distributed-tracing]], [[correlation-ids]], [[orphaned-services]].

Key raw chapters: [[monolith-to-microservices#chapter-3-splitting-the-monolith]], [[monolith-to-microservices#chapter-4-decomposing-the-database]], [[monolith-to-microservices#chapter-5-growing-pains]], [[designing-data-intensive-applications#chapter-7-transactions]], [[designing-data-intensive-applications#chapter-8-the-trouble-with-distributed-systems]], [[site-reliability-engineering#chapter-4-service-level-objectives]].

Special note for money- or safety-critical domains (payments, healthcare, safety): [[parallel-run-pattern]] is not optional. Ship the new service dark, compare every request's result against the monolith for weeks, and cut over only when the new side has proven correct. Pair with saga-based correctness per [[moc-consistency-and-transactions]].

## Pattern: Scale an existing service 10x

*Examples*: "Checkout needs to handle Black Friday traffic"; "We're sharding the orders table — what should we consider?"; "Our p99 latency is blowing out under load"; "Reads are slow and we think we need a cache."

Scaling questions are almost always a combination of data-shape decisions (partitioning, replication, the right engine for the workload), serving-shape decisions (replicated vs sharded vs scatter/gather), and reliability-shape decisions (capacity planning, overload handling, cascading-failure prevention). Naive "just add replicas" answers miss the failure modes — retries, queue buildup, cache stampedes — that only appear at 10x load and turn small blips into full outages.

Read: [[moc-data-models-and-storage]], [[moc-distributed-systems]], [[moc-container-and-serving-patterns]], [[moc-reliability-and-operations]], [[moc-architecture-styles]].

Key concept pages: [[partitioning]], [[partitioning-strategies]], [[consistent-hashing]], [[rebalancing-partitions]], [[replication]], [[replicated-load-balanced-service]], [[sharded-service-pattern]], [[scatter-gather-pattern]], [[hot-sharding]], [[shard-key-selection]], [[space-based-architecture]], [[capacity-planning]], [[server-overload]], [[handling-overload]], [[cascading-failure]], [[addressing-ongoing-cascading-failure]], [[retry-budget]], [[retry-amplification]], [[circuit-breaker]], [[timeouts]], [[graceful-degradation]], [[load-shedding]], [[robustness-and-resiliency-at-scale]].

Key raw chapters: [[designing-data-intensive-applications#chapter-5-replication]], [[designing-data-intensive-applications#chapter-6-partitioning]], [[site-reliability-engineering#chapter-21-handling-overload]], [[site-reliability-engineering#chapter-22-addressing-cascading-failures]], [[designing-distributed-systems#chapter-6-sharded-services]], [[designing-distributed-systems#chapter-7-scatter-gather]].

## Pattern: Pick an architecture style for a greenfield project

*Examples*: "We're starting a new product — should it be microservices from day one?"; "Modular monolith or service-based architecture?"; "Event-driven or synchronous?"

The most common failure here is reaching for a style before calibrating characteristics. Start with the business drivers and the system's must-be-good-ats; the -ilities, the quantum, and the trade-off frame are the upstream decisions. Most systems should start on the monolithic half of the catalogue and move only when an actual force demands it — distribution is a one-way door priced in operational complexity for the system's lifetime, not just its launch quarter.

Read: [[moc-architecture-fundamentals]], [[moc-architecture-styles]], [[moc-components-and-partitioning]], [[moc-domain-driven-design]], [[moc-microservices]].

Key concept pages: [[software-architecture-definition]], [[architecture-characteristics]], [[architectural-quantum]], [[trade-off-analysis]], [[least-worst-trade-offs]], [[monolithic-vs-distributed]], [[fallacies-of-distributed-computing]], [[layered-architecture]], [[modular-monolith]], [[service-based-architecture]], [[microkernel-architecture]], [[event-driven-architecture]], [[space-based-architecture]], [[microservices]], [[distributed-monolith]], [[bounded-context]], [[domain-driven-design]], [[entity-trap]], [[technical-vs-domain-partitioning]], [[components]].

Key raw chapters: [[fundamentals-of-software-architecture#chapter-9-foundations]], [[fundamentals-of-software-architecture#chapter-18-choosing-the-appropriate-architecture-style]], [[fundamentals-of-software-architecture#chapter-17-microservices-architecture]], [[fundamentals-of-software-architecture#chapter-8-component-based-thinking]].

## Pattern: Design event-driven communication between services

*Examples*: "Should this be a synchronous call or an event?"; "Orchestration or choreography for this 5-step workflow?"; "How do we publish events atomically with our database writes?"; "We adopted Kafka — now what?"

Event-driven questions span three MOCs that collaborate closely: the *integration substrate* (brokers, topologies, event contracts), the *correctness bridge* (saga, outbox, idempotence, effectively-once), and the *execution mechanics* (stream-processing internals, CDC, log-based brokers). Answer only from one and you'll produce a plan that's either over-engineered on correctness, under-engineered on operations, or misses the architectural trade-off the team is actually wrestling with.

Read: [[moc-events-and-streaming]], [[moc-consistency-and-transactions]], [[moc-microservices]], [[moc-distributed-systems]], [[moc-data-processing]].

Key concept pages: [[event-driven-architecture]], [[event-driven-microservices]], [[synchronous-microservices]], [[event-broker]], [[log-based-message-brokers]], [[broker-topology]], [[mediator-topology]], [[event-streams]], [[event-structure]], [[event-design-guidelines]], [[schema-evolution]], [[avro]], [[schema-registry]], [[entity-event]], [[event-as-single-source-of-truth]], [[saga]], [[workflow-orchestration]], [[workflow-choreography]], [[outbox-table-pattern]], [[change-data-capture]], [[idempotence]], [[eventual-consistency]].

Key raw chapters: [[fundamentals-of-software-architecture#chapter-14-event-driven-architecture-style]], [[building-event-driven-microservices#chapter-1-why-event-driven-microservices]], [[building-event-driven-microservices#chapter-2-event-driven-microservice-fundamentals]], [[building-event-driven-microservices#chapter-3-communication-and-data-contracts]], [[building-event-driven-microservices#chapter-8-building-workflows-with-microservices]], [[designing-data-intensive-applications#chapter-11-stream-processing]].

For the saga-variant question specifically ("choreography or orchestration?"), read [[moc-consistency-and-transactions]]'s saga-taxonomy section — the *Hard Parts* eight-saga catalogue ([[epic-saga]], [[phone-tag-saga]], [[fairy-tale-saga]], [[time-travel-saga]], [[fantasy-fiction-saga]], [[horror-story-saga]], [[parallel-saga]], [[anthology-saga]]) reframes the decision as three binary axes (communication, consistency, coordination), not a single chevron between "choreo" and "orch".

## Pattern: Adopt SLOs and reliability practices for an existing system

*Examples*: "We have no SLOs and want to start — what's a sensible adoption path?"; "Our alerts wake us up every night and we can't tell signal from noise"; "How do we stop shipping outages — do we need SRE?"

SLO adoption is the operational-discipline question. The load-bearing framing is the error budget as an economic object that converts velocity-vs-reliability from a debate into an accounting exercise. Everything else — monitoring philosophy, on-call design, incident response, postmortem culture, production-readiness review — compounds off that foundation. Answering only with "pick an SLO number and alert on it" misses the organisational practice that makes SLOs actually stick.

Read: [[moc-reliability-and-operations]], [[moc-risk-and-communication]], [[moc-architecture-fundamentals]], [[moc-container-and-serving-patterns]].

Key concept pages: [[sre-discipline]], [[sre-tenets]], [[velocity-vs-reliability-tradeoff]], [[risk-tolerance]], [[error-budget]], [[risk-management-sre]], [[service-level-indicator]], [[service-level-objective]], [[service-level-agreement]], [[slo-expectations]], [[sli-standardization]], [[availability-measurement]], [[monitoring-and-observability]], [[black-box-vs-white-box-monitoring]], [[distributed-tracing]], [[correlation-ids]], [[progressive-delivery]], [[canary-test]], [[feature-toggle]], [[deployment-vs-release]], [[production-readiness-review]], [[launch-coordination-engineering]], [[blameless-postmortem]], [[postmortem-culture-activities]], [[architecture-characteristics]], [[architecture-risk-matrix]].

Key raw chapters: [[site-reliability-engineering#chapter-1-introduction]], [[site-reliability-engineering#chapter-3-embracing-risk]], [[site-reliability-engineering#chapter-4-service-level-objectives]], [[site-reliability-engineering#chapter-6-monitoring-distributed-systems]], [[site-reliability-engineering#chapter-15-postmortem-culture-learning-from-failure]], [[site-reliability-engineering#chapter-27-reliable-product-launches-at-scale]].

## Pattern: Resolve a Conway-caused organisational friction

*Examples*: "Our three-tier architecture has three teams, and every feature takes three quarters to ship"; "We moved to microservices but the teams still match the old monolith layers"; "Who owns this service?"

Conway's law is unforgiving, and most "architecture is slow" complaints are actually Conway complaints. The technical answer without the organisational answer is a non-answer: you can't carve services across a team boundary that doesn't exist, and a service without a clear owner becomes an orphan. This pattern routes into the ownership, team-shape, and change-management material.

Read: [[moc-microservices]], [[moc-decomposition]], [[moc-risk-and-communication]], [[moc-architecture-fundamentals]].

Key concept pages: [[conways-law]], [[team-autonomy]], [[reorganizing-teams]], [[microservice-to-team-assignment]], [[code-ownership-models]], [[measuring-microservice-transition]], [[kotters-change-model]], [[skills-self-assessment]], [[orphaned-services]], [[independent-deployability]], [[communication-structures]], [[trade-off-analysis]].

Key raw chapters: [[monolith-to-microservices#chapter-5-growing-pains]], [[fundamentals-of-software-architecture#chapter-22-making-teams-effective]], [[fundamentals-of-software-architecture#chapter-23-negotiation-and-leadership-skills]].

## Pattern: Choose a database or data model for a new workload

*Examples*: "We need to pick a database for X"; "Relational or document?"; "Do we need a graph DB, a search index, a time-series store?"; "Is polyglot persistence worth the operational cost?"

Model choice dominates; engine choice follows; schema and encoding come next. The failure mode is picking by what's fashionable rather than by the shape of the workload. This pattern also routes into the per-service data-ownership story — "we need a new database" is sometimes actually "we need a new service."

Read: [[moc-data-models-and-storage]], [[moc-data-processing]], [[moc-consistency-and-transactions]], [[moc-data-engineering]].

Key concept pages: [[data-models]], [[relational-model]], [[document-model]], [[graph-data-models]], [[key-value-store]], [[wide-column-database]], [[search-database]], [[time-series-database]], [[nosql]], [[polyglot-persistence]], [[storage-engines]], [[b-trees]], [[sstables-and-lsm-trees]], [[column-oriented-storage]], [[encoding-formats]], [[schema-evolution]], [[backward-forward-compatibility]], [[partitioning]], [[replication]], [[isolation-levels]], [[acid]], [[transactions]], [[technology-selection]], [[data-ownership]], [[database-per-bounded-context]].

Key raw chapters: [[designing-data-intensive-applications#chapter-2-data-models-and-query-languages]], [[designing-data-intensive-applications#chapter-3-storage-and-retrieval]], [[designing-data-intensive-applications#chapter-4-encoding-and-evolution]], [[fundamentals-of-data-engineering#chapter-6-storage]], [[fundamentals-of-data-engineering#chapter-4-choosing-technologies-across-the-data-engineering-lifecycle]].

## Pattern: Evolve a schema or contract without downtime

*Examples*: "We're adding a required field to an API many services consume"; "We want to rename a column used by three pipelines"; "How do we version events so old and new consumers can coexist?"

Schema-evolution questions are really *contracts-between-deployables* questions. They span encoding choices (what format gives forward/backward compatibility), the publication pattern (outbox, broker schemas, API versioning), the rollout pattern (progressive delivery, canary, feature flags), and the consumer-discipline pattern (consumer-driven contracts). The common failure is treating a breaking change as a coordination problem instead of an architectural one.

Read: [[moc-data-models-and-storage]], [[moc-events-and-streaming]], [[moc-consistency-and-transactions]], [[moc-reliability-and-operations]], [[moc-microservices]].

Key concept pages: [[schema-evolution]], [[backward-forward-compatibility]], [[encoding-formats]], [[avro]], [[schema-registry]], [[event-structure]], [[event-design-guidelines]], [[consumer-driven-contracts]], [[deployment-vs-release]], [[feature-toggle]], [[progressive-delivery]], [[canary-test]], [[outbox-table-pattern]], [[change-data-capture]], [[idempotence]].

Key raw chapters: [[designing-data-intensive-applications#chapter-4-encoding-and-evolution]], [[building-event-driven-microservices#chapter-3-communication-and-data-contracts]], [[site-reliability-engineering#chapter-8-release-engineering]].

## Pattern: Build or mature a data platform

*Examples*: "We're bootstrapping a data function — where do we start?"; "Warehouse, lake, lakehouse, or mesh for our stage?"; "How should we think about DataOps vs SRE for our pipelines?"; "We need a data governance program."

Data-platform questions sit at the intersection of the *discipline view* (lifecycle, undercurrents, governance, DataOps), the *storage view* (warehouse / lake / lakehouse / mesh), and the *execution view* (batch and stream pipelines, orchestration, ingestion patterns). The right answer depends heavily on organisational maturity ([[data-maturity]]) — a Stage 1 org that tries to build a Stage 3 platform burns its budget on infrastructure nobody can use.

Read: [[moc-data-engineering]], [[moc-data-models-and-storage]], [[moc-data-processing]], [[moc-reliability-and-operations]], [[moc-security-and-privacy]].

Key concept pages: [[data-engineer]], [[data-engineering-lifecycle]], [[data-maturity]], [[data-architecture]], [[principles-of-good-data-architecture]], [[data-warehousing]], [[data-lake]], [[data-lakehouse]], [[data-mesh]], [[modern-data-stack]], [[technology-selection]], [[dataops]], [[orchestration]], [[data-ingestion]], [[etl-vs-elt]], [[data-transformation]], [[data-serving]], [[data-governance]], [[data-quality]], [[metadata]], [[master-data-management]], [[data-modeling]], [[batch-processing]], [[stream-processing]], [[change-data-capture]], [[data-integrity-sre]].

Key raw chapters: [[fundamentals-of-data-engineering#chapter-1-data-engineering-described]], [[fundamentals-of-data-engineering#chapter-2-the-data-engineering-lifecycle]], [[fundamentals-of-data-engineering#chapter-3-designing-good-data-architecture]], [[fundamentals-of-data-engineering#chapter-4-choosing-technologies-across-the-data-engineering-lifecycle]], [[site-reliability-engineering#chapter-25-data-processing-pipelines]].

## Pattern: Secure and govern a data platform (privacy + compliance)

*Examples*: "What does least privilege actually look like for our data lake?"; "How do we handle GDPR right-to-be-forgotten requests?"; "Our backup strategy hasn't accounted for ransomware — what does defense-in-depth look like for data?"; "We need to pass a SOC 2 audit."

Security-and-privacy for a data platform is dual-MOC by design: the security discipline owns the mindset, primitives, and governance; the reliability MOC owns the availability-and-restore side of the same backups and monitoring pages. Answer from only one lens and you'll produce a plan that either treats backups as a confidentiality problem with no restore story, or as an availability problem with no ransomware posture.

Read: [[moc-security-and-privacy]], [[moc-data-engineering]], [[moc-reliability-and-operations]], [[moc-data-models-and-storage]].

Key concept pages: [[data-security]], [[least-privilege]], [[zero-trust-security]], [[defense-in-depth-data]], [[encryption-at-rest]], [[encryption-in-transit]], [[secrets-management]], [[security-monitoring]], [[data-governance]], [[data-lifecycle-management]], [[data-quality]], [[metadata]], [[backups-vs-archives]], [[data-integrity-sre]], [[data-integrity-failure-modes]], [[data-integrity-principles]].

Key raw chapters: [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]], [[site-reliability-engineering#chapter-26-data-integrity-what-you-read-is-what-you-wrote]].

## Pattern: Respond to a cascading-failure or recurring reliability incident

*Examples*: "A small blip turned into a full outage — why?"; "Our retries made things worse"; "Same incident pattern every quarter — what do we do structurally?"; "Running an incident as incident commander."

Cascading-failure questions are distinctive in that the naive fix (retry, autoscale) actively makes things worse. This pattern routes into overload-and-retry dynamics, the incident-response practice (ICS, roles, communications), and the postmortem-and-learning loop. The architectural half — circuit breakers, bulkheads, load shedding, graceful degradation — sits alongside the organisational half (ICS roles, blameless postmortems, review process).

Read: [[moc-reliability-and-operations]], [[moc-distributed-systems]], [[moc-container-and-serving-patterns]], [[moc-consistency-and-transactions]].

Key concept pages: [[cascading-failure]], [[cascading-failure-triggers]], [[addressing-ongoing-cascading-failure]], [[testing-for-cascading-failures]], [[server-overload]], [[handling-overload]], [[retry-budget]], [[retry-amplification]], [[circuit-breaker]], [[timeouts]], [[graceful-degradation]], [[load-shedding]], [[robustness-and-resiliency-at-scale]], [[incident-command-system]], [[incident-commander]], [[incident-management-framework]], [[incident-response-mindset]], [[declaring-an-incident]], [[unmanaged-incident-anti-patterns]], [[blameless-postmortem]], [[postmortem-template]], [[postmortem-review-process]], [[postmortem-culture-activities]].

Key raw chapters: [[site-reliability-engineering#chapter-21-handling-overload]], [[site-reliability-engineering#chapter-22-addressing-cascading-failures]], [[site-reliability-engineering#chapter-14-managing-incidents]], [[site-reliability-engineering#chapter-15-postmortem-culture-learning-from-failure]], [[designing-data-intensive-applications#chapter-8-the-trouble-with-distributed-systems]].

## When no pattern fits

The patterns above are deliberately broad, but they won't cover every question. If you land here, walk through [[index]]'s MOC table and pick the 2–4 most plausible MOCs to read before drafting. Then, if the question turns out to recur (same shape, different domain), add it as a new pattern so the next agent has a shortcut.

## Related pages

- [[index]]
- [[moc-architecture-fundamentals]]
- [[moc-risk-and-communication]]
- [[moc-architecture-styles]]
- [[moc-components-and-partitioning]]
- [[moc-decomposition]]
- [[moc-microservices]]
- [[moc-domain-driven-design]]
- [[moc-data-models-and-storage]]
- [[moc-data-processing]]
- [[moc-data-engineering]]
- [[moc-distributed-systems]]
- [[moc-consistency-and-transactions]]
- [[moc-events-and-streaming]]
- [[moc-container-and-serving-patterns]]
- [[moc-reliability-and-operations]]
- [[moc-security-and-privacy]]
