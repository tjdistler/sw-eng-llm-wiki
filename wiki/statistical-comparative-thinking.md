# Statistical and Comparative Thinking

**Summary**: The second of Chapter 28's three aspirational SRE attributes — the ability to prune a massive decision tree under time pressure by constructing careful hypotheses and comparing controlled variables. Incident response is a "which of these things is not like the other?" game; this attribute is the mental machinery for playing it well.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The framing

Chapter 28 reframes incident response as navigation through a massive decision tree (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> You can think of an SRE's approach to incident response for large-scale systems as navigating through a massive decision tree unfolding in front of them. In the limited time window afforded by the demands of incident response, the SRE can take a few actions out of hundreds with the goal of mitigating the outage.

Time is the binding constraint. The SRE must **prune aggressively**, and do so correctly. The attribute this page names is the mental machinery that makes that pruning reliable rather than lucky.

## Two components

Widdowson splits the attribute into two halves (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Experience** — only time and exposure to a breadth of production systems produces this; it is the substrate of pattern-matching that lets the SRE see the shape of the decision tree at all
- **Careful hypothesis construction** — explicit mental work that, when proven or disproven, further narrows the decision space

Neither alone is sufficient. Pure experience degenerates into [[troubleshooting-anti-patterns|latching onto past causes]]. Pure hypothesis work without experience is too slow to finish in the time available.

## The "which of these things is not like the other?" game

Chapter 28's evocative framing of the comparative half (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Tracking down system breakages is often akin to playing a game of "which of these things is not like the other?" where "things" might entail kernel version, CPU architecture, binary version(s) in your stack, regional traffic mix, or a hundred other factors.

For the game to be playable, each of those factors must be **controllable and individually analysable**. That is partly an architectural responsibility of the team — build systems where variables can be isolated — and partly a reverse-engineering responsibility of the individual SRE (see [[reverse-engineering-skills]]).

## Connection to Chapter 12's hypothetico-deductive loop

This attribute is the human-capability side of what Chapter 12's [[troubleshooting-model|six-step loop]] formalises as process. Chapter 12's [[hypothetico-deductive-debugging]] names debugging as a scientific method of observation + theoretical basis + iteration; Chapter 28 names the underlying *attribute* that Chapter 12's process depends on.

- Chapter 12 provides the procedural scaffolding (the loop, the triage step, the test-and-treat step)
- Chapter 28 argues that the **scaffolding only produces results with trained comparators** behind it, and makes training that attribute a first-class onboarding goal

## What the training target looks like

Chapter 28's directive: *train our newest SREs to become good analysts and comparators from their earliest moments on the job* (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). The "from their earliest moments" is load-bearing — comparative thinking is not a senior skill to defer; it is a habit cultivated from day one.

[[reverse-engineering-class]] develops it by teaching students to trace requests through multiple paths and compare the discoveries. [[disaster-role-playing]] develops it by forcing the student to articulate hypotheses aloud for the game master to test. [[teachable-postmortems]] develops it by exposing students to the real decision trees other SREs navigated in the past.

## The architectural responsibility

The game requires individually controllable variables. Chapter 28 is explicit (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Architecturally, it's the team's responsibility to ensure all of these factors can be controlled for and individually analyzed and compared.

That is a system-design investment, not only a training investment. Services that make it easy to compare last week's behaviour with this week's, one region with another, one binary version with another, are debuggable under pressure. Services that don't, aren't — regardless of how skilled the on-caller is.

## Related pages

- [[sre-onboarding]]
- [[reverse-engineering-skills]]
- [[improvisational-troubleshooting]]
- [[reverse-engineering-class]]
- [[troubleshooting-model]]
- [[hypothetico-deductive-debugging]]
- [[troubleshooting-anti-patterns]]
- [[disaster-role-playing]]
