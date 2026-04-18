# Interrupt Role Structuring

**Summary**: Chapter 29's concrete prescriptions for how SRE teams should divide on-call, tickets, and ongoing responsibilities — derived from [[polarizing-time]] and [[context-switch-cost]]. The through-line: each role is full-time for its duration, and spreading load across everyone is worse than concentrating it.

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## The organising rule

> For any given class of interrupt, if the volume of interrupts is too high for one person, add another person.

*(source: chapter-29-dealing-with-interrupts.md)*

Not: spread the work across the whole team. The chapter's recommendation is always to **add a second dedicated person** rather than distribute the same load across an extra four or five.

## On-call

Chapter 29's specific rules for on-call (source: chapter-29-dealing-with-interrupts.md):

- **The primary on-call engineer focuses solely on on-call work.** If the pager is quiet, tickets and other interrupt-based work that can be abandoned quickly are part of on-call duties.
- **An on-call week is written off for project work.** If a project is too important to let slip, the engineer shouldn't be on-call — escalate and assign someone else.
- **Never expect a person to be on-call and simultaneously make progress on projects or anything else with a high context-switching cost.**
- **Secondary duties depend on onerousness.** A fall-through-only secondary can safely do project work. A secondary expected to actually help the primary with high page volume should do interrupt work too — and the role might as well be merged with ticket handling.

A Chapter 29 aside: *you never run out of cleanup work.* Ticket count at zero? There is always documentation to update, configs to clean up. Your future on-call engineers will thank you, and it means they'll be less likely to interrupt you during your make time.

## Tickets

> If you currently assign tickets randomly to victims on your team, stop.

The chapter's stance on random ticket assignment is unusually direct. Random assignment is *extremely disrespectful of your team's time, and works completely counter to the principle of not being interruptible as much as possible* (source: chapter-29-dealing-with-interrupts.md).

The prescribed shape:

- **Tickets should be a full-time role for a manageable duration.** Typically a week, matching on-call.
- **If ticket volume exceeds primary + secondary combined**, structure the rotation with **two people handling tickets at any given time** — not spread across the whole team. People are not machines, and spreading load out produces expensive context switches on everyone.
- **Don't let non-ticket-handlers pull tickets to look busy.** It skews the tractability signal and makes it look like the ticket queue is manageable when it isn't.

## Ongoing responsibilities

The single biggest lever is making responsibilities **portable** (source: chapter-29-dealing-with-interrupts.md):

- **Define roles so anyone on the team can take up the mantle.** If there's a well-defined procedure for a push or a flag flip, no individual has to shepherd that change for its entire lifetime, even after they stop being on-call.
- **Create a push manager role** who juggles pushes for the duration of their time on-call or on interrupts.
- **Formalise the handover.** A small price to pay for uninterrupted make time for the people not on-call.

Without formal handovers, a multi-week rollout drags its originator across the non-interrupt weeks it was supposed to exempt.

## "Be on interrupts, or don't be"

The chapter's named sub-principle. Two corollaries (source: chapter-29-dealing-with-interrupts.md):

- **Uniquely-qualified-expert interrupts should be rare.** Occasionally a team receives an interrupt that only one specific engineer can handle, even though that engineer is not on interrupts. Work to make such occurrences rare — cross-training and documentation are the mechanism. Ideally this never happens.
- **Don't pull tickets when not assigned to them.** It's easy to look busy that way, but it reduces the effectiveness of the polarisation mechanism: the designated ticket handler's metrics get skewed, and the helpful person is less effective than they should be on whatever they were actually supposed to be doing.

## Why this shape and not alternatives

The rejected alternative shapes Chapter 29 names, and what's wrong with each:

- **"Spread load across the whole team" (auto-assign everywhere).** Maximises aggregate context switches, making the team's total project-output worse than concentrated load. Each distributed interrupt costs two context switches for its recipient.
- **"One on-call engineer who also does project work."** The chapter's constant-interruptability failure mode — neither mode of [[cognitive-flow-state|flow]] is reachable.
- **"Originator carries their rollout forever."** Turns [[polarizing-time]] into a fiction: there are always residual interrupts from previous weeks leaking into supposedly project-only weeks.

## Sources of these prescriptions

Chapter 29 is careful to state the suggestions are *based on what's worked for various SRE teams that I've managed at Google* and *are mainly for the benefit of team managers or influencers.* The chapter is *agnostic to personal habits*: its concern is **team function and structure**, not individual productivity. If the general model doesn't work for a particular team, the prescriptions can be adopted piecemeal.

## Related pages

- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[context-switch-cost]]
- [[cognitive-flow-state]]
- [[operational-load]]
- [[reducing-interrupts]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[toil-and-engineering-balance]]
