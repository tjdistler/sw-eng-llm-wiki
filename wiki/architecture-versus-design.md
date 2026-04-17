# Architecture Versus Design

**Summary**: The traditional separation — architect defines characteristics, patterns, and components; developer produces class diagrams, UI, and code — is what Richards and Ford say makes architecture rarely work. The required fix is a bidirectional, collaborative relationship in which architecture and design are treated as one continuous activity, not sequential handoffs.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`

**Last updated**: 2026-04-16

---

## The traditional split

In the traditional model, the architect is responsible for (source: chapter-02-architectural-thinking.md):

- analysing business requirements to extract and define the [[architecture-characteristics|architecture characteristics]] ("-ilities")
- selecting which architecture patterns and styles fit the problem domain
- creating components — the building blocks of the system

The development team is then responsible for:

- creating class diagrams for each component
- creating user-interface screens
- developing and testing source code

The architect produces artefacts and hands them off. The developer implements.

## Why the traditional split fails

The failure mode is the handoff itself — a unidirectional arrow through a virtual and physical barrier between the two groups (source: chapter-02-architectural-thinking.md):

- Decisions the architect makes sometimes never reach the development teams.
- Decisions the development teams make that change the architecture rarely return to the architect.
- The architect becomes disconnected from the people building the system, and the architecture stops delivering what it was set out to do.

Richards and Ford are blunt: this illustration "shows exactly why architecture rarely works" (source: chapter-02-architectural-thinking.md).

## The required fix: bidirectional collaboration

Both the physical and virtual barriers between architect and developer must be broken down, forming a strong bidirectional relationship. The architect and developer must be on the same virtual team (source: chapter-02-architectural-thinking.md). This enables two payoffs:

1. **Strong bidirectional communication** — changes in either direction land where they need to.
2. **Mentoring and coaching** — the architect is close enough to the code to guide developers.

See [[balancing-architecture-and-coding]] for the concrete practices (POCs, technical-debt work, bug fixes, automation, code reviews) that keep the architect close enough to the code for the bidirectional relationship to work.

## "Where does architecture end and design begin?"

The chapter's answer: **it doesn't** (source: chapter-02-architectural-thinking.md). Architecture and design are both part of the "circle of life" within a software project and must always be kept in synchronisation. The modern iterative project changes and evolves architecture every iteration — the old waterfall model of static, rigid architecture is explicitly rejected.

This reframes the question. Rather than drawing a line between architecture and design, the architect's job is to keep them tightly coupled — structurally different activities that feed each other continuously.

## Relationship to the rest of the wiki

- [[evolutionary-architecture]] — the book-wide answer to why architecture cannot be "finished" and thrown over a wall; architecture-design synchronisation is an evolutionary-architecture precondition.
- [[architecture-vitality]] — the ongoing analysis that detects when design decisions have silently eroded the architecture the architect intended.
- [[architect-role-intersections]] — the Chapter 1 framing of the role's expansion to intersect with engineering practices is the same argument at an organisational scale: the old "architect apart from engineering" model doesn't work either.
- [[architect-expectations]] — expectation #4 (ensuring compliance with decisions) is the bidirectional-relationship mechanism in practice.

## Related pages

- [[architectural-thinking]]
- [[balancing-architecture-and-coding]]
- [[evolutionary-architecture]]
- [[architecture-vitality]]
- [[architect-role-intersections]]
- [[architect-expectations]]
- [[software-architecture-definition]]
- [[fundamentals-of-software-architecture]]
