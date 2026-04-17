# Architecture Katas

**Summary**: A timeboxed exercise invented by Ted Neward (and adapted by Neal Ford and Mark Richards) for practising the skill of deriving [[identifying-architecture-characteristics|architecture characteristics]] from a domain problem. A small team gets a domain description, a user volume estimate, requirements, and "additional context"; they have 45 minutes to produce a design; the other teams vote on it.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-05-identifying-architectural-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-24-developing-a-career-path.md`

**Last updated**: 2026-04-16 (Chapter 24 cross-references added)

---

## Origin

From Japan and martial arts, a **kata** is an individual training exercise emphasising proper form and technique. Ted Neward applied the idea to architecture practice, reasoning from Fred Brooks's line:

> How do we get great designers? Great designers design, of course.

The frustration Neward was answering: most architects get fewer than half a dozen greenfield architectural opportunities in a career. A kata is a way to practise the skill in the intervening years. Neal Ford and Mark Richards adapted and updated the original site (source: chapter-05-identifying-architectural-characteristics.md).

## Format

Each kata has four predefined sections:

- **Description** — the overall domain problem the system should solve.
- **Users** — expected number and/or types of users.
- **Requirements** — domain/business-level requirements, as an architect might expect from domain users or subject-matter experts.
- **Additional context** (Neal Ford's addition) — implicit knowledge about the problem domain that isn't in the requirements but affects the design. This is where the [[identifying-architecture-characteristics|implicit domain knowledge]] source of characteristics lives.

The exercise is timeboxed: small teams have **45 minutes** to produce a design, then present to the other teams, who vote on the best architecture.

## Why it works as a training exercise

The kata format is deliberately under-specified. The architect-in-training has to:

1. **Translate domain language into -ilities** — extracting characteristics from the Description and Users fields.
2. **Read the requirements for hidden characteristics** — scalability from user counts, reliability from integration points, etc.
3. **Use the additional-context section** — inferring implicit characteristics from domain knowledge.
4. **Prioritise** — pick the fewest characteristics that matter (the [[architecture-characteristics#trade-offs-and-the-least-worst-principle|least-worst principle]]).
5. **Make trade-offs** — every design choice has alternatives, and voting forces the team to defend them.

This is the full loop that Chapter 5 describes for real projects, compressed into 45 minutes and repeatable.

Chapter 24 returns to katas as the **deliberate practice loop** for the architecture skill itself — the answer to Ted Neward's lament that architects get fewer than half a dozen greenfield opportunities in a career. The chapter also fields the common "is there an answer key?" question: the authors tried to build one from live-training student designs and abandoned the effort because the artefacts were incomplete — teams captured the *how* (topology, decisions) but didn't have time to capture the *why* in [[architecture-decision-record|ADRs]], and "the why is much more interesting because it contains the trade-offs they considered" (source: chapter-24-developing-a-career-path.md). This is [[laws-of-software-architecture|Second Law]] reasoning applied to the practice loop: a kata design without its trade-off rationale is half the artefact. See [[architect-career-path]] for the chapter's full daily/weekly/career-long practice stack in which katas are the career-long layer.

## How to run one

Chapter 5 encourages a lightweight approach: **host a brown-bag lunch**. Gather aspiring architects, pick a kata from the site, run the 45-minute exercise, and have an experienced architect evaluate the design and trade-off analysis — either on the spot or as short written feedback afterwards. The designs won't be elaborate; the point is the reasoning, not the artefact.

## Silicon Sandwiches (the book's worked kata)

Chapter 5 uses a kata called **Silicon Sandwiches** as its worked example for deriving characteristics from requirements.

**Description**. A national sandwich shop wants to enable online ordering in addition to its current call-in service.

**Users**. Thousands, perhaps one day millions.

**Requirements**.

- Users place orders, receive a pickup time, and get directions (integrated with external mapping services that include traffic).
- If the shop offers delivery, dispatch a driver.
- Mobile-device accessibility.
- National daily promotions/specials.
- Local daily promotions/specials.
- Accept payment online, in person, or on delivery.

**Additional context**.

- Sandwich shops are franchised, each with a different owner.
- Parent company has near-future plans to expand overseas.
- Corporate goal: hire inexpensive labour to maximise profit.

The full walk-through of how each line produces (or doesn't produce) an architecture characteristic lives on [[identifying-architecture-characteristics#extracting-characteristics-from-requirements|the identifying-characteristics page]]. The short version: the requirements yield **scalability, elasticity, performance, reliability (graceful-degradation flavour), customizability**; the implicit set adds **availability, reliability, security**; some requirements (mobile, payments, delivery dispatch) yield no special characteristic.

## Related pages

- [[identifying-architecture-characteristics]] — the Chapter 5 techniques this exercise drills
- [[architecture-characteristics]] — what a characteristic is (Chapter 4 hub)
- [[trade-off-analysis]] — the defence-your-choices part of the voting
- [[architect-expectations]] — "have exposure to multiple technologies, frameworks, platforms, and environments" (expectation #5)
- [[architect-career-path]] — Chapter 24's deliberate-practice framing for katas
- [[architecture-decision-record]] — the missing half of the answer-key problem: why matters more than how
- [[fundamentals-of-software-architecture]]
