# Breaking Real Systems, Fixing Real Systems

**Summary**: Chapter 28's hands-on counterpart to [[disaster-role-playing|Wheel of Misfortune]] — deliberate chaos exercises run against a real (but isolated) production instance, so newbies develop reflexive responses to company tooling and monitoring before their first real page. Includes Google Search SRE's "Let's burn a search cluster to the ground!" exercise.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## Why hands-on beats hypothetical

Chapter 28's ordering (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> A newbie can learn much about SRE by reading documentation, postmortems, and taking trainings. Disaster role playing can help get a newbie's mind into the game. However, the experience derived from hands-on experience breaking and/or fixing real production systems is even better.

The argument: real hands-on work builds the **reflexive responses** — typing the commands, interpreting real dashboard shapes, feeling the time pressure — that [[disaster-role-playing|tabletop]] cannot. Chapter 28 explicitly says this training should happen *before* a new SRE goes on-call; there will be "plenty of time for hands-on experience" after, but the reflexes need to be in place first.

## Realism is paramount

Chapter 28's requirement (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Multihomed stack** — at least one instance can be diverted from live traffic and "loaned" to the exercise
- **Alternative: fully featured staging or QA instance** — if production loan isn't possible, a smaller but still fully featured environment works
- **Synthetic load** that approximates real user/client traffic, plus matching resource consumption if possible

Without realism, the exercise teaches reflexes that don't transfer. A demo environment with no load is a different animal from a production replica under realistic traffic.

## Pattern 1: proctor injects a specific breakage

The first exercise shape Chapter 28 describes (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- A **senior SRE plans a specific type of breakage** they want the newbie to repair
- The newbie approaches it as they would a live incident: diagnose, find contributing factors, restore behaviour
- Misconfigurations, memory leaks, performance regressions, crashing queries, storage bottlenecks are all fair game

This pattern's weakness is its overhead — the senior SRE must design the scenario carefully. Chapter 28 offers a second pattern with lower overhead and broader team engagement.

## Pattern 2: "Let's burn a search cluster to the ground"

The Google Search SRE team's inverse exercise (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Instead of breaking first and letting the newbie diagnose, the team **starts from a known-good configuration and progressively impairs the stack**, observing effects through monitoring:

1. As a group, discuss what observable performance characteristics might change as the stack is crippled
2. Before inflicting damage, **poll participants for their predictions** and reasoning
3. Validate assumptions and justify the reasoning behind the observed behaviour

The exercise is run **quarterly** and has an unexpected second payoff: it "shakes out new bugs that we eagerly fix, because our systems do not always degrade as we would expect." The prediction step is the crucial one — it forces participants to commit to a model before reality tests it, which exposes mis-calibrations that would otherwise stay hidden.

## What this builds

The exercises build three things simultaneously:

- **Tool reflexes** — the newbie types real commands against real production-like systems; the muscle memory transfers directly to incidents
- **Calibrated intuition** — real degradation curves rarely match textbook descriptions; the exercises recalibrate participants' expectations
- **Bugs fixed** — the "burn a cluster" pattern discovers graceful-degradation failures that wouldn't surface otherwise, because the system is never deliberately stressed in production

## Relationship to chaos engineering

Chapter 28's exercises are an early, team-scale form of what is now called chaos engineering. The book's dedicated chaos treatment is in Chapter 17's [[statistical-testing-techniques|statistical testing techniques]] (Lemon, Chaos Monkey, Jepsen). The distinction:

- **Statistical testing techniques** (Ch 17) — automated, ongoing, production-integrated chaos; aims to surface bugs by continuous stress
- **Breaking real systems** (Ch 28) — scheduled, team-participatory, pedagogical chaos; aims to train engineers and incidentally surface bugs

The same infrastructure can serve both — but the *framing* and the *audience* differ. Chapter 28's version is consciously a training exercise; Chapter 17's version is consciously a testing discipline. Many organisations blur the two; Chapter 28 is clear that the training purpose should not be diluted by making the exercise a pure bug hunt.

## Bridging to production operations

Chapter 28 places breaking-real-systems exercises in the **week-before-on-call** window of the Figure 28-1 blueprint. The progression across the chapter's five practices:

1. [[teachable-postmortems|Postmortem reading]] — build abstract pattern library
2. [[disaster-role-playing|Wheel of Misfortune]] — exercise hypothesis-formation verbally
3. **Break real systems** — develop tool reflexes under realistic conditions
4. [[documentation-as-apprenticeship|Documentation overhaul]] — demonstrate that the newbie can explain the system
5. [[shadow-on-call]] — observe real incidents before owning them

Each step builds on the previous ones. Breaking real systems is where the abstract pattern library gets converted into usable motor skills.

## Related pages

- [[sre-onboarding]]
- [[disaster-role-playing]]
- [[shadow-on-call]]
- [[statistical-testing-techniques]]
- [[testing-for-cascading-failures]]
- [[operational-underload]]
- [[on-call-playbook]]
