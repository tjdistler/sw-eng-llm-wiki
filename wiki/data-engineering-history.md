# Data Engineering History

**Summary**: A four-era sketch of how the [[data-engineer]] role evolved — from 1980s data warehousing, through the big-data and cloud inflections of the 2000s, to the modularised "modern data stack" of the 2020s. The recurring theme is that old ideas come back under new names: what feels revolutionary one decade becomes foundational the next.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## Era 1: 1980–2000 — data warehousing and the web

The role traces back to the 1970s relational database and SQL work at IBM, popularised by Oracle. The **business data warehouse** took shape in the 1980s; **Bill Inmon** coined the term "data warehouse" in 1990. **Ralph Kimball** and Inmon developed their eponymous dimensional and normalised modelling approaches — still in use today (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Key developments:

- **MPP databases** (massively parallel processing) — multiple processors crunching previously unheard-of data volumes.
- **BI engineer, ETL developer, data warehouse engineer** — role titles that were the direct ancestors of the modern [[data-engineer]].
- **The dot-com boom** (mid-1990s) spawned AOL, Yahoo, Amazon, and countless backend systems nobody had scaled before. Infrastructure was expensive, monolithic, and heavily licensed.

See [[data-warehousing]] for the warehouse architecture itself.

## Era 2: Early 2000s — birth of contemporary data engineering

The dot-com bust left survivors (Yahoo, Google, Amazon) running up against the limits of traditional relational/warehouse tech. Simultaneously, commodity hardware became cheap. The "big data" era began (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Named inflections:

- **Three V's of big data** — *velocity, variety, volume*.
- **2003** — Google publishes the **Google File System** paper.
- **2004** — Google publishes the **[[mapreduce|MapReduce]]** paper.
- **2006** — Yahoo engineers open-source **Apache Hadoop**, inspired by those papers.
- **AWS (EC2, S3, DynamoDB)** — Amazon's own scaling pain turned into the first popular public cloud, virtualising and reselling commodity hardware. Azure, GCP, and DigitalOcean followed.

Antecedents existed (MPP warehouses, experimental-physics data management), but Google's papers were the "big bang" for data technologies. See [[hadoop-vs-mpp-databases]] for the MPP-vs-Hadoop comparison.

## Era 3: 2000s–2010s — big data engineering

Hadoop-ecosystem tools (Pig, Hive, HBase, Dremel, Storm, Cassandra, Spark, Presto) matured rapidly. For the first time any company could use the same tools as top tech companies. The field transitioned from **batch computing to event streaming**, launching the "real-time" era. **Big data engineers** were born — software engineers proficient in distributed infrastructure hacking who mostly maintained massive commodity clusters (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Then came the backlash. Big data became a victim of its own success:

- Companies stood up Hadoop clusters to process a few gigabytes.
- Dan Ariely's famous tweet: *"Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it."*
- Managing open-source big-data tooling was itself a full-time job; whole teams costing millions existed to babysit clusters that rarely delivered proportional business value.

**Simplification** killed the term. The tools matured, managed services took over cluster administration, and "big data engineer" became simply **data engineer** again. The term "big data" is now essentially a relic of a particular era (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Era 4: 2020s — engineering for the data lifecycle

Tooling proliferated at an astonishing rate. The authors' preferred framing for today's data engineer is **data lifecycle engineer** — see [[data-engineering-lifecycle]] (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

Characteristic shifts:

- **Decentralized, modular, managed, highly abstracted** tools. The "modern data stack" is a LEGO of best-of-breed services.
- **Interoperation is the core skill.** Connecting tools matters more than building them.
- **Focus moved up the value chain** — security, data management, [[dataops]], data architecture, orchestration — and away from low-level plumbing.
- **"Enterprisey" concerns return.** Data quality, governance, [[data-lineage|lineage]], cataloguing — the concerns pre-big-data enterprises always had — are back, now in smaller companies too, but reimagined around decentralisation and agility rather than command-and-control.
- **Privacy and compliance are core skills.** Data engineers now work fluently with GDPR, CCPA, anonymisation, data garbage collection.

## Era 5: 2020s onward — toward the live data stack (Chapter 11's prediction)

Chapter 11 extends the history into speculation. Reis and Housley argue the [[modern-data-stack]] is already an "era 4" pattern — cloud-repackaged warehouse concepts — and predict a coming [[live-data-stack]] era defined by (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Streaming by default** — batch ingestion becomes the new dial-up modem.
- **[[real-time-olap|Real-time OLAP databases]]** — Druid, ClickHouse, Rockset, Firebolt class.
- **[[stream-transform-load|STL]] instead of ELT** — transformation moves into the stream.
- **[[data-application-fusion|Application/data fusion]]** — application stacks and data stacks merge.
- **[[cloud-data-os|Cloud data OS]]** — standardised APIs, formats, catalogs, and data-aware orchestration.
- **[[enterprisey-data-engineering|"Enterprisey"]] concerns continue trickling down** — governance, quality, observability, operations.

The chapter honestly hedges: the safer predictions are the tooling simplification and enterprisey trickle-down; the live-data-stack paradigm shift is more speculative.

## The recurring pattern

What's old is new again. Every era rediscovers concerns the previous era "solved" and re-solves them under different names and with different distribution. Kimball-and-Inmon modelling was near-dead during peak MapReduce; it's now back in dbt and modern SQL warehouses. Enterprise governance was "for banks"; it's now in every well-run Stage 3 ([[data-maturity|leading-with-data]]) company (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## Related pages

- [[data-engineer]]
- [[data-engineering-lifecycle]]
- [[data-maturity]]
- [[data-warehousing]]
- [[hadoop-vs-mpp-databases]]
- [[mapreduce]]
- [[fundamentals-of-data-engineering]]
- [[future-of-data-engineering]]
- [[live-data-stack]]
- [[modern-data-stack]]
