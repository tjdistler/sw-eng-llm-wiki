# Dealing with Interrupts

**Summary**: Chapter 29 (Dave O'Connor) is the SRE book's treatise on how a team structures its response to operational load so that engineers can actually get project work done. The thesis: pages are not the only interruption that matters, context switches are expensive, and a team's interrupt model is a design decision the manager owns — not an individual-productivity problem to leave to each engineer.

**Sources**: `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## The thesis

The chapter opens by broadening the aperture from pages to [[operational-load]] as a whole: the work required to keep a complex system functional, of which pages are only one part. Its creators are as imperfect as the systems they build, and much of the load is unplanned or can interrupt someone at a nonspecific time. The job of a manager or team lead is to **structure how the team handles all that load so that engineers can reach and stay in** [[cognitive-flow-state|cognitive flow]] (source: chapter-29-dealing-with-interrupts.md).

This is orthogonal to personal time-management habits. Chapter 29 is agnostic to those. Its concern is team policy: who handles what, for how long, on which days, with what handoff.

## Three kinds of operational load

The chapter names three general categories (source: chapter-29-dealing-with-interrupts.md):

- **Pages** — production alerts and their fallout, triggered in response to emergencies. Response time SLO typically in minutes. See [[sre-on-call-engagement]] and [[emergency-response]].
- **Tickets** — customer requests requiring an action (code reviews, design consultations, capacity questions). Response time SLO typically in hours, days, or weeks.
- **Ongoing operational responsibilities** — team-owned code pushes, flag rollouts, ad-hoc time-sensitive customer questions. No defined SLO but can interrupt at any time. Also named "kicking the can down the road" and [[toil-and-engineering-balance|toil]].

The chapter's recurring terminology uses **interrupts** to cover tickets and ongoing responsibilities — that is, everything that isn't a page. All three kinds produce interruptions, but they are managed differently because their SLOs and severities differ.

## Managing each kind of load

Chapter 29 describes Google's common shapes for each (source: chapter-29-dealing-with-interrupts.md):

- **Pages** are almost always handled by a single **primary on-call engineer**. One engineer at a time prevents the bystander effect and minimises team-wide disruption. A **secondary** backs up the primary; duties vary (fall-through, related duties, or cross-team backup).
- **Tickets** are managed in multiple shapes: primary on-call handles them between pages, or the secondary does, or a dedicated ticket person not on-call does. Distribution can be auto-random or ad hoc.
- **Ongoing responsibilities** may be held by the on-call engineer, assigned ad hoc, or held by whoever is on interrupts (even across shift boundaries for multi-week rollouts).

The chapter catalogues the most common metrics teams use to choose among these arrangements: interrupt SLO, expected backlog, severity, frequency, and available headcount. It warns that these metrics all optimise for fastest response, **without** factoring in the human cost of context switching — which is the rest of the chapter's subject.

See [[interrupt-role-structuring]] for the chapter's prescriptions.

## The underlying model: imperfect machines

Chapter 29's argument grounds in a bluntly-stated model: **humans are imperfect machines**. They get bored, their internal state is not well understood by themselves or others, and they are not uniformly efficient. Treating an engineer as "an interruptible unit of work whose context switches are free" is suboptimal for producing either happy engineers or useful output (source: chapter-29-dealing-with-interrupts.md).

The two consequences the chapter develops:

- [[cognitive-flow-state]] — the "zone" state engineers reach when working intently on a problem. Creative and productive, but fragile.
- [[context-switch-cost]] — a 20-minute interruption is not a 20-minute interruption. It is two context switches, which cost a couple of hours of productive work.

These two ideas anchor every recommendation in the rest of the chapter.

## Flow in a mixed project / on-call environment

Chapter 29 recognises two shapes of flow an SRE can reach (source: chapter-29-dealing-with-interrupts.md):

- **"Creative and engaged"** — engineer is working on a hard problem they understand, loses track of time, ignores interrupts, produces good work by volume.
- **"Angry Birds" flow** — engineer is concentrating full-time on interrupts; ticket-closing and bug-fixing become a clear set of goals with immediate feedback. At a visceral level, *when you're doing interrupts, your projects are the distraction.*

Both can be fulfilling. What doesn't work is the middle: trying to code while on-call, or trying to do projects while the ticket queue fills up. That engineer exists in a state of **constant interruptability**, which is extremely stressful. The chapter argues the remedy is structural, not individual — see [[polarizing-time]].

## The two practical ideas

The chapter's concrete guidance condenses to two principles:

- **[[polarizing-time]]** — an engineer coming into work on any given day should know whether they are doing project work or interrupt work. Ideally the period is a week; a day or half-day is workable. The goal is to stop treating engineers as interruptible units whose context switches are free.
- **"Do one thing well"** — on-call should be on-call (project work written off for the week); ticket handling should be a full-time role; ongoing responsibilities should be defined so *anyone* on the team can pick them up via a formal handoff rather than following the originator around. See [[interrupt-role-structuring]].

## Reducing interrupts

The other half of the chapter is about shrinking the load rather than distributing it. See [[reducing-interrupts]]. Key moves (source: chapter-29-dealing-with-interrupts.md):

- **Conduct ticket scrubs** as well as page reviews. Most teams do the latter; few do the former.
- **Silence known-fixable interrupts** until the root cause is expected to be fixed, creating a concrete deadline for the fixer.
- **Use policy to push effort back onto customers** who file onerous tickets; requesting a code change prepared by the requestor, for example.
- Recognise that **respect for yourself is as legitimate as respect for your customer**. At the limit, *giving back the pager / deprecating / replacing* a pathologically-noisy component is a legitimate option.

## Connection to the rest of the book

Chapter 29 sits at the intersection of three earlier strands:

- **The 50% cap**. [[toil-and-engineering-balance]] establishes that toil is bounded. Chapter 29 explains the *mechanics* — structuring time-polarisation, interrupt roles, and scrubs — that keep the team under the cap in practice. Chapter 5's ranked toil sources place **interrupts at #1**; Chapter 29 is the chapter about that #1.
- **Operational overload**. [[operational-overload]]'s "misconfigured monitoring" as the common overload cause is the page-side problem; Chapter 29 generalises to the ticket and ongoing-responsibility sides and adds the flow/context-switch analysis. Chapter 11 explicitly points forward to this chapter.
- **Software engineering in SRE**. [[fostering-software-engineering-in-sre]]'s warning that *dedicated non-interrupted project time is essential* and must be *aggressively defended* is the Chapter 18 restatement of the Chapter 29 argument from the project-work side.

## Related pages

- [[operational-load]]
- [[cognitive-flow-state]]
- [[context-switch-cost]]
- [[polarizing-time]]
- [[interrupt-role-structuring]]
- [[reducing-interrupts]]
- [[toil-and-engineering-balance]]
- [[operational-overload]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[fostering-software-engineering-in-sre]]
- [[alert-philosophy]]
