# On-Call Learning Checklist

**Summary**: The document artifact that encodes an SRE team's onboarding curriculum — an organised reading and comprehension list of the technologies and concepts a student must internalise before shadow-on-call. Chapter 28 presents it as the backbone of the team's apprenticeship system, carrying different meaning for students, mentors, and the team as a whole.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## What it is

Chapter 28 describes the checklist as "an organised reading and comprehension list of the technologies and concepts relevant to the system(s) they maintain" (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). It is a team-maintained living document; the Google Search SRE team's version is the running example in the chapter.

A simplified section of such a checklist **enumerates**:

- **Expert contacts** — the senior SREs and developers to reach out to for each area
- **Key documentation resources** — where authoritative information lives
- **Basic knowledge to internalise** — the core facts and mental models
- **Probing questions** — generative questions that can only be answered after the basic knowledge is absorbed
- **Concrete outcomes** — what the student should know or be able to do after completing the section

## What it deliberately does *not* contain

Chapter 28 is explicit: the checklist does not encode procedures, diagnostic steps, or playbooks (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Those age quickly; duplicating them in the checklist creates a maintenance burden and a drift problem.

Instead the checklist is "relatively future-proof" because it points at the authoritative sources rather than copying them. Procedures live in the [[on-call-playbook|playbook]]; diagnostic steps live in runbooks; the checklist just tells the student where to look and what to understand.

## Three audiences, three purposes

Chapter 28 lists the distinct uses the checklist serves (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

### To the student

- Establishes the **boundaries** of the system the team supports
- Shows which systems are most important and why, so the student knows what to dwell on and what to defer

### To mentors and managers

- A shared surface for tracking progress: *what sections are you working on today? what sections are the most confusing?*
- Early signal on where the student is struggling

### To all team members

- A **social contract**: mastering the checklist qualifies the student to join the on-call ranks
- Sets the standard that all team members should aspire to and uphold — the senior SREs are implicitly held to the same bar

## The newbie-overhaul dynamic

Chapter 28 uses the checklist as an instrument for keeping senior knowledge fresh. The Search SRE team's practice (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- When a new team member is arriving, senior SREs review the checklist and **sort sections by how out-of-date they are**
- The newbie is pointed at the overall checklist *and* tasked with overhauling one or two of the most outdated sections
- The newbie makes early contact with the listed subject-matter experts to learn inner workings
- Their revised section is then peer-reviewed by the listed senior SREs

This is a bidirectional flow: the newbie learns the system (from the expert), and the senior expert is forced to revisit a piece of the system they probably haven't thought about in a while. Senior SREs keep state on the system in their own heads, so stale documentation doesn't bother them; newbies, lacking that state, are the best customers for up-to-date docs and therefore the best authors of them. See [[documentation-as-apprenticeship]].

## The tiered-access pairing

The checklist typically pairs with a **tiered access model**: completing sections satisfactorily earns the student progressively deeper access to production systems. The Search team calls these levels *powerups* on the route to on-call (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). See [[cumulative-learning-paths]] for the full pattern.

## Homework and progression

Moving through the checklist requires demonstrating understanding, not just reading. Chapter 28 recommends informal homework — probing questions the student answers in writing, reviewed by a mentor. Example questions from the chapter:

- Which backends of this server are in the critical path, and why?
- What aspects of this server could be simplified or automated?
- Where is the first bottleneck? What would you do to alleviate it if saturated?

Satisfactory answers signal that learning should continue to the next phase.

## Relationship to the milestone

Chapter 28 closes by noting that **completion of the on-call learning checklist is one of the typical evidences of readiness** for on-call. Some teams use a separate final exam; many use the checklist itself as the gate (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Either way, going on-call is a rite of passage that should be celebrated as a team — and the checklist is what the celebration acknowledges was completed.

## Related pages

- [[sre-onboarding]]
- [[cumulative-learning-paths]]
- [[documentation-as-apprenticeship]]
- [[shadow-on-call]]
- [[on-call-playbook]]
- [[targeted-project-work]]
