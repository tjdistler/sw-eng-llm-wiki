# Operational Load

**Summary**: Chapter 29's opening definition — the work that must be done to maintain a complex system in a functional state. The chapter divides operational load into three general categories (pages, tickets, ongoing responsibilities) with distinct SLOs and management patterns, and this three-way split structures every later discussion in the chapter.

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## Definition

> Operational load, when applied to complex systems, is the work that must be done to maintain the system in a functional state.

Chapter 29's opening analogy: if you own a car, you (or someone you pay) always end up servicing it, putting gas in it, or doing other regular maintenance. Any complex system is as imperfect as its creators, and the creators are also imperfect machines (source: chapter-29-dealing-with-interrupts.md).

Operational load takes many forms, some more obvious than others. The terminology varies across teams, but the load falls into three general categories.

## The three categories

### Pages

Production alerts and their fallout. Triggered in response to emergencies. **Expected response time (SLO) typically measured in minutes.**

Pages can be monotonous and recurring, requiring little thought, or engaging and requiring tactical in-depth thought. See [[sre-on-call-engagement]] and [[emergency-response]].

### Tickets

Customer requests that require an action from the team. **SLO typically measured in hours, days, or weeks.** Examples:

- A simple ticket: a code review for a config the team owns.
- A more complex ticket: a design consultation or capacity plan for an unusual request.

Tickets are the primary target of Chapter 29's interrupt-management argument — they are where team structure has the most leverage, because ticket SLOs are loose enough that batching and role rotation are practical.

### Ongoing operational responsibilities

Also known as "kicking the can down the road" and as [[toil-and-engineering-balance|toil]] (the chapter cites Chapter 5). Includes:

- Team-owned code or flag rollouts.
- Responses to ad hoc, time-sensitive customer questions.

**No defined SLO**, but these tasks can interrupt at any time, requiring the recipient to decide whether the issue can wait. A multi-week rollout owned by one engineer is the archetype.

## Planned vs unplanned load

Some types of operational load are easily anticipated or planned for (scheduled releases, routine flag flips). Much of it is unplanned or can interrupt at a nonspecific time. The unplanned portion is what makes operational load pernicious: it prevents planning and destroys [[cognitive-flow-state|flow]] even when the aggregate work hours would otherwise be manageable.

## Managing each category

Chapter 29 catalogues Google's common patterns per category (source: chapter-29-dealing-with-interrupts.md):

| Category | Typical shape |
|---|---|
| Pages | Single primary on-call engineer, secondary backup |
| Tickets | Primary handles while on-call, or dedicated ticket person, or secondary handles, or auto-distributed |
| Ongoing responsibilities | On-call handles, or assigned ad hoc, or whoever-is-on-interrupts holds them across shifts |

See [[interrupt-role-structuring]] for Chapter 29's specific prescriptions about which of these arrangements work well and which fail.

## The metrics teams use to choose

Chapter 29 enumerates the metrics SRE teams at Google have found useful when deciding how to manage a given interrupt class (source: chapter-29-dealing-with-interrupts.md):

- Interrupt SLO or expected response time
- The number of interrupts usually backlogged
- The severity of the interrupts
- The frequency of the interrupts
- The number of people available to handle that kind of interrupt (e.g., some teams require a certain amount of ticket work before going on-call)

Chapter 29 then warns that all of these metrics are oriented toward meeting the lowest possible response time, **without** factoring in the human cost. Taking stock of that cost is difficult, but it is what Chapter 29 insists must happen — see [[context-switch-cost]] and [[cognitive-flow-state]].

## Relationship to toil

Operational load is a superset of toil. Toil is the kind of operational work that is manual, repetitive, automatable, tactical, devoid of enduring value, and O(n) with service growth ([[toil-and-engineering-balance]]). Not all operational load is toil: genuinely novel incidents, first-time customer requests, and architecture consultations are operational load but **not** toil.

Chapter 5 ranks the three largest sources of measured toil as (source: chapter-05-eliminating-toil.md):

1. **Interrupts** — non-urgent service-related messages and emails.
2. **On-call (urgent) response**.
3. **Releases and pushes**.

Interrupts lead. Chapter 29 is the chapter about that #1 source, and its interrupt model pulls most aggressively on the ticket and ongoing-responsibility categories.

## Related pages

- [[dealing-with-interrupts]]
- [[toil-and-engineering-balance]]
- [[engineering-work-categories]]
- [[sre-on-call-engagement]]
- [[emergency-response]]
- [[interrupt-role-structuring]]
- [[operational-overload]]
- [[cognitive-flow-state]]
