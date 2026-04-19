# Data Lifecycle Management

**Summary**: The management of data archival, retention, and destruction at the end of its useful life — a facet of [[data-management]]. The rise of cloud pay-as-you-go storage and privacy regulation (GDPR, CCPA) has forced engineers to pay attention to *what happens at the end* of the [[data-engineering-lifecycle]], where previously data was simply accumulated forever.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Why engineers stopped ignoring the end

Chapter 2 observes that the advent of [[data-lake|data lakes]] "encouraged organizations to ignore data archival and destruction" — when storage is cheap and bottomless, why discard anything? Two forces have changed the calculus (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

### 1. Cloud storage economics

In the cloud, storage is pay-as-you-go instead of up-front capex for on-prem storage. "When every byte shows up on a monthly AWS statement, CFOs see opportunities for savings."

Cloud environments make archival straightforward: major vendors offer archival-specific object-storage classes (S3 Glacier, GCS Archive, Azure Archive) with very cheap monthly storage and high retrieval prices, plus extra policy controls to prevent accidental or deliberate deletion of critical archives (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). See [[data-temperature]].

### 2. Privacy and retention regulation

GDPR and CCPA require engineers to **actively manage data destruction** to respect users' "right to be forgotten." Data engineers must know what consumer data they retain and have procedures to destroy it in response to requests and compliance requirements (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## How destruction works across storage types

| Store type | Destruction story |
|---|---|
| **Cloud data warehouse** | Straightforward — SQL `DELETE` with a `WHERE` clause. |
| **Data lake (classic, write-once-read-many)** | Harder — the default was append-only files. Tools like **Hive ACID** and **Delta Lake** make scalable deletion transactions practical. |
| **Object storage (archival)** | Per-object deletion; policy controls to prevent accidental deletion of what you *must* retain. |

(source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md)

## Supporting tooling

Chapter 2 notes that new generations of [[metadata|metadata management]], [[data-lineage|lineage]], and cataloguing tools "will also streamline the end of the data engineering lifecycle" — because you cannot destroy data compliantly if you cannot find it or know who depends on it (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Ch 6 — storage lifecycle vs. data retention

Chapter 6 splits the broader "lifecycle" question into two related but distinct decisions (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Data storage lifecycle** — "How important is the data to downstream users, and how often do they need to access it?" → choose the storage tier (hot / warm / cold). See [[data-temperature]].
- **Data retention** — "How long should I keep this data?" → choose retention duration. See [[data-retention]].

The two compose. Example: keep CDC events in hot storage for 30 days, move to warm for 1 year, tier to archival for 7 years, then delete.

Chapter 6 is explicit about automating this with **cloud lifecycle policies**: move to Infrequent Access after N days, to archival after M days, delete after P days. The engineer sets the policy once; the cloud enforces it. Without automation, lifecycle decisions decay into "nobody ever deletes anything, and the bill keeps growing."

## Ch 6 — retention's four inputs

Chapter 6 defines **four things to think about with data retention** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Value.** Is this data asset worth retaining? Can it be re-created by rerunning pipelines from upstream? What is the impact to downstream users if it's gone?
2. **Time.** Value decays with age. Hot-storage limits may force time-to-live (TTL) settings.
3. **Compliance.** HIPAA, PCI, etc. often *require* minimum retention; GDPR/CCPA often *require* deletion on request or past defined windows. The engineer must support both directions.
4. **Cost.** Data has an ROI. Implement automatic lifecycle policies to move aging data to cheaper tiers; delete what's past useful life.

See [[data-retention]] for the full treatment.

## Cross-book connections

- [[backups-vs-archives]] names the orthogonal reliability distinction: a backup is for restoring, an archive is for retaining.
- [[data-ethics]] — privacy-regulation compliance is an ethical floor, not a ceiling.

## Related pages

- [[data-management]]
- [[data-engineering-lifecycle]]
- [[data-temperature]]
- [[data-retention]]
- [[data-ethics]]
- [[data-lineage]]
- [[metadata]]
- [[backups-vs-archives]]
- [[object-storage]]
- [[lakehouse-table-formats]]
