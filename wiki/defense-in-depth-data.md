# Defense in Depth for Data

**Summary**: Chapter 26's structural response to the [[data-integrity-failure-modes|24 failure-mode combinations]]: no single defence is sufficient, so layer complementary defences that together cover the matrix. The three named layers are [[soft-deletion]] (undelete, undo, lazy deletion), [[tiered-backup-strategy|backups and recovery]] (multi-tier, diverse media, point-in-time), and [[data-validation-pipelines|regular data validation]] (out-of-band invariant checks). [[replication]] is an overarching optimisation — occasionally helpful, never a substitute for any of the three.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`, `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## Why layers, not a single strategy

Given the many ways data can be lost, there is no silver bullet (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Instead, you need defense in depth. Defense in depth comprises multiple layers, with each successive layer of defense conferring protection from progressively less common data loss scenarios.

Each layer is strongest against a different subset of the 24 modes. The outer layers are cheap and catch the common cases; the inner layers are expensive but catch the rare ones. Together they cover a broad swathe at reasonable total cost.

## An object's journey

Chapter 26 visualises an object's lifecycle as it moves through the layers (Figure 26-2, source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

1. **Live data** — in use, protected by replication, checksums, normal availability mechanisms.
2. **Soft deleted** — user or application marked it deleted. Still recoverable by administrative code paths. See [[soft-deletion]].
3. **Lazy deleted** (developer-facing systems) — deleted by the application, purged by the cloud service provider after a grace period of days to weeks.
4. **Destroyed** — actual bytes gone.

At every stage, backups and validators provide orthogonal coverage. Even after destruction of the live copy, backups remain.

## Layer 1: Soft deletion

See [[soft-deletion]].

The primary defence against **accidental data deletion** — whether by users (trash folder), developers (API-level undelete), internal developers (lazy deletion at the storage layer), or hijackers (admin undelete for recovered accounts).

Effectiveness notes:

- Cheapest layer: data isn't copied, just marked.
- Strongest against user-action and application-bug root causes.
- Weak against infrastructure, hardware, and site-catastrophe causes (if the storage tier is compromised, soft-deleted data is compromised too).
- Bounded retention (15–60 days typical) to respect privacy requirements and cost.

## Layer 2: Backups and their related recovery methods

See [[tiered-backup-strategy]] and [[backups-vs-archives]].

The line of defence after soft deletion. The chapter's most important principle in this layer (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Backups don't matter; what matters is recovery. The factors supporting successful recovery should drive your backup decisions, not the other way around.

A well-designed backup strategy is **tiered** by freshness and restore speed:

- **Tier 1**: frequent local snapshots, hours to days retention, minutes to restore.
- **Tier 2**: distributed filesystem copies, single-digit days retention, hours to restore.
- **Tier 3**: nearline/offline/offsite media (tape), weeks to months retention, days to restore.

Each tier protects against failures the previous tier's storage technology can't handle. Diversity — **media isolation** — is essential: a zero-day in your filesystem driver compromises every copy that lives on that filesystem.

## Layer 3: Regular data validation

See [[data-validation-pipelines]].

Out-of-band validators check invariants that cross datastores: referential integrity between blobs and metadata, alignment between file contents and folder listings, conservation laws across replicated systems. They catch **low-grade corruption before it propagates beyond recovery**.

Effectiveness notes:

- Strongest against creeping application bugs — the class that dominates Google's 19-recovery study.
- Expensive at scale (Gmail devotes a significant portion of compute to its validators).
- Must be **strict enough** to catch real problems, **loose enough** that engineers don't disable them.
- Validators that can **auto-repair** turn emergencies into business-as-usual (Google Drive's 2013 file-listing reconciliation is the canonical example).

## Overarching layer: replication

Replication is useful across layers but is not itself a layer. The chapter is explicit (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> In an ideal world, every storage instance, including the instances containing your backups, would be replicated. During a data recovery effort, the last thing you want is to discover that your backups themselves lost the needed data or that the datacenter containing the most useful backup is under maintenance.

At scale, replicating every storage instance isn't always feasible. The alternatives: **stagger successive backups across different sites** and **write backups using a redundancy code** (RAID, Reed-Solomon erasure codes, GFS-style replication). Chapter 26's discipline for picking a redundancy scheme:

> Don't rely upon an infrequently used scheme whose only "tests" of efficacy are your own infrequent data recovery attempts. Instead, choose a popular scheme that's in common and continual use.

This is [[testing-disaster-recovery|testing-disaster-recovery]]'s principle applied to redundancy: exercised mechanisms work, unexercised ones don't.

## Scale breaks simple strategies

See [[tiered-backup-strategy]] for the full "1T vs 1E" discussion. At terabyte scale you can iterate over every byte and compute checksums. At **exabyte** scale, a single serial task to copy and validate 700 PB of structured data at 300 MB/s would take **eight decades**. The defence-in-depth strategy adapts through two mechanisms:

- **Trust points** — verify data once it's immutable (through passage of time), then take incremental backups of new data only. Reduces 80-year jobs to chains of daily jobs.
- **Horizontal sharding** — run N parallel validation tasks against 1/N of the data. Combined with trust points, brings wall-time back to reasonable levels.

Both adaptations apply across all three layers. Validators shard. Backups are incremental. Restores are parallel.

## Why each layer is non-negotiable

A thought experiment from the chapter (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md): suppose an application uses a BASE datastore for blobs and a Paxos-backed service for metadata, with client-side caches. Without all three layers:

- **No soft deletion**: any user or app-bug deletion is immediately permanent, and only backups can help (slow, with referential-integrity pain).
- **No backups**: any widespread data loss is final.
- **No validators**: inconsistencies between blobs and metadata go unnoticed until they surface months later as user-visible breakage.

The relationships between distinct datastores are where low-grade corruption hides — validators are the only layer that sees across them.

## The nuclear-power origin (Chapter 33)

Chapter 26's defense-in-depth treatment is data-integrity-specific. Chapter 33 names the cross-industry origin (source: chapter-33-lessons-learned-from-other-industries.md):

> In the nuclear power industry, defense in depth is a key element to preparedness. Nuclear reactors feature redundancy on all systems and implement a design methodology that mandates fallback systems behind primary systems in case of failure. The system is designed with multiple layers of protection, including a final physical barrier to radioactive release around the plant itself. Defense in depth is particularly important in the nuclear industry due to the zero tolerance for failures and incidents.

The pattern Chapter 26 applies to data-integrity is directly imported from this nuclear-engineering tradition. Three structural properties carry across:

- **Multiple independent layers**, each effective against different failure modes — soft-deletion / backups / validators in the Chapter 26 stack; redundant reactor systems / containment vessel / physical plant barrier in the nuclear stack
- **Fallback behind primary** — the next layer activates only when the previous one fails. Nothing is single-point-of-failure
- **Final physical barrier** — the last-resort layer that contains the consequence even if all the others fail. In the data-integrity stack, the offsite media (tape) plays this role; in the nuclear stack, the containment building does

The chapter makes clear that defense in depth is justified by **zero tolerance for catastrophic outcome**. Where the consequence cost is lower (Google's typical SLO-bounded products), shallower defenses suffice. The data-integrity layer cake is built deep precisely because data loss at scale falls into the catastrophic-consequence category that makes deep defense the right design — see [[data-integrity-sre|the 24-hour threshold]] for why.

## Related pages

- [[data-integrity-sre]]
- [[data-integrity-failure-modes]]
- [[soft-deletion]]
- [[backups-vs-archives]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[replication]]
- [[testing-disaster-recovery]]
- [[fault-tolerance]]
- [[lessons-from-other-industries]]
- [[preparedness-and-disaster-testing]]
