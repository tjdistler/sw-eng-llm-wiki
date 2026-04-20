# MOC: Data Engineering

**Summary**: Entry point for questions about *the discipline of data engineering* — what the role is, what the lifecycle is, what the enduring "undercurrents" (governance, security, quality, data management, DataOps, orchestration, software engineering) are that cut through every lifecycle stage, which architectural patterns fit which organisational shape, and how to pick technologies that won't trap you in two years. Start here when the question is about *what a data engineering organisation should be doing*, rather than about the mechanics of a pipeline or the shape of a store.

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have — or are bootstrapping, or are scaling, or are rationalising — a data function. The design surface in front of you is organisational, architectural, and strategic: *what does a data engineer actually do, what shape should the platform take, how do we govern and secure data, how do we pick technologies, how does this whole practice interlock with data scientists, ML engineers, and analysts?* This MOC is the discipline map.

The canonical shape of a question that lands here: *"We're hiring a first data engineer — what should they be responsible for?"*, *"Should we build a lakehouse, a warehouse, a mesh?"*, *"We're drowning in pipeline duplication — is the answer DataOps?"*, *"How do Kimball vs Inmon vs data vault stack up for us?"*, *"We need a data governance program — where do we even start?"* The answer is rarely one page; it is a composition of lifecycle-stage awareness, undercurrent discipline, and architectural choice in the service of the business.

This MOC is drawn almost entirely from *Fundamentals of Data Engineering* (Reis and Housley, 2022). FoDE is the source; the other seven books in the wiki touch data-engineering territory from specialist angles (Kleppmann on internals, Bellemare on event-driven systems, SRE on pipeline reliability), and this MOC cross-links into them when they deepen a point the discipline has opinions about.

Jurisdictional rule for this MOC:

- **This MOC** owns the *discipline view* — the lifecycle, the undercurrents, the role of the data engineer, the data-architecture patterns (warehouse / lake / lakehouse / mesh / modern data stack), technology selection, governance, data management, data modelling as a practice.
- [[moc-data-models-and-storage]] owns the *shape of the store* — concrete models, engines, encoding, replication, partitioning.
- [[moc-data-processing]] owns the *execution mechanics* — batch and stream engines, pipeline topologies, CDC as source-capture, Lambda/Kappa/Dataflow.
- [[moc-security-and-privacy]] owns the *deep* security-and-privacy discipline; this MOC names security as an undercurrent but routes the deep material there.
- [[moc-reliability-and-operations]] owns the *operations-and-SRE* discipline; this MOC names DataOps but routes SLO/SLI/error-budget material there.

## The discipline itself

Before pipelines, before architectures, before technology choices: *what is a data engineer, and what do they do?*

- [[data-engineer]] — the role definition; the responsibilities; the languages (SQL, Python, sometimes Scala/Java); the balancing act between internal systems and external stakeholders. Start here.
- [[data-engineering-lifecycle]] — five stages (generation, storage, ingestion, transformation, serving) plus six undercurrents. The structuring device of the entire book and of this MOC.
- [[data-maturity]] — the three-stage model (starting with data / scaling with data / leading with data); how the data engineer's job differs at each stage. Read before recommending any architectural change — the right answer at one stage is the wrong answer at another.
- [[type-a-vs-type-b-data-engineers]] — abstraction-focused vs build-focused. Why hiring unicorns fails; why most organisations actually need one of each and pretend to want both.
- [[data-engineering-history]] — four-era sketch from 1980s warehousing to the 2020s modern data stack. Useful context for why the discipline's vocabulary has the shape it does.
- [[data-science-hierarchy-of-needs]] — Rogati's pyramid: data engineering is upstream of and equal to data science; you can't do ML on data nobody has cleaned, ingested, or governed. The slide you project whenever the question "why do we need data engineering at all?" gets asked.
- [[data-engineer-stakeholders]] — upstream (architects, software engineers, DevOps/SRE) and downstream (scientists, analysts, ML engineers, the C-suite) collaborators. The relationship map that shapes the role.
- [[dataops]] — Agile + DevOps + statistical process control, applied to data pipelines. Framed as an undercurrent in the lifecycle; framed here as a cultural stance the whole discipline tilts toward.

Deeper reading: [[fundamentals-of-data-engineering#chapter-1-data-engineering-described]].

## The data engineering lifecycle — five stages

The lifecycle is Reis and Housley's structuring device. It is *not* a waterfall; each stage continuously feeds and is fed by the others. When a question about the discipline doesn't obviously fit somewhere, asking "which lifecycle stage is this about?" is usually the shortest route to an answer.

- [[data-engineering-lifecycle]] (re-cited) — the hub; the five-stage diagram; the undercurrents that cut through them.
- [[source-systems]] — generation; evaluation questions for any source the engineer consumes from. The upstream dependency that the data engineer doesn't own but is accountable for.
- [[source-system-considerations]] — the expanded FoDE Ch 5 checklist: DBMS, shape, cadence, reliability, ownership, per-undercurrent concerns. The questionnaire every new integration should run through.
- [[data-storage-stage]] — storage; why it underpins every other stage; the evaluation criteria for picking storage at lifecycle-stage scope, not at individual-component scope.
- [[data-temperature]] — hot / lukewarm / cold tiers and the cloud archival economics; the vocabulary for storage-cost decisions.
- [[data-ingestion]] — the ingestion stage; batch vs streaming; push vs pull; the streaming-first checklist. Execution mechanics live on [[moc-data-processing]]; the *choice* lives here.
- [[data-transformation]] — basic-through-complex; business logic as driver. Mechanics on [[moc-data-processing]]; discipline here.
- [[data-serving]] — analytics / ML / reverse ETL; the "data vanity projects" anti-pattern. The payoff stage; the one executives care about.
- [[analytics]] — BI vs operational vs embedded/customer-facing; self-service; multi-tenancy. The single largest category of serving.
- [[reverse-etl]] — warehouse-to-source feedback; Hightouch / Census. The closing of the loop from analytics back to operations.
- [[etl-vs-elt]] — transform-before-load vs transform-after-load; why ELT rose with cloud warehouses. A lifecycle-ordering decision, not just an engineering taste.
- [[feature-store]] — the data-engineering × ML-engineering artefact; feature history, sharing, backfill. The serving-to-ML handoff, productised.

### Source-system patterns the data engineer sees repeatedly

- [[application-database-as-source]] — OLTP-backend producer/consumer tension; extraction patterns; the data-application hybrid. The most common source-system shape.
- [[file-sources]] — Excel, CSV, JSON, XML, TXT as the ubiquitous messy source category. Never going away.
- [[crud]] / [[insert-only]] — the two source-design philosophies; CRUD loses history at the source, insert-only keeps it. Your life downstream is very different depending on which one upstream chose.
- [[webhooks]] — reverse APIs; source pushes to consumer endpoint.
- [[graphql]] — Facebook's query-shaped alternative; one API paradigm among four.
- [[data-sharing]] — cloud-native multi-tenant data access; the infrastructure under data-mesh.
- [[key-value-store]] / [[wide-column-database]] / [[search-database]] / [[time-series-database]] — the non-relational source-system families the engineer will meet.

Deeper reading: [[fundamentals-of-data-engineering#chapter-2-the-data-engineering-lifecycle]] for the lifecycle overview; [[fundamentals-of-data-engineering#chapter-5-data-generation-in-source-systems]] for the generation stage; Chapters 6-9 for storage, ingestion, transformation, and serving at depth.

## The six undercurrents — what the discipline actually is

Reis and Housley's most important framing innovation. The undercurrents are *not* stages; they are disciplines that cut through *every* stage. An organisation that runs pipelines without running the undercurrents has a data factory, not a data engineering function.

### Security (undercurrent 1)

- [[data-security]] — security as undercurrent; people as the biggest vulnerability; multi-tenant blast radius. The framing; the deep material lives in [[moc-security-and-privacy]].
- [[least-privilege]] — the access-control principle at the heart of the security undercurrent. The default every new pipeline, table, and role should inherit.

Deeper material: FoDE Ch 10 — [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]] (the deep security MOC is [[moc-security-and-privacy]]).

### Data management (undercurrent 2)

- [[data-management]] — the umbrella discipline; DAMA DMBOK definition; the facets. The vocabulary for talking about data as an organisational asset.
- [[data-governance]] — the three core categories (discoverability, security, accountability). The practice that distinguishes an engineered data function from a data scramble.
- [[metadata]] — the four DMBOK categories (business, technical, operational, reference). The substrate that makes governance enforceable rather than aspirational.
- [[data-quality]] — accuracy, completeness, timeliness. A human-plus-technical problem; nobody ships a quality programme without both.
- [[master-data-management]] — golden records across the organisation. The specific practice that keeps "customer" or "product" from meaning three different things in three different systems.
- [[data-modeling]] — Kimball / Inmon / data vault; avoiding the WORN ("write once, read never") and data-swamp traps. Framed here as a management discipline; see [[moc-data-models-and-storage]] for the schema-shape view.
- [[data-lifecycle-management]] — archival, destruction, and GDPR/CCPA compliance. The retention policy you wish someone had written before the subpoena arrived.
- [[data-catalog]] — where metadata lives and serves discoverability. The operational artefact of the governance programme.

### DataOps (undercurrent 3)

- [[dataops]] (re-cited) — Agile + DevOps + SPC applied to data pipelines. The cultural stance.
- [[data-observability]] — DODD (data-observability-driven development); statistical process control; "data is a silent killer." The operational discipline inside DataOps.

### Data architecture (undercurrent 4)

- [[data-architecture]] — subset of enterprise architecture; Chapter 3's working definition; operational vs technical. The role-level and practice-level framing.
- [[data-architect]] — the role; technical + business; *Architectus Oryzus* (Martin Fowler's term). How it relates to and differs from the data engineer.

### Orchestration (undercurrent 5)

- [[orchestration]] — DAG-aware scheduling; Airflow and successors; strictly batch. FoDE frames orchestration as an undercurrent because it's an organising discipline, not just a tool choice. Execution mechanics live on [[moc-data-processing]].

### Software engineering for data (undercurrent 6)

- [[software-engineering-for-data]] — core processing code, streaming, IaC, pipelines-as-code. The undercurrent that says "data engineering is software engineering" and means it — tests, CI/CD, code review, modularity.
- [[infrastructure-as-code]] — declarative infra as version-controlled code. The default for cloud-native data stacks.

Deeper reading: [[fundamentals-of-data-engineering#chapter-2-the-data-engineering-lifecycle]] (undercurrents are introduced here); each undercurrent then threads through the chapter-5-through-9 stage chapters.

## Data architecture — principles and patterns

The architectural layer of the discipline. This section pairs the FoDE principles with the architecture-pattern catalogue; pick the pattern that matches the organisation's shape and maturity, and pressure-test it against the principles before committing.

### Principles

- [[principles-of-good-data-architecture]] — Reis and Housley's nine principles for evaluating any data-architecture decision. The rubric.
- [[well-architected-framework]] — AWS's six pillars; one of the two external frameworks the nine principles synthesise.
- [[cloud-native-principles]] — Google Cloud's five cloud-native principles; the other inspiration.
- [[loose-coupling]] — four technical properties; the Bezos API Mandate as the organisational translation. A principle that FoDE brings forward from general architecture as a first-class data-architecture principle.
- [[finops]] — cloud cost as an architectural signal; cost attacks; graceful spending limits. The principle the 2015-era data engineer didn't need and the 2026-era data engineer can't ignore.
- [[zero-trust-security]] — the cloud-native replacement for the hardened perimeter.
- [[shared-responsibility-model]] — security *of* the cloud vs security *in* the cloud; the line that decides what the data engineer is accountable for.
- [[elasticity]] — dynamic and automatic scaling; scale-to-zero; over-scaling pitfalls.
- [[brownfield-vs-greenfield]] — two project types; strangler vs big-bang; shiny-object syndrome. The framing for every "should we rebuild?" question.

### Architecture patterns

- [[data-warehousing]] — OLAP-dedicated database; Inmon's definition; organisational vs technical distinction; cloud DW as the dominant modern variant. Still the workhorse of BI and analytics for most organisations.
- [[data-mart]] — refined warehouse subset per department. A deliberate duplicate for analyst-friendliness.
- [[data-lake]] — raw-first, schema-on-read; the 1.0 failures ("data swamp"); the convergence story with warehouses.
- [[data-lakehouse]] — lake foundation plus warehouse guarantees (ACID, schema, transactions); the 2020s-era convergent platform. Often the current default for new builds at scale.
- [[modern-data-stack]] — cloud plug-and-play modular components; self-serve; clear pricing. The pragmatic default for smaller teams; the thing most analytics-engineering-style organisations are building on.
- [[lambda-architecture]] / [[kappa-architecture]] / [[dataflow-model]] — the three pipeline-architecture shapes. Execution mechanics on [[moc-data-processing]]; framed here as architectural-pattern choices that shape the whole data function.
- [[iot-architecture]] — devices, gateways, constrained-network ingestion, reverse-ETL control loops. The pattern the data function inherits when the source systems are things, not services.
- [[data-mesh]] — Dehghani's four principles (domain ownership, data as product, self-serve platform, federated governance). The organisational architecture of the 2020s; as much a Conway's-law statement as a technical one.
- [[data-as-a-product]] — the organisational stance inside data mesh. The thing that separates a mesh from "microservices for data" in caricature.

Deeper reading: [[fundamentals-of-data-engineering#chapter-3-designing-good-data-architecture]].

Cross-link: [[moc-domain-driven-design]] and [[moc-microservices]] for the software-architecture discipline that data mesh explicitly imports. Data mesh is partly "DDD for data"; reading the service-side material makes the mesh principles click.

## Technology selection — architecture first, technology second

The most Reis-and-Housley of sections. The whole of FoDE Chapter 4 is a sustained argument that most teams pick technologies badly — by hype, by familiarity, by vendor contact — and a method for picking them well.

- [[technology-selection]] — the ten criteria; architecture-first-technology-second as the central discipline. Start here.
- [[speed-to-market]] — "perfect is the enemy of good"; slow decisions kill data teams. The criterion most sophisticated engineers under-weight.
- [[interoperability]] — JDBC/ODBC work; REST is quirks all the way down; modularity's prerequisite.
- [[total-cost-of-ownership]] — direct and indirect costs; capex vs opex.
- [[total-opportunity-cost-of-ownership]] — the cost of lost options; the "bear trap" warning. A framing most TCO arguments miss.
- [[opex-vs-capex]] — why the cloud pushed data engineering opex-first. The shape of the decision, not just the arithmetic.
- [[immutable-vs-transitory-technologies]] — the Lindy effect applied to data tooling; build transitory around immutable; the two-year re-evaluation cadence.
- [[cloud]] / [[on-premises]] / [[hybrid-cloud]] / [[multicloud]] — the deployment-target axis; IaaS/PaaS/SaaS as sub-varieties; cloud economics; the "cloud ≠ on premises" reminder.
- [[cloud-repatriation]] — "you are not Dropbox, nor are you Cloudflare." The FoDE pushback on the zeal for getting off the cloud.
- [[data-gravity]] — why egress fees make cloud decisions sticky. The force that's quietly decisive in most multi-year architectural trajectories.
- [[build-vs-buy]] — the tire analogy; build where you have competitive advantage. The default for most data-engineering work is buy; know when that's wrong.
- [[open-source-software]] — community-managed OSS evaluation factors.
- [[commercial-oss]] — Databricks / Confluent / dbt Labs pattern; the COSS evaluation framework.
- [[proprietary-walled-garden]] — independent vendors and cloud proprietary services. The other side of COSS; evaluate with eyes open.
- [[monolith-vs-modular-data]] — the monolith/modular debate applied to the data stack itself. Shape of the platform, not shape of the application.
- [[distributed-monolith]] — the anti-pattern; Hadoop and Python orchestration; container mitigation. Data-stack flavour of the architectural failure mode.
- [[serverless-vs-servers]] — serverless first; containers next; owned servers last. FoDE's default ordering.
- [[containers]] — lightweight virtualisation; the middle path; security caveats.
- [[benchmark-wars]] — the 787-vs-Tesla analogy; vendor benchmark tricks. The specific epistemic hygiene to bring to any technology evaluation.
- [[cargo-cult-engineering]] — copying big-tech without the context. The failure mode every data-engineering blog-post-driven decision makes.

Deeper reading: [[fundamentals-of-data-engineering#chapter-4-choosing-technologies-across-the-data-engineering-lifecycle]].

## The data-engineer role and the stakeholder map

The discipline exists in relation to other disciplines. The data engineer works with software engineers upstream and data scientists / analysts / ML engineers downstream; the boundaries are not always clean, and FoDE is explicit that getting the boundary right is part of the job.

- [[data-engineer-stakeholders]] (re-cited) — the relationship map.
- [[data-science-hierarchy-of-needs]] (re-cited) — the pyramid that locates data engineering underneath data science.
- [[data-product]] — how the discipline frames its output; jobs-to-be-done; three build-time questions.
- [[trust-in-data]] — the root consideration of serving; once lost, fatal. The quality-and-SLA discipline.
- [[data-definitions-and-logic]] — the tribal-knowledge failure mode; catalog + semantic layer as the fix. The organisational-alignment problem every growing data function hits.
- [[self-service-analytics]] — aspirational more often than achieved; three classic blockers.
- [[metrics-layer]] — authoritative business-logic definitions independent of transformations. The discipline that keeps "revenue" from meaning three different things.
- [[semantic-layer]] — authoritative business definitions on top of the warehouse; Looker / dbt as examples.

## The future of data engineering

FoDE Chapter 11 is forward-looking; Reis and Housley's predictions have aged well enough to be worth including in the discipline map. Cite sparingly — these are directional bets, not doctrine.

- [[future-of-data-engineering]] — the chapter hub; seven predictions.
- [[live-data-stack]] — streaming-first successor to the modern data stack; fuses apps, analytics, and ML in real time.
- [[real-time-olap]] — Druid, ClickHouse, Rockset, Firebolt — purpose-built backends for streaming OLAP.
- [[stream-transform-load]] — STL: the streaming-era successor to ELT.
- [[data-application-fusion]] — application stacks become data stacks; tight ML feedback loops; the "throw it over the wall" handoff dies.
- [[cloud-data-os]] — standardised APIs, formats, catalogs, data-aware orchestration — the cloud as a distributed data OS.
- [[enterprisey-data-engineering]] — governance, quality, and operations trickling down from big-enterprise to every-size company.
- [[titles-will-morph]] — DE / SWE / DS / MLE boundaries blur; a new ML-focused engineer emerges between DE and MLE.
- [[spreadsheets-as-data-platform]] — the dark-matter prediction: 700M-2B users; spreadsheet interactivity plus cloud OLAP backend.
- [[data-ethics]] — predictive analytics bias, surveillance, privacy, consent, engineer responsibility. Kleppmann's closing chapter argument, borrowed here as a discipline-level concern FoDE agrees with.

Deeper reading: [[fundamentals-of-data-engineering#chapter-11-the-future-of-data-engineering]]; [[designing-data-intensive-applications#chapter-12-the-future-of-data-systems]] for Kleppmann's complementary long-run view.

## Sibling MOCs

- [[moc-data-models-and-storage]] — owns the shape of the store (models, engines, encoding, replication, partitioning, warehouse/lake/lakehouse shape). This MOC names the architectural pattern (warehouse, lake, lakehouse, mesh) as a discipline-level choice; the storage MOC owns the concrete schemas and engines inside it.
- [[moc-data-processing]] — owns the execution mechanics (batch and stream engines, pipeline topologies, CDC as source-capture, schedulers, Lambda/Kappa/Dataflow). This MOC names ingestion and transformation as lifecycle stages and orchestration as an undercurrent; the processing MOC owns how the mechanics actually work.
- [[moc-security-and-privacy]] — owns the deep security discipline. This MOC names [[data-security]] and [[least-privilege]] as undercurrents and routes FoDE Ch 10 material there; the security MOC owns threat modelling, encryption, secrets management, network access, and the security-policy discipline.
- [[moc-reliability-and-operations]] — owns the operations-and-SRE discipline. This MOC names DataOps and [[data-observability]] as an undercurrent; the reliability MOC owns SLO/SLI/error-budget, on-call, incident response, and the operations playbook.
- [[moc-events-and-streaming]] — owns the event-driven architectural view. This MOC names data-mesh data-sharing and event-based ingestion; the events MOC owns brokers as integration substrate and event design.
- [[moc-domain-driven-design]] — owns the modelling discipline. Data mesh explicitly imports DDD vocabulary (bounded contexts as data domains); reading that MOC is the shortest path to internalising mesh principles.
- [[moc-microservices]] — owns running microservices. Data mesh is partly "microservices for data"; the microservices MOC's ownership, independence, and platform-tax discussions translate directly.
- [[moc-architecture-fundamentals]] — owns characteristics, trade-off analysis, ADRs, fitness functions. The data-engineering *architect* role sits inside that general discipline; the technology-selection material in this MOC is a specialised application of [[trade-off-analysis]].

## Related pages

- [[index]]
- [[fundamentals-of-data-engineering]]
- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-maturity]]
- [[dataops]]
- [[data-management]]
- [[data-governance]]
- [[data-architecture]]
- [[data-architect]]
- [[principles-of-good-data-architecture]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-lakehouse]]
- [[modern-data-stack]]
- [[data-mesh]]
- [[technology-selection]]
- [[data-quality]]
- [[master-data-management]]
- [[data-observability]]
- [[data-catalog]]
- [[finops]]
- [[cloud]]
- [[build-vs-buy]]
- [[data-product]]
- [[feature-store]]
- [[future-of-data-engineering]]
