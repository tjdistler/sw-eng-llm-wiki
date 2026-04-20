# Wiki Index

## Maps of Content (MOCs)

Narrative entry points for multi-cluster questions. Read the MOC first to find the concepts that compose for a given question shape, then follow wikilinks into concept pages.

| Page | Description |
|---|---|
| [[moc-architecture-fundamentals]] | What software architecture *is* — definition, laws, characteristics (-ilities), the quantum, fitness functions, evolution, ADRs, trade-off discipline, the architect's stance |
| [[moc-risk-and-communication]] | The architect's soft-skills half — risk matrix and risk storming, diagramming, presentation, leadership, providing guidance, negotiation, career path |
| [[moc-architecture-styles]] | The catalogue of canonical styles — layered, pipeline, microkernel, service-based, event-driven, space-based, orchestration-driven SOA, microservices; comparison and choice |
| [[moc-components-and-partitioning]] | The inside-the-box partitioning view — components, technical-vs-domain partitioning, the cohesion/coupling/connascence triad, granularity drivers, *Hard Parts*'s component-decomposition playbook |
| [[moc-decomposition]] | Extracting a service from a monolith — decision frame, seams, extraction patterns, DB decomposition, correctness, org pressure, operational step-up |
| [[moc-microservices]] | Running microservices — defining properties, granularity, data ownership, sync/async/event-driven communication, reuse trade-offs, the platform/substrate, growing pains, organisational shape |
| [[moc-domain-driven-design]] | The modelling discipline — domain/subdomain/bounded context/aggregate vocabulary, event storming and workshop techniques, domain partitioning, the bridge into microservices and data ownership |

## Source summaries

| Page | Description |
|---|---|
| [[designing-data-intensive-applications]] | Book by Martin Kleppmann — concepts, organization, and ingestion status |
| [[monolith-to-microservices]] | Book by Sam Newman — concepts, organization, and ingestion status |
| [[designing-distributed-systems]] | Book by Brendan Burns — concepts, organization, and ingestion status |
| [[fundamentals-of-software-architecture]] | Book by Mark Richards & Neal Ford — concepts, organization, and ingestion status |
| [[building-event-driven-microservices]] | Book by Adam Bellemare — concepts, organization, and ingestion status |
| [[site-reliability-engineering]] | Book edited by Beyer, Jones, Petoff & Murphy — concepts, organization, and ingestion status |
| [[fundamentals-of-data-engineering]] | Book by Joe Reis & Matt Housley — concepts, organization, and ingestion status |
| [[software-architecture-the-hard-parts]] | Book by Ford, Richards, Sadalage & Dehghani — trade-off analysis for decomposing systems, data, and workflows |

## Data engineering discipline

| Page | Description |
|---|---|
| [[data-engineer]] | The role definition: responsibilities, languages, balancing act, internal vs external facing |
| [[data-engineering-lifecycle]] | Five stages (generation, storage, ingestion, transformation, serving) plus six undercurrents |
| [[data-maturity]] | Three-stage model (starting / scaling / leading with data) and how it shapes the engineer's job |
| [[dataops]] | Agile + DevOps + statistical process control applied to data pipelines; a cultural undercurrent |
| [[type-a-vs-type-b-data-engineers]] | Abstraction-focused vs build-focused engineers; why hiring unicorns fails |
| [[data-engineering-history]] | Four-era sketch from 1980s warehousing to the 2020s modern data stack |
| [[data-engineer-stakeholders]] | Upstream (architects, SWEs, DevOps/SRE) and downstream (scientists, analysts, ML, C-suite) collaborators |
| [[data-science-hierarchy-of-needs]] | Rogati's pyramid: why data engineering is upstream of, and equal to, data science |

## Data engineering lifecycle stages

| Page | Description |
|---|---|
| [[source-systems]] | Generation stage; evaluation questions for any source the engineer consumes from |
| [[data-storage-stage]] | Storage stage; why it underpins every other stage; evaluation questions |
| [[data-temperature]] | Hot / lukewarm / cold tiers and cloud archival economics |
| [[data-ingestion]] | Ingestion stage; batch vs streaming, push vs pull, streaming-first checklist |
| [[data-transformation]] | Transformation stage; basic → complex; business logic as driver |
| [[data-serving]] | Serving stage; analytics / ML / reverse ETL; data vanity projects |
| [[analytics]] | BI vs operational vs embedded / customer-facing; self-service; multi-tenancy |
| [[reverse-etl]] | Warehouse-to-source feedback; Hightouch/Census productisation |
| [[etl-vs-elt]] | Transform before load vs after; why ELT rose with cloud warehouses |
| [[feature-store]] | Data-engineering × ML-engineering tool; feature history, sharing, backfill |

## Source systems (FoDE Ch 5)

| Page | Description |
|---|---|
| [[source-system-considerations]] | Expanded Chapter 5 checklist — DBMS, shape, cadence, reliability, ownership, per-undercurrent concerns |
| [[application-database-as-source]] | OLTP-backend producer/consumer tension; extraction patterns; the data-application hybrid |
| [[file-sources]] | Excel, CSV, JSON, XML, TXT as the ubiquitous messy source-system category |
| [[crud]] | Create/Read/Update/Delete; the pattern that loses history at the source |
| [[insert-only]] | Append-only table design that keeps history inside the source |
| [[webhooks]] | Reverse APIs; source pushes to consumer endpoint |
| [[graphql]] | Facebook's query-shaped REST alternative; one API paradigm among four |
| [[data-sharing]] | Cloud-native multitenant data access; data marketplaces; the infrastructure under data-mesh |
| [[key-value-store]] | Simplest NoSQL; cache, session, high-volume KV |
| [[wide-column-database]] | Single-index row-key-partitioned; Bigtable, Cassandra |
| [[search-database]] | Elasticsearch/Solr; text search and log analysis workloads |
| [[time-series-database]] | IoT, metrics, ad-tech; write-heavy, time-ordered storage |

## Data engineering undercurrents

| Page | Description |
|---|---|
| [[data-security]] | Security as undercurrent; people-as-biggest-vulnerability; multi-tenant blast radius |
| [[least-privilege]] | Access-control principle at the heart of the security undercurrent |
| [[data-management]] | Umbrella discipline; DAMA DMBOK definition; the facets |
| [[data-governance]] | Three core categories: discoverability, security, accountability |
| [[metadata]] | Four DMBOK categories: business, technical, operational, reference |
| [[data-quality]] | Accuracy, completeness, timeliness; human + technical problem |
| [[master-data-management]] | Golden records across the organisation |
| [[data-modeling]] | Kimball/Inmon/data vault; avoiding the WORN / data-swamp trap |
| [[data-lifecycle-management]] | Archival, destruction, and GDPR/CCPA compliance |
| [[data-architecture]] | Subset of enterprise architecture; Chapter 3's working definition; operational vs technical |
| [[orchestration]] | DAG-aware scheduling; Airflow and successors; strictly batch |
| [[software-engineering-for-data]] | Core processing code, streaming, IaC, pipelines-as-code |
| [[infrastructure-as-code]] | Declarative infra as version-controlled code |
| [[data-observability]] | DODD; SPC; "data is a silent killer" |
| [[data-catalog]] | Where metadata lives and serves discoverability |

## Data architecture principles

| Page | Description |
|---|---|
| [[principles-of-good-data-architecture]] | Reis & Housley's nine principles for evaluating data-architecture decisions |
| [[well-architected-framework]] | AWS's six pillars; one of two external frameworks behind the nine principles |
| [[cloud-native-principles]] | Google Cloud's five cloud-native principles; the other inspiration |
| [[data-architect]] | The role; technical + business; *Architectus Oryzus* |
| [[loose-coupling]] | Four technical properties; Bezos API Mandate; organisational translation |
| [[finops]] | Cloud cost as architectural signal; cost attacks; graceful spending limits |
| [[zero-trust-security]] | Cloud-native replacement for the hardened perimeter |
| [[shared-responsibility-model]] | Security *of* the cloud vs security *in* the cloud |
| [[elasticity]] | Dynamic and automatic scaling; scale-to-zero; over-scaling pitfalls |
| [[brownfield-vs-greenfield]] | Two project types; strangler vs big-bang; shiny-object syndrome |

## Data architecture patterns

| Page | Description |
|---|---|
| [[data-warehousing]] | Warehouse: OLAP-dedicated DB; Inmon's definition; organisational vs technical; cloud DW |
| [[data-mart]] | Refined warehouse subset per department |
| [[data-lake]] | Raw-first schema-on-read; "data lake 1.0" failures; convergence |
| [[data-lakehouse]] | Lake foundation + warehouse guarantees; converged data platforms |
| [[modern-data-stack]] | Cloud plug-and-play modular components; self-serve; clear pricing |
| [[lambda-architecture]] | Batch + speed + serving; historical influence, practical headache |
| [[kappa-architecture]] | Kreps's 2014 stream-only alternative to Lambda |
| [[dataflow-model]] | Google/Beam "batch as a special case of streaming" |
| [[iot-architecture]] | Devices, gateways, constrained-network ingestion, reverse-ETL control loops |
| [[data-mesh]] | Dehghani's four principles: domain ownership, data as product, self-serve platform, federated governance |
| [[data-as-a-product]] | The organisational stance inside data mesh |

## Technology selection

| Page | Description |
|---|---|
| [[technology-selection]] | Reis & Housley's ten criteria; architecture first, technology second |
| [[speed-to-market]] | "Perfect is the enemy of good"; slow decisions kill data teams |
| [[interoperability]] | JDBC/ODBC work; REST is quirks all the way down; modularity's prerequisite |
| [[total-cost-of-ownership]] | Direct and indirect costs; capex vs opex |
| [[total-opportunity-cost-of-ownership]] | The cost of lost options; the "bear trap" warning |
| [[opex-vs-capex]] | Why the cloud pushed data engineering opex-first |
| [[immutable-vs-transitory-technologies]] | Lindy effect; build transitory around immutable; two-year re-evaluation |
| [[cloud]] | IaaS/PaaS/SaaS; cloud economics; "Cloud ≠ On Premises" |
| [[on-premises]] | Still the default for established companies; modern on-prem ≠ legacy |
| [[hybrid-cloud]] | Analytics-in-the-cloud pattern minimising egress |
| [[multicloud]] | Motivations, disadvantages, "cloud of clouds" |
| [[cloud-repatriation]] | "You are not Dropbox, nor are you Cloudflare" |
| [[data-gravity]] | Why egress fees make cloud decisions sticky |
| [[build-vs-buy]] | Tire analogy; build where you have competitive advantage |
| [[open-source-software]] | Community-managed OSS evaluation factors |
| [[commercial-oss]] | Databricks/Confluent/dbt Labs pattern; COSS evaluation |
| [[proprietary-walled-garden]] | Independent vendors and cloud proprietary services |
| [[monolith-vs-modular-data]] | Data-stack version of the monolith/modular debate |
| [[distributed-monolith]] | The anti-pattern; Hadoop and Python orchestration; container mitigation |
| [[serverless-vs-servers]] | Serverless first; containers next; owned servers last |
| [[containers]] | Lightweight virtualisation; the middle path; security caveats |
| [[benchmark-wars]] | The 787-vs-Tesla analogy; vendor benchmark tricks |
| [[cargo-cult-engineering]] | Copying big-tech without the context |

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
| [[column-oriented-storage]] | Store by column not row; compression, vectorized processing, OLAP cubes |

## Storage systems (FoDE Ch 6)

| Page | Description |
|---|---|
| [[storage-raw-ingredients]] | HDD/SSD/RAM, networking, CPU, serialization, compression, caching hierarchy |
| [[object-storage]] | S3/GCS/Azure Blob; immutable key-value; consistency, versioning, storage classes |
| [[block-storage]] | Raw blocks, RAID, SAN, EBS, instance volumes |
| [[file-storage]] | Local filesystems, NAS, cloud filesystem services; the three file properties |
| [[compression-algorithms]] | gzip, bzip2, snappy, LZ4, LZMA, zstd; the speed/ratio trade |
| [[cache-memory-storage]] | Memcached and Redis as RAM-tier stores |
| [[streaming-storage]] | Kafka/Pulsar/Kinesis/Pub-Sub as long-retention storage with tiered offload |
| [[stream-to-batch-storage]] | Stream fan-out to batch storage; relationship to Lambda |
| [[storage-compute-separation]] | Object storage + ephemeral compute; multitier caching; hybrid object storage |
| [[lakehouse-table-formats]] | Delta Lake, Iceberg, Hudi — ACID + history over object storage |
| [[data-retention]] | Value, time, compliance, cost; lifecycle automation |
| [[data-platform]] | Vendor-curated ecosystem around a storage core; walled-garden trade-offs |

## Ingestion (FoDE Ch 7)

| Page | Description |
|---|---|
| [[data-pipeline]] | Reis & Housley's fluid definition; modern pipelines include ETL, ELT, reverse ETL, and data sharing together |
| [[ingestion-frequency]] | Batch, micro-batch, real-time; why "real-time" is always near-real-time; batch as downstream bottleneck |
| [[push-vs-pull-vs-poll]] | Three directional patterns; who initiates; where each fits; why the lines blur |
| [[ingestion-payload]] | Five payload characteristics: kind, shape, size, schema/types, metadata |
| [[snapshot-vs-differential-ingestion]] | Full-snapshot vs incremental; the "missing intermediate changes" pitfall; link to CDC patterns |
| [[file-based-ingestion]] | Push-style file export; object storage / SFTP / SCP; CSV vs Parquet/Avro/ORC |
| [[data-migration]] | One-time bulk moves; schema subtleties; pipeline-connection cut-over as the hard part |
| [[managed-connector]] | Fivetran/Airbyte/Matillion/Stitch; outsource undifferentiated plumbing |
| [[dead-letter-queue]] | Error-segregation topic; three schema-evolution defenses; poison-message containment |
| [[edi]] | Archaic email/flash-drive transport; automate around it |
| [[web-scraping]] | Legal/ethical caution; HTML-structure churn; downstream architecture implications |
| [[transfer-appliance]] | Physical box of hard drives; Snowball, Snowmobile; 100+ TB one-time migration |

## Queries and query performance (FoDE Ch 8)

| Page | Description |
|---|---|
| [[life-of-a-query]] | Parse, compile to bytecode, optimize, execute; what happens when you press Execute |
| [[query-optimizer]] | Reorders steps and picks join strategies; EXPLAIN as the lever; matches queries to materialized views |
| [[query-performance-tuning]] | Scan less data, pick the right join, avoid row explosion, use CTEs, cache, vacuum, batch over single-row inserts |
| [[broadcast-join]] | Small side shipped to every node; joins local slice of the large side; the cheap case |
| [[shuffle-hash-join]] | Both sides repartitioned by hash of join key; the expensive default |
| [[common-table-expression]] | `WITH ... AS`; preferred over nested subqueries and temp tables; enables SQL DAGs |
| [[window-functions]] | `OVER (PARTITION BY ... ORDER BY ...)`; declarative analytics the optimizer can push down |
| [[user-defined-function]] | Extending the engine with custom code; deterministic vs not; JS/Python UDF performance trap |
| [[nested-data]] | Structs, arrays, maps as first-class column types; the semistructured escape hatch |
| [[streaming-queries]] | Fast-follower CDC, Kappa queries, data-triggered computation; windows and triggers |

## Data modeling paradigms (FoDE Ch 8)

| Page | Description |
|---|---|
| [[conceptual-logical-physical-models]] | Three-step continuum from business abstraction to database implementation; the grain rule |
| [[normalization-levels]] | Denormalized → 1NF → 2NF → 3NF; partial and transitive dependencies |
| [[inmon-model]] | Top-down 3NF integration; department marts downstream; integration as primary virtue |
| [[kimball-model]] | Bottom-up facts + dimensions in star schemas directly in the warehouse |
| [[star-schema]] | Fact table centre, dimensions radiating out; fewer joins than 3NF; analyst-legible |
| [[snowflake-schema]] | Normalized star variant; less common in practice than the plain star |
| [[fact-table]] | Immutable append-only numeric events; narrow and long; lowest-grain rule |
| [[dimension-table]] | Descriptive attributes; wide and short; surrogate keys; conformed dimensions |
| [[slowly-changing-dimensions]] | Type 0/1/2/3 patterns; Type 2 is standard; determinism technique for stream-table joins |
| [[data-vault]] | Linstedt's hubs + links + satellites; insert-only, schema-stable; agile under change |
| [[wide-denormalized-table]] | One very wide table with nested fields; works because columnar storage makes nulls free |
| [[one-big-table]] | The no-modeling extreme; fast to start, trust-erosive |
| [[streaming-data-modeling]] | Flexible schemas, nested columns, trust source-system definitions; the unsettled frontier |

## Transformation stage (FoDE Ch 8)

| Page | Description |
|---|---|
| [[update-patterns]] | Truncate-and-reload, insert-only, delete, upsert/merge, schema update; copy-on-write cost |
| [[upsert]] | Update-on-match, insert-on-no-match; designed for row-based, painful in columnar; the CDC-merge anti-pattern |
| [[materialized-view]] | Precomputed view refreshed on source change; optimizer rewrites; live-table composition |
| [[federated-query]] | Query external sources as if local; Snowflake external tables; can become materialized views |
| [[data-virtualization]] | Trino/Presto; storage-less query engines; query pushdown; data-mesh enabler |
| [[dbt]] | Git-managed templated SQL compiled to warehouse DAGs; analytics-engineering-as-code |
| [[feature-engineering]] | ML-targeted transformation; data scientists design, data engineers automate |
| [[data-wrangling]] | IDEs for malformed data; Reis & Housley push back against dismissing no-code tools |
| [[metrics-layer]] | Authoritative business-logic definitions independent of transformations |

## Serving — general considerations (FoDE Ch 9)

| Page | Description |
|---|---|
| [[trust-in-data]] | Root consideration of serving; two dimensions (quality, SLA); silent death knell when lost |
| [[data-product]] | DJ Patil's definition; jobs-to-be-done; positive feedback loops; three build-time questions |
| [[self-service-analytics]] | Mostly aspirational; succeeds only with the right audience; three classic blockers |
| [[data-definitions-and-logic]] | Meaning vs derivation rules; tribal-knowledge failure; catalog + semantic layer as fix |

## Serving — analytics sub-varieties (FoDE Ch 9)

| Page | Description |
|---|---|
| [[business-analytics]] | Strategic decisions; dashboards, reports, ad-hoc; the running-shorts case |
| [[operational-analytics]] | Immediate action; real-time monitoring; streaming-supplants-batch 10-year forecast |
| [[embedded-analytics]] | Customer-facing; three hard requirements (latency, performance, concurrency); scaling arc |

## Serving — ML fundamentals for DEs (FoDE Ch 9)

| Page | Description |
|---|---|
| [[model-drift]] | Why models degrade; DE's role in drift observability |
| [[training-test-sets]] | Train/test/validation splits; point-in-time correctness; the leakage trap |

## Serving — mechanisms (FoDE Ch 9)

| Page | Description |
|---|---|
| [[semantic-layer]] | Authoritative business definitions; query quality vs data quality; Looker/dbt examples |
| [[file-exchange-serving]] | Ad-hoc file hand-off; five considerations; when to use / when to migrate to data sharing |
| [[serving-in-notebooks]] | Jupyter as a serving target; credential hygiene; scaling off the laptop |

## Security and privacy (FoDE Ch 10)

| Page | Description |
|---|---|
| [[security-theater]] | Compliance-as-performance antipattern; 200-page unread policies; the habit antidote |
| [[active-security]] | Research real attacks, not just checklist items; every engineer involved in their systems' security |
| [[threat-modeling]] | The habit beneath active security; negative thinking; minimise data; enumerate attack scenarios |
| [[encryption-at-rest]] | Baseline for devices, servers, DBs, object storage, backups; useless against credential breach |
| [[encryption-in-transit]] | HTTPS as default; FTP as anti-example; keys and bucket permissions as common undoings |
| [[secrets-management]] | Credentials as configuration; SSO + MFA; secrets managers; never in code |
| [[security-monitoring]] | Access, resource, billing, and excess-permission anomalies; team dashboard |
| [[network-access-security]] | IP allowlists, VPCs, VPN, bastion hosts; the public-S3 / open-SSH catalogue |
| [[security-policy]] | Short, practical, habitual example policy — credentials, devices, software updates |

## Future of data engineering (FoDE Ch 11)

| Page | Description |
|---|---|
| [[future-of-data-engineering]] | Chapter 11 hub — seven predictions about where data engineering is going |
| [[live-data-stack]] | Streaming-first successor to the modern data stack; fuses apps, analytics, ML in real time |
| [[real-time-olap]] | Druid, ClickHouse, Rockset, Firebolt — purpose-built backends for streaming OLAP |
| [[stream-transform-load]] | STL: the streaming-era successor to ELT; transformation happens in the stream |
| [[data-application-fusion]] | Application stacks become data stacks; tight ML feedback loops; throw-it-over-the-wall dies |
| [[cloud-data-os]] | Standardised APIs, formats, catalogs, data-aware orchestration — the cloud as a distributed data OS |
| [[enterprisey-data-engineering]] | Governance, quality, operations trickling down from big-enterprise to every-size company |
| [[titles-will-morph]] | DE/SWE/DS/MLE boundaries blur; new ML-focused engineer between DE and MLE |
| [[spreadsheets-as-data-platform]] | Dark-matter prediction: 700M–2B users; spreadsheet interactivity + cloud OLAP backend |

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
| [[managing-critical-state]] | SRE Ch 23 hub: consensus as the answer to leader election, critical shared state, distributed locking, group membership, and reliable queuing |
| [[consensus-coordination-failures]] | SRE Ch 23's three opening case studies: STONITH-via-heartbeats split-brain, human-escalated failover that doesn't scale, gossip-based membership under partition |
| [[paxos]] | Lamport's 1998 protocol: sequence numbers + majority-quorum overlap; safe but agrees on one value once |
| [[multi-paxos]] | Stable-leader Paxos; one RTT steady-state; dueling-proposers livelock on re-election |
| [[fast-paxos]] | Client-to-acceptor direct sends; sometimes slower because of the latency-tail effect; hard to batch |
| [[flp-impossibility]] | The 1985 result that bounded-time asynchronous consensus is impossible; how production systems sidestep it |
| [[stable-leader]] | The Multi-Paxos/Zab/Raft design pattern; three liabilities (non-local latency, leader bandwidth, leader machine) |
| [[mencius-epaxos]] | Rotating-leader (Mencius) and leaderless (EPaxos) alternatives for wide-area workloads |
| [[replicated-state-machine]] | The deliberate architectural layer above consensus; any deterministic program can be made HA as an RSM |
| [[reliable-replicated-datastore]] | Consensus in the critical path of every write; the ZooKeeper/etcd/Chubby packaging |
| [[distributed-barrier]] | RSM-backed primitive blocking a group until a condition is met; MapReduce phase boundary as the canonical case |
| [[atomic-broadcast]] | Reliable + totally-ordered delivery; Chandra-Toueg equivalence to consensus |
| [[reliable-distributed-queue]] | Queue as RSM; lease-based task claiming; work-distribution vs publish-subscribe shapes |
| [[consensus-performance]] | Workload and deployment axes; the optimisation menu — leaders, leases, batching, disk-log combining |
| [[quorum-leases]] | Read-lease optimisation for geographically concentrated read-heavy workloads |
| [[consensus-read-optimisations]] | Four options for strongly-consistent reads: consensus read, leader read, quorum lease, stale replica |
| [[consensus-disk-access]] | The durable-log bottleneck; combine RSM and consensus logs; batch to amortise disk cost |
| [[consensus-replica-count]] | 2f+1 tolerates f failures; 3 is floor, 5 is practical; why losing quorum is (in theory) unrecoverable |
| [[consensus-replica-placement]] | Failure domains vs latency; the rule that you shouldn't be more geographically robust than your clients |
| [[quorum-composition]] | Linchpin placements across continents; drastic latency jump on linchpin loss |
| [[hierarchical-quorums]] | Majority-of-groups plus majority-of-members; mitigates the flat-quorum linchpin weakness |
| [[consensus-monitoring]] | Member health, lagging replicas, leader existence, leader-change rate, transaction number, proposals |

## Distributed scheduling

| Page | Description |
|---|---|
| [[distributed-cron]] | SRE Ch 24 hub: Google's datacenter-wide cron service; Paxos-replicated state, Fast-Paxos leader as service leader, Borg as backing scheduler, per-datacenter scope sharing fate with Borg |
| [[cron-reliability-challenges]] | Ch 24 — what changes when cron goes distributed: multiple failure domains, container isolation, partial launch failures, diverse replica placement, per-datacenter-not-global scope |
| [[cron-idempotency-and-skip-vs-double-launch]] | Ch 24 — cron jobs span idempotent/non-idempotent and skippable/not-skippable; the fail-closed default (skip rather than double-launch) because skipped launches are usually recoverable while double launches often are not |
| [[cron-leader-follower]] | Ch 24 — Paxos leader holds mutual exclusion to the datacenter scheduler; launches bracketed by synchronous about-to-launch and launch-completed Paxos records; on lost leadership the leader must immediately stop talking to the datacenter scheduler |
| [[cron-partial-failure-resolution]] | Ch 24 — precomputed datacenter-scheduler job names plus scheduled launch time embedded in the name; state lookup on the downstream scheduler as the resolution mechanism; idempotence-or-lookup as the implementation-independent requirement |
| [[cron-state-storage]] | Ch 24 — Paxos logs on local disk only (three copies), snapshots on local disk *and* distributed filesystem; the asymmetric backup strategy from the observation that losing logs is bounded-time loss while losing snapshots is unrecoverable |
| [[cron-thundering-herd]] | Ch 24 — the `?` crontab extension: "any value is acceptable", chosen by hashing the job configuration to distribute launches stably across the range; mitigates the midnight-daily synchronised MapReduce spawn |

## Data processing pipelines

| Page | Description |
|---|---|
| [[data-processing-pipelines]] | SRE Ch 25 hub: the operational pathology of large-scale periodic data pipelines and Google's continuous-processing alternative; the periodic-vs-continuous architectural choice point |
| [[periodic-pipeline]] | Ch 25 — cron-scheduled chained-program design pattern; the depth metric; stable when carefully tuned, fragile under organic growth; the catalogue of failure modes that compound |
| [[pipeline-uneven-work-distribution]] | Ch 25 — the hanging chunk problem: end-to-end runtime capped by largest chunk; standard kill-and-restart wastes all completed work because pipelines have no checkpointing |
| [[pipeline-batch-scheduling-drawbacks]] | Ch 25 — periodic pipelines as low-priority batch jobs: open-ended startup latency, preemption risk, and the execution-frequency floor below which scheduling more often produces overlapping or aborted runs |
| [[pipeline-monitoring-problems]] | Ch 25 — collect-during-report-on-completion is a structural blind spot: jobs that fail mid-run produce no statistics; continuous pipelines escape this by construction |
| [[pipeline-thundering-herd]] | Ch 25 — synchronised worker spawn at start-of-cycle; engineers adding workers to compensate makes the next cycle's herd worse; only fix that addresses the root is to stop being periodic |
| [[moire-load-pattern]] | Ch 25 — multi-pipeline generalisation: pipelines whose schedules drift into occasional alignment produce aggregate spikes on shared resources; visible only in stacked plots |
| [[google-workflow]] | Ch 25 — Google's 2003 continuous data processing system: leader-follower + system prevalence + MVC framing; Task Master as model, stateless workers as view, optional controller for runtime concerns |
| [[task-master]] | Ch 25 — the in-memory model at the heart of Workflow: holds all job state in RAM for fast access, synchronously journals mutations to disk; holds only pointers to work with bulk data in a distributed filesystem |
| [[system-prevalence-pattern]] | Ch 25 — the storage technique Task Master uses: in-memory model + synchronous mutation journal + periodic snapshots; conceptually identical to Redis AOF, event-sourcing, in-memory databases with WAL |
| [[workflow-correctness-guarantees]] | Ch 25 — the four structural mechanisms for exactly-once semantics: configuration tasks as barriers, lease-bound commits, unique output filenames, server-token validation; correctness without requiring idempotent payloads |
| [[workflow-business-continuity]] | Ch 25 — multi-cluster pattern for surviving datacenter loss: local Workflows in distinct clusters plus a global Workflow holding reference tasks; Spanner-backed with Chubby-elected writers |
| [[continuous-data-processing]] | Ch 25 — the architectural alternative the chapter advocates: workers never stop running, work flows in continuously rather than per-cycle; structurally avoids each periodic-pipeline failure mode |

## Data integrity

| Page | Description |
|---|---|
| [[data-integrity-sre]] | SRE Ch 26 hub — user-perspective definition; the 24-hour "too long" threshold; 99.99% good bytes is catastrophic; three-layer defence; two case studies; five closing principles |
| [[data-availability-vs-integrity]] | Ch 26 — data integrity is the means, data availability is the goal; users can't distinguish loss, corruption, and extended unavailability |
| [[data-integrity-failure-modes]] | Ch 26 — the 24 combinations: root cause × scope × rate; Google's empirical finding that app-bug creeping loss dominates; point-in-time recovery |
| [[defense-in-depth-data]] | Ch 26 — the three-layer architecture (soft deletion + backups + validators); replication as overarching optimisation, never a substitute |
| [[soft-deletion]] | Ch 26 layer 1 — trash folder / admin undelete / developer lazy deletion; 15-60 day retention windows; Blobstore's default tombstones |
| [[backups-vs-archives]] | Ch 26 — the distinction (backups are loadable, archives aren't); the "nobody wants backups, they want restores" maxim; designing backward from the recovery requirement |
| [[tiered-backup-strategy]] | Ch 26 layer 2 — local snapshots + distributed-filesystem + offsite tape; retention and restore-time trade-offs; point-in-time recovery; the 1T vs 1E scale argument (trust points, horizontal sharding); redundancy codes and media isolation |
| [[data-validation-pipelines]] | Ch 26 layer 3 — out-of-band MapReduce/Hadoop validators; Google Drive's 2013 auto-repair transformation; engineering-velocity payoff; tiered validation and central-framework organisation |
| [[recovery-testing]] | Ch 26 — the light-bulb analogy; why manual annual DiRT isn't enough; the five things a recovery test must confirm; continuous automation as the only reliable discipline |
| [[gmail-gtape-restore]] | Ch 26 case study — February 2011 first large-scale GTape restore; 99%+ data recovered within estimated window; tape as media diversity |
| [[google-music-runaway-deletion]] | Ch 26 case study — March 2012 runaway deletion; 600,000 audio references deleted for 21,000 users; 5,475 tape restores, 1.5 PB, 7 days; the race-condition root cause |
| [[data-integrity-principles]] | Ch 26 closing — the five principles (beginner's mind, trust but verify, hope is not a strategy, defence in depth, revisit and reexamine); the N→0 recovery-time aspiration |

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
| [[derived-data]] | Data created by transforming a system of record; write path vs read path |
| [[end-to-end-argument]] | Infrastructure guarantees are insufficient; application-level operation IDs needed |
| [[exactly-once-semantics]] | Effectively-once via idempotence and end-to-end operation identifiers |
| [[idempotence]] | Operations safe to retry without changing the result beyond the first application; the building block behind effectively-once |
| [[timeliness-and-integrity]] | Two requirements conflated under "consistency"; decoupling them |
| [[coordination-avoidance]] | Maintaining integrity without synchronous coordination |
| [[data-ethics]] | Predictive analytics bias, surveillance, privacy, consent, engineer responsibility |

## Site Reliability Engineering

| Page | Description |
|---|---|
| [[sre-discipline]] | SRE is what happens when you ask a software engineer to design an operations team; hiring split, the bored-by-manual-work filter, sublinear scaling |
| [[sysadmin-approach]] | The industry-standard alternative SRE replaces; direct and indirect costs; the structural dev-vs-ops conflict and its trench warfare |
| [[devops-vs-sre]] | Treynor Sloss's framing — DevOps as generalisation, SRE as a specific (more opinionated) implementation |
| [[sre-tenets]] | Hub for the eight core responsibilities: availability, latency, performance, efficiency, change, monitoring, emergency response, capacity planning |
| [[error-budget]] | 100% is the wrong reliability target; the SLO's unavailability share is a budget spent on velocity; the mechanism that dissolves the dev-vs-ops conflict |
| [[service-level-objective]] | The reliability target; a product decision, not a technical one; the denominator from which error budgets derive |
| [[toil-and-engineering-balance]] | The 50% cap on operational work; the safety-valve feedback loop; automatic not just automated; the two-events-per-shift on-call target; Ch 5's six toil characteristics, the on-call arithmetic floor, ranked toil sources, and the personal/organisational harms of excess toil |
| [[engineering-work-categories]] | Ch 5's four-way time accounting (software engineering, systems engineering, toil, overhead); which count toward the 50% engineering half and the boundary-case rules (grungy-but-permanent, manually-run scripts, first/second-time work) |
| [[blameless-postmortem]] | Surfacing faults without blame; significant-incident postmortems whether they paged or not; non-paging postmortems as monitoring-gap signals |
| [[mttr-and-mttf]] | Reliability as a function of mean time to failure and mean time to repair; why lowering MTTR (by removing humans) often beats lowering failure frequency |
| [[emergency-response]] | The MTTR-focused tenet; humans add latency; the ~3x advantage of a practised on-call engineer with a playbook |
| [[on-call-playbook]] | Documented troubleshooting steps ahead of the incident; Wheel of Misfortune drills |
| [[change-management-sre]] | 70% of outages come from change; the automation trio — progressive rollouts, fast detection, safe rollback |
| [[capacity-planning]] | Organic + inorganic demand forecasting; load-testing to correlate raw to service capacity; why SRE owns it |
| [[provisioning]] | The intersection of change management and capacity planning; quickly and only when necessary; riskier than load shifting |
| [[sre-efficiency]] | Resource use as a function of demand, capacity, and software efficiency; SRE's control of provisioning as the lever |
| [[sre-monitoring-outputs]] | The only three valid monitoring outputs: alerts, tickets, logs; email-alert-requires-interpretation as the named anti-pattern |
| [[risk-management-sre]] | Chapter 3's framing: risk as a continuum, nonlinear cost, two cost dimensions (redundancy + opportunity), the availability target as both minimum and maximum |
| [[availability-measurement]] | Time-based `uptime/(uptime+downtime)` vs Google's request-success-rate formula; generalisation to non-serving systems; quarterly targets tracked weekly/daily |
| [[risk-tolerance]] | Consumer services (availability, failure shape, cost, non-availability metrics; Google Apps for Work vs YouTube; the $900 nine; ISP background error rate) and infrastructure services (partition by service level; Bigtable low-latency vs throughput clusters; externalise cost to clients) |
| [[service-level-indicator]] | SLI as the metric; direct vs proxy; server-vs-client-side collection; four service-type SLI sets; pick a handful; availability as yield; nines |
| [[service-level-agreement]] | The explicit-or-implicit contract with consequences; the "what happens if the SLOs aren't met?" test; SRE's role in avoiding breaches and defining measurable SLIs; Google Search vs Google for Work |
| [[sli-aggregation]] | Windows, percentiles vs averages; 200-req/even-sec burst example; tail-hidden-by-average; Ch 4 statistical-fallacy warnings against assuming normal distributions |
| [[sli-standardization]] | The six-dimension template (interval, region, frequency, filter, source, latency-definition) that collapses SLI specs from paragraphs to sentences |
| [[slo-expectations]] | Publishing SLOs sets expectations; over-reliance vs under-reliance; safety margin and don't-overachieve tactics; Chubby's synthesized planned outages |
| [[four-golden-signals]] | Ch 6's canonical metrics: latency (success and failure separately), traffic, errors (explicit/implicit/by-policy), saturation (with leading-indicator-via-tail-latency and imminent-saturation predictions); the "measure these four and you're at least decently covered" rule |
| [[symptoms-vs-causes]] | Ch 6's "what vs why" distinction — the single biggest lever for monitoring signal/noise; page on symptoms, debug with causes; one layer's symptom is another's cause in multi-layer systems |
| [[black-box-vs-white-box-monitoring]] | External user-view probing vs internal-metric instrumentation; Google's heavy-white-box plus modest-critical-black-box mix; why black-box is always symptom-oriented and white-box sometimes-symptom-sometimes-cause |
| [[alert-philosophy]] | Ch 6's four principles (urgent / actionable / intelligent / novel) and five-question checklist for new alerts; the Bigtable over-alerting and Gmail rote-response case studies; pager fatigue as the cost of noise |
| [[long-tail-latency]] | Why histograms beat means — the 1%-at-5-seconds example; exponential bucket boundaries; error-latency-separately; tail as leading indicator of saturation; the Bigtable mean-to-75th-percentile switch |
| [[monitoring-resolution]] | Matching measurement granularity to the question; the server-local sampling into buckets plus external minute-granularity aggregation trick; when not to go high-frequency |
| [[monitoring-simplicity]] | The complexity trap (alerts on every percentile, dashboards for every cause); three pruning rules; avoid magic; limit dependency hierarchies; keep monitoring/profiling/log-analysis as distinct loosely-coupled systems |
| [[automation-at-google]] | Ch 7 hub: five values of automation (consistency, platform, faster repairs, faster action, time saving); the five-level hierarchy; three case studies (MoB, cluster turnup, Borg); autonomous-system argument; reliability-is-the-fundamental-feature closing |
| [[hierarchy-of-automation-classes]] | The five-level path: no automation → externally maintained system-specific → externally maintained generic → internally maintained system-specific → autonomous; bit rot and maintainer-incentive arguments for why level 4 beats level 3 |
| [[autonomous-systems]] | Level 5 in detail: automatic-vs-automated, the CPU analogy, preconditions (decoupled subsystems, APIs, minimised side effects, self-introspection), operator-skill-atrophy failure mode |
| [[mysql-on-borg]] | Ch 7 case study: Decider reduced MySQL failover from 30-90 min to under 30 s 95% of the time; 95% ops-work drop, 60% hardware freed; platform-over-script as the lesson |
| [[cluster-turnup-automation]] | Ch 7 case study: shell scripts → Prodtest → idempotent fixes → dedicated turnup team (specialisation trap) → Service-Oriented Architecture with per-service Admin Server RPCs |
| [[prodtest]] | Python unit tests extended to validate real services; dependency-aware chains; paired idempotent fix scripts; the forerunner of modern reconciliation-loop automation |
| [[automation-gone-wrong]] | Ch 7 cautionary tales: the Bigtable disk-zero wipe and Diskerase CDN-wide erase; implicit-safety-signal failure; rate-limiting / audit trails / workflow idempotence as mitigations |
| [[release-engineering]] | Ch 8 hub: the named engineering discipline for building and delivering software; the release-engineer role; four guiding principles; the Rapid + Blaze + MPM + Sisyphus tooling stack; branching and configuration management; start-at-the-beginning and "not-just-for-Googlers" lessons |
| [[release-engineering-principles]] | Ch 8's four principles: self-service, high velocity, hermetic builds, policy enforcement; how they reinforce each other |
| [[self-service-release-model]] | Principle 1 — teams run their own releases; release engineering provides tools, documentation, defaults, and telemetry; the structural reason the model scales at Google |
| [[high-release-velocity]] | Principle 2 — frequent releases mean fewer changes per version; hourly builds with selective deployment vs push-on-green; velocity as a consequence of everything else in the chapter |
| [[hermetic-builds]] | Principle 3 — builds insensitive to the machine; same revision + versioned build tools = identical output; the property that makes cherry-picking onto old branches safe and release audits trustworthy |
| [[release-policy-enforcement]] | Principle 4 — layered access control on the six gated release operations; CL review as first layer; auto-generated release change report for SRE troubleshooting |
| [[rapid-release-system]] | Ch 8 — Google's automated release system; blueprints, workflows, Borg-resident task executors; typical release flow (branch, build-and-test, system-test-and-canary, report); handoff to Sisyphus for complicated rollouts |
| [[blaze-bazel]] | Ch 8 — Google's build tool, open-sourced as Bazel; declarative build targets with explicit dependency graphs; the mechanism behind hermetic builds |
| [[midas-package-manager]] | Ch 8 — MPM: named, hash-versioned, signed packages; movable labels (dev / canary / production) as the promotion primitive; configuration packages |
| [[sisyphus]] | Ch 8 — SRE-developed general-purpose rollout automation framework; Python classes plus dashboard; rollout paced to the risk profile of the service |
| [[release-branching-and-cherry-picking]] | Ch 8 — branch-from-mainline, never-merge-back, cherry-pick-fixes model; what makes each release's contents precisely known; needs hermetic builds and branch-test reruns |
| [[configuration-management-sre]] | Ch 8 — four models for distributing configuration files (mainline, bundled-in-MPM, separate MPM config package, external store); the two universal rules (in-repo + strict code review) |
| [[push-on-green]] | Ch 2 / Ch 8 — every build that passes all tests is automatically deployed; preconditions (hermetic builds, test coverage, change-management trio, error budget); the endpoint of the high-velocity logic chain |
| [[simplicity-sre]] | Ch 9 hub: software simplicity as a prerequisite to reliability; the stability-vs-agility tension; boring as a virtue; deleting code; minimal APIs; modularity and loose coupling between binaries; release simplicity; Hoare's Turing-lecture epigraph |
| [[system-stability-vs-agility]] | Ch 9 — the governing tension; the vacuum thought experiment; reliable processes actually increase developer agility; exploratory coding as a deliberate imbalance |
| [[virtue-of-boring]] | Ch 9 — boring is a desirable property of source code; Muth's "unlike a detective story" quote; Brooks's essential-vs-accidental framing; the SRE mandate to push back on accidental complexity |
| [[negative-lines-of-code]] | Ch 9 — every line in a 24/7 service is a liability; deleting dead code as a high-value activity; the three bad objections (keep for later / comment out / flag) and their answers; the Knight Capital cautionary tale |
| [[minimal-apis]] | Ch 9 — Saint-Exupery's "no longer anything to take away"; small APIs as the hallmark of a well-understood problem; the connection to Newman's expose-as-little-as-possible rule |
| [[release-simplicity]] | Ch 9 — simple releases are better than complicated releases; the gradient-descent analogy; the convergence of the Ch 8 high-velocity and Ch 9 simplicity arguments |
| [[varz-endpoints]] | Ch 10 — Google's standardised `/varz` HTTP metrics exposition format; plain-text key/value pairs, mapped variables for labels; auto-registered in every Google binary; the interface Prometheus inherited essentially unchanged |
| [[time-series-arena]] | Ch 10 — Borgmon's in-memory store of `(timestamp, value)` tuples indexed by labelset; horizon, ~24 bytes per point, ~12 hours typical sizing; older data archived to an external TSDB |
| [[borgmon-rules]] | Ch 10 — Borgmon's algebraic rule language; counters over gauges; sum-of-rates-not-rate-of-sums; aggregation as the cornerstone; the `agg:var:op` naming convention; unit-tested and CI-shipped rule config |
| [[alertmanager]] | Ch 10 — centrally-run alert routing service; deduplicates, inhibits, groups, fans in/out; realises the sre-monitoring-outputs three-bucket routing; name and design inherited by Prometheus |
| [[prober]] | Ch 10 — Google's black-box monitoring tool; protocol checks with payload validation; alerts directly or via its own `/varz`; probes both in front of and behind the load balancer to distinguish localised vs user-visible failure |
| [[monitoring-topology-sharding]] | Ch 10 — the Borgmon hierarchy (scraper shards / DC aggregators / global aggregators); streaming protocol between tiers; filtered pull-up; why two global replicas |
| [[prometheus-connection]] | Ch 10 — explicit genealogy from Borgmon to Prometheus and friends (Riemann, Heka, Bosun); what carried over (pull model, rule language, Alertmanager, federation) and what didn't (BNS, auto-varz, internal CI) |
| [[sre-on-call-engagement]] | Ch 11 — SRE engagement model for on-call; paging response times (5 min / 30 min); primary and secondary rotation patterns; guardian-of-production framing |
| [[balanced-on-call]] | Ch 11 — the two axes (quantity, quality); 25% on-call sub-cap; 8-engineer single-site / 6-engineer dual-site arithmetic; 6-hour-per-incident average → 2-incidents-per-12-hour-shift upper bound |
| [[on-call-compensation]] | Ch 11 — time-off or cash, capped at a salary fraction; the cap as the structural limit that prevents individual overload and burnout |
| [[multi-site-on-call]] | Ch 11 — follow-the-sun rotations preferred once a service justifies growth; night shifts harmful; coordination overhead as the trade-off |
| [[incident-response-mindset]] | Ch 11 — Kahneman intuitive vs rational; stress hormones (cortisol, CRH) impair cognition; confirmation bias as the named trap; escalation paths, incident-management protocol, and blameless postmortems as supporting resources |
| [[operational-overload]] | Ch 11 — measurable overload symptoms; misconfigured monitoring as the common cause; alert fan-out control; give-back-the-pager as last-resort escape hatch; SRE-dev balance of powers |
| [[operational-underload]] | Ch 11 — the treacherous enemy; confidence drift and knowledge gaps surfaced only by incidents; remedies: team sizing (on-call at least 1-2x per quarter), Wheel of Misfortune, DiRT |
| [[troubleshooting-model]] | Ch 12 hub — the six-step loop (problem report → triage → examine → diagnose → test/treat → cure); hypothetico-deductive framing; stop-the-bleeding rule; Shakespeare running example; App Engine whitelist-caching case study |
| [[hypothetico-deductive-debugging]] | Ch 12 — debugging as scientific method; observations + theoretical basis + iteration; knowing what you know / don't know / need to know; system knowledge as the accelerator; the five-whys connection |
| [[triage-sre]] | Ch 12 — fly-the-airplane-first rule; emergency options (divert, drop, disable, freeze); preserve evidence while mitigating; counterintuitive for product-development transplants |
| [[troubleshooting-anti-patterns]] | Ch 12 — the four common pitfalls; horses-not-zebras; Occam vs Hickam; correlation is not causation; latching onto past causes; naming as the antidote |
| [[divide-and-conquer-debugging]] | Ch 12 — simplify-and-reduce; bisection vs linear scan; ask what/where/why with the Spanner regex worked example; "what touched it last" |
| [[test-and-treat]] | Ch 12 — rule-in/rule-out experiments; five considerations (mutual exclusivity, likelihood ordering, confounds, side effects, suggestive tests); written notes; reversibility of active tests |
| [[negative-results]] | Ch 12 sidebar (Bosetti) — disconfirming experiments are conclusive; web-server-lock-contention worked example; tools outlive the experiment; the data-driven culture argument; publish-including-failure as postmortem culture generalised |
| [[making-troubleshooting-easier]] | Ch 12 — design-time disciplines that reduce MTTR: observability from the ground up; well-defined observable interfaces; consistent request IDs; simplify/control/log changes |
| [[test-induced-emergency]] | Ch 13 case study — proactive MySQL dependency test blows up; rollback was never rehearsed; the then-new incident-response process hadn't been disseminated; rule: thoroughly test rollback procedures before large-scale tests |
| [[change-induced-emergency]] | Ch 13 case study — Friday abuse-protection config push crash-loops external Google services and internal tooling; saved by push engineer watching chat, out-of-band communication, and CLI fallback tools; canary must match the combinatorial surface, not the apparent risk |
| [[process-induced-emergency]] | Ch 13 case study — Diskerase CDN wipe retold from the response side; traffic drain, automation freeze, three-day phased manual rebuild; recovery infrastructure is a system in its own right |
| [[learning-from-outages]] | Ch 13 closing — keep a written history of outages; ask the big, improbable questions; encourage proactive testing; follow-through on action items as the accountability rule; "an incident is closed when the follow-ups land" |
| [[incident-management-framework]] | Ch 14 hub — Google's adaptation of FEMA's Incident Command System; the five elements (recursive role separation, named roles, command post, live incident document, handoff); the unmanaged vs managed narrative contrast; best practices |
| [[incident-command-system]] | Ch 14 — FEMA NIMS / FIRESCOPE-derived emergency-response framework; modular, scalable, common-terminology; the source Google adapted; what kept and what was dropped |
| [[unmanaged-incident-anti-patterns]] | Ch 14 — sharp focus on the technical problem, poor communication, freelancing; structural failure modes the framework is designed to defeat; everyone-is-doing-their-job framing |
| [[recursive-separation-of-responsibilities]] | Ch 14 — the organising principle; clear boundaries increase autonomy; IC holds everything not delegated; vertical (sub-incidents) and horizontal (system components) recursion |
| [[incident-commander]] | Ch 14 — the apex coordinating role; structures the response, holds high-level state, removes roadblocks; default holder of every undelegated position |
| [[incident-ops-lead]] | Ch 14 — the technical hands-on role; the *only* group permitted to modify the system during an incident; the structural defence against freelancing |
| [[incident-communications-lead]] | Ch 14 — public face of the response; periodic updates to the team and stakeholders; may keep the incident document current; audience-appropriate framing |
| [[incident-planning-lead]] | Ch 14 — longer-horizon support; bugs, dinners, handoffs, tracking deviations from the norm so they can be reverted |
| [[recognized-command-post]] | Ch 14 — the known place (war room, IRC) for stakeholders to find the IC; reliability, log-as-byproduct, geographic-distribution as Google's IRC rationale; bots that log alerts to the channel |
| [[live-incident-state-document]] | Ch 14 — IC's most important responsibility; concurrently editable (Google Docs); independent of the system being fixed (Google Docs SRE on Sites); messy-but-functional with important info at top; retained for postmortem |
| [[incident-handoff]] | Ch 14 — explicit verbal "you're now the incident commander, okay?" with firm acknowledgment; broadcast to the team; aviation-cockpit derivation; follow-the-sun handoffs |
| [[declaring-an-incident]] | Ch 14 — bias toward declaring early; three-question test (second team / customer-visible / unsolved after an hour); use the framework on planned operations to keep the muscle fresh |
| [[postmortem-philosophy]] | Ch 15 hub — why postmortems exist (scale + velocity → inevitable incidents); three primary goals (document, understand root causes, put preventive actions in place); blameless foundation; not-a-formality framing; the compounding loop |
| [[postmortem-triggers]] | Ch 15 — define criteria before the incident; common triggers (user-visible degradation, data loss, on-call intervention, resolution-time threshold, monitoring failure); stakeholder-requested postmortems; team flexibility with mandatory blamelessness |
| [[postmortem-template]] | Ch 15 — Google Docs template (Appendix D); required capabilities (real-time collaboration, commenting, email notifications); metadata fields for trend analysis; Etsy's Morgue as the public-domain repository |
| [[postmortem-review-process]] | Ch 15 — senior-engineer internal review; five review criteria (data, impact, root-cause depth, action plan, stakeholder sharing); "no postmortem left unreviewed" best practice; regular review sessions; transparent broad sharing |
| [[postmortem-culture-activities]] | Ch 15 — postmortem of the month, Google+ postmortem group, reading clubs, Wheel of Misfortune reenactments; each targets a specific failure mode (filed-and-forgotten, authors-only audience, no external learning, knowledge-dies-with-responder) |
| [[rewarding-postmortems]] | Ch 15 best practice — visibly reward people for doing the right thing; peer bonuses, TGIF public recognition, internal social networks; the four-minute-outage TGIF story; why fear removal alone is insufficient |
| [[postmortem-feedback-surveys]] | Ch 15 best practice — ask for feedback on postmortem effectiveness; the four survey questions (culture, toil, best practices, tools); defence against process calcification; surveys as governance instrument |
| [[postmortems-at-google-working-group]] | Ch 15 — central coordinating group for postmortem practice across Google; template stewardship, incident-tool integration, cross-product trend analysis; forward-looking ML workstreams (weakness prediction, real-time investigation, duplicate detection) |
| [[outage-tracking]] | Ch 16 hub — the baseline-and-progress thesis; tracking every alert and outage as the breadth complement to per-incident postmortem depth; the two-layer Escalator/Outalator architecture; unexpected benefits (cross-team visibility, system-of-record uses) |
| [[escalator]] | Ch 16 — centralised replicated paging system tracking ack/no-ack and auto-escalating on timeout; the transparent-email-copy design that let it integrate with existing workflows without forcing user or monitoring-system change |
| [[outalator]] | Ch 16 — outage tracker built on Escalator; time-interleaved multi-queue view, original-notification storage, important-annotation affordance, grouping, tagging, reporting; dummy-Escalator system-of-record use for audit and non-idempotent periodic jobs |
| [[incident-aggregation]] | Ch 16 — grouping multiple alerts into one logical incident; horizontal vs vertical fan-out; why "incidents per day" and "alerts per day" are distinct useful numbers; post-hoc archival counterpart to Alertmanager's real-time inhibition/dedup |
| [[incident-tagging]] | Ch 16 — free-form colon-namespaced metadata (`cause:network:switch`, `bug:76543`, `bogus`); the avoid-predetermined-list design; `cause:` and `action:` primary prefixes; per-team suggested-prefix feedback loop; probably Outalator's most useful unique feature |
| [[outage-analysis]] | Ch 16 — the three analytic layers (counting, comparison across time/teams, semantic cross-cutting); weekly report mode; shift-handoff email; surfacing over-performing infrastructure that warrants deliberate artificial failures; most-incidents-caused as starting-point-not-verdict |
| [[testing-for-reliability]] | Ch 17 hub — testing as the mechanism for quantifying confidence in change; traditional vs production test taxonomy; zero-MTTR testing as the most potent reliability lever |
| [[zero-mttr-testing]] | Ch 17 — system-level test applied to a subsystem that detects exactly what monitoring would detect, but at push time; blocks the bug from reaching users; raises user-experienced MTBF |
| [[unit-tests]] | Ch 17 — smallest form of testing; verification and specification in one; the base of the traditional-test pyramid |
| [[integration-tests]] | Ch 17 — assembled components with dependency-injected mocks; Dagger as the tool; controlled assembly |
| [[system-tests]] | Ch 17 — largest-scale undeployed test; three flavours (smoke, performance, regression); the expensive batch tier |
| [[smoke-tests]] | Ch 17 — very simple critical behaviour; short-circuits more expensive testing; the highest-impact first test for an untested codebase |
| [[performance-tests]] | Ch 17 — guards against incremental degradation release over release; 8 GB → 32 GB memory, 10 ms → 100 ms response time |
| [[regression-tests]] | Ch 17 — gallery of rogue bugs preserved as recurring assertions; bug-to-test conversion as the cultural practice |
| [[configuration-test]] | Ch 17 — production test comparing checked-in config with the running config; inherently non-hermetic; distributed-monitoring input |
| [[stress-tests]] | Ch 17 — find the catastrophic-failure cliff before production does; calibrates capacity planning and saturation thresholds |
| [[canary-test]] | Ch 17 — not really a test, structured user acceptance; exponential rollout; mathematical framing for fault-order estimation (U=1 regression-testable, U≥2 not) |
| [[testing-at-scale]] | Ch 17 — dependency-closure problem; release tests transitively depend on every object in the repository; Bazel's dependency graph enables selective rebuild-and-test |
| [[testing-scalable-tools]] | Ch 17 — SRE tools need their own tests; barrier-protected tools vs mainstream-API tools vs automation tools; distinct testing profiles |
| [[testing-automation-tools]] | Ch 17 — automation tools' purpose is an invisible side effect to another API client; tests verify the other layer's invariants; circular-dependency case (restart semantics, test coverage, independent checkpoint health) |
| [[testing-disaster-recovery]] | Ch 17 — offline-checkpoint tools are easy to test; online repair tools operate outside the mainstream API and race against eventually-consistent state — significantly harder |
| [[statistical-testing-techniques]] | Ch 17 — Lemon, Chaos Monkey, Jepsen; non-deterministic but useful; log the seed, refactor failures as release tests, escalate when later runs produce worse failures; the SRE-book's earliest chaos-engineering treatment |
| [[test-flakiness-budget]] | Ch 17 — 21,000 tests × 2 (before and after patch) × 1% rejection tolerance → 99.9999% per-test reliability floor; flakiness at scale is structurally unaffordable |
| [[testing-deadlines]] | Ch 17 — interactive (self-contained, seconds) vs batch (orchestrated, minutes-to-hours); the engineer's context-switch as the informal deadline |
| [[break-glass-push]] | Ch 17 — emergency push before tests complete; don't disable tests, run them in parallel and back-annotate; boost test priority; file a bug for a more robust resolution |
| [[build-system-discipline]] | Ch 17 — source control + continuous build + instant breakage notification + fix-the-build-first culture; stability drives agility via emergency-release readiness |
| [[testing-entry-strategy]] | Ch 17 — where to start when joining an untested project: smoke tests on mission-critical paths, bug-to-test conversion, tests on APIs other teams integrate against |
| [[barrier-defenses]] | Ch 17 — three-tool pattern (set barrier, risky work, remove barrier) that keeps unhealthy replicas away from users and risky software away from healthy replicas |
| [[production-probes]] | Ch 17 — three request sets replayed as monitoring probes; covers frontend × backend version combinations that release tests never see; probe failure pauses rollout |
| [[fake-backend-versions]] | Ch 17 — peer-team-maintained fake backends cut on the same schedule as the real backend; cross-product testing on new releases; rollout block, not release block |
| [[configuration-integration-testing]] | Ch 17 — config content as potentially hostile input; protocol buffers > YAML+safe_load > interpreted-language config; bounded runtime + load-time schema validation |
| [[software-engineering-in-sre]] | Ch 18 hub — why SRE teams run full software-engineering projects, not just one-off scripts; firsthand experience; the sublinear-scaling argument; balance against interrupts; staffing and retention; stay-embedded as the non-negotiable |
| [[auxon]] | Ch 18 case study — Google's intent-based capacity planner; seven-component architecture (Performance Data / Forecast / Supply / Pricing / Intent Config / Config Engine / Solver → Allocation Plan); agnostic decoupling as the adoption lever |
| [[intent-based-capacity-planning]] | Ch 18 — "specify the requirements, not the implementation"; the four-rung chain of abstraction; the three precursors (dependencies, performance metrics, prioritisation); regenerable plans that reach known-optimal solutions |
| [[traditional-capacity-planning]] | Ch 18 — the demand-driven spreadsheet cycle Auxon replaces; four structural weaknesses (brittle, laborious, imprecise, loses intent); the tooling pathology |
| [[sre-software-development-lessons]] | Ch 18 — practices distilled from Auxon: stay embedded; approximation over perfection (the Stupid Solver); agnostic design; modular interfaces for fuzzy requirements; launch and iterate |
| [[sre-product-adoption]] | Ch 18 — the adoption playbook: sustained socialisation, aspirational-vs-MVP expectation setting, targeting teams without existing solutions, white-glove early-adopter support, designing at the right level of generality |
| [[fostering-software-engineering-in-sre]] | Ch 18 — project selection (good candidates vs red flags); the two-extremes failure modes; generalist seed team plus specialists later; PM/TPM partnership; defending non-interrupt project time; the stay-embedded rule |
| [[introducing-sre-software-development]] | Ch 18 — change-management guide: create and communicate a clear message, evaluate organisational capabilities, launch and iterate with a six-month rhythm, don't lower standards |
| [[frontend-load-balancing]] | Ch 19 hub — the layered architecture (DNS → VIP → backend); why not one big machine (speed of light + single-point-of-failure); latency vs throughput; the HTTP-over-TCP vs stateless-UDP caveat |
| [[dns-load-balancing]] | Ch 19 — DNS as the first load-balancing layer; 512-byte reply cap; the recursive-resolver middleman (resolver IP vs user IP, nondeterministic paths, TTL caching); capacity and health as parts of "best location"; why DNS alone is not enough |
| [[anycast-dns]] | Ch 19 — advertising the authoritative nameserver IP from multiple regions so queries flow to the nearest instance by BGP; the public-DNS and large-ISP cases where resolver-near-user assumption breaks |
| [[edns0-client-subnet]] | Ch 19 — the DNS extension that carries the user's subnet upstream so the authoritative server optimises for the user, not the resolver; the scope field for correct cache partitioning; privacy vs routing-quality trade-off |
| [[virtual-ip-address]] | Ch 19 — the IP not bound to a single interface; hides the backend fleet behind one stable address; the second layer DNS resolves *to* |
| [[network-load-balancer]] | Ch 19 — the device fronting a VIP; two design axes (backend selection: least-loaded / hash-mod-N / consistent-hashing; packet delivery: NAT / L2 rewriting / encapsulation); Google's Maglev-style combination |
| [[direct-server-return]] | Ch 19 — reply-path optimisation where backends bypass the balancer and send replies directly to the client; the asymmetric-HTTP case; L2 MAC rewriting vs GRE encapsulation |
| [[packet-encapsulation-load-balancer]] | Ch 19 — Google's current VIP load balancer; wraps forwarded packets in outer IP+GRE so backends can be anywhere routable, not just on the same L2 segment; the MTU cost and the larger-internal-MTU mitigation |
| [[datacenter-load-balancing]] | Ch 20 hub — the intra-datacenter arc (state management → subsetting → policies); the ideal-case "1,000 reserved but only 700 usable" framing; Google's four-layer balancer (DNS / VIP / service / RPC); integration with GFE and Stubby |
| [[backend-task-states]] | Ch 20 — the three-state model (healthy / refusing connections / lame duck); the crude active-request-limit flow control (default 100) as predecessor and last-resort; why three states beat a binary readiness signal; propagation to inactive clients via UDP health checks |
| [[lame-duck-state]] | Ch 20 — backend-initiated graceful drain; five-step shutdown protocol with 10-150s interval; RPC-framework-level clean shutdown for every service; the symmetric "connect early, ready later" startup use; has no vanilla Kubernetes equivalent |
| [[subsetting]] | Ch 20 — limiting each client's connection pool to 20-100 backends; the three requirements (uniform load, low churn, graceful resizes); the idle-connection TCP-to-UDP optimisation that complements but does not replace subsetting |
| [[random-subsetting]] | Ch 20 — the rejected naive algorithm; 300×300×30% simulation produces 63%-121% spread; 10% subsets produce 50%-150% spread; would need ≥75% subsets to balance, defeating the point |
| [[deterministic-subsetting]] | Ch 20 — Google's algorithm; clients grouped into rounds, shared round seed for intra-round shuffle, different seeds across rounds so a backend failure redistributes across the whole fleet; per-backend connection count differs by at most 1 |
| [[load-balancing-policies]] | Ch 20 hub — the per-request backend selection problem; the distributed-stale-partial-realtime decision framing; why the three-rung ladder is mostly about getting more information into the decision |
| [[simple-round-robin]] | Ch 20 — the baseline; Google's most common policy for years; up to 2x CPU spread in practice from four compounding factors (small subsetting, varying query cost up to 1000x, machine diversity addressed via GCU, antagonistic neighbours and restart warmup) |
| [[least-loaded-round-robin]] | Ch 20 — filter by minimum active-request count then round-robin; the sinkholing pitfall where fast-failing backends attract more traffic; the error-counting fix; residual 2x spread at scale from the poor-proxy and partial-view problems |
| [[weighted-round-robin]] | Ch 20 — backends report QPS, errors, and utilisation in every response; clients maintain capability scores and route proportionally with error penalties; Figure 20-6's dramatic CPU-distribution tightening; the closed-loop controller inside the RPC client |
| [[handling-overload]] | Ch 21 hub — the cooperating stack of eight mechanisms (QPS pitfalls, quotas, throttling, criticality, utilisation, shedding, degradation, retry budgets, connection load) that lets a serving system degrade gracefully at 2-10x provisioned load instead of collapsing |
| [[queries-per-second-pitfalls]] | Ch 21 — why QPS (and request-shape proxies like keys-read) is a moving target; measure capacity in CPU directly; cost-of-a-request as normalised CPU-time; GC-memory-becomes-CPU simplification |
| [[per-customer-quotas]] | Ch 21 — CPU-second-per-second per-customer limits; the Gmail/Calendar/Android 4k+4k+3k+2k+500 example summing above the 10k fleet; over-subscription as intentional; real-time global aggregation pushing per-task effective limits |
| [[adaptive-throttling]] | Ch 21 — client-side self-regulation; two-minute `requests` / `accepts` window; drop probability `max(0, (requests − K × accepts) / (requests + 1))`; K = 2 as the speed-of-propagation-vs-waste trade-off; worst case one rejection per success |
| [[request-criticality]] | Ch 21 — four-valued ladder (CRITICAL_PLUS / CRITICAL / SHEDDABLE_PLUS / SHEDDABLE); automatic RPC-stack propagation; set close to the browser/mobile client; orthogonal to latency and network QoS; standardisation replaces ad hoc per-service notions |
| [[utilization-signals]] | Ch 21 — the executor load average (smoothed count of ready threads vs processor count) as Google's preferred overload signal; plug in any backend-specific signal; combine multiple; higher thresholds for higher criticalities |
| [[load-shedding]] | Ch 21 — reject-but-preserve-the-rest; the shed-vs-serve decision combines utilisation and criticality; the "task continues serving at provisioned rate even under 10x traffic" corollary; rejecting cheaply as a design requirement |
| [[graceful-degradation]] | Ch 21 — serve a cheaper response instead of rejecting; partial-corpus search and local-cache-instead-of-canonical as canonical examples; the ordering correct → degraded → rejected → failed; degradation as designed architectural work |
| [[retry-budget]] | Ch 21 — three-attempts per-request budget, 10% per-client retry ratio, retry-count metadata with backend histograms, "overloaded; don't retry" when widespread overload is detected, retry-only-at-the-layer-immediately-above rule that prevents 3^N combinatorial explosion |
| [[connection-level-load]] | Ch 21 — the CPU/memory cost of maintaining and churning connections; the health-check-dominates-work pathology at large low-rate-client fan-in; dynamic connection creation/teardown; the batch-proxy fuse pattern that absorbs batch-job connection storms |
| [[cascading-failure]] | Ch 22 hub — failures that grow through positive feedback; causes (overload, resource exhaustion, service-unavailability snowball), triggers, prevention, testing, in-progress remedies; also known as meltdown / thundering herd; the closing warning that reliability-improving changes can worsen cascade risk |
| [[server-overload]] | Ch 22 — the dominant cause of cascades; the 1,000-QPS-in-each-of-two-clusters worked example; 10,000-QPS-healthy-needing-drop-to-1,000-to-recover snowball mechanic; the overload-inversion where served rate falls as offered rate climbs |
| [[resource-exhaustion]] | Ch 22 — CPU, memory, threads, file descriptors; the effects of each; the nine-step worked scenario where Java GC tuning is the root cause and backend health-check failure is step nine's visible symptom |
| [[gc-death-spiral]] | Ch 22 — memory-pressure → more GC → less CPU → slower requests → more concurrent requests → more RAM → more GC; why the spiral is self-sustaining; restart as the only escape |
| [[queue-management]] | Ch 22 — 50% queue-to-thread ratio for steady traffic; Gmail's queueless approach; dynamic queue sizing for bursty loads; LIFO and CoDel as staleness-aware alternatives to FIFO; deadlines complement queue management |
| [[retry-amplification]] | Ch 22 — naïve retries turning 100 QPS of overload into runaway growth; randomised exponential backoff; the combinatorial-retry rule (retry at only one layer); clear retriable/nonretriable error codes; even restoring pre-overload traffic may not fix the cascade |
| [[latency-and-deadlines]] | Ch 22 — deadlines cap how long a server consumes client resources; missed deadlines waste work; picking a deadline as a balance; the stages-of-processing deadline-check discipline |
| [[deadline-propagation]] | Ch 22 — a single absolute deadline flowing through the RPC tree; the 30s-root-to-23s-A→B-to-19s-B→C worked example; cancellation propagation; per-hop safety margin and outgoing-deadline upper bounds |
| [[bimodal-latency]] | Ch 22 — 5% unservable × 100s deadline / 1,000 threads = 80% error rate; look at distributions not means; match deadline to mean latency; per-keyspace concurrency limits |
| [[slow-startup-and-cold-caching]] | Ch 22 — the restart-after-crash amplifier; latency caches (service works when empty) vs capacity caches (it doesn't); overprovisioning, separate caching tier (memcache), gradual ramp as mitigations |
| [[intra-layer-communication]] | Ch 22 — "Always go downward in the stack"; distributed deadlock, sudden-mode-switch under load, bootstrap complexity; client-mediated routing vs backend-to-backend proxying |
| [[cascading-failure-triggers]] | Ch 22 — the five trigger classes (process death, process updates, new rollouts, organic growth, planned drains / turndowns); the "check recent changes first" diagnostic hint |
| [[testing-for-cascading-failures]] | Ch 22 — test to failure and beyond; gradual vs impulse load; recovery-after-overload testing; per-component testing; production tests (reducing task counts, losing a cluster, blackholing backends); test popular clients and noncritical backends |
| [[addressing-ongoing-cascading-failure]] | Ch 22 — the eight remedies (increase resources, stop health-check deaths, restart servers, drop traffic, enter degraded modes, eliminate batch load, eliminate bad traffic, escalate); the meta-rule: fix the triggering condition before restoring load |

## Reliable product launches

| Page | Description |
|---|---|
| [[reliable-product-launches]] | SRE Ch 27 hub — launches as a distinctive reliability problem; the 70-per-week rate; the five criteria for a good launch process; three-piece organising principle (LCE, checklist, gradual-rollout/feature-flag techniques); LCE evolution 2003→2008; the three unsolved post-launch pathologies |
| [[launch-coordination-engineering]] | Ch 27 — the dedicated SRE consulting team for launches; five activities (audit, liaise, drive, gatekeep, educate); breadth/cross-functional/objectivity as the team advantages; formal staffing in 2004 |
| [[launch-coordination-engineer-role]] | Ch 27 — the individual LCE role; hiring paths; SWE plus communication plus leadership skills; six-month training; dual accelerator-plus-gatekeeper responsibility |
| [[launch-checklist]] | Ch 27 — the curated launch checklist as the central LCE artifact; question/action-item/pointer-to-infrastructure shape; substantiated-by-disaster and concrete-instruction curation rules; continuous plus annual full-review rhythm |
| [[launch-checklist-themes]] | Ch 27 — the nine checklist themes: architecture/dependencies, integration, capacity, failure modes, client behaviour, processes/automation, development process, external dependencies, rollout planning |
| [[gradual-rollout]] | Ch 27 — the canonical three-stage pattern (subset-in-one-datacenter → whole-datacenter → global) with observation windows; client-side variants (Android app install fractions); invite systems as rate-limited sign-up ramps |
| [[feature-flag-framework]] | Ch 27 — infrastructure for parallel small-scope feature rollouts; six framework requirements; two classes (HTTP payload rewriter for stateless UI vs request routing for stateful business logic) |
| [[abusive-client-behavior]] | Ch 27 — the non-user-initiated-request problem; retry amplification and thundering-herd pitfalls; server-controlled client configuration; the dormant-functionality pattern (ship inactive, activate server-side) |
| [[overload-behavior-launches]] | Ch 27 — why overload deserves extra launch-time attention; non-linear behaviour at the top of the load curve; logging-amplification lockup; GC thrashing; load tests as mandatory because first-principles prediction fails |
| [[norad-tracks-santa]] | Ch 27 — the opening case study: Keyhole at 25x normal peak (1M req/s) on Christmas Eve 2011; all the hard-launch attributes in one project; the "Make-children-cry switches" kill-switch name |

## SRE training and onboarding

| Page | Description |
|---|---|
| [[sre-onboarding]] | SRE Ch 28 hub — blueprint for bootstrapping a new SRE to on-call and beyond; Figure 28-1 time-by-abstract/applied blueprint; three aspirational attributes; five practices for aspiring on-callers; "scale your humans faster than your machines" maxim |
| [[trial-by-fire-anti-pattern]] | Ch 28 — the named anti-pattern (throwing newbies at the ticket queue); survivorship bias, false premise that SRE can be taught strictly by doing, three unanswered questions; why ops-driven teams self-perpetuate this failure mode |
| [[cumulative-learning-paths]] | Ch 28 — sequential, ordered curriculum; frontload abstract concepts + intermix hands-on work; the query-path ordering example; tiered access as progress gating ("powerups") |
| [[on-call-learning-checklist]] | Ch 28 — the document artifact: expert contacts, key docs, basic knowledge, probing questions, concrete outcomes; three audiences (student / mentor / team); deliberately does not encode procedures; Search SRE practice |
| [[targeted-project-work]] | Ch 28 — starter projects instead of menial tickets; three patterns (user-visible feature + release shepherding, monitoring blind spots, automate a pain point); bidirectional trust building |
| [[reverse-engineering-skills]] | Ch 28 aspirational attribute 1 — figuring out how systems you've never seen work; debugging surfaces, RPC boundaries, logs as reflexive fluencies; "follow the RPC" heuristic |
| [[statistical-comparative-thinking]] | Ch 28 aspirational attribute 2 — pruning a massive decision tree under pressure via experience + hypothesis construction; the "which of these things is not like the other?" game; architectural requirement that variables be individually controllable |
| [[improvisational-troubleshooting]] | Ch 28 aspirational attribute 3 — defence in depth applied to problem-solving behaviour; the zoom-out manoeuvre; two named failure modes (too procedural, too many untested assumptions) |
| [[reverse-engineering-class]] | Ch 28 — the Google News Bermuda Triangle cruise class; all three attributes in one session; take-home assignment that produces bidirectional senior-newbie learning |
| [[teachable-postmortems]] | Ch 28 practice 1 — postmortems as training material for engineers not yet hired; teachable vs rote; reading clubs and "tales of fail" formats; feedstock for Wheel of Misfortune scenarios |
| [[disaster-role-playing]] | Ch 28 practice 2 — the Wheel of Misfortune full operational manual; GM + primary/secondary, 30-60 min scenarios, Kennedy's SRE Zork framing, successful-session criterion |
| [[breaking-real-systems]] | Ch 28 practice 3 — hands-on chaos on a loaned-from-production instance; Search SRE's "Let's burn a search cluster to the ground!" quarterly inverse-pattern exercise |
| [[documentation-as-apprenticeship]] | Ch 28 practice 4 — newbie overhauls outdated checklist sections; the senior-carries-state-in-head asymmetry that makes newbies the natural doc maintainers |
| [[shadow-on-call]] | Ch 28 practice 5 — business-hours page copying; two visibility payoffs; the trust-building-to-prevent-burnout mechanism; postmortem co-authorship rule |
| [[reverse-shadow-on-call]] | Ch 28 — optional final pre-on-call step: newbie is primary, mentor lurks and independently diagnoses without modifying state |
| [[sre-continuing-education]] | Ch 28 closing — learning after on-call; regular learning series with developer co-presenters; recorded sessions as future training material; talks to developer counterparts |

## Dealing with interrupts

| Page | Description |
|---|---|
| [[dealing-with-interrupts]] | SRE Ch 29 hub — interrupt management as a team-design problem; the three operational-load categories; the two shapes of flow; the three levers (polarise / structure roles / reduce); connection to the 50% cap and Ch 11 overload |
| [[operational-load]] | Ch 29 — the three-category taxonomy (pages / tickets / ongoing responsibilities) with distinct SLOs; Google's common management shapes; the metrics teams use to choose; the warning that response-time metrics don't price human cost |
| [[cognitive-flow-state]] | Ch 29 — Csikszentmihalyi's four flow elements; the two SRE-flavoured shapes (creative-engaged and Angry-Birds); the constant-interruptability failure mode that prevents both |
| [[context-switch-cost]] | Ch 29 — the 20-minutes-costs-two-hours principle; the Fred-has-a-free-day running example; the rejected "engineer as interruptible unit of work" model |
| [[polarizing-time]] | Ch 29 — week / day / half-day work-mode polarisation; Paul Graham's maker schedule; what polarisation rules out and requires; the handoff discipline |
| [[interrupt-role-structuring]] | Ch 29 — "do one thing well"; the add-another-person-not-distribute-load rule; on-call / tickets / ongoing-responsibilities rules including *stop randomly assigning tickets* and *be on interrupts or don't be* |
| [[reducing-interrupts]] | Ch 29 — ticket scrubs as well as page reviews; silencing-with-deadlines; policy-pushback on customers; the deprecate / replace / give-the-pager-back ladder |

## Embedding an SRE to recover from overload

| Page | Description |
|---|---|
| [[embedding-sre]] | SRE Ch 30 hub — the rescue playbook for a team stuck in ops mode; one-SRE-not-two; three phases (learn / share / drive); the postvitam exit; also the starter playbook for a first SRE team; positioning on the overload-escalation ladder |
| [[ops-mode]] | Ch 30 — the named failure mode: humans-per-load instead of software-per-load; the "more tickets should not require more SREs" test; the "my service is tiny" rationalisation and its refutation; healthy work habits matter as much as automation |
| [[identifying-kindling]] | Ch 30 — Phase 1's complement to existing-stress-sources; nine specific warning signals including shallow postmortem action items, "we don't own that" answers, reactive capacity plans, and common undiagnosed alerts; the don't-fix-it-yourself discipline |
| [[bad-apple-theory]] | Ch 30 — the unspoken belief that outages come from flawed individuals; Dekker's cross-industry evidence that it's false; the canonical refutation phrasing for the "why me?" postmortem reaction; what blameless culture has to displace |
| [[explaining-reasoning]] | Ch 30 — Phase 3's pedagogical discipline: explain every decision whether or not asked; refer to first principles; four worked examples (two good, two insufficient); success criterion is the team predicting the visiting SRE's comment |
| [[leading-questions]] | Ch 30 — Phase 3's partner technique: specific observation + invitation to reason about a shared principle; leading vs loaded; two good examples (TaskFailures / turnup) and two counter-examples; why an outside voice is required |
| [[postvitam]] | Ch 30 — the exit-report artefact named in contrast to a postmortem; perspective + examples + explanation + action items; the prospective (not retrospective) character of the document |

## Communication and collaboration in SRE

| Page | Description |
|---|---|
| [[communication-and-collaboration-in-sre]] | SRE Ch 31 hub — SRE as two-masters distributed org; data-flow and API-as-contract metaphors; production meetings + cross-SRE collaboration + SRE-dev collaboration; the Viceroy and DFP-to-F1 case studies |
| [[production-meetings]] | Ch 31 — weekly 30-60 minute service-oriented meeting; default agenda (changes / metrics / outages / paging / nonpaging / actions); rotating chair with the chair-on-smaller-side VC trick; compulsory attendance with partner product-dev; the Google Docs real-time-collaborative agenda |
| [[sre-team-composition]] | Ch 31 — the three formal roles (TL / SRM / TPM); the rigid-vs-fluid responsibility spectrum; diversity as collaboration multiplier; great role-holders flex across all three |
| [[cross-sre-collaboration]] | Ch 31 — why SRE collaboration is mostly cross-site; specialisation as a double-edged tool; crisp team charters; homogeneity-by-culture; singleton projects usually fail; written-first + periodic-travel |
| [[viceroy-case-study]] | Ch 31 — 2012-2014 cross-SRE monitoring-dashboard consolidation; Monarch migration as trigger; Viceroy + Consoles++ initial incompatibility; late-2013 convergence; extended-team churn and dilution-of-ownership challenges; declared (not mandated) the SRE-wide solution |
| [[cross-site-project-recommendations]] | Ch 31 — the distilled recommendations from Viceroy: only cross-site when you must, vet contributor commitment, strong project leaders with local decision authority, divide-and-conquer, beware Conway's distortion, design documents and reviews, time-limited debates → decisions → documentation, in-person leaders and team summits |
| [[sre-dev-collaboration]] | Ch 31 — the early-in-design thesis; OKRs as the tracking mechanism; service-team-mainstay framing; SRE (infrastructure) + dev (BL) complementarity; peer engineering status as the leverage |
| [[dfp-to-f1-migration]] | Ch 31 — case study: DoubleClick for Publishers' main DB migrated MySQL → F1 while the serving system stayed untouched; SRE drove infrastructure design, dev owned BL, weekly syncs, interface-contract-up-front, validation-by-output-comparison, seamless cutover |

## SRE engagement model

| Page | Description |
|---|---|
| [[sre-engagement-model]] | SRE Ch 32 hub — the production-concerns set every engagement points at; the three successive engagement models (Simple PRR / Early Engagement / Frameworks and SRE Platform); how SRE decides to engage |
| [[simple-prr-model]] | Ch 32 — the classical takeover pattern for already-launched services; six phases (Engagement / Analysis / Improvements / Training / Onboarding / Continuous Improvement); the typical initial step of SRE engagement; limitations that motivate the other two models |
| [[production-readiness-review]] | Ch 32 — the formal review SRE conducts before accepting production responsibility; the gate concept; checklist examples; the lead-time costs that drove the framework-based model |
| [[prr-engagement-phase]] | Ch 32 phase 1 — SRE leadership picks a team, 1-3 SRE reviewers self-nominate, discussion opens with the development team on SLO/SLA, disruptive design changes, and planning |
| [[prr-analysis-phase]] | Ch 32 phase 2 — reviewers learn the service, run the PRR checklist, review recent incidents and postmortems; checklist drawn from domain expertise + Production Guide; team-specific gold standards |
| [[prr-improvements-and-refactoring]] | Ch 32 phase 3 — prioritise gaps for reliability impact, negotiate execution with the development team, jointly refactor and add controls; the longest and most variable phase |
| [[prr-training-phase]] | Ch 32 phase 4 — PRR reviewers train the receiving SRE team via design overviews, request-flow deep dives, production setup, hands-on exercises |
| [[prr-onboarding-phase]] | Ch 32 phase 5 — progressive transfer of operations, change management, access rights; development team stays available to advise as SRE settles in |
| [[prr-continuous-improvement]] | Ch 32 phase 6 — steady-state partnership; SRE maintains reliability as the service evolves and contributes lessons back to the Production Guide |
| [[shakespeare-example-prr]] | Ch 32 worked example — Shakespeare service runs through a PRR; monitoring-coverage gap found and fixed, pager handed to SRE with two devs remaining in rotation, weekly on-call meeting becomes the coordination venue |
| [[early-engagement-model]] | Ch 32 — the engagement model that moves SRE into the Design phase; cheaper fixes, smoother launches, faster onboarding; "the best production incidents are those that never happen" |
| [[early-engagement-candidates]] | Ch 32 — the three qualifying patterns (significant new functionality in an SRE-managed system, significant rewrite, dev team that proactively approached SRE); the entrance criterion that has to be satisfied without production evidence |
| [[disengaging-from-a-service]] | Ch 32 — valid Early Engagement outcome where SRE doesn't take over: service turned out reliable enough to stay with devs, or failed to meet projected scale; named explicitly as positive outcomes |
| [[frameworks-and-sre-platform]] | Ch 32 — the structural answer to the SRE staffing barrier; codify production best practices as service frameworks, build on a common platform with uniform control surface; faster PRR, lower cognitive load, shared-responsibility model |
| [[service-framework]] | Ch 32 — what a framework provides: module-encapsulated production concerns, standard semantic components, monitoring dimensions, log formats, load-shedding configuration, capacity/overload measure; per-language implementations with identical APIs and behaviour |
| [[shared-responsibility-engagement]] | Ch 32 — the staffing model frameworks unlock: SRE supports platform infrastructure, dev teams carry the pager for application bugs; breaks the "full SRE or nothing" binary |
| [[sre-alternative-support]] | Ch 32 — fallback support for services SRE can't take on: documentation (Production Guide) and consultation (LCE, ad-hoc SRE advice); the two original alternatives plus the framework-era shared-responsibility middle ground |
| [[production-guide]] | Ch 32 — Google's internal repository of production best practices documented from SRE and dev experience; substrate for PRR checklists; consumed directly by teams without SRE engagement; fed back by Continuous Improvement |

## Lessons from other industries

| Page | Description |
|---|---|
| [[lessons-from-other-industries]] | SRE Ch 33 hub — Petoff's cross-industry survey across aviation, lifeguarding, LASIK, telecom/E911, medical devices, military, rail, manufacturing, finance, nuclear, ATC; the four-theme distillation; the closing velocity-vs-reliability argument |
| [[preparedness-and-disaster-testing]] | Ch 33 — *hope is not a strategy*; DiRT and Wheel of Misfortune in the family of nuclear-Navy live drills, lifeguard mystery-shopper drownings, aviation simulators with live data feeds; the seven cross-industry preparedness strategies |
| [[organizational-safety-culture]] | Ch 33 — *every management meeting started with a discussion of safety*; Alcoa under O'Neill's 24-hour-notification practice and CEO-distributed-home-phone-number; the empowered-to-speak-up cultural property |
| [[near-miss-reporting]] | Ch 33 — manufacturing/chemical preemptive postmortem; the UK CHIRP confidential reporting programme; *latent error plus enabling condition equals things not working quite the way you planned* (Brasseur) |
| [[swing-capacity]] | Ch 33 — telecom switch-on-wheels mobile telco office; predictable surges (Olympics) and unpredictable ones (2005 leaked-celebrity-phone-number traffic); pre-built reserved capacity moved into position |
| [[safety-integrity-level]] | Ch 33 — SIL 1-4 from UK Defence Standard 00-56, IEC 61508, IEC513, US DO-178B/C, DO-254; externally imposed reliability classification compared to SRE's self-set SLO |
| [[structured-and-rational-decision-making]] | Ch 33 — four-property data-driven discipline; the *HiPPO* (Highest-Paid Person's Opinion) anti-pattern; the four-shape industry spectrum (if-it-ain't-broke / playbook-and-binder / controlled-experiment / enforcement-team-separation); 2010 Flash Crash and 2012 Knight Capital |
| [[velocity-vs-reliability-tradeoff]] | Ch 33 closing argument — Google's higher appetite for velocity is correct because most products live where lives aren't at stake; error budgets fund the difference; Google adopts practices compatible with high velocity from regulated industries and leaves the others |

## Google production infrastructure

| Page | Description |
|---|---|
| [[google-datacenter-topology]] | Machine / rack / row / cluster / building / campus; the machine-vs-server terminology split |
| [[borg]] | Google's cluster OS; failure-domain-aware binpacking; Kubernetes' ancestor |
| [[bns]] | Borg Naming Service; stable symbolic names → `IP:port`; the service-discovery layer for Borg |
| [[jupiter-network]] | Clos network fabric inside a datacenter; 1.3 Pbps bisection bandwidth |
| [[b4-network]] | OpenFlow-based software-defined backbone between datacenters; elastic bandwidth allocation |
| [[software-defined-networking]] | The control-plane/data-plane split underlying Jupiter and B4 |
| [[colossus]] | Cluster-wide filesystem over per-machine D fileservers; GFS successor |
| [[bigtable]] | Sparse multidimensional sorted-map NoSQL DB on Colossus; eventual consistency |
| [[spanner]] | SQL-like globally consistent database; backed by TrueTime |
| [[chubby]] | Paxos-based lock and coordination service; ZooKeeper's ancestor |
| [[borgmon]] | Scrape-based metrics monitoring; Prometheus' ancestor |
| [[gslb]] | Global Software Load Balancer; three-level (DNS / service / RPC) over BNS addresses |
| [[google-frontend]] | Edge HTTP reverse proxy; TCP/TLS termination and service lookup |
| [[stubby]] | Internal RPC framework; gRPC is its open-source release |
| [[protocol-buffers]] | Binary schema-driven wire format for Stubby and storage |
| [[google-monorepo]] | Single shared repo; CL review, datacenter-parallel build, continuous testing, push-on-green |
| [[n-plus-2-redundancy]] | Sizing rule: N for peak load, + 2 for one task updating and one failing during the update |
| [[life-of-a-request]] | The Shakespeare end-to-end trace: DNS → GSLB → GFE → frontend → backend → Bigtable |

## Trade-off analysis (Hard Parts)

| Page | Description |
|---|---|
| [[least-worst-trade-offs]] | Don't find the best — find the least worst; architect as objective arbiter against evangelism |
| [[mece-principle]] | Mutually exclusive, collectively exhaustive — decision-option discipline and its model-vs-reality caveats |
| [[operational-vs-analytical-data]] | The first structural data lens; OLTP boundary drives decomposition decisions |

## Coupling taxonomy (Hard Parts)

| Page | Description |
|---|---|
| [[static-coupling]] | How quanta are wired together — dependencies, contracts, topology; measured via bootstrap test |
| [[dynamic-coupling]] | Runtime coupling along three axes: communication (sync/async) × consistency (atomic/eventual) × coordination (orchestrated/choreographed) |
| [[semantic-coupling]] | Domain-concept coupling inherent in the workflow; the floor implementation can only worsen |
| [[stamp-coupling]] | Passing whole structures when only a subset is needed; GraphQL as the counter-pattern |
| [[orthogonal-coupling]] | Distinct-purposes-that-must-intersect; sidecars/mesh as the cleanest implementation |

## Architectural modularity and granularity

| Page | Description |
|---|---|
| [[architectural-modularity]] | Degree of decomposition into deployment units; five-driver rubric (maintainability, testability, deployability, scalability, fault tolerance) |
| [[agility]] | Compound characteristic = maintainability + testability + deployability |
| [[testability]] | Ease + completeness of testing; chatter failure mode; contract tests as preserver |
| [[deployability]] | Ease + frequency + risk; Matt Stine "big ball of distributed mud" warning |
| [[granularity-disintegrators]] | Six forces pulling services apart: scope, code volatility, scalability, fault tolerance, security, extensibility |
| [[granularity-integrators]] | Four forces keeping services together: transactions, workflow/choreography, shared code, data relationships |
| [[code-volatility]] | Change-rate as an objective, measurable decomposition driver |

## Decomposition patterns (Hard Parts Ch 4–5)

| Page | Description |
|---|---|
| [[component-based-decomposition]] | Hub — six-pattern sequence; preferred approach when a monolith is decomposable |
| [[tactical-forking]] | De La Torre clone-then-delete pattern; coarse-grained services from coupled code |
| [[big-ball-of-mud]] | Foote's 1999 antipattern; the decomposability gate |
| [[identify-and-size-components-pattern]] | Inventory every component; statements metric; standard-deviation balance rule |
| [[gather-common-domain-components-pattern]] | Consolidate cross-cutting domain logic; leaf-name heuristic; shared component vs library |
| [[flatten-components-pattern]] | Leaf-node definition; eliminate orphaned classes; push-down vs pull-up flattening |
| [[determine-component-dependencies-pattern]] | Component-level Ca/Ce; golfball/basketball/airliner triage; ArchUnit enforcement |
| [[create-component-domains-pattern]] | Namespace-prefix domains; 1:many service-to-components mapping |
| [[create-domain-services-pattern]] | Physical extraction to a service-based architecture; "soft landing" before microservices |

## Data decomposition (Hard Parts Ch 6)

| Page | Description |
|---|---|
| [[data-decomposition-drivers-and-integrators]] | Six disintegrators vs two integrators; the rubric that justifies a database split |
| [[data-domain]] | Soccer-ball model; groups of tables forming the unit of ownership and extraction |
| [[data-sovereignty]] | Step-3 outcome; one-owner-per-database rule |
| [[database-type-selection]] | Eight-family × eight-characteristic star-ratings trade-off matrix |
| [[polyglot-persistence]] | Decomposition end-state; multiple DB types chosen per workload |
| [[newsql-database]] | NoSQL scale + ACID; CockroachDB, Spanner, YugabyteDB |
| [[cloud-native-database]] | Snowflake, Redshift, Cosmos, Datomic; compute/storage separation; opex cost shape |

## Data ownership and access (Hard Parts Ch 9–10)

| Page | Description |
|---|---|
| [[data-ownership]] | Writer-owns rule; sole vs common vs joint ownership |
| [[joint-ownership-techniques]] | Four techniques for legit multi-writer tables: table split, data domain, delegate, service consolidation |
| [[table-split-technique]] | Split columns into two tables to resolve joint writes; CAP trade-off |
| [[delegate-technique]] | One service writes; others send write requests; primary-domain vs operational-priority choice |
| [[base-properties]] | Basically Available, Soft state, Eventual consistency — the ACID complement across services |
| [[compensating-update]] | Semantic rollback; the core saga building block |
| [[distributed-data-access]] | Four-pattern hub for reading data a service doesn't own |
| [[interservice-communication-pattern]] | Remote call for read access; three latencies; tight runtime coupling |
| [[column-schema-replication-pattern]] | Copy columns into the reader's DB; async sync; staleness trade-off |
| [[replicated-caching-pattern]] | In-memory replicated cache (Hazelcast-style); ~500 MB ceiling |
| [[data-domain-pattern]] | Shared schema for cross-service read access |
| [[background-synchronization-pattern]] | Eventual consistency via a background reconciler (Ch 9) |
| [[orchestrated-request-based-pattern]] | Synchronous orchestrated workflow; atomic-ish consistency across services (Ch 9) |
| [[event-based-consistency-pattern]] | Default eventual-consistency pattern via events (Ch 9) |

## Distributed workflows and sagas (Hard Parts Ch 11–12)

| Page | Description |
|---|---|
| [[distributed-workflow-patterns]] | Hub — orchestration vs choreography trade-off matrix and the four-force rubric |
| [[workflow-orchestration]] | Mediator coordinates; central state tracking; scalability ceiling |
| [[workflow-choreography]] | Peer-to-peer events; responsive/scalable but hard to track state |
| [[choreography]] | Top-level hub — no central coordinator; cross-links to broker-topology, saga, EDM |
| [[epic-saga]] | sync + atomic + orchestrated — traditional DT; rarely advisable |
| [[phone-tag-saga]] | sync + atomic + choreographed — worst of both worlds |
| [[fairy-tale-saga]] | sync + eventual + orchestrated — common real-world default |
| [[time-travel-saga]] | sync + eventual + choreographed |
| [[fantasy-fiction-saga]] | async + atomic + orchestrated — rarely viable |
| [[horror-story-saga]] | async + atomic + choreographed — avoid |
| [[parallel-saga]] | async + eventual + orchestrated — very common, strong default |
| [[anthology-saga]] | async + eventual + choreographed — event-driven architecture's native form |

## Reuse and contracts (Hard Parts Ch 8, 13)

| Page | Description |
|---|---|
| [[reuse-patterns]] | Hub — replication / shared library / shared service / sidecar; decision matrix |
| [[code-replication-pattern]] | Copy code into each service; fine when abstraction + slow change |
| [[shared-library-pattern]] | Compile-time reuse; versioning as the "ninth fallacy"; granular libraries over god-libs |
| [[shared-service-pattern]] | Runtime reuse via a shared service; latency/availability/versioning trade-offs |
| [[contracts]] | Strict-to-loose spectrum hub; coupling vs productivity trade-off |
| [[strict-contract]] | Strongly typed name/type/count/order; compile-time safety, evolution pain |
| [[loose-contract]] | Minimal shape; evolution-friendly; needs consumer-driven tests to stay safe |

## Analytical data in distributed systems (Hard Parts Ch 14)

| Page | Description |
|---|---|
| [[data-product-quantum]] | DPQ — data-product analogue of `architectural-quantum`; cooperative quantum to the operational service |
