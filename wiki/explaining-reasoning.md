# Explaining Reasoning

**Summary**: Chapter 30's Phase 3 discipline for embedded SREs: explain the reasoning behind every decision, whether or not anyone asks for it. The goal is that after the embedded SRE leaves, the team should be able to **predict** what the visiting SRE would say about a design or changelist. Unverbalised reasoning can't be inherited.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The discipline

Chapter 30's framing (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> Prepare for this undertaking to be challenged. If you're lucky, the challenge will be along the lines of, "Explain why. Right now. In the middle of the weekly production meeting." If you're unlucky, no one demands an explanation. Sidestep this problem entirely by simply explaining all of your decisions, whether or not someone requests an explanation.

The **unlucky** case is the important one. A team that has slid into [[ops-mode]] often stops asking why because the answers stopped mattering — they're too busy reacting. The embedded SRE's job is to put the reasoning back into the air, unasked, so the team starts remembering what good reasoning sounds like.

The success criterion is concrete: *After you leave, the team should be able to predict what your comment on a design or changelist would be* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). That is only possible if the reasoning has been verbalised many times.

## Refer to the basics

The discipline is not just "say more words". Chapter 30 specifically prescribes that every explanation **refer back to the basics** — [[service-level-objective|SLOs]], [[error-budget|error budgets]], the [[toil-and-engineering-balance|50% cap]], [[alert-philosophy|actionable alerting]], and the other principles introduced in Chapters 1 and 6. Grounding each decision in first principles builds the team's mental model. A reasoning chain that stops at "this felt wrong" teaches nothing.

## The four worked examples

Chapter 30 gives two good explanations and two bad ones. Studying both pairs is worthwhile because the bad versions are not *wrong* — they're just insufficient, which is the common trap (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

### Good: refer to the SLO and error budget

> I'm not pushing back on the latest release because the tests are bad. I'm pushing back because the error budget we set for releases is exhausted.

The reasoning terminates in an explicit, quantitative agreement the team has already made. Anyone can reproduce the decision by looking up the error-budget state.

### Good: connect SLO to engineering requirement

> Releases need to be rollback-safe because our SLO is tight. Meeting that SLO requires that the mean time to recovery is small, so in-depth diagnosis before a rollback is not realistic.

The reasoning chain is **SLO → MTTR requirement → rollback-safety requirement**. The chain is short, but each link is explicit. A team that hears this can apply the same chain to a different release or a different safety property.

### Insufficient: intuition without mechanism

> I don't think having every server generate its routing config is safe, because we can't see it.

Chapter 30's note: *this decision is probably correct, but the reasoning is poor (or poorly explained). The team can't read your mind, so they very likely might emulate the observed poor reasoning.*

Better phrasing the chapter supplies:

> […] isn't safe because a bug in that code can cause a correlated failure across the service and the additional code is a source of bugs that might slow down a rollback.

Two specific failure modes are named (correlated failure; rollback slowdown), each connected to a reliability principle. The team can now apply the same reasoning to the next "every server does X" proposal.

### Insufficient: assert the rule without the rule's purpose

> The automation should give up if it encounters a conflicting deployment.

Chapter 30's note: *like the previous example, this explanation is probably correct, but insufficient.* The chapter's replacement:

> […] because we're making the simplifying assumption that all changes pass through the automation, and something has clearly violated that rule. If this happens often, we should identify and remove sources of unorganized change.

The improved version makes two things explicit: the assumption that is being violated, and the corrective action when the violation recurs. The team can now reason about when the rule applies (and when it doesn't) rather than applying it ritually.

## The predicted-comment heuristic

Chapter 30's success check — that the team can predict the visiting SRE's comment — is a concrete test for whether the reasoning transfer has worked. If two team members pre-review a changelist and converge on the same concerns the visiting SRE would have raised, the mental model has been transferred. If they diverge wildly or can only predict the *conclusion* but not the *reason*, the reasoning hasn't landed yet.

## Relationship to leading questions

[[leading-questions|Leading questions]] and explaining reasoning are the two halves of Chapter 30's Phase 3 pedagogy:

- **Explain your reasoning** establishes the principles the team is meant to use.
- **Leading questions** gives the team practice applying those principles themselves.

The explanation is the demonstration; the leading question is the exercise. A team that gets only explanations can repeat the principles but not apply them; a team that gets only questions without prior explanations can't answer them. Chapter 30 uses both, in roughly that order.

## Related pages

- [[embedding-sre]]
- [[leading-questions]]
- [[service-level-objective]]
- [[error-budget]]
- [[mttr-and-mttf]]
- [[alert-philosophy]]
- [[blameless-postmortem]]
- [[architectural-thinking]]
