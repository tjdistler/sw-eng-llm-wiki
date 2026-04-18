# Data Availability vs Data Integrity

**Summary**: Chapter 26's foundational distinction: **data integrity is the means, data availability is the goal**. A service can preserve every byte and still fail its users if those bytes can't be reached when wanted. Google SRE treats data integrity as the set of mechanisms (checksums, replication, backups, validators) and data availability as the measurable outcome (users can read what they wrote, on demand, within the service's time window).

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Why the distinction matters

Chapter 26 opens with the observation that users can't tell the difference between **data loss**, **data corruption**, and **extended unavailability** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). From the user's point of view, all three are *"my data is gone."* The technical distinction — "we still have the bytes, just not reachable right now" — does not restore trust.

The chapter's canonical example is a real competing email provider's 10-day outage (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Days 1–10: users told data is unrecoverable. Many establish new identities elsewhere.
- Day 10+: provider announces the data is fine after all — it was "only an outage."

The lesson: **from the user's point of view, data integrity without expected and regular data availability is effectively the same as having no data at all**.

## The revised definition

The chapter's revised operational definition (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Data integrity means that services in the cloud remain accessible to users. User access to data is especially important, so this access should remain in perfect shape.

Access is a first-class component of the integrity guarantee — not a separate uptime concern.

## How the goal reframes the metric

Consider a corruption event that happens exactly once a year. Two handlings (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- **Undetected, unrecoverable** — the year's uptime for that artifact is zero from the corruption onward. Data integrity scored by byte count is high, but users can't tell the difference from total loss.
- **Detected immediately, removed, repaired, returned in 30 minutes** — users see 99.99% availability that year on the affected artifact, and **data integrity is effectively 100% during the accessible lifetime of the object**.

The second universe is the one Google engineers toward. The metric is not "how many bytes survived" but "how much of the time did users see correct data when they asked for it."

## Framing Google's investment

The reframing drives every other prescription in the chapter:

- **Prioritise restores, not backups.** See [[backups-vs-archives]]. The measurable deliverable is the restore, because only the restore produces availability.
- **Team SLOs are stated as data availability targets in the face of various failure modes**, not as backup-completion metrics. The [[service-level-objective|SLO]] is what users experience; the backup machinery is how the team meets it.
- **Proactive detection beats passive protection.** The faster you detect corruption, the shorter the unavailability window, the higher the observed integrity.
- **[[recovery-testing|Continuously exercise the recovery path]].** Recovery is the load-bearing mechanism for availability; if it silently breaks between exercises, the integrity guarantee has already failed.

## Connection to Kleppmann's framing

[[timeliness-and-integrity|Kleppmann's timeliness/integrity distinction]] splits "consistency" differently — timeliness as self-healing ("wait and retry") vs integrity as permanent ("explicit repair needed"). Chapter 26 operates one level up: even perfect Kleppmann-style integrity (no corruption, no contradiction) is insufficient if users can't *access* the preserved bytes. The SRE framing adds **availability of the integrity-preserved data** as an explicit goal.

The two framings are compatible:

- Kleppmann: "integrity violations are perpetual inconsistency"
- SRE Ch 26: "data integrity without data availability is effectively the same as no data"

Both agree that integrity is not optional. SRE adds that integrity-plus-unavailability is no better than no integrity at all, in the user's experience.

## Related pages

- [[data-integrity-sre]]
- [[backups-vs-archives]]
- [[recovery-testing]]
- [[service-level-objective]]
- [[mttr-and-mttf]]
- [[timeliness-and-integrity]]
- [[reliability]]
