# Technical Breadth vs Depth

**Summary**: Richards and Ford model all of a technologist's knowledge as a three-tier pyramid — *stuff you know*, *stuff you know you don't know*, and *stuff you don't know you don't know*. Developers build their careers by growing the top (depth); architects deliberately sacrifice some depth to grow the middle (breadth), because an architect's job is to know that multiple solutions exist, not to be the expert in any one of them.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`, `raw/fundamentals-of-software-architecture/chapter-24-developing-a-career-path.md`

**Last updated**: 2026-04-16 (Chapter 24 cross-references added)

---

## The knowledge pyramid

All of a technologist's knowledge can be partitioned into three sections (source: chapter-02-architectural-thinking.md):

| Section | What it contains | Example |
|---|---|---|
| **Stuff you know** | Technologies, frameworks, languages, tools used daily | Knowing Java as a Java programmer |
| **Stuff you know you don't know** | Things you've heard of but lack expertise in | Having heard of Clojure but being unable to code in it |
| **Stuff you don't know you don't know** | The largest part — solutions that might be perfect for your problem but you don't know they exist | Any technology you've never encountered |

The size of the **top** is a technologist's **technical depth**. The size of the **middle** — specifically, how far it penetrates into the bottom — is a technologist's **technical breadth** (source: chapter-02-architectural-thinking.md).

## The two career shapes

### Developer: grow the top

A developer's early career focuses on expanding the top of the pyramid — building experience and expertise. This is the correct focus: developers need perspective, working knowledge, and hands-on experience (source: chapter-02-architectural-thinking.md). Expanding the top incidentally expands the middle as developers encounter more technologies.

The catch: **the stuff you know is the stuff you must maintain**. Nothing is static in software. A Ruby on Rails expert who ignores Ruby on Rails for a year or two will lose the expertise (source: chapter-02-architectural-thinking.md). Depth requires continuous time investment.

### Architect: grow the middle

When a developer transitions into the architect role, the nature of knowledge changes. A large part of an architect's value is a broad understanding of technology and how to use it to solve particular problems (source: chapter-02-architectural-thinking.md):

> As an architect, it is more beneficial to know that five solutions exist for a particular problem than to have singular expertise in only one.

An architect must make decisions that match capabilities to technical constraints; a broad understanding of a wide variety of solutions is what makes that possible. The wise course is to **sacrifice some hard-won expertise** and invest that time in broadening the portfolio. Some areas of enjoyable expertise will remain; others usefully atrophy (source: chapter-02-architectural-thinking.md).

## Two dysfunctions to watch for

When developers transition to architect, two common failure modes appear (source: chapter-02-architectural-thinking.md):

1. **Trying to maintain expertise in a wide variety of areas** — succeeding in none of them and working oneself ragged in the process.
2. **Stale expertise** — the mistaken sensation that outdated information is still cutting edge. Often seen in large companies where the developers who founded the company moved into leadership but still make technology decisions using ancient criteria.

## The frozen caveman anti-pattern

Chapter 2 names a specific form of stale expertise as its own behavioural anti-pattern (source: chapter-02-architectural-thinking.md):

> An architect who always reverts back to their pet irrational concern for every architecture.

The canonical example: one of Neal Ford's colleagues worked on a centralised architecture, and the client architects obsessively asked "but what if we lose Italy?" — a reference to a freak communication outage years earlier. The chance of recurrence was extremely small, but the architects had become obsessed with that particular architectural characteristic (source: chapter-02-architectural-thinking.md).

The pattern generally manifests in architects who were burned by a poor decision or unexpected occurrence and became over-cautious in response. The fix is distinguishing **genuine risk** from **perceived risk** as part of the ongoing learning process. Architectural thinking requires overcoming these frozen caveman ideas, seeing other solutions, and asking more relevant questions.

## Why this matters: the larger quiver

The chapter's closing image: architects should focus on technical breadth so they have a larger quiver from which to draw arrows (source: chapter-02-architectural-thinking.md). Every additional solution known is another option in the [[trade-off-analysis]] the architect must perform on every decision. Narrow expertise produces narrow trade-offs.

## Balancing the portfolio throughout a career

Balancing the portfolio of knowledge regarding depth versus breadth is something every developer should consider throughout their career (source: chapter-02-architectural-thinking.md) — not just at the moment of transition. See [[balancing-architecture-and-coding]] for the complementary discipline: the architect who has moved toward breadth still needs to maintain *some* technical depth, and Chapter 2 lays out specific techniques for doing so.

Chapter 24 operationalises this balancing act for the breadth side. [[architect-career-path]] introduces the **20-minute rule** (a scheduled daily learning slot that grows the middle of the pyramid one buzzword at a time) and the **personal developer radar** (a four-quadrant × four-ring classification that turns ad-hoc tech-tracking into a living portfolio treated like a financial one) (source: chapter-24-developing-a-career-path.md). Both techniques are defences against the two dysfunctions above: the 20-minute rule forces breadth to actually happen instead of being always-tomorrow, and the radar — especially following weak-link technologists on social media to populate the Assess ring — defends against the technology-bubble echo chamber that produces stale expertise.

## Relationship to Chapter 1 material

[[architect-expectations|Expectation #5]] ("diverse exposure and experience") is the behavioural expression of the breadth-over-depth principle. Chapter 1 named the expectation; Chapter 2 supplies the underlying knowledge model and the cautionary tales (the two dysfunctions, the frozen caveman).

[[unknown-unknowns]] connects directly: the bottom of the pyramid — stuff you don't know you don't know — is precisely the Rumsfeld "unknown unknowns" that make all architecture iterative. Broadening the middle of the pyramid is how the architect shrinks the bottom over time.

## Related pages

- [[architectural-thinking]]
- [[architect-expectations]]
- [[trade-off-analysis]]
- [[balancing-architecture-and-coding]]
- [[architect-career-path]]
- [[unknown-unknowns]]
- [[architect-role-intersections]]
- [[laws-of-software-architecture]]
- [[fundamentals-of-software-architecture]]
