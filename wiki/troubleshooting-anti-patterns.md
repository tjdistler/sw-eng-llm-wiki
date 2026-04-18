# Troubleshooting Anti-Patterns

**Summary**: Chapter 12's catalogue of common failure modes in the Triage / Examine / Diagnose phases of troubleshooting. All four are rooted in shallow system knowledge or logical fallacies; all four are avoidable with a methodical approach and a few named heuristics (horses-not-zebras, Occam, Hickam, correlation-not-causation).

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## The four pitfalls

Chapter 12's Common Pitfalls subsection lists four (source: chapter-12-effective-troubleshooting.md):

1. **Looking at irrelevant symptoms or misunderstanding the meaning of system metrics.** Produces wild goose chases.
2. **Misunderstanding how to change the system, its inputs, or environment safely to test hypotheses.** Produces dangerous experiments that either destroy evidence or make the incident worse.
3. **Coming up with wildly improbable theories, or latching onto causes of past problems** ("since it happened once, it must be happening again").
4. **Hunting down spurious correlations** that are actually coincidences, or correlated only because they share a common cause.

## Why the first two happen

Pitfalls 1 and 2 are system-knowledge failures. Chapter 12's diagnosis (source: chapter-12-effective-troubleshooting.md):

> Fixing the first and second common pitfalls is a matter of learning the system in question and becoming experienced with the common patterns used in distributed systems.

There is no shortcut. Expertise in troubleshooting a service is expertise in how that service works. The generic process helps, but without system knowledge the generic process is slow.

See [[hypothetico-deductive-debugging]] for the relationship between system knowledge and debugging speed.

## Horses, not zebras

Pitfall 3 (wildly improbable theories) is fought with Theodore Woodward's 1940s medical-school heuristic (source: chapter-12-effective-troubleshooting.md):

> As doctors are taught, "when you hear hoofbeats, think of horses not zebras."

Not all failures are equally probable. Prior likelihood matters. The most common causes of an outage — recent deployment, config change, capacity shortfall — should be investigated before the rare ones.

Chapter 12 adds the important caveat: this heuristic works better in some domains than others. In a distributed filesystem with well-designed replication, an entire class of failures (single-disk latency) may have been eliminated by construction. Zebra-hunting is unhelpful when the ecosystem has no zebras; it is crucial when an entire zebra herd has just arrived (a new subsystem, a new dependency, a new traffic pattern).

## Occam's Razor, balanced by Hickam's Dictum

The chapter pairs two competing heuristics (source: chapter-12-effective-troubleshooting.md):

- **[Occam's Razor](https://en.wikipedia.org/wiki/Occam%27s_razor):** all things equal, prefer simpler explanations.
- **[Hickam's Dictum](https://en.wikipedia.org/wiki/Hickam%27s_dictum):** a patient can have as many diagnoses as they damn well please.

The book's gloss (source: chapter-12-effective-troubleshooting.md):

> It may still be the case that there are multiple problems; in particular, it may be more likely that a system has a number of common low-grade problems that, taken together, explain all the symptoms rather than a single rare problem that causes them all.

In practice: prefer simplicity, but don't force every symptom under one root cause. Distributed systems fail in combinations more often than in singletons.

## Correlation is not causation

Pitfall 4 (spurious correlations) gets its own mini-essay. Chapter 12's example (source: chapter-12-effective-troubleshooting.md):

> Packet loss within a cluster and failed hard drives in the cluster share common causes — in this case, a power outage, though network failure clearly doesn't cause the hard drive failures nor vice versa.

Two failure modes here:

- **Common-cause confusion.** A and B correlate because C causes both. Treating B because you observed A doesn't help.
- **Coincidence at scale.** As systems grow and more metrics are monitored, inevitable that some will correlate by chance. The chapter's footnote references the [Spurious Correlations](http://tylervigen.com/view_correlation?id=1099) site (CS PhDs awarded correlates r² = 0.94 with per-capita cheese consumption 2000–2009).

The antidote is **mechanism**. A causal claim requires a plausible path: this metric's motion *caused* this failure *because* the system works as follows. Without a mechanism, the correlation is a hypothesis to test, not evidence.

## Latching onto past causes

Chapter 12 names this as a specific form of pitfall 3 (source: chapter-12-effective-troubleshooting.md):

> Latching on to causes of past problems, reasoning that since it happened once, it must be happening again.

[[incident-response-mindset]] (Chapter 11) names the underlying cognitive failure: **confirmation bias**. The fourth page in a week looks like the previous three, and the engineer jumps to the previous diagnosis without checking.

The antidote is the pace-before-decide discipline: the current page's evidence must be re-examined afresh, not matched against the previous page's pattern.

## Why naming them helps

Chapter 12 is clear that the antidote to these pitfalls is not genius but awareness (source: chapter-12-effective-troubleshooting.md):

> Understanding failures in our reasoning process is the first step to avoiding them and becoming more effective in solving problems.

All four pitfalls are recognisable in the moment if you have a name for them. An SRE who has internalised "horses not zebras" will catch themselves mid-hypothesis-generation and check. An SRE who knows "correlation is not causation" will demand a mechanism before acting on a correlation. Naming converts a cognitive failure from an unnoticed habit into a noticeable event.

## The App Engine case study confirms the pattern

Chapter 12's closing case study features a near-miss spurious correlation (source: chapter-12-effective-troubleshooting.md). A developer noticed the latency spike correlated with increased `merge_join` datastore calls — a plausible indexing theory. The team built on this hypothesis until static-asset requests (which don't touch the datastore) turned out to be equally slow, *disconfirming* the merge-join theory as the whole story. The real cause was a whitelist-caching antipattern exercised by an automated security scanner. If the team had committed to the first theory without checking the broader evidence, they would have wasted significant time on an irrelevant fix.

## Cross-book connection

- [[incident-response-mindset]] — Chapter 11's confirmation-bias discussion is the cognitive-science substrate for Chapter 12's "latching onto past causes" pitfall.
- [[fallacies-of-distributed-computing]] (Deutsch via Newman) — the structural fallacies of distributed-system *design*; Chapter 12's pitfalls are the cognitive fallacies of distributed-system *debugging*. Both are defended against by naming.
- [[unknown-unknowns]] (Richards & Ford) — the pitfalls are the mechanisms by which unknowns masquerade as knowns during an incident.

## Related pages

- [[troubleshooting-model]]
- [[hypothetico-deductive-debugging]]
- [[triage-sre]]
- [[incident-response-mindset]]
- [[divide-and-conquer-debugging]]
- [[site-reliability-engineering]]
