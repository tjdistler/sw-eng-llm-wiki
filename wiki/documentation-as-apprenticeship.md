# Documentation as Apprenticeship

**Summary**: Chapter 28's practice of assigning documentation overhaul to newbies — specifically, overhauling outdated sections of the on-call learning checklist. This exploits the asymmetry that senior SREs don't need up-to-date docs (they carry state in their heads) while newbies do, making newbies the natural maintainers. The exercise builds senior-newbie trust bidirectionally.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The asymmetry

Chapter 28's observation (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> In a rapidly changing environment, documentation can fall out of date quickly. Outdated documentation is less of a problem for senior SREs who are already up to speed, because they keep state on the world and its changes in their own heads. Newbie SREs are much more in need of up-to-date documentation, but may not feel empowered or knowledgeable enough to make changes.

This is a classic principal-agent problem: the people who most need good docs have the least authority to fix them; the people with the authority don't need the docs. Chapter 28's solution is to grant authority to the people with the need, and scaffold it with senior review.

## The Search SRE practice

The Google Search SRE team's routine (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

1. In anticipation of a new team member's arrival, senior SREs **review the [[on-call-learning-checklist|on-call learning checklist]]** and **sort sections by how out-of-date they are**
2. The new team member is pointed at the overall checklist
3. They are **tasked with overhauling one or two of the most outdated sections**
4. The checklist lists senior SRE and developer contacts for each technology — the newbie **makes an early connection** with the relevant subject-matter experts
5. As they become familiar with the scope and tone of the checklist, they **contribute a revised section**
6. The revision is **peer-reviewed by one or more senior SREs** listed as experts

Every step is intentional. The experts are named so the newbie knows who to ask; the review is by-role so the feedback is authoritative; the output is a concrete artefact the newbie can point to.

## The three audiences revisited

Documentation-as-apprenticeship works because the [[on-call-learning-checklist|on-call learning checklist]] already has three distinct audiences with three distinct uses:

- **Student** — establishes boundaries of the system; signals what matters
- **Mentors and managers** — tracks progress: *what sections are you working on? what is most confusing?*
- **Team** — a social contract: mastery of the checklist = qualification for on-call

When a newbie overhauls a section, the artefact serves all three audiences simultaneously: it documents the current system for future students, demonstrates the newbie's progress to mentors, and contributes back to the team's shared standard.

## Bidirectional trust building

The Chapter 28 theme recurs here: activities should "benefit everyone's education." Documentation overhaul is one of the chapter's purest examples because the flow of learning is genuinely bidirectional (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- The **newbie** learns the technology by having to explain it in writing
- The **subject-matter expert** is forced to articulate knowledge they have been carrying informally — which surfaces their own assumptions and gaps
- The **peer reviewer** re-reads their own area with fresh eyes because the newbie's draft may raise questions the expert hadn't considered

The outcome is not just better docs — it is a team whose informal knowledge is being continuously externalised by the onboarding process.

## The senior-carries-state-in-head pathology

Chapter 28's framing hints at a failure mode it doesn't name explicitly: a team where all knowledge lives in the heads of senior SREs is fragile to their departure, promotion, or even their being on vacation when a new incident strikes. [[learning-from-outages|Chapter 13]]'s *"could the person sitting next to you do the same?"* question is the cultural prompt that makes this pathology visible; documentation-as-apprenticeship is the ongoing mechanism that keeps the pathology at bay.

A team that doesn't do this will discover its knowledge gaps only during incidents. A team that does will discover them during onboarding, when there is time to fix them without production pressure.

## Design requirements for the checklist

For this practice to work, the checklist itself must be designed to support overhaul-by-newbies. Chapter 28's implicit requirements:

- **Section-level modularity** — a newbie can overhaul one section without understanding the whole document
- **Named experts per section** — the newbie knows who to talk to
- **Tone and scope examples** — previous sections show what "done well" looks like
- **Peer-review workflow** — changes are formally accepted rather than merged directly

These requirements are unusual for documentation. Most doc systems don't list experts or enforce review. Chapter 28's practice essentially treats the checklist as code: it's a living repository with ownership, review, and change management.

## Relationship to the broader onboarding arc

In Chapter 28's blueprint (Figure 28-1), documentation overhaul appears **after** system-fundamentals work and **before** [[shadow-on-call|shadow on-call]]. The ordering makes sense:

- The newbie needs enough fundamentals to have something to document
- The overhaul exercise demonstrates that they can articulate the system — a prerequisite for shadowing a real incident

Completing a section is often a milestone toward going on-call, alongside the rest of the [[cumulative-learning-paths|learning path]] and the [[targeted-project-work|starter project]].

## Related pages

- [[sre-onboarding]]
- [[on-call-learning-checklist]]
- [[cumulative-learning-paths]]
- [[shadow-on-call]]
- [[learning-from-outages]]
- [[on-call-playbook]]
