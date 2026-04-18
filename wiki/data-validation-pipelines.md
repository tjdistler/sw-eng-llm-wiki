# Data Validation Pipelines

**Summary**: Chapter 26's third layer of [[defense-in-depth-data|defence in depth]]: out-of-band checks and balances that continuously validate data-invariant properties **both within and between an application's datastores**. Validators catch low-grade corruption and deletion before they propagate beyond recovery — the class of failure the first two layers can't reliably address. Typically implemented as MapReduce or Hadoop pipelines run daily (or more often) at meaningful scale.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## The propagation problem

Chapter 26's opening observation (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> "Bad" data doesn't sit idly by, it propagates. References to missing or corrupt data are copied, links fan out, and with every update the overall quality of your datastore goes down. Subsequent dependent transactions and potential data format changes make restoring from a given backup more difficult as the clock ticks.

The earlier you detect corruption, the easier and more complete the recovery. Validators are the mechanism that makes "earlier" possible — they find problems the moment they manifest rather than after they've been amplified by downstream consumers.

## Why distributed-consistency APIs aren't enough

Novice cloud developers sometimes assume that choosing a distributed-consistent storage API (Megastore, Spanner) delegates data integrity to the consensus algorithm underneath. Chapter 26's rebuttal (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> While such algorithms are infallible in theory, their implementations are often riddled with hacks, optimizations, bugs, and educated guesses.

Paxos ignores failed nodes in theory; in practice it uses timeouts, retries, and failure-handling heuristics that produce edge cases at scale. Eventually consistent systems (Bigtable) have weaker theoretical guarantees and more of the same practical issues. The larger the application, the more frequently these issues affect it.

> Trust storage systems, but verify!

This is the data-integrity form of [[data-integrity-principles|"trust but verify"]]. Validators are the verification step.

## What validators check

The kinds of invariants Chapter 26 names:

- **Referential integrity between datastores** — e.g., Google Drive periodically validates that file contents align with listings in Drive folders. Misalignment means some files would appear missing.
- **Aging code invariants** — contracts that ought to still hold after old code paths have been replaced.
- **Post-migration reconciliation** — schemas evolve, data migrates; validators confirm nothing was left behind.
- **Cross-service integration points** — dependencies between microservices that might drift out of sync.

The discipline (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Only validate invariants that cause devastation to users.

Over-strict validation fails on simple innocuous changes, engineers abandon it, and the protection evaporates. Too-loose validation misses user-affecting corruption. The right balance is user-impact-oriented invariants — the ones whose violation would produce a disaster.

## Auto-repair turns emergencies into routine

The strongest pattern in the chapter is **validators that also repair**. The canonical example (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Google Drive periodically validates that file contents align with listings in Drive folders. If these two elements don't align, some files would be missing data — a disastrous outcome. Drive infrastructure developers were so invested in data integrity that they also enhanced their validators to automatically fix such inconsistencies. This safeguard turned a potential emergency "all-hands-on-deck-omigosh-files-are-disappearing!" data loss situation in 2013 into a business as usual, "let's go home and fix the root cause on Monday," situation.

By transforming emergencies into routine, validators improve engineering morale, quality of life, and predictability. This is the pattern Chapter 26 holds up as the gold standard.

## The engineering-velocity argument

Shunting developers to work on a validation pipeline slows engineering velocity in the short term (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> However, devoting engineering resources to data validation endows other developers with the courage to move faster in the long run, because the engineers know that data corruption bugs are less likely to sneak into production unnoticed.

Gmail developers run validators and derive comfort from the knowledge that inconsistencies are detected within 24 hours. This has enabled them to introduce code changes to Gmail's production storage implementation more than once a week — a velocity their validator-free state would not have sustained.

The argument parallels unit tests: up-front investment in correctness checks accelerates long-term development by making regression-free change routine.

## Cost and performance at scale

Chapter 26 is candid about the cost (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Out-of-band validators can be expensive at scale. A significant portion of Gmail's compute resource footprint supports a collection of daily validators.

Validators also reduce server-side cache hit rates by touching data the users aren't touching, indirectly degrading user-facing responsiveness. Mitigations at Gmail:

- **Knobs for rate-limiting** the validators.
- **Periodic refactoring** — one round cut disk-spindle contention by 60% without reducing invariant coverage.
- **Sharded workloads** — the largest Gmail validator is divided into 10–14 shards, one shard validated per day, because running everything daily would be too expensive.

Google Compute Storage hit a scaling wall where even out-of-band validators couldn't finish within 24 hours; the team had to devise a more efficient metadata verification approach than brute force alone.

## Tiered validation

Just as [[tiered-backup-strategy|backups are tiered]], validation is tiered at scale:

> As a service scales, sacrifice rigor in daily validators. Make sure that daily validators continue to catch the most disastrous scenarios within 24 hours, but continue with more rigorous validation at reduced frequency to contain costs and latency.

Daily validators are the fast broad coverage. Deeper invariants run weekly or monthly. Mirrors the multi-tier backup structure's cost-vs-thoroughness trade-off.

## Running a validator in production

Chapter 26's catalogue of what an effective out-of-band data validation system needs (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Validation **job management** (scheduling, retries, resource allocation).
- **Monitoring, alerts, dashboards** so failures are visible.
- **Rate-limiting features** to bound impact on live systems.
- **Troubleshooting tools** including BigQuery-style investigation tools, dashboards, playbooks.
- **Production playbooks** for on-call engineers.
- **Data validation APIs** that make validators easy to add and refactor.

Small engineering teams at high velocity can't afford to design, build, and maintain all of this alone. The organisational recommendation:

> Structure your engineering teams such that a central infrastructure team provides a data validation framework for multiple product engineering teams. The central infrastructure team maintains the out-of-band data validation framework, while the product engineering teams maintain the custom business logic at the heart of the validator to keep pace with their evolving products.

This is the same separation that makes [[data-validation-pipelines|validators]] economically viable as a third layer alongside backups and soft deletion: the framework is general, the invariants are product-specific, and the two responsibilities live with the teams that have the right context.

## Troubleshooting failed validations

Failed validations often have transient causes that vanish within hours. The ability to rapidly drill down into validation audit logs is essential. Gmail's on-call engineers have:

- A suite of playbook entries for validation-failure alerts.
- A BigQuery-like investigation tool.
- A data validation dashboard.

The playbook discipline here is the same as [[on-call-playbook]]: validated, documented, available in real time.

## Cross-book framing

- [[fault-tolerance]] (Kleppmann Ch 12) — Kleppmann's "self-auditing systems" section (HDFS read-back, S3 replica comparison, testing backups by restoring) is the exact pattern Ch 26 names as the third layer. Merkle trees and certificate transparency are possible future directions.
- [[end-to-end-argument]] (Kleppmann Ch 12) — validators are end-to-end integrity checks: they don't trust the storage layer's internal guarantees, they verify the properties users actually care about.
- [[timeliness-and-integrity]] (Kleppmann Ch 12) — integrity violations are "perpetual inconsistency" that won't self-heal; validators are how you discover them before the gap between actual and expected state grows unrecoverable.
- [[testing-for-reliability]] (SRE Ch 17) — validators are a form of production testing specifically scoped to data invariants.
- [[architecture-fitness-function]] (Richards & Ford) — a validator is a fitness function for a data-integrity characteristic: objective, automatable, continuously evaluated.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[soft-deletion]]
- [[tiered-backup-strategy]]
- [[data-integrity-principles]]
- [[data-integrity-failure-modes]]
- [[fault-tolerance]]
- [[timeliness-and-integrity]]
- [[end-to-end-argument]]
- [[testing-for-reliability]]
- [[on-call-playbook]]
