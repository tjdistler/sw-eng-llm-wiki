# Providing Guidance via Design Principles

**Summary**: Richards & Ford's third Chapter 22 technique for making teams effective: instead of prescriptive rules or absent silence, an architect gives the team *design principles* with clear decision boundaries. The worked example — governing which third-party libraries developers can add — shows how to turn a recurring judgement call into a shared framework, and how **asking for business justification** converts disruptive enthusiasm into productive engagement.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-22-making-teams-effective.md`

**Last updated**: 2026-04-16

---

## The technique

Providing guidance is the third leg of Chapter 22's team-effectiveness stool (alongside the [[architect-control-spectrum|control spectrum]] and [[architectural-checklists|checklists]]). The technique: define **design principles** — guidelines rather than hard rules — and communicate the *constraints around how developers apply them* (source: chapter-22-making-teams-effective.md). This is how an effective architect draws "the box" without listing every rule inside it.

Design principles live on the flexible half of the Chapter 19 distinction — see [[architecture-decisions-vs-design-principles]]. A *decision* is a hard-and-fast rule requiring variance approval. A *principle* is a guideline; developers apply judgement inside it. Providing guidance means making that judgement well-scaffolded.

## The two-question filter for proposed libraries

The worked example in the chapter is governing the **layered stack** — the collection of third-party libraries (JARs, DLLs) that make up the application. Developers constantly want to add new ones. An effective architect prompts the developer through two questions (source: chapter-22-making-teams-effective.md):

1. **Are there any overlaps between the proposed library and existing functionality within the system?**
2. **What is the justification for the proposed library?** — both a **technical** and a **business** justification.

Question 1 is the overlap check — it catches the duplicate-dependency problem that plagues large projects with large teams. Developers often skip this step, creating parallel implementations of the same capability.

Question 2 is the powerful one. Asking for a **business justification** — not just a technical one — converts "I want this library because it's cool" into "does this benefit cost, time to market, user satisfaction, or strategic positioning?" (the same four categories listed on [[architecture-decision-anti-patterns]] as Chapter 19's business-justification taxonomy).

## The Scala anecdote

The chapter's worked example is Mark Richards's own project: a Java codebase with a team member aggressively lobbying to introduce Scala. Two key team members were ready to quit the "toxic" environment. Mark's move was neither to forbid Scala nor to allow it — he told the enthusiast he would support Scala **if the enthusiast produced a business justification**, citing training costs and rewriting effort (source: chapter-22-making-teams-effective.md).

The enthusiast left ecstatic. He returned the next day *transformed*:

> He could come up with all the technical reasons in the world to use Scala, but none of those technical advantages had any sort of business value in terms of the architecture characteristics needed ("-ilities"): cost, budget, and timeline. In fact, the Scala enthusiast realized that the increase in cost, budget, and timeline would provide no benefit whatsoever.

The enthusiast became one of the best contributors on the team. The two seniors who had threatened to quit stayed to the end. The intervention cost the architect one conversation and a framing question — no prescription, no veto.

The broader lesson: **business justification is a teaching tool as much as a gating tool**. Asking for it raises developer awareness of the "-ilities" and their trade-offs (see [[architecture-characteristics]] and [[trade-off-analysis]]), and it converts adversarial advocacy into shared reasoning.

## Categorising the decision surface

Once the overlap/justification questions are in place, the next piece of guidance is **who decides**. The chapter's worked example (Figure 22-13) splits third-party libraries into three categories, with a different level of developer autonomy for each:

| Category | Examples | Who decides |
|---|---|---|
| **Special purpose** | PDF rendering, barcode scanning, specialised work that doesn't warrant custom code | Developer decides; no architect consultation required |
| **General purpose** | Wrappers on the language API (Apache Commons, Guava) | Developer performs overlap analysis and justification; **architect approval required** |
| **Framework** | Entire-layer libraries that are highly invasive (Hibernate for persistence, Spring for IoC) | **Architect decides**; developers don't even undergo analysis |

The categories themselves are project-specific — Richards and Ford present them as an example, not a standard. The deeper principle is the pattern: **explicitly demarcate where developer autonomy ends and architect approval begins**, and make that demarcation visible (the chapter recommends a graphic).

This maps directly to the [[architect-control-spectrum|control spectrum]]: in the Special category the architect is closer to armchair; in the Framework category, closer to control freak. Correctness is context-dependent, and the graphic is how the context becomes legible to the team.

## Why this beats prescription

The alternative — listing every allowed library and forbidding everything else — is prescription. It breaks for the same reasons all whitelist governance breaks: the list is always wrong, always out of date, and always requires an architect in the loop for cases the architect hasn't met yet.

Guidance via design principles instead gives the team the *framework for deciding* new cases. The team asks: is this Special, General, or Framework? Have I done overlap analysis? Do I have a business justification? The architect isn't the gatekeeper — the architect is the author of the decision-making process. That's what "effective" looks like on the [[architect-control-spectrum|control spectrum]].

## Relationship to other mechanisms

- [[architecture-decision-record|ADRs]] — the format a principle gets recorded in once it's shared; the Decision and Consequences sections of an ADR are where "why" lives
- [[architectural-checklists]] — checklists capture operational discipline; design principles capture the reasoning template for open-ended decisions
- [[architecture-fitness-function|fitness functions]] — where a principle can be expressed as an automated check, it becomes a fitness function (ArchUnit "only this layer can call this layer"); where it can't, it stays in the Providing Guidance technique on this page
- [[trade-off-analysis]] — the business-justification question is the trade-off-analysis frame applied at the developer-decision level
- [[laws-of-software-architecture|Second Law]] — *why is more important than how* — the business justification is the why

## Related pages

- [[architect-control-spectrum]]
- [[architectural-checklists]]
- [[architecture-decisions-vs-design-principles]]
- [[architecture-decision-record]]
- [[architecture-decision-anti-patterns]]
- [[architecture-fitness-function]]
- [[architecture-characteristics]]
- [[trade-off-analysis]]
- [[laws-of-software-architecture]]
- [[fundamentals-of-software-architecture]]
