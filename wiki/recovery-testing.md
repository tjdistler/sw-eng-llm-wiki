# Recovery Testing

**Summary**: Chapter 26's discipline: the only way to know your recovery process works is to run it. Parts of the recovery path quietly break between exercises — bad backups, missing machine resources, vendor processes that changed, permissions drift. **Continuously test the recovery process as part of normal operations, and alert on heartbeat failures**. Anything less is a light-bulb-by-the-switch assumption: you discover the bulb is burned out only when you flip the switch in an actual emergency.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## The light-bulb analogy

Chapter 26's opening framing (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> When does a light bulb break? When flicking the switch fails to turn on the light? Not always — often the bulb had already failed, and you simply notice the failure at the unresponsive flick of the switch. By then, the room is dark and you've stubbed your toe.

Recovery dependencies — backups, machine pools, media handling, vendor processes, access credentials — can be in a latent broken state you aren't aware of until you attempt recovery. The only defence is to exercise them before you need them.

## The prescription

Two disciplines (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

1. **Continuously test the recovery process as part of your normal operations.**
2. **Set up alerts that fire when a recovery process fails to provide a heartbeat indication of its success.**

If recovery tests are manual, staged events, testing becomes unwelcome drudgery that isn't performed deeply or frequently enough to deserve confidence. **Automate the tests and run them continuously.**

## The chapter's single lesson

The one-sentence takeaway from Chapter 26 (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> You only know that you can recover your recent state if you actually do so.

Every other aspect of the chapter depends on this. Soft deletion you can't undelete from is theatre. Backups you can't restore are archives. Validators that detect corruption but can't be acted on are noise. Only a tested, automated, end-to-end recovery pipeline grounds the data-availability guarantee.

## What the test must confirm

Chapter 26's checklist for a recovery test (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Are your **backups valid and complete**, or are they empty?
- Do you have **sufficient machine resources** to run all of the setup, restore, and post-processing tasks?
- Does the recovery process **complete in reasonable wall time** (i.e., within the SLO)?
- Are you able to **monitor the state** of your recovery process as it progresses?
- Are you free of **critical dependencies on resources outside your control** (e.g., offsite media storage vault not available 24/7)?

Each of these items is a plausible failure mode. Each is invisible until the test (or a real recovery) reveals it.

## What Google's testing has discovered

Chapter 26 reports (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Our testing has discovered the aforementioned failures, as well as failures of many other components of a successful data recovery. If we hadn't discovered these failures in regular tests — that is, if we came across the failures only when we needed to recover user data in real emergencies — it's quite possible that some of Google's most successful products today may not have stood the test of time.

The implicit claim: real-failure-during-real-emergency is a dangerous enough outcome that the substantial cost of continuous recovery testing is easily justified.

## Connection to the two case studies

Both Chapter 26 case studies explicitly credit prior testing:

- **[[gmail-gtape-restore|Gmail 2011]]** — "similar situations had been previously simulated many times." The team was able to deliver an estimate of restore time and hit it because they'd rehearsed the process before.
- **A 2012 deletion-pipeline recovery** — the recovery occurred weeks after the company's annual [[testing-disaster-recovery|DiRT]] exercise. The tape-backup team already knew the capabilities and limitations of their subsystems and began dusting off a tool they'd tested during DiRT.

Without those tests, both recoveries would have been significantly worse or impossible. The tests paid back multiple years of investment in a single incident.

## What "continuous" means in practice

Chapter 26's framing allows a spectrum of testing cadences, but insists the extreme — manual, annual — is inadequate. Reasonable interpretations:

- **Per-commit** — every change to the recovery tooling triggers a restore from a canned backup to a test environment.
- **Per-day** — an automated job restores last night's backup to a scratch cluster and validates key invariants.
- **Per-week** — a staged restore of a representative data subset that exercises the full pipeline including offsite recall.
- **Per-year** — the company-wide DiRT exercise rehearses site-level catastrophe scenarios.

The pyramid shape mirrors [[testing-for-reliability|the test pyramid]]: many cheap fast tests at the bottom, fewer expensive realistic tests at the top.

## Scale breaks annual-only testing

If a recovery rehearsal is required once a year, and the rehearsal takes days of engineering effort to set up and execute, it's inevitable that between rehearsals:

- New services will be added without rehearsed restore paths.
- Vendor contracts will change, invalidating rehearsed offsite-recall assumptions.
- Access-control changes will break recovery-time credentials.
- Infrastructure migrations will silently move backups to non-recoverable locations.

Continuous automation is the response. A recovery pipeline that fails daily is a problem that gets fixed this week, not a problem that surprises the team in 13 months.

## Failure categories this exposes

Common things that continuous recovery testing has discovered at Google (inferred from the chapter plus adjacent material):

- **Backup content drift** — backups are being taken but what's inside them has changed schema and can't be restored.
- **Scale drift** — the backup volume has grown past what the restore pipeline can handle in wall time.
- **Vendor process drift** — a tape recall used to take hours; now it takes days because the vendor changed their procedure.
- **Credential drift** — service accounts with restore permissions have been rotated; the restore tool still references the old account.
- **Dependency drift** — a library or infrastructure service the restore tool depends on has been deprecated and isn't available anymore.

None of these are discoverable by inspection of the backup state alone. Only running the full pipeline end-to-end surfaces them.

## Cross-book connections

- [[testing-disaster-recovery]] (SRE Ch 17) — DiRT is Google's annual company-wide exercise; Chapter 26's "continuous" testing is what fills in the other 364 days.
- [[testing-for-reliability]] (SRE Ch 17) — recovery tests are a specific subtype of production-side reliability test; the testing infrastructure serves them the same way.
- [[fault-tolerance]] (Kleppmann Ch 1) — Kleppmann's "backups should be periodically tested by restoring from them" is the same discipline named from a different angle.
- [[statistical-testing-techniques]] (SRE Ch 17) — Chaos Monkey is an adjacent discipline: continuously perturb the live system to exercise recovery mechanisms, rather than running the recovery mechanism itself.
- [[learning-from-outages]] (SRE Ch 13) — Chapter 13's "encourage proactive testing" directive and Chapter 26's recovery-testing discipline are two specific applications of the same principle.
- [[blameless-postmortem]] (SRE Ch 15) — broken recovery tests produce small postmortems that prevent the large one.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[tiered-backup-strategy]]
- [[backups-vs-archives]]
- [[data-integrity-principles]]
- [[testing-disaster-recovery]]
- [[testing-for-reliability]]
- [[statistical-testing-techniques]]
- [[fault-tolerance]]
- [[learning-from-outages]]
- [[gmail-gtape-restore]]
