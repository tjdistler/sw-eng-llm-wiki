# SRE Discipline

**Summary**: Site Reliability Engineering is Google's answer to service management: staff the operations function with software engineers and let them replace manual work with code. Treynor Sloss's one-line definition: *SRE is what happens when you ask a software engineer to design an operations team*.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`, `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`, `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`, `raw/site-reliability-engineering/chapter-34-conclusion.md`

**Last updated**: 2026-04-17

---

## Origin

Benjamin Treynor Sloss joined Google in 2003 and was asked to run a "Production Team" of seven engineers. His prior career was entirely software engineering, so he designed the group the way he — as an SRE — would have wanted it to work. That team is the ancestor of Google's present-day SRE organisation, which still carries the imprint of having been designed by a career software engineer (source: chapter-01-introduction.md).

## Team composition

Google's SRE hiring is split into two tracks (source: chapter-01-introduction.md):

- **50–60% standard Google Software Engineers** — people who passed the normal SWE interview pipeline unchanged.
- **40–50% near-SWE candidates** — candidates who were within 85–99% of the SWE skill bar and possessed technical skills that are rare in the SWE pipeline but valuable for SRE. The two most sought-after are **UNIX system internals** and **Layer 1–3 networking**.

Google tracks career progression for both groups and has found no practical performance difference. The mix tends to produce designs that clearly synthesise multiple skill sets.

## The selection filter

What unites both tracks is a predisposition: SREs (source: chapter-01-introduction.md)

1. will quickly become bored performing tasks by hand; and
2. have the software engineering skills to write the automation that replaces those tasks — even when the solution is complicated.

This is a deliberate hiring stance, not a happy accident. You cannot staff SRE with people who are content to run runbooks; if you do, you end up back in the [[sysadmin-approach|sysadmin approach]] with a different job title.

## Shared intellectual background with developers

Because SREs are hired through (or close to) the SWE pipeline, they share academic and intellectual background with the rest of the engineering organisation. This enables two things (source: chapter-01-introduction.md):

- Easy transfers between product development and SRE — cross-training both groups over time.
- A working vocabulary and risk model that is compatible with the dev side, rather than the sysadmin-vs-developer gulf that drives the [[sysadmin-approach|ops-dev conflict]].

## Running operations as an engineering problem

SREs are doing what has traditionally been operations work, but *using engineers with software expertise and banking on the fact that these engineers will design and implement automation to replace human labour*. The explicit goal is systems that are **automatic, not just automated** (source: chapter-01-introduction.md) — systems that basically run and repair themselves.

The mechanism that enforces this stance is the [[toil-and-engineering-balance|50% engineering-focus cap]]: no more than half of any SRE's time is allowed to go to tickets, on-call, and manual tasks. Cross that line and ops work gets pushed back to the product development team until the balance is restored.

## Cost and scaling

Google's stated advantages of the SRE model (source: chapter-01-introduction.md):

- SRE teams are characterised by **rapid innovation** and **large acceptance of change** — because they are the ones modifying code to make the system run itself.
- SRE teams are **relatively inexpensive** compared to a traditional ops team supporting the same service.
- The number of SREs needed to run, maintain, and improve a system **scales sublinearly** with the size of the system. A pure-ops team, by contrast, scales linearly with traffic.

## Challenges

The SRE model has its own problems (source: chapter-01-introduction.md):

- **Hiring** is hard: SRE competes directly with product-development hiring, and the dual coding + systems-engineering bar narrows the pool further.
- **Industry information is thin** (at least as of 2016) — the discipline is new, so practices have to be invented locally.
- **Management support must be real**, not nominal. Some SRE practices — for example, halting releases once the [[error-budget]] is depleted — will not survive without executive backing.

## Software engineering within SRE

Chapter 18 sharpens the discipline's self-understanding: SREs don't just write automation — they **run full software-engineering projects** that solve internal production problems. [[auxon|Auxon]], Google's [[intent-based-capacity-planning|intent-based capacity planner]], is the case study. Chapter 18's argument:

- Firsthand production experience makes SREs the right authors of tools that solve production problems
- SRE-supported services grow exponentially while SRE headcount grows linearly or slower — perpetual tool development is the only way to close that gap
- Development work is also a **career development** and **retention lever** — engineers who want to keep their coding skills sharp need the outlet
- The non-negotiable: engineers working on SRE software-development projects **must continue working as SREs**. Losing the creator-customer loop costs more than it saves

See [[software-engineering-in-sre]] for the full framing, [[fostering-software-engineering-in-sre]] for project selection, and [[engineering-work-categories]] for where this counts toward the 50% engineering half.

## Scaling humans faster than machines (Chapter 28)

Chapter 28's governing maxim captures the operational-scale precondition for sublinear SRE growth (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> As SRE, you have to scale your humans faster than you scale your machines.

The [[sre-discipline|sublinear scaling]] claim above assumes newly hired SREs reach full productivity quickly. Chapter 28 is the operational manual for making that assumption hold: a deliberate onboarding blueprint (see [[sre-onboarding]]) that trains reverse-engineering, statistical-comparative thinking, and improvisation as the three core SRE attributes, culminating in a structured handoff to on-call via shadow and reverse-shadow rotations.

Without this kind of investment, the "bored by manual work" selection filter cannot be trusted to produce competent on-callers on its own. The filter is necessary; the curriculum is what makes it sufficient.

## Scaling the discipline through engagement models (Chapter 32)

Chapter 32 develops the scaling argument from a different direction — not how fast new SREs reach productivity (Ch 28), but how much *service* each SRE can reach. The evolution of the [[sre-engagement-model|engagement model]] from the [[simple-prr-model|Simple PRR Model]] through the [[early-engagement-model|Early Engagement Model]] to the [[frameworks-and-sre-platform|Frameworks and SRE Platform]] structure is the discipline's structural answer to chronic hiring constraints (source: chapter-32-the-evolving-sre-engagement-model.md):

> Hiring experienced, qualified SREs is difficult and costly. . . . Once SREs are hired, their training is also a lengthier process than is typical for development engineers. Finally, the SRE organization is responsible for serving the needs of the large and growing number of development teams that do not already enjoy direct SRE support.

Frameworks are the structural lever that breaks the staffing barrier: services built on SRE-validated infrastructure get production-quality behaviour by construction, and SRE-supported production features reach services that would never have warranted full SRE engagement. The [[shared-responsibility-engagement|shared-responsibility model]] that frameworks unlock also changes the staffing curve — platform teams scale with platform size, not service count.

This is the long-range reading of the "sublinear scaling" claim: it's not just about automation replacing toil for a given service; it's about the discipline scaling by *not* engaging most services directly.

## The compact-team aspiration (Chapter 34)

Benjamin Lutch's closing chapter (source: chapter-34-conclusion.md) crystallises the discipline's long-range goal using a commercial-aviation analogy: a modern 747 is a model of safety and reliability, carries hundreds of passengers across 6,000 miles, and still has only **two pilots** in the cockpit. Every other element of the flight experience scaled up while the crew size did not. The mechanism is well-designed, approachable-in-normal-conditions interfaces that are flexible enough for robust emergency response, backed by redundant subsystems and sufficiently trained operators.

The stated SRE aspiration, by analogy:

> An SRE team should be as compact as possible and operate at a high level of abstraction, relying upon lots of backup systems as failsafes and thoughtful APIs to communicate with the systems. At the same time, the SRE team should also have comprehensive knowledge of the systems—how they operate, how they fail, and how to respond to failures—that comes from operating them day-to-day.

This is the synthesised picture the rest of the book has been building toward: sublinear scaling (fewer SREs per service as systems mature), [[frameworks-and-sre-platform|framework-mediated engagement]] (SRE best practice reaching services without direct staffing), [[automation-at-google|automation as a human-capacity multiplier]], and day-to-day operational knowledge as the precondition for good [[emergency-response]]. The two pilots do not scale by adding more pilots; they scale by adding systems that *act on the pilot's behalf*, with the pilot retaining authority at the high-abstraction control surface. The same logic applies to SRE.

Chapter 34 also restates the [[toil-and-engineering-balance|50% cap]] as an identity rather than a policy: an SRE is simultaneously *the pilot and the engineer/designer* — operating the system and designing its successor. The codified output — production experience packaged as code and systems — is consumable by other SRE teams, by anyone at Google, and externally via Google Cloud. This is the closing-chapter restatement of Chapter 18's [[software-engineering-in-sre|software-engineering-in-SRE]] thesis.

## SRE vs DevOps

DevOps, introduced into industry around late 2008, shares SRE's core principles (IT involvement in design, automation over human effort, engineering practices applied to ops). Treynor Sloss's framing: *DevOps can be seen as a generalisation of several core SRE principles to a wider range of organisations; equivalently, SRE is a specific implementation of DevOps with some idiosyncratic extensions* (source: chapter-01-introduction.md). See [[devops-vs-sre]].

## Related pages

- [[site-reliability-engineering]]
- [[sysadmin-approach]]
- [[devops-vs-sre]]
- [[toil-and-engineering-balance]]
- [[sre-tenets]]
- [[error-budget]]
- [[software-engineering-in-sre]]
- [[fostering-software-engineering-in-sre]]
- [[auxon]]
- [[sre-onboarding]]
- [[sre-engagement-model]]
- [[frameworks-and-sre-platform]]
