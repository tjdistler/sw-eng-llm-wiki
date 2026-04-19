# Separation of Storage and Compute

**Summary**: The architectural move that defines cloud-era data platforms: keep durable data in cheap, shared [[object-storage]]; spin up **ephemeral compute clusters** on demand to query, transform, or serve it; tear them down when idle. The opposite pattern — **colocation** — couples storage and compute on the same nodes and was the defining trait of earlier systems like [[mapreduce|MapReduce-on-HDFS]]. In practice, modern systems **hybridise** the two.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The two designs

### Colocation

Data sits on the same nodes that process it. A query job is **scheduled onto the nodes that already hold the relevant data**; the scan is local disk, only the shuffle and reduce phases go over the network (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

- **Classic example.** [[mapreduce|MapReduce]] on [[distributed-filesystems|HDFS]]: the NameNode tells the scheduler which blocks live where; map tasks run next to their input.
- **Transactional databases.** Data in local block storage — even virtualised block storage like EBS — stays close to the host for low-latency disk I/O.
- **Strength.** Best-case performance: memory-bus or local-disk speed for scans, network reserved for shuffle. Filter-heavy map steps reduce data volume before it ever crosses the network.
- **Weakness.** Storage and compute must scale together. Peak workloads mean over-provisioning; idle clusters still burn money. Expanding the cluster is a heavy operation.

### Separation

Data lives in [[object-storage]]; compute is ephemeral. Queries pull data over the network each time, trading locality for elasticity (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

Reis and Housley identify two driving motivations:

- **Ephemerality and scalability.** Workloads vary wildly; pay-as-you-go is dramatically cheaper when servers can scale to zero. Engineers can spin up huge clusters to finish a nightly batch job, then delete them. The peak throughput of a 1,000-node ephemeral cluster can beat any realistic colocated cluster, even accounting for object-storage bandwidth.
- **Durability and availability.** Cloud object stores replicate across availability zones; a regional failover is just "start compute in a different region." Copying object storage across regions further hardens against misconfiguration or disaster.

This shift is what cloud data warehouses (Snowflake, BigQuery, Redshift RA3) and [[data-lakehouse|lakehouses]] rely on. Object storage at the bottom, query engines spun up on demand.

## The hybrid reality

Chapter 6 is blunt: "The practical realities of separating compute from storage are more complicated than we've implied. In reality, we constantly hybridize colocation and separation to realize the benefits of both approaches" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Two hybridisation techniques dominate:

### Multitier caching

Use object storage for long-term data retention, but **stage it into faster local storage during processing**. Concrete patterns (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **AWS EMR + S3 + HDFS.** EMR clusters spin up temporary HDFS on SSDs, pull source data from S3, keep intermediate step outputs local on HDFS, write final results back to S3. Local HDFS is the cache; S3 is the source of truth.
- **Apache Spark.** Spark heavily caches in RAM for iterative processing. Running Spark on colocated hardware is expensive because DRAM is expensive; separating compute and storage lets engineers rent massive amounts of RAM for a job and release it when done.
- **Apache Druid.** Druid keeps a single copy of data on cluster SSDs for performance, backed by object storage for durability. If a node dies or the cluster is torn down, data can be rebuilt from the object store.

### Hybrid object storage

Cloud vendors expose features that **narrow the latency gap** between object and block storage, often without giving engineers explicit control (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Google BigQuery on [[colossus]].** BigQuery uses Colossus's fine-grained block-placement to colocate customer tables in a single location, achieving ultra-high-bandwidth reads — effectively hybrid object storage, even though the customer only sees an object-store interface.
- **Amazon S3 Select.** Filters object data directly inside the S3 cluster before returning bytes over the network, cutting bandwidth use for selective queries.

Chapter 6's prediction: "public clouds will adopt hybrid object storage more widely to improve the performance of their offerings." The cleanness of the object-storage abstraction hides substantial back-end complexity designed to recover what pure separation would give away.

## Zero-copy cloning

A specific capability that falls out of storage/compute separation: **zero-copy cloning** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Creating a clone of a table just creates **new pointers to the existing object-storage files**. Future writes go to the clone; the original is untouched. No physical copy is performed.

This is a familiar abstraction for anyone who has used shallow copying in Python — and it has the same hazard. In systems that expose the underlying object store (Databricks, some lake setups), **deleting the files in the original can wipe out the clone**. Fully managed systems (Snowflake, BigQuery) hide the object store and eliminate the hazard at the cost of less flexibility. "Deep copying" is an escape hatch: physically copy all referenced objects. More expensive, but robust against accidental deletion.

## Why the trajectory matters

Separation of compute and storage is what makes the cloud data platform **economically attainable for small organisations**. A team of five can run Spark on petabyte-scale data without owning a datacenter — spin up a transient cluster, read from S3, write back, tear down. The pay-as-you-go model matches workload variance. In 2010 this required Netflix-scale ops teams to do on-prem Hadoop; in 2022 it is a few lines of Terraform.

The downstream consequence Chapter 6 calls out is that **the lines between OLAP databases and data lakes are blurring** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Cloud warehouses use object storage; lakehouses adopt warehouse-style table semantics. See [[data-lakehouse]] and [[lakehouse-table-formats]] for the concrete convergence.

## Cross-book connections

- [[hadoop-vs-mpp-databases]] (DDIA) — the historical Hadoop-vs-warehouse debate was partly about colocation vs external data.
- [[cloud]], [[elasticity]] — storage/compute separation is one of the cloud's defining economic advantages.
- [[data-gravity]] — separation only works because moving bytes between storage and compute inside a cloud region is cheap. Cross-region or cross-cloud egress reverses the calculus.

## Related pages

- [[object-storage]]
- [[data-lakehouse]]
- [[lakehouse-table-formats]]
- [[data-warehousing]]
- [[data-lake]]
- [[distributed-filesystems]]
- [[colossus]]
- [[mapreduce]]
- [[cloud]]
- [[elasticity]]
- [[data-gravity]]
- [[data-storage-stage]]
