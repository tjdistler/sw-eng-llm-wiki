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
