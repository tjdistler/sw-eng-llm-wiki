# Bad Apple Theory

**Summary**: The demonstrably-false belief that if you get rid of the individuals who make mistakes, the system will keep working fine. Chapter 30 names this as the underlying (often unspoken) reason postmortems feel punitive to unhealthy teams, and prescribes direct refutation with the opposing framing: **mistakes are inevitable in any system with multiple subtle interactions**.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The theory

The unspoken premise Chapter 30 names (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> The system is working fine, and if we get rid of all the bad apples and their mistakes, the system will continue to be fine.

This is the **Bad Apple Theory**: failures come from flawed individuals, and the organisational response to failure is to identify and remove those individuals. A team that believes this will treat postmortems as trials, treat "why me?" as a reasonable reaction to being asked to write one, and quietly avoid surfacing incidents to stay off the suspect list.

## Why it is false

Chapter 30 cites evidence from other high-reliability fields: *The Bad Apple Theory is demonstrably false, as shown by evidence [Dek14] from several disciplines, including airline safety* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The reference is to Sidney Dekker's work on human factors and systems safety.

The counter-evidence is the same across domains: incidents almost always result from **multiple subtle interactions** that nobody could have fully anticipated at the time. Removing the operator who happened to be at the controls doesn't change any of the interactions. The next operator, faced with the same system in a similar state, makes the same class of mistake. The individual was **misled by the system**, not deficient.

This is structurally the same argument the Chapter 15 [[blameless-postmortem|blameless-postmortem philosophy]] makes: *you can't fix people, but you can fix systems and processes to better support people making the right choices.* Chapter 30 just names the specific belief the blameless culture has to defeat.

## The refutation phrasing

Chapter 30 supplies the canonical replacement phrasing to use when co-authoring a postmortem with an engineer who feels blamed (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> Mistakes are inevitable in any system with multiple subtle interactions. You were on-call, and I trust you to make the right decisions with the right information. I'd like you to write down what you were thinking at each point in time, so that we can find out where the system misled you, and where the cognitive demands were too high.

Every clause does work:

- **"Mistakes are inevitable"** — states the non-Bad-Apple premise directly.
- **"I trust you to make the right decisions with the right information"** — separates the person's competence from the incident's cause.
- **"Write down what you were thinking at each point in time"** — collects the raw material for the real analysis. Thinking-at-the-time is what a postmortem actually needs; blame produces sanitised timelines.
- **"Where the system misled you, and where the cognitive demands were too high"** — frames the output as system changes, not personnel changes.

## Why teams believe it

Chapter 30 doesn't dwell on the origin, but the pattern is consistent with the Chapter 15 analysis: the Bad Apple Theory is what happens when an organisation conflates **accountability** with **blame**. Accountability is "someone owns the follow-ups"; blame is "someone deserves punishment". The two are often confused because both involve naming individuals, but they function oppositely: accountability keeps postmortems useful, blame drives them into ritual.

An embedded SRE should expect to encounter this belief silently rather than openly. The visible symptom is the "why me?" reaction to postmortem ownership (Chapter 30's example). The underlying cause is the unspoken Bad Apple Theory; *you should point out this falsity* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

## Relationship to the blameless culture

The Chapter 15 [[blameless-postmortem|blameless-postmortem culture]] is the operational answer to the Bad Apple Theory. Chapter 15 imports the practice from aviation and healthcare; Chapter 30 names the theory it replaces. The connection:

- **Chapter 15** supplies the positive framing: "investigate the systematic reasons why an individual or team had incomplete or incorrect information."
- **Chapter 30** supplies the negative framing: the belief that has to be displaced for the positive framing to land.

Without displacing Bad Apple Theory first, a team can go through the blameless-postmortem motions while the substance — fear-driven cover-ups — remains unchanged. This is why Chapter 30 prescribes **writing a great postmortem with the team** (not correcting their old postmortems) as the Phase 2 intervention: the demonstration displaces the theory; the commentary reinforces it.

## Related pages

- [[embedding-sre]]
- [[blameless-postmortem]]
- [[postmortem-philosophy]]
- [[postmortem-culture-activities]]
- [[incident-response-mindset]]
- [[learning-from-outages]]
