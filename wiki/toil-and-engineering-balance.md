# Toil and Engineering Balance

**Summary**: Google's SRE teams are capped at 50% operational work — tickets, on-call, manual tasks — with the remaining time required to be spent on engineering. Chapter 5 defines toil precisely (six characteristics), distinguishes it from overhead and grungy-but-valuable work, and explains why unchecked toil harms both the individual and the organisation.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-05-eliminating-toil.md`, `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`, `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`, `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The 50% cap

Without a structural limit on manual work, an ops-focused team grows linearly with service traffic. More users, more tickets, more people doing the same things over and over. To avoid that trajectory, Google places a **50% cap on aggregate "ops" work** for all SREs (source: chapter-01-introduction.md). The cap covers tickets, on-call load, and manual tasks in total.

The cap is an upper bound, not a target. Left to their own devices, SREs should drift toward *very little* operational load, because the service increasingly runs itself. In practice, scale and new features keep the floor well above zero, but the direction is always to reduce it.

Chapter 5 restates this as two paired promises: *at most* 50% on toil, *at least* 50% on engineering project work that either reduces future toil or adds service features (source: chapter-05-eliminating-toil.md). Feature work typically targets reliability, performance, or utilisation — which reduces toil as a second-order effect. The engineering half is what enables the organisation to scale **sublinearly** with service size; it is also a hiring promise that the organisation makes to every new SRE, which is why letting a team devolve into an ops team is treated as a breach of faith.

## What toil is (Chapter 5)

Toil is **not** simply work people dislike, nor is it equivalent to admin chores or grungy work (source: chapter-05-eliminating-toil.md). It has a precise definition: toil is the kind of work **tied to running a production service** that tends to be:

- **Manual** — including manually running a script. The hands-on time counts, not the elapsed time; the script itself doesn't rescue the task from being toil.
- **Repetitive** — done over and over. First- or second-time work, or work solving a novel problem, is not toil.
- **Automatable** — a machine could do it just as well, or the need could be designed away. If *genuine* human judgement is required, it is probably not toil. Rau warns against escape-hatching bad design as "needs human judgement": a service that pages SREs many times a day with complex alerts needs to be redesigned, and until then the human-judgement work is unambiguously toil.
- **Tactical** — interrupt-driven and reactive, not strategic and proactive. Pager handling is the archetype.
- **Devoid of enduring value** — the service is in the same state after the work is done. A permanent improvement disqualifies the task from being toil even if it involved grungy effort.
- **O(n) with service growth** — scales linearly with service size, traffic, or user count. A well-designed service should grow an order of magnitude with near-zero additional work.

Not every toil task has every attribute; the more of these that apply, the more clearly it is toil.

### Toil vs overhead vs grungy-but-valuable work

Chapter 5 separates three neighbouring categories that are easy to conflate (source: chapter-05-eliminating-toil.md):

- **Toil** — the six-characteristic work above.
- **Overhead** — administrative work not directly tied to running a production service: team meetings, OKR setting, snippets, HR paperwork, training. Not toil, but also not engineering.
- **Grungy-but-valuable work** — e.g. cleaning up an alerting configuration and removing clutter. It's not toil because it produces a permanent improvement.

The precision matters because each category has a different remedy. Toil gets engineered away. Overhead gets budgeted for. Grungy-but-valuable work gets done and counted as engineering.

See [[engineering-work-categories]] for the full four-way taxonomy (software engineering, systems engineering, toil, overhead) that Ch 5 uses to account for an SRE's time.

## The safety valve

Making the cap real requires measurement and a mechanism. Google (source: chapter-01-introduction.md):

1. **Measures** how SRE time is spent.
2. When an SRE team consistently spends less than 50% of its time on development work, **changes the team's practices**.
3. Concretely, this means **redirecting excess operations work back to the product development team**: reassigning bugs and tickets to development managers, (re)integrating developers into on-call pager rotations.
4. The redirection ends when the operational load drops back to 50% or lower.

This is the **safety valve**: ops overflow is a signal that the product is not automatable enough, and the signal is routed to the people who can fix that — the developers building the product. The redirection is also a feedback mechanism that teaches developers to build systems that don't require manual intervention.

## Calculating toil in practice

Chapter 5 grounds the 50% cap in arithmetic (source: chapter-05-eliminating-toil.md). A typical SRE does one week of primary and one week of secondary on-call per cycle. That establishes a **floor** on toil set by the rotation size:

- 6-person rotation → 2/6 ≈ **33% floor**
- 8-person rotation → 2/8 = **25% floor**

So the 50% cap already leaves limited room above the on-call floor, which is why interrupts and on-call response dominate measured toil. Quarterly Google-wide surveys report **~33% average toil** — comfortably under the 50% cap — but the average hides outliers: some SREs report 0% (pure project work, no on-call) and others report 80%. Individual outliers are a signal for managers to spread toil more evenly and help overloaded SREs find engineering projects.

The reported ranking of toil sources (source: chapter-05-eliminating-toil.md):

1. **Interrupts** — non-urgent service-related messages and emails.
2. **On-call (urgent) response**.
3. **Releases and pushes** — even with significant automation, still a real toil source.

Chapter 29 is the full treatise on the #1 source. See [[dealing-with-interrupts]] for the interrupt-management policies ([[polarizing-time]], [[interrupt-role-structuring]], [[reducing-interrupts]]) that drive measured interrupt toil down — not by adding headcount, but by pricing in the [[context-switch-cost]] and protecting [[cognitive-flow-state|flow]]. The Chapter 5 ranking and the Chapter 29 prescriptions are complementary: Chapter 5 says where the toil is, Chapter 29 says what to do about it.

## Automatic, not just automated

Treynor Sloss's phrasing: *we want systems that are automatic, not just automated* (source: chapter-01-introduction.md). The distinction matters:

- **Automated** = a human triggers a script.
- **Automatic** = the system handles the situation itself; the human doesn't know it happened.

The 50% cap pushes toward the second kind because scripts still count as ops work when you have to run them — the "manually running a script" clause of the Chapter 5 toil definition makes this explicit.

## The on-call target

The same tenet governs on-call load directly (source: chapter-01-introduction.md):

- **Target: at most two events per 8–12 hour on-call shift.**
- Two events gives the on-call engineer enough time to handle each accurately, restore service, and **conduct a postmortem**.
- More than two events per shift and investigations suffer; the engineer is too overwhelmed to learn from them, and pager fatigue does not improve with scale.
- Fewer than one event per shift consistently means keeping SREs on-call is a waste of their time.

## The 25% on-call sub-cap (Chapter 11)

Chapter 11 subdivides the 50% operational half with a tighter rule for on-call specifically (source: chapter-11-being-on-call.md):

> At least 50% of SRE time on engineering; of the remainder, **no more than 25% on-call**, leaving up to 25% for other operational non-project work.

The arithmetic produces a concrete minimum team size: assuming two people on-call at all times (primary + secondary) and week-long shifts, an **8-engineer single-site team** puts each engineer on-call one week per month (25%). Dual-site teams work with ≥ 6 per site. See [[balanced-on-call]], [[sre-on-call-engagement]], and [[multi-site-on-call]].

Chapter 11 also derives the two-events-per-shift target from the other direction: **dealing with a single incident averages 6 hours of end-to-end work** (root-cause analysis, remediation, postmortem, bug fixes). A 12-hour shift therefore tops out at 2 incidents. See [[balanced-on-call]].

The failure modes at each end of the quantity axis are [[operational-overload]] and [[operational-underload]].

## Is toil always bad?

Chapter 5 is careful not to moralise (source: chapter-05-eliminating-toil.md). Small amounts of toil can be calming, low-risk, low-stress; some people genuinely enjoy repetitive tasks and the quick sense of accomplishment. Some toil is unavoidable in any engineering role. **In small doses, if the person is happy with it, toil is not a problem.**

Toil becomes toxic in **large quantities**. The harms fall into two groups.

### Personal harms

- **Career stagnation** — too little project time means too little career progress. Grunge with big positive impact is rewarded, but a career can't be made from it.
- **Low morale** — everyone has a limit; past it, toil produces burnout, boredom, and discontent.

### Organisational harms

- **Creates confusion** — visible toil-heavy individuals or teams undermine the message that SRE is an engineering organisation.
- **Slows progress** — a toil-burdened SRE team can't roll out new features promptly, slowing the whole product's feature velocity.
- **Sets precedent** — willingness to absorb toil incentivises Dev counterparts (and other teams) to push more operational work onto SRE that rightfully belongs to them.
- **Promotes attrition** — even if the current team tolerates toil, the team's best engineers will look elsewhere.
- **Causes breach of faith** — hires and transfers who joined for engineering project work feel cheated, damaging morale further.

The attrition and breach-of-faith items loop back to the Chapter 1 hiring promise: the 50% rule is part of the SRE employment contract, and violating it is not just bad practice but dishonest.

## Organisational preconditions

The cap only works if the whole organisation — SRE and dev — understands **why the safety valve exists** and shares the goal of eliminating overflow events by making the product less operationally needy. Without that shared understanding, redirecting tickets back to dev looks like SRE dumping work, and the mechanism breaks down (source: chapter-01-introduction.md).

## Automate yourself out of a job (Chapter 7)

Chapter 7 supplies the [[mysql-on-borg|MySQL-on-Borg]] case study as the concrete worked example of what a team looks like when the engineering half of the 50/50 split is spent well (source: chapter-07-the-evolution-of-automation-at-google.md). The Ads SRE team believed their MySQL work was already "mature and managed" after automating routine replica replacements. Then they migrated onto [[borg|Borg]] — and the project forced them to eliminate 30–90-minute manual master failovers, because Borg's fluid task placement was incompatible with any human-dependent failover procedure that couldn't hit the 30-second error-budget threshold.

The outcome cited:

- The **Decider** failover daemon completed planned and unplanned failovers in under 30 seconds 95% of the time.
- **Operational time dropped 95%.** A single-database-task outage no longer paged a human.
- **Schema changes were subsequently automated** too, driving total operational maintenance down roughly 95% overall.
- **Hardware utilisation improved** enough to free 60% of the fleet via bin-packing.
- The freed engineering time funded further automation — the cascade effect the 50% cap is designed to enable.

Chapter 7's Chapter-7-specific takeaway: the reason this worked is that the team went the extra mile to deliver a *platform* (MoB) rather than replacing existing manual procedures with scripts. Level 4 of the [[hierarchy-of-automation-classes|automation hierarchy]] approaching level 5 ([[autonomous-systems|autonomy]]). The 95% toil drop is what the 50% cap looks like when sustained over years: not a ceiling that gets bumped every quarter, but a bound the system falls well below because automatic behaviour has been designed in.

The chapter also sharpens the **automatic vs automated** distinction introduced here: Decider is automatic (no human triggers it; the database notices and fails over), not merely automated (there is no script the SRE has to remember to run). The 50% cap drives teams toward automatic because running scripts still counts as toil.

See [[automation-at-google]] for the chapter's broader argument about autonomy being the mechanism that makes sub-linear-ops-scaling possible.

## Growing operational load as a launch-era pathology (Chapter 27)

Chapter 27 names **growing operational load** as one of the three long-horizon pathologies [[launch-coordination-engineering|LCE]] couldn't solve at launch time (source: chapter-27-reliable-product-launches-at-scale.md):

> When running a service after it launches, operational load, the amount of manual and repetitive engineering needed to keep a system functioning, tends to grow over time unless efforts are made to control such load. Noisiness of automated notifications, complexity of deployment procedures, and the overhead of manual maintenance work tend to increase over time and consume increasing amounts of the service owner's bandwidth, leaving the team less time for feature development.

The 50% cap is the explicit mechanism that defends against this drift: "SRE has an internally advertised goal of keeping operational work below a maximum of 50%." Staying below the cap requires **constant tracking of sources of operational work** and **directed effort to remove them** — not a one-time automation push. Chapter 27's framing connects back to Chapter 5's point that the cap is an upper bound, not a target, and that organic creep (alert fanout growing, deploy steps multiplying, ad-hoc migrations piling up) is the dominant threat over long timescales.

The chapter also names **infrastructure churn** as a distinct organisational-level threat: when underlying substrate evolves without automated client migration, every service owner runs fast to stay still. The fix is a **churn-reduction policy** that prohibits backward-incompatible infrastructure changes without automated client migration — a structural defence against toil originating outside the service team's control.

## Sorting fires into toil and not-toil (Chapter 30)

Chapter 30's [[embedding-sre|embedded-SRE rescue pattern]] operationalises the toil definition into a concrete Phase 2 exercise: **sort the team's fires into toil and not-toil** (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The chapter offers a two-category model:

- Fires that **shouldn't exist** — they are toil and should be automated or designed away.
- Fires that **cause stress but are actually part of the job** — they are legitimate operational work that needs tooling to control the burn (playbooks, drills, better observability), not elimination.

The sorting output is presented to the team with the reasoning attached. The exercise has two effects: it gives the team a shared vocabulary for discussing which ops work is acceptable vs. unacceptable, and it surfaces the cases where the team has silently accepted something as "part of the job" that is actually toil the 50% cap should be defending against. See [[embedding-sre]] and [[ops-mode]] for the embedding context, and [[identifying-kindling]] for the complementary Phase 1 "what will burn next" exercise.

## Why this matters

Consciously maintaining the ops/engineering balance keeps SREs with the **bandwidth to do creative, autonomous engineering** while still retaining the operational wisdom that comes from actually running the service. Drop the cap and the team regresses to the [[sysadmin-approach|sysadmin trajectory]]; drop the operational exposure entirely and the team loses touch with reality.

Chapter 5 closes with a small, cumulative framing: if every SRE eliminates a little toil each week with good engineering, the services get steadily cleaner, and the collective effort shifts to engineering for scale, architecting the next generation of services, and building cross-SRE toolchains (source: chapter-05-eliminating-toil.md).

## Related pages

- [[sre-discipline]]
- [[sre-tenets]]
- [[engineering-work-categories]]
- [[sysadmin-approach]]
- [[blameless-postmortem]]
- [[emergency-response]]
- [[error-budget]]
- [[automation-at-google]]
- [[autonomous-systems]]
- [[mysql-on-borg]]
- [[balanced-on-call]]
- [[sre-on-call-engagement]]
- [[multi-site-on-call]]
- [[on-call-compensation]]
- [[operational-overload]]
- [[operational-underload]]
- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[interrupt-role-structuring]]
- [[reducing-interrupts]]
- [[cognitive-flow-state]]
- [[context-switch-cost]]
- [[embedding-sre]]
- [[ops-mode]]
- [[identifying-kindling]]
