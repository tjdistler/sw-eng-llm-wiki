# Simplicity (SRE)

**Summary**: Chapter 9 of *Site Reliability Engineering* (Max Luebbe) argues that **software simplicity is a prerequisite to reliability**. The chapter is short and declarative: every line of code is a liability, boring is a virtue, APIs and releases should be minimal, and modularity with loose coupling is the architectural enabler. Simplicity is presented as the opposite of accidental complexity, with SRE teams responsible for pushing back against complexity they did not ask for.

**Sources**: `raw/site-reliability-engineering/chapter-09-simplicity.md`

**Last updated**: 2026-04-17

---

## The framing quote

Chapter 9 opens with C.A.R. Hoare's Turing Award observation (source: chapter-09-simplicity.md):

> The price of reliability is the pursuit of the utmost simplicity.

The rest of the chapter is the SRE-specific elaboration. The central tension Luebbe names is between **stability** and **agility**: a perfectly stable system is one that never changes, but a useful system must evolve. SRE's job is to keep these two in balance.

## The chapter's concepts, each catalogued separately

The chapter moves through seven short sections. Each has been filed as its own page so it can be linked from specific practices elsewhere in the wiki:

- [[system-stability-vs-agility]] — the governing tension: a system in a vacuum is perfectly stable; useful systems must change; SRE's job is to keep the two in balance
- [[virtue-of-boring]] — "unlike a detective story, the lack of excitement, suspense, and puzzles is actually a desirable property of source code"; essential vs accidental complexity (Brooks); the SRE mandate to push back on accidental complexity
- [[negative-lines-of-code]] — every line of code is a liability; source control makes deletion safe; commented-out code and permanently-disabled flags are time bombs; the Knight Capital cautionary tale
- [[minimal-apis]] — Saint-Exupery's "perfection is attained when there is no longer anything to take away"; small APIs are easier to understand, test, and improve; a small API is a hallmark of a well-understood problem
- [[release-simplicity]] — smaller batches of changes are easier to debug; releases as gradient descent; the direct Ch 9 restatement of the Ch 8 [[high-release-velocity|high-velocity]] argument

## Modularity as the architectural enabler

Chapter 9 extends the object-oriented rules-of-thumb about modularity to distributed systems (source: chapter-09-simplicity.md):

> Expanding outward from APIs and single binaries, many of the rules of thumb that apply to object-oriented programming also apply to the design of distributed systems. The ability to make changes to parts of the system in isolation is essential to creating a supportable system. Specifically, loose coupling between binaries, or between binaries and configuration, is a simplicity pattern that simultaneously promotes developer agility and system stability.

Three concrete consequences Luebbe draws:

1. **Bug fixes can be pushed independently.** If a component of a larger system has a bug, it can be fixed and deployed without rebuilding or redeploying the rest.
2. **APIs must themselves be modular.** A single change to an API can force every consumer to rebuild. API versioning lets consumers upgrade on their own schedule.
3. **No "util" or "misc" binaries.** Just as a grab-bag class is poor object-oriented practice, a util binary is poor distributed-system practice. A well-designed distributed system consists of collaborators, each with a clear purpose.

Data formats are modular too — protocol buffers were designed with backward and forward compatibility as a central goal (source: chapter-09-simplicity.md). See [[protocol-buffers]] and [[backward-forward-compatibility]].

The distributed-system modularity argument connects to [[modularity]] (Richards & Ford's theoretical framing), [[coupling]] (Newman's four types), [[information-hiding]] (Parnas), and [[microservices]] (the deployment-independence payoff).

## The "I won't give up my code!" section

Chapter 9 acknowledges that engineers form emotional attachments to code they wrote, and objects to the common objections when deletion is proposed (source: chapter-09-simplicity.md):

- "What if we need it later?" — source control already solves this.
- "Why not comment it out?" — dead code creates distraction and confusion as surrounding files evolve.
- "Why not gate it behind a flag?" — code gated by a flag that is always disabled is a time bomb.

The Knight Capital incident (SEC, 2013) is the canonical example of the time-bomb case: dormant code re-activated by a reused configuration flag caused a ~$440M trading loss in 45 minutes. See [[negative-lines-of-code]] for the fuller treatment.

## The closing summary

Luebbe closes with the chapter's one-line thesis:

> Software simplicity is a prerequisite to reliability. We are not being lazy when we consider how we might simplify each step of a given task. Instead, we are clarifying what it is we actually want to accomplish and how we might most easily do so. Every time we say "no" to a feature, we are not restricting innovation; we are keeping the environment uncluttered of distractions so that focus remains squarely on innovation, and real engineering can proceed. (source: chapter-09-simplicity.md)

## Cross-book connections

- [[accidental-complexity]] (Richards & Ford / Kleppmann) — Chapter 9 is the SRE-specific application of Brooks's essential-vs-accidental distinction; the "push back on accidental complexity" mandate is the operational form of the architect's role Richards and Ford describe
- [[modularity]] (Richards & Ford) — Chapter 9 extends the logical-grouping framing to distributed systems; the no-util-binary rule is Constantine's low-cohesion warning at binary granularity
- [[coupling]] (Newman) — Chapter 9's "loose coupling between binaries" is the distributed-system application of Newman's deployment-coupling analysis
- [[information-hiding]] (Newman / Parnas) — Chapter 9's minimal-API advice is Newman's "expose as little as possible" rule, motivated by the Saint-Exupery quote rather than by Parnas
- [[independent-deployability]] (Newman) — Chapter 9's "bug fixes pushed independently" is the payoff half of the same property
- [[high-release-velocity]] (Ch 8) — Chapter 9's release-simplicity section restates the Ch 8 argument from a different angle: the reason small releases are better is the same reason small changes in general are better
- [[microservices]] (Newman / Bellemare) — the architectural style that treats Chapter 9's modularity advice as a design premise rather than a best practice
- [[monitoring-simplicity]] (Ch 6) — Chapter 6's monitoring-specific simplicity discipline is a specialisation of Chapter 9's general argument
- [[unix-philosophy]] (Kleppmann) — "do one thing and do it well" is the same impulse half a century earlier; small programs that compose are the tool-level version of small services that compose

## Related pages

- [[system-stability-vs-agility]]
- [[virtue-of-boring]]
- [[negative-lines-of-code]]
- [[minimal-apis]]
- [[release-simplicity]]
- [[accidental-complexity]]
- [[modularity]]
- [[coupling]]
- [[information-hiding]]
- [[monitoring-simplicity]]
- [[high-release-velocity]]
- [[protocol-buffers]]
- [[backward-forward-compatibility]]
- [[site-reliability-engineering]]
