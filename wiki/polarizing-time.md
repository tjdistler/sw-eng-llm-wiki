# Polarizing Time

**Summary**: Chapter 29's core team-design principle for interrupt management — when an engineer arrives at work, they should know whether they are doing project work *or* interrupts, not both. The period is ideally a week, with a day or half-day as practical minimums. Polarisation exists to price in the [[context-switch-cost]] and protect [[cognitive-flow-state|flow]].

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## The principle

> Polarizing time means that when a person comes into work each day, they should know if they're doing just project work or just interrupts. Polarizing their time in this way means they get to concentrate for longer periods of time on the task at hand. They don't get stressed out because they're being roped into tasks that drag them away from the work they're supposed to be doing.

*(source: chapter-29-dealing-with-interrupts.md)*

Chapter 29 also cites the complementary concept of **make time** (Paul Graham's *Maker's Schedule, Manager's Schedule*): long unbroken blocks suit production work, short fragmented blocks suit management. Polarising time is the SRE-team version of the same observation.

## Period length

The chapter gives three practical length tiers (source: chapter-29-dealing-with-interrupts.md):

- **A week** — the ideal. Aligns with the natural on-call shift length, the ticket-rotation period, and the time it takes to get into deep engineering flow on a meaningful project.
- **A day** — acceptable if a week doesn't fit the team.
- **A half-day** — acceptable if neither fits. Morning-blocks-for-projects / afternoon-blocks-for-interrupts is the typical half-day shape.

Each period is chosen to be large enough that the engineer can reach [[cognitive-flow-state|flow]] inside it. Anything shorter degenerates into the constant-interruptability state the chapter is designed to prevent.

## What polarisation rules out

The structure the chapter specifically rejects (source: chapter-29-dealing-with-interrupts.md):

- **Everyone on project work with tickets randomly assigned to the team.** A ticket can arrive on any engineer on any day.
- **On-call engineers expected to also make progress on projects.** The two fight each other on context switches; project work is what loses.
- **Ongoing responsibilities following the original engineer forever.** A multi-week rollout that the originator alone can shepherd blocks that engineer from ever being fully off-interrupts.
- **Engineers who look busy by pulling tickets when not assigned to tickets.** Noisily helpful, but they skew the tractability signal (if one person is assigned but two others also pull, the queue looks manageable when it isn't).

## What polarisation requires

For polarisation to actually work (source: chapter-29-dealing-with-interrupts.md):

- **Interrupt role on, interrupt role off, with a handoff.** Tickets the engineer hasn't finished go to the next interrupt holder at shift boundary, not "follow" the original engineer.
- **Ongoing responsibilities defined so *anyone* can pick them up.** If there's a well-defined procedure for a push or flag flip, there's no reason one engineer has to shepherd that change for its entire multi-week lifetime. Define a **push manager role**; formalise the handover.
- **Project work on-call is written off.** If a project is too important to slip for a week, escalate and put someone else on-call.
- **"Be on interrupts, or don't be."** People working tickets when not assigned to tickets is unhelpful. It's an easy way to look busy, but it reduces the effectiveness of the polarisation mechanism.

## Connection to the context-switch arithmetic

Polarising time is the direct team-design consequence of [[context-switch-cost]]: if a 20-minute interrupt costs two hours of flow, the right unit of work assignment is not "a task" but "a block of time long enough to reach and stay in flow." Chapter 29's weekly rotations are the block-length that makes the arithmetic work out.

## Connection to Paul Graham's make time

Graham's *Maker's Schedule, Manager's Schedule* essay (cited in Chapter 29 as [Gra09]) argues that makers — programmers, writers — need blocks of unfragmented time, while managers operate well on hour-by-hour schedules. A single unexpected meeting can destroy a maker's afternoon. Polarising time is SRE's way of giving every engineer a maker schedule for half the time and a manager-like-interrupt schedule for the other half, rather than trying to run both at once.

## Connection to existing wiki material

- [[fostering-software-engineering-in-sre]] — Chapter 18's *dedicated non-interrupted project time is essential; nearly impossible to write code while thrashing between several tasks per hour* is the same argument from the software-engineering side. Polarising time is how that protected project time is actually enforced.
- [[toil-and-engineering-balance]] — Chapter 5's 50% cap bounds the aggregate; polarising time bounds the *within-week* mixing. Without polarisation, a 25%-toil engineer can still live in constant interruptability.
- [[balanced-on-call]] — Chapter 11's 25% on-call cap assumes that on-call weeks are *fully* on-call. Polarising time is the principle that makes the 25% figure meaningful rather than an average.

## Related pages

- [[dealing-with-interrupts]]
- [[context-switch-cost]]
- [[cognitive-flow-state]]
- [[interrupt-role-structuring]]
- [[reducing-interrupts]]
- [[fostering-software-engineering-in-sre]]
- [[toil-and-engineering-balance]]
- [[balanced-on-call]]
