# Leading Questions

**Summary**: Chapter 30's Phase 3 technique for moving a team from ops mode to SRE thinking without framing the move as correction. A leading question is **not** a loaded question — it points the engineer toward a first-principles check on their own practice, reinforcing the mental model the embedded SRE has been building through [[explaining-reasoning|explicit reasoning]].

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## Leading vs loaded

Chapter 30's first clarification: *leading questions are not loaded questions* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The distinction matters:

- A **leading question** invites the engineer to apply a principle they already know. The question's phrasing gestures at the principle; the engineer supplies the application.
- A **loaded question** is a rhetorical accusation framed as a question. It invites defensiveness, not reasoning.

The whole point of the technique is pedagogical, not persuasive. A visiting SRE who loads their questions will push the team into the same defensive posture that makes old postmortems feel punitive. See [[bad-apple-theory]].

## Why this technique matters

Chapter 30 names a subtle but important reason (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> It's particularly valuable for you to model this behavior because, by definition, a team in ops mode rejects this sort of reasoning from its own constituents.

A team that has slid into [[ops-mode]] systematically tunes out first-principles challenges from within. The embedded SRE's **outside** position is what makes the technique work — the team is willing to entertain principles-based reasoning from the visitor that it wouldn't entertain from a team member. Done well, the technique re-legitimises principled reasoning inside the team, so teammates can start asking each other the same questions after the visitor leaves.

## The two worked examples

Chapter 30 gives two concrete leading questions (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> I see that the TaskFailures alert fires frequently, but the on-call engineers usually don't do anything to respond to the alert. How does this impact the SLO?

The scaffolding: the visiting SRE has observed a specific pattern (noisy alert + no response) and the question invites the engineer to evaluate that pattern against a principle the team has agreed to (the [[service-level-objective|SLO]]). The engineer does the actual reasoning — *is this alert contributing to SLO violations we care about, or is it noise?* — which is both the diagnosis and the engineer's practice applying the principle.

> This turnup procedure looks pretty complicated. Do you know why there are so many config files to update when creating a new instance of the service?

Again, a specific observation + an invitation to reason about a principle ([[simplicity-sre|simplicity]], [[toil-and-engineering-balance|toil]]). The question doesn't accuse the procedure of being bad; it invites the engineer to surface whether the complexity is earned. Often the answer is "historical accident" — which is the engineer diagnosing their own kindling.

## The two counter-examples

Chapter 30 names two phrasings to **avoid** (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> What's up with all of these old, stalled releases?

> Why does the Frobnitzer do so many things?

Both are loaded, not leading. They convey a verdict ("these are bad") in the form of a question, which puts the engineer on the defensive. A team asked these questions will either explain away the situation or stop volunteering information, neither of which is useful.

The difference between these counter-examples and the good examples is **what the question points at**: good leading questions point at a shared principle (SLO impact, procedure complexity), while loaded questions point at the engineer's work ("why is your code like this?"). The first invites reasoning; the second invites a defence.

## The technique in sequence

Chapter 30 sequences the Phase 3 pedagogy deliberately. Leading questions come **after** [[explaining-reasoning|explaining your reasoning]] on policy questions (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> Once you've spent some time explaining your reasoning for various policy questions, this practice reinforces the team's understanding of SRE philosophy.

The explanation phase establishes the principles; the leading-questions phase gives the team practice applying them. Asking leading questions before principles have been explained produces puzzlement rather than reasoning — the team doesn't know which principle the question is gesturing at.

## Relationship to hypothetico-deductive debugging

Leading questions borrow structurally from the Chapter 12 [[hypothetico-deductive-debugging]] loop: observation → hypothesis → test. The question names the observation; the engineer supplies the hypothesis; the engineer's subsequent action is the test. The visiting SRE is modelling the same cognitive pattern that makes a good on-call engineer effective, just applied to team practice rather than incident diagnosis.

## Related pages

- [[embedding-sre]]
- [[explaining-reasoning]]
- [[ops-mode]]
- [[bad-apple-theory]]
- [[service-level-objective]]
- [[alert-philosophy]]
- [[simplicity-sre]]
- [[toil-and-engineering-balance]]
- [[hypothetico-deductive-debugging]]
- [[postvitam]]
