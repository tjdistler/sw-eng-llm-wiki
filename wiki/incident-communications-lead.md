# Incident Communications Lead

**Summary**: The public face of the response in Chapter 14's [[incident-management-framework]]. The comms lead issues periodic updates to the response team and stakeholders, and may extend to keeping the [[live-incident-state-document]] accurate and up to date. The role exists so that the [[incident-ops-lead|ops lead]] never has to choose between fixing the system and writing status emails.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## What the comms lead does

> This person is the public face of the incident response task force. Their duties most definitely include issuing periodic updates to the incident response team and stakeholders (usually via email), and may extend to tasks such as keeping the incident document accurate and up to date. (source: chapter-14-managing-incidents.md)

Concrete duties Chapter 14's managed-incident narrative shows the role doing:

- Sending an initial email to a **prearranged mailing list** as soon as command is taken, summarising what's happened so far.
- Following up to the same email thread when significant events occur — keeping VPs and other stakeholders abreast at the **right level of detail** (high-level status, no minutiae).
- Recording statements from the [[incident-ops-lead|ops lead]] (e.g. "users have yet to be impacted; let's just hope we don't lose a third datacenter") in the live incident document.
- Pulling in an **external communications representative** to draft user-facing messaging, when the incident is large enough to warrant it.

## Why this needs to be a dedicated role

Chapter 14's opening unmanaged-incident case study illustrates the failure mode: when nobody owns communication, two things happen at once:

- **The on-call engineer is interrupted constantly** by VPs demanding ETAs and by colleagues asking what's going on. Their cognitive budget for the technical problem evaporates (source: chapter-14-managing-incidents.md, Sharp Focus on the Technical Problem section).
- **The information that does reach stakeholders is uncoordinated** — different people hear different things from different sources, which makes the situation feel worse than it is and triggers escalations that further interrupt the response.

Naming a comms lead solves both problems with one move: stakeholders learn they have one source to ask, and that source produces a steady stream of updates so they don't have to ask.

## Audiences

In the chapter's managed narrative, the comms lead is implicitly serving multiple audiences with different needs:

- **The response team** itself — IRC chatter, incident-document updates.
- **Internal stakeholders** (VPs, sister teams, management) — periodic emails on the prearranged mailing list.
- **External communications staff** (PR, support) — handed off the user-messaging draft work; the response team does not typically write the user-facing status post itself.

The art is matching the *level of detail* to the audience. VPs do not need to know which binary is being rolled back; they need to know the impact, the trajectory, and whether help is needed.

## In the IC's absence

If communications hasn't been delegated, the IC holds it (per the [[recursive-separation-of-responsibilities|hold-everything-not-delegated]] default). For a small incident this is fine; for a large one, the IC's coordination work and the comms work compete for attention, and one or both suffer.

## Cross-book connection

- The role is the human form of a [[unified-monitoring-interface|fan-out broadcast]]: one source, many consumers, with structured periodicity.
- Audience-appropriate updates are a specific case of [[architecture-presentation|the presenter's audience-fit problem]].

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-planning-lead]]
- [[live-incident-state-document]]
- [[recursive-separation-of-responsibilities]]
