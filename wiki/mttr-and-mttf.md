# MTTR and MTTF

**Summary**: Reliability is a function of **mean time to failure** (how often the system breaks) and **mean time to repair** (how long it takes to recover when it does). SRE's emergency-response tenet focuses on MTTR: a system that recovers without human intervention has higher availability than one of equal MTTF that requires hands-on repair.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## The basic relationship

Reliability is a function of **mean time to failure (MTTF)** and **mean time to repair (MTTR)** (source: chapter-01-introduction.md, citing Schroeder 2015). Availability over a period is roughly `MTTF / (MTTF + MTTR)`: long time between failures and short repair time produce high availability; either going the wrong way reduces availability.

## Humans add latency

The SRE framing of the trade-off (source: chapter-01-introduction.md):

> Even if a given system experiences more actual failures, a system that can avoid emergencies that require human intervention will have higher availability than a system that requires hands-on intervention.

In other words: *lower MTTR beats higher MTTF when the MTTR win comes from taking humans out of the loop*. Automated recovery that triggers on the first symptom can bring MTTR down by orders of magnitude compared to paging a human, waiting for them to log in, run diagnostics, and type commands.

This is the justification for investing heavily in automation around recovery — not just detection — and for building systems that fail over, reroute, or restart themselves.

## When humans are necessary

Not every incident can be handled by automation. When humans are necessary, SRE has a concrete finding (source: chapter-01-introduction.md):

> Thinking through and recording the best practices ahead of time in a "playbook" produces **roughly a 3x improvement in MTTR** as compared to the strategy of "winging it".

The hero jack-of-all-trades on-call engineer does work, but the practised on-call engineer armed with a playbook works much better. See [[on-call-playbook]].

## Automation as an MTTR lever (Chapter 7)

Chapter 7 lists **faster repairs** as one of the five values of automation (source: chapter-07-the-evolution-of-automation-at-google.md). An automated system that runs regularly and successfully enough reduces MTTR for common faults: the engineers no longer spend time preventing or cleaning up after the problem, and velocity improves because those cycles free up for other work. The chapter adds a product-lifecycle argument: the later a problem is discovered, the more expensive it is to fix — production problems are the most expensive — so automation that surfaces issues as they arise lowers total cost of the system at scale.

MySQL-on-Borg (Decider) is the concrete MTTR-reduction story. Manual master failover was 30–90 minutes; the business required under 30 seconds per failover to hit the [[error-budget]]; no human-dependent procedure could close that gap. The Ads team built Decider, which completed failovers in under 30 seconds 95% of the time. The philosophical shift captured in the chapter:

> We graduated from optimizing our infrastructure for a lack of failover to embracing the idea that failure is inevitable, and therefore optimizing to recover quickly through automation.

This is the MTTR-over-MTTF stance at full commitment. Failure frequency stopped being the target metric once the cost of each failure fell far enough. The same inversion drives [[autonomous-systems|autonomous-system]] design more generally: once MTTR is low enough, more frequent failures become tolerable, which buys design flexibility everywhere else.

## Testing as a zero-MTTR lever (Chapter 17)

Chapter 17 adds the most potent MTTR lever of all: **zero-MTTR testing**. A system-level test applied to a subsystem that detects the exact problem monitoring would detect produces an MTTR of zero — the push is blocked, the user never sees the bug (source: chapter-17-testing-for-reliability.md). See [[zero-mttr-testing]] for the full treatment.

The framing inverts the MTTR/MTBF trade-off. If testing catches a growing share of bugs at zero MTTR, user-experienced MTBF rises, and the team can ship faster:

> The more bugs you can find with zero MTTR, the higher the Mean Time Between Failures (MTBF) experienced by your users. As MTBF increases in response to better testing, developers are encouraged to release features faster. (source: chapter-17-testing-for-reliability.md)

Chapter 17 also uses the MTTR lens to classify configuration files. A config file that exists to keep MTTR low, and is edited only during failures, should have a release cadence slower than MTBF. A config file that changes more than once per application release holds release state, and needs testing-and-monitoring coverage at least as strong as the user application — or it will dominate site reliability negatively (source: chapter-17-testing-for-reliability.md).

## Data-integrity recovery as the MTTR frontier (Chapter 26)

Chapter 26 applies the same MTTR logic to **data loss** events specifically (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). A data-integrity failure has the same two-metric structure as any other reliability event: MTTF (how often data is lost) and MTTR (how long until users see correct, accessible data again). The chapter's thought experiment:

> Suppose an artifact were corrupted or lost exactly once a year. If the loss were unrecoverable, uptime of the affected artifact is lost for that year... in an alternate universe, suppose the corruption were immediately detected before users were affected and that the artifact was removed, fixed, and returned to service within half an hour. Ignoring any other downtime during that 30 minutes, such an object would be 99.99% available that year.

So the MTTR lever for data integrity is what reduces user-visible downtime from a year to half an hour. The three levers Ch 26 prescribes map to the MTTR frame:

- **[[soft-deletion]]** shrinks MTTR to near-zero for user-triggered deletions (admin undelete, trash recovery).
- **[[tiered-backup-strategy|Tiered backups]]** bound MTTR per failure class — local snapshots restore in minutes, offsite tape in hours.
- **[[data-validation-pipelines|Validators]]** shrink MTTF-detection-to-MTTR-start (the time the corruption lives in the system before the restore is initiated) by detecting creeping corruption within 24 hours rather than months.

Chapter 26's closing aspiration is a pure MTTR-to-zero argument (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> As you get better at recovering from any breakage in reasonable time N, find ways to whittle down that time through more rapid and finer-grained loss detection, with the goal of approaching N = 0. You can then switch from planning recovery to planning prevention.

Same shift as Ch 7 and Ch 17: drive MTTR low enough that failures become routine, then invest the freed attention in prevention. [[recovery-testing|Continuously-tested recovery]] is the data-integrity counterpart to the [[autonomous-systems|automation-based MTTR lever]].

## Cross-book connection

Kleppmann's [[reliability]] page covers MTTF mechanics on the fault-vs-failure side — a 10,000-disk cluster expects roughly one disk failure per day. SRE layers the organisational counterpart on top: *given that faults will happen, design the emergency-response pipeline to minimise MTTR*.

## Related pages

- [[emergency-response]]
- [[on-call-playbook]]
- [[sre-tenets]]
- [[reliability]]
- [[fault-tolerance]]
- [[automation-at-google]]
- [[autonomous-systems]]
- [[testing-for-reliability]]
- [[zero-mttr-testing]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[recovery-testing]]
