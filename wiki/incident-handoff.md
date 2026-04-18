# Incident Handoff

**Summary**: Chapter 14's protocol for transferring [[incident-commander|incident commander]] responsibility between shifts or locations. The handoff must be **explicit, verbal, and acknowledged** — and broadcast to the rest of the response team — so there is no ambiguity at any moment about who is leading the response.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## The protocol

> It's essential that the post of incident commander be clearly handed off at the end of the working day. If you're handing off command to someone at another location, you can simply and safely update the new incident commander over the phone or a video call. Once the new incident commander is fully apprised, the outgoing commander should be explicit in their handoff, specifically stating, "You're now the incident commander, okay?", and should not leave the call until receiving firm acknowledgment of handoff. The handoff should be communicated to others working on the incident so that it's clear who is leading the incident management efforts at all times. (source: chapter-14-managing-incidents.md)

The protocol's six parts:

1. **Brief** — the outgoing IC walks the incoming IC through the [[live-incident-state-document|live incident document]] and the current state.
2. **Confirm full apprisal** — the incoming IC has had their questions answered and understands the incident.
3. **Explicit verbal transfer** — the outgoing IC says, *literally*, "You're now the incident commander, okay?"
4. **Firm acknowledgment** — the incoming IC confirms.
5. **The outgoing IC stays on the call until acknowledgment** — no quiet drift.
6. **Broadcast to the response team** — everyone working the incident learns who is now in charge.

The form is rigid because the cost of getting it wrong is severe: an incident with no commander is one in which decisions don't get made, communication stops, and the response degrades.

## Why the explicit verbalisation

The "You're now the incident commander, okay?" sentence sounds awkwardly formal. It is — deliberately. Chapter 14 borrows this discipline from aviation cockpit handoffs, where the same protocol exists (the call is "your aircraft" / "my aircraft") for the same reason: in stressful, multi-person operations, **assumed transitions fail**. Explicit, ceremonial transitions don't.

The broadcast step matters for the same reason. If the outgoing IC tells only the new IC, then the response team may continue routing questions to the wrong person, who may not realise they're being asked because they think they've handed off.

## Follow-the-sun handoffs

Chapter 14's managed-incident narrative shows the handoff used in its most common scenario: **end-of-day transfer to a sister office in another time zone**. The pattern:

- Around 5pm local, the outgoing IC starts arranging replacement staff.
- A brief phone conference (5:45pm in the example) brings the incoming team up to speed.
- At 6pm local, responsibilities transfer with the explicit-verbal protocol.

This composes naturally with [[multi-site-on-call|multi-site rotations]]: the same time-zone structure that prevents night shifts in normal on-call also enables clean incident handoffs for major outages. A solo-site team would have to choose between waking somebody up or running the incident through their own night.

## Mid-day handoffs

Handoffs aren't only end-of-day. The IC role can transfer:

- When the original IC is overloaded and someone better-positioned takes over.
- When the original IC needs to step away for any reason.
- When the incident escalates and requires a more senior or more experienced commander.

The protocol is the same.

## Cross-book connection

- The protocol is structurally a **two-phase commit**: the incoming IC must explicitly accept before the outgoing IC commits to the transfer, and the broadcast to the team is the announcement of the committed state.
- The aviation analogy continues the [[triage-sre|fly-the-airplane-first]] cross-domain borrowing pattern Chapter 14 favours.

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[live-incident-state-document]]
- [[recognized-command-post]]
- [[multi-site-on-call]]
