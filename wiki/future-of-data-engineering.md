# Future of Data Engineering

**Summary**: Reis and Housley's closing chapter of *Fundamentals of Data Engineering* — a set of forward-looking predictions about where the discipline is going. The central forecast is a shift from the batch-oriented [[modern-data-stack]] to a streaming-first [[live-data-stack]] in which applications, analytics, and ML are fused in real time. Secondary predictions: the [[data-engineering-lifecycle]] survives intact, tooling gets simpler, a cloud-scale "data OS" emerges, data engineering becomes [[enterprisey-data-engineering|"enterprisey"]], and role boundaries between SWE / DE / DS / MLE blur.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The chapter's framing

Chapter 11 opens with a disclaimer: nobody can predict the future, and the entire point of the book is to focus on durable concepts (the lifecycle and undercurrents) rather than specific tools. But Reis and Housley have watched the field evolve from a front-row seat and are willing to go on record with speculation — some safer, some wilder (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

The chapter groups its predictions into roughly seven themes, each covered in its own section below and in dedicated wiki pages.

## Prediction 1: The lifecycle isn't going away

Despite breathless claims that easier tools will eliminate the [[data-engineer]] role, Reis and Housley call that thinking "shallow, lazy, and shortsighted" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). As organisations use data in new ways, new foundations and workflows are needed; the [[data-engineering-lifecycle]] is the engineer's home. If tooling gets easier, data engineers **move up the value chain** to higher-level work — the same arc mobile app developers went through as iOS/Android matured.

See [[data-engineer]] for the evolving role.

## Prediction 2: Decline of complexity, rise of easy-to-use tools

Simplified, SaaS-managed, commodity cloud services keep lowering the barrier to entry. Big data was a victim of its own success — once-impossibly-hard systems (petabyte SQL) are now a GCP account away. Managed OSS blurs the line between open source and proprietary. Off-the-shelf [[managed-connector|managed connectors]] (Fivetran, Airbyte) let engineers stop maintaining bespoke API plumbing and focus on unique business problems (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

The field-wide effect: data engineering grows, not shrinks, because more companies can afford to do it.

## Prediction 3: The cloud-scale data OS and improved interoperability

Today's simplified cloud data services (BigQuery, Snowflake, Blob Storage, Lambda) resemble operating-system services — but at multi-machine scale. The next frontier is a **standardised "data OS"** at a higher level of abstraction: standard data APIs, standard file formats as the batch interface layer (Parquet, Avro), standard metadata catalogs (successors to the Hive Metastore), and data-aware orchestration platforms that integrate cataloging, lineage, IaC, and CI/CD (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

See [[cloud-data-os]] for the full prediction.

## Prediction 4: "Enterprisey" data engineering

As tooling stabilises, the focus shifts from hard technology problems to the **boring stuff that big companies already do well** — data management, governance, operations, quality. Reis and Housley expect this to trickle down to all sizes of organisation, making data engineering more [[enterprisey-data-engineering|"enterprisey"]] in the good sense (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Prediction 5: Titles and responsibilities will morph

Boundaries between [[data-engineer|data engineers]], [[software-engineering-for-data|software engineers]], data scientists, and ML engineers are already fuzzy and will keep blurring (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **ML engineer ↔ data engineer** — a new ML-focused engineer sits between them, owning model automation, monitoring, and the data pipelines that feed models. Research ML stays specialised.
- **Software engineer ↔ data engineer** — [[data-application-fusion|data applications]] force SWEs to learn streaming, pipelines, modeling, and quality. DEs get integrated into product-development teams. The "throw it over the wall" pattern dies.

## Prediction 6: Beyond the modern data stack — the live data stack

The chapter's flagship prediction. The [[modern-data-stack]] brought warehouse-based analytics to the masses, but it's "basically a repackaging of old data warehouse practices" and is fundamentally batch-oriented. The [[live-data-stack]] uses streaming pipelines and [[real-time-olap|real-time OLAP databases]] to fuse applications, analytics, and ML in real time — the way TikTok, Uber, DoorDash already do internally (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

Sub-predictions that flow from the live data stack:

- **Streaming-first ingestion.** Batch ingestion will eventually look like dial-up modems. See [[ingestion-frequency]].
- **Streaming transformation — STL, not ELT.** See [[stream-transform-load]].
- **Purpose-built streaming OLAP databases.** Druid, ClickHouse, Rockset, Firebolt. See [[real-time-olap]].
- **Streaming-friendly modeling.** Upstream definitions layer in the source application; modeling at every stage. See [[streaming-data-modeling]].
- **Data-application fusion.** Application stacks and data stacks become one. See [[data-application-fusion]].
- **Tight application-ML feedback loops.** Most applications integrate ML because data is too voluminous to process by hand. See [[feature-store]] and [[model-drift]].

## Prediction 7: Dark matter data — spreadsheets rise

The most-used data platform in the world is the spreadsheet (700M–2B users). Spreadsheets are **interactive data applications that support complex analytics** — accessible to the whole spectrum of users, something BI tools have never managed. Reis and Housley predict a new class of tool that marries spreadsheet interactivity with the backend power of cloud OLAP. See [[spreadsheets-as-data-platform]] (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Prediction hedging

The chapter explicitly calls out which predictions are safer than others (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Safer:** simplification of managed tooling, rise of [[enterprisey-data-engineering|"enterprisey"]] data engineering. These have been happening day by day.
- **More speculative:** the [[live-data-stack]]. It's a significant paradigm shift and could stall; many companies may stick with batch.

Reis and Housley hedge: "Surely, other trends exist that we have completely failed to identify." The honest position is that technology evolution involves complex interactions of technology and culture, both unpredictable.

## The conclusion's advice

The book closes with advice to practitioners (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Read, listen, participate.** Books, blog posts, papers, meetups, talks — treat vendor claims with a healthy grain of salt.
- **Focus on the lifecycle and the customer.** Don't lose sight of the larger goals.
- **Tool adoption matters as much as tool creation.** Real-time technology will become an industry standard through people putting it to good use in real applications.

## Cross-book resonance

Many of Chapter 11's predictions echo [[designing-data-intensive-applications]]'s closing chapter on [[unbundling-databases]] and the [[dataflow-model|dataflow model]]:

- The **live data stack** is a product-of-cloud-services version of Kleppmann's [[unbundling-databases|unbundled database]] — both fuse OLTP and OLAP around a streaming substrate.
- Reis & Housley's **STL** is Kleppmann's [[derived-data]] pipeline under a new name.
- The **data-application fusion** prediction is Kleppmann's "stream operators as microservices" and "reads as events" ideas applied to the business world.
- [[kappa-architecture]] and the [[dataflow-model]] are the theoretical foundations of the live-data-stack pitch.

From [[building-event-driven-microservices]]: the live data stack's "applications emit events, stream processors react, data and intelligence flow" architecture is precisely Bellemare's [[event-driven-microservices|event-driven microservices]] pattern — just extended with real-time OLAP and ML on the output side.

## Related pages

- [[fundamentals-of-data-engineering]]
- [[live-data-stack]]
- [[real-time-olap]]
- [[cloud-data-os]]
- [[enterprisey-data-engineering]]
- [[stream-transform-load]]
- [[data-application-fusion]]
- [[spreadsheets-as-data-platform]]
- [[modern-data-stack]]
- [[data-engineering-lifecycle]]
- [[data-engineer]]
- [[unbundling-databases]]
- [[dataflow-model]]
- [[kappa-architecture]]
