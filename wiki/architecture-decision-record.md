# Architecture Decision Record

**Summary**: A short text file (one to two pages) capturing a single architecture decision in a fixed structure — Title, Status, Context, Decision, Consequences — so the *why* of the decision survives the team that made it. ADRs were evangelised by Michael Nygard (2011 blog post) and marked "adopt" on the ThoughtWorks Technology Radar; they are the canonical answer to the [[laws-of-software-architecture|Second Law of Software Architecture]] (why beats how) and the direct cure for the Email-Driven Architecture anti-pattern.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-19-architecture-decisions.md`

**Last updated**: 2026-04-16

---

## What an ADR is

An **Architecture Decision Record** is a short text file, usually one to two pages, that describes a single architecture decision in a consistent template (source: chapter-19-architecture-decisions.md). ADRs are typically written in Markdown or AsciiDoc and stored next to the source they govern (repo, wiki, or shared directory). Nat Pryce's open-source **ADR-tools** provides a CLI for managing numbering, locations, and supersession.

Nygard's original format has five sections; Richards and Ford recommend two additions (Compliance and Notes), and name Alternatives as a common optional section:

| Section | Purpose |
|---|---|
| Title | Sequentially numbered short phrase describing the decision |
| Status | Proposed, Accepted, or Superseded (plus Request for Comments as a useful extension) |
| Context | The forces at play — what situation is forcing this decision |
| Decision | The decision itself, stated affirmatively, with full justification (the *why*) |
| Consequences | Overall impact — good and bad — plus trade-off analysis |
| Compliance *(recommended)* | How the decision will be measured and governed — manual vs automated fitness function |
| Notes *(recommended)* | Metadata: author, approval date, approver, superseded date, modification history |
| Alternatives *(optional)* | Analysis of rejected alternatives when not already in Context |

## The five sections

### Title

Sequentially numbered plus a short phrase: *"42. Use of Asynchronous Messaging Between Order and Payment Services."* Descriptive enough to remove ambiguity about what was decided; short enough to fit in a list (source: chapter-19-architecture-decisions.md).

### Status

Three core values plus a useful extension:

- **Proposed** — awaiting approval by a higher-level decision maker, the [[architecture-decisions-vs-design-principles|architecture review board]], or another governance body.
- **Accepted** — approved and ready for implementation.
- **Superseded** — changed by a later ADR. The superseded ADR marks *"Superseded by N"* and the superseding ADR marks *"Accepted, supersedes M"*. The paired back-links preserve the historical trail that avoids the inevitable *"what about using messaging?"* question years later. Superseded status always assumes the prior ADR was accepted — a proposed ADR continues to be modified until accepted rather than being superseded.
- **Request for Comments (RFC)** — a Richards-Ford recommended status for draft ADRs circulated for stakeholder review, always with a deadline date (*"Request For Comments, Deadline 09 JAN 2010"*). The deadline prevents the [[choosing-architecture-style|Analysis Paralysis]] anti-pattern where the decision is discussed forever but never made.

The Status section also forces a prior conversation with the lead architect or boss about **what the architect can approve on their own**. Three criteria form a good starting point: **cost** (dollar amount above which approval is required — level-of-effort times the company's FTE rate), **cross-team impact**, and **security** (anything with security implications must go to a higher-level governing body). Once agreed ("costs exceeding €5,000 must be approved by the architecture review board"), the criteria are documented so all architects know their self-approval limits (source: chapter-19-architecture-decisions.md).

### Context

*"What situation is forcing me to make this decision?"* The Context section describes the scenario and concisely names the alternatives. *"The order service must pass information to the payment service to pay for an order currently being placed. This could be done using REST or asynchronous messaging."*

If the alternative analysis is long, promote it to a separate Alternatives section. A side-effect of writing context well is that it **documents the architecture itself** — this is how ADRs end up doubling as architecture documentation (see below).

### Decision

The decision stated in an **affirmative commanding voice**, not a passive opinion. Nygard's phrasing discipline: *"We will use asynchronous messaging between services"* — not *"I think asynchronous messaging between services would be the best choice"* (source: chapter-19-architecture-decisions.md). The latter leaves it unclear whether a decision was even made.

The Decision section is where the **Second Law lives in practice**. It must carry the full justification — both the technical reasoning and the [[laws-of-software-architecture|business justification]]. The book's worked cautionary tale: an early decision to use gRPC between two services with no recorded justification; years later a different architect refactors to messaging for decoupling, unaware that gRPC was chosen specifically for latency reduction at the known cost of tight coupling; upstream timeouts follow.

### Consequences

The overall impact of the decision — good and bad — and the explicit **[[trade-off-analysis|trade-off analysis]]**. Forcing the architect to name the consequences is itself a correctness check: if the negatives outweigh the benefits, the decision should be reconsidered.

The book's worked example: async fire-and-forget messaging to post a review drops request latency from 3,100 ms to 25 ms, at the cost of more complex error handling ("what happens if someone posts a review with bad words?"). That trade-off was discussed with business stakeholders and accepted; recording it in Consequences prevents the argument from being reopened by a reader who doesn't know that context.

## The two recommended additions

### Compliance

Not one of Nygard's five, but Richards and Ford recommend adding it. Compliance forces the architect to decide:

1. Will the decision be measured **manually** or via an automated **[[architecture-fitness-function|fitness function]]**?
2. If automated, what does the fitness function look like, and what code changes are needed to make the decision measurable?

The book's worked example — *"All shared objects used by business objects will reside in the shared services layer"* — is automatable via ArchUnit in Java or NetArchTest in C#. The Compliance section names the fitness function, where the test lives, and when it runs. Note that automation often requires new user stories (e.g. creating a `@SharedService` annotation and applying it to all shared classes); the Compliance section is where those stories are named.

### Notes

Metadata that survives whatever storage system the ADR lives in:

- Original author
- Approval date
- Approved by
- Superseded date
- Last modified date
- Modified by
- Last modification

Even when ADRs live in Git, the authors recommend Notes because not every storage system is version-controlled and useful metadata (who approved) is not always inferrable from commit history (source: chapter-19-architecture-decisions.md).

## Storing ADRs

Each ADR is one file or one wiki page. Three options with trade-offs:

- **In the source repository (Git)** — versioning is free, but (1) not every stakeholder who needs to see a decision has repo access and (2) decisions with scope beyond the application (integration, enterprise-wide) don't belong in any single application repo. Richards and Ford **caution against repo storage for larger organisations** on both grounds.
- **In a wiki** — their recommendation. Each ADR is a wiki page; directory structure mirrors scope.
- **On a shared file server** rendered by wiki or documentation software — equivalent to the wiki option.

Recommended directory structure by scope:

```
application/
  common/          -- decisions applying to all applications
  atp/             -- application-specific ADRs
  pstd/
integration/       -- decisions about communication between apps/services
enterprise/        -- global decisions impacting every system
```

The `application/common/` directory holds things like *"all framework classes carry a `@Framework` annotation"*. The `enterprise/` directory holds things like *"all access to a system database is only from the owning system"* (source: chapter-19-architecture-decisions.md). Names are recommendations — companies adopt whatever naming is consistent for them.

## What ADRs are for

### As documentation

Software architecture documentation has no equivalent to diagramming's C4 Model or The Open Group's ArchiMate. **ADRs fill that gap** (source: chapter-19-architecture-decisions.md):

- The **Context** section describes the area of the system requiring a decision — so writing it documents that part of the architecture.
- The **Decision** section records *why* — the form of documentation Richards and Ford call "by far the best form of architecture documentation."
- The **Consequences** section records the trade-offs made — the most often-missing piece of architecture docs.

### As standards

Most people dislike standards because they feel controlling. ADRs can fix this. The Context section describes the *situation forcing the standard*; the Decision section records what the standard is **and why it must exist**. If the architect cannot justify the standard in the Decision section, *perhaps it should not be a standard at all.* The Consequences section provides a second sanity check on whether the standard should exist. And developers who understand *why* a standard exists are much more likely to follow it without contesting it (source: chapter-19-architecture-decisions.md).

## Why ADRs exist: the three anti-patterns

ADRs are specifically engineered to fix the [[architecture-decision-anti-patterns|three architecture decision anti-patterns]] the chapter names:

- **Covering Your Assets** — fixed by the last-responsible-moment rule plus stakeholder collaboration; ADRs force a decision to be written down, which forces it to be made.
- **Groundhog Day** — fixed by the Decision section's *why* — the rationale that prevents the same decision from being re-litigated.
- **Email-Driven Architecture** — fixed by the ADR being the **single system of record**. Emails may *link* to the ADR but must never carry the decision text.

## Example: ADR 42 → ADR 68

The book's worked supersession example:

```
ADR 42. Use of Asynchronous Messaging Between Order and Payment Services
Status: Superseded by 68
```

```
ADR 68. Use of REST Between Order and Payment Services
Status: Accepted, supersedes 42
```

The history trail preserves both decisions and prevents a future architect from arguing for messaging again without first reading ADR 42's original rationale and ADR 68's reasons for overriding it.

## Relation to other wiki concepts

- [[laws-of-software-architecture]] — the Second Law ("why beats how") is the motivation for ADRs; the Decision section is where the *why* lives.
- [[architecture-decisions-vs-design-principles]] — ADRs capture decisions (rules). Principles are typically documented elsewhere (a design-principles wiki page, coding standards) and enforced via monitoring rather than variance review.
- [[architecture-decision-anti-patterns]] — the three anti-patterns ADRs cure.
- [[architecture-fitness-function]] — ADRs and fitness functions are paired deliverables: the ADR records the decision and its *why*; the fitness function automates compliance with it. Chapter 18 names both as selection-process outputs.
- [[architecture-governance]] — ADR approval workflows (self-approved vs ARB-approved based on cost / cross-team impact / security) are the governance layer around decision-making.
- [[trade-off-analysis]] — the Consequences section is where the trade-off analysis lands as durable artefact.
- [[choosing-architecture-style]] — Chapter 18 names ADRs as the second of three deliverables from style selection (topology, ADRs, fitness functions).
- [[architecture-vitality]] — the Superseded status is the machinery by which architecture vitality is recorded: what was decided, what changed, and why.
- [[reversible-vs-irreversible-decisions]] — the Consequences section is the natural place to note whether a decision is one-way or two-way.

## Related pages

- [[architecture-decisions-vs-design-principles]]
- [[architecture-decision-anti-patterns]]
- [[laws-of-software-architecture]]
- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[trade-off-analysis]]
- [[choosing-architecture-style]]
- [[architecture-vitality]]
- [[fundamentals-of-software-architecture]]
