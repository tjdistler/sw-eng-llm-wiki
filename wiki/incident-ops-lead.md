# Incident Ops Lead

**Summary**: The hands-on technical role in Chapter 14's [[incident-management-framework]]. The Ops lead works with the [[incident-commander]] to apply operational tools to the incident. Critically, the operations team should be the *only* group modifying the system during an incident — this is the structural defence against the freelancing failure mode.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## What the Ops lead does

> The Ops lead works with the incident commander to respond to the incident by applying operational tools to the task at hand. The operations team should be the only group modifying the system during an incident. (source: chapter-14-managing-incidents.md)

This role does the actual debugging, mitigation, rollback, traffic shifting, and configuration changes. In the Chapter 14 managed-incident narrative, Mary stays in this role after handing command off to Sabrina — she's the one running the failed binary rollback and inspecting logs.

## The exclusivity rule

The most important property of the role: **only the operations team modifies the system during an incident**.

This rule exists to prevent the third [[unmanaged-incident-anti-patterns|unmanaged-incident anti-pattern]]: freelancing. In the chapter's opening case study, Malcolm — well-intentioned, technically capable — applies a CPU-affinity change without coordination, and it kills the remaining datacentres. The change might have worked under other circumstances; the failure was not the change but the *uncoordinated* change.

The exclusivity rule means:

- Volunteers who want to help (Robin in the managed-incident narrative) get directed to the IC, who decides whether to incorporate them into the response.
- Engineers who join the response are reminded to "prioritise any tasks delegated to them by Mary, and that they must keep Mary informed of any additional actions they take" (source: chapter-14-managing-incidents.md).
- People with bright ideas need to route them through Ops, not implement them directly.

This is the structural reason Chapter 14's "Trust" best-practice item works without producing chaos: trust is conferred *within an assigned role*, and the boundary between roles is bright.

## Delegation within Ops

When the incident is large enough, the Ops lead can delegate **system components** to colleagues. Each colleague effectively acts as Ops for their slice and reports rolled-up state back. This is the horizontal recursion described at [[recursive-separation-of-responsibilities]].

## Coordination with Comms and IC

The Ops lead doesn't write the status emails or update the live document directly — that's the [[incident-communications-lead|comms lead]]'s job (or the IC's, if comms hasn't been delegated). The Ops lead's role is to **report state up** so Comms can broadcast it and the IC can decide what to do next.

In the Chapter 14 narrative, Mary mutters her findings to Robin (the volunteer-now-helper); Robin updates IRC; Sabrina pastes the IRC update into the live incident document. The Ops lead is freed from the overhead of formatting and routing communications.

## Cross-book connection

- The exclusivity rule is the human-process analogue of [[idempotence|change serialisation]]: by routing all changes through one channel, the system stays reasoning-friendly.
- The structural similarity to [[change-management-sre|Google's change-management discipline]] is direct: both are about controlling who modifies production state, and when.

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[recursive-separation-of-responsibilities]]
- [[unmanaged-incident-anti-patterns]]
- [[triage-sre]]
- [[change-management-sre]]
