# SRE-Dev Collaboration

**Summary**: Chapter 31's model for how SRE teams collaborate with product development teams. The central claim: collaboration is best when it starts **early in the design phase, ideally before any code has been committed**, because SREs are uniquely positioned to make recommendations about architecture and software behaviour that are painful or impossible to retrofit. Work is tracked via the OKR process, and for some service SRE teams this consultation is the main activity. The worked example is [[dfp-to-f1-migration]].

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`, `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The core thesis

Collaboration between the product development organisation and SRE is *"really at its best when it occurs early on in the design phase, ideally before any line of code has been committed"* (source: chapter-31-communication-and-collaboration-in-sre.md).

The reasoning:

- SREs are best placed to make recommendations about architecture and software behaviour that can be **quite difficult (if not impossible) to retrofit**.
- Having that voice present *in the room* when a new system is being designed *"goes better for everyone."*

This is the chapter's framing of why SRE is a design activity, not merely a deployment-and-operations activity. The reliability-relevant decisions get made early; SRE needs to be involved at that stage if it wants to influence them.

## The OKR process

Chapter 31 names **Objectives & Key Results (OKRs)** as the tracking mechanism for this kind of work (source: chapter-31-communication-and-collaboration-in-sre.md, citing Kla12). OKRs give SRE-dev collaborations a concrete shape: agreed objectives with measurable key results, reviewed periodically, so that "SRE consults on the design" becomes a tracked commitment rather than informal goodwill.

## Service SRE teams' mainstay

For some service teams, this kind of collaboration *"is the mainstay of what they do — tracking new designs, making recommendations, helping to implement them, and seeing those through to production"* (source: chapter-31-communication-and-collaboration-in-sre.md).

This sharpens the definition of what service SRE teams are for: they are not on-call operators with a coding habit; they are software engineers whose work sits **inside** the product's design and delivery cycle.

## What SRE brings

The chapter frames the collaboration as bringing together two complementary skill sets (source: chapter-31-communication-and-collaboration-in-sre.md, from the DFP-to-F1 case study):

- **Product development teams** are typically more familiar with the **Business Logic** of the software, and in closer contact with Product Managers and the "business need."
- **SRE teams** usually have more expertise about **infrastructure components** — libraries for distributed storage, databases, RPC, etc. — because SREs often reuse the same building blocks across services and learn the caveats that make software scale and run reliably over time.

Neither team holds both halves. Joint design in the room means BL and infrastructure decisions get made with each other's constraints visible.

## The atmosphere that makes it work

*"The best designs and the best implementations result from the joint concerns of production and the product being met in an atmosphere of mutual respect"* (source: chapter-31-communication-and-collaboration-in-sre.md).

The chapter's explicit claim: *"simply having someone in charge of reliability, without also having the complete skill set, is not enough."* SRE's leverage with product development comes from peer engineering status — SRE engineers can write, review, and own code at the same level as product developers. Without that peer status, reliability concerns get filtered through a translator and lose resolution.

## The production meeting as the recurring venue

Once SRE and product development are collaborating on a service, the [[production-meetings|production meeting]] is the weekly recurring venue. The chapter is explicit that product development teams should attend, and that *"If your relationship is such that you cannot invite your product development partners, you need to fix that relationship"* (source: chapter-31-communication-and-collaboration-in-sre.md). The meeting is where operational data flows back to drive design decisions in the ongoing relationship.

## Early involvement and the handoff model

The chapter's early-involvement thesis is the inverse of the traditional handoff model: in the handoff model, developers build and then hand the operating system over to a separate operations team, who discover the reliability implications at the moment they have the least leverage to change them. SRE's model is to be present at the design, own infrastructure-adjacent parts of the implementation, and participate through to production. The DFP-to-F1 case study ([[dfp-to-f1-migration]]) is a worked example of this full-cycle involvement; the [[sre-discipline|SRE discipline]] page and Chapter 32 develop the broader model.

Contrast [[architecture-versus-design]] and [[architect-role-intersections]] (Richards & Ford) — both make similar arguments about architects remaining connected to implementation. Chapter 31's version is the operations-side sibling argument: the reliability discipline only has leverage if it participates in design.

Chapter 32 makes the early-involvement thesis concrete in engagement terms. The [[early-engagement-model|Early Engagement Model]] is precisely "collaboration that starts early in the design phase" packaged as an SRE engagement pattern (source: chapter-32-the-evolving-sre-engagement-model.md). The benefits Chapter 31 frames abstractly — fewer future disputes over design choices, cheaper fixes, smoother launches — are the same benefits Chapter 32 enumerates from the engagement-model angle. [[prr-continuous-improvement|PRR Continuous Improvement]] then carries the collaboration forward into the steady state.

## Worked example

[[dfp-to-f1-migration]] — the migration of DoubleClick for Publishers' main database from MySQL to F1. Joint SRE + product-development collaboration from the start of the project. SRE drove the infrastructure design (indexing, extract/join/filter, capacity planning), product development owned the business-logic changes, weekly meetings synchronised the tracks, and the production rollout was seamless to users.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[production-meetings]]
- [[sre-team-composition]]
- [[dfp-to-f1-migration]]
- [[sre-discipline]]
- [[software-engineering-in-sre]]
- [[launch-coordination-engineering]]
- [[architect-role-intersections]]
- [[architecture-versus-design]]
- [[reliable-product-launches]]
- [[sre-engagement-model]]
- [[early-engagement-model]]
- [[prr-continuous-improvement]]
