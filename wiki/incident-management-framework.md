# Incident Management Framework

**Summary**: Chapter 14's hub topic — Google's structured approach to running a production incident, derived from the US National Incident Management System / Incident Command System. The framework's argument is that without explicit structure, well-meaning engineers will hurt the response by focusing too narrowly, communicating poorly, and freelancing fixes; with a defined set of roles, a recognised command post, a living incident document, and a clear handoff protocol, the same engineers compound their effort.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## Why a framework

Chapter 14 opens with a portrait of an unmanaged incident in which everybody is doing their job as they see it, and the response spirals out of control anyway (source: chapter-14-managing-incidents.md). The named failure modes in the opening case are catalogued at [[unmanaged-incident-anti-patterns]]:

- Sharp focus on the technical problem (no bandwidth for the bigger picture)
- Poor communication (nobody knows what anyone else is doing)
- Freelancing (uncoordinated changes that worsen the situation)

The framework's purpose is to *channel the energies of enthusiastic individuals* — turn the same people into a coordinated response without removing their autonomy.

## The five elements

Chapter 14 describes a well-designed incident management process as having the following features (source: chapter-14-managing-incidents.md):

1. **[[recursive-separation-of-responsibilities]]** — clear, delegable roles so nobody strays onto another's turf and the leader can subdivide work as scale demands.
2. **Named roles**: [[incident-commander]], [[incident-ops-lead]], [[incident-communications-lead]], [[incident-planning-lead]] — each delegable, each with a specific mandate.
3. **[[recognized-command-post]]** — a known place (war room, IRC channel) where interested parties can find the incident commander.
4. **[[live-incident-state-document]]** — a concurrently editable document the IC keeps as the source of truth on incident state.
5. **[[incident-handoff]]** — explicit verbal handoff of the IC role between shifts, communicated to the rest of the response team.

Together these are Google's adaptation of the [[incident-command-system|Incident Command System]] (ICS), known for its clarity and scalability.

## When the framework applies

A separate page covers [[declaring-an-incident|when to declare an incident]] — Chapter 14's three-question test (second team needed? customer-visible? unsolved after an hour?) and the bias toward declaring early. The framework applies once an incident is declared.

Chapter 14 also recommends using the same framework for **planned operational changes** that span time zones or teams, so engineers stay fluent in it. Incident management proficiency atrophies quickly when not in constant use; routine application during disaster-recovery testing and large rollouts is the antidote.

## A managed incident illustrated

Chapter 14 contrasts the unmanaged opening case with a parallel narrative of the same incident handled with the framework. The arc:

- **Mary recognises rapid growth** in the issue and asks **Sabrina** to take command. (Recognising overload early is itself a learnable skill.)
- **Sabrina** captures state in an email to a prearranged mailing list and a [[live-incident-state-document|live document]], asks an external communications representative to draft user messaging, and pulls in **Josephine** (developer on-call) and **Robin** (volunteer help) — but only after Mary's approval.
- The team uses **IRC** as the [[recognized-command-post|command post]]; updates flow through the document and the email thread, keeping VPs informed without bogging them down.
- At 5pm Sabrina starts arranging the **handoff** to a sister office; a 5:45 phone conference brings the new shift up to speed; at 6pm responsibilities transfer.
- Mary returns the next morning to find the problem mitigated, the incident closed, and postmortem work underway.

The point is not that the technical fix was faster — the technical work proceeds at the speed it always would. The framework saves the *coordination cost* that would otherwise consume the team's attention.

## Best practices

Chapter 14's closing list (source: chapter-14-managing-incidents.md):

- **Prioritize.** Stop the bleeding, restore service, and preserve the evidence for root-causing.
- **Prepare.** Develop and document procedures in advance, in consultation with participants.
- **Trust.** Give full autonomy within the assigned role.
- **Introspect.** Notice your own emotional state; if panicky, ask for support.
- **Consider alternatives.** Periodically re-evaluate whether to keep going or change tack.
- **Practice.** Routine use makes the framework second nature.
- **Change it around.** Rotate roles between incidents so everyone is fluent in each.

These map cleanly onto material elsewhere in the wiki: prioritisation is [[triage-sre]] and [[emergency-response]]; preparation is [[on-call-playbook]] and disaster role-playing; trust is [[recursive-separation-of-responsibilities]]; introspection is [[incident-response-mindset]]; practice and rotation are the response to [[operational-underload]].

## Cross-book connection

- The framework is the operational scaffolding that makes the [[incident-response-mindset|cognitive prescription]] of Chapter 11 actually achievable: offloading coordination overhead to defined roles preserves the budget for deliberate System-2 thinking.
- It composes with [[triage-sre|Chapter 12's triage discipline]]: once roles are assigned, the Ops lead's first job is "fly the airplane" — divert, drop, disable, or freeze — before diving into root cause.
- The Ch 13 case studies are case studies in *applying* (or not applying, in the Ch 13 [[test-induced-emergency|MySQL case]]) the Chapter 14 framework.

## Related pages

- [[incident-command-system]]
- [[recursive-separation-of-responsibilities]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[recognized-command-post]]
- [[live-incident-state-document]]
- [[incident-handoff]]
- [[declaring-an-incident]]
- [[unmanaged-incident-anti-patterns]]
- [[emergency-response]]
- [[incident-response-mindset]]
- [[on-call-playbook]]
- [[triage-sre]]
- [[blameless-postmortem]]
