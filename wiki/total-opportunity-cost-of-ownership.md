# Total Opportunity Cost of Ownership (TOCO)

**Summary**: The cost of *lost opportunities* that you incur in choosing a technology, architecture, or process. Reis and Housley's second cost lens and their most emphasised one — the part of [[total-cost-of-ownership|TCO]] engineers usually forget.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The concept

Chapter 4 defines TOCO directly (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Total opportunity cost of ownership (TOCO) is the cost of lost opportunities that we incur in choosing a technology, an architecture, or a process.

Any choice inherently excludes other possibilities. If you pick data stack A, you've committed to the benefits of A over all other options — and to the team to support it, training, setup, and maintenance. You've effectively excluded stacks B, C, and D.

"Ownership" here doesn't require long-term purchases of hardware or licenses. **Even in a cloud environment, we effectively own a technology, a stack, or a pipeline once it becomes a core part of our production data processes and is difficult to move away from.**

## The questions TOCO asks

Chapter 4 lists them (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- What happens if data stack A was a poor choice?
- What happens when data stack A becomes obsolete?
- Can you still move to data stack B?
- How quickly and cheaply can you move to something newer and better?
- Does the expertise you've built up on data stack A translate to the next wave?
- Can you swap out components of data stack A and buy yourself some time and options?

## The bear-trap warning

Reis and Housley's signature metaphor (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Inflexible data technologies are a lot like bear traps. They're easy to get into and extremely painful to escape.

The first step to minimising opportunity cost is **evaluating it with eyes wide open**. Data engineers often fail to evaluate TOCO when undertaking a new project — Chapter 4 calls it a "massive blind spot." Teams routinely get stuck with technologies that seemed good at the time and are either inflexible for future growth or simply obsolete.

## How to reduce TOCO

- **Favour [[reversible-vs-irreversible-decisions|reversible decisions]].** The whole point of Principle 7.
- **Favour [[interoperability|interoperable]], [[monolith-vs-modular-data|modular]] stacks.** Components you can swap have low exit cost.
- **Favour [[immutable-vs-transitory-technologies|immutable technologies]] at the base.** Object storage, SQL, bash — things that won't obsolete under your feet.
- **Have an escape plan.** Chapter 4's advice: "Ideally, your escape plan will remain locked behind glass, but preparing this plan will help you to make better decisions in the present and give you a way out if things go wrong in the future."

## Relationship to vendor lock-in

Chapter 4's treatment of [[cloud|single-cloud vs multicloud]] is a direct TOCO application: single-cloud is simpler and cheaper to run day-to-day but accumulates significant lock-in. "In this instance, we're talking about mental flexibility, the flexibility to evaluate the current state of the world and imagine alternatives."

[[data-gravity]] — data-egress costs that make moving data between clouds expensive — is the concrete mechanism by which cloud TOCO accumulates.

## Cross-book framing

- [[cost-of-change]] (Richards and Ford / Booch) is TOCO named at the decision level: architecture decisions are the ones whose cost-of-change is high.
- [[reversible-vs-irreversible-decisions]] is TOCO's decision-theoretic shape: prefer low-TOCO (reversible) decisions.
- [[data-liberation]] (Bellemare) is the microservice-data equivalent — emit events so consumers aren't locked into querying your private store.

## Related pages

- [[technology-selection]]
- [[total-cost-of-ownership]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[immutable-vs-transitory-technologies]]
- [[interoperability]]
- [[monolith-vs-modular-data]]
- [[data-gravity]]
- [[finops]]
- [[principles-of-good-data-architecture]]
