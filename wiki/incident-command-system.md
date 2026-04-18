# Incident Command System

**Summary**: The US emergency-management standard from which Google's [[incident-management-framework]] is adapted. Originally developed for coordinating multi-agency wildfire response, ICS provides a role-based, delegable, scalable structure that gracefully expands from a single responder to a multi-thousand-person operation. Chapter 14 cites it as the source of the framework's *clarity and scalability*.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`, `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## What ICS is

The Incident Command System is a component of the US National Incident Management System (NIMS), administered by FEMA (source: chapter-14-managing-incidents.md, citing http://www.fema.gov/national-incident-management-system). It evolved from FIRESCOPE, an inter-agency wildfire-response framework developed in California in the 1970s, and has since been generalised to all hazards.

ICS's organising principles map directly onto the elements Chapter 14 adopts:

- A single **Incident Commander** holds overall responsibility — see [[incident-commander]].
- Functional sections (Operations, Planning, Logistics, Finance/Administration in full ICS; Ops, Planning, Communications in Chapter 14's slimmer version) are delegable and themselves expandable into sub-units.
- A **modular, scalable** structure: the IC initially holds every position; positions are delegated only as the incident grows. See [[recursive-separation-of-responsibilities]].
- A **common terminology** so personnel from different organisations can plug in without retraining.
- A **manageable span of control** — a leader supervises 3–7 reports, with 5 as the target. (Chapter 14 doesn't quote this number but it is the structural reason the framework subdivides.)

## Why Google adopted it

Chapter 14 picks ICS specifically because it is *known for its clarity and scalability* (source: chapter-14-managing-incidents.md). The two properties matter for different reasons:

- **Clarity** — engineers under stress need an unambiguous answer to "what is my job right now?"; ICS's pre-defined roles deliver it. See [[incident-response-mindset]] for the cognitive-load argument.
- **Scalability** — a small incident may have one person filling every role; a major outage may need a dedicated IC, two ops leads, a comms lead, and a planning lead, each with a small staff under them. ICS handles both with the same vocabulary and the same delegation pattern, so escalation doesn't require a different framework.

## What Chapter 14 keeps and what it drops

Chapter 14's adaptation is pragmatic rather than literal. The kept ideas:

- Single incident commander as the apex authority.
- Delegable, named functional roles.
- A formal handoff protocol — see [[incident-handoff]].
- A recognised command post — see [[recognized-command-post]].

Things Chapter 14 doesn't adopt explicitly (full ICS includes Logistics, Finance/Administration, and a more elaborate organisational chart). The book's slimmer version reflects software-incident reality: there is no equipment to procure, no perimeter to secure, no public-safety jurisdiction. The roles that remain are the ones that produce value in a software outage.

## Cross-domain note

ICS is one of several cases in the SRE book where Google explicitly imports a discipline from outside software:

- Aviation crew resource management informs [[incident-response-mindset|stay-rational-under-pressure]] practices.
- Pilot training is the source of [[triage-sre|fly-the-airplane-first]].
- ICS is the source of the incident management framework.

The pattern: where another industry has decades of refined practice for managing high-stakes uncertainty under time pressure, borrow the practice rather than reinvent it. Chapter 33 generalises this borrow-the-practice instinct across the four SRE themes (preparedness/disaster-testing, postmortem culture, automation, structured decision-making); see [[lessons-from-other-industries]].

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[recursive-separation-of-responsibilities]]
- [[recognized-command-post]]
- [[incident-handoff]]
- [[incident-response-mindset]]
- [[triage-sre]]
- [[lessons-from-other-industries]]
