# Data Gravity

**Summary**: Once large volumes of data land in a specific cloud or storage system, moving it out becomes prohibitively expensive, so everything else gets pulled toward it. Cloud providers monetise gravity directly via **data egress fees**. Reis and Housley treat this as one of the core cost traps of the cloud.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The mechanism

Chapter 4 names data gravity in its discussion of cloud economics (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Vendors want to lock you into their offerings. Getting data onto the platform is cheap or free on most cloud platforms, but getting data out can be extremely expensive. Be aware of data egress fees and their long-term impacts on your business before getting blindsided by a large bill.

The asymmetry is deliberate. Ingress (into the cloud) is free or cheap — the vendor wants your data. Egress (out of the cloud) is priced per-gigabyte because the vendor wants the data to *stay*.

> Data gravity is real: once data lands in a cloud, the cost to extract it and migrate processes can be very high.

## Why it matters

Data gravity is one of the strongest forms of vendor lock-in in the cloud era, and it accumulates silently:

- **Every new workload on the same cloud increases gravity.** The more data and processes you have in one place, the more expensive it is to move any piece out — and the cheaper it is to keep adding workloads there.
- **[[multicloud|Multicloud strategies suffer]].** If the "best-of-breed" strategy requires moving data between clouds, egress charges make it uneconomical at scale.
- **[[cloud-repatriation|Repatriation is expensive]].** Dropbox, Cloudflare, Netflix's CDN — companies with enough network bandwidth that egress charges would dominate their cost structure.
- **"Cloud of clouds" services try to finesse it** — Snowflake's multi-cloud account model with scheduled replication is explicitly designed to reduce the cost of moving data between clouds.

## Relationship to TOCO

Data gravity is the mechanism by which cloud [[total-opportunity-cost-of-ownership|TOCO]] accumulates. Chapter 4's "bear trap" framing maps directly onto it: easy to pour data into a cloud; painful to extract it later.

## Practical implications

- **Estimate egress before committing.** When evaluating a cloud stack, model the cost of moving data out — not just this year, but as data grows.
- **Design flows to minimise egress.** The [[hybrid-cloud]] analytics pattern works because data flows predominantly one way (on-prem → cloud), avoiding egress charges.
- **Prefer tools that support open formats.** Parquet, Iceberg, Delta — storage formats that are interoperable reduce the "re-ingestion" cost of moving data elsewhere.
- **Keep the [[total-opportunity-cost-of-ownership|escape plan]] current.** Chapter 4's core advice for the single-cloud strategy: know what it would cost to leave, even if you never do.

## Related pages

- [[cloud]]
- [[multicloud]]
- [[hybrid-cloud]]
- [[cloud-repatriation]]
- [[total-opportunity-cost-of-ownership]]
- [[total-cost-of-ownership]]
- [[finops]]
- [[interoperability]]
- [[technology-selection]]
