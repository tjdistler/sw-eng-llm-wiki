# Automation at Google

**Summary**: Chapter 7's organising argument: automation is a force multiplier for SRE, but the ultimate goal is **autonomous** systems that don't need glue logic at all. The chapter develops a five-level hierarchy of automation, illustrates it with three case studies (MySQL on Borg, cluster turnup, Borg itself), and closes with the failure mode that "highly effective automation" produces when the humans behind it lose their mental model of the system.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## The five values of automation

Chapter 7 lists five distinct benefits so that "time saving" doesn't swamp the conversation (source: chapter-07-the-evolution-of-automation-at-google.md):

1. **Consistency** — "the primary value of automation." Any action done hundreds of times by humans will not be done the same way each time; the inconsistency leaks into mistakes, data-quality issues, and reliability problems. The execution of well-scoped, known procedures is the domain where consistency is worth more than any other property.
2. **A platform** — designed correctly, automation is not a pile of scripts but a reusable platform. A bug fixed in the platform is fixed once and forever; the platform can be extended, can run more frequently than humans could, can run at inconvenient hours, and — crucially — can export metrics about itself that reveal properties of the process the operators didn't previously know.
3. **Faster repairs** — automation that resolves common faults drops [[mttr-and-mttf|MTTR]] because the detect-diagnose-fix loop runs without waiting for a human. Lower MTTR means higher availability at the same fault rate, and frees engineers from the cleanup work that dominates many ops teams.
4. **Faster action** — in many SRE domains humans simply can't react quickly enough. A failover or traffic switch that completes in seconds cannot be human-gated. Google's production wouldn't survive without its automation because the manual-operation threshold was crossed long ago.
5. **Time saving** — the most-cited benefit but often the hardest to calculate. The under-appreciated part: *once a task is encapsulated, anyone can run it*. Decoupling operator from operation is the multiplier. Joseph Bironas's warning about staffing humans to maintain un-automatable processes — "Think *The Matrix* with less special effects and more pissed off System Administrators" — closes the section.

The chapter is explicit that the benefits compound: consistency enables a platform, a platform enables faster repair, faster repair enables time savings, and time savings fund the engineering work that produces the next round of automation.

## Why Google in particular

Two factors tip Google's trade-offs toward aggressive automation (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Planet-spanning scale** — the hand-holding typical of smaller ops cultures is not an option.
- **A uniform production environment** — Google controls its own source across the stack, so when a vendor didn't expose an API, Google wrote one. Building APIs even when off-the-shelf software was cheaper was a deliberate long-term bet on automation.

Chapter 2's [[google-datacenter-topology|uniform infrastructure]] is precisely the precondition that makes aggressive automation feasible. Contrast organisations with black-box equipment, no-source-available software, or unautomatable vendor processes — each of those is an automation ceiling.

## The hierarchy of automation classes

The chapter proposes a five-level evolution path (see [[hierarchy-of-automation-classes]] for the full page):

1. **No automation** — database master failed over manually between locations.
2. **Externally maintained system-specific automation** — an SRE has a failover script in their home directory.
3. **Externally maintained generic automation** — the SRE adds database support to a shared "generic failover" script.
4. **Internally maintained system-specific automation** — the database ships with its own failover script.
5. **Autonomous systems** — the database notices problems and fails over without human intervention.

The chapter's thesis is that level 5 is qualitatively different from levels 1–4. Everything below level 5 is glue logic grafted onto the side of the system; autonomy means the "automation" disappears into the system's design itself.

## The three case studies

Chapter 7 grounds the hierarchy in three extended case studies, each illustrating a different lesson:

- **[[mysql-on-borg]]** — the "automate yourself out of a job" story. Decider reduced failover from 30–90 minutes to under 30 seconds 95% of the time, dropped operational work 95%, and freed 60% of the hardware. The lesson: *go the extra mile to deliver a platform rather than replacing existing manual procedures.*
- **[[cluster-turnup-automation]]** — the "specialisation trap" story. A turnup team with dedicated scripts achieved low latency but lost domain expertise; relevance and competence decayed; the team eventually re-approached it as a Service-Oriented Architecture where service owners expose per-service Admin Server RPCs. The lesson: *the most functional tools are usually written by those who use them.*
- **[[borg|Borg itself]]** — the "autonomous system" story. Borg didn't start as a cluster OS; it evolved from Python scripts that SSHed into machines, through a machine-state database, into a system where cluster management became an entity with an API. The lesson: *bring classic distributed-system ideas to infrastructure management and rescheduling becomes an intrinsic feature rather than something to automate.*

See also **[[automation-gone-wrong]]** for the Diskerase and Bigtable disk-zero cautionary tales Chapter 7 pairs with the success stories.

## Reliability is the fundamental feature

The chapter's closing argument (source: chapter-07-the-evolution-of-automation-at-google.md):

- Highly effective automation has a well-documented downside (cited via Air France 447 and the Bainbridge/Sarter literature): humans lose direct contact with the system, their mental models drift out of sync with reality, and when automation eventually fails they can no longer operate the system.
- This failure mode bites hardest for **non-autonomous** automation — where the script replaces a manual action that is *presumed* to still be performable. Over time the manual path rots away.
- The Google response is to push harder on *[[autonomous-systems|autonomous]]* behaviour rather than retreat to more manual work, while making internal state aggressively observable so the humans who do need to intervene still have a model.
- Reliability is framed as **the fundamental feature**, and autonomous resilient behaviour is one concrete way to deliver it.

This links directly back to the Chapter 1 [[toil-and-engineering-balance|toil cap]]: autonomous systems are how SRE holds the 50% engineering line as service count grows. Without autonomy, ops work scales linearly with service count and the cap is impossible to sustain.

## Recommendations

The chapter gives two practical takeaways that apply below Google scale (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Start in design.** Autonomous operation is difficult to retrofit convincingly. Standard good software-engineering practices — decoupled subsystems, explicit APIs, minimised side effects — are the preconditions that let autonomy be designed in rather than bolted on.
- **Don't wait for Google scale.** The benefits of automation are broader than the naïve time-saved-vs-time-spent calculation suggests; consistency and platform effects alone often justify it.

## The cross-industry foil (Chapter 33)

Chapter 7 argues for aggressive automation; Chapter 33 surveys industries that take the opposite stance and explains why (source: chapter-33-lessons-learned-from-other-industries.md).

**Industries that deliberately limit automation:**

- **US nuclear Navy (during Jeff Stevenson's tenure)** — *eschewed automation in favor of a series of interlocks and administrative procedures*. Operating a single valve required an operator, a supervisor, and a crew member on the phone with the engineering watch officer. Three reasons: a human spots failure modes an automated system might miss; a *trusted human decision chain* (a series of people, not one individual) is the safety property; computers can commit large irreparable mistakes faster than they can be stopped.
- **Proprietary trading (recent years)** — *increasingly cautious in its application of automation* after experience showed that incorrectly configured automation can inflict significant financial damage in very short time. The 2012 Knight Capital $440M loss in *a few hours* and the 2010 Flash Crash *trillions of dollars in 30 minutes* are the named cautionary tales.

**Industries that embrace automation, with stated justification:**

- **Manufacturing** — efficiency and monetary savings; automation produces higher quality and tighter tolerances than manual work
- **UK civil nuclear** — *if a plant is required to respond to a given situation in less than 30 minutes, that response must be automated.* The 30-minute rule encodes the human-reaction-time threshold below which automation is mandatory
- **Aviation** — applies automation selectively. Operational failover is automated; air-traffic-control system implementations must be manually inspected by humans even when monitoring is automatic. Trust automation only when verified by a human
- **LASIK / refractive eye surgery** — automation eliminated entire classes of medical error. The first improvement was a sanity check on manually entered measurements; later, iris-photo matching at surgery time eliminated the patient-data-mix-up failure mode entirely

**The Chapter 33 reframe of Chapter 7's argument:**

Chapter 7 names the *automation gone wrong* failure mode (Diskerase, Bigtable disk-zero) and proposes mitigations (rate-limiting, audit trails, idempotent workflows). Chapter 33 supplies the cross-industry context: the proprietary trading industry has converged on the same lesson — *speed can be a negative if these tasks are configured incorrectly*. The two chapters together suggest that the right reading of Chapter 7 is not *automate everything* but *automate the things whose failure mode is recoverable, and apply progressive-delivery discipline to the automation itself*.

The nuclear Navy's *trusted human decision chain* is the structural opposite: when failure isn't recoverable, the answer is to slow the action down enough that multiple humans can each veto it. Both stances are correct in their own consequence-cost regimes. The Chapter 33 takeaway is that the choice is consequence-driven, not philosophical.

## Cross-book connections

- [[toil-and-engineering-balance]] — autonomy is the mechanism that makes the 50% cap sustainable; Chapter 7's "automate yourself out of a job" is the concrete story.
- [[desired-state-management]] (Newman) — Borg's declarative cluster-management API is the progenitor of the Kubernetes-era desired-state pattern.
- [[operator-pattern]] (Burns) — application-specific reconciliation loops are the open-source realisation of the level-4-approaching-level-5 story.
- [[change-management-sre]] — Chapter 7's "implicit safety signals" caution (the Bigtable disk-zero story) sharpens Chapter 1's change-management trio.
- [[progressive-delivery]] (Newman / Burns) — the rate-limiting and audit-trail mitigations the chapter adds after the Diskerase incident are progressive-delivery practices applied to automation itself.

## Related pages

- [[hierarchy-of-automation-classes]]
- [[autonomous-systems]]
- [[mysql-on-borg]]
- [[cluster-turnup-automation]]
- [[prodtest]]
- [[automation-gone-wrong]]
- [[borg]]
- [[toil-and-engineering-balance]]
- [[desired-state-management]]
- [[mttr-and-mttf]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
- [[lessons-from-other-industries]]
- [[velocity-vs-reliability-tradeoff]]
