# Reducing Interrupts

**Summary**: Chapter 29's prescriptions for shrinking the interrupt load rather than distributing it. The core moves are **ticket scrubs**, **silencing-with-deadlines**, **using policy to push legwork back to customers**, and (as a last resort) **giving back / deprecating / replacing** components that generate unfixable interrupts.

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## Why reduction matters

Chapter 29's prior argument — [[polarizing-time]] and [[interrupt-role-structuring]] — is about distributing interrupts well. But distribution has a ceiling: if a team's aggregate interrupt load is too high to be handled by one or two interrupt holders at a time, distribution runs out of room and something else has to change. The chapter's closing sections are about that something else.

> Your team's interrupt load may be unmanageable if it requires too many team members to simultaneously staff interrupts at any given time.

*(source: chapter-29-dealing-with-interrupts.md)*

## Actually analyse tickets

The chapter's first and sharpest criticism of common SRE practice:

> Lots of ticket rotations or on-call rotations function like a gauntlet. This is especially true of rotations on larger teams. If you're only on interrupts every couple of months, it's easy to run the gauntlet, heave a sigh of relief, and then return to your regular duties. Your successor then does the same, and the root causes of tickets are never investigated.

*(source: chapter-29-dealing-with-interrupts.md)*

The structural fix:

- **Conduct a regular scrub for tickets as well as pages.** Examine classes of interrupts and identify root causes. Most teams do page reviews and on-call handoffs; *very few teams do the same for tickets.*
- **Include a handoff for tickets.** Shared state between successive ticket handlers is what lets patterns be recognised across rotations.
- **Even basic introspection helps.** Chapter 29 does not demand formal RCA; a regular conversation about *why did we see five of these?* is enough.

## Silencing-with-deadlines

If a class of interrupts has an identifiable, reasonably-fixable root cause:

> Silence the interrupts until the root cause is expected to be fixed. Doing so provides relief for the person handling interrupts and creates a handy deadline enforcement for the person fixing the root cause.

*(source: chapter-29-dealing-with-interrupts.md)*

Two mechanisms in one move: the interrupt handler gets immediate relief; the engineer fixing the bug has a concrete deadline (when silencing expires). This is a structural pattern — not a one-off trick — because it ties the annoyance to the remediation in a way ad-hoc silencing doesn't.

## Respect yourself, as well as your customers

Chapter 29 is explicit that policy is a legitimate mechanism for reducing interrupt burden, even when the interrupts come from real customers:

> Your team sets the level of service provided by your service. It's OK to push back some of the effort onto your customers.

*(source: chapter-29-dealing-with-interrupts.md)*

The policy levers:

- **Push legwork to the requestor.** If particular steps are time-consuming or tricky but don't require the SRE team's privileges, require the requestor to prepare the code/config/change and submit it for review, rather than having SRE do the steps themselves.
- **Require meaningful, rational, well-prepared requests.** The guiding principle: the request should be meaningful, rational, and include all the information and legwork needed to fulfill it. *In return, your response should be helpful and timely.*

The chapter frames this as balance: *strike a good balance between respect for the customer and respect for yourself.* Policy is as powerful a tool as code — a temporary or permanent policy fix can make an unmanageable workload manageable without waiting for a code fix.

## The nuclear option: give the pager back

For a component whose interrupts *can't* be fixed at a reasonable pace:

> If you can't get the attention you need to fix the root cause of the problems causing interrupts, perhaps the component you're supporting isn't that important. You should consider giving the pager back, deprecating it, replacing it, or another strategy in this vein that might make sense.

*(source: chapter-29-dealing-with-interrupts.md)*

Three shapes this can take:

- **Give the pager back** to the product team, along with the responsibility. Chapter 11's [[operational-overload]] catalogues the same remedy as the aggressive form of the Chapter 1 safety valve.
- **Deprecate the component.** If the SRE team's time is worth more than the component's continued operation, shutting it down is the right decision.
- **Replace the component.** Often the root-cause fix is architectural, not tactical. At some point the cost of the interrupts exceeds the cost of a replacement.

This connects to [[toil-and-engineering-balance]]'s *automate-yourself-out-of-a-job* reasoning: if SRE cannot automate the component because nobody will fund the work, the component's continued existence is itself a policy choice that SRE can challenge.

## Compounding with the other levers

The three chapter levers compound:

1. [[polarizing-time]] — protects whatever flow time is actually available.
2. [[interrupt-role-structuring]] — concentrates the remaining load so fewer engineers eat it.
3. **Reducing interrupts** (this page) — shrinks the load itself so fewer engineers are needed in step 2.

Done together, they shift a team from "everyone distracted all the time" to "a small rotating interrupt handler with a shrinking queue, while everyone else is in flow."

## Connection to other SRE chapters

- [[alert-philosophy]] (SRE Ch 6) — the *urgent / actionable / intelligent / novel* alert principles and the five-question new-alert checklist are the paging-tier equivalent of Chapter 29's ticket scrubs. Both are structural defences against noise accumulation.
- [[operational-overload]] (SRE Ch 11) — Chapter 11's give-back-the-pager remedy is the strongest form of the "deprecate / replace" end of Chapter 29's ladder.
- [[toil-and-engineering-balance]] (SRE Ch 5) — interrupts are the #1 ranked toil source; Chapter 29's reductions are what drives the toil number down, not more headcount.
- [[postmortem-culture-activities]] (SRE Ch 15) — teachable postmortems play the same role for significant incidents that ticket scrubs play for low-severity interrupts.

## Related pages

- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[interrupt-role-structuring]]
- [[context-switch-cost]]
- [[operational-load]]
- [[operational-overload]]
- [[alert-philosophy]]
- [[toil-and-engineering-balance]]
