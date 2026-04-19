# Wiki Log

Append-only record of all operations.

---


## 2026-04-18 — Fundamentals of Data Engineering (Reis & Housley) — start

- Created wiki/fundamentals-of-data-engineering.md book summary with ingestion status table.
- Added entry to wiki/index.md under "Source summaries".

## 2026-04-18 — FoDE Ch 1 ingested

- Created wiki/data-engineer.md
- Created wiki/data-engineering-lifecycle.md
- Created wiki/data-maturity.md
- Created wiki/dataops.md
- Created wiki/type-a-vs-type-b-data-engineers.md
- Created wiki/data-engineering-history.md
- Created wiki/data-engineer-stakeholders.md
- Created wiki/data-science-hierarchy-of-needs.md
- Updated wiki/fundamentals-of-data-engineering.md (Ch 1 status, concept list)
- Updated wiki/index.md (new "Data engineering discipline" section)

## 2026-04-18 — FoDE Ch 2 ingested

Created (lifecycle stages):
- Created wiki/source-systems.md
- Created wiki/data-storage-stage.md
- Created wiki/data-temperature.md
- Created wiki/data-ingestion.md
- Created wiki/data-transformation.md
- Created wiki/data-serving.md
- Created wiki/analytics.md
- Created wiki/reverse-etl.md
- Created wiki/etl-vs-elt.md
- Created wiki/data-lake.md
- Created wiki/data-lakehouse.md
- Created wiki/feature-store.md

Created (undercurrents):
- Created wiki/data-security.md
- Created wiki/least-privilege.md
- Created wiki/data-management.md
- Created wiki/data-governance.md
- Created wiki/metadata.md
- Created wiki/data-quality.md
- Created wiki/master-data-management.md
- Created wiki/data-modeling.md
- Created wiki/data-lifecycle-management.md
- Created wiki/data-architecture.md
- Created wiki/orchestration.md
- Created wiki/software-engineering-for-data.md
- Created wiki/infrastructure-as-code.md
- Created wiki/data-observability.md
- Created wiki/data-catalog.md

Augmented:
- Updated wiki/data-engineering-lifecycle.md (stage-entanglement detail, top-level goals, full undercurrent map)
- Updated wiki/dataops.md (three pillars; data products vs software products; maturity arc)
- Updated wiki/data-lineage.md (FoDE audit-trail framing; DODD; GDPR destruction)
- Updated wiki/data-ethics.md (FoDE lifecycle-undercurrent framing)
- Updated wiki/change-data-capture.md (FoDE push/pull flavours)
- Updated wiki/batch-processing.md (FoDE "batch is a specialisation of streaming" framing)
- Updated wiki/stream-processing.md (FoDE streaming-at-ingestion perspective)
- Updated wiki/schema-evolution.md (FoDE source-system and metadata framing)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 2 status, new Ch 2 section)
- Updated wiki/index.md (new "Data engineering lifecycle stages" and "Data engineering undercurrents" sections)

## 2026-04-18 — FoDE Ch 3 ingested

Created (principles and roles):
- Created wiki/principles-of-good-data-architecture.md
- Created wiki/well-architected-framework.md
- Created wiki/cloud-native-principles.md
- Created wiki/data-architect.md
- Created wiki/loose-coupling.md
- Created wiki/finops.md
- Created wiki/zero-trust-security.md
- Created wiki/shared-responsibility-model.md
- Created wiki/elasticity.md
- Created wiki/brownfield-vs-greenfield.md

Created (patterns):
- Created wiki/data-mart.md
- Created wiki/modern-data-stack.md
- Created wiki/kappa-architecture.md
- Created wiki/dataflow-model.md
- Created wiki/iot-architecture.md
- Created wiki/data-mesh.md
- Created wiki/data-as-a-product.md

Augmented:
- Updated wiki/data-architecture.md (Ch 3 working definition, operational vs technical, good-architecture framing)
- Updated wiki/data-lake.md (Ch 3 "data lake 1.0" failures and convergence narrative)
- Updated wiki/data-warehousing.md (Inmon definition, organisational vs technical, cloud DW, MPP, ELT)
- Updated wiki/data-lakehouse.md (convergence and converged data platforms)
- Updated wiki/lambda-architecture.md (FoDE framing, sequence to Kappa and Dataflow)
- Updated wiki/reversible-vs-irreversible-decisions.md (FoDE Principle 7 adoption)
- Updated wiki/event-driven-architecture.md (FoDE data-architecture treatment)
- Updated wiki/strangler-fig-pattern.md (FoDE brownfield adoption)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 3 status, new Ch 3 section)
- Updated wiki/index.md (new "Data architecture principles" and "Data architecture patterns" sections)

## 2026-04-18 — FoDE Ch 4 ingested

Created (selection framework):
- Created wiki/technology-selection.md
- Created wiki/speed-to-market.md
- Created wiki/interoperability.md
- Created wiki/cargo-cult-engineering.md

Created (cost):
- Created wiki/total-cost-of-ownership.md
- Created wiki/total-opportunity-cost-of-ownership.md
- Created wiki/opex-vs-capex.md

Created (today vs future):
- Created wiki/immutable-vs-transitory-technologies.md

Created (location):
- Created wiki/cloud.md
- Created wiki/on-premises.md
- Created wiki/hybrid-cloud.md
- Created wiki/multicloud.md
- Created wiki/cloud-repatriation.md
- Created wiki/data-gravity.md

Created (build vs buy):
- Created wiki/build-vs-buy.md
- Created wiki/open-source-software.md
- Created wiki/commercial-oss.md
- Created wiki/proprietary-walled-garden.md

Created (architecture style):
- Created wiki/monolith-vs-modular-data.md
- Created wiki/distributed-monolith.md
- Created wiki/serverless-vs-servers.md
- Created wiki/containers.md

Created (benchmarks):
- Created wiki/benchmark-wars.md

Augmented:
- Updated wiki/finops.md (TCO/TOCO/FinOps as three cost lenses; FinOps as making money)
- Updated wiki/reversible-vs-irreversible-decisions.md (Ch 4 bear-trap framing, two-year rule, escape plans)
- Updated wiki/brownfield-vs-greenfield.md (cargo-cult engineering as related failure mode)
- Updated wiki/modern-data-stack.md (stack as operational shape of Ch 4 selection criteria)
- Updated wiki/type-a-vs-type-b-data-engineers.md (Ch 4 build-vs-buy application of the split)
- Updated wiki/orchestration.md (Airflow deep-dive: advantages, disadvantages, Prefect/Dagster)
- Updated wiki/dataops.md (DataOps as undercurrent technology must support)
- Updated wiki/data-architecture.md (Ch 4 architecture-vs-tools opening)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 4 status, new Ch 4 section)
- Updated wiki/index.md (new "Technology selection" section)

## 2026-04-18 — FoDE Ch 5 ingested

Created (source-system hub + checklist):
- Created wiki/source-system-considerations.md
- Created wiki/application-database-as-source.md
- Created wiki/file-sources.md

Created (state patterns):
- Created wiki/crud.md
- Created wiki/insert-only.md

Created (API paradigms):
- Created wiki/webhooks.md
- Created wiki/graphql.md

Created (data sharing):
- Created wiki/data-sharing.md

Created (NoSQL families):
- Created wiki/key-value-store.md
- Created wiki/wide-column-database.md
- Created wiki/search-database.md
- Created wiki/time-series-database.md

Augmented:
- Updated wiki/source-systems.md (Ch 5 source-category taxonomy, stakeholders, undercurrents checklist, closing philosophy)
- Updated wiki/oltp-vs-olap.md (FoDE source-system framing; OLAP as source; data-application hybrid)
- Updated wiki/event-streams.md (message-vs-stream distinction; topics/partitions/hotspotting; four types of time)
- Updated wiki/message-brokers.md (FoDE message-queue framing; delivery frequency, ordering, scalability)
- Updated wiki/nosql.md (FoDE six-family enumeration; extraction implications)
- Updated wiki/acid.md (FoDE relax-for-performance at source-system level)
- Updated wiki/document-model.md (FoDE not-ACID framing; extraction via full scan or CDC)
- Updated wiki/relational-model.md (FoDE canonical-application-backend framing; state-capture challenge)
- Updated wiki/graph-data-models.md (FoDE three modelling-path choices for graph sources)
- Updated wiki/data-contract.md (FoDE source-system-extraction framing; Denmore definition; SLA/SLO)
- Updated wiki/data-engineer-stakeholders.md (Ch 5 systems vs data stakeholder split; feedback loop)
- Updated wiki/change-data-capture.md (Ch 5 per-vendor variability; CRUD-alternative framing)
- Updated wiki/third-party-api-integration.md (FoDE REST/GraphQL/gRPC/Webhook category survey)
- Updated wiki/data-ingestion.md (Ch 5 expansion of source-system shapes)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 5 status, new Ch 5 section)
- Updated wiki/index.md (new "Source systems (FoDE Ch 5)" section)

### 2026-04-18 — FoDE Ch 6 ingested

Created (raw ingredients):
- Created wiki/storage-raw-ingredients.md
- Created wiki/compression-algorithms.md

Created (storage systems):
- Created wiki/object-storage.md
- Created wiki/block-storage.md
- Created wiki/file-storage.md
- Created wiki/cache-memory-storage.md
- Created wiki/streaming-storage.md
- Created wiki/stream-to-batch-storage.md

Created (storage abstractions and big ideas):
- Created wiki/storage-compute-separation.md
- Created wiki/lakehouse-table-formats.md
- Created wiki/data-retention.md
- Created wiki/data-platform.md

Augmented:
- Updated wiki/data-storage-stage.md (Ch 6 three-layer model, big-ideas list, undercurrents)
- Updated wiki/data-temperature.md (hot/warm/cold Ch 6 detail; spillover; lifecycle automation; cache hierarchy)
- Updated wiki/data-lake.md (WORM retrospective; object storage as gold standard; unstructured data)
- Updated wiki/data-lakehouse.md (Ch 6 feature-list; interoperability advantage; hybrid structure)
- Updated wiki/data-warehousing.md (Ch 6 storage-abstraction framing; cloud DW + object storage; micro-partitioning)
- Updated wiki/column-oriented-storage.md (Ch 6 analytics default; partitioning+clustering; Snowflake micro-partitioning)
- Updated wiki/partitioning.md (analytics partitioning/clustering; Snowflake micro-partitioning)
- Updated wiki/distributed-filesystems.md (Ch 6 "Hadoop is dead, long live Hadoop"; HDFS mechanics recap)
- Updated wiki/eventual-consistency.md (BASE; S3 history; three consistency decision points)
- Updated wiki/data-catalog.md (Ch 6 catalog-across-layers; catalog as lakehouse ingredient)
- Updated wiki/data-lifecycle-management.md (lifecycle vs retention; four retention inputs)
- Updated wiki/schema-on-read-vs-write.md (Ch 6 storage-layer framing; schema beyond relational; lakehouse compromise)
- Updated wiki/acid.md (ACID on object storage via lakehouse table formats)
- Updated wiki/mvcc.md (MVCC in lakehouse table formats)
- Updated wiki/tombstone.md (tombstones in lakehouse table formats; GDPR deletion)
- Updated wiki/log-based-message-brokers.md (tiered storage; replay; streaming-as-storage)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 6 status, new Ch 6 section)
- Updated wiki/index.md (new "Storage systems (FoDE Ch 6)" section)

### 2026-04-18 — FoDE Ch 7 ingested

Chapter 7 ("Ingestion") from *Fundamentals of Data Engineering*.

Created (ingestion hub):
- Created wiki/data-pipeline.md
- Created wiki/ingestion-frequency.md
- Created wiki/push-vs-pull-vs-poll.md
- Created wiki/ingestion-payload.md

Created (batch ingestion patterns):
- Created wiki/snapshot-vs-differential-ingestion.md
- Created wiki/file-based-ingestion.md
- Created wiki/data-migration.md
- Created wiki/transfer-appliance.md

Created (streaming ingestion and tooling):
- Created wiki/dead-letter-queue.md
- Created wiki/managed-connector.md
- Created wiki/edi.md
- Created wiki/web-scraping.md

Augmented:
- Updated wiki/data-ingestion.md (Ch 7 deep dive: 8 considerations, sync vs async, batch/stream pattern tables, ingestion-mechanisms table, stakeholders, undercurrents)
- Updated wiki/change-data-capture.md (Ch 7 batch vs continuous CDC; bank-account missing-intermediate-changes example; CDC vs synchronous replication; source-resource cost)
- Updated wiki/etl-vs-elt.md (Ch 7 extract/load as ingestion-stage; inserts/updates/batch-size)
- Updated wiki/webhooks.md (Ch 7 recommended AWS architecture Lambda → Kinesis → Flink → S3)
- Updated wiki/data-sharing.md (Ch 7 "strictly not ingestion" caveat)
- Updated wiki/late-arriving-events.md (Ch 7 ingestion-layer framing; cutoff-time prescription)
- Updated wiki/reprocessing-event-streams.md (Ch 7 replay-as-ingestion-consideration; TTL interaction)
- Updated wiki/schema-evolution.md (Ch 7 automation-mixed-blessing; three-part defense; Git-style branching)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 7 status, new Ch 7 section)
- Updated wiki/index.md (new "Ingestion (FoDE Ch 7)" section)

### 2026-04-18 — FoDE Ch 8 ingested

Chapter 8 ("Queries, Modeling, and Transformation") from *Fundamentals of Data Engineering*.

Created (queries and performance):
- Created wiki/life-of-a-query.md
- Created wiki/query-optimizer.md
- Created wiki/query-performance-tuning.md
- Created wiki/broadcast-join.md
- Created wiki/shuffle-hash-join.md
- Created wiki/common-table-expression.md
- Created wiki/window-functions.md
- Created wiki/user-defined-function.md
- Created wiki/nested-data.md
- Created wiki/streaming-queries.md

Created (data modeling):
- Created wiki/conceptual-logical-physical-models.md
- Created wiki/normalization-levels.md
- Created wiki/inmon-model.md
- Created wiki/kimball-model.md
- Created wiki/star-schema.md
- Created wiki/snowflake-schema.md
- Created wiki/fact-table.md
- Created wiki/dimension-table.md
- Created wiki/slowly-changing-dimensions.md
- Created wiki/data-vault.md
- Created wiki/wide-denormalized-table.md
- Created wiki/one-big-table.md
- Created wiki/streaming-data-modeling.md

Created (transformations):
- Created wiki/update-patterns.md
- Created wiki/upsert.md
- Created wiki/materialized-view.md
- Created wiki/federated-query.md
- Created wiki/data-virtualization.md
- Created wiki/dbt.md
- Created wiki/feature-engineering.md
- Created wiki/data-wrangling.md
- Created wiki/metrics-layer.md

Augmented:
- Updated wiki/data-modeling.md (Ch 8 deep dive: conceptual/logical/physical, grain, three paradigms, wide-table alternatives, streaming frontier)
- Updated wiki/data-transformation.md (Ch 8 query-vs-transformation, batch transformations, update patterns, views/materialization/federation, business logic, streaming, feature engineering)
- Updated wiki/mapreduce.md (Ch 8 post-MapReduce framing; map/shuffle/reduce worked example)
- Updated wiki/feature-store.md (Ch 8 placement of feature engineering in transformation)
- Updated wiki/normalization.md (pointer to normalization-levels for full normal-form sequence)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 8 status, new Ch 8 section)
- Updated wiki/index.md (new "Queries and query performance", "Data modeling paradigms", "Transformation stage" sections)

### 2026-04-18 — FoDE Ch 9 ingested

Chapter 9 ("Serving Data for Analytics, Machine Learning, and Reverse ETL") from *Fundamentals of Data Engineering*.

Created (general considerations):
- Created wiki/trust-in-data.md
- Created wiki/data-product.md
- Created wiki/self-service-analytics.md
- Created wiki/data-definitions-and-logic.md

Created (analytics sub-varieties):
- Created wiki/business-analytics.md
- Created wiki/operational-analytics.md
- Created wiki/embedded-analytics.md

Created (ML fundamentals):
- Created wiki/model-drift.md
- Created wiki/training-test-sets.md

Created (serving mechanisms):
- Created wiki/semantic-layer.md
- Created wiki/file-exchange-serving.md
- Created wiki/serving-in-notebooks.md

Augmented:
- Updated wiki/data-serving.md (Ch 9 general considerations, serving mechanisms, per-undercurrent framing)
- Updated wiki/analytics.md (Ch 9 use-case-and-user framing; hub to three sub-variety pages)
- Updated wiki/reverse-etl.md (Ch 9 lead-scoring example; BLT renaming; feedback-loop hazard)
- Updated wiki/feature-store.md (Ch 9 DE/ML collaboration surface; factory-loom example)
- Updated wiki/metrics-layer.md (Ch 9 query-quality-vs-data-quality separation)
- Updated wiki/data-mesh.md (Ch 9 mesh-as-serving-architecture)
- Updated wiki/data-as-a-product.md (link to sibling data-product page)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 9 status, new Ch 9 section)
- Updated wiki/index.md (new serving-general-considerations, analytics sub-varieties, ML fundamentals, and serving mechanisms sections)

### 2026-04-18 — FoDE Ch 10 ingested

Chapter 10 ("Security and Privacy") from *Fundamentals of Data Engineering*.

Created (processes):
- Created wiki/security-theater.md
- Created wiki/active-security.md
- Created wiki/threat-modeling.md
- Created wiki/security-policy.md

Created (technology):
- Created wiki/encryption-at-rest.md
- Created wiki/encryption-in-transit.md
- Created wiki/secrets-management.md
- Created wiki/security-monitoring.md
- Created wiki/network-access-security.md

Augmented:
- Updated wiki/data-security.md (Ch 10 people/processes/technology organising frame; links to all new specialised pages)
- Updated wiki/least-privilege.md (Ch 10 time-boxing and revocation; column/row/cell-level controls; PII masking; broken-glass processes)
- Updated wiki/shared-responsibility-model.md (Ch 10 "most cloud breaches are end-user-caused")
- Updated wiki/zero-trust-security.md (Ch 10 cloud-vs-air-gapped framing)
- Updated wiki/backups-vs-archives.md (Ch 10 ransomware framing; backups as a security control)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 10 status, new Ch 10 section)
- Updated wiki/index.md (new "Security and privacy (FoDE Ch 10)" section)

### 2026-04-18 — FoDE Ch 11 ingested

Chapter 11 ("The Future of Data Engineering") from *Fundamentals of Data Engineering* — the final chapter.

Created (Chapter 11 predictions):
- Created wiki/future-of-data-engineering.md (chapter hub)
- Created wiki/live-data-stack.md
- Created wiki/real-time-olap.md
- Created wiki/stream-transform-load.md
- Created wiki/data-application-fusion.md
- Created wiki/cloud-data-os.md
- Created wiki/enterprisey-data-engineering.md
- Created wiki/titles-will-morph.md
- Created wiki/spreadsheets-as-data-platform.md

Augmented:
- Updated wiki/modern-data-stack.md (Ch 11 candid reassessment; MDS as cloud-repackaged warehouse; live-data-stack successor)
- Updated wiki/data-engineer.md (Ch 11 role trajectory; move up value chain; blurring titles)
- Updated wiki/data-engineering-lifecycle.md (Ch 11 lifecycle-survives / time-between-stages-collapses prediction)
- Updated wiki/data-engineering-history.md (Era 5 — toward the live data stack)
- Updated wiki/stream-processing.md (Ch 11 streaming as the default mode)
- Updated wiki/kappa-architecture.md (live data stack as practical descendant of Kappa)
- Updated wiki/dataflow-model.md (theoretical backbone of live data stack and STL)
- Updated wiki/feature-store.md (substrate for the application-ML feedback loop)
- Updated wiki/orchestration.md (Ch 11 data-aware orchestration; IaC, CI/CD, stream orchestration)
- Updated wiki/managed-connector.md (Ch 11 connectors-as-outsourced-plumbing driver of engineer focus)

Index/summary:
- Updated wiki/fundamentals-of-data-engineering.md (Ch 11 status, new Ch 11 section, Cross-book connections section)
- Updated wiki/index.md (new "Future of data engineering (FoDE Ch 11)" section)

FoDE ingestion complete.

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 1 ingested

Chapter 1 ("What Happens When There Are No 'Best Practices'?") of *Software Architecture: The Hard Parts* (Ford, Richards, Sadalage, Dehghani, 2021).

Created:
- Created wiki/software-architecture-the-hard-parts.md (book summary page)
- Created wiki/operational-vs-analytical-data.md (OLTP vs analytical split)
- Created wiki/least-worst-trade-offs.md (don't find the best; find the least worst)

Augmented:
- Updated wiki/trade-off-analysis.md (Hard Parts least-worst reframing + identify/analyze/document method)
- Updated wiki/laws-of-software-architecture.md (Hard Parts restatement + snowflake corollary)
- Updated wiki/architecture-decision-record.md (Hard Parts ADR usage; Consequences as trade-off artefact)
- Updated wiki/architecture-fitness-function.md (Hard Parts governance framing; Equifax cautionary tale)
- Updated wiki/architecture-versus-design.md (Hard Parts "hard as solidity" framing)
- Updated wiki/coupling.md (Page-Jones static-vs-dynamic split as organizing axis of the book)
- Updated wiki/saga.md (Oxford etymology; Sysops Squad literary framing)
- Updated wiki/distributed-monolith.md (Sysops Squad pathology as worked example)
- Updated wiki/data-outlives-code.md (Tim Berners-Lee framing + architecture-in-service-of-data)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 2 ingested

Chapter 2 ("Discerning Coupling in Software Architecture") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/static-coupling.md (how quanta are wired together; bootstrap-time dependencies; topology-to-quanta enumeration)
- Created wiki/dynamic-coupling.md (runtime communication coupling; three-dimensional decision space: communication × consistency × coordination)
- Created wiki/choreography.md (coordination style with no central coordinator; hub to broker-topology, event-driven, saga coverage)

Augmented:
- Updated wiki/architectural-quantum.md (Hard Parts refined definition: high static coupling + synchronous dynamic coupling; topology-to-quanta table)
- Updated wiki/connascence.md (static/dynamic lifted to architectural scale; Rule of Locality extended to quantum boundaries)
- Updated wiki/coupling.md (Ch 2 working definition; three-dimensional dynamic-coupling lens)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 2 status; added cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 3 ingested

Chapter 3 ("Architectural Modularity") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/architectural-modularity.md (hub page: degree of decomposition into deployment units; five-driver rubric; chatter caveat)
- Created wiki/agility.md (compound characteristic = maintainability + testability + deployability)
- Created wiki/testability.md (ease + completeness of testing; chatter failure mode)
- Created wiki/deployability.md (ease + frequency + risk of deployment; big-ball-of-distributed-mud warning)

Augmented:
- Updated wiki/scalability.md (Hard Parts scalability-vs-elasticity split; modularity-vs-granularity)
- Updated wiki/elasticity.md (MTTS framing; granularity-driven; concert-ticket example)
- Updated wiki/maintainability.md (scope-of-change progression; von Zitzewitz incoming-coupling metric)
- Updated wiki/fault-tolerance.md (architectural-modularity-as-bulkhead; async-to-preserve isolation)
- Updated wiki/modularity.md (code-modularity vs architectural-modularity distinction)
- Updated wiki/speed-to-market.md (Ford/Richards business-driver hierarchy; agility as enabler)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 3 status; added new-page cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 4 ingested

Chapter 4 ("Architectural Decomposition") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/big-ball-of-mud.md (Foote 1999 antipattern; decomposability gate; coupling-metrics signature)
- Created wiki/tactical-forking.md (De La Torre; clone-then-delete; coarse-grained services; trade-offs)
- Created wiki/component-based-decomposition.md (preferred approach rubric; Ch 4 decision tree; service-based-architecture stepping-stone)

Augmented:
- Updated wiki/coupling-metrics.md (metrics as decomposability-readiness check; JDepend tool-chain)
- Updated wiki/migration-pattern-selection.md (Hard Parts Ch 4 decision tree orthogonal to Newman patterns)
- Updated wiki/service-based-architecture.md (Hard Parts framing as migration stepping-stone)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 4 status; added cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 5 ingested

Chapter 5 ("Component-Based Decomposition Patterns") of *Software Architecture: The Hard Parts*.

Created (six patterns):
- Created wiki/identify-and-size-components-pattern.md (component inventory; statements metric; standard-deviation rule; fitness functions)
- Created wiki/gather-common-domain-components-pattern.md (domain vs infrastructure cross-cutting; leaf-name heuristic; shared component vs library)
- Created wiki/flatten-components-pattern.md (component = leaf-node namespace; orphaned classes; push-down vs pull-up flattening; shared-code metric)
- Created wiki/determine-component-dependencies-pattern.md (component-level Ca/Ce; golfball/basketball/airliner triage; ArchUnit restrictions)
- Created wiki/create-component-domains-pattern.md (namespace-prefix domains; one-to-many service-to-components; domain restriction fitness function)
- Created wiki/create-domain-services-pattern.md (physical extraction into service-based architecture; soft-landing framing; per-service namespace rule)

Augmented:
- Updated wiki/component-based-decomposition.md (expanded hub: six patterns in order with cross-links)
- Updated wiki/components.md (leaf-node rule; statements-per-namespace metric from Ch 5)
- Updated wiki/architecture-fitness-function.md (table of per-pattern decomposition fitness functions)
- Updated wiki/coupling-metrics.md (component-granularity use in Determine Component Dependencies pattern)
- Updated wiki/service-based-architecture.md (soft-landing framing from Ch 5)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 5 status; added pattern cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 6 ingested

Chapter 6 ("Pulling Apart Operational Data") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/data-decomposition-drivers-and-integrators.md (six disintegrators vs two integrators; trade-off framing)
- Created wiki/data-domain.md (soccer-ball metaphor; synonyms as stepping-stone; domain vs schema distinction)
- Created wiki/database-type-selection.md (eight-family, eight-characteristic star-ratings summary)
- Created wiki/polyglot-persistence.md (Sadalage/Fowler term; endpoint of decomposition; trade-offs)
- Created wiki/newsql-database.md (scalability of NoSQL + ACID of SQL; CockroachDB, Spanner, TiDB)
- Created wiki/cloud-native-database.md (Snowflake, Redshift, Cosmos, Datomic; cost shape; lock-in)
- Created wiki/data-sovereignty.md (nirvana state; one-owner-per-DB; Step 3 outcome)

Augmented:
- Updated wiki/database-decomposition.md (hub: Hard Parts disintegrators/integrators; full five-step pattern)
- Updated wiki/relational-model.md (Hard Parts ratings; when not relational)
- Updated wiki/document-model.md (Hard Parts ratings; Sysops Squad aggregate design trade-off)
- Updated wiki/key-value-store.md (Hard Parts ratings; reference-data use case)
- Updated wiki/wide-column-database.md (Hard Parts ratings under column-family framing)
- Updated wiki/graph-data-models.md (Hard Parts ratings; relationship-type-change cost)
- Updated wiki/nosql.md (aggregate orientation; eight families; star-rating matrix reference)
- Updated wiki/time-series-database.md (Hard Parts ratings; not-general-purpose warning)
- Updated wiki/acid.md (Hard Parts: ACID as data integrator; sagas as the cost of decomposition)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 6 status; Ch 6 cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 7 ingested

Chapter 7 ("Service Granularity") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/granularity-disintegrators.md (six forces pulling services apart; service-naming test)
- Created wiki/granularity-integrators.md (four forces keeping services together; "hold until disintegrators outweigh")
- Created wiki/code-volatility.md (volatility-based decomposition; Notification Service example)

Augmented:
- Updated wiki/service-granularity.md (Hard Parts disintegrator/integrator hub; modularity-vs-granularity; architect/sponsor dialogues)
- Updated wiki/architectural-modularity.md (Ch 7 modularity-vs-granularity clarification)
- Updated wiki/architectural-quantum.md (granularity as per-quantum sizing decision; integrator-collapse caveat)
- Updated wiki/microservices.md (Ch 7 disintegrator/integrator extension to Ch 17 three-guideline test)
- Updated wiki/when-microservices-are-a-bad-idea.md (when integrators outweigh disintegrators; re-consolidation)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 7 status; Ch 7 cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 8 ingested

Chapter 8 ("Reuse Patterns") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/reuse-patterns.md (hub: replication / library / service / sidecar; decision matrix; abstraction + slow rate of change)
- Created wiki/code-replication-pattern.md (copy-source-per-service; when tiny static code makes it OK)
- Created wiki/shared-library-pattern.md (compile-time coupling; granularity; "versioning is simple" as 9th fallacy)
- Created wiki/shared-service-pattern.md (runtime coupling; performance/scalability/fault-tolerance tax; API versioning pitfalls)
- Created wiki/orthogonal-coupling.md (distinct-purposes-that-must-intersect; why sidecars are the clean answer)

Augmented:
- Updated wiki/sidecar-pattern.md (Ch 8 framing: cleanest cross-cutting reuse; Decorator-at-architecture-scale)
- Updated wiki/service-mesh.md (Ch 8: mesh as home of orthogonal coupling; governance over polyglot fleets)
- Updated wiki/gather-common-domain-components-pattern.md (Ch 5 finds candidates → Ch 8 picks shape)
- Updated wiki/static-coupling.md (reuse-pattern lens: library adds static, service doesn't, sidecar per-pod only)
- Updated wiki/dynamic-coupling.md (shared service = deliberate dynamic coupling for reuse)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 8 status; Ch 8 cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 9 ingested

Chapter 9 ("Data Ownership and Distributed Transactions") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/data-ownership.md (hub: sole / common / joint; writer-owns rule; resolution rubric)
- Created wiki/joint-ownership-techniques.md (table split / data domain / delegate / service consolidation comparison)
- Created wiki/table-split-technique.md (split shared table into two; CAP trade-off becomes explicit)
- Created wiki/delegate-technique.md (pick a delegate by primary-domain vs operational-characteristics priority)
- Created wiki/base-properties.md (BA + S + E; what remains when ACID is lost across services)
- Created wiki/compensating-update.md (semantic rollback; prerequisites; "compensation of compensation fails")
- Created wiki/background-synchronization-pattern.md (external process; breaks bounded contexts)
- Created wiki/orchestrated-request-based-pattern.md (consistency over responsiveness; compensation complexity)
- Created wiki/event-based-consistency-pattern.md (pub/sub + DLQ; Ch 9's recommended default)

Augmented:
- Updated wiki/distributed-transactions.md (Ch 9: ACID property-by-property loss; three eventual-consistency patterns)
- Updated wiki/two-phase-commit.md (Ch 9 reiteration: 2PC impractical at microservice scale)
- Updated wiki/acid.md (Ch 9 property-by-property breakage across services; BASE vocabulary)
- Updated wiki/eventual-consistency.md (Ch 9's three-pattern catalogue; default = event-based)
- Updated wiki/saga.md (Ch 9 introduces saga vocabulary; compensation-of-compensation failure)
- Updated wiki/change-data-ownership.md (Hard Parts writer-owns rule vs Newman's behaviour heuristic)
- Updated wiki/data-domain.md (Ch 9 reuse: data domain as joint-ownership technique)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 9 status; Ch 9 cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 10 ingested

Chapter 10 ("Distributed Data Access") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/distributed-data-access.md (hub: four patterns + trade-off matrix + selection rubric)
- Created wiki/interservice-communication-pattern.md (remote call per read; three latencies; tight coupling)
- Created wiki/column-schema-replication-pattern.md (replicate columns; async sync; governance softness)
- Created wiki/replicated-caching-pattern.md (Hazelcast/Ignite/Coherence; ~500 MB ceiling; static data only)
- Created wiki/data-domain-pattern.md (shared schema for read access; Ch 9 data-domain technique on reads)

Augmented:
- Updated wiki/data-ownership.md (Ch 10 cross-link for read-access side)
- Updated wiki/data-domain.md (Ch 10: data domain reused as read-access pattern)
- Updated wiki/cache-memory-storage.md (three caching models from Ch 10; replicated-cache contrast)
- Updated wiki/synchronize-data-in-application.md (contrast: migration-time vs steady-state patterns)
- Updated wiki/cross-service-analytics.md (Ch 10 lens: column-schema-replication at system scale)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 10 status; Ch 10 cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts — Ch 11 ingested

Chapter 11 ("Managing Distributed Workflows") of *Software Architecture: The Hard Parts*.

Created:
- Created wiki/workflow-orchestration.md (architecture-style orchestration; per-workflow orchestrator; error-links already exist)
- Created wiki/workflow-choreography.md (Ch 11 workflow-grain treatment; Front Controller / stateless / stamp-coupling state options)
- Created wiki/semantic-coupling.md (domain-inherent coupling; floor that implementation can worsen not reduce)
- Created wiki/distributed-workflow-patterns.md (hub: trade-off matrix + four-force rubric; fractal at style and workflow grain)

Augmented:
- Updated wiki/choreography.md (Ch 11 workflow-grain pointer; error-links-add-per-scenario observation)
- Updated wiki/saga.md (Ch 11 as coordination axis; sagas as consistency-flavour of workflow patterns; eight-pattern split)
- Updated wiki/mediator-topology.md (Ch 11 workflow-grain = workflow-orchestration; scope hierarchy)
- Updated wiki/broker-topology.md (Ch 11 workflow-grain = workflow-choreography; three state-management options)
- Updated wiki/event-driven-architecture.md (Ch 11 workflow-grain counterpart to mediator/broker topology)
- Updated wiki/dynamic-coupling.md (coordination axis pointer to Ch 11 pages)
- Updated wiki/software-architecture-the-hard-parts.md (Ch 11 status; Ch 11 cross-links)

## 2026-04-19 — Ingest *Software Architecture: The Hard Parts* Ch 12 "Transactional Sagas"

Created:
- wiki/epic-saga.md (sao — sync/atomic/orchestrated; most coupled; traditional distributed transaction)
- wiki/phone-tag-saga.md (sac — sync/atomic/choreographed; rare combination; chain-of-responsibility compensations)
- wiki/fairy-tale-saga.md (seo — sync/eventual/orchestrated; common real-world choice)
- wiki/time-travel-saga.md (sec — sync/eventual/choreographed; fire-and-forget pipelines)
- wiki/fantasy-fiction-saga.md (aao — async/atomic/orchestrated; mostly implausible)
- wiki/horror-story-saga.md (aac — async/atomic/choreographed; worst combination; cautionary)
- wiki/parallel-saga.md (aeo — async/eventual/orchestrated; strong scale-needing default)
- wiki/anthology-saga.md (aec — async/eventual/choreographed; least coupled; EDA default)

Augmented:
- wiki/saga.md (Ch 12 eight-pattern taxonomy; axis-substitution intuition; saga state machines; annotations/CLI management)
- wiki/dynamic-coupling.md (Ch 12 as canonical worked example of 3-axis model; names for all eight corners)
- wiki/distributed-transactions.md (Ch 12 eight-pattern catalogue as honest replacement for distributed transactions)
- wiki/compensating-update.md (Ch 12 compensating updates vs saga state machines trade-off)
- wiki/eventual-consistency.md (Ch 12 saga state machines as eventual-consistency error-handling primitive)
- wiki/workflow-orchestration.md (named orchestrated sagas linked)
- wiki/workflow-choreography.md (named choreographed sagas linked)
- wiki/distributed-workflow-patterns.md (saga pattern names now wikilinked)
- wiki/software-architecture-the-hard-parts.md (Ch 12 status; cross-links)

## 2026-04-19 — Ingested Software Architecture: The Hard Parts, Chapter 13 (Contracts)

Source: `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

Created:
- wiki/contracts.md (hub — strict-to-loose spectrum; trade-off matrix; microservices default pairing)
- wiki/strict-contract.md (RMI/gRPC/SOAP/XSD end of spectrum; advantages, disadvantages, when-to-pick)
- wiki/loose-contract.md (JSON name-value-pair end of spectrum; loose+CDC as microservices default)
- wiki/stamp-coupling.md (anti-pattern — over-specified contracts; bandwidth fallacy arithmetic; legit use in choreographed saga state passing)

Augmented:
- wiki/consumer-driven-contracts.md (Ch 13 push-vs-pull inversion; loose+CDC default; advantages/disadvantages)
- wiki/data-contract.md (Hard Parts' broadened "any wiring point" definition; convergence with Bellemare and FoDE framings)
- wiki/graphql.md (middle-of-spectrum case study; consumer-driven field selection defeats stamp coupling)
- wiki/protocol-buffers.md (strict end of spectrum; gRPC-over-Protobuf defaults)
- wiki/avro.md (strict-but-evolvable positioning via reader/writer schemas)
- wiki/schema-evolution.md (evolution as part of the strictness trade-off)
- wiki/backward-forward-compatibility.md (compatibility as the mechanism that keeps strict contracts workable)
- wiki/connascence.md (contract strictness as the connascence-across-boundary dial)
- wiki/static-coupling.md (Ch 13 strictness dial as the primary static-coupling lever)
- wiki/software-architecture-the-hard-parts.md (Ch 13 status; cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts Ch 14 (Managing Analytical Data)

Source: `raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md`

Created:
- wiki/data-product-quantum.md (DPQ — cooperative quantum semantics, three DPQ types, dynamic-coupling constraint, sidecar-analogy framing)

Augmented:
- wiki/data-mesh.md (Ch 14 architectural treatment; four principles restated; DPQ introduction; when-to-use trade-off)
- wiki/data-warehousing.md (Ch 14 failure modes in distributed architectures; technical-vs-domain partitioning critique)
- wiki/data-lake.md (Ch 14 reactionary-swing critique; discovery/PII/staleness issues; still technically partitioned)
- wiki/data-as-a-product.md (Ch 14 architectural consequence — introduces the DPQ; product qualities)
- wiki/data-product.md (cross-link to data-product-quantum)
- wiki/cross-service-analytics.md (Ch 14 framing as the cross-cutting problem; evolution Newman → lake → mesh)
- wiki/architectural-quantum.md (Ch 14 DPQ extension; cooperative quantum definition)
- wiki/data-governance.md (federated computational governance; sidecar-based policy enforcement)
- wiki/data-architecture.md (Ch 14 architect's verdict on technical-vs-domain partitioning across warehouse/lake/mesh)
- wiki/software-architecture-the-hard-parts.md (Ch 14 status; cross-links)

## 2026-04-19 — Software Architecture: The Hard Parts Ch 15 (Build Your Own Trade-Off Analysis) — BOOK COMPLETE

Source: `raw/software-architecture-the-hard-parts/chapter-15-build-your-own-trade-off-analysis.md`

Created:
- wiki/mece-principle.md (Mutually Exclusive Collectively Exhaustive — overlap and gap failures; role in trade-off analysis; model-vs-reality)

Augmented:
- wiki/trade-off-analysis.md (Ch 15 build-your-own method; find/analyze/assess three-step; trade-off techniques — qualitative over quantitative, MECE, out-of-context trap, modelling relevant domain cases, bottom-line-over-evidence, avoiding snake-oil and evangelism; iterative trade-off analysis; model-vs-reality)
- wiki/architecture-decision-record.md (Ch 15 — ADR as terminal step of build-your-own method; Consequences holds qualitative comparison; Alternatives should be MECE; bottom line in Decision; Superseded as audit trail for iterative re-examination)
- wiki/least-worst-trade-offs.md (Ch 15 — architect as objective arbiter; anti-evangelism stance; fitness functions as evangelism counter-measure)
- wiki/laws-of-software-architecture.md (Ch 15 — First Law made operational; iteration because each choice constrains the next; anti-evangelism corollary)
- wiki/architectural-thinking.md (Ch 15 turns aspect #3 into repeatable method)
- wiki/software-architecture-the-hard-parts.md (Ch 15 status; book marked fully ingested; cross-links)
