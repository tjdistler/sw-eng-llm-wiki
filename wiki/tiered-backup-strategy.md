# Tiered Backup Strategy

**Summary**: Chapter 26's answer to "what does a backup architecture look like at Google scale?" A **multi-tier strategy** combines fast expensive local snapshots (hours retention, minutes to restore) with progressively cheaper slower tiers (distributed filesystems, then nearline storage, then offsite tape). Each tier protects against failures the previous tier's storage technology can't handle. No single tier — or single backup mechanism — covers the 24 failure modes; the composition does.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Why a single tier isn't enough

Chapter 26's framing. A backup tier is defined by:

- **How fresh** the data is (backup frequency).
- **How fast** you can restore it.
- **How diverse** its storage technology is from the live data's.
- **How long** you retain it.

A single tier optimises one or two of these at the expense of the others. Local snapshots are fresh and fast but share a failure domain with live data. Offsite tape is diverse and durable but slow and old. To cover the full space — from "user deleted their mailbox five minutes ago" to "a regional datacenter caught fire" — you layer tiers that each trade differently.

## The three canonical tiers

Chapter 26's architecture (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

### Tier 1: Local snapshots

- **Retention**: hours to single-digit days.
- **Restore latency**: minutes.
- **Frequency**: very frequent (many per day).
- **Storage**: same storage instance as live data (e.g., SQL snapshot, copy-on-write).
- **Protects against**: majority of software-bug and developer-error scenarios.
- **Cost**: expensive — contends with live datastore storage; the faster your data mutates, the less copy-on-write efficiency helps.

### Tier 2: Distributed filesystem copies

- **Retention**: single-digit to low double-digit days.
- **Restore latency**: hours.
- **Frequency**: daily or every few days.
- **Storage**: different distributed filesystem, same site.
- **Protects against**: failures of the Tier 1 storage technology; bugs detected too late for Tier 1; infrastructure-layer issues local to the storage stack.
- **Retention rule of thumb**: if new code ships twice a week, retain at least a week or two.

### Tier 3: Nearline / offline / offsite

- **Retention**: weeks to months.
- **Restore latency**: hours to days.
- **Frequency**: weekly or monthly.
- **Storage**: dedicated tape libraries or offsite disk.
- **Protects against**: site-level issues (datacenter power failure, distributed filesystem corruption due to a bug).
- **Cost**: cheap per byte, but moving data to and from these tiers is expensive in wall time.

## The key ratios

Chapter 26's observations on the forces in tension (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> The further down the stack you push a snapshot of your data, the longer it takes to make a copy, which means that the frequency of copies decreases. At the database level, a transaction may take on the order of seconds to replicate. Exporting a database snapshot to the filesystem underneath may take 40 minutes. A full backup of the underlying filesystem may take hours.

So the *data freshness* you can achieve for a given tier is fundamentally limited by the tier's copy cost. And **restore time** is typically comparable to backup time — if a backup takes hours, the restore takes hours too.

## Point-in-time recovery

See also [[data-integrity-failure-modes]]. The hardest scenario is recovering **different subsets of data to different times** — the creeping-application-bug case. Chapter 26's assessment (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> A backup and recovery solution that provides point-in-time recovery for an application across its ACID and BASE datastores while meeting strict uptime, latency, scalability, velocity, and cost goals is a chimera today!

The pragmatic guidance: *adopt a tiered strategy*, and if point-in-time recovery is available in your cloud APIs use it. **Don't skip both.** Each (or both together) will be valuable at some point.

## How far back to reach

The backup strategy's reach determines which scenarios are recoverable. Longer reach = more scenarios covered but higher cost. Chapter 26's empirical rule (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Low-grade data mutation or deletion bugs are sometimes noticed *months* after the first data loss began.
- So the ideal reach is as far back as possible.
- But high-velocity environments change code and schema faster than old backups stay compatible; reaching back 12 months means also maintaining 12 months of schema-migration fidelity.
- Google's pragmatic line: **30 to 90 days** for many services, with position in the window determined by tolerance for data loss vs investment in early detection.

The more investment in [[data-validation-pipelines|early detection]], the less reach the backup strategy needs to provide.

## Retention for creeping losses

A separate retention concern: the chapter notes that reaching back far enough to recover a slow data loss means the **restored data has to be merged with current state** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). This is operationally complex — a recovery effort against a 60-day-old backup must reconcile every subsequent change the restored data would have participated in. Early detection is the asymmetric-cost lever that keeps recovery from needing this.

## Scaling: 1T vs 1E

Chapter 26's scale-breaks-simple-strategies section (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Validating, copying, and performing round-trip tests on a few gigabytes of structured data is an interesting problem... Now let's up the ante: instead of a few gigabytes, let's try securing and validating 700 petabytes of structured data. Assuming ideal SATA 2.0 performance of 300 MB/s, a single task that iterates over all of your data and performs even the most basic of validation checks will take 8 decades.

Two design responses make exabyte-scale backup and validation practical:

### Trust points (incremental from known-good)

Once a portion of data is **rendered immutable** (by policy or by passage of time), verify its state once, then make suitable copies for recovery. Subsequent backups only include modified or added data. This aligns backup wall-time with mainline processing time.

But incremental chains have their own cost: a three-year-old full backup followed by ~1,000 daily incrementals requires serially processing the entire chain to restore, and each incremental introduces an independent risk of failure.

### Horizontal sharding

Split the data into independent shards and run N parallel backup/restore tasks. Reduces wall time by N. Requirements:

- Balance data evenly across shards.
- Ensure shard independence (no cross-shard dependencies during backup/restore).
- Avoid contention among concurrent sibling tasks.

Combined with trust points, horizontal sharding brings 80-year jobs down to hours.

## Media isolation

The backup strategy must span **diverse** storage technologies at the tier boundaries. A bug or attack in a disk device driver is unlikely to affect tape drives; the media diversity is what makes a lower tier protective against a failure mode the upper tier shares with live data. Chapter 26's whimsical version: *If we could, we'd make backup copies of our valuable data on clay tablets.*

## Tier composition example

The chapter's summary (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Addressing a broad range of scenarios at reasonable cost demands a tiered backup strategy. The first tier comprises many frequent and quickly restored backups stored closest to the live datastores... Due to relative expense, backups are retained in this tier for anywhere from hours to single-digit days, and may take minutes to restore. The second tier comprises fewer backups retained for single-digit or low double-digit days on random access distributed filesystems local to the site... Subsequent tiers take advantage of nearline storage such as dedicated tape libraries and offsite storage.

The two Chapter 26 case studies exercise different tiers:

- **[[gmail-gtape-restore|Gmail 2011]]** — primary failure of Gmail's internal redundancy triggered a restore from GTape, the offsite tape system (tier 3).
- **[[google-music-runaway-deletion|Google Music 2012]]** — 5,475 tape restores of 1.5 PB from offsite locations, also tier 3.

The live-site tiers handle day-to-day recovery invisibly; the rare tier-3 use is the payoff for the investment.

## Backups must themselves be reliable

The overarching concern: *the instances containing your backups would themselves be replicated* (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). When that's infeasible, stagger backups across different sites and write them with **redundancy codes** — RAID, Reed-Solomon erasure codes, GFS-style replication. Google Music 2012 specifically relied on redundant encoding: when 17 tapes turned out to be bad, redundancy tapes were recalled to cover the gap.

The discipline: choose a popular, continuously-exercised redundancy scheme, not a bespoke one your team tests only during disasters.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[backups-vs-archives]]
- [[recovery-testing]]
- [[data-integrity-failure-modes]]
- [[data-validation-pipelines]]
- [[replication]]
- [[distributed-filesystems]]
- [[gmail-gtape-restore]]
- [[google-music-runaway-deletion]]
