# Launch Checklist

**Summary**: The central artifact of [[launch-coordination-engineering|LCE]]: a curated catalogue of questions to ask about any product launch, with concrete action items and pointers to shared infrastructure. Inspired by aviation preflight and surgical checklists (Gawande's *Checklist Manifesto*). Every entry's importance must be substantiated by a previous launch disaster; every instruction must be concrete, practical, and reasonable to accomplish. Curated continuously, with a full review once or twice a year.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## What the checklist is for

Checklists reduce failure and ensure consistency and completeness across disciplines — aviation preflight and surgical checklists are the canonical examples the chapter cites (source: chapter-27-reliable-product-launches-at-scale.md). LCE applies the same idea to launch qualification: the checklist helps an LCE assess the launch and provides the launching team with action items and pointers to more information.

## Shape of an entry

Each checklist item pairs a question with an action item and (ideally) a pointer to shared infrastructure. Examples from the chapter (source: chapter-27-reliable-product-launches-at-scale.md):

> Question: Do you need a new domain name?
> Action item: Coordinate with marketing on your desired domain name, and request registration of the domain. Here is a link to the marketing form.

> Question: Are you storing persistent data?
> Action item: Make sure you implement backups. Here are instructions for implementing backups.

> Question: Could a user potentially abuse your service?
> Action item: Implement rate limiting and quotas. Use the following shared service.

The concreteness is deliberate. A question that prompts open-ended deliberation rather than a specific action wastes the checklist's tight format.

## Curation discipline

Left uncurated, the checklist grows without bound. At one point, adding a new question required VP approval (source: chapter-27-reliable-product-launches-at-scale.md). LCE's current guidelines:

- **Every question's importance must be substantiated, ideally by a previous launch disaster.** The checklist is not a theoretical exercise in completeness; it's a record of failures worth preventing.
- **Every instruction must be concrete, practical, and reasonable to accomplish.**

And the ongoing curation rhythm:

- Small updates continuously as team members notice items needing modification
- A full end-to-end review once or twice a year, coordinated with service owners and subject-matter experts

The rationale: recommendations change over time, internal systems get replaced, and areas of concern become obsolete under new policies. Treat the checklist as a living document, not a static artifact.

## Why developers tolerate it

The checklist is part of the process that engineers might sidestep if it feels too burdensome. LCE's continuous optimisation of the cost/benefit balance is deliberate — the chapter's broader point is that a checklist developers dodge is worse than no checklist. Mechanisms that make the checklist tolerable:

- **Fast paths for low-risk launches** — launches with no new server executables and <10% traffic increase get a nearly trivial checklist
- **Standardised infrastructure** — "Implement rate limiting using system X" replaces pages of rate-limiting requirements
- **Concrete pointers** — the action items tell developers exactly what to do, not that something must be done

## The checklist as convergence vehicle

Because almost every launch flows through the checklist, LCE uses it as a **driving convergence on common infrastructure** instrument. Instead of implementing a custom solution, LCE can recommend hardened existing infrastructure as building blocks. This collapses checklist items ("here are ten requirements to satisfy") into single lines ("use X") while also spreading known-good solutions across the company.

## Novel-territory launches

When a launch enters a new product vertical (mobile, hardware, consumer devices) the existing checklist may not apply. LCE's discipline is to **synthesise the new checklist from first principles** (source: chapter-27-reliable-product-launches-at-scale.md) — structure around broad themes such as reliability, failure modes, and processes, then engage domain experts to determine which existing sections translate. It's important to keep the *intent* of each existing question in mind rather than applying the wording mindlessly.

## Themes covered

The checklist's themes (detailed in [[launch-checklist-themes]]):

- Architecture and dependencies
- Integration with internal ecosystem
- Capacity planning
- Failure modes
- Client behavior
- Processes and automation
- Development process (version control, releases)
- External dependencies
- Rollout planning

## Industry parallel

The *Checklist Manifesto* discipline translates from surgery to SRE, but it's worth naming the difference: the checklist isn't a [[architecture-fitness-function|fitness function]] — it can't be automated, and it depends on human judgment for each answer. The items a checklist captures are precisely the things that can't yet be automated. See [[architectural-checklists]] for Richards & Ford's framing of what makes a good checklist candidate (infrequent, non-procedural, error-prone work) — LCE's launch checklist fits that frame.

## Related pages

- [[launch-coordination-engineering]]
- [[launch-checklist-themes]]
- [[reliable-product-launches]]
- [[architectural-checklists]]
- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[site-reliability-engineering]]
