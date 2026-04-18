# Postvitam

**Summary**: Chapter 30's name (*in contrast to a postmortem*) for the after-action report an embedded SRE writes at the end of the engagement. Where a postmortem documents what went wrong and why, a postvitam documents what went *right*: the critical decisions at each step that led to success, reiterated as takeaways the team can reference after the visiting SRE leaves.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The artefact

At the end of an [[embedding-sre|embedded engagement]], the visiting SRE's final task is to write an after-action report. Chapter 30's framing (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> This report should reiterate your perspective, examples, and explanation. It should also provide some action items for the team to ensure they exercise what you've taught them. You can organize the report as a postvitam, explaining the critical decisions at each step that led to success.

The footnote makes the naming intentional: *in contrast to a postmortem*. A postmortem explains why something broke; a postvitam explains why something worked.

## What goes in it

Three elements (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

- **Perspective.** Why the team's practices are (were) problematic; what good looks like; the reasoning that connects practices to outcomes. This is the durable version of the reasoning the embedded SRE has been verbalising throughout Phase 3.
- **Examples and explanation.** Concrete cases encountered during the engagement, with the reasoning the visiting SRE applied. The postvitam is where the chapter's *explain your reasoning* discipline is recorded in written form so it survives the handoff.
- **Action items.** Work for the team to exercise the principles after the engagement ends. The action items mirror the Phase 3 *get help clearing kindling* pattern — specific, attributable, and reviewable — extended across the months after the visit.

## Why the name matters

Chapter 30 is careful about what kind of document this is. A postmortem is a *failure* document; using the same word for the exit report would signal that the engagement ended badly. A postvitam is a *success* document: the engagement achieved its goal, the team has been pointed in the right direction, and the report captures the decisions that got them there.

The naming also reinforces Chapter 30's broader framing that **team health is a process**, not a project. A postvitam is a milestone in that process, not its conclusion. The embedded SRE remains available for design and code reviews and *should keep an eye on the team for the next few months* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md) — the postvitam sets the baseline the follow-up observes.

## Relationship to other SRE written artefacts

The SRE book names several kinds of written documents with distinct purposes; the postvitam fills a specific niche:

| Artefact | Purpose | Trigger |
|---|---|---|
| [[blameless-postmortem]] | Root-cause + action items for a specific incident | Incident |
| [[postmortem-template|postmortem template]] | Structured format for the above | Template |
| [[on-call-playbook]] | Repeatable troubleshooting steps ahead of incidents | Preparation |
| [[on-call-learning-checklist]] | What a new on-caller needs to learn | Onboarding |
| **Postvitam** | **Perspective + reasoning + action items after an embedded engagement** | **End of engagement** |
| [[live-incident-state-document]] | Real-time shared state during an incident | In-flight incident |

The postvitam's distinctive property: it is **prospective**. Unlike a postmortem, it isn't about a past event — it's about the ongoing work the team needs to do after the visitor is gone. The *postvitam* name emphasises that the life of the intervention continues after the author's departure.

## Related pages

- [[embedding-sre]]
- [[identifying-kindling]]
- [[blameless-postmortem]]
- [[postmortem-philosophy]]
- [[on-call-playbook]]
- [[explaining-reasoning]]
- [[leading-questions]]
