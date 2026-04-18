# Context Switch Cost

**Summary**: Chapter 29's named principle that an engineer's context switch is **not** free and must be priced in. A 20-minute interruption while working on a project involves two context switches, and realistically destroys a couple of hours of productive work — not 20 minutes. This is the arithmetic underlying every other piece of Chapter 29's interrupt-management advice.

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## The arithmetic

> In order to limit your distractibility, you should try to minimize context switches. Some interrupts are inevitable. However, viewing an engineer as an interruptible unit of work, whose context switches are free, is suboptimal if you want people to be happy and productive. Assign a cost to context switches. A 20-minute interruption while working on a project entails two context switches; realistically, this interruption results in a loss of a couple hours of truly productive work.

*(source: chapter-29-dealing-with-interrupts.md)*

The two context switches:

1. Out of the project work, into the interrupt.
2. Out of the interrupt, back into the project work.

Each switch costs time and [[cognitive-flow-state|flow]]. The second one is often the more expensive — re-establishing mental state in a code base or design problem can take substantially longer than the interrupt itself took to handle.

## Why 20 minutes costs two hours

Chapter 29 doesn't derive the "couple of hours" figure — it states it as received wisdom from engineering practice. The underlying mechanics:

- The [[cognitive-flow-state|flow state]] takes time to re-enter after disruption. The pre-interrupt mental stack is no longer warm.
- Short-term memory of the sub-problem being worked on may be lost and require re-derivation.
- Emotional state shifts out of deep focus; re-motivation is required.
- Follow-up thoughts from the interrupt continue to leak attention for a period after the interrupt itself ends.

The practical takeaway: optimising for **fewest interrupts**, not **shortest interrupts**, is usually the right move. Five 4-minute interrupts is worse than one 20-minute interrupt even though the raw interrupt time is the same.

## Distractibility

Chapter 29 enumerates the mechanisms by which an engineer who is not formally on interrupts becomes distractible anyway (source: chapter-29-dealing-with-interrupts.md). Using its running example of "Fred," who is not on-call or on interrupts today:

- Fred's team uses an automated ticket system that randomly assigns tickets to the team — a ticket gets assigned to him, due today.
- Fred's colleague is on-call and receives a page about a component Fred is expert in, and interrupts him to ask about it.
- A user raises the priority of a ticket assigned to Fred since last week (when he was on-call).
- A flag rollout assigned to Fred (rolling out over 3-4 weeks) goes wrong, and Fred has to drop everything.
- A user contacts Fred directly because Fred is helpful.

Some of these Fred can manage himself by closing email, turning off IM, using "do not disturb" headphones. Some are caused by **policy** or **assumptions about interrupts and ongoing responsibilities** — and no amount of personal discipline will remove those. This is the gap Chapter 29's team-level prescriptions are designed to close.

## The assumption Chapter 29 rejects

The bad assumption that Chapter 29 explicitly names and rejects:

> Viewing an engineer as an interruptible unit of work, whose context switches are free.

This model is seductive because it makes staffing math easy: aggregate interrupt-time / headcount = load per person. But it produces stressed-out, under-productive engineers, because the hidden cost of context switching doesn't appear in the spreadsheet. Chapter 29's interrupt-management prescriptions ([[polarizing-time]], [[interrupt-role-structuring]]) are all specialisations of the corrective: **price the context switch in, and the team-design choices follow.**

## Consequences for team design

The context-switch cost is the lever that forces Chapter 29's larger rules:

- **Longer work periods are better.** Ideally a week at a time on each work mode; a day or half-day as a practical minimum. Each period is exactly enough time for the engineer to reach flow and stay in it. See [[polarizing-time]].
- **Ticket randomisation is harmful.** Auto-distributing a ticket to whoever-is-on-project-work-today imposes two context switches on an engineer who was specifically not supposed to be doing interrupts.
- **Spreading load across the whole team backfires.** Many small interrupts on many engineers costs more productive time than concentrating the same load on a dedicated interrupt handler.
- **On-call is interrupt work, not project work.** An engineer on-call should not be expected to make progress on projects. Project work has too high a context-switch cost relative to a week-long pager interruption.

The running Fred example is the demonstration: Fred has the entire calendar day free, but his distractibility is extreme. Personal habits close some of the holes; team policy has to close the rest.

## Related pages

- [[dealing-with-interrupts]]
- [[cognitive-flow-state]]
- [[polarizing-time]]
- [[interrupt-role-structuring]]
- [[reducing-interrupts]]
- [[operational-load]]
- [[fostering-software-engineering-in-sre]]
