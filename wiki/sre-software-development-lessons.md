# SRE Software Development Lessons

**Summary**: Chapter 18's catalogue of practices distilled from [[auxon|Auxon]]'s development — how to build SRE-developed software under uncertainty. The short version: **launch and iterate**, approximate where bounds aren't known, stay modular where requirements are fuzzy, design at a general-enough level that customers don't have to commit to your whole ecosystem to get value.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## Stay embedded

The Auxon team kept SREs on call for several Google services throughout development — the developers remained customers of their own product. When it failed, they were directly affected. Feature requests came from their own firsthand experience (source: chapter-18-software-engineering-in-sre.md).

Beyond the product-quality benefit, this **buys credibility**: the tool is obviously legitimate within SRE because the developers live in the same world as the users. Chapter 18 treats this as non-negotiable. See [[software-engineering-in-sre]] for the organisational-level form of the same rule: SREs doing software development must continue to work as SREs.

## Approximation over perfection

When bounds of the problem aren't well-understood, build a **simplified component** that demonstrates viability and replace it later (source: chapter-18-software-engineering-in-sre.md):

- Auxon's early solver was the **"Stupid Solver"** — heuristic-based, not optimising anything — because the team wasn't yet sure how much linear-programming could buy. The Stupid Solver proved the vision was achievable and let development continue while understanding matured.
- The solver interface was abstracted so the Stupid Solver could be swapped out. Later, confidence in a unified linear-programming model let them replace it without disruption.

The rule: approximate where you must, but **leave a swap point**. Don't bake the approximation into the rest of the design.

## Design for fuzzy requirements

Software with uncertain requirements is a frustrating starting point but not a showstopper. Chapter 18's recipe: use the fuzziness as an incentive for **generality and modularity** (source: chapter-18-software-engineering-in-sre.md).

### Agnostic integration

Auxon was supposed to integrate with Google's automation systems to enact allocation plans directly — but the automation landscape was in flux with many competing approaches. Rather than bind Auxon to any one tool, the team shaped the **Allocation Plan to be universally useful** so each automation system could integrate on its own terms.

This "agnostic" approach became Auxon's single most important adoption lever. Customers could use Auxon without switching to a particular turnup tool, forecasting tool, or performance-data tool. The onboarding message was: *come as you are; we'll work with what you've got.*

### Modular interfaces

The machine-performance model was hidden behind a single interface. Users could plug in different models of future machine power. Later, the team supplied a simple machine-performance modelling library that worked within the same interface.

The rule for both: when requirements will move, **hide what will change behind a stable interface**. Future changes don't force a rewrite.

## Launch and iterate

Chapter 18's closing theme — and the old motto it quotes — is **launch and iterate** (source: chapter-18-software-engineering-in-sre.md):

- Don't wait for the perfect design
- Keep the overall vision in mind while moving ahead with design and development
- When you encounter areas of uncertainty, design the software to be flexible enough that a higher-level process or strategy change doesn't incur huge rework cost
- Stay grounded by making sure general solutions have a real-world-specific implementation that demonstrates utility

The balance the chapter names: **general enough to survive change, specific enough to deliver immediate value**. Over-generality is as much a failure mode as under-generality.

## What not to do

The chapter doesn't frame these negatively, but the anti-patterns implied by the recipe are worth naming:

- **Over-designing the solver before the need is clear** — the Stupid Solver anecdote is a rebuke of the engineer's instinct to build the fanciest thing first
- **Tying the tool to one integration partner** — once you've onboarded a customer whose upstream tool doesn't exist, you've either lost that customer or locked yourself into a vendor relationship
- **Shipping frameworks without concrete implementations** — Chapter 18 is explicit: general solutions need a real-world implementation that demonstrates their utility. Pure framework is worse than no framework

## Cross-book connections

- [[evolutionary-architecture]] (Richards & Ford) — launch-and-iterate is the SRE-software form of evolutionary architecture; the Stupid Solver is the incremental-change affordance, the abstracted solver interface is the fitness-function surface
- [[information-hiding]] (Parnas via Newman) — the abstracted solver interface, agnostic Allocation Plan, and swappable machine-performance model are all applications of Parnas's rule: stable interfaces hide what changes
- [[independent-deployability]] (Newman) — the agnostic design lets Auxon evolve independently of upstream and downstream tools; same property, module-to-module scale rather than service-to-service
- [[minimal-apis]] — the Auxon Allocation Plan is an example of a minimal, well-understood interface that accommodates many clients
- [[consumer-driven-contracts]] (Newman) — the agnostic approach *prevented* consumer coupling by choice; CDCs are how you catch it happening on accident

## Related pages

- [[auxon]]
- [[software-engineering-in-sre]]
- [[sre-product-adoption]]
- [[fostering-software-engineering-in-sre]]
- [[minimal-apis]]
- [[modularity]]
