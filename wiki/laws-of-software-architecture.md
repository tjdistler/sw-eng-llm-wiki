# Laws of Software Architecture

**Summary**: Richards and Ford's two unifying laws that run through *Fundamentals of Software Architecture*. First law: **everything in software architecture is a trade-off**. Second law: **why is more important than how**.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`, `raw/fundamentals-of-software-architecture/chapter-19-architecture-decisions.md`, `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`, `raw/software-architecture-the-hard-parts/chapter-15-build-your-own-trade-off-analysis.md`

**Last updated**: 2026-04-19
---

## First Law: everything is a trade-off

> Everything in software architecture is a trade-off. — *First Law of Software Architecture* (source: chapter-01-introduction.md)

Nothing in architecture lives on a clean spectrum where one option dominates. Every decision balances opposing forces — performance against simplicity, scalability against consistency, evolvability against stability, team autonomy against global coherence.

**Corollary**: if an architect thinks they have found something that isn't a trade-off, they probably just haven't identified the trade-off yet (source: chapter-01-introduction.md).

The law is why this wiki is full of pages like [[cap-theorem]], [[reversible-vs-irreversible-decisions]], [[robustness-vs-resilience]], [[schema-on-read-vs-write]], [[replicated-sharded-service]], and dozens of others whose entire content is a named tension. The book's architectural-styles chapters (10–18) each carry a "star rating" across [[architecture-characteristics]] precisely so that trade-offs become explicit and comparable rather than buried in prose.

Chapter 2 develops the applied form of this law as [[trade-off-analysis]] — the discipline of enumerating benefits *and* disadvantages on each candidate solution before deciding, with the auction-system topic-vs-queues case as the worked example (source: chapter-02-architectural-thinking.md). The closing Rich Hickey quote is the warning that programmers tend to know the benefits of everything and the trade-offs of nothing; architects have to know both.

## Second Law: why beats how

> Why is more important than how. — *Second Law of Software Architecture* (source: chapter-01-introduction.md)

Given an existing system with no documentation, a competent architect can usually reverse-engineer *how* it works from the code and topology. They cannot reverse-engineer *why* the team made the particular choices they made versus plausible alternatives. The rationale — which trade-offs were considered, which characteristics were prioritised, which constraints were binding — is the load-bearing knowledge, and it evaporates unless it is captured.

Richards and Ford discovered this while running architecture workshops: they preserved the topology diagrams students produced but not the reasoning, and found the diagrams alone were nearly useless a week later (source: chapter-01-introduction.md).

The Second Law is the motivation for **[[architecture-decision-record|Architecture Decision Records]]** (Chapter 19) — a lightweight written artefact that captures context, decision, and consequences per decision, so the *why* survives the team that made the decision. The Decision section of an ADR is where the Second Law lives in practice: the chapter's worked cautionary tale is a years-old un-justified gRPC choice being refactored to messaging for decoupling, at which point upstream timeouts fire because the original gRPC choice was specifically for latency reduction — a fact nobody had recorded (source: chapter-19-architecture-decisions.md). Chapter 19 also names the [[architecture-decision-anti-patterns|three decision anti-patterns]] (Covering Your Assets, Groundhog Day, Email-Driven Architecture) that ADRs exist to cure, with Groundhog Day being the Second Law's direct counter-example.

## The *Hard Parts* restatement

The authors' follow-up book *Software Architecture: The Hard Parts* (2021) restates both laws and draws out the operational consequence: if the First Law holds, then the architect's job is not to find *the best* design but the **least worst combination of trade-offs** — see [[least-worst-trade-offs]]. The Second Law then explains why this combination has to be documented: without the *why*, the next architect can only see a design that looks suboptimal and cannot tell which trade-offs were deliberate (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md).

The book adds a pointed corollary to both laws: **for architects, every problem is a snowflake.** The exact combination of team, environment, business drivers, and constraints is usually unique in the world, so searching for a pre-made answer rarely works. Fred Brooks's 1986 "No Silver Bullet" is invoked to reinforce the point: *"There is no single development, in either technology or management technique, which by itself promises even one order of magnitude improvement..."* The two laws are the constructive answer to that absence — architecture advances by documenting trade-offs, not by discovering silver bullets.

### Chapter 15 — the First Law made operational

*Hard Parts* Chapter 15 closes the book with the most explicit restatement of the First Law the authors have written: *"everything in software architecture is a trade-off"* — **thus, choosing a fundamental dimension like synchronicity first limits future choices** (source: chapter-15-build-your-own-trade-off-analysis.md). The law is not decoration; it is the operational reason architecture decisions have to be **iterated** — each decision closes off or opens up the next layer of decisions, and the architect cannot skip ahead.

The chapter also sharpens the law into an **anti-evangelism stance**. If every architecture decision is a trade-off, then anyone selling something as having no downside — a silver bullet, a shocking new capability, an "always use X" rule — is either oversold or under-examined. The First Law is why the architect's role is **objective arbiter of trade-offs**, not fan. See [[least-worst-trade-offs]] and [[trade-off-analysis]] for the full Ch 15 technique catalogue (qualitative analysis, [[mece-principle|MECE lists]], the out-of-context trap, relevant-domain modelling, bottom-line-over-evidence, and avoiding snake oil / evangelism).

## How the laws compose

The two laws interlock:

- The First Law says every decision is a choice among trade-offs.
- The Second Law says the value of capturing a decision lies in capturing *which* trade-offs were identified and *why* this side of them was chosen.

Together they reframe the architect's job. The output is not "the architecture" as a static artefact — it is a stream of trade-off decisions plus the documented reasoning behind each one. That framing runs through every subsequent chapter.

## Relation to other perspectives in the wiki

- Newman's migration work in [[reversible-vs-irreversible-decisions]] is the First Law applied to migration choices: one-way vs two-way doors.
- [[cost-of-change]] is the First Law applied to sequencing: push expensive experiments toward the whiteboard.
- [[accidental-complexity]] is often where the First Law hides — a seemingly universal best practice turns out to have a context cost that wasn't priced in.

## Related pages

- [[software-architecture-definition]]
- [[architect-expectations]]
- [[architecture-decisions-vs-design-principles]]
- [[architecture-decision-record]]
- [[architecture-decision-anti-patterns]]
- [[architecture-characteristics]]
- [[evolutionary-architecture]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[accidental-complexity]]
- [[architectural-thinking]]
- [[trade-off-analysis]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
- [[least-worst-trade-offs]]
- [[mece-principle]]
