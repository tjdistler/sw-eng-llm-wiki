# Identifying Architecture Characteristics

**Summary**: Chapter 5 of *Fundamentals of Software Architecture* describes how an architect actually derives the ranked, short list of [[architecture-characteristics|characteristics]] a system needs. Characteristics come from three places — **domain concerns**, **explicit requirements**, and **implicit domain knowledge** — and the architect's distinctive skill is translating between the vocabulary of stakeholders and the vocabulary of "-ilities."

**Sources**: `raw/fundamentals-of-software-architecture/chapter-05-identifying-architectural-characteristics.md`

**Last updated**: 2026-04-16

---

## The three sources

Chapter 4 defined what an architecture characteristic *is*; Chapter 5 answers *where they come from* (source: chapter-05-identifying-architectural-characteristics.md):

1. **Domain concerns** — the things business stakeholders care about, expressed in their own language (mergers, user satisfaction, time to market, competitive advantage). The architect must **translate** these into -ilities.
2. **Explicit requirements** — characteristics named outright in a requirements document ("the system must sustain 10,000 concurrent users"). Covered by the [[architecture-characteristics#explicit-vs-implicit-characteristics|explicit/implicit split]] in Chapter 4.
3. **Implicit domain knowledge** — characteristics that never appear in any document but every competent architect infers from knowing the domain. The university-registration example: nominally 1,000 students × 10 hours of registration, but every architect who has ever met a student knows the real load is 1,000 students in the last 10 minutes. No requirement will ever say that.

The chapter spends most of its pages on (1) and (3); (2) is the easiest of the three.

## Extracting characteristics from domain concerns

Domain stakeholders and architects speak different languages. Stakeholders talk about **mergers and acquisitions, user satisfaction, time to market, competitive advantage**. Architects talk about **scalability, interoperability, fault tolerance, learnability, availability**. Without a translation step, the two groups talk past each other: the architect has no idea how to build for "user satisfaction," and the stakeholder has no idea why the architect keeps bringing up "interoperability."

Table 5-1 in the chapter is the translation (source: chapter-05-identifying-architectural-characteristics.md):

| Domain concern | Architecture characteristics |
|---|---|
| Mergers and acquisitions | interoperability, scalability, adaptability, extensibility |
| Time to market | agility, testability, deployability |
| User satisfaction | performance, availability, fault tolerance, testability, deployability, security |
| Competitive advantage | agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | simplicity, feasibility |

### The "agility ≠ time to market" trap

The most load-bearing warning in this section: **agility is not a single characteristic.** Time to market decomposes into *agility + testability + deployability*. Focusing on just one ingredient is "like forgetting to put the flour in the cake batter." An architect who hears "time to market" and designs only for fast coding has failed — without automated tests and a push-button deploy, the code can be written fast but cannot reach production fast.

The fund-pricing example in the chapter makes the same point in reverse. A stakeholder says "due to regulatory requirements, end-of-day fund pricing must complete on time." An ineffective architect hears **performance** and stops. A good architect hears performance **plus availability** (performance doesn't matter if the system is down), **plus scalability** (more funds over time), **plus reliability** (can't crash mid-run), **plus recoverability** (must restart where it left off if it does crash), **plus auditability** (the prices have to be correct, not just fast). One domain concern, six characteristics.

The moral is the same as [[architecture-characteristics#trade-offs-and-the-least-worst-principle|Chapter 4's least-worst principle]]: characteristics interlock. A shallow translation from one domain concern to one characteristic almost always misses dependencies.

## The "pick three" consensus trick

A recurring stakeholder request is to rank the final list of characteristics in priority order. Richards and Ford say this is usually a **fool's errand** (source: chapter-05-identifying-architectural-characteristics.md):

- Stakeholders rarely agree on an ordering of every characteristic.
- The exercise wastes time and generates frustration and disagreement.

The practical alternative: **have stakeholders pick the top three, in any order.** This is much easier to reach consensus on, surfaces the real priorities quickly, and — crucially — gives the architect the frame for every later [[trade-off-analysis|trade-off analysis]]. When a choice has to be made between two characteristics and both are outside the top three, the decision is easy. When one is in the top three, the other is not, the decision is easy. The top-three list *is* the architecture's priority system.

## Extracting characteristics from requirements

Some characteristics are stated outright. Others lurk in requirements worded as domain facts — the architect has to decode them.

The [[architecture-katas#silicon-sandwiches-the-books-worked-kata|Silicon Sandwiches]] kata in the chapter is the worked example. A national sandwich shop wants online ordering; users are "thousands, perhaps one day millions"; it must integrate with mapping services, offer national and local specials, support mobile, and accept multiple payment methods. The shops are franchised; the company plans to expand overseas; they want to hire inexpensive labour.

Walking the requirements, the chapter derives:

- **Scalability** — from "thousands, perhaps one day millions" users. The requirement never used the word; it gave a number. *Architects must often decode domain language into engineering equivalents.*
- **Elasticity** — never stated in the requirements. An architect with sandwich-shop domain knowledge infers the bursty lunch/dinner traffic pattern. Scalability and elasticity are distinct: scalability is steady-state concurrent users; elasticity is the ability to absorb bursts. Hotel reservations are scalable-not-elastic; concert-ticket sales are both.
- **Performance** — implied by all of the above; an online ordering system with poor performance at peak is a dead product.
- **Reliability** — implied by the external mapping-service integration. But the chapter adds a warning: don't build in **unnecessary brittleness**. If traffic information is down, should the site fail or just work slightly worse? The latter — so reliability here is *graceful degradation*, not "every dependency must be up."
- **Customizability** — derived from three separate requirements (national specials, local specials, locally overridden traffic info). This is the case where the chapter splits **architecture vs design**: customizability can be supported structurally (a microkernel style with a plug-in architecture) or behaviourally (Template Method inside any architecture). Which is better? Trade-off dependent. See [[architecture-versus-design]].

Requirements that do **not** raise a characteristic matter too. "If the shop offers a delivery service, dispatch the driver" — no special characteristic. "Mobile-device accessibility" — design decision (mobile-optimized web app) with some page-load-time performance sub-goals. "Online payments" — security is already implicit, but the payment flow is delegated to a third-party processor, so no *special* structural security is needed. *Architects must be wary of over-specifying characteristics.* Every extra characteristic adds design cost and interacts with every other one.

### Implicit characteristics in the same example

Alongside the requirements-derived ones, Silicon Sandwiches has implicit characteristics that every online system has:

- **Availability** — users must be able to reach the site.
- **Reliability** — sessions must not drop mid-order.
- **Security** — implicit in every system, but stays a hygiene concern here because payments are delegated. If payments were handled in-app, security would rise to an architecture characteristic (the Chapter 4 three-criteria test).

See [[architecture-characteristics#explicit-vs-implicit-characteristics|the explicit/implicit split]].

## Try to drop one

After a first-pass list of characteristics, the chapter's last recommended move is to ask: **which is the least important? If I had to eliminate one, which would it be?**

This is a sharpening exercise. It forces the architect to revisit the "critical or important to application success" criterion from Chapter 4. In the Silicon Sandwiches case, the answer turns out to be *customizability* (push it into application design) or *performance* (still care about it, but don't let it outrank scalability and availability). The top-three-consensus trick and the drop-one trick are two sides of the same move: the architect is not looking for the *right* set, just the *fewest* set.

This is a recurring idea in the book: **there is no best architecture, only a least worst collection of trade-offs** ([[laws-of-software-architecture|First Law]]). Chapter 5's contribution is the specific set of techniques — translation, top-three, drop-one, implicit inference — for producing a concrete short list.

## Don't over-specify: the Vasa

The chapter's case study in the other direction is the **Vasa**, a Swedish warship built 1626–1628. The king wanted the most magnificent ship ever. Most ships of the era had one deck — the Vasa would have two. Most were either troop transports or gunships — the Vasa would be both. The cannons were twice the size of those on comparable ships. The shipbuilders had misgivings but couldn't say no. On its maiden voyage, the Vasa fired a cannon salute, capsized from being top-heavy, and sank in Stockholm harbour.

The moral for architecture: **over-specifying characteristics is just as dangerous as under-specifying them**. Every characteristic added to the design adds weight; at some point the ship stops floating. The "generic architecture that supports every characteristic" anti-pattern the chapter warns against is the Vasa re-implemented in software. See also the [[architecture-characteristics#italy-ility-custom-characteristics|Italy-ility]] story in the Chapter 4 hub — the opposite failure mode, under-specification of a custom characteristic.

## Collaboration, not solo work

A running sub-theme: the architect should **not** be making these identifications alone. The chapter calls out the [[architect-expectations|ivory-tower architect]] anti-pattern explicitly. Mobile strategy, payment design, customizability approach — all should be decided alongside developers, tech leads, UX, domain analysts, and project managers. Architecture characteristics are the team's priorities, not the architect's private list.

## Related pages

- [[architecture-characteristics]] — what characteristics are (Chapter 4 hub)
- [[architecture-katas]] — Ted Neward's practice format for this skill
- [[architecture-katas#silicon-sandwiches-the-books-worked-kata|silicon-sandwiches]] — the worked example for requirements-driven derivation
- [[architecture-versus-design]] — the architecture-or-design question raised by customizability
- [[trade-off-analysis]] — the top-three list as the frame for later trade-offs
- [[laws-of-software-architecture]] — least-worst principle applied to the short list
- [[architect-expectations]] — expectation #3 (understand the business domain); ivory-tower warning
- [[fundamentals-of-software-architecture]]
