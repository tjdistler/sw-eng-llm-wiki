# Architecture Decisions vs Design Principles

**Summary**: Two of the four dimensions of the Richards-Ford [[software-architecture-definition|definition of software architecture]]. A **decision** is a hard-and-fast rule that constrains construction. A **principle** is a guideline that informs choice without forcing it. Distinguishing them matters because each requires different governance. Chapter 19 adds the process and documentation layer: how to decide *which* decisions are architecturally significant, how to justify them, and how to record them as [[architecture-decision-record|ADRs]] so the *why* survives.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-software-architecture/chapter-19-architecture-decisions.md`

**Last updated**: 2026-04-16
---

## Architecture decisions

Architecture decisions define **rules** for how a system should be constructed. They form the constraints of the system and direct development teams on what is and is not allowed (source: chapter-01-introduction.md).

Example: *in a layered architecture, only the business and services layers may access the database; the presentation layer is forbidden from making direct database calls.* The decision controls change — schema changes can happen without impacting the presentation layer because the presentation layer does not depend on the schema directly.

Decisions have an escape hatch: **variance**. If a specific part of the system cannot implement the decision due to some constraint, the team files a variance request, typically reviewed by an **architecture review board (ARB)** or by a chief architect in organisations without an ARB (source: chapter-01-introduction.md). The variance is either approved (with trade-offs documented) or denied. This is how rules stay sharp without becoming impossible — the exceptions are explicit and reviewed rather than silently taken.

## Design principles

Design principles are **guidelines** rather than rules. They cannot cover every possible situation, but they express the preferred approach and let developers pick the right tool for each specific case (source: chapter-01-introduction.md).

Example: *prefer asynchronous messaging between microservices to improve performance.* A rule could never enumerate every communication need — some calls must be synchronous (real-time validation), some must be request/response for semantic reasons, some must be streamed. The principle nudges the default toward asynchronous while leaving the developer free to use REST or gRPC where they fit.

## Why the distinction matters

Treating a guideline as a rule creates friction: developers who hit a legitimate exception must file variances for things the architect never intended to forbid, and the ARB wastes time on non-decisions. Treating a rule as a guideline allows erosion: individual developers deviate for local reasons and the architectural property the rule was meant to preserve (e.g. change isolation) quietly dies.

The right move at decision time is to ask: *must* this hold everywhere, or do I just *prefer* it? The answer determines whether it is a decision or a principle and whether variance review or trust-the-developer is the governance model.

## Governance mechanisms

- **Human review**: ARB evaluates variance requests; architect communicates decisions and principles to teams in writing.
- **Automated enforcement**: tests and linters fail builds that violate decisions. Ford names this family **[[architecture-fitness-function|fitness functions]]** — tests whose failure means an architectural characteristic has been violated. Decisions tend to map to hard fitness functions (unit-test-style pass/fail); principles map to observability (metrics, trends) rather than gates.

## When is a decision *architecturally significant*? (Chapter 19)

Many architects assume that any decision involving a specific technology is merely a "technical decision" rather than an architecture decision. Richards and Ford push back: if the technology directly affects an architecture characteristic (e.g., a database choice driven by scalability), it is an architecture decision (source: chapter-19-architecture-decisions.md).

Michael Nygard's term **architecturally significant** names the test. A decision is architecturally significant if it affects any of:

| Factor | What it means |
|---|---|
| **Structure** | The patterns or styles of architecture in use. *Example*: sharing data between microservices affects each service's [[bounded-context]] and therefore the system's structure. |
| **Non-functional characteristics** | The [[architecture-characteristics|"-ilities"]] important to the system. If a technology choice impacts performance and performance matters, it's an architecture decision. |
| **Dependencies** | Coupling between components or services, which drives scalability, modularity, agility, testability, reliability, and more. |
| **Interfaces** | How services are accessed and orchestrated — gateways, integration hubs, service buses, API proxies. Includes contract definition and the versioning / deprecation strategy. |
| **Construction techniques** | Platforms, frameworks, tools, and processes that might look technical but affect an architectural property. |

A decision failing all five is probably just a technical decision. Passing even one means it deserves an [[architecture-decision-record|ADR]].

## The five factors of an architecture decision (Chapter 19)

Once a decision is identified as architecturally significant, Richards and Ford argue an architect has to address five factors when making it. The first is the trigger; the remaining four are what must be captured (source: chapter-19-architecture-decisions.md):

1. **Is it architecturally significant?** (the gate above)
2. **Justification (the *why*).** The most important part. The [[laws-of-software-architecture|Second Law]] lives here. Must include both a technical rationale and a **business justification** — cost, time to market, user satisfaction, or strategic positioning. If there is no business justification, reconsider whether the decision should be made at all.
3. **Trade-offs.** Every decision is the First Law in miniature — what are you giving up? This becomes the Consequences section of the ADR and anchors [[trade-off-analysis]].
4. **Assumptions.** What must hold for this decision to remain correct? Assumptions that later stop holding are the most common cause of a decision becoming a superseded ADR.
5. **Impact.** Who does this decision affect? Which parts of the system, which teams, which stakeholders? The answer determines who gets notified — only the people the decision *directly impacts* (see [[architecture-decision-anti-patterns|Email-Driven Architecture]]).

These five factors are what an [[architecture-decision-record|ADR]] is structurally engineered to capture — Title identifies the decision, Status tracks its governance state, Context covers significance and alternatives, Decision carries the justification, and Consequences carries the trade-offs, assumptions, and impact.

## What goes wrong — and how ADRs fix it

Richards and Ford catalogue [[architecture-decision-anti-patterns|three decision anti-patterns]] that emerge progressively as an architect's decision practice matures:

- **Covering Your Assets** — avoiding the decision. Fix: last-responsible-moment rule plus close collaboration with implementation teams.
- **Groundhog Day** — making decisions without recording *why*, so the same discussion repeats forever. Fix: always capture both technical and business justification.
- **Email-Driven Architecture** — decisions scattered across inboxes. Fix: one single system of record (an ADR), linked to from emails rather than duplicated in them.

The cure for all three is the **[[architecture-decision-record|Architecture Decision Record]]** — a structured, stored, justified record of each decision, in the canonical Nygard template (Title / Status / Context / Decision / Consequences) plus the Richards-Ford-recommended Compliance and Notes sections.

## Relation to other wiki concepts

- [[architecture-vitality]] — decisions and principles drift over time unless actively maintained; structural decay is what happens when you stop.
- [[evolutionary-architecture]] — Ford's "fitness function" language comes from his *Building Evolutionary Architectures* book; decisions and principles are what fitness functions protect.
- [[laws-of-software-architecture]] — the [[laws-of-software-architecture|Second Law]] ("why beats how") applies directly: record why a decision is a rule (not a principle), or a future team cannot tell.
- [[architect-expectations]] — expectation #4 is *ensure compliance with decisions*; compliance is easier when decisions and principles are correctly distinguished.

## Related pages

- [[architecture-decision-record]]
- [[architecture-decision-anti-patterns]]
- [[software-architecture-definition]]
- [[architecture-characteristics]]
- [[architect-expectations]]
- [[architecture-vitality]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[laws-of-software-architecture]]
- [[trade-off-analysis]]
- [[fundamentals-of-software-architecture]]
