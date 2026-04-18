# Postmortem Review Process

**Summary**: A written postmortem is only half the work. Chapter 15 insists that every postmortem must go through a **formal review by senior engineers**, get its action items closed out, and then be **broadcast to the widest possible audience**. The named best practice — *no postmortem left unreviewed* — is the discipline that turns postmortems from private notes into organisational memory.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## The pipeline

Chapter 15 describes the review workflow as three phases (source: chapter-15-postmortem-culture-learning-from-failure.md):

1. **Draft + internal senior-engineer review** — the authoring team shares the first draft internally and pulls in a group of senior engineers to assess it.
2. **Review-session close-out** — a scheduled review meeting where ongoing comments are resolved, ideas are captured, and the document is finalised.
3. **Broad publication** — shared with the larger engineering team or internal mailing list; added to the team or organisation **repository of past incidents**.

The discipline here is that none of the three phases is optional. A postmortem that stalled in phase 1 — sitting in a Google Doc with unresolved comments — never makes it into the institutional memory and so never delivers the learning value it was supposed to.

## Review criteria

Chapter 15 suggests five questions senior engineers should ask of a draft (source: chapter-15-postmortem-culture-learning-from-failure.md):

- **Was key incident data collected for posterity?** Timestamps, scopes, affected services, detection mechanism — the facts that allow future readers to reconstruct what happened.
- **Are the impact assessments complete?** All affected users, all affected systems, all downstream consequences. Partial impact assessments miss follow-up actions.
- **Was the root cause sufficiently deep?** The anti-pattern is stopping at the first plausible cause; good postmortems probe deeper, find the conditions that made the proximate cause reachable, and capture the **contributing** factors rather than a single scapegoat cause.
- **Is the action plan appropriate and are resulting bug fixes at appropriate priority?** Action items tagged P4 that nobody will ever get to are the visible sign of postmortem-theatre.
- **Did we share the outcome with relevant stakeholders?** The authoring team has specific knowledge; propagating it requires identifying and informing the broader audience.

These are the questions that make the postmortem useful as opposed to merely complete.

## The root-cause-depth question

The third criterion ("was the root cause sufficiently deep?") deserves separate mention. Chapter 15 doesn't prescribe a specific technique — the chapter refers readers to Rooney's survey [Roo04] — but it does insist on **all contributing root cause(s)** (plural) (source: chapter-15-postmortem-culture-learning-from-failure.md). This is consistent with the [[blameless-postmortem]] framing that systems have multiple contributing causes, not a single root cause, and with the Chapter 12 [[hypothetico-deductive-debugging]] position that definitive proof of causation is often impossible in complex distributed systems.

Practical versions of "sufficiently deep" include: five-whys, Ishikawa/fishbone diagrams, causal chain diagrams, and systemic-factors analyses. The team picks what fits; the reviewer's job is to push back when the chain stops too early.

## Best practice: no postmortem left unreviewed

Chapter 15 names this as an explicit best practice (source: chapter-15-postmortem-culture-learning-from-failure.md):

> An unreviewed postmortem might as well never have existed.

The remedy it prescribes is **regular review sessions** — meetings scheduled specifically to close out pending postmortems. These meetings:

- Close ongoing discussions and comments.
- Capture ideas that didn't make it into the draft.
- Finalise the document state.
- Add it to the team or organisation repository.

The structure matters because without scheduled meetings, postmortems drift into the "almost done" pile indefinitely. A standing slot on the team calendar forces closure.

## Transparent sharing

Chapter 15 (source: chapter-15-postmortem-culture-learning-from-failure.md):

> Our goal is to share postmortems to the widest possible audience that would benefit from the knowledge or lessons imparted.

The default should be the broadest plausible audience. The chapter notes two constraints:

- **Privacy.** Google's rules around user-identifying information apply even in internal postmortems — nothing identifying goes in the document, regardless of audience.
- **Noise.** The widest-possible-audience rule has to be balanced against signal-to-noise for readers; that's why [[postmortem-culture-activities|postmortem of the month]] exists as the curation layer on top.

## Follow-up accountability

The review process captures the action plan, but Chapter 15's broader culture arguments demand that the actions **actually land**. Chapter 13's [[learning-from-outages]] page captures this: an incident is not closed when the service recovers; it is closed when the follow-up actions land. The review meeting is where incomplete action items from previous postmortems can be surfaced and escalated.

## Repository and retrieval

Chapter 15 refers to **a repository of past incidents** as the destination for reviewed postmortems. Morgue (Etsy, open-sourced) is the tool the chapter names; Google has an internal equivalent. The repository makes past postmortems **findable** — which is a precondition for reading clubs ([[postmortem-culture-activities]]), trend analysis ([[postmortems-at-google-working-group]]), and Wheel of Misfortune replays ([[on-call-playbook]]).

## Cross-book connection

The review-and-broadcast discipline is the operational counterpart to [[architecture-decision-record|ADRs]]: a structured record whose value depends on it being findable and reviewed, not just written.

## Related pages

- [[postmortem-philosophy]]
- [[blameless-postmortem]]
- [[postmortem-template]]
- [[postmortem-culture-activities]]
- [[postmortems-at-google-working-group]]
- [[learning-from-outages]]
