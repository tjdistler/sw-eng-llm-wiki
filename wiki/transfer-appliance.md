# Transfer Appliance

**Summary**: A physical storage device — shipped, loaded with customer data, shipped back — that cloud vendors use to bulk-import data that would be impractical or costly to send over the internet. AWS Snowball, Google Transfer Appliance, and AWS Snowmobile (a literal semitrailer) are the canonical examples. Reis and Housley's heuristic: consider a transfer appliance when your data volume "hovers around 100 TB" or more, and remember that it is a **one-time event, not an ongoing transport**.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## Why appliances exist

Ch 7's framing: "For massive data (100 TB or more), transferring data directly over the internet may be a slow and costly process. At this scale, the fastest, most efficient way to move data is not over the wire but by truck" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Two costs dominate at multi-TB scale:

- **Time.** Consumer-grade and even business-grade internet connections take days to weeks to push 100 TB, and the transfer is vulnerable to interruption.
- **Egress fees.** Cloud providers bill heavily for data egress. Sending tens or hundreds of TB between clouds over the internet is **"a costly proposition"** regardless of available bandwidth (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

A physical appliance sidesteps both.

## How it works

"Simply order a storage device, called a transfer appliance, load your data from your servers, and then send it back to the cloud vendor, which will upload your data" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

For truly enormous volumes, AWS offers **Snowmobile**, a transfer appliance shipped in a semitrailer — "intended to lift and shift an entire data center, in which data sizes are in the petabytes or greater" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Multicloud and hybrid-cloud moves

Appliances are handy when migrating between clouds or building hybrid-cloud setups. Reis and Housley's example: "Amazon's data transfer appliance (AWS Snowball) supports import and export. To migrate into a second cloud, users can export their data into a Snowball device, and then import it into a second transfer appliance to move data into GCP or Azure. This might sound awkward, but even when it's feasible to push data over the internet between clouds, data egress fees make this a costly proposition. Physical transfer appliances are a cheaper alternative when the data volumes are significant" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## One-time, not ongoing

The hard rule: "transfer appliances and data migration services are one-time data ingestion events and are not suggested for ongoing workloads" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

An appliance is the right answer for a migration. For **continuous** movement — hybrid or multicloud — the data should be small enough (once broken into batches or streams) to move online. If an ongoing workload is producing 100 TB a month, the architecture almost certainly needs to change, not the transport.

## Relation to data-migration planning

Transfer appliances sit inside the broader [[data-migration]] playbook. For a migration of hundreds of terabytes or more:

1. Stage data onto the appliance at the source.
2. Ship the appliance to the cloud vendor.
3. Vendor uploads into customer-owned [[object-storage|object storage]].
4. Run the downstream ingestion pipeline (schema validation, transformation, loading into the target database) from object storage as if it were any other [[file-based-ingestion|file-based ingestion]] source.

The appliance handles step 1-3; everything after is a normal pipeline.

## Related pages

- [[data-migration]]
- [[data-ingestion]]
- [[object-storage]]
- [[data-gravity]]
- [[multicloud]]
- [[hybrid-cloud]]
- [[file-based-ingestion]]
