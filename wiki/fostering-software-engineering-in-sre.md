# Fostering Software Engineering in SRE

**Summary**: Chapter 18's guidance on which projects are worth promoting from one-off tool to a full software-engineering effort, how to staff them, and how to protect the development time they need. The running question: what makes a good candidate, what makes a bad one, and how do you keep engineers doing this kind of work without severing them from production?

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`, `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## What makes a good candidate project

Strong positive signals (source: chapter-18-software-engineering-in-sre.md):

- **Engineers with firsthand domain experience who want to work on it** — the Auxon origin story: an SRE and a TPM who had each done manual capacity planning and understood the pain directly
- **A highly-technical target user base** — internal customers who can file high-signal bug reports during early phases
- **Noticeable benefits** — reducing toil for SREs, improving existing infrastructure, streamlining a complex process
- **Alignment with overall organisational objectives** — so engineering leaders can weigh the impact and advocate for it, both inside their teams and across team boundaries
- **Cross-organisational socialisation and review** early — prevents disjoint or overlapping efforts, and makes staffing and support easier to defend

Chapter 18's frame: a product that "furthers a department-wide objective" is much easier to staff and support than one that doesn't.

## What makes a poor candidate

Red flags (source: chapter-18-software-engineering-in-sre.md):

- **Software that touches many moving parts at once** — too much coupled change for safe iteration
- **Software requiring an all-or-nothing approach** — can't be developed iteratively; high-risk single delivery
- **Overly specific work that benefits only a small percentage of the organisation** — Google's service-aligned SRE team structure makes this the common trap: team incentives favour one service's user experience, not cross-SRE standardisation
- **Overly generic frameworks** — the opposite trap. If the tool tries to be too flexible and too universal, it risks fitting no use case well enough to deliver end-user benefit on a reasonable time frame
- **Grand scope and abstract goals without concrete use cases** — often requires significant development effort for unclear benefit

The balance to strike: **general enough to be shared, specific enough to be useful** — the same duality [[sre-software-development-lessons]] names at the design level.

## The layer-3 load balancer anecdote

Chapter 18 offers one counterexample to illustrate how broad the use case can legitimately be: a layer-3 load balancer originally developed by Google SREs proved so successful over the years that it was **repurposed as a customer-facing product** — Google Cloud Load Balancer (source: chapter-18-software-engineering-in-sre.md).

The moral: cross-organisational utility is a sign something is working, and the upper bound of "appropriate generality" is larger than the instinctive SRE team boundary.

## Staffing

SREs are often generalists, because **breadth-first learning serves the bigger-picture goal** of understanding complex technical infrastructure (source: chapter-18-software-engineering-in-sre.md). They typically have strong coding and software-development skills but may lack experience as part of a product team thinking about customer feature requests.

The anecdote: *"I have a design doc; why do we need requirements?"* — the conventional SRE approach to software as the chapter saw it when the SRE development culture was forming.

The fix: **partner with PMs, TPMs, or SWE-experienced engineers** who know how to run a product team and convert design docs into requirements, roadmaps, and user-facing features. The goal is a team that combines the best of software-product discipline with hands-on production experience.

## Defending development time

**Dedicated, non-interrupted project time is essential** — nearly impossible to write code while thrashing between several tasks per hour (source: chapter-18-software-engineering-in-sre.md).

Protected project time is also one of the strongest **recruiting and retention levers** for SRE software development: engineers want it, and the ability to offer it is what attracts the right people.

Chapter 18: such time must be **aggressively defended**. The operational side will always find reasons to pull engineers back; leadership has to hold the line.

Chapter 29 is the specific chapter about how to hold that line. Its three levers — [[polarizing-time]] (week-scale rotation between project work and interrupts), [[interrupt-role-structuring]] (full-time interrupt roles rather than team-wide distribution), and [[reducing-interrupts]] (ticket scrubs and policy push-back) — are the concrete mechanisms that turn "aggressively defend project time" from an exhortation into a team design. The [[context-switch-cost]] framing — 20 minutes of interrupt destroys a couple of hours of productive work — is what justifies Chapter 18's "nearly impossible to write code while thrashing" statement in arithmetic terms.

## Trajectories

Most SRE software products begin as **side projects** whose utility leads them to grow and become formalised. At that point, one of three paths (source: chapter-18-software-engineering-in-sre.md):

1. Remain a grassroots effort developed in engineers' spare time
2. Become a formal project through structured processes (see [[introducing-sre-software-development]])
3. Gain executive sponsorship from SRE leadership to expand into a fully staffed software-development effort

## The non-negotiable: stay embedded

Chapter 18 is emphatic: **SREs involved in any development effort must continue working as SREs** rather than becoming full-time embedded developers (source: chapter-18-software-engineering-in-sre.md).

The reason: immersion in the world of production is what gives SREs doing development work their invaluable perspective. They are both creator and customer. Lose the creator-customer loop and you lose the defining advantage of developing the tool inside SRE in the first place.

## Cross-book connections

- [[team-autonomy]] (Newman) — protected project time is an autonomy investment; leadership defence of it is the governance side of autonomy
- [[architect-control-spectrum]] (Richards & Ford) — the balance between generalist seed team and in-house specialists is elastic-leadership applied to staffing
- [[code-ownership-models]] (Newman) — SRE-developed software often crosses team boundaries; ownership and contribution norms need explicit design early
- [[skills-self-assessment]] (Newman) — the generalist/specialist mix evolves over a project's life; team-level skill maps help predict when to engage specialists
- [[global-vs-local-optimization]] (Newman) — Chapter 18's warning about service-aligned SRE teams producing overly-specific tools is this principle applied to SRE

## Related pages

- [[software-engineering-in-sre]]
- [[sre-software-development-lessons]]
- [[sre-product-adoption]]
- [[introducing-sre-software-development]]
- [[engineering-work-categories]]
- [[toil-and-engineering-balance]]
- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[interrupt-role-structuring]]
- [[context-switch-cost]]
