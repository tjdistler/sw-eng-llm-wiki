# Postmortem Template

**Summary**: Google uses an in-house postmortem template (Appendix D in the book) implemented as a Google Doc — real-time-collaborative, annotation-friendly, with email notifications for crowdsourcing input. Chapter 15's requirements for the tool matter more than the specific choice: any tool that supports these workflows works.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## Required capabilities

Chapter 15 lists three features any postmortem tool must have (source: chapter-15-postmortem-culture-learning-from-failure.md):

- **Real-time collaboration.** Enables rapid collection of data and ideas during the early creation of the postmortem, when multiple responders are still offloading their memory of what happened.
- **An open commenting/annotation system.** Makes crowdsourcing solutions easy and improves coverage — engineers who weren't in the incident can contribute observations and suggestions.
- **Email notifications.** Directed at collaborators within the document, or used to loop in others for input.

These requirements drive Google's choice of Google Docs for the template. Any tool (wiki, specialised postmortem system, purpose-built tool) that supports the three requirements is acceptable.

## The in-house template (Appendix D)

The chapter references Appendix D for the actual template. Chapter 15's own description of it is terse, but the implicit shape that emerges from the chapter and from the [[postmortem-review-process|review criteria]] is:

- **Incident data** — timestamps, services affected, duration, detection mechanism
- **Impact assessment** — user impact, SLI/SLO consumption, data loss or none
- **Root cause(s)** — with depth: not just what failed but why the conditions for failure were reachable
- **Timeline** — often derived from the [[live-incident-state-document|live incident document]] and [[recognized-command-post|command-post chat log]]
- **Response** — what was tried, what worked, what didn't (including [[negative-results|negative results]])
- **Action plan** — follow-up items with appropriate priority and owners
- **Lessons learned** — the "what should we do differently" section

## The tool as raw material pipeline

A key property Chapter 15 emphasises: postmortem creation should be **built on top of existing incident artefacts**. The live incident document ([[live-incident-state-document]]) already captured most of the raw material during the response; a good postmortem template **incorporates that material directly** rather than asking the author to reconstruct it.

Chapter 15's closing section on the [[postmortems-at-google-working-group|Postmortems at Google working group]] makes this explicit: the group is working on *automating postmortem creation with data from tools used during an incident*. The template is the destination for that data.

## Metadata for trend analysis

Chapter 15 notes that the template has recently been **enhanced with additional metadata fields** to facilitate comprehension and automated analysis (source: chapter-15-postmortem-culture-learning-from-failure.md). Specific fields aren't listed, but the purpose is:

- Identify **common themes** across product boundaries (YouTube, Gmail, Google Cloud, AdWords, Google Maps — all of which share the same postmortem practice).
- Enable machine-learning-based **prediction of weaknesses**.
- Support **real-time incident investigation** by pattern-matching against past incidents.
- **Reduce duplicate incidents** by detecting when a new postmortem looks structurally like a past one.

This pushes the postmortem template in the direction of a structured database record rather than just a prose document — metadata fields are load-bearing once aggregation matters.

## Privacy discipline

Chapter 15 notes that Google has stringent rules around user-identifying information, and **even internal documents like postmortems never include such information** (source: chapter-15-postmortem-culture-learning-from-failure.md). The template should not make it easy to paste a raw log that contains user data; sanitisation is part of the authoring discipline.

## Morgue and related tools

Chapter 15 mentions that **Etsy has released Morgue**, a tool for managing postmortems, for teams wanting to start their own repository (source: chapter-15-postmortem-culture-learning-from-failure.md, footnote 2). Morgue is specifically a **repository** — the structured store that sits under the template, storing past postmortems in a searchable way. The template produces entries; the repository preserves them for [[postmortem-review-process|review]] and [[postmortem-culture-activities|reading clubs]].

## Related pages

- [[postmortem-philosophy]]
- [[postmortem-review-process]]
- [[blameless-postmortem]]
- [[live-incident-state-document]]
- [[recognized-command-post]]
- [[postmortems-at-google-working-group]]
- [[postmortem-culture-activities]]
