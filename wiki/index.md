# Wiki Index

## Source summaries

| Page | Description |
|---|---|
| [[designing-data-intensive-applications]] | Book by Martin Kleppmann — concepts, organization, and ingestion status |
| [[monolith-to-microservices]] | Book by Sam Newman — concepts, organization, and ingestion status |
| [[designing-distributed-systems]] | Book by Brendan Burns — concepts, organization, and ingestion status |
| [[fundamentals-of-software-architecture]] | Book by Mark Richards & Neal Ford — concepts, organization, and ingestion status |
| [[building-event-driven-microservices]] | Book by Adam Bellemare — concepts, organization, and ingestion status |

## Architecture fundamentals

| Page | Description |
|---|---|
| [[software-architecture-definition]] | The four-part Richards-Ford definition: structure + characteristics + decisions + design principles |
| [[laws-of-software-architecture]] | First Law: everything is a trade-off. Second Law: why beats how |
| [[architect-expectations]] | The eight behavioural expectations placed on any architect regardless of title |
| [[architecture-decisions-vs-design-principles]] | Hard-and-fast rules vs guidelines; variance and ARB governance; Chapter 19's architecturally-significant test and five factors |
| [[architecture-decision-record]] | Nygard's ADR template (Title / Status / Context / Decision / Consequences) plus Compliance and Notes; RFC status; cost / cross-team / security approval triggers; wiki storage by scope; ADRs as documentation and as standards |
| [[architecture-decision-anti-patterns]] | Three progressive decision anti-patterns — Covering Your Assets (no decision), Groundhog Day (no justification), Email-Driven Architecture (no single system of record); ADRs as the cure |
| [[architecture-characteristics]] | The "-ilities" as a first-class dimension; three-criteria test; operational/structural/cross-cutting; least-worst-architecture principle |
| [[identifying-architecture-characteristics]] | Three sources (domain concerns, requirements, implicit domain knowledge); the domain-to-ility translation; top-three consensus; drop-one sharpening; the Vasa over-specification case |
| [[measuring-architecture-characteristics]] | Objective definition as the prerequisite to governance; the three measurement axes (operational, structural, process); performance budgets, K-weight budgets, coverage and pipeline metrics |
| [[architectural-quantum]] | The independently-deployable unit with high functional cohesion and synchronous connascence; the scope at which architecture characteristics apply; monolith = 1, microservices = many; Going, Going, Gone kata |
| [[cyclomatic-complexity]] | McCabe's 1976 structural metric; E − N + 2; thresholds (< 10, < 5 preferred); Crap4J; TDD's emergent effect; CC as a fitness function |
| [[architecture-governance]] | Steering the project so declared characteristics hold; the XP → CI → DevOps → governance progression; Checklist Manifesto framing; fitness functions as the primary mechanism |
| [[architecture-katas]] | Ted Neward's 45-minute team exercise for drilling characteristic identification; Silicon Sandwiches worked kata |
| [[architecture-vitality]] | Continuous analysis; structural decay as its opposite |
| [[evolutionary-architecture]] | Architecture designed to change gracefully; fitness-function-driven governance |
| [[architecture-fitness-function]] | Objective automatable integrity assessment of an architecture characteristic; atomic/holistic/triggered/continual/static/dynamic axes; JDepend, ArchUnit, NetArchTest, Simian Army |
| [[unknown-unknowns]] | Rumsfeld's framing; why all architecture becomes iterative |
| [[architect-role-intersections]] | Architecture now intersects engineering practices, ops/DevOps, process, and data |
| [[architectural-thinking]] | The architect's cognitive stance; four aspects (architecture-vs-design, breadth, trade-offs, business drivers) |
| [[architecture-versus-design]] | Why the handoff model fails; bidirectional collaboration as the fix |
| [[technical-breadth-vs-depth]] | The three-tier knowledge pyramid; breadth-over-depth for architects; the frozen caveman anti-pattern |
| [[trade-off-analysis]] | Architecture is the stuff you can't Google; Hickey's warning; the auction-system worked example |
| [[balancing-architecture-and-coding]] | The bottleneck trap; techniques for keeping the architect hands-on |

## Risk analysis

| Page | Description |
|---|---|
| [[architecture-risk-matrix]] | Richards & Ford's 3×3 impact × likelihood grid (ratings 1–9; bands 1–2 / 3–4 / 6–9); the risk-assessment report with row/column totals, audience filtering, and the plus/minus and arrow-with-target techniques for direction; fitness functions as the direction signal |
| [[risk-storming]] | Collaborative risk-identification session — silent individual phase, then consensus, then mitigation; one dimension per session; the nurse-diagnostics three-session walkthrough; the structural parallel with event storming |

## Communicating architecture

| Page | Description |
|---|---|
| [[architecture-diagramming]] | The diagramming soft skill — representational consistency; the Irrational Artifact Attachment anti-pattern and the low-fidelity-first discipline; the three standards (UML; C4's Context/Container/Component/Class; ArchiMate); the six diagram guidelines with the solid-vs-dotted synchronous/asynchronous line convention |
| [[architecture-presentation]] | The presenting soft skill — document-vs-presentation time control; transitions and animations; the Bullet-Riddled Corpse and Cookie-Cutter anti-patterns; the Incremental Build pattern; infodecks vs presentations; the two-channel (verbal/visual) model; Invisibility as deliberate emphasis |

## Components and partitioning

| Page | Description |
|---|---|
| [[components]] | Hub page: the physical packaging of modules; libraries/layers/services; the architect's unit of design; link out to Part II style chapters |
| [[technical-vs-domain-partitioning]] | The top-level partitioning axis; CatalogCheckout change-smear; trade-offs; Inverse Conway Maneuver; industry drift toward domain |
| [[component-identification-cycle]] | Five-step iterative loop; why step 4 (characteristics analysis) turns monolith designs into distributed ones |
| [[entity-trap]] | Named anti-pattern: one *Manager per database entity; ORM in architectural clothing; Naked Objects / Rails as the legitimate alternative |

## Architecture styles

| Page | Description |
|---|---|
| [[monolithic-vs-distributed]] | The top-level split for every Part II style chapter; what distribution buys vs what it costs; relationship to partitioning and the quantum |
| [[fallacies-of-distributed-computing]] | Deutsch's 1994 eight fallacies; architect-facing summary with DDIA cross-links; stamp coupling and the bandwidth worked example |
| [[layered-architecture]] | The n-tier default; closed vs open layers and layers of isolation; the sinkhole anti-pattern with the 80-20 rule; characteristics scorecard (cost/simplicity max, operational ratings low) |
| [[pipeline-architecture]] | Pipes-and-filters; four filter types (producer/transformer/tester/consumer); Unix shells, ETL, Apache Camel, MapReduce; technically partitioned and single-quantum; slightly better modularity/deployability/testability than layered at the same operational ceilings |
| [[microkernel-architecture]] | Plug-in architecture; minimal core + independent plug-in components; plug-in registry and standard contracts; Eclipse/Jira/browsers/tax-prep/claims-processing; the only style that is both technically and domain partitioned; single quantum even in the remote-plug-in variant |
| [[service-based-architecture]] | The pragmatic sweet spot: separately deployed UI + 4–12 coarse-grained domain services + shared monolithic database; ACID transactions preserved; no five-star ratings but many four-star ones; federated shared entity libraries contain schema-change blast radius; the cheapest and simplest distributed style |
| [[event-driven-architecture]] | Distributed asynchronous style built around decoupled event processors; five stars on performance/scalability/elasticity/fault-tolerance; two canonical topologies (broker and mediator); often embedded inside other styles (event-driven microservices, event-driven space-based); the style-level home for the wiki's existing lower-level event machinery |
| [[broker-topology]] | Event-driven architecture's peer-to-peer topology: no central mediator, pub/sub topics, past-tense-fact events, relay-race handoff; architectural extensibility as the killer feature; equivalent to Newman's choreographed saga |
| [[mediator-topology]] | Event-driven architecture's coordinated topology: central mediator, point-to-point command queues, explicit workflow control, error handling with a home, recoverability; Apache Camel / Mule / BPEL / jBPM by complexity; equivalent to Newman's orchestrated saga |
| [[space-based-architecture]] | Tuple-space-inspired distributed style that removes the database from the synchronous request path; processing units + replicated in-memory data grid + asynchronous data pumps; five stars on elasticity/scalability/performance, one star on simplicity/testability/cost; the ticketing/auction/booking burst workload style; hybrid cloud-plus-on-prem deployment as a distinctive option |
| [[processing-unit]] | SBA's compute-and-cache unit: application code + in-memory replicated data grid (Hazelcast/Ignite/Coherence); dynamically scaled; named-cache member lists track scaling automatically; three startup paths (hot/cold/archive) |
| [[data-pump]] | SBA's asynchronous one-way messaging conduit from processing units to the database; the eventual-consistency-by-construction mechanism that keeps the request path DB-free; per-cache vs per-domain granularity; reverse data pumps for cold-start cache hydration |
| [[orchestration-driven-soa]] | Historical cautionary tale: the 2000s enterprise-SOA style with a four-layer service taxonomy (business / enterprise / application / infrastructure) stitched by a central ESB; the reuse-through-orchestration thesis that didn't deliver; one-star on deployability/testability/performance/simplicity/cost; single quantum despite being distributed; the architecture microservices are a direct backlash against |
| [[choosing-architecture-style]] | Chapter 18's selection process: six inputs (domain, characteristics, data, org, process, domain-architecture isomorphism), three decisions (monolith-vs-distributed via quantum analysis, data placement, sync-by-default comms), three deliverables (topology + ADRs + fitness functions); shifting architecture fashion with the six forces; Silicon Sandwiches and Going, Going, Gone worked to resolution |
| [[architecture-style-comparison]] | Cross-cutting scorecard hub across all eight Part II styles; structural-shape table (partitioning, quantum, class); full scorecard on 15 characteristics; four scorecard shapes (cheap-low-ceiling, pragmatic middle, five-star-operational-costly, historical cautionary tale); what the scorecard does not capture |

The ninth Part II style — microservices — is catalogued in *Microservices fundamentals* below, where the canonical page already lived when Chapter 17 was ingested. Richards & Ford's style-level contribution (star-rating, duplication-over-coupling philosophy, SOA-negation placement, operational-reuse-via-sidecars framing) is added as a major section on that page.

## Single-node container patterns

| Page | Description |
|---|---|
| [[sidecar-pattern]] | Two-container pattern: application container augmented by a sidecar through shared namespaces; legacy modernization and modular reuse |
| [[ambassador-pattern]] | Coresident container that brokers the application's outbound connections; sharding, service brokering, request splitting |
| [[pod]] | Atomic container group with shared network, filesystem, and PID namespaces; the Kubernetes substrate for single-node patterns |
| [[modular-reusable-containers]] | Design discipline for reusable sidecars and ambassadors: parameterize, define the API surface, document |
| [[legacy-modernization]] | Adapting pre-existing applications to new requirements (HTTPS, dynamic config, observability) via sidecars rather than source changes |
| [[client-side-sharding]] | Ambassador-pattern use: proxy to a sharded backend from the client's pod (twemproxy/Redis/ketama worked example) |
| [[service-brokering]] | Ambassador-pattern use: introspect the environment and broker the right dependency connection (MySQL across clouds) |
| [[request-splitting]] | Ambassador-pattern use: divert a fraction of traffic for canary, dark launch, or parallel-run teeing |
| [[adapter-pattern]] | Coresident container that transforms the application's outward interface to match a fleet standard (monitoring, logging, health checks) |
| [[unified-monitoring-interface]] | Adapter-pattern use: one metrics interface across heterogeneous apps; Redis + Prometheus exporter worked example |
| [[log-normalization]] | Adapter-pattern use: convert heterogeneous log output into a consistent structured stream; fluentd + Redis SLOWLOG and Apache Storm examples |
| [[health-check-adapter]] | Adapter-pattern use: expose rich application-specific health probes without modifying the upstream image; Go + MySQL worked example |

## Serving patterns

| Page | Description |
|---|---|
| [[replicated-load-balanced-service]] | The simplest multi-node pattern: stateless replicas behind a load balancer; the foundation for the other serving patterns |
| [[health-probes]] | Liveness vs readiness; orchestrator-restart vs load-balancer-deregister; why both are required |
| [[session-tracked-services]] | Sticky sessions via IP hash or cookie/header; consistent hashing for resilience to scaling events |
| [[caching-layer]] | Varnish as a replicated HTTP cache tier; few-large-replicas sizing; interaction with session affinity |
| [[rate-limiting]] | Edge-tier DoS defence; 429 and X-RateLimit-Remaining; anonymous vs authenticated quotas |
| [[ssl-termination]] | Dedicated nginx edge tier; per-layer certificates; the full three-tier serving stack |
| [[sharded-service-pattern]] | The second serving pattern: root + shards; stateful services whose state exceeds one machine; the service-level analogue of DDIA partitioning |
| [[sharded-cache]] | Burns's deep-dive example: memory-utilisation math, hit-rate as capacity multiplier, shard-failure impact, twemproxy + memcached Kubernetes deployment |
| [[replicated-sharded-service]] | Each shard is itself a replicated load-balanced service; shard-failure tolerance and safe rollouts |
| [[hot-sharding]] | Per-shard autoscaling in response to organic traffic skew; the service-level answer to celebrity-key hot spots |
| [[shard-key-selection]] | Choosing what to hash; the "too general / too specific / just right" discussion with the country+path example |
| [[scatter-gather-pattern]] | The third serving pattern: root fans request out to all leaves in parallel and combines partial results; replication for time; two variants (root-distributed vs leaf-sharded) |
| [[tail-latency-amplification]] | Why a backend's p99 becomes the scatter/gather system's p50 at modest fan-out; the straggler problem; availability amplification; mitigations |
| [[functions-as-a-service]] | The fourth serving pattern: short-lived stateless functions triggered by events; when FaaS fits and when it doesn't; benefits, challenges, cost-curve inversion |
| [[event-stream-listener]] | The adapter between an event broker and a FaaS trigger; pulls batches and invokes the function |
| [[faas-triggers]] | What wakes a function up: HTTP, schedule, queue, stream, bucket events; the control-flow input |
| [[faas-offset-management]] | When to commit stream offsets relative to function invocation; at-least-once vs effectively-once |
| [[cold-start-warm-start]] | The first-invocation latency tax; mitigation strategies and the cost/latency/concurrency trade-off |
| [[faas-batch-processing]] | Invoking a function with many events per call; throughput, retry granularity, and poison-pill handling |
| [[faas-function-composition]] | Chaining functions into workflows; orchestration via queues/streams vs a dedicated workflow engine |
| [[serverless-vs-event-driven]] | Burns's opening distinction: two separate axes that FaaS happens to combine; the four corners of the matrix; why the two benefits come from different axes |
| [[faas-decorator-pattern]] | Stateless request/response transformation via FaaS; Python-decorator analogy; defaulting worked example; comparison with adapter containers |
| [[event-pipeline-pattern]] | Directed graph of FaaS handlers connected by webhooks; CI-with-human-approval and new-user-signup worked examples; vs microservices and vs streaming |
| [[ownership-election-pattern]] | The fifth serving pattern: distributing *assignment*; master election + handoff over etcd/ZooKeeper/Consul; when you don't need it and when you do |
| [[singleton-pattern]] | The simplest form of ownership: one replica plus orchestrator-backed restart; three-to-four-nines uptime; the upgrade-window SLA ceiling |
| [[distributed-locks-on-kv-stores]] | Building a correct distributed mutex from compare-and-swap + TTL + resource versions; derivation via fixing the naive implementation's bugs |
| [[renewable-leases]] | Long-running ownership via short TTL + background refresh every `ttl/2`; Kubernetes active-scheduler example |
| [[operator-pattern]] | Application-specific controller inside the orchestrator; declarative desired-state API; CoreOS etcd operator worked example |

## Batch computational patterns

| Page | Description |
|---|---|
| [[work-queue-pattern]] | The first batch pattern: independent items dispatched to worker containers; generic queue-manager + two narrow interfaces; Kubernetes Jobs as durable state |
| [[source-container-interface]] | The producer-side ambassador in a work queue; two-endpoint REST API; deliberate omission of completion tracking |
| [[worker-container-interface]] | The consumer-side file-based interface; `WORK_ITEM_FILE` + ConfigMap mount; Kubernetes Job as reliability substrate; idempotence requirement |
| [[dynamic-worker-scaling]] | Interarrival vs processing time; `P > processing_time / interarrival_time` for a stable queue; the 90%-heuristic for scaling down |
| [[multi-worker-pattern]] | Adapter-pattern specialisation for batch workers; aggregator container composing reusable processing containers behind the standard worker interface |
| [[event-driven-batch-pattern]] | The second batch pattern: chain work queues into workflow DAGs via named linking patterns over a pub/sub broker; workflow-as-specification |
| [[copier-pattern]] | Fan-out primitive: duplicate one stream into N identical streams; video-transcoding worked example |
| [[filter-pattern]] | Drop items not meeting criteria; implemented as a source ambassador wrapping an upstream source; Unix `grep` analogy |
| [[splitter-pattern]] | Route items to different queues by criterion; shipping-notification worked example; subsumes copier and filter |
| [[sharder-pattern]] | Hash-based even distribution across queues; motivated by reliability and failure-zone spreading rather than semantic routing |
| [[merger-pattern]] | Fan-in primitive: combine N upstream sources into one; multi-source adapter; CI-across-many-repos worked example |
| [[publisher-subscriber-infrastructure]] | Kafka/EventGrid/SQS as the workflow transport; Kafka-on-Kubernetes-via-Helm walkthrough; topic-per-output-shard convention |
| [[coordinated-batch-pattern]] | The third batch pattern: pull parallel workflow outputs back together into a single aggregate; Burns's image-tagging worked example composing every batch pattern |
| [[join-pattern]] | Barrier synchronization; hold downstream work until every upstream parallel worker has completed; guards destructive steps and global aggregates |
| [[reduce-pattern]] | Associative pairwise combine that pipelines with upstream work; the container-level naming of MapReduce's reduce step; Burns's count/sum/histogram examples |

## Core system properties

| Page | Description |
|---|---|
| [[reliability]] | Systems that work correctly even when faults occur |
| [[scalability]] | Coping with increased load while maintaining performance |
| [[maintainability]] | Keeping systems workable for engineers and operators over time |
| [[fault-tolerance]] | Preventing component faults from becoming system-wide failures |

## Microservices fundamentals

| Page | Description |
|---|---|
| [[microservices]] | Independently deployable services modeled around a business domain, owning their own data; Richards & Ford's style-catalog framing with star-rating, duplication-over-coupling philosophy, and SOA-negation placement |
| [[monolith]] | Single-process, modular, distributed, and third-party black-box variants; advantages and challenges |
| [[modular-monolith]] | Single-deployable application with stable internal module boundaries; the cheaper alternative Newman invokes throughout |
| [[independent-deployability]] | The central discipline: change and deploy one service without touching any other |
| [[service-granularity]] | The hardest decision in microservices and the dividing axis across Part II styles; the three Chapter-17 guidelines (purpose, transactions, choreography); "fix granularity, not transactions" |
| [[conways-law]] | Systems mirror the communication structure of the organizations that build them |

## Microservice migration

| Page | Description |
|---|---|
| [[why-microservices]] | The three-question test; legitimate motivations and a cheaper alternative for each |
| [[when-microservices-are-a-bad-idea]] | Unclear domain, true startups, customer-installed software, no clear reason |
| [[incremental-migration]] | Chip away one service at a time; production is what counts |
| [[reversible-vs-irreversible-decisions]] | Bezos's two-way / one-way doors applied to migration choices |
| [[cost-of-change]] | Push experiments toward the whiteboard; database splits are the expensive end |
| [[extraction-prioritization]] | Two-axis effort/benefit model for picking the first service to extract |
| [[event-storming]] | Brandolini's collaborative bottom-up domain modelling technique |
| [[robustness-vs-resilience]] | David Woods's distinction; microservices give you neither for free |
| [[measuring-microservice-transition]] | Quantitative + qualitative; checkpoints; the sunk cost fallacy |

## Migration patterns

| Page | Description |
|---|---|
| [[migration-pattern-selection]] | Choosing among the patterns; can-you-change-the-monolith; copy vs reimplement |
| [[strangler-fig-pattern]] | Intercept calls at the perimeter; new service grows alongside the monolith |
| [[branch-by-abstraction]] | In-place migration via abstraction + alternative implementation; for deep functionality |
| [[parallel-run-pattern]] | Run both implementations on every call; compare results; high-risk verification |
| [[decorating-collaborator-pattern]] | Proxy triggers new-service calls based on monolith's request/response |
| [[ui-composition]] | Splice UI from old and new at page, widget, or micro-frontend level |
| [[seams-and-legacy-code]] | Feathers's seam concept; the refactoring unit inside the monolith |
| [[deployment-vs-release]] | The separation that makes all the patterns possible |
| [[feature-toggle]] | Runtime switches for cutover and rollback |
| [[progressive-delivery]] | Umbrella for parallel run, canary, dark launch, feature toggles |

## Database decomposition

| Page | Description |
|---|---|
| [[database-decomposition]] | Hub page: why split the database; the pattern catalogue and Newman's sequencing guidance |
| [[shared-database-antipattern]] | Multiple services on one schema; what's wrong, where it's acceptable |
| [[database-view-pattern]] | Read-only projection from a shared schema; coping pattern |
| [[database-wrapping-service]] | Thin service in front of a tangled schema; converts DB dependencies to service dependencies |
| [[database-as-a-service-interface]] | Expose a separate read-only DB as a managed endpoint; generalised reporting database |
| [[aggregate-exposing-monolith]] | New service calls back to monolith for data the monolith still owns |
| [[change-data-ownership]] | Move data into the new service; invert the dependency |
| [[synchronize-data-in-application]] | Three-step pattern for migrating data with rollback safety; Trifork medical-records example |
| [[tracer-write]] | Incrementally move source of truth; tolerate two sources during migration; Square Fulfillments |
| [[split-the-database-first]] | Sequencing — schema-first vs code-first vs both-at-once; physical vs logical separation |
| [[repository-per-bounded-context]] | Factor data-access code along context lines as a first step |
| [[database-per-bounded-context]] | Separate schemas inside a modular monolith; preserves future extraction options |
| [[monolith-as-data-access-layer]] | Expose an API on the monolith; JustSocial's pattern |
| [[multischema-storage]] | New service holds its own schema for new data while still reading from the monolith |
| [[split-table-pattern]] | Separate a table whose columns belong to different bounded contexts |
| [[move-foreign-key-to-code]] | Replace a cross-service DB join with a service call; handle referential-integrity fallout |
| [[shared-static-data]] | Four patterns for country-code-style reference data: duplicate, dedicated schema, library, service |
| [[saga]] | Coordinate multi-service operations without distributed locks; orchestrated vs choreographed; compensating actions |
| [[workflows-in-edm]] | Multi-step business processes in an event-driven system; choreographed vs orchestrated realizations |
| [[compensation-workflow]] | The undo half of a saga: explicit compensating events that roll back committed local steps |

## Team and organization

| Page | Description |
|---|---|
| [[team-autonomy]] | Gore, Timpsons, two-pizza teams; how microservices amplify (and don't grant) autonomy; Richards & Ford's elastic-leadership complement |
| [[reorganizing-teams]] | Moving from competency silos to product teams; don't copy the Spotify model |
| [[skills-self-assessment]] | Private 1-5 self-rating; anonymised aggregate informs team-level investment |
| [[kotters-change-model]] | Eight-step process for organisational change applied to microservice adoption |
| [[code-ownership-models]] | Strong, weak, collective; collective stops working past ~20 devs; strong "almost universal" past 100 |
| [[global-vs-local-optimization]] | Local team decisions compose into global duplication; cross-cutting forums without centralising |
| [[architect-control-spectrum]] | Richards & Ford's three architect personalities (control freak / armchair / effective) and the elastic-leadership five-factor dial; the three team warning signs (process loss, pluralistic ignorance, diffusion of responsibility) |
| [[architectural-checklists]] | When to use checklists and when not to; the three canonical lists (code completion, unit/functional testing, software release); Gawande's *Checklist Manifesto*; the Hawthorne effect for governance |
| [[architect-providing-guidance]] | Design-principle guidance as the alternative to prescription; the two-question library filter (overlap + technical *and* business justification); the Scala-enthusiast anecdote; the three-category layered-stack demarcation |
| [[architect-negotiation]] | Richards & Ford's Chapter 23 negotiation techniques per counterparty: stakeholders (five-nines-to-seconds reframing, grammar, validate-before-redirect, divide-and-conquer, save-cost-for-last), peer architects (demonstration defeats discussion; calm leadership), developers (justification before demand; let them arrive at the solution; Ivory Tower anti-pattern) |
| [[architect-leadership-skills]] | The 4 C's of architecture (communication, collaboration, clarity, conciseness) as the antidote to architect-introduced accidental complexity; pragmatic-yet-visionary balance; leading by example (not title) with collaborative grammar and people-skills techniques; meeting control as the integration mechanism |
| [[architect-career-path]] | Chapter 24's career-long practice loop — the 20-minute rule (learn something daily, first thing in the morning before email); the personal developer radar (four quadrants x four rings adapted from ThoughtWorks, with Hold extended to cover habits to break); McAfee's weak-link argument for social media populating the Assess ring; architecture katas as deliberate practice; "always learn, always practice, and go do some architecture" |

## Microservices at scale

| Page | Description |
|---|---|
| [[breaking-changes]] | Eliminate accidental contract breakage or the architecture becomes untenable; structural vs semantic; three rules |
| [[consumer-driven-contracts]] | Pact-style consumer-written specifications; replace cross-service tests; "poorly underused" |
| [[end-to-end-testing]] | Large cross-team suites become slow and flaky; limit scope, use CDCs, lean on progressive delivery |
| [[cross-service-analytics]] | Split databases break single-schema analytics; push to a dedicated analytics database |
| [[local-developer-experience]] | JVM hits the laptop ceiling; stubbing, hybrid setups, Telepresence; ongoing investment |
| [[running-too-many-things]] | Manual deployment doesn't scale; serverless-first on cloud; Kubernetes when needed |
| [[desired-state-management]] | Declarative spec + continuous reconciliation; the operational counterpart to many small services |
| [[robustness-and-resiliency-at-scale]] | Two questions per call; isolation, time-outs, circuit breakers; document what you learn |
| [[circuit-breaker]] | Fail-fast wrapper around a remote call; open/closed/half-open states; stops cascading failure |
| [[bulkhead]] | Isolate resources per dependency so one failing call path can't exhaust the whole pool |
| [[orphaned-services]] | Services running for years with no owner; FT's Biz Ops and the System Operability Score |

## Observability

| Page | Description |
|---|---|
| [[monitoring-and-observability]] | From monitoring (known causes) to observability (open-ended questions); the murder-mystery quote |
| [[log-aggregation]] | Newman's "do this first" recommendation; ELK and Humio; an organisational litmus test |
| [[distributed-tracing]] | Jaeger and friends; latency attribution where logs can't help |
| [[synthetic-transactions]] | Test in production via scripted fake users; the 200-washing-machines warning |

## Domain-driven design

| Page | Description |
|---|---|
| [[domain-driven-design]] | Eric Evans's discipline for modeling the problem domain in software |
| [[bounded-context]] | A larger organizational boundary with explicit responsibilities and hidden internals |
| [[aggregate]] | A real domain entity (Order, Invoice) with a self-governing state-machine life cycle |

## Coupling and cohesion

| Page | Description |
|---|---|
| [[modularity]] | Richards & Ford's umbrella: logical grouping of related code; the implicit characteristic; the three measurement tools |
| [[coupling]] | Four types from Newman (implementation, temporal, deployment, domain) plus the Structured Design afferent/efferent axes |
| [[cohesion]] | "The code that changes together, stays together"; Constantine's seven-level scale; LCOM; business vs technology cohesion |
| [[coupling-metrics]] | Afferent/efferent coupling; Martin's abstractness, instability, and distance from the main sequence |
| [[connascence]] | Page-Jones's framework: five static types, four dynamic types, three properties (strength, locality, degree) |
| [[information-hiding]] | Parnas's principle: stable interfaces hide what changes; the engine of independent deployability |

## Scalability concepts

| Page | Description |
|---|---|
| [[load-parameters]] | Quantitative metrics describing current system load |
| [[response-time-percentiles]] | Why percentiles beat averages for measuring service performance |
| [[scaling-approaches]] | Vertical, horizontal, elastic, and manual scaling tradeoffs |

## Maintainability concepts

| Page | Description |
|---|---|
| [[accidental-complexity]] | Complexity from implementation choices, not the problem itself |

## Data models

| Page | Description |
|---|---|
| [[data-models]] | The layered abstraction concept; overview of the three dominant models |
| [[relational-model]] | SQL, tables, joins, history, and the query optimizer insight |
| [[document-model]] | JSON documents, schema flexibility, and data locality advantages |
| [[graph-data-models]] | Property graphs, triple-stores, Cypher, SPARQL, and Datalog |
| [[nosql]] | The NoSQL movement, driving forces, and polyglot persistence |

## Data modeling concepts

| Page | Description |
|---|---|
| [[object-relational-mismatch]] | Impedance mismatch between OOP code and relational tables |
| [[normalization]] | Removing duplication with IDs; the join trade-off |
| [[schema-on-read-vs-write]] | Enforcing schema at write time (relational) vs read time (document) |
| [[declarative-vs-imperative-queries]] | Why declarative languages (SQL, CSS) beat imperative APIs |
| [[data-locality]] | Adjacent storage for faster full-document reads; trade-offs |

## Storage engines

| Page | Description |
|---|---|
| [[storage-engines]] | Two families (log-structured vs update-in-place) and OLTP vs OLAP split |
| [[indexes]] | What an index is; read/write tradeoff; clustered, covering, multi-column, fuzzy |
| [[hash-indexes]] | Append-only log + in-memory hash map (Bitcask); segment compaction |
| [[sstables-and-lsm-trees]] | Sorted segments, memtable, LSM-tree, compaction strategies, Bloom filters |
| [[b-trees]] | Fixed-size pages, WAL, branching factor, comparison to LSM-trees |
| [[write-amplification]] | One logical write causing multiple physical writes; SSD impact |

## Analytics and warehousing

| Page | Description |
|---|---|
| [[oltp-vs-olap]] | OLTP (many small key lookups) vs OLAP (few huge scans for aggregates) |
| [[data-warehousing]] | ETL, star/snowflake schemas, fact and dimension tables |
| [[column-oriented-storage]] | Store by column not row; compression, vectorized processing, OLAP cubes |

## Encoding and compatibility

| Page | Description |
|---|---|
| [[backward-forward-compatibility]] | New code reads old data (backward); old code reads new data (forward); the two directions required for rolling upgrades |
| [[encoding-formats]] | Three categories: language-specific (avoid), textual (JSON/XML/CSV), binary schema-driven (Thrift/Protobuf/Avro) |
| [[schema-evolution]] | Field tags (Thrift/Protobuf) and writer's/reader's schema (Avro) as mechanisms for safe schema change over time |
| [[avro]] | Binary format with no field tags; writer's/reader's schema resolution; ideal for dynamically generated schemas |
| [[data-outlives-code]] | Database records encoded under old schemas persist long after the code that wrote them is gone |
| [[data-contract]] | The producer-consumer agreement enforced by the event format and schema registry; the decoupling mechanism at the heart of EDM |
| [[schema-registry]] | Central store of schemas by subject/version; producers register and consumers fetch; enforcement of compatibility modes |
| [[code-generation]] | Generating typed producer/consumer classes from schemas; compile-time safety and refactor-friendliness |
| [[explicit-vs-implicit-schemas]] | Why explicit schemas always beat implicit ones in EDM; the cost of implicit schemas expressed as consumer fragility |
| [[event-design-guidelines]] | Principles for designing good events: truth, single definition, narrow purpose, thin events, avoiding coupling |
| [[single-purpose-events]] | One event type per business fact; why multi-purpose events break consumer contracts |
| [[singular-event-definition-per-stream]] | Every stream holds exactly one event type; the predictability contract consumers depend on |
| [[event-as-single-source-of-truth]] | The producer's stream is the canonical record; all derived state flows from it |

## Service communication

| Page | Description |
|---|---|
| [[rpc]] | Remote procedure calls, why the local-call abstraction leaks, REST as the honest alternative, gRPC and modern RPC |
| [[message-brokers]] | Async message passing; buffering, fan-out, decoupling; the actor model and distributed actor frameworks |

## Service communication infrastructure

| Page | Description |
|---|---|
| [[service-discovery]] | General problem of locating services across redundant machines; DNS, coordination services, gossip |
| [[service-mesh]] | Per-service local proxies; avoids the shared-smart-pipe problem |
| [[correlation-ids]] | Single ID propagated through call chains; the prerequisite for distributed tracing |

## Replication

| Page | Description |
|---|---|
| [[replication]] | Hub page: why replicate, three architectures, sync vs async, the fundamental tension |
| [[leader-based-replication]] | Single-leader mechanics, sync vs async, WAL/statement/row-based/trigger replication methods |
| [[failover]] | Promoting a new leader; split brain; lost writes; the many ways automatic failover goes wrong |
| [[replication-lag]] | Async replication lag: the three anomalies and why they matter at scale |
| [[read-after-write-consistency]] | Guarantee that users always see their own writes; implementation strategies |
| [[monotonic-reads]] | Guarantee that reads never go backward in time; sticky replica approach |
| [[consistent-prefix-reads]] | Guarantee that causally related writes appear in order; the causality anomaly |
| [[eventual-consistency]] | The weakest useful guarantee: convergence with no time bound; operability implications |
| [[multi-leader-replication]] | Multiple leaders accept writes; multi-datacenter, offline-first, collaborative editing use cases |
| [[write-conflicts]] | Conflict detection and resolution: LWW, merge, CRDTs, custom logic, tombstones |
| [[leaderless-replication]] | Dynamo-style; any replica accepts writes; read repair; anti-entropy; sloppy quorums |
| [[quorums]] | w+r>n overlap guarantee; tuning; sloppy quorums; the many edge cases that break quorum safety |
| [[version-vectors]] | Per-replica version numbers; happens-before vs concurrent; sibling merging |

## Partitioning

| Page | Description |
|---|---|
| [[partitioning]] | Splitting datasets across nodes for scalability; terminology across systems |
| [[partitioning-strategies]] | Key-range vs hash partitioning and their trade-offs for range queries and load distribution |
| [[hot-spots]] | Disproportionate load on a single partition; skew causes and mitigation |
| [[consistent-hashing]] | Hash-based partition boundaries for CDNs; why the term is misleading for databases |
| [[partitioning-secondary-indexes]] | Document-partitioned (local) vs term-partitioned (global) secondary indexes across partitions |
| [[rebalancing-partitions]] | Strategies for redistributing partitions: fixed count, dynamic splitting, proportional to nodes |
| [[request-routing]] | Service discovery for partitioned databases: routing tiers, client-side awareness, ZooKeeper coordination |

## Transactions

| Page | Description |
|---|---|
| [[transactions]] | Grouping reads and writes into all-or-nothing logical units for simplified error handling |
| [[acid]] | The four safety guarantees: Atomicity, Consistency, Isolation, Durability — and how each varies in practice |
| [[isolation-levels]] | The spectrum from weak to strong isolation; what each level prevents and allows |
| [[read-committed]] | Prevents dirty reads and dirty writes; the most basic useful isolation level |
| [[snapshot-isolation]] | MVCC-based consistent snapshots; valuable for backups and analytics but vulnerable to write skew |
| [[mvcc]] | Multi-version concurrency control: multiple committed versions for lock-free consistent reads |
| [[dirty-reads-and-dirty-writes]] | Two race conditions where transactions see or overwrite uncommitted data |
| [[read-skew]] | Nonrepeatable read anomaly: seeing the database at different points in time |
| [[lost-updates]] | Concurrent read-modify-write cycles silently overwriting each other; prevention strategies |
| [[write-skew]] | Two transactions read the same data but write different objects, violating a cross-object invariant |
| [[phantoms]] | One transaction's write changes another's search query results; predicate locks and index-range locks |
| [[serializability]] | Strongest isolation: serial-equivalent execution; three implementation approaches |
| [[two-phase-locking]] | Pessimistic serializability via shared/exclusive locks; readers and writers block each other |
| [[serializable-snapshot-isolation]] | Optimistic serializability (2008) atop snapshot isolation; detects conflicts at commit time |
| [[actual-serial-execution]] | Single-threaded execution with stored procedures; feasible when datasets fit in memory |

## Distributed systems challenges

| Page | Description |
|---|---|
| [[partial-failures]] | The defining characteristic of distributed systems: nondeterministic, partial breakdowns |
| [[unreliable-networks]] | Shared-nothing asynchronous networks; no delivery guarantees; queueing and congestion |
| [[network-faults]] | Practical prevalence of network problems; partitions; fault detection mechanisms |
| [[timeouts]] | The only sure fault detection mechanism; the long-vs-short dilemma; adaptive timeouts |
| [[unreliable-clocks]] | Time-of-day vs monotonic clocks; drift; why timestamps are dangerous for ordering |
| [[clock-synchronization]] | NTP limitations; GPS/PTP/atomic clocks; Google TrueTime; monitoring offsets |
| [[process-pauses]] | GC, VM suspension, disk I/O — causes of unpredictable delays; real-time systems |
| [[truth-and-leadership-in-distributed-systems]] | Why a node cannot trust its own judgment; quorum-based truth |
| [[fencing-tokens]] | Monotonically increasing tokens to reject stale lock holders; ZooKeeper implementation |
| [[byzantine-faults]] | Nodes that lie; Byzantine Generals Problem; where BFT matters and where it doesn't |
| [[system-models]] | Timing models and failure models for reasoning about distributed algorithm correctness |
| [[safety-and-liveness]] | Two categories of properties: safety (nothing bad) vs liveness (something good eventually) |

## Consistency and consensus

| Page | Description |
|---|---|
| [[linearizability]] | Strongest single-object consistency: atomic recency guarantee; cost and implementation |
| [[causal-consistency]] | Preserving cause-and-effect ordering; strongest model without coordination |
| [[lamport-timestamps]] | Sequence numbers consistent with causality; piggyback-maximum mechanism; limitations |
| [[total-order-broadcast]] | Reliable + totally ordered message delivery; equivalent to consensus |
| [[consensus]] | The fundamental agreement problem; FLP impossibility; Paxos/Raft/Zab; epoch numbering |
| [[two-phase-commit]] | Distributed atomic commit; coordinator failure and in-doubt blocking; not fault-tolerant |
| [[distributed-transactions]] | Transactions spanning nodes; XA; database-internal vs heterogeneous; operational problems |
| [[cap-theorem]] | Linearizability vs availability during partitions; historically important but practically limited |
| [[state-machine-replication]] | Deterministic replicas processing same operations in same order stay consistent |
| [[zookeeper]] | Coordination service: consensus-based primitives, failure detection, leader election |

## Batch processing

| Page | Description |
|---|---|
| [[batch-processing]] | The three system types (online, batch, stream); Unix-to-MapReduce-to-dataflow lineage |
| [[unix-philosophy]] | Do one thing well; uniform interface; separation of logic and wiring; transparency |
| [[mapreduce]] | Map, sort, reduce; distributed execution; fault tolerance; limitations |
| [[distributed-filesystems]] | HDFS architecture; NameNode; fault tolerance via replication; data locality |
| [[sort-merge-joins]] | Reduce-side joins: shuffle by key, secondary sort, skew handling techniques |
| [[map-side-joins]] | Broadcast hash join, partitioned hash join, map-side merge join |
| [[dataflow-engines]] | Spark/Tez/Flink: flexible DAGs, pipelining, in-memory state, RDD lineage |
| [[materialization-of-intermediate-state]] | Why MapReduce's full materialization is expensive; how dataflow engines improve it |
| [[batch-workflow-outputs]] | Search indexes, key-value stores, immutable inputs / replaceable outputs philosophy |
| [[hadoop-vs-mpp-databases]] | Schema-on-read vs up-front modeling; diversity of processing; fault tolerance design |
| [[graph-batch-processing]] | Pregel/BSP model: vertex-centric message passing in synchronized rounds |

## Stream processing

| Page | Description |
|---|---|
| [[stream-processing]] | Hub page: bounded vs unbounded data, core concepts, processing patterns |
| [[event-streams]] | What events are; producers, consumers, topics; delivery mechanisms |
| [[log-based-message-brokers]] | Kafka/Kinesis: partitioned append-only logs with consumer offsets and replay |
| [[change-data-capture]] | Making one database the leader for all derived systems via binlog/WAL parsing |
| [[event-sourcing]] | Storing application-level intent events; deriving state; CQRS |
| [[stream-joins]] | Three join types: stream-stream, stream-table, table-table |
| [[windowing]] | Event time vs processing time; tumbling, hopping, sliding, session windows |
| [[stream-processing-fault-tolerance]] | Microbatching, checkpointing, idempotent writes, atomic commits |
| [[stateless-stream-processing]] | Transformations that need no accumulated state; map/filter/branch; the scalability default |
| [[event-transformations]] | Per-event functions: map, filter, flatMap; the workhorse operators |
| [[stream-branching-and-merging]] | Predicate-based splitting of a stream into multiple streams; union/merge of streams into one |
| [[repartitioning]] | Rekeying and reshuffling a stream to co-locate data for joins and aggregations |
| [[copartitioning]] | Partitioning two streams on the same key and partition count so matching keys land together |
| [[stream-table-table-join]] | The three-way join pattern for enriching a stream with two table streams |

## Event structure and types

| Page | Description |
|---|---|
| [[event-structure]] | The envelope: key + value + metadata + timestamp; the substrate every event type builds on |
| [[unkeyed-event]] | Events with no key; for append-only facts that need no co-location; round-robin partitioned |
| [[entity-event]] | Events whose key is a domain entity ID; carry the full entity state; the compacted-stream payload |
| [[keyed-event]] | Events with a key but no full-entity snapshot; for co-location and partial updates |
| [[tombstone]] | Null-valued event signaling deletion; how entity streams represent "gone" under compaction |
| [[log-compaction]] | Broker-side retention by key: keep the latest value per key forever; the mechanism behind entity streams |
| [[table-stream-duality]] | Every stream implies a table and every table implies a stream; the theoretical core of stream processing |

## Determinism in stream processing

| Page | Description |
|---|---|
| [[deterministic-stream-processing]] | Given the same input streams, produce the same output streams; the reprocessing prerequisite |
| [[event-timestamps]] | Event time vs ingestion time vs processing time; the clock the system uses for ordering |
| [[event-scheduling]] | The runtime discipline of picking which event to process next; how processors advance time |
| [[watermarks]] | Progressing notion of "time has passed"; the signal that windows can close |
| [[stream-time]] | The processor's internal clock derived from observed event timestamps |
| [[out-of-order-events]] | Events whose timestamps go backward relative to the stream; causes and mitigations |
| [[late-arriving-events]] | Events whose timestamp is older than the current watermark; grace periods and side outputs |
| [[reprocessing-event-streams]] | Replaying from the beginning to rebuild derived state or apply new logic |

## Stateful streaming

| Page | Description |
|---|---|
| [[stateful-stream-processing]] | Processors that accumulate state across events; aggregations, joins, enrichment |
| [[materialized-state]] | A table view derived from a stream; the query surface for key lookups |
| [[state-store]] | The abstraction for durable per-processor state; internal, external, or global |
| [[internal-state-store]] | State colocated with the processor and backed by a changelog stream; the recommended default |
| [[external-state-store]] | State held in a remote database; flexibility at the cost of latency and coupling |
| [[global-state-store]] | Fully replicated state on every processor instance; for small shared reference data |
| [[changelog-stream]] | The compacted stream that backs an internal state store; enables rebuilds and hot replicas |
| [[hot-replicas]] | Stand-by processor instances tailing the changelog; how stateful services fail over quickly |
| [[state-store-rebuilding-vs-migrating]] | Trade-off on instance restart: replay the changelog fresh, or copy state from a peer |
| [[effectively-once-processing]] | Exactly-once semantics in practice: idempotence plus transactional offset commits |

## Event-driven microservice fundamentals

| Page | Description |
|---|---|
| [[event-driven-microservices]] | Microservices that communicate via durable event streams; Bellemare's organizing architecture |
| [[communication-structures]] | Business, implementation, and data communication structures; Conway's law in the EDM context |
| [[synchronous-microservices]] | The request-response baseline Bellemare contrasts EDM against; the coupling and availability costs |
| [[microservice-topology]] | The logical graph of microservices and the streams connecting them |
| [[business-topology]] | The mapping of business domains and sub-domains onto microservice boundaries |
| [[event-broker]] | The durable immutable log substrate (Kafka, Pulsar) that makes EDM possible |
| [[single-writer-principle]] | One microservice, one stream: the write ownership rule that keeps data sources unambiguous |
| [[consumer-offset]] | Per-consumer-group position pointer in a partitioned log; the basis for replay and progress tracking |
| [[consumer-group]] | The unit of parallel consumption and offset tracking; how multiple instances share a stream |
| [[partition-assignor]] | The algorithm that distributes partitions to consumer-group members; range, round-robin, sticky |
| [[microservice-tax]] | The fixed cost overhead every service pays for infrastructure, ops, tooling, CI/CD |
| [[container-management-system]] | Kubernetes and peers: the scheduling substrate EDM microservices deploy onto |

## Data liberation and integration

| Page | Description |
|---|---|
| [[data-liberation]] | Extracting data from legacy siloed systems into event streams so EDM consumers can use it |
| [[query-based-cdc]] | Periodic polling of source tables; simple but lossy and load-bearing on the database |
| [[outbox-table-pattern]] | Writing events to a same-transaction outbox table and streaming them out asynchronously |
| [[cdc-triggers]] | Trigger-based CDC that inserts into a change table; precise but intrusive |
| [[event-sinking]] | The reverse flow: writing events back into downstream databases for query |
| [[eventification]] | The act of turning request/response APIs or legacy data into first-class events |
| [[data-liberation-framework]] | The organizational capability and tooling for sustained liberation across many sources |

## EDM implementation styles

| Page | Description |
|---|---|
| [[basic-producer-consumer-microservice]] | The simplest EDM shape: consume, process per-event, produce; no framework required |
| [[gating-pattern]] | A guard consumer that admits events into a downstream stream only when a condition is met |
| [[hybrid-bpc-stream-processing]] | Mixing a basic producer-consumer with stream-processing library features as needs grow |
| [[heavyweight-framework-microservice]] | Flink/Spark-style: microservice runs on a cluster that provides scheduling, state, checkpointing |
| [[stream-processing-cluster]] | The shared compute substrate for heavyweight frameworks; JobManager/TaskManager topology |
| [[application-submission-modes]] | Job submission styles in heavyweight frameworks: client, cluster, session, per-job |
| [[checkpointing-stream-processing]] | Periodic durable snapshots of operator state and offsets; the recovery primitive |
| [[external-shuffle-service]] | Cluster-level component that holds shuffle data independent of executor lifetimes |
| [[stream-processing-scaling-strategies]] | Horizontal scaling, parallelism, partition count, and state-store implications |
| [[multitenancy-in-streaming-clusters]] | Running many jobs on one cluster; resource isolation, quota, noisy-neighbor mitigation |
| [[lightweight-framework-microservice]] | Kafka-Streams-style: library embedded in the service; no cluster; coordination via the broker |
| [[broker-as-shuffle-service]] | Using the event broker itself for repartitioning traffic; the lightweight-framework secret |

## Request-response integration with EDM

| Page | Description |
|---|---|
| [[event-driven-request-response-integration]] | Hub: how synchronous clients, external APIs, and UIs plug into an event-driven backbone |
| [[external-events-ingestion]] | Accepting events from outside the organization (webhooks, partner feeds); validation and trust |
| [[third-party-api-integration]] | Wrapping external request-response APIs so EDM services see events instead of synchronous calls |
| [[serving-state-from-edm]] | Exposing read APIs backed by materialized state built from event streams |
| [[smart-load-balancer]] | Partition-aware routing that sends requests to the instance already hosting the relevant state |
| [[request-as-event]] | Modelling a synchronous request as an event with a reply-to stream; turning RPC into async |
| [[asynchronous-ui]] | UIs that display eventual-consistency state and reflect updates as they arrive |
| [[micro-frontends]] | Composing a UI from independently deployed fragments owned by different teams |

## EDM supportive tooling

| Page | Description |
|---|---|
| [[edm-supportive-tooling]] | Hub: the platform services every mature EDM org builds around its broker |
| [[microservice-to-team-assignment]] | The registry that maps services and streams to owning teams; the on-call prerequisite |
| [[event-stream-metadata]] | Per-stream documentation: owner, schema, retention, purpose, SLAs |
| [[event-broker-quotas]] | Per-client throughput and storage limits; noisy-neighbor defense at the broker |
| [[event-stream-acls]] | Who can produce to and consume from each stream; authorization at the broker |
| [[schema-change-notifications]] | Alerting downstream consumers when an upstream schema changes |
| [[application-reset-tool]] | Operational tooling to wipe state and rewind offsets so a service can reprocess from scratch |
| [[consumer-lag-monitoring]] | Tracking how far behind each consumer group is; the primary EDM health metric |
| [[microservice-creation-workflow]] | The paved road: scaffolding, repo, CI/CD, topic ACLs, dashboards created in one step |
| [[cluster-creation-and-management]] | Provisioning and operating broker clusters; the capacity-and-config surface |
| [[cross-cluster-replication]] | MirrorMaker-style replication across regions or environments; DR and data locality |
| [[dependency-tracking-and-topology-visualization]] | Tools that render the live graph of streams and services; the "what calls what" map |
| [[data-lineage]] | End-to-end tracking of how an event flows from source to every derived dataset |
| [[orphaned-streams]] | Streams with no active consumers; the EDM analogue of dead code |

## Testing event-driven systems

| Page | Description |
|---|---|
| [[unit-testing-topology-functions]] | Testing pure per-event functions in isolation; the fastest, cheapest feedback tier |
| [[topology-testing]] | Driving a whole processor topology with fixture inputs in-process; verifying emitted events |
| [[local-integration-testing]] | Running a real broker locally (Docker, Testcontainers) and asserting end-to-end behavior |
| [[remote-integration-testing]] | Running against a shared remote staging environment; isolating per-test via topic namespacing |
| [[hosted-service-mocks]] | Fake implementations of third-party APIs you integrate with; repeatable tests without external flake |
| [[test-data-strategies]] | Synthetic, sampled, and captured-from-prod fixture approaches; privacy and reproducibility trade-offs |

## Deploying event-driven systems

| Page | Description |
|---|---|
| [[edm-deployment-principles]] | The ground rules: reversibility, compatibility, observability, blast-radius control |
| [[edm-deployment-patterns]] | Hub: the canonical deployment patterns and when each applies |
| [[continuous-integration-delivery-deployment]] | CI/CD/CD pipeline shape for EDM services; schema checks and topic provisioning |
| [[basic-full-stop-deployment]] | Stop all instances, deploy, start; the simplest and most disruptive pattern |
| [[rolling-update-pattern]] | Replace instances one by one while consumer-group rebalance handles partition handoff |
| [[blue-green-deployment]] | Two full parallel deployments with traffic cutover; safe rollback at the cost of double capacity |
| [[breaking-schema-deployment]] | Coordinating a producer-consumer schema break across the fleet; dual-write and dual-read phases |

## Future of data systems

| Page | Description |
|---|---|
| [[data-integration]] | Making data available in the right form across multiple specialized systems |
| [[unbundling-databases]] | Decomposing database features into composable systems connected by event logs |
| [[lambda-architecture]] | Running batch and stream in parallel; problems and successors |
| [[derived-data]] | Data created by transforming a system of record; write path vs read path |
| [[end-to-end-argument]] | Infrastructure guarantees are insufficient; application-level operation IDs needed |
| [[exactly-once-semantics]] | Effectively-once via idempotence and end-to-end operation identifiers |
| [[idempotence]] | Operations safe to retry without changing the result beyond the first application; the building block behind effectively-once |
| [[timeliness-and-integrity]] | Two requirements conflated under "consistency"; decoupling them |
| [[coordination-avoidance]] | Maintaining integrity without synchronous coordination |
| [[data-ethics]] | Predictive analytics bias, surveillance, privacy, consent, engineer responsibility |
