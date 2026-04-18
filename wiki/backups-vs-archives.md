# Backups vs Archives

**Summary**: Chapter 26's framing: archives safekeep data for compliance and discovery over long time windows; backups exist to restore service after data loss. **The most important difference is that backups can be loaded back into an application, while archives cannot**. Confusing the two is the most common cause of the classic failure mode: "we have backups" turns out to mean "we have archives that can't restore service within the uptime window."

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## The chapter's maxim

> No one really wants to make backups; what people really want are restores. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

The chapter's reframing: focus on the restore, not on the backup. Backups are a tax paid for the service of guaranteed data availability; the product being purchased is the ability to restore.

## The distinction

| Dimension | Archive | Backup |
|---|---|---|
| Primary purpose | Long-term retention for auditing, discovery, compliance | Restore service after data loss |
| Recovery-time expectation | Days to weeks | Within the uptime SLO of the service (minutes to hours) |
| Typical retention | Years (7 years for financial records is common) | Weeks to months |
| Copy frequency | Monthly or quarterly | Daily, hourly, or continuous |
| Loadability into the application | Not required | **Required** |

The key operational question (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Is your "backup" really an archive, rather than appropriate for use in disaster recovery?

If the loadability and recovery-time properties don't hold, what you have is an archive, no matter what it's called.

## What archives are for

Long-term retention for (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- **Auditing** — financial records, access logs.
- **Legal discovery** — email retained for litigation purposes.
- **Compliance** — regulatory requirements (HIPAA, SOX, GDPR retention clauses).

Archives tolerate slow recovery because the business process consuming them runs on a days-or-weeks cadence. A month-long audit that takes a week to assemble is fine.

## What backups are for

Restoration of live service when data is lost. Two operational constraints (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

1. **Recovery must complete within the service's uptime SLO** — otherwise users are without useful access for the entire gap between the incident and the end of the restore.
2. **Backups must be recent** — any data written after the last backup is at risk. For Gmail, Google ran a near-real-time streaming backup strategy to shrink this window.

The trade-off behind backup frequency: the more often you back up, the less data is at risk; but full backups are expensive and impose compute load on live datastores. The typical compromise is **full during off-peak + incrementals during busy hours + streaming/continuous for critical data**.

## Why people get this wrong

The classic pattern: a team ticks the "backups" box by scheduling a monthly dump to cheap long-term storage. The storage is technically adequate; what's missing is the ability to actually restore. At incident time:

- The backup format doesn't match the production schema version.
- The restore path runs at a rate that would take weeks for the current data volume.
- No one has ever run the full restore pipeline, so half of it is broken.
- The storage medium requires human intervention (offsite recall, physical tape handling) that isn't rehearsed.

The team has archives, not backups. The chapter's prescription is to design backward from the recovery requirement.

## Key design questions

Chapter 26's framing of backup strategy (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> The scenarios in which you want your backups to help you recover should dictate the following:
> - Which backup and recovery methods to use
> - How frequently you establish restore points by taking full or incremental backups of your data
> - Where you store backups
> - How long you retain backups

These four questions collapse into two practical operational questions:

- **How much recent data can you afford to lose?** → Backup frequency (and whether you need streaming).
- **How quickly do you need to recover?** → Storage tier proximity (local snapshot vs remote tape).

See [[tiered-backup-strategy]] for how Google layers multiple backup tiers to answer both questions simultaneously for different failure classes.

## Backups must also be tested

A backup that can't be restored is an archive in disguise. The only way to know a backup is a backup is to restore from it, repeatedly. See [[recovery-testing]] — the continuous, automated, end-to-end test of the restore pipeline is the discipline that keeps archives from silently replacing backups.

## Cross-book framing

- [[testing-disaster-recovery]] (SRE Ch 17) — the offline-checkpoint / online-repair testing distinction applies specifically to the recovery tools that back up and restore.
- [[fault-tolerance]] (Kleppmann Ch 1) — Kleppmann's "backups should be periodically tested by restoring from them" is Ch 26's same argument from the auditing-for-data-integrity angle.
- [[timeliness-and-integrity]] (Kleppmann Ch 12) — an archive can preserve integrity (bytes survive) without supporting timeliness (current service restoration); Ch 26 makes explicit that this is insufficient.

## Related pages

- [[data-integrity-sre]]
- [[tiered-backup-strategy]]
- [[recovery-testing]]
- [[defense-in-depth-data]]
- [[testing-disaster-recovery]]
- [[fault-tolerance]]
- [[timeliness-and-integrity]]
