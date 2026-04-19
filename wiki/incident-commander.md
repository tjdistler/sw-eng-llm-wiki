# Incident Commander

**Summary**: The apex role in Chapter 14's [[incident-management-framework]]. The IC holds the high-level state of the incident, structures the response task force, and assigns responsibilities. By default the IC holds every role they have not yet delegated — so the position scales gracefully from a one-person early response to a multi-team escalated response.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## What the IC does

> The incident commander holds the high-level state about the incident. They structure the incident response task force, assigning responsibilities according to need and priority. (source: chapter-14-managing-incidents.md)

The IC's job is **coordination**, not technical fixing. In the Chapter 14 managed-incident narrative, Sabrina (the IC) doesn't write any code or change any production state — she captures status, sends emails, decides whether to page the developer on-call, organises the handoff. Mary (the on-call engineer who started the response) hands command off and stays focused on the technical work as the [[incident-ops-lead|ops lead]].

This separation matters because the technical lead is the most likely person to become cognitively saturated by the problem itself, leaving no bandwidth for the bigger picture (source: chapter-14-managing-incidents.md, Sharp Focus on the Technical Problem section).

## Default: IC holds everything not delegated

> De facto, the commander holds all positions that they have not delegated. (source: chapter-14-managing-incidents.md)

In a small incident, the IC is also the ops lead, the comms lead, and the planning lead — there's no need to subdivide. As the incident grows, the IC delegates each role to a specific person, and the framework scales without changing shape. See [[recursive-separation-of-responsibilities]].

The IC also has the authority to **remove roadblocks** that prevent Ops from working most effectively (source: chapter-14-managing-incidents.md). This is the political part of the role: clearing approvals, pulling in additional teams, talking down anxious VPs.

## Other duties

- **Maintain the [[live-incident-state-document]]**: Chapter 14 calls this the IC's *most important responsibility*.
- **Authorise external action**: in the Chapter 14 narrative, Sabrina checks with Mary before pulling in Josephine (the developer on-call) — the IC controls who joins the response.
- **Manage the [[incident-handoff]]**: explicit, verbal, with firm acknowledgment.

## Who can be IC

Chapter 14 doesn't restrict the role by seniority. In the managed-incident narrative, Mary (on-call) asks Sabrina (a peer) to take command. The implicit rule: anyone with operational fluency and the willingness to coordinate can be IC; the role moves to whoever is best positioned to hold the high-level state.

The Chapter 14 best practices include "**Change it around** — Were you incident commander last time? Take on a different role this time." Rotation is a deliberate part of the practice; everyone should be familiar with each role.

## Cross-book connection

- The IC role is the human-side analogue of an orchestrator in workflow systems: a single point that holds state about a multi-step distributed process and dispatches work to participants.
- Pulling-people-in-when-overwhelmed is the explicit form of escalation that [[incident-response-mindset]] argues for as a structural pressure-relief valve.

## Related pages

- [[incident-management-framework]]
- [[recursive-separation-of-responsibilities]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[live-incident-state-document]]
- [[incident-handoff]]
- [[incident-response-mindset]]
