# Introducing SRE Software Development

**Summary**: Chapter 18's change-management guide for introducing a software-development model into an existing SRE organisation — an organisational problem as much as a technical one. Recognises that moving from ad hoc tool-writing to shared, formal software engineering is a multi-year change in larger orgs, and lays out four disciplines for making it land.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## The problem this solves

SREs are used to working closely with teammates and quickly analysing and reacting to problems. The natural instinct is to **write some code to meet the immediate need** — which, in a small team, works fine. As the organisation grows, the same instinct produces largely-functional but narrow, single-purpose, unshareable software solutions that lead to duplicated effort and wasted time (source: chapter-18-software-engineering-in-sre.md).

The goal of introducing a formal software-development model is not to stop writing code — it's to convert one-off work into reusable work at the organisation's scale.

Chapter 18's framing question: are you trying to foster better software-development practices inside your team, or to produce results that are usable across teams (possibly as an organisational standard)? The latter takes longer and needs more explicit change management, but has higher payoff.

## The four moves

### 1. Create and communicate a clear message

SREs are skeptical — deliberately so; skepticism is a trait Google hires for (source: chapter-18-software-engineering-in-sre.md). An SRE's initial response to a software-development program will likely be *"that sounds like too much overhead"* or *"it will never work."*

Start by making a compelling case about how the strategy helps SRE. Chapter 18's examples:

- **Consistent, supported software solutions speed ramp-up for new SREs** — fewer bespoke systems for newcomers to learn
- **Reducing the number of ways to perform the same task** lets the whole department benefit from skills any single team developed, making knowledge and effort portable across teams

The signal you've crossed the first hurdle: SREs start asking *how* the strategy will work rather than *whether* it should be pursued.

### 2. Evaluate organisational capabilities

Building useful software means effectively creating a **product team** — with required roles and skills the SRE organisation may not have historically needed (source: chapter-18-software-engineering-in-sre.md):

- Who will play product manager, acting as customer advocate?
- Does the tech lead or project manager have skills and experience to run an agile development process?

Start by borrowing skills already present in the company:

- Ask the product development team for help establishing agile practices via training or coaching
- Solicit consulting time from a product manager to help define requirements and prioritise feature work
- Given a large enough software-development opportunity, make the case to hire dedicated people for these roles — **easier to justify after some positive experimental results**

### 3. Launch and iterate

An SRE software-development program will be **followed by many watchful eyes**. Establish credibility by delivering product value on a reasonable timeline (source: chapter-18-software-engineering-in-sre.md):

- First-round products should aim for **straightforward, achievable targets** — ones without controversy or existing solutions
- Chapter 18's observed cadence: a **six-month rhythm of product update releases** that provide additional useful features. Lets teams focus on identifying the right set of features to build, and then build them while simultaneously learning how to be a productive software-development team
- After initial launch, some Google teams moved to a **push-on-green** model for even faster delivery and feedback

This is the same launch-and-iterate advice the chapter gives for product development ([[sre-software-development-lessons]]), applied to organisational change.

### 4. Don't lower standards

As the new practice ramps up, there's temptation to cut corners. Resist. Hold SRE-developed software to **the same standards as product-development teams' software** (source: chapter-18-software-engineering-in-sre.md):

- *Would you onboard this product if it came from a separate dev team?*
- If the solution enjoys broad adoption, it becomes **critical to SREs performing their jobs** — so reliability is paramount
- Proper code-review practices in place?
- End-to-end or integration testing?
- Have another SRE team **review the product for production readiness** as they would for any other service being onboarded

Chapter 18's warning: it takes a long time to build credibility for SRE software-development efforts, but only a short time to lose it.

## Cross-book connections

- [[kotters-change-model]] (Newman) — Chapter 18's four moves map roughly onto Kotter's urgency / coalition / vision / short-term-wins steps applied to SRE software-development adoption
- [[architecture-governance]] (Richards & Ford) — the "don't lower standards" move is governance applied to internal tooling; onboarding review is the fitness-function gate for SRE software
- [[reorganizing-teams]] (Newman) — introducing a software-development practice is team reorganisation with new roles (PM, product owner); Newman's "don't copy the Spotify model" caution applies
- [[progressive-delivery]] (Newman / Burns) — push-on-green for internal tools is progressive delivery adopted one step at a time as the practice matures
- [[architect-providing-guidance]] (Richards & Ford) — the "clear message" discipline is guidance-over-prescription: help skeptics understand why before telling them what
- [[kotters-change-model]] — also the operative model for move 1's hurdle ("do SREs ask *how* or *whether*")

## Related pages

- [[software-engineering-in-sre]]
- [[fostering-software-engineering-in-sre]]
- [[sre-product-adoption]]
- [[sre-software-development-lessons]]
