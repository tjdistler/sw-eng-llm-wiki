# Cumulative Learning Paths

**Summary**: Chapter 28's constructive alternative to the [[trial-by-fire-anti-pattern|trial-by-fire anti-pattern]]: a sequential, ordered onboarding curriculum that frontloads recurring abstract concepts, intermixes hands-on work as early as practical, and gives the student a visible path forward at every step.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The principle

> Put some amount of learning order into your system(s) so that your new SREs see a path before them. Any type of training is better than random tickets and interrupts, but do make a conscious effort to combine the right mix of theory and application. (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md)

Two design rules fall out:

- **Frontload abstract concepts** that will recur throughout the newbie's journey.
- **Intermix hands-on work** as soon as practical — don't run pure-theory for months before letting the student touch a keyboard.

The goal is a learner who can answer *what am I working on today, how much progress have I made, how much farther is it to on-call?* at every moment. See the three unanswered questions under [[trial-by-fire-anti-pattern]].

## Grouping the curriculum

Chapter 28 offers two axes for ordering trainings (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- By **similarity of purpose** (all caches together, all backends together, all alerting together), or
- By **normal-case order of execution** (follow a request through the stack)

For a user-facing real-time serving stack, Widdowson's example ordering follows the request:

1. **How a query enters the system** — networking and datacenter fundamentals, frontend load balancing, proxies
2. **Frontend serving** — application frontend, query logging, user-experience SLOs
3. **Mid-tier services** — caches, backend load balancing
4. **Infrastructure** — backends, infrastructure, compute resources
5. **Tying it all together** — debugging techniques, escalation procedures, emergency scenarios

The "follow the request" ordering happens to match [[life-of-a-request|Chapter 2's Shakespeare walkthrough]] — not a coincidence. It is the same pedagogical instinct applied twice.

## Delivery formats are a choice

How you present the material is up to the team: informal whiteboard chats, formal lectures, or hands-on discovery exercises. Chapter 28 is **deliberately agnostic** because students have different learning preferences and no single modality suits them all (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). A well-designed curriculum mixes modalities across the sequential arc.

## The document backbone

The sequential path is typically recorded in an [[on-call-learning-checklist|on-call learning checklist]] — the living document that:

- enumerates expert contacts and key documentation resources
- lists the basic knowledge to absorb
- poses probing questions that can only be answered *after* the basic knowledge is internalised
- names the concrete outcomes of each section

Widdowson emphasises that the checklist **does not directly encode procedures, diagnostic steps, or playbooks**. That would date quickly. Instead it is "future-proof" — it points at where the authoritative information lives, rather than duplicating it.

## Homework and feedback

It's a good idea for interested parties to gauge what the trainee is retaining. Chapter 28 suggests informal homework — pose questions about how the services work, and have a mentor check the answers before the student moves to the next phase (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Example questions:

- Which backends of this server are considered "in the critical path," and why?
- What aspects of this server could be simplified or automated?
- Where do you think the first bottleneck is in this architecture? If that bottleneck were saturated, what steps could you take to alleviate it?

These are deliberately *generative* questions rather than multiple-choice — they require the student to build and defend a mental model, which is the skill they will need on-call.

## Tiered access as progress-gating

Where access permissions allow, Chapter 28 recommends a **tiered access model**:

- Tier 1: read-only access to component internals
- Tier 2 (and beyond): increasing ability to mutate production state

Completing sections of the learning checklist earns progressively deeper access. The Google Search SRE team calls these attained levels *"powerups"* on the route to on-call — a nod to video games (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). The gamification is deliberate: it makes progress legible and celebrates each step.

## Relationship to the broader blueprint

Cumulative learning paths are the backbone on which Chapter 28's [[sre-onboarding|other practices]] hang:

- [[teachable-postmortems]] and [[reverse-engineering-class]] feed into the **frontloaded abstract** end
- [[targeted-project-work]] and [[breaking-real-systems]] fill the **hands-on** end
- [[on-call-learning-checklist]] tracks where the student is on the path
- [[shadow-on-call]] follows once the path is substantially complete

The path does not "end" at on-call — see [[sre-continuing-education]]. Going on-call changes the shape of learning (from defined to self-directed) but does not conclude it.

## Related pages

- [[sre-onboarding]]
- [[trial-by-fire-anti-pattern]]
- [[on-call-learning-checklist]]
- [[targeted-project-work]]
- [[reverse-engineering-class]]
- [[teachable-postmortems]]
- [[shadow-on-call]]
- [[sre-continuing-education]]
- [[life-of-a-request]]
