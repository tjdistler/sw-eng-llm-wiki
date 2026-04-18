# Google Music — Runaway Deletion (March 2012)

**Summary**: Chapter 26's second case study. A refactored privacy-driven data-deletion pipeline at Google Music introduced a race condition that deleted audio references for 21,000 users — approximately 600,000 audio tracks. The loss was discovered only after a user complained about unplayable tracks. Recovery required recalling over 5,000 backup tapes from offsite storage, restoring 1.5 petabytes of data, and took ~7 days end-to-end. The case is the chapter's clearest example of the [[data-integrity-failure-modes|application-bug / creeping-scope / widespread]] failure class that dominates Google's recovery history.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Timeline

**Tuesday, March 6, 2012, mid-afternoon**: A Google Music user reports that previously unproblematic tracks are being skipped (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md).

**March 7**: The investigating engineer discovers the unplayable track's metadata is missing a reference to the actual audio data. Digging deeper, he discovers the reference was **removed by a privacy-protecting data-deletion pipeline**. He immediately escalates to engineering management and SRE.

**March 8, 4:34 PM Pacific**: The recovery team begins. A hasty MapReduce job assesses damage: the refactored deletion pipeline removed **~600,000 audio references** that shouldn't have been, affecting **~21,000 users**. The offending pipeline is disabled to stem the tide.

**March 9, midnight**: All 5,475 restore jobs have been programmatically requested against the tape backup system.

**March 9, 4 AM**: The tape backup system produces a list of 5,337 tapes to be recalled from offsite locations.

**March 9, ~noon**: Truck deliveries of tapes arrive at a datacenter.

**March 10**: 74% of files restored to distributed filesystem; 17 bad tapes plus 1,862 tapes omitted by a vendor still to be handled. Redundancy tapes recalled.

**March 11**: >99.95% of restore complete; redundancy recall in progress.

**March 11–13**: Google Music production paged on an **unrelated** critical failure; recovery effort paused for two days.

**March 13**: All 436,223 tape-restored audio tracks once again made accessible to users — 7 days after incident start, 5 days of actual recovery work.

**Second wave**: Of 600,000 total missing files, **436,223 were found on tape**. The remaining ~**161,000 were eaten by the bug before they were backed up**. Store-bought tracks were re-sourced from the original copies. A small portion were user-uploaded; Google Music servers prompted affected clients to re-upload.

## Scale characteristics

- **1.5 petabytes** of data recovered.
- **5,475 restore jobs** (one per backup).
- **5,337 backup tapes** recalled from offsite locations.
- **17 bad tapes** in the first recall; redundancy coding was the saving grace.
- **1,862 tapes** omitted by a vendor from the first recall; required a second truck delivery.
- **Two days'** extra delay from an unrelated production incident during the recovery.

## The root-cause race condition

The refactored deletion pipeline was designed for scale. To avoid overloading the serving systems, data processing was done in **short-lived secondary copies on separate storage** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). The design assumed strict ordering: stage 2 ran three hours after stage 1, so stage 2 could make a simplifying correctness assumption about its inputs.

As Google Music's data grew:

- Upstream stages took longer.
- The fixed inter-stage delay stopped covering all cases.
- A race condition opened for a small fraction of data.
- As data volume grew, the fraction at risk grew.
- When the pipeline was refactored, the probability jumped sharply, and the race started occurring regularly.

The result: audio references the privacy pipeline should have left alone were removed non-deterministically.

## Why soft deletion didn't save it

Soft deletion covers the case where a user or a normal code path deletes something that can be undeleted. This bug was in the **privacy-driven deletion pipeline** — the part of the system whose explicit purpose is to destroy data after user-driven deletion. The pipeline believed it was correctly deleting user-deleted audio; it was deleting correct audio that shouldn't have been deleted.

> The bug was in the pipeline that honours user privacy requests — the layer that *is* the permanent destruction path.

[[soft-deletion]] protects against accidental deletion by the serving path. It does not protect against a bug in the deletion pipeline itself. That's what [[tiered-backup-strategy|tape backups]] are for, and why they exist.

## Why early detection didn't save it

The first buggy run was February 6, 2012. The loss was noticed **March 6** — a month later, by a user complaint. The chapter's implied lesson: this is exactly the class of failure [[data-validation-pipelines|out-of-band validators]] are designed to catch. A validator that confirmed "every audio metadata reference points to a valid audio file" would have alerted within 24 hours of the first buggy run.

Chapter 26's closing remediation explicitly names this (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> In the wake of the recovery effort, Google Music redesigned its data deletion pipeline to eliminate this type of race condition. In addition, we enhanced production monitoring and alerting systems to detect similar large-scale runaway deletion bugs with the aim of detecting and fixing such issues before users notice any problems.

The post-incident alerting: monitor the **global data-deletion rate aggregated across all users**, and alert when it exceeds some threshold (e.g., 10x the observed 95th percentile). Per-user deletion rates vary too much for useful alerts; global aggregated rate is what spikes when a bug goes runaway.

## Why prior DiRT exercises mattered

The recovery occurred weeks after Google's annual [[testing-disaster-recovery|DiRT]] exercise (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> The tape backup team already knew the capabilities and limitations of their subsystems that had been the subjects of DiRT tests and began dusting off a new tool they'd tested during a DiRT exercise.

Without prior DiRT experience, the team would have had to learn the limits of the tape subsystem during the recovery — much more slowly, and with higher chance of error.

Specific DiRT-influenced decisions during the real incident:

- **Manual tape loading was hundreds of times faster** than the robot-based methods from the vendor. DiRT had already shown this.
- **A programmatic solution** was needed to request 5,475 restores (manually typing would take 3+ days and produce errors). SRE built it fast because SREs are practising software engineers.
- **Redundancy tapes** had been planned for and were recalled when 17 bad tapes showed up in the first batch.

## The second-wave problem

Of the 161,000 tracks never backed up to tape:

- **Most were store-bought and promotional** — Google had the originals elsewhere and re-sourced them quickly.
- **A minority were user-uploaded** — the Google Music client re-uploaded from user devices. This process lasted over a week.

The design implication: the window between "user uploads new content" and "content is backed up to tape" is a permanent exposure. Gmail uses near-real-time streaming backups specifically to minimise this window. Google Music's tape backups covered the time-since-last-backup gap; during that gap, the only other copy was on the user's device.

## What the case demonstrates about Chapter 26's principles

- **[[data-integrity-failure-modes|Application-bug, creeping-rate, widespread scope]]** — the most challenging failure-mode class; exactly the one Chapter 26 names as dominating Google's recovery history.
- **[[defense-in-depth-data|Defence in depth]]** — soft deletion didn't apply (bug was in the deletion path). Early detection hadn't been built. Backups saved what could be saved.
- **[[data-validation-pipelines|Validators]]** — the absence of validators during the buggy month is explicitly called out as the gap; the post-incident fix adds them.
- **[[recovery-testing|Exercise recovery]]** — DiRT-tested capabilities made the recovery tractable.
- **[[data-integrity-principles|Hope is not a strategy]]** — the race condition had been dormant but growing for a long time; it wasn't discovered by monitoring, it was discovered by a user.

## Cross-book connections

- [[idempotence]] / [[effectively-once-processing]] (Kleppmann / Bellemare) — the race condition is a textbook example of the kind of correctness bug that at-least-once-with-idempotent-handlers pipelines are designed to avoid.
- [[stream-processing-fault-tolerance]] (Kleppmann) — modern streaming frameworks (Flink, Kafka Streams) that operate on immutable events with exact offsets would have made this class of bug structurally harder to introduce.
- [[event-sourcing]] (Kleppmann) — append-only logs with no in-place mutation would have made recovery to a pre-bug state trivially easy.
- [[distributed-filesystems]] — the chapter notes that the 1.5 PB was restored to distributed filesystem storage from tape; the downstream steps made files accessible through the standard serving path.
- [[incident-management-framework]] (SRE Ch 14) — the "2 groups" split (root-cause team + recovery team) is a textbook vertical separation of responsibilities from the Ch 14 framework.
- [[blameless-postmortem]] (SRE Ch 15) — the public Google disclosure and the detailed post-incident alerting additions are the outputs of a healthy postmortem.

## Related pages

- [[data-integrity-sre]]
- [[data-integrity-failure-modes]]
- [[defense-in-depth-data]]
- [[soft-deletion]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[data-integrity-principles]]
- [[gmail-gtape-restore]]
- [[testing-disaster-recovery]]
- [[incident-management-framework]]
- [[learning-from-outages]]
