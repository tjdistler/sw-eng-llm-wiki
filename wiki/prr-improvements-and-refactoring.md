# PRR Improvements and Refactoring

**Summary**: The phase of the [[simple-prr-model|Simple PRR Model]] that turns the [[prr-analysis-phase|Analysis]] phase's findings into changes in the service. Priorities are negotiated with the development team, SRE and product developers collaborate on refactoring and new controls, and execution proceeds until the service meets SRE standards. This is typically the longest and most variable phase.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The sequence

Chapter 32 describes three steps (source: chapter-32-the-evolving-sre-engagement-model.md):

1. Improvements are **prioritised** based upon importance for service reliability
2. The priorities are **discussed and negotiated** with the development team, and a plan of execution is agreed upon
3. Both SRE and product development teams **participate and assist each other** in refactoring parts of the service or implementing additional features

Shared execution is the distinctive feature. PRR improvement work is not thrown over the wall in either direction — the refactoring and new controls are built jointly so knowledge transfers along with code.

## Why this phase varies most

Chapter 32 explicitly calls out the variability (source: chapter-32-the-evolving-sre-engagement-model.md):

> This phase typically varies the most in duration and amount of effort.

The reasons:

- **Available engineering time.** Developer attention is finite; refactoring contends with feature work
- **Starting maturity.** A service that already follows [[production-guide|production best practices]] has less to do than one that doesn't
- **Starting complexity.** Larger, older, more intertwined services take longer to refactor safely
- **Myriad other factors.** Integration constraints, cross-team dependencies, platform migrations in flight

## The cost that motivates the other engagement models

The Improvements phase is the most tangible cost of the Simple PRR Model. Chapter 32 opens with the software-engineering analogy: the earlier a bug is found, the cheaper it is to fix. The Improvements phase is where the late-stage tax is paid (source: chapter-32-the-evolving-sre-engagement-model.md). The [[early-engagement-model|Early Engagement Model]] reduces this cost by moving the SRE conversation to the Design phase, where design trade-offs are still cheap to change. The [[frameworks-and-sre-platform|Frameworks and SRE Platform]] model shrinks it further by codifying the fixes into reusable code so services avoid needing them in the first place.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-analysis-phase]]
- [[prr-training-phase]]
- [[early-engagement-model]]
- [[frameworks-and-sre-platform]]
- [[site-reliability-engineering]]
