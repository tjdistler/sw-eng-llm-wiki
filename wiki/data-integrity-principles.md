# Data Integrity Principles (SRE)

**Summary**: Chapter 26's closing synthesis. Five general SRE principles specialised to the data-integrity domain: **beginner's mind** (never assume you understand the system), **trust but verify** (APIs have bugs; validate critical data out of band), **hope is not a strategy** (unexercised mechanisms fail when needed most), **defense in depth** (multiple tiers that individually fall short but collectively succeed), and **revisit and reexamine** (yesterday's safety doesn't guarantee tomorrow's).

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Beginner's mind

> Large-scale, complex services have inherent bugs that can't be fully grokked. Never think you understand enough of a complex system to say it won't fail in a certain way. Trust but verify, and apply defense in depth. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

The parenthetical in the chapter: *"Beginner's mind" does not suggest putting a new hire in charge of that data deletion pipeline*. The point is epistemic humility, not organisational inexperience. The most devastating Google data-deletion cases came from experienced engineers *unfamiliar with the specific code they were modifying* — see [[soft-deletion]]'s batch-pipeline-developer framing.

Practical consequence: don't write off failure modes as "impossible given the architecture" without a demonstrable integrity check that would catch them. The assumption that a mature system won't fail a certain way is exactly the assumption that produces the failure.

## Trust but verify

> Any API upon which you depend won't work perfectly all of the time. It's a given that regardless of your engineering quality or rigor of testing, the API will have defects. Check the correctness of the most critical elements of your data using out-of-band data validators, even if API semantics suggest that you need not do so. Perfect algorithms may not have perfect implementations. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

This is the operational rationale for the entire [[data-validation-pipelines|out-of-band validator]] layer. Paxos is correct in theory; its implementations are hacks-riddled in practice. Bigtable is eventually consistent in theory; in practice it has edge cases that manifest more frequently at scale. Consumers who trust storage-layer guarantees without verifying invariants end up losing data in the gap between theoretical correctness and practical correctness.

The principle also echoes **[[end-to-end-argument|Saltzer-Reed-Clark's end-to-end argument]]**: infrastructure guarantees are insufficient; application-level integrity checks are the only reliable protection.

## Hope is not a strategy

> System components that aren't continually exercised fail when you need them most. Prove that data recovery works with regular exercise, or data recovery won't work. Humans lack discipline to continually exercise system components, so automation is your friend. However, when you staff such automation efforts with engineers who have competing priorities, you may end up with temporary stopgaps. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

The principle behind [[recovery-testing]]. The parenthetical matters: staffing is an engineering-priorities issue. If your recovery-test automation is owned by someone with competing priorities, it will become a temporary stopgap that silently rots. Chapter 26's implicit recommendation: give recovery testing a dedicated owner — as explicit as the ownership of the primary service.

The principle also motivates [[statistical-testing-techniques|Chaos Monkey]], [[testing-disaster-recovery|DiRT]], and the Wheel of Misfortune: all are forms of continuous exercise designed to keep recovery muscle from atrophying.

## Defense in depth

> Even the most bulletproof system is susceptible to bugs and operator error. In order for data integrity issues to be fixable, services must detect such issues quickly. Every strategy eventually fails in changing environments. The best data integrity strategies are multitiered — multiple strategies that fall back to one another and address a broad swath of scenarios together at reasonable cost. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

The architectural framing of the entire chapter. See [[defense-in-depth-data]] for the three-layer structure ([[soft-deletion]], [[tiered-backup-strategy|backups]], [[data-validation-pipelines|validators]]). The principle here is broader than the specific three layers: **every single strategy will eventually fail**, and the only defence is a set of complementary strategies that don't share failure modes.

The [[gmail-gtape-restore|Gmail 2011]] case is the canonical demonstration: internal redundancy and backups failed together. Only the offsite tape layer — deliberately chosen for media diversity — still worked. If the choice had been "replicate three times to the same kind of storage" rather than "replicate *and* also copy to tape," all layers would have failed simultaneously.

## Revisit and reexamine

> The fact that your data "was safe yesterday" isn't going to help you tomorrow, or even today. Systems and infrastructure change, and you've got to prove that your assumptions and processes remain relevant in the face of progress. (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md)

The chapter's worked example: the Shakespeare service has user-visible index data. Originally, if the index Bigtable was lost, it could be rebuilt from the source texts via a MapReduce — so no backups were needed. Then a new feature was added that lets users annotate text. Now the dataset can no longer be trivially re-created. The original decision "we don't need backups" was correct at the time and wrong now.

The principle operationally:

- Replay the "what could fail, and what's our response?" question every time the system materially changes.
- Treat backup and recovery strategy as an ADR-level decision that deserves revisiting on a regular cadence.
- Run DiRT not just on the original failure scenarios but on the new ones that architecture changes have introduced.

## How the five compose

The principles describe an epistemic posture (beginner's mind), an engineering discipline (trust but verify), an operational rigour (hope is not a strategy), a structural commitment (defense in depth), and a temporal discipline (revisit and reexamine). They reinforce each other:

- Beginner's mind motivates verification.
- Verification requires mechanisms (validators).
- Mechanisms require exercise (recovery testing).
- Exercise requires diverse layers (defence in depth).
- All of it requires continuous re-evaluation (revisit and reexamine).

A team that internalises all five is doing data-integrity engineering. A team that internalises four is leaving a gap that will eventually produce a major incident.

## The closing aspiration

Chapter 26's closing sentence on the goal state (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> As you get better at recovering from any breakage in reasonable time N, find ways to whittle down that time through more rapid and finer-grained loss detection, with the goal of approaching N = 0. You can then switch from planning recovery to planning prevention, with the aim of achieving the holy grail of all the data, all the time.

**Recovery time is the forcing function.** The five principles produce organisations that can recover quickly; the goal is to use the freed attention to prevent the losses in the first place. The same philosophical move that [[mttr-and-mttf|Chapter 7]] makes for general failures — optimise MTTR ruthlessly, and MTBF improves as a consequence.

## Cross-book connections

- [[unknown-unknowns]] (Richards & Ford) — beginner's mind is the epistemic humility that unknown-unknowns reasoning requires.
- [[architecture-fitness-function]] (Richards & Ford) — out-of-band validators are fitness functions; continuous recovery tests are fitness functions on the recovery subsystem.
- [[end-to-end-argument]] (Kleppmann) — "trust but verify" is the end-to-end argument's operational form: never rely on intermediate layers for properties you care about at the application level.
- [[evolutionary-architecture]] (Richards & Ford) — "revisit and reexamine" is the data-integrity specialisation of evolutionary-architecture discipline.
- [[learning-from-outages]] (SRE Ch 13) — "hope is not a strategy" is the positive form of Ch 13's "proactively test" directive.
- [[testing-for-reliability]] (SRE Ch 17) — testing is the mechanism behind the first four principles; Ch 17's coverage argument applies to data-integrity tests too.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[soft-deletion]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[recovery-testing]]
- [[data-integrity-failure-modes]]
- [[gmail-gtape-restore]]
- [[learning-from-outages]]
- [[testing-for-reliability]]
- [[end-to-end-argument]]
- [[unknown-unknowns]]
