# Fundamentals of Data Engineering

**Summary**: Joe Reis & Matt Housley's 2022 O'Reilly book that defines the discipline of data engineering around a six-stage lifecycle (generation, storage, ingestion, transformation, serving, plus the "undercurrents" of security, data management, DataOps, architecture, orchestration, and software engineering). The book is deliberately technology-agnostic: its organising thesis is that the tools change every two years, but the lifecycle and the principles that govern architecture decisions do not.

**Sources**: `raw/fundamentals-of-data-engineering/`

**Last updated**: 2026-04-18

---

## About the book

*Fundamentals of Data Engineering: Plan and Build Robust Data Systems* is co-authored by Joe Reis and Matt Housley, two practitioners who have spent years consulting on data platforms. Their motivation is explicit: by the early 2020s, the "modern data stack" had exploded into hundreds of competing tools, and most educational material was tied to specific vendors. The book reacts to that by stepping one level of abstraction above the tooling — into the durable concepts every data platform has to implement somehow.

The authors frame data engineering as the practice of designing, building, and operating systems that take raw data from source systems and deliver it in usable form for analytics, machine learning, and reverse ETL back into operational systems. They argue that data engineers increasingly do less low-level plumbing (cloud services took that over) and more architectural work: choosing technologies, composing pipelines, enforcing data quality and governance, and collaborating with upstream producers and downstream consumers.

## Ingestion status

| Chapter | Title | Status |
|---|---|---|
| 1 | Data Engineering Described | Ingested 2026-04-18 |
| 2 | The Data Engineering Lifecycle | Ingested 2026-04-18 |
| 3 | Designing Good Data Architecture | Ingested 2026-04-18 |
| 4 | Choosing Technologies Across the Data Engineering Lifecycle | Ingested 2026-04-18 |
| 5 | Data Generation in Source Systems | Ingested 2026-04-18 |
| 6 | Storage | Ingested 2026-04-18 |
| 7 | Ingestion | Ingested 2026-04-18 |
| 8 | Queries, Modeling, and Transformation | Ingested 2026-04-18 |
| 9 | Serving Data for Analytics, Machine Learning, and Reverse ETL | Ingested 2026-04-18 |
| 10 | Security and Privacy | Ingested 2026-04-18 |
| 11 | The Future of Data Engineering | Ingested 2026-04-18 |

## Chapter 1 — Data Engineering Described

Chapter 1 defines the discipline. It walks through the history of the role, lands on a definition, sketches the [[data-engineering-lifecycle|five-stage lifecycle]] and its six undercurrents, introduces a three-stage [[data-maturity|data-maturity model]] that shapes the engineer's day-to-day work, and maps the web of stakeholders the engineer collaborates with.

Concept pages touched by Chapter 1:

- [[data-engineer]] — the role: definition, responsibilities (business and technical), languages, what the engineer does *not* do.
- [[data-engineering-lifecycle]] — five stages (generation → storage → ingestion → transformation → serving) and six undercurrents (security, data management, DataOps, architecture, orchestration, software engineering).
- [[data-maturity]] — three-stage model (starting / scaling / leading with data) and how it shapes the engineer's job.
- [[dataops]] — Agile + DevOps + statistical process control applied to data; one of the six undercurrents.
- [[type-a-vs-type-b-data-engineers]] — abstraction-focused vs build-focused engineers; why the unicorn job description is wrong.
- [[data-engineering-history]] — four-era sketch from 1980s warehousing to the 2020s modern data stack.
- [[data-engineer-stakeholders]] — upstream (architects, software engineers, DevOps/SRE) and downstream (data scientists, analysts, ML engineers, C-suite) collaborators.
- [[data-science-hierarchy-of-needs]] — Rogati's pyramid; the argument for why data engineering is upstream of, and equal to, data science.

## Chapter 2 — The Data Engineering Lifecycle

Chapter 2 is the deep dive into the five lifecycle stages and six undercurrents introduced in Chapter 1. Its key added framing: **virtually all data is inherently streaming**; batch is a specialised way of processing a stream. The chapter also elevates *data management* — traditionally thought of as "corporate" — to first-class data-engineering concern as cloud tools absorb low-level plumbing.

New concept pages created for Chapter 2's lifecycle-stage coverage:

- [[source-systems]] — stage 1 (generation); evaluation questions, schema handling, coupling to source load.
- [[data-storage-stage]] — stage 2 (storage); why it underpins rather than sits alongside; evaluation questions.
- [[data-temperature]] — hot/warm/cold framework and cloud archival economics.
- [[data-ingestion]] — stage 3; batch vs streaming, push vs pull, why streaming-first isn't free.
- [[data-transformation]] — stage 4; transformations entangled with every other stage; business logic as the driver.
- [[data-serving]] — stage 5; three consumption modes (analytics, ML, reverse ETL); data vanity projects.
- [[analytics]] — BI vs operational vs embedded; self-service; multi-tenancy blast radius.
- [[reverse-etl]] — warehouse → source-system feedback loop; why it's no longer an antipattern.
- [[etl-vs-elt]] — transform before vs after load; why ELT rose with cloud warehouses.
- [[data-lake]] — raw-first architecture; archival/destruction problem; Chapter 2's "vanity project" framing.
- [[data-lakehouse]] — lake foundation + warehouse guarantees; Delta Lake and peers.
- [[feature-store]] — data-engineering/ML-engineering intersection; feature history, sharing, backfill.

New concept pages created for the undercurrents:

- [[data-security]] — least-privilege mindset, people-as-biggest-vulnerability, multi-tenant blast radius.
- [[least-privilege]] — the access-control principle at the core of the security undercurrent.
- [[data-management]] — the umbrella discipline; DAMA DMBOK definition; its facets.
- [[data-governance]] — three core categories (discoverability, security, accountability).
- [[metadata]] — the four DMBOK categories: business, technical, operational, reference.
- [[data-quality]] — three characteristics (accuracy, completeness, timeliness); the human+technical nature.
- [[master-data-management]] — golden records; cross-organisation business-operations process.
- [[data-modeling]] — Kimball/Inmon/data-vault; the WORN/data-swamp antipattern.
- [[data-lifecycle-management]] — archival, destruction, and GDPR/CCPA compliance.
- [[data-architecture]] — the lifecycle's undercurrent pointer to Chapter 3.
- [[orchestration]] — DAG-aware scheduling; Airflow and successors; strictly a batch concept.
- [[software-engineering-for-data]] — core processing code, streaming, IaC, pipelines-as-code.
- [[infrastructure-as-code]] — declarative infra as version-controlled code.
- [[data-observability]] — DODD; SPC; "data is a silent killer."
- [[data-catalog]] — where metadata lives and serves discoverability.

Existing pages augmented with Chapter 2 content:

- [[data-engineering-lifecycle]] — stage-entanglement detail, top-level goals, full undercurrent map.
- [[dataops]] — three pillars (automation, observability, incident response); data products vs software products; maturity arc.
- [[data-lineage]] — FoDE's audit-trail framing; DODD; lineage as infrastructure for GDPR destruction.
- [[data-ethics]] — FoDE's positioning of ethics inside data management.
- [[change-data-capture]] — push/pull flavours of CDC from Chapter 2's ingestion taxonomy.
- [[batch-processing]] — FoDE's "batch is a specialisation of streaming" framing.
- [[stream-processing]] — FoDE's streaming-at-ingestion perspective.
- [[schema-evolution]] — source-system and storage-metadata framing of schema change.

## Chapter 3 — Designing Good Data Architecture

Chapter 3 defines data architecture as a subset of enterprise architecture — "the design of systems to support the evolving data needs of an enterprise, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs" — then lays out nine principles and surveys the major architecture patterns. The chapter borrows the first-law framing from Richards and Ford's *Fundamentals of Software Architecture* and cites Jeff Bezos, Martin Fowler, Werner Vogels, Grady Booch, and Zhamak Dehghani along the way.

New concept pages created for Chapter 3:

- [[principles-of-good-data-architecture]] — the nine principles: choose common components, plan for failure, scalability, leadership, always be architecting, loose coupling, reversibility, security, FinOps.
- [[well-architected-framework]] — AWS's six pillars; one of the two external frameworks the principles lean on.
- [[cloud-native-principles]] — Google Cloud's five cloud-native principles; the other inspiration source.
- [[data-architect]] — the role; technical + business; against command-and-control; the *Architectus Oryzus* archetype.
- [[loose-coupling]] — the four technical properties, the Bezos API Mandate, the organisational translation.
- [[finops]] — cloud cost as an architectural signal; cost attacks; graceful spending limits.
- [[zero-trust-security]] — the cloud-native replacement for the hardened perimeter.
- [[shared-responsibility-model]] — security *of* the cloud vs security *in* the cloud.
- [[elasticity]] — dynamic and automatic scaling; scale-to-zero; when it costs more than it saves.
- [[brownfield-vs-greenfield]] — the two project types; strangler vs big-bang; shiny-object syndrome.
- [[data-mart]] — refined subset of a warehouse per department.
- [[modern-data-stack]] — cloud, plug-and-play, modular, self-serve, clear pricing.
- [[kappa-architecture]] — Kreps's 2014 alternative to Lambda.
- [[dataflow-model]] — Google/Beam "batch as a special case of streaming."
- [[iot-architecture]] — devices, gateways, ingestion quirks, and reverse-ETL serving.
- [[data-mesh]] — Dehghani's four principles: domain ownership, data as a product, self-serve platform, federated governance.
- [[data-as-a-product]] — the organisational stance inside data mesh.

Existing pages augmented with Chapter 3 content:

- [[data-architecture]] — Chapter 3's working definition; operational vs technical; "good" data architecture.
- [[data-lake]] — Chapter 3's "data lake 1.0" failures and the convergence story.
- [[data-warehousing]] — Inmon's definition, organisational-vs-technical split, cloud DW, MPP, ELT.
- [[data-lakehouse]] — the convergence narrative and converged data platforms.
- [[lambda-architecture]] — FoDE's practical verdict and sequence to Kappa/Dataflow.
- [[reversible-vs-irreversible-decisions]] — Chapter 3's adoption as Principle 7; Fowler's remove-architecture framing.
- [[event-driven-architecture]] — FoDE's lightweight treatment as data-architecture concept.
- [[strangler-fig-pattern]] — FoDE's adoption for brownfield data architecture.

## Chapter 4 — Choosing Technologies Across the Data Engineering Lifecycle

Chapter 4 is the tactical counterpart to Chapter 3's strategy. Once the architecture is set, ten criteria govern how to pick specific technologies: team size and capabilities; speed to market; interoperability; cost (TCO, TOCO, FinOps, opex vs capex); today vs future (immutable vs transitory); location (on-prem, cloud, hybrid, multicloud); build vs buy (OSS, COSS, walled gardens); monolith vs modular; serverless vs servers; and the benchmark wars. The chapter's message: architecture first, technology second — and every technology choice should be tested against how it supports the [[data-engineering-lifecycle|lifecycle's six undercurrents]].

New concept pages created for Chapter 4:

- [[technology-selection]] — the ten-criteria framework and its relationship to the nine principles.
- [[speed-to-market]] — "perfect is the enemy of good"; slow decisions kill data teams.
- [[interoperability]] — connecting systems; JDBC/ODBC work, REST doesn't.
- [[total-cost-of-ownership]] — direct and indirect costs; capex vs opex.
- [[total-opportunity-cost-of-ownership]] — the cost of lost options; the "bear trap" framing.
- [[opex-vs-capex]] — why the cloud pushed data engineering opex-first.
- [[immutable-vs-transitory-technologies]] — Lindy effect; build transitory tools around immutable foundations.
- [[cloud]] — the cloud model; IaaS/PaaS/SaaS; "Cloud ≠ On Premises."
- [[on-premises]] — still the default for established companies; owned hardware realities.
- [[hybrid-cloud]] — analytics-in-the-cloud pattern that minimises egress.
- [[multicloud]] — motivations, disadvantages, the "cloud of clouds" emerging category.
- [[cloud-repatriation]] — Dropbox/Cloudflare case studies; "you are not Dropbox, nor are you Cloudflare."
- [[data-gravity]] — why egress fees make cloud decisions sticky.
- [[build-vs-buy]] — the tire analogy; when to build; the type A/B link.
- [[open-source-software]] — community-managed OSS evaluation factors.
- [[commercial-oss]] — Databricks/Confluent/dbt Labs; COSS evaluation factors.
- [[proprietary-walled-garden]] — independent vendors and cloud-proprietary services.
- [[monolith-vs-modular-data]] — data-stack version of the monolith/modular debate.
- [[distributed-monolith]] — the anti-pattern; Hadoop and Python orchestration; container mitigation.
- [[serverless-vs-servers]] — serverless first, containers-on-orchestrator next, owned servers last.
- [[containers]] — lightweight virtualisation; the middle path; security caveats.
- [[benchmark-wars]] — the 787-vs-Tesla analogy; vendor benchmark tricks.
- [[cargo-cult-engineering]] — copying big-tech architectures without the context.

Existing pages augmented with Chapter 4 content:

- [[finops]] — TCO/TOCO/FinOps as the three cost lenses; "FinOps is about making money."
- [[reversible-vs-irreversible-decisions]] — bear-trap framing, two-year re-evaluation rule, escape plans.
- [[brownfield-vs-greenfield]] — cargo-cult engineering as a related failure mode.
- [[modern-data-stack]] — the stack as the operational shape of Chapter 4's selection criteria.
- [[type-a-vs-type-b-data-engineers]] — Chapter 4's "lean toward type A" directive on build-vs-buy.
- [[orchestration]] — Chapter 4's Airflow deep-dive (advantages, disadvantages, Prefect/Dagster contenders).
- [[dataops]] — DataOps as the undercurrent that technology selection must support.
- [[data-architecture]] — the architecture-vs-tools split from Chapter 4's opening.

## Chapter 5 — Data Generation in Source Systems

Chapter 5 is the first deep dive into a lifecycle stage — the **generation** stage. It surveys the varieties of source systems (files, APIs, application databases, OLAP systems, CDC, logs, insert-only patterns, messages and streams, data sharing, third-party data, NoSQL in its many shapes), tours the practical details the data engineer must know about each (DBMS internals, lookups, consistency, partitioning), and runs the source-system problem through the six lifecycle undercurrents. Its closing message: source systems feel like "someone else's problem" — treat them that way at your peril.

New concept pages created for Chapter 5:

- [[source-system-considerations]] — the expanded Chapter 5 checklist (database, shape, cadence, reliability, source load, ownership, undercurrents).
- [[application-database-as-source]] — the producer-consumer tension when an OLTP application database must also supply analytics data.
- [[file-sources]] — flat files (Excel, CSV, JSON, XML, TXT) as the first-enumerated but messiest source-system category.
- [[crud]] — the four-operation persistent-storage pattern and its history-losing update semantics.
- [[insert-only]] — the append-only alternative that preserves history inside the source table.
- [[webhooks]] — reverse APIs; source pushes to consumer endpoint.
- [[graphql]] — Facebook's query-shaped alternative to REST.
- [[data-sharing]] — cloud-native multitenant sharing; data marketplaces; the infrastructure under [[data-mesh]].
- [[key-value-store]] — the simplest NoSQL family; caches and large-scale hash-map stores.
- [[wide-column-database]] — single-index, row-key-partitioned; Bigtable, Cassandra.
- [[search-database]] — Elasticsearch/Solr; text-search and log-analysis workloads.
- [[time-series-database]] — IoT, metrics, ad-tech; write-heavy, time-ordered storage.

Existing pages augmented with Chapter 5 content:

- [[source-systems]] — full Chapter 5 source-category taxonomy, stakeholder classes, per-undercurrent checklist, closing philosophy.
- [[oltp-vs-olap]] — FoDE's source-system framing; OLAP as source too; "data applications" hybrid.
- [[event-streams]] — message-vs-stream distinction; topics, partitions, hotspotting; four types of time.
- [[message-brokers]] — FoDE message-queue framing; delivery frequency, ordering, scalability as source-system considerations.
- [[nosql]] — FoDE's six-family enumeration; extraction implications.
- [[acid]] — FoDE's relax-for-performance framing at the source-system level.
- [[document-model]] — FoDE's not-ACID framing; schema-evolution hazards; extraction via full scan or CDC.
- [[relational-model]] — FoDE's canonical-application-backend framing; state-capture-over-time challenge.
- [[graph-data-models]] — FoDE's three modelling-path choices for graph sources.
- [[data-contract]] — Reis & Housley's source-system-extraction framing; the Denmore definition; SLAs and SLOs.
- [[data-engineer-stakeholders]] — systems vs data stakeholder split; feedback-loop practice.
- [[change-data-capture]] — Chapter 5's per-database-vendor variability and CRUD-alternative framing.
- [[third-party-api-integration]] — FoDE's REST/GraphQL/gRPC/Webhook category survey and tooling advice.
- [[data-ingestion]] — Chapter 5 expansion of what "source-system shape" ingestion must handle.

## Chapter 6 — Storage

Chapter 6 is the deep dive into the **storage** stage. It structures storage into three layers — raw ingredients, storage systems, and storage abstractions — and adds a set of cross-cutting big ideas (catalogs, schema, storage/compute separation, zero-copy cloning, retention, single- vs multi-tenant storage). The chapter's closing message: "Storage is everywhere and underlays many stages of the data engineering lifecycle."

New concept pages created for Chapter 6:

- [[storage-raw-ingredients]] — HDD, SSD, RAM, networking, CPU, serialization, compression, caching; the cache hierarchy.
- [[object-storage]] — S3/GCS/Azure Blob as immutable key-value stores; durability, consistency, versioning, storage classes.
- [[block-storage]] — RAID, SAN, EBS, local instance volumes; the raw block-addressable tier underneath filesystems.
- [[file-storage]] — NAS, NFS, cloud filesystem services; the three properties of a file.
- [[compression-algorithms]] — gzip, bzip2, snappy, LZ4, LZMA, zstd; choosing by workload.
- [[cache-memory-storage]] — Memcached and Redis as RAM-tier stores.
- [[streaming-storage]] — Kafka/Pulsar/Kinesis/Pub-Sub with long retention and tiered storage as a storage layer.
- [[stream-to-batch-storage]] — fan-out from a stream to a batch-storage consumer; relationship to Lambda.
- [[storage-compute-separation]] — the defining architectural move of cloud data platforms; hybrid caching and hybrid object storage.
- [[lakehouse-table-formats]] — Delta Lake, Apache Iceberg, Apache Hudi; the ACID-and-history-over-object-storage substrate.
- [[data-retention]] — the four-input retention decision (value, time, compliance, cost).
- [[data-platform]] — vendor-curated walled garden of tools around a storage core.

Existing pages augmented with Chapter 6 content:

- [[data-storage-stage]] — Ch 6 three-layer model, big-ideas list, undercurrents.
- [[data-temperature]] — hot/warm/cold with Ch 6 specifics; spillover; lifecycle automation.
- [[data-lake]] — the WORM retrospective; object storage as gold standard; unstructured data.
- [[data-lakehouse]] — Ch 6 feature-list definition; interoperability advantage; hybrid structure.
- [[data-warehousing]] — Ch 6 as storage abstraction; cloud DW / object-storage pairing; micro-partitioning.
- [[column-oriented-storage]] — analytics default; partitioning+clustering; Snowflake micro-partitioning.
- [[partitioning]] — analytics partitioning and clustering; Snowflake micro-partitioning as metadata-indexed columnar storage.
- [[distributed-filesystems]] — "Hadoop is dead, long live Hadoop"; HDFS mechanics recap; colocation vs object storage.
- [[eventual-consistency]] — BASE definition; S3 history; three places to decide consistency.
- [[data-catalog]] — catalog across storage layers; catalog-as-lakehouse-ingredient.
- [[data-lifecycle-management]] — lifecycle vs retention split; four retention inputs.
- [[schema-on-read-vs-write]] — Ch 6 storage-layer framing; schema is not just relational; lakehouse compromise.
- [[acid]] — ACID via lakehouse table formats on object storage.
- [[mvcc]] — MVCC in lakehouse table formats.
- [[tombstone]] — tombstones in lakehouse table formats; GDPR deletion.
- [[log-based-message-brokers]] — tiered storage; replay as standard retrieval; streaming-as-storage.

## Chapter 7 — Ingestion

Chapter 7 is the deep dive into the **ingestion** stage — the third lifecycle stage and the point where data engineers begin actively designing pipeline activity. It defines data ingestion and data pipelines, enumerates eight engineering considerations (bounded vs unbounded, frequency, sync vs async, serialization, throughput, reliability, payload, push/pull/poll), treats batch and stream ingestion patterns separately, surveys the concrete ways to ingest (direct DB, CDC, APIs, streams, managed connectors, object storage, EDI, file export, shell, SSH, SFTP, webhooks, web scraping, transfer appliances, data sharing), discusses upstream and downstream stakeholders, and closes with ingestion-specific framings of the six undercurrents.

New concept pages created for Chapter 7:

- [[data-pipeline]] — Reis & Housley's deliberately fluid definition; modern pipelines include every historical pattern (ETL, ELT, reverse ETL, data sharing).
- [[ingestion-frequency]] — batch, micro-batch, real-time; why "real-time" is always near-real-time; why batch is always somewhere downstream.
- [[push-vs-pull-vs-poll]] — the three directional patterns; where each fits; why the lines are blurry.
- [[ingestion-payload]] — the five payload characteristics: kind, shape, size, schema/types, metadata.
- [[snapshot-vs-differential-ingestion]] — full-snapshot vs incremental; the "missing intermediate changes" pitfall; connection to CDC patterns.
- [[data-migration]] — one-time bulk moves; schema subtleties; the often-overlooked pipeline-connection cut-over.
- [[dead-letter-queue]] — the error-segregation topic; one of the three schema-evolution defenses.
- [[managed-connector]] — Fivetran/Airbyte/Matillion/Stitch; outsource undifferentiated plumbing.
- [[file-based-ingestion]] — push-style file export over object storage / SFTP / SCP; format landscape.
- [[edi]] — archaic email/flash-drive transport; automate around it.
- [[web-scraping]] — legal/ethical caution; maintenance burden; downstream architecture implications.
- [[transfer-appliance]] — physical box of hard drives for 100+ TB migrations; Snowball, Snowmobile.

Existing pages augmented with Chapter 7 content:

- [[data-ingestion]] — the Ch 7 deep dive: eight engineering considerations, sync vs async mini-case, batch/stream pattern tables, ingestion-mechanisms table, stakeholders, per-undercurrent framing.
- [[change-data-capture]] — Ch 7's batch-oriented vs continuous CDC distinction; the bank-account missing-intermediate-changes example; CDC vs native synchronous replication trade-off; source-resource cost warning.
- [[etl-vs-elt]] — Ch 7's extract (E) and load (L) as ingestion-stage responsibilities; the inserts/updates/batch-size section.
- [[webhooks]] — Ch 7's recommended AWS full-fat architecture (Lambda → Kinesis → Flink → S3); the entanglement-with-storage-and-processing point.
- [[data-sharing]] — Ch 7's "strictly speaking, this isn't ingestion" caveat — you don't get physical possession.
- [[late-arriving-events]] — Ch 7's ingestion-layer framing; the cutoff-time prescription.
- [[reprocessing-event-streams]] — Ch 7's replay-as-ingestion-consideration framing; TTL-replay interaction; platform-choice dependency.
- [[schema-evolution]] — Ch 7's automation-is-mixed-blessing point; three-part defense (registry + DLQ + communication); Git-style branching floated as a future direction.

## Chapter 8 — Queries, Modeling, and Transformation

Chapter 8 is the deep dive into the **transformation** stage. Rather than a linear stage-by-stage walk, it's a three-part treatise on the intellectual layers that make data useful: what a **query** is and how to make it fast; how to **model** data for the business; and how to **transform** it for downstream consumption. The chapter is the book's longest and densest — and the one that leans hardest on durable concepts over named technologies.

New concept pages created for Chapter 8 — **queries and performance**:

- [[life-of-a-query]] — Reis & Housley's four-phase narrative: parse, compile to bytecode, optimize, execute.
- [[query-optimizer]] — the component that reorders and refactors your query; what it can and can't do; the EXPLAIN interface.
- [[query-performance-tuning]] — scan less data, better joins, no row explosion, CTEs over subqueries, caching, vacuuming, batch over single-row inserts.
- [[broadcast-join]] — small side shipped to every node; joins the local slice of the large side.
- [[shuffle-hash-join]] — both sides repartitioned by hash of join key; the expensive default.
- [[common-table-expression]] — `WITH ... AS`; CTEs preferred over nested subqueries and temp tables for readability and performance.
- [[window-functions]] — `OVER (PARTITION BY ... ORDER BY ...)`; declarative analytics that the optimizer can push into native parallel primitives.
- [[user-defined-function]] — extend the engine with custom code; deterministic vs non-deterministic; why JavaScript/PySpark UDFs can be catastrophically slow.
- [[nested-data]] — structs, arrays, maps as first-class column types; the semistructured escape hatch that softened the star-schema orthodoxy.
- [[streaming-queries]] — fast-follower CDC, Kappa queries, data-triggered computation; windows and triggers; streaming joins.

New concept pages created for Chapter 8 — **data modeling paradigms**:

- [[conceptual-logical-physical-models]] — the three-step continuum from business abstraction to database implementation; the grain rule.
- [[normalization-levels]] — denormalized → 1NF → 2NF → 3NF; partial and transitive dependencies; Codd's four objectives.
- [[inmon-model]] — top-down 3NF integration in the warehouse; data marts downstream; "integration is the most important."
- [[kimball-model]] — bottom-up facts + dimensions directly in the warehouse; denormalization and duplication accepted.
- [[star-schema]] — the canonical Kimball arrangement; fewer joins, analyst-legible.
- [[snowflake-schema]] — normalized star variant; less common in practice.
- [[fact-table]] — immutable, append-only, narrow and long, all numeric; lowest-grain rule.
- [[dimension-table]] — descriptive attributes; wide and short; surrogate keys; conformed dimensions.
- [[slowly-changing-dimensions]] — Type 0, 1, 2, 3 patterns for dimension change; Type 2 most common; determinism technique for stream-table joins.
- [[data-vault]] — Linstedt's insert-only, hub/link/satellite model; agile under source change; often feeds a downstream Kimball star.
- [[wide-denormalized-table]] — one very wide table with nested fields; works because columnar storage makes null cells free and schema evolution cheap.
- [[one-big-table]] — the no-modeling extreme; fast to start, trust-erosive; most teams gravitate back.
- [[streaming-data-modeling]] — the unsettled frontier; flexible schemas, nested columns, trust source-system definitions.

New concept pages created for Chapter 8 — **transformation**:

- [[update-patterns]] — truncate-and-reload, insert-only, delete, upsert/merge, schema update; copy-on-write cost; merge-frequency trap.
- [[upsert]] — update-on-match, insert-on-no-match; designed for row-based, expensive in columnar; the CDC-merge anti-pattern.
- [[materialized-view]] — precomputed results refreshed on source change; optimizer rewrites; live-table composition.
- [[federated-query]] — select from external sources as if they were local tables.
- [[data-virtualization]] — Trino/Presto; storage-less query engines; query pushdown; data-mesh enabler.
- [[dbt]] — Git-managed templated SQL compiled to warehouse DAGs; the analytics-engineering-as-code embodiment.
- [[feature-engineering]] — the ML-targeted transformation mode; data scientists design, data engineers automate.
- [[data-wrangling]] — IDEs for malformed data; the Reis & Housley push-back against engineers' dismissal of no-code tools.
- [[metrics-layer]] — a semantic layer that holds authoritative business-logic definitions independently of transformations.

Existing pages augmented with Chapter 8 content:

- [[data-modeling]] — the full Ch 8 deep dive: conceptual/logical/physical, grain, the three paradigms, wide-table alternatives, streaming frontier.
- [[data-transformation]] — Ch 8's query-vs-transformation distinction, batch transformations, update-pattern family, views/materialization/federation, business logic as derived data, streaming transformations, feature engineering.
- [[mapreduce]] — Ch 8's post-MapReduce framing (relaxation, not replacement); the map/shuffle/reduce worked example.
- [[feature-store]] — Ch 8's placement of feature engineering inside transformation.
- [[normalization]] — pointer to [[normalization-levels]] for the full normal-form sequence.

## Chapter 9 — Serving Data for Analytics, Machine Learning, and Reverse ETL

Chapter 9 is the deep dive into the **serving** stage — the final lifecycle stage, where the engineer's output meets its users. The chapter is organised around general considerations first (trust, use case/user, data products, self-service, definitions and logic, data mesh as serving), then the three major serving modes (analytics / ML / reverse ETL), then the concrete serving mechanisms (files, databases, streaming, federation, data sharing, semantic/metrics layers, notebooks), and closes with the six undercurrents applied to serving.

The chapter's organising argument: **trust is the root consideration**; everything else — architecture, performance, tooling — is worthless without it.

New concept pages created for Chapter 9 — **general considerations**:

- [[trust-in-data]] — the root consideration; two dimensions (data quality, SLAs); silent-death-knell framing.
- [[data-product]] — DJ Patil's definition; jobs-to-be-done; positive feedback loops; three questions.
- [[self-service-analytics]] — mostly aspirational; succeeds only with the right audience; Chapter 9's refinement of Chapter 2's three blockers.
- [[data-definitions-and-logic]] — meaning vs derivation rules; the tribal-knowledge failure mode; catalog + semantic layer as the fix.

New concept pages created for Chapter 9 — **analytics sub-varieties**:

- [[business-analytics]] — strategic decisions; dashboards, reports, ad-hoc; the running-shorts case.
- [[operational-analytics]] — immediate action; real-time monitoring; the 10-year streaming-supplants-batch forecast.
- [[embedded-analytics]] — customer-facing; three hard requirements (low latency, fast queries, high concurrency); the scaling arc.

New concept pages created for Chapter 9 — **ML fundamentals for DEs**:

- [[model-drift]] — why models degrade; DE role in drift observability.
- [[training-test-sets]] — train/test/validation splits; point-in-time correctness; leakage trap.

New concept pages created for Chapter 9 — **serving mechanisms**:

- [[semantic-layer]] — authoritative business definitions; query quality vs data quality; Looker/dbt examples.
- [[file-exchange-serving]] — ad-hoc file hand-off; five considerations; when to use / when to migrate.
- [[serving-in-notebooks]] — Jupyter as a serving target; credential hygiene; scaling off the laptop.

Existing pages augmented with Chapter 9 content:

- [[data-serving]] — Ch 9 deep dive: general considerations, serving mechanisms, per-undercurrent framing.
- [[analytics]] — Ch 9 use-case-and-user framing; hub pointing to the three sub-variety pages.
- [[reverse-etl]] — Ch 9 lead-scoring example; "BLT" renaming; feedback-loop hazard.
- [[feature-store]] — Ch 9 DE/ML collaboration surface; factory-loom example.
- [[metrics-layer]] — Ch 9 query-quality-vs-data-quality separation; the "are these numbers correct?" problem.
- [[data-mesh]] — Ch 9 view of the mesh as a serving architecture.
- [[data-as-a-product]] — link to sibling [[data-product]] page.

## Chapter 10 — Security and Privacy

Chapter 10 is the first of two short closing chapters. It revisits the [[data-security|security undercurrent]] — previously introduced briefly in Chapter 2 and sharpened architecturally in Chapter 3 — and gives it a full dedicated treatment organised around **people, processes, and technology, in that order**. The chapter's core argument is that the weakest link in every data system is the human, so process and technology must both be designed to survive human error, not to assume it away.

New concept pages created for Chapter 10:

- [[security-theater]] — the named antipattern of compliance-as-performance; 200-page unread policies; the habit antidote.
- [[active-security]] — research current attacks rather than run scheduled drills; every engineer involved in their systems' security.
- [[threat-modeling]] — the habit beneath active security; negative thinking; minimise data; enumerate attack scenarios.
- [[encryption-at-rest]] — baseline for devices, servers, databases, object storage, backups; useless against credential compromise.
- [[encryption-in-transit]] — HTTPS as default; FTP as anti-example; keys and bucket permissions as common undoings.
- [[secrets-management]] — credentials as configuration; SSO + MFA; cloud/self-hosted secrets managers; the anti-pattern list.
- [[security-monitoring]] — access, resources, billing, and excess-permission monitoring; team dashboard; rehearsed incident response.
- [[network-access-security]] — IP allowlists, VPCs, VPN, bastion hosts; the public-S3 / open-SSH catalogue of common mistakes.
- [[security-policy]] — the short-practical-habitual example policy (credentials, devices, software updates).

Existing pages augmented with Chapter 10 content:

- [[data-security]] — the full Ch 10 treatment: people/processes/technology organising frame; links to all the new specialised pages.
- [[least-privilege]] — Ch 10's time-boxing and revocation; column/row/cell-level controls and PII masking; broken-glass processes.
- [[shared-responsibility-model]] — "most cloud breaches continue to be caused by end users, not the cloud."
- [[zero-trust-security]] — Ch 10's cloud-vs-air-gapped framing; air gap as the ultimate hardened perimeter; still vulnerable to humans.
- [[backups-vs-archives]] — ransomware as a reason backups are a security control, not just a reliability control; shrinking insurance payouts.

## Chapter 11 — The Future of Data Engineering

Chapter 11 is the short closing chapter — a set of forward-looking predictions grounded in the authors' perspective on past, present, and current trends. Its organising claim is that the [[data-engineering-lifecycle]] itself is durable, but the shape of each stage, the tools used, and the role boundaries around data engineers will keep morphing. The chapter explicitly hedges: some predictions are safe ("proceeded day by day as we've written this book"), others are speculative ("significant paradigm shift that might stall").

New concept page created as the chapter hub:

- [[future-of-data-engineering]] — full walkthrough of the chapter's seven predictions and how they relate to each other.

New concept pages created for Chapter 11's specific predictions:

- [[live-data-stack]] — the chapter's flagship prediction; streaming-first successor to the [[modern-data-stack]] that fuses real-time analytics and ML with applications.
- [[real-time-olap]] — Druid, ClickHouse, Rockset, Firebolt class of databases purpose-built for streaming ingestion and subsecond queries; backend of the live data stack.
- [[stream-transform-load]] — STL as the back-to-the-future successor to ELT; transformation in the stream, not in the warehouse.
- [[data-application-fusion]] — application stacks become data stacks; tight real-time loop between applications, streams, and ML.
- [[cloud-data-os]] — standardised APIs, file formats, metadata catalogs, and data-aware orchestration across cloud data services.
- [[enterprisey-data-engineering]] — "enterprisey" management, governance, and quality practices trickling down to all company sizes.
- [[titles-will-morph]] — DE/SWE/DS/MLE boundaries blur; a new ML-focused engineer emerges; "throw it over the wall" dies.
- [[spreadsheets-as-data-platform]] — the "dark matter" prediction: 700M–2B spreadsheet users; a future product category combining spreadsheet interactivity with cloud OLAP.

Existing pages augmented with Chapter 11 content:

- [[modern-data-stack]] — Ch 11's candid reassessment; the MDS as a cloud-repackaged warehouse; limitations that motivate the live data stack.
- [[data-engineer]] — Ch 11's role trajectory; move up the value chain; streaming-first competence; blurring titles.
- [[data-engineering-lifecycle]] — Ch 11's "lifecycle survives, time between stages collapses" prediction.
- [[data-engineering-history]] — new "Era 5" section extending the four-era history into the live-data-stack speculation.
- [[stream-processing]] — Ch 11's elevation of streaming from harder-path to default.
- [[kappa-architecture]] — the live data stack as the practical descendant of Kappa, now economically viable thanks to managed cloud stream processors and real-time OLAP.
- [[dataflow-model]] — Dataflow's batch-is-a-bounded-stream unification as the theoretical backbone of the live data stack and STL.
- [[feature-store]] — Ch 11's placement of feature stores as substrate for the application-ML feedback loop.
- [[orchestration]] — Ch 11's forecast of data-aware orchestration with built-in IaC, CI/CD, and managed-stream-processor stitching.
- [[managed-connector]] — Ch 11's framing of connectors as an outsourced problem, enabling engineer focus on differentiated work.

## Cross-book connections

Across ten chapters ingested, the FoDE material repeatedly rhymes with and refines concepts from other ingested books. The strongest throughlines:

**With [[designing-data-intensive-applications]]:**

- FoDE's [[live-data-stack]] and [[data-application-fusion]] are the cloud-productised form of Kleppmann's [[unbundling-databases]] vision and [[derived-data]] framing — same technical direction, different rhetorical frame (cloud engineers vs. database researchers).
- FoDE's [[stream-transform-load|STL]] is Kleppmann's derived-data pipeline under a new name.
- FoDE's [[batch-processing]] "batch is a specialisation of streaming" stance directly adopts Kleppmann's and Beam's unification argument — see [[dataflow-model]].
- FoDE's [[event-streams]] coverage draws on the DDIA Ch 11 stream-processing treatment (four types of time, partitioning, windowing).
- FoDE's [[data-ethics]] echoes DDIA Ch 12's ethics section almost point for point.

**With [[building-event-driven-microservices]]:**

- [[data-contract]] is FoDE's formalisation of the producer-consumer contract that Bellemare makes central to EDM.
- [[data-application-fusion]] is the data-engineering-team view of what Bellemare calls [[event-driven-microservices|event-driven microservices]].
- [[schema-evolution]] is covered similarly in both: explicit schemas, registry, backward/forward compatibility, DLQ as last resort.

**With [[site-reliability-engineering]]:**

- [[dataops]] is the data-flavoured descendant of [[devops-vs-sre|DevOps]]/SRE culture; the automation/observability/incident-response triad is the same pattern.
- [[orchestration]] sits directly above [[distributed-cron]] — FoDE's orchestrators are reliability layers on top of the cron-like primitive SRE Ch 24 describes.
- [[stream-processing]] and [[google-workflow]] — Google Workflow is the prototype of the modern stream processor; SRE Ch 25's failure-mode catalogue for periodic pipelines is the operational counterpart to FoDE's optimistic framing.
- [[data-observability]]'s SPC inheritance and DODD framing echo SRE's [[four-golden-signals]] and monitoring culture.

**With [[fundamentals-of-software-architecture]]:**

- [[data-architect]] as *Architectus Oryzus* lifts Richards/Ford's hands-on architect ideal and applies it to data.
- [[loose-coupling]] and [[reversible-vs-irreversible-decisions]] reuse the same software-architecture principles verbatim in the data-architecture context.
- [[principles-of-good-data-architecture]] is a direct parallel to Richards/Ford's *Laws of Software Architecture*, including the "everything is a trade-off" first law.

## Related pages

- [[designing-data-intensive-applications]]
- [[building-event-driven-microservices]]
- [[site-reliability-engineering]]
- [[fundamentals-of-software-architecture]]
- [[future-of-data-engineering]]
