# Balancing Architecture and Hands-On Coding

**Summary**: Richards and Ford argue every architect should code and maintain some technical depth, but full-time architecture work makes that hard. Chapter 2 offers concrete techniques: avoid the bottleneck trap by delegating critical-path code; if coding with the team isn't possible, stay hands-on via proof-of-concepts, technical-debt stories, bug fixes, automation tooling, and frequent code reviews.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`

**Last updated**: 2026-04-16

---

## The claim

> Every architect should code and be able to maintain a certain level of technical depth. (source: chapter-02-architectural-thinking.md)

This is the complement to [[technical-breadth-vs-depth|the breadth-over-depth argument]]: the architect shifts the knowledge portfolio toward breadth but does *not* abandon depth entirely. Chapter 2 is concrete about why — the architect needs to identify with the development team, understand the pain of their daily work, and retain the credibility to mentor them. That is not achievable from the whiteboard alone.

## The bottleneck trap

The first and most dangerous failure mode:

> The bottleneck trap occurs when the architect has taken ownership of code within the critical path of a project (usually the underlying framework code) and becomes a bottleneck to the team. (source: chapter-02-architectural-thinking.md)

The architect is not a full-time developer — they split time between writing/testing source code and the architecture-role work of diagrams, meetings, and more meetings. Owning critical-path code that the team is blocked on means the architecture role starves the development team.

### The fix: delegate the critical path, code business features

The chapter's prescription (source: chapter-02-architectural-thinking.md):

- **Delegate critical path and framework code to the development team.** Ownership belongs with them; it gives them a better understanding of the harder parts of the system.
- **The architect codes a piece of business functionality** — a service or a screen — **one to three iterations down the road.** Not on the critical path. Not blocking anyone.

This produces three benefits:

1. The architect is gaining hands-on experience writing production code, without being a bottleneck.
2. Critical-path and framework code is distributed to the development team, where it belongs.
3. The architect writes the *same* business code the team writes, so they identify with the team's pain around processes, procedures, and the development environment.

## Four fallback techniques

If coding alongside the team isn't possible, Chapter 2 offers four alternative ways to stay hands-on (source: chapter-02-architectural-thinking.md):

### 1. Frequent proof-of-concepts (POCs)

POCs require writing source code *and* help validate architecture decisions by forcing implementation details to surface. The canonical scenario: an architect stuck between two caching solutions builds a working example in each and compares the results. The POC reveals:

- Amount of effort required for the full solution
- Architectural characteristics in practice (scalability, performance, fault tolerance)

**Discipline**: write the best production-quality code possible, even in throwaway POCs. Two reasons (source: chapter-02-architectural-thinking.md):

- Throwaway POC code often lands in the source repository and becomes a reference architecture for others. The last thing an architect wants is their sloppy throwaway code representing their typical work.
- Writing production-quality POC code is itself practice — and avoids the slow drift into bad coding habits.

### 2. Technical-debt and architecture stories

Pick up low-priority stories the development team would otherwise work around. Upside:

- The architect stays hands-on.
- The development team is freed for critical functional stories.
- If the architect doesn't finish the story in an iteration, it generally doesn't jeopardise the iteration.

### 3. Bug fixes

Not glamorous, but it keeps the architect inside the codebase. The side benefit: bug work reveals where issues and weaknesses live, which often exposes problems in the architecture itself (source: chapter-02-architectural-thinking.md).

### 4. Automation and fitness functions

> Look for repetitive tasks the development team performs and automate the process. (source: chapter-02-architectural-thinking.md)

Command-line tools, analysers, checklists, coding-standard validators, code refactoring scripts. The team is grateful; the architect codes.

Automation also includes **architectural analysis and [[architecture-fitness-function|fitness functions]]** to ensure vitality and compliance (source: chapter-02-architectural-thinking.md). The chapter cites ArchUnit for JVM projects, with Chapter 6 providing the full treatment.

### 5. Code reviews

> While the architect is not actually writing code, at least they are involved in the source code. (source: chapter-02-architectural-thinking.md)

The added benefits: ensuring compliance with the architecture (see [[architect-expectations|expectation #4]]) and finding mentoring and coaching opportunities on the team.

## Why this matters

The techniques above are the operational discipline that makes Chapter 2's first aspect of [[architectural-thinking]] — [[architecture-versus-design|architecture versus design]] — workable in practice. Without ongoing hands-on participation:

- The bidirectional architect-developer relationship breaks, and the architecture stops connecting with reality.
- [[architect-expectations|Expectation #4]] (ensuring compliance with decisions) becomes lecture-based rather than evidence-based.
- [[architect-expectations|Expectation #7]] (interpersonal skills) suffers; developers stop trusting an architect who never writes code.
- The architect accumulates the **stale expertise** Chapter 2 warns about in [[technical-breadth-vs-depth]] — making decisions with ancient criteria because they haven't touched real code in years.

Richards and Ford's practice-at-home advice is tacked on at the end of the section: "we recommend practicing coding at home as well" (source: chapter-02-architectural-thinking.md). The in-work techniques are the minimum; personal practice is the supplement.

## Relationship to earlier wiki material

- [[architecture-fitness-function]] — the Chapter 6 coverage of fitness functions is flagged here as a hands-on coding opportunity; writing them is itself a way for the architect to stay in code.
- [[architecture-vitality]] — code reviews and bug-fix work are the evidence-gathering arm of vitality analysis.
- [[architect-expectations]] — expectation #4 (ensuring compliance) and expectation #5 (diverse exposure) both get practical mechanisms here.
- [[technical-breadth-vs-depth]] — this page is the "how to keep some depth while growing breadth" companion to that page's "how to grow breadth."

## Related pages

- [[architectural-thinking]]
- [[architecture-versus-design]]
- [[technical-breadth-vs-depth]]
- [[architect-expectations]]
- [[architecture-vitality]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[fundamentals-of-software-architecture]]
