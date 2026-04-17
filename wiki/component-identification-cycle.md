# Component Identification Cycle

**Summary**: Richards and Ford's five-step iterative loop for deriving [[components]] from requirements. Component design is never a one-shot activity — it's a feedback loop that starts with a rough partitioning and refines it by assigning stories, checking roles, and (crucially) folding in [[architecture-characteristics]]. Step 4, characteristics analysis, is the step that often turns an apparent monolith design into a distributed one.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`

**Last updated**: 2026-04-16

---

## Why iterate

> No one can anticipate all the unknown issues that usually occur during software projects. Thus, an iterative approach to component design is key. (source: chapter-08-component-based-thinking.md)

Software design throws up "unexpected difficulties" — edge cases, contradictory requirements, latent characteristics — that don't surface until you try to fit real stories to candidate components. The first draft of a component breakdown is almost never right; the cycle exists to make that explicit and planned-for.

This matches the wider book position that **all architecture is iterative** because of [[unknown-unknowns]] (Chapter 1). Component identification is one of the places where that principle has an operational loop.

## The five steps

### 1. Identify initial components

Before any code exists, the architect picks a [[technical-vs-domain-partitioning|partitioning strategy]] and sketches top-level components (source: chapter-08-component-based-thinking.md). This is admittedly arbitrary — "the likelihood of achieving a good design from this initial set of components is disparagingly small," which is *why* the rest of the cycle exists. The goal of step 1 is a first draft, not a final design.

### 2. Assign requirements to components

Map user stories / requirements onto the candidate components. The mapping reveals:

- Components with **nothing** assigned — probably don't need to exist.
- Components with **too much** assigned — probably need to be split.
- Requirements that don't fit **anywhere** — new components probably need to be created.

The mapping doesn't need to be exact — the architect is looking for a coarse-grained substrate for tech leads and developers to refine (source: chapter-08-component-based-thinking.md).

### 3. Analyze roles and responsibilities

Cross-check the component-to-requirement mapping against the roles (actors) the system supports. Component granularity should match the granularity of the roles and behaviours. The chapter calls this "one of the greatest challenges for architects" — discovering the right granularity (source: chapter-08-component-based-thinking.md).

### 4. Analyze architecture characteristics

**This is the critical step.** Look at each component through the [[architecture-characteristics|characteristic]] lens. If two components serving similar functions need *materially different* characteristics, they should probably be different components (source: chapter-08-component-based-thinking.md).

The chapter's example: a single `User interaction` component might seem fine from a purely functional view, but if part of the user interaction handles hundreds of concurrent users and another part serves only a handful, the characteristics diverge enough to justify subdivision. The *Going, Going, Gone* walk-through makes this concrete: `BidCapture` started as one component, but once the architect noticed the auctioneer's reliability / availability needs exceeded a bidder's, it split into `BidCapture` + `AuctioneerCapture`.

This step is also the hand-off to the [[architectural-quantum]] analysis: if components have systematically different characteristics, the system probably needs multiple quanta (distributed). If they all converge on one characteristic profile, a monolith is viable.

### 5. Restructure components

Feed the insights from steps 2-4 back into the design. Create new components, consolidate redundant ones, split overloaded ones. Loop.

## Why step 4 is load-bearing

Most teams do a version of steps 1-3 intuitively. Step 4 is the step that distinguishes architectural thinking from functional decomposition. A purely functional decomposition (what does the system *do*?) can produce a perfectly reasonable monolith-shaped answer. Layering in characteristics (*how* must each part do its thing?) is where monolith-vs-distributed decisions emerge naturally rather than being imposed top-down.

See [[identifying-architecture-characteristics]] for the source-of-characteristics treatment that Chapter 5 provides — and which step 4 of this cycle consumes.

## The cycle is generic

The chapter calls this a "generic architecture exposition cycle" — specific domains may insert steps (security review, audit, regulatory sign-off) or alter it (source: chapter-08-component-based-thinking.md). The five steps are the backbone; specialised environments specialise it.

## Relationship to the development process

The cycle is **process-agnostic**. It fits formal Joint Application Design, waterfall-style analysis, Agile story cards, or any hybrid (source: chapter-08-component-based-thinking.md). What matters is that the architect is running *some* version of the loop — not which requirements-gathering process upstream feeds it.

## Related pages

- [[components]]
- [[technical-vs-domain-partitioning]]
- [[architecture-characteristics]]
- [[identifying-architecture-characteristics]]
- [[architectural-quantum]]
- [[entity-trap]]
- [[event-storming]]
- [[architectural-thinking]]
- [[unknown-unknowns]]
- [[fundamentals-of-software-architecture]]
