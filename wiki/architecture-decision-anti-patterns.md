# Architecture Decision Anti-Patterns

**Summary**: Richards and Ford name three anti-patterns that emerge when architects make decisions — **Covering Your Assets**, **Groundhog Day**, and **Email-Driven Architecture** — and note that they emerge progressively: overcoming each one exposes the next. Together they motivate the existence of [[architecture-decision-record|ADRs]] as the canonical cure.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-19-architecture-decisions.md`

**Last updated**: 2026-04-16

---

## The progression

Andrew Koenig's definition of an anti-pattern is *"something that seems like a good idea when you begin but leads you into trouble"*; an alternative definition is *"a repeatable process that produces negative results"* (source: chapter-19-architecture-decisions.md). Richards and Ford's three decision anti-patterns form a progression — fixing each one reveals the next:

1. **Covering Your Assets** — no decisions get made.
2. **Groundhog Day** — decisions get made but the *why* isn't captured, so the same decision is re-litigated endlessly.
3. **Email-Driven Architecture** — decisions get made *with* rationale but are scattered across inboxes, so the people who need to implement them never see them.

An effective architect has to beat all three.

## 1. Covering Your Assets

**Symptom**: the architect avoids or defers a decision out of fear of making the wrong choice. Analysis continues; meetings happen; development teams wait.

**Two fixes** (source: chapter-19-architecture-decisions.md):

- **Wait for the last responsible moment** — the point at which enough information exists to justify the decision, but no later (waiting longer holds up development teams or slides into the Analysis Paralysis anti-pattern). *Last responsible*, not *last possible*.
- **Collaborate continuously with the development teams implementing the decision** — the architect cannot possibly know every detail of every technology, so close collaboration surfaces implementation issues early enough to adjust the decision without rework.

**Worked example from the chapter**: an architect decides that all product reference data is replicated via in-memory read-only caches across services, with the catalog service owning the primary replica. Justification: reduced coupling and avoided cross-service calls. Close collaboration with implementation teams surfaces that some services' scaling requirements don't leave room for the in-process memory the replicated cache needs. The architect adjusts the decision — quickly, because they were collaborating, not handing-off.

## 2. Groundhog Day

Named for the Bill Murray movie where February 2 repeats indefinitely.

**Symptom**: once a decision is made, nobody records *why*. Six weeks or six months later the same conversation happens again. And again. The decision was reached, but the reasoning was not preserved, so nobody can tell whether the reasoning still applies to today's situation.

**Fix**: record **both technical and business justifications** for every decision (source: chapter-19-architecture-decisions.md). Technical-only is half the answer.

**Worked example from the chapter**: *"Split the monolith into services because each service uses fewer VM resources and can be maintained and deployed separately."* That's a technical justification. The missing business justification might be *deliver new business functionality faster (time to market)* or *reduce cost of new feature development*. The technical reason alone doesn't tell a business stakeholder why they should pay for the refactoring.

**The business-justification litmus test**: if a decision has no business justification, maybe it isn't a good decision to make. The four most common business justifications Richards and Ford name are:

- **Cost**
- **Time to market**
- **User satisfaction**
- **Strategic positioning**

Picking the right one depends on what the business stakeholders actually care about. A cost-savings justification can land badly with stakeholders whose priority is time to market.

Groundhog Day is the direct target of the [[laws-of-software-architecture|Second Law of Software Architecture]] (why beats how) and of [[architecture-decision-record|ADRs]] — the Decision section of an ADR exists specifically to capture the rationale that prevents re-litigation.

## 3. Email-Driven Architecture

**Symptom**: decisions are made, justified, and circulated by email — and then lost, forgotten, missed by new team members, or overridden by a later email that not everyone received. *Email is a great tool for communication but a poor document repository system.* (source: chapter-19-architecture-decisions.md)

**Two rules for communicating architecture decisions** (source: chapter-19-architecture-decisions.md):

**Rule 1: never put the decision text in the body of an email.** Doing so creates multiple systems of record (the email *and* the eventual documentation). Important details, especially justification, routinely fall out during the copy into email. And if the decision is superseded, there's no way to reach every inbox that received the earlier text.

Instead, the email should name the *nature* of the decision and the *context* plus a link to the single system of record (typically a wiki page or repo file — i.e., an [[architecture-decision-record|ADR]]):

> Hi Sandra, I've made an important decision regarding communication between services that directly impacts you. Please see the decision using the following link…

**Rule 2: notify only the people the decision directly impacts.** The phrasing *"that directly impacts you"* is also the litmus test — if the decision doesn't directly impact someone, don't send it to them. This stops the tendency to CC everyone and dilute signal.

## Why the progression matters

The progressive structure has a practical consequence: an architect fixing their decision process has to fix the anti-patterns *in order*. A team with Covering Your Assets can't benefit from an ADR template (no decisions to document). A team that makes decisions but doesn't justify them (Groundhog Day) won't fix the situation by moving the un-justified decisions into ADRs — the Decision section of each ADR will just be a restatement of the un-justified decision. Only once decisions *get made* and *are justified* does the storage-and-distribution problem (Email-Driven Architecture) become the binding constraint, at which point ADRs-in-a-wiki is the canonical fix.

## Relation to other wiki concepts

- [[architecture-decision-record]] — ADRs are engineered specifically to cure these three anti-patterns. The Decision section carries the justification (fixes Groundhog Day); the stored-in-a-wiki-not-in-email storage model (fixes Email-Driven Architecture); the last-responsible-moment rule + continuous collaboration (fixes Covering Your Assets).
- [[laws-of-software-architecture]] — the Second Law (why beats how) is the underlying principle Groundhog Day violates.
- [[reversible-vs-irreversible-decisions]] — the last-responsible-moment rule is easier to apply to reversible decisions than to irreversible ones; the anti-pattern for Bezos-style one-way-door decisions looks different (more analysis is cheaper than a wrong decision).
- [[trade-off-analysis]] — the business-justification discipline in Groundhog Day's fix is where the trade-off analysis meets the stakeholders who authorise it.
- [[architecture-decisions-vs-design-principles]] — the base page on decisions vs principles; this page is the "what goes wrong" companion to its "what to do" framing.

## Related pages

- [[architecture-decision-record]]
- [[architecture-decisions-vs-design-principles]]
- [[laws-of-software-architecture]]
- [[trade-off-analysis]]
- [[reversible-vs-irreversible-decisions]]
- [[fundamentals-of-software-architecture]]
