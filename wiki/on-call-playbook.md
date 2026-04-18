# On-Call Playbook

**Summary**: A document prepared ahead of time that records best-practice troubleshooting steps for a class of incident. Chapter 1 of the SRE book reports that a practised on-call engineer armed with a playbook recovers from incidents roughly 3× faster than an equally skilled engineer winging it.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The finding

> When humans are necessary, we have found that thinking through and recording the best practices ahead of time in a "playbook" produces roughly a 3x improvement in MTTR as compared to the strategy of "winging it". (source: chapter-01-introduction.md)

The 3× is striking because the alternative — a smart engineer figuring it out live — is already a reasonable baseline. What playbooks buy is not cognitive capacity but *time*: the steps are pre-debated, the commands are pre-tested, the dead ends are pre-eliminated.

## What goes in a playbook

Chapter 1 doesn't prescribe a format but identifies the ingredients (source: chapter-01-introduction.md):

- **Clear and thorough troubleshooting steps** for the incident class.
- **Tips** — the kind of tacit knowledge that's otherwise only in someone's head.

Later chapters of the book expand on playbook contents (escalation paths, diagnostic queries, safe-to-run commands vs destructive commands, links to dashboards).

## What a playbook is not

> While no playbook, no matter how comprehensive it may be, is a substitute for smart engineers able to think on the fly [...] (source: chapter-01-introduction.md)

The playbook is scaffolding for the engineer's judgment, not a replacement for it. Incidents will always involve novel combinations that the playbook didn't anticipate. The playbook's job is to eliminate the *routine* portion of the response so the engineer can spend all their attention on the novel portion.

## Wheel of Misfortune

Chapter 1 mentions Wheel of Misfortune as a complementary practice — a scenario-based exercise where on-call engineers walk through hypothetical incidents live, building the reflexes and familiarity with playbooks that cannot be acquired by reading alone (source: chapter-01-introduction.md). The book's "Disaster Role Playing" section covers it in depth.

Chapter 11 adds the operational-underload motivation: Wheel of Misfortune is the antidote to a quiet system (source: chapter-11-being-on-call.md). When production rarely pages, scenario drills are how engineers stay calibrated on the tools, the playbook, and their own judgement. Google's company-wide annual **DiRT** (Disaster Recovery Training) event is the organisational-scale version — see [[operational-underload]].

Chapter 28 gives the exercise its full operational manual — GM, primary/secondary contestants, 30-60 minute scenarios, deliberate red-herring injection — and also exposes the bidirectional framing that Chapter 11 understates. It isn't only an underload remedy; it is **the week-to-week mechanism for keeping SREs of wildly different experience levels current on each other's knowledge and on new stack features** (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). See [[disaster-role-playing]] for the full exercise and [[sre-onboarding]] for where it fits in Chapter 28's broader training blueprint.

## What playbooks encode (Chapter 12 reading)

Chapter 12's [[troubleshooting-model|generic troubleshooting loop]] is what a skilled SRE runs in their head. A playbook encodes the *hypothesis-generation step* for known incident classes — the ranked list of "for this alert, here's what has gone wrong before and here's how to check each possibility" (source: chapter-12-effective-troubleshooting.md).

The Shakespeare worked example illustrates the pattern: the alert fires, links to the playbook, the playbook links to the black-box prober's recent results and tells the on-call engineer the expected request/response format. The engineer can skip straight to the Examine phase with the context pre-assembled.

A good playbook also incorporates [[making-troubleshooting-easier|troubleshooting-easier]] infrastructure — links to dashboards showing the relevant [[four-golden-signals|golden signals]], known [[correlation-ids|request IDs]] to grep on, commands that exercise [[distributed-tracing|distributed tracing]]. It is the "system knowledge" half of troubleshooting expertise captured as a runnable artifact.

## Tool familiarity and rollback rehearsal (Chapter 13)

Chapter 13's case studies surface two playbook-adjacent lessons (source: chapter-13-emergency-response.md):

- **The CLI and alternative-access tools that the playbook points to must themselves be exercised regularly.** The [[change-induced-emergency|Friday config-push incident]]'s findings explicitly note that engineers needed to be more familiar with the CLI and alternative-access tools and to test them more routinely. A tool referenced by the playbook but never used is a dead link, discovered at the worst possible moment.
- **Rollback procedures are part of the playbook and must be tested before the operation that relies on them.** The [[test-induced-emergency|MySQL permissions-test incident]] extended its outage because the rollback had never been rehearsed in a test environment. Chapter 13's explicit follow-up rule: **thoroughly test rollback procedures before large-scale tests**.

The combined directive for a playbook author: if a command appears in the playbook, someone should have run it successfully (in a test environment) in the last quarter.

## Playbook as onboarding artifact (Chapter 28)

Chapter 28 adds two framings the earlier chapters don't (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **The playbook is a deliverable of the [[on-call-learning-checklist|on-call learning checklist]].** Checklist completion proves the newbie understands the systems; the playbook is then what they operate on when pages fire. Checklist → playbook is the path from comprehension to action.
- **Playbook familiarity is developed before going on-call, not after.** [[disaster-role-playing|Wheel of Misfortune]] sessions exercise the playbook verbally; [[breaking-real-systems|break-real-things exercises]] exercise it against realistic infrastructure; [[shadow-on-call|shadow on-call]] exposes the newbie to the playbook being used in a real incident. By the time the newbie is primary, the playbook is a familiar tool rather than something they first encounter under stress.

## Relationship to other tenets

- [[emergency-response]] is the tenet this page implements; playbooks are one of its two main levers (the other being automated recovery).
- [[blameless-postmortem|Postmortems]] feed playbooks: each significant incident should produce action items, and updating the playbook is among the most common of those items.
- [[toil-and-engineering-balance]]: writing and maintaining playbooks is engineering work, not ops work; it counts toward the 50% engineering half of the cap.

## Related pages

- [[emergency-response]]
- [[mttr-and-mttf]]
- [[blameless-postmortem]]
- [[sre-tenets]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[operational-underload]]
- [[incident-response-mindset]]
- [[troubleshooting-model]]
- [[making-troubleshooting-easier]]
- [[learning-from-outages]]
- [[test-induced-emergency]]
- [[change-induced-emergency]]
- [[sre-onboarding]]
- [[on-call-learning-checklist]]
- [[disaster-role-playing]]
- [[shadow-on-call]]
- [[breaking-real-systems]]
