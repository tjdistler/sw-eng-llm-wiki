# Engineering Work Categories

**Summary**: Chapter 5's four-way accounting scheme for an SRE's time: *software engineering*, *systems engineering*, *toil*, and *overhead*. The first two count toward the 50%-engineering half of the [[toil-and-engineering-balance|engineering balance]]; the last two do not. The taxonomy exists so the 50% cap can be measured honestly.

**Sources**: `raw/site-reliability-engineering/chapter-05-eliminating-toil.md`, `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`, `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## Why a taxonomy at all

The 50% engineering cap is only meaningful if SREs and managers agree on what counts as engineering. Chapter 5 draws a bright line by naming the four categories SRE time falls into, giving examples for each, and saying exactly which ones are engineering (source: chapter-05-eliminating-toil.md).

> Engineering work is novel and intrinsically requires human judgment. It produces a permanent improvement in your service, and is guided by a strategy. It is frequently creative and innovative, taking a design-driven approach to solving a problem — the more generalized, the better.

The test is whether the work helps the team (or the SRE organisation) **handle a larger service, or more services, at the same staffing level**. That is the sublinear-scaling goal the 50% cap exists to protect.

## The four categories

### Software engineering

Writing or modifying code, with associated design and documentation (source: chapter-05-eliminating-toil.md). Examples:

- Automation scripts
- Tools and frameworks
- Service features for scalability and reliability
- Modifications to infrastructure code for robustness

Unambiguously engineering. Counts toward the 50%.

### Systems engineering

Configuring production systems, modifying configurations, or documenting them in a way that produces **lasting improvements from a one-time effort** (source: chapter-05-eliminating-toil.md). Examples:

- Monitoring setup and updates
- Load balancer configuration
- Server configuration and OS-parameter tuning
- Architecture / design / productionisation consulting with developer teams

Also engineering. Counts toward the 50%. The "lasting improvement from a one-time effort" phrase is the operative distinction from toil: tuning a load balancer once per quarter to absorb growth is systems engineering; running a script every week to restart a stuck balancer is toil.

### Toil

Work directly tied to running a service that is manual, repetitive, automatable, tactical, enduring-value-free, and O(n) with service growth (source: chapter-05-eliminating-toil.md). Full definition on [[toil-and-engineering-balance]].

Does not count toward the 50% engineering half; it is the thing the 50% cap limits.

### Overhead

Administrative work **not directly tied to running a service** (source: chapter-05-eliminating-toil.md). Examples:

- Hiring
- HR paperwork
- Team and company meetings
- Bug-queue hygiene
- Snippets (short weekly work summaries — Google-specific)
- Peer reviews and self-assessments
- Training courses

Not toil (because it's not service-running work) and not engineering (because it isn't novel, strategic, or producing permanent service improvements). Has to be budgeted for separately; cannot be used either to bloat the engineering number or as a reason to exceed the toil cap.

## The boundary cases

Three pairs that Chapter 5 explicitly disambiguates (source: chapter-05-eliminating-toil.md):

- **Grungy work that produces a permanent improvement** — e.g. cleaning up the entire alerting configuration and removing clutter. This is *systems engineering*, not toil, despite being unpleasant.
- **Running an automation script manually** — still *toil*. The script being automation does not make the invocation engineering; hands-on human time is what's counted.
- **First- or second-time work** — *engineering*, not toil, even if the task would be toil at scale. Toil requires repetition.

A useful mental sharpening from Chapter 5's footnote: before classifying something as "not toil because it requires human judgement," ask whether the judgement is intrinsic to the problem or an artefact of poor design. If the latter, the work is still toil until the redesign ships.

## Interrupts threaten the engineering half (Chapter 29)

Chapter 29's [[context-switch-cost]] argument adds a quality dimension to the taxonomy: even when the *hours* allocation is under the 50% cap, the engineering half can fail to produce engineering output if those hours are fragmented. A day with two 20-minute interrupts has (on the chapter's arithmetic) about four hours of productive work destroyed, regardless of how those four hours would have been classified.

The implication for this taxonomy: **protecting the 50% engineering half requires more than a time-ledger**. It requires [[polarizing-time]] so the engineering hours are contiguous enough to reach [[cognitive-flow-state|flow]], and [[interrupt-role-structuring]] so interrupts don't leak into the project-work weeks. Without these policies, the same timesheet that satisfies the 50% rule can produce very little actual software-engineering or systems-engineering output.

## How the 50% is applied

Every SRE is expected to average **≥ 50% on software engineering + systems engineering** over a few quarters or a year (source: chapter-05-eliminating-toil.md). Toil is spiky, so individual quarters may dip below; a sustained dip over the long haul is the signal that something is wrong and the team needs to step back and diagnose it.

The [[toil-and-engineering-balance|arithmetic floor]] from on-call rotations (≈33% for a 6-person rotation, ≈25% for an 8-person rotation) means the engineering half has comparatively little headroom before toil crowds it out, which is why the taxonomy has to be tight: misclassifying overhead or repetitive drudgery as "engineering" silently violates the cap.

## Software engineering within SRE as a category

Chapter 18 develops the **software engineering** category into a named organisational practice. The chapter's argument: not every bit of code SREs write is a "software engineering project" — one-off scripts and quick hacks are still valuable, but **fully-fledged software engineering projects** (with a product-based mindset, a target user base, and a roadmap for future plans) are a distinct and larger thing (source: chapter-18-software-engineering-in-sre.md).

Chapter 18 adds three implications for the taxonomy:

- **Software engineering work is both a category and a career path**. Chapter 18 frames SRE software-development projects as a "career development opportunity" and an "outlet for engineers who don't want their coding skills to get rusty." Long-term project work provides needed balance against interrupts and on-call.
- **The 50% cap funds it**. The engineering half of an SRE's time is where non-trivial software development projects must live. Chapter 18 is the answer to "what should we actually *do* with that 50%" beyond automation scripts.
- **Staying embedded matters**. Chapter 18 is explicit that SREs doing software development must **continue working as SREs** — not become full-time embedded developers. The hands-on production exposure is what makes the software any good. See [[software-engineering-in-sre]].

## Related pages

- [[toil-and-engineering-balance]]
- [[sre-discipline]]
- [[sre-tenets]]
- [[sysadmin-approach]]
- [[software-engineering-in-sre]]
- [[fostering-software-engineering-in-sre]]
- [[auxon]]
- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[context-switch-cost]]
