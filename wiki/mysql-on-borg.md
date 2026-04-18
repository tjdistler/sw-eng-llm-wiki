# MySQL on Borg

**Summary**: Chapter 7's "automate yourself out of a job" case study. The Ads SRE team migrated their MySQL instances onto [[borg|Borg]] to gain bin-packing efficiency and automatic restart, but Borg's assumption that tasks move every week or two was incompatible with the 30-90-minute manual failover process. Building an automated failover daemon called **Decider** — which completed failovers in under 30 seconds, 95% of the time — unlocked the migration, dropped operational work by 95%, and freed 60% of the hardware.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`

**Last updated**: 2026-04-17

---

## The starting position

From 2005 to 2008 the Ads MySQL database ran in "a mature and managed state" (source: chapter-07-the-evolution-of-automation-at-google.md). Routine replica replacements had already been automated; the team believed the low-hanging fruit had been picked. The team then looked at the next level of improvement: moving MySQL onto Google's cluster scheduling system, [[borg|Borg]].

Two benefits motivated the move:

- **Eliminate machine/replica maintenance** — Borg would handle setup and restart of new and broken tasks automatically.
- **Bin-pack MySQL instances on the same physical machine** — Borg's container-based resource sharing would improve hardware utilisation.

A proof-of-concept MySQL-on-Borg deployment succeeded in late 2008. That's when the real problem surfaced.

## The Borg-vs-master-failover conflict

Borg moves tasks around the cluster frequently — "as frequently as once or twice per week" — because machines reboot for kernel upgrades, fail, or get drained for other reasons (source: chapter-07-the-evolution-of-automation-at-google.md). For database *replicas* this rate was tolerable. For *masters* it was not.

The arithmetic:

- Manual master failover took 30–90 minutes per instance.
- Reboots for kernel upgrades plus normal machine failure implied multiple otherwise-unrelated failovers per week.
- Across the shard count the team ran, manual failovers would consume a substantial amount of human hours **and** yield a best-case 99% uptime — below the business requirement.
- To stay within the [[error-budget]], each failover had to cost less than 30 seconds of downtime. No human-dependent procedure could hit that target.

The team had no choice: automate failover.

## Decider

In 2009 the team shipped **Decider**, an automated failover daemon that could complete planned and unplanned MySQL failovers in under 30 seconds 95% of the time (source: chapter-07-the-evolution-of-automation-at-google.md). With Decider, MySQL on Borg ("MoB") became viable.

The philosophical shift named in the chapter:

> We graduated from optimizing our infrastructure for a lack of failover to embracing the idea that failure is inevitable, and therefore optimizing to recover quickly through automation.

This is the [[mttr-and-mttf|MTTR-first]] stance made concrete: instead of trying to prevent failover events, reduce the cost of each one until frequency stops mattering.

## The cost of embracing failure

Decider made failover cheap but not free. The price was paid in the application layer (source: chapter-07-the-evolution-of-automation-at-google.md):

- Every application that used Ads MySQL had to grow **significantly more failure-handling logic** than before.
- The standard MySQL-world assumption — that the database is the most stable component in the stack — had to be inverted.
- The team customised client software like JDBC to be more tolerant of a failure-prone environment.

This is a general pattern in autonomous-system design: pushing the reliability property into the system relocates complexity rather than eliminating it. The question is whether the relocation is net-positive. For MoB it was, overwhelmingly.

## The payoff

The quantitative outcomes cited in the chapter (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Operational time dropped by 95%.** A single-database-task outage no longer paged a human.
- **Schema changes were subsequently automated**, pushing total operational maintenance down by about 95% overall.
- **60% of hardware was freed** through bin-packing multiple MySQL instances onto shared machines.
- The team was "flush with hardware and engineering resources" — the freed capacity was available to fund further automation work.

The cascade effect is the point: the more toil the team eliminated, the more engineering time they had, the more automation they could build, the more toil came off, and so on. See [[toil-and-engineering-balance]] for the organisational mechanism that this case study exemplifies.

## The takeaway

Chapter 7's one-line summary of the case study: *go the extra mile to deliver a platform rather than replacing existing manual procedures*. Decider isn't a script that automates a failover; it's a component of a platform (MoB) that has been restructured so failover is a routine, low-cost operation. Level 4 of the [[hierarchy-of-automation-classes|automation hierarchy]] moving toward level 5.

## Cross-book connections

- [[borg]] — the platform MoB runs on; Decider is an SRE-authored companion that bridges Borg's task-movement assumption with MySQL's master-is-stable assumption.
- [[container-management-system]] (Bellemare) — Kubernetes is the open-source descendant of Borg; stateful-database-on-container-orchestrator patterns today (StatefulSets, operators for MySQL/Postgres) are the Kubernetes-era equivalents of MoB.
- [[operator-pattern]] (Burns) — Decider is morally equivalent to a Kubernetes operator for MySQL: application-specific reconciliation inside the scheduler's world model.
- [[failover]] (Kleppmann) — the chapter's failover-must-finish-in-30-seconds requirement is a concrete instance of Kleppmann's "many ways failover goes wrong" problem, solved by compressing the window rather than removing it.
- [[error-budget]] — Decider's 30-second target was derived from the error budget for the service.

## Related pages

- [[automation-at-google]]
- [[borg]]
- [[autonomous-systems]]
- [[hierarchy-of-automation-classes]]
- [[toil-and-engineering-balance]]
- [[mttr-and-mttf]]
- [[failover]]
- [[error-budget]]
