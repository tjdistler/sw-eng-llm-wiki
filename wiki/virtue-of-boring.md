# The Virtue of Boring

**Summary**: Chapter 9 of *Site Reliability Engineering*'s claim that **"boring" is a positive attribute for software**. Programs should stick to the script and predictably accomplish their goals; surprise in production is the SRE's enemy. The chapter uses Fred Brooks's essential-vs-accidental-complexity framing to operationalise the advice: SREs push back on accidental complexity as a core part of the job.

**Sources**: `raw/site-reliability-engineering/chapter-09-simplicity.md`

**Last updated**: 2026-04-17

---

## Boring as a desired property

Chapter 9 opens the section with a memorable inversion (source: chapter-09-simplicity.md):

> Unlike just about everything else in life, "boring" is actually a positive attribute when it comes to software! We don't want our programs to be spontaneous and interesting; we want them to stick to the script and predictably accomplish their business goals.

Google engineer Robert Muth's version, quoted in the chapter:

> Unlike a detective story, the lack of excitement, suspense, and puzzles is actually a desirable property of source code.

The SRE-specific framing is simpler: **surprises in production are the nemeses of SRE**. Production surprises are incidents waiting to happen, and most of them are caused by behaviour the code's author would have called "interesting."

## Essential vs accidental complexity (Brooks)

Chapter 9 grounds the boring-is-good claim in Fred Brooks's 1986 "No Silver Bullet" essay (source: chapter-09-simplicity.md):

- **Essential complexity** — the complexity inherent in a given situation that cannot be removed from the problem definition.
- **Accidental complexity** — complexity that is more fluid and can be resolved with engineering effort.

Chapter 9's example: writing a web server carries the essential complexity of serving pages quickly. Writing it in Java introduces the accidental complexity of managing garbage-collection pauses so they don't blow latency SLOs. The latter is a consequence of an implementation choice, not of the problem.

The page [[accidental-complexity]] has the full framing, including Richards and Ford's architectural-scale extension and the orchestration-driven-SOA case study.

## The SRE mandate

From the essential/accidental framing, Chapter 9 derives two specific responsibilities for SRE teams (source: chapter-09-simplicity.md):

1. **Push back when accidental complexity is introduced** into the systems for which they are responsible.
2. **Constantly strive to eliminate complexity** in systems they onboard and assume operational responsibility for.

The second is worth emphasising: simplicity is not a one-time design decision, it is an ongoing operational practice. Systems accumulate accidental complexity continuously (every shortcut, every special case, every "we'll clean this up later") and the SRE team has structural authority to push back because they carry the operational cost.

## Why it is the SRE's job

The mandate is load-bearing because:

- The product development team sees the benefits of new features but not the [[toil-and-engineering-balance|operational overhead]] they create.
- The team that runs the system at 3am has both the motivation and the authority (via the [[toil-and-engineering-balance|50% cap]] and the [[error-budget]]) to refuse changes that make the system harder to run.
- Complexity does not announce itself. It compounds through locally-reasonable decisions that aggregate into unmaintainable systems.

SRE's place in the organisation — embedded enough to catch the complexity as it arrives, independent enough to push back — is what makes the mandate enforceable.

## Cross-book connections

- [[accidental-complexity]] — the full Brooks framing, with Richards and Ford's architectural-scale extension and the canonical orchestration-driven-SOA cautionary tale
- [[monitoring-simplicity]] (Ch 6) — the Ch 6 specialisation: monitoring systems are fertile ground for accidental complexity and the same pushback discipline applies
- [[architecture-characteristics]] (Richards & Ford) — "simplicity" is explicitly in Richards and Ford's scorecard; boring and simple are closely related architectural ratings
- [[unix-philosophy]] (Kleppmann) — "do one thing and do it well" is the tool-level version of the boring-is-a-virtue claim

## Related pages

- [[simplicity-sre]]
- [[accidental-complexity]]
- [[monitoring-simplicity]]
- [[negative-lines-of-code]]
- [[minimal-apis]]
- [[toil-and-engineering-balance]]
- [[error-budget]]
- [[site-reliability-engineering]]
