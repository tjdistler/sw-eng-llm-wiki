# Architect Expectations

**Summary**: Rather than defining the role of software architect, Richards and Ford enumerate eight behavioural expectations that hold regardless of title, company, or seniority. Understanding and practising each is the first step to being effective in the role.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`, `raw/fundamentals-of-software-architecture/chapter-23-negotiation-and-leadership-skills.md`, `raw/fundamentals-of-software-architecture/chapter-24-developing-a-career-path.md`

**Last updated**: 2026-04-16 (Chapter 24 cross-references added)

---

## Why expectations, not a role definition

The job title "software architect" is defined differently at every company — from "very senior programmer" to "sets technical strategy for the enterprise" (source: chapter-01-introduction.md). Rather than argue about the right scope, Richards and Ford focus on the behaviours that differentiate an effective architect from an ineffective one. The eight expectations are the *observable* part of the job.

## The eight expectations

### 1. Make architecture decisions

An architect is expected to make [[architecture-decisions-vs-design-principles|architecture decisions and design principles]] that **guide** technology choices within a team, department, or enterprise. *Guide* is the load-bearing word. "Use React.js" is a technology decision; "use a reactive-based frontend framework" is an architecture decision that still lets teams choose between Angular, Elm, React, Vue (source: chapter-01-introduction.md).

The exception: an architect may specify a particular technology when doing so is the only way to preserve a named [[architecture-characteristics|characteristic]] (e.g. a specific caching product for a performance target). That is still an architecture decision.

### 2. Continually analyze the architecture

Assessing whether an architecture defined three or more years ago is still viable under today's technology and business environment. Richards and Ford call this **[[architecture-vitality]]**; its opposite is **structural decay** — the slow accumulation of coding and design changes that erode required characteristics (source: chapter-01-introduction.md).

An often-forgotten extension: the testing and release environments matter too. Agility in source code cannot rescue agility in the overall architecture if testing takes weeks and releases take months.

### 3. Keep current with the latest trends

Architects' decisions are long-lasting and hard to change, so staying current matters more than it does for developers (who largely need to keep current on the technologies they touch daily). Techniques for tracking trends are developed in Chapter 24 (source: chapter-01-introduction.md) and are catalogued on [[architect-career-path]]: the **20-minute rule** (20 minutes of learning a day, scheduled first thing in the morning before email), the **personal developer radar** (four quadrants × four rings adapted from ThoughtWorks, with Hold extended to cover habits to break), using social media weak links to seed the Assess ring, and [[architecture-katas|architecture katas]] as deliberate practice — "always learn, always practice, and go do some architecture" (source: chapter-24-developing-a-career-path.md).

### 4. Ensure compliance with decisions

An architect must continuously verify that development teams follow the documented decisions and principles. The worked example: if the decision is "presentation layer may not access the database directly," a UI developer bypassing that for performance reasons silently defeats the rule and the associated [[architecture-characteristics|characteristic]] that motivated it (source: chapter-01-introduction.md). Chapter 6 covers measuring compliance via automated [[architecture-fitness-function|fitness functions]] and tooling.

### 5. Diverse exposure and experience

An architect must be **familiar** with many technologies, not expert in one. Breadth beats depth: knowing the pros and cons of ten caching products is more valuable than expert knowledge of one (source: chapter-01-introduction.md). Heterogeneous environments are the default, and an architect's job is to interface across them.

Chapter 2 develops this expectation in depth as the knowledge-pyramid model of [[technical-breadth-vs-depth]], including the two failure modes (trying to maintain expertise everywhere; stale expertise) and the [[technical-breadth-vs-depth#the-frozen-caveman-anti-pattern|frozen caveman anti-pattern]] (source: chapter-02-architectural-thinking.md).

### 6. Have business domain knowledge

An architect cannot design an effective system for a problem space they do not understand. For a financial institution: terms like *average directional index*, *aleatory contracts*, *rates rally*, *nonpriority debt* (source: chapter-01-introduction.md). Without the vocabulary, the architect loses credibility with stakeholders and cannot translate requirements.

### 7. Possess interpersonal skills

Teamwork, facilitation, leadership. Gerald Weinberg: "no matter what they tell you, it's always a people problem" (source: chapter-01-introduction.md). Leadership is *at least half* of what it takes to be an effective architect. Many technically excellent architects fail here and struggle to hold positions. Covered further in Chapter 22 via the [[architect-control-spectrum|control spectrum]] and in Chapter 23 via [[architect-leadership-skills]] — the 4 C's (communication, collaboration, clarity, conciseness), the pragmatic-yet-visionary balance, leading-by-example grammar ("have you considered…" versus "you must…"), and meeting/calendar control as the mechanism for staying integrated with the team (source: chapter-23-negotiation-and-leadership-skills.md).

### 8. Understand and navigate politics

Almost every architectural decision will be challenged — by product owners, project managers, business stakeholders (cost/time), and by developers (technical opinion). Unlike a programming decision, which rarely needs approval, an architecture decision usually needs to be justified and negotiated (source: chapter-01-introduction.md). Chapter 23's [[architect-negotiation]] covers the techniques: grammar-and-buzzword reading, gathering information before the negotiation (the five-nines-to-seconds reframing), validating before redirecting, divide-and-conquer scope qualification, saving cost and time for last with stakeholders; demonstration-defeats-discussion and calm-leadership with peer architects; and justification-before-demand plus letting-developers-arrive-at-the-solution with developers (source: chapter-23-negotiation-and-leadership-skills.md).

## Why this list matters

These eight expectations cut across the [[laws-of-software-architecture|two laws]]:

- Expectations 1–4 and 7–8 are operational forms of the **First Law** — every decision is a trade-off that must be made, governed, and defended.
- Expectation 2 is where the **Second Law** ("why beats how") gets practical teeth — analysing an architecture means reconstructing the *why*, checking whether it still holds, and updating the decisions when the context has moved.

## Relation to other roles in the wiki

- [[conways-law]] — the organisation's communication structure constrains what architectures are reachable; expectations 7 and 8 are where the architect works with rather than against Conway's pull.
- [[team-autonomy]] — ensuring compliance (#4) is in tension with team autonomy; Chapter 22 covers the control-continuum dial.
- [[reorganizing-teams]] — an architect's interpersonal and political skills are what let structural reorganisations succeed at all.

## Related pages

- [[software-architecture-definition]]
- [[architecture-decisions-vs-design-principles]]
- [[architecture-characteristics]]
- [[architecture-vitality]]
- [[architecture-fitness-function]]
- [[laws-of-software-architecture]]
- [[architect-role-intersections]]
- [[architectural-thinking]]
- [[technical-breadth-vs-depth]]
- [[trade-off-analysis]]
- [[balancing-architecture-and-coding]]
- [[architect-control-spectrum]]
- [[architect-negotiation]]
- [[architect-leadership-skills]]
- [[architect-career-path]]
- [[fundamentals-of-software-architecture]]
