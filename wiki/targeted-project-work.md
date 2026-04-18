# Targeted Project Work

**Summary**: Chapter 28's rule for applied onboarding work — give the newbie a real problem to own rather than a queue of menial tasks. A small but shippable starter project builds a sense of ownership, earns trust with senior colleagues, and balances the student's time between pure learning and productive output.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The principle

> SREs are problem solvers, so give them a hearty problem to solve! When starting out, having even a minor sense of ownership in the team's service can do wonders for learning. (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md)

Project work is the applied counterweight to the frontloaded theory in [[cumulative-learning-paths]]. Splitting the newbie's time between learning and project work provides a sense of purpose and productivity that neither activity produces alone. A pure-learning onboarding feels disconnected from reality; a pure-project onboarding (see [[trial-by-fire-anti-pattern]]) skips the theory that makes later work efficient.

## Why it earns trust

A deliberate side effect of project ownership: **senior colleagues approach the newbie to learn about the new component or process**. This reverses the usual power asymmetry where newbies are always the ones asking questions (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Once the senior team has asked the newbie for information about *their* area, trust-building accelerates — the newbie has demonstrated competence on something, which is the precondition for being trusted with on-call.

## Google's company-wide starter-project convention

Chapter 28 notes that all Google engineers are given a **starter project** meant to provide a tour through the infrastructure sufficient to make a small but useful contribution early (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). The SRE-specific version applies the same instinct to production infrastructure.

## Three starter-project patterns

Widdowson names three patterns that work well (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

### Trivial user-visible feature change + release shepherding

- Make a small user-facing change in the serving stack
- Shepherd the feature release all the way through to production
- **Value**: forces the newbie to learn both the development toolchain *and* the [[release-engineering|binary release process]]; builds empathy for the developers

### Adding monitoring to blind spots

- Find an area of the service that currently lacks [[four-golden-signals|golden-signal monitoring]]
- Add the metrics and alerts
- **Value**: forces the newbie to **reason with the monitoring logic** while reconciling their understanding of the system with how it *actually* behaves; the mismatch is pedagogical

### Automating a pain point not yet worth anyone else's time

- Find something repetitive that isn't painful enough for senior SREs to have automated already
- Automate it
- **Value**: gives the newbie firsthand appreciation for **why SREs place such high value on removing [[toil-and-engineering-balance|toil]]**

## What these patterns have in common

All three produce **shippable output** (a deployed feature, a live dashboard, a running automation) and all three **traverse the full stack** in one way or another. That combination — real output plus cross-stack exposure — is what distinguishes targeted project work from the ticket queue, which produces neither.

The patterns also all align with [[sre-tenets|canonical SRE responsibilities]]: change management, monitoring, and toil reduction. The newbie is learning the discipline by doing a scoped instance of the discipline.

## The build-over-time shape

The triangular shape of project work in Chapter 28's blueprint (Figure 28-1) is deliberate: project work **starts small and builds over time**, becoming more complex and continuing well after the newbie goes on-call (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). A starter project is the first rung; mid-career SRE [[software-engineering-in-sre|software-engineering projects]] are a later rung on the same ladder.

## Relationship to the 50% cap

Targeted project work is also a precondition for honouring the [[toil-and-engineering-balance|50% cap on toil]] at the individual level. A newbie whose entire onboarding is reactive ticket work is by definition 100% toil, which trains them to see SRE as an ops role. Project work from day one trains them to see it as the engineering role Chapter 1 defines.

## Related pages

- [[sre-onboarding]]
- [[cumulative-learning-paths]]
- [[trial-by-fire-anti-pattern]]
- [[toil-and-engineering-balance]]
- [[release-engineering]]
- [[four-golden-signals]]
- [[software-engineering-in-sre]]
