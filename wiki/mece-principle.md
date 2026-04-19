# MECE Principle

**Summary**: **Mutually Exclusive, Collectively Exhaustive** — a concept borrowed from technology-strategy consulting that Ford, Richards, Sadalage, and Dehghani recommend architects use when building a list of options for [[trade-off-analysis]]. MECE is the discipline that prevents the two most common category errors in trade-off analysis: comparing things that aren't really the same kind of thing (the *overlap* failure), and leaving important options out of the comparison (the *gap* failure).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-15-build-your-own-trade-off-analysis.md`

**Last updated**: 2026-04-19

---

## What the acronym means

A MECE list of options covers a decision space completely, with no overlaps and no holes (source: chapter-15-build-your-own-trade-off-analysis.md):

- **Mutually Exclusive** — none of the compared items overlap in capability. The [[trade-off-analysis|trade-off analysis]] is only valid if the things being compared are actually the same category of thing.
- **Collectively Exhaustive** — the comparison covers every meaningful option in the decision space. Leaving out an obvious capability turns the exercise into a false dichotomy.

The book visualises this as a set of non-overlapping tiles covering a rectangle — no gaps, no double-covered regions.

## The two failure modes

### The overlap failure

The book's canonical example: comparing a **simple message queue** to an **enterprise service bus** is *not* a valid comparison. An ESB contains a message queue but also dozens of other components (mediation, transformation, orchestration, etc.) — they are not the same category of thing. Any trade-off table produced from that comparison is noise. If the real question is *which messaging substrate?*, the architect must first reduce the ESB to its messaging capability and compare that to the simple queue; or add the non-messaging capabilities explicitly as their own comparable items.

This failure mode tends to come from **asymmetric familiarity**: the architect knows the small thing well and the big thing vaguely, and compares them as if they were the same size of thing.

### The gap failure

The book's example: a team evaluating high-performance message queues that considers only an ESB and a simple queue but not **Kafka** is not exhausting the space (source: chapter-15-build-your-own-trade-off-analysis.md). The resulting decision is defended by comparisons that were never run.

The ecosystem evolves constantly — new capabilities arrive regularly. The collectively-exhaustive check is the scheduled reminder to re-scan the decision space for **newly available options** before committing. For long-term decisions this check should be repeated periodically (see [[trade-off-analysis]] — iterative trade-off analysis).

## Why MECE matters for architects

Ford et al. introduce MECE in Chapter 15 as one of the **trade-off techniques** that make [[trade-off-analysis]] honest (source: chapter-15-build-your-own-trade-off-analysis.md). Its role in the method:

- **Before** running the comparison — MECE is how the option list is sanity-checked. Are these the same category of thing? Have we missed anything?
- **During** the comparison — if a dimension shows wildly unequal ratings, MECE asks whether the items are really comparable or whether one of them has capabilities the other doesn't have at all.
- **After** the comparison — if a decision looks obvious, the MECE check against gaps is a final "did we miss an option?" guard against lock-in to a false dichotomy.

## Relationship to model-vs-reality

MECE is a property of the **model** the architect builds, not of reality. Real systems have capability overlaps, ambiguous categorisations, and options the market hasn't surfaced yet. MECE is the discipline that makes the *model* clean enough to reason about — **it is not a claim that reality is MECE.** The *out-of-context* trap and *model relevant domain cases* techniques elsewhere in Chapter 15 are the counterweights that re-inject the messiness MECE temporarily strips out.

## Relation to other wiki concepts

- [[trade-off-analysis]] — MECE lists are a prerequisite technique. If the option list isn't MECE, the trade-off matrix is measuring the wrong things.
- [[least-worst-trade-offs]] — the "least worst" choice is only defensible against the options actually compared; a non-exhaustive list can make a middling option look best.
- [[architecture-decision-record]] — the Context / Alternatives sections of an ADR are where the MECE-ness of the option list becomes visible; if the Alternatives section has gaps or overlapping entries, the decision's defensibility erodes.
- [[structured-and-rational-decision-making]] — MECE is a structured-decision hygiene check; it belongs with the cognitive-bias countermeasures architects use to avoid premature convergence.

## Related pages

- [[trade-off-analysis]]
- [[least-worst-trade-offs]]
- [[architecture-decision-record]]
- [[structured-and-rational-decision-making]]
- [[software-architecture-the-hard-parts]]
