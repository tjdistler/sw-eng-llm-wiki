# Structured and Rational Decision Making

**Summary**: Chapter 33's fourth cross-industry theme — SRE's data-driven decision discipline, where the basis for a decision is agreed in advance, the inputs are clear, assumptions are explicit, and data wins over hunches or the most-senior opinion (the *HiPPO* anti-pattern). Other industries land at very different points on the spectrum: telecom's "if it ain't broke, don't fix it ever" (1980s long-distance switches still in use), the playbook-and-binder approach of fields with limited-skill workforces, manufacturing's controlled-experiment culture, and proprietary trading's enforcement-team separation that can shut down trading on an abnormality.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## SRE's framing

Chapter 33 names four properties of a structured decision (source: chapter-33-lessons-learned-from-other-industries.md):

- The basis for the decision is **agreed upon in advance**, rather than justified ex post facto.
- The **inputs** to the decision are clear.
- Any **assumptions** are explicitly stated.
- **Data-driven decisions** win over decisions based on feelings, hunches, or the opinion of the most senior employee in the room.

Plus two operating assumptions about the team (source: chapter-33-lessons-learned-from-other-industries.md):

- Everyone has the best interests of a service's users at heart.
- Everyone can figure out how to proceed based on the data available.

Decisions should be **informed rather than prescriptive**, and made without deference to the *HiPPO* — the **Highest-Paid Person's Opinion** (Eric Schmidt and Jonathan Rosenberg's coinage, source: chapter-33-lessons-learned-from-other-industries.md).

## The HiPPO anti-pattern

Chapter 33's named warning: when the room defaults to whatever the senior person says, three things break at once:

- **Decision quality** — the senior person's information set is no better than the team's, and is often worse for low-level operational details.
- **Team development** — junior engineers stop reasoning in advance because the decision will be made for them anyway.
- **Justification rigour** — the post-hoc rationalisations after a HiPPO call don't get critiqued because the decision is already locked.

The structural antidote isn't to remove senior people from the decision; it's to require that the *decision basis* and *inputs* exist before the decision is made. A senior opinion that meets the criteria becomes data; one that doesn't, doesn't override the data that does.

## The cross-industry spectrum

Chapter 33 surveys decision-making practice across four distinct shapes:

### "If it ain't broke, don't fix it ever"

Industries with thoroughly-engineered systems are reluctant to change them (source: chapter-33-lessons-learned-from-other-industries.md):

- **Telecom long-distance switches** are still implemented from 1980s designs. *"They are pretty much bulletproof and massively redundant"* (Gus Hartmann).
- **Civil nuclear** is similarly slow to change. *If it works now, don't change it.*

The model works when the underlying technology evolves slowly enough that the un-replaced design isn't compounding new problems. Software doesn't usually have this property — the dependencies underneath the unchanged component evolve.

### Playbook-and-binder

Many industries focus on captured procedures (source: chapter-33-lessons-learned-from-other-industries.md):

> Every humanly conceivable scenario is captured in a checklist or in "the binder." When something goes wrong, this resource is the authoritative source for how to react. This prescriptive approach works for industries that evolve and develop relatively slowly, because the scenarios of what could go wrong are not constantly evolving due to system updates or changes. This approach is also common in industries in which the skill level of the workers may be limited, and the best way to make sure that people will respond appropriately in an emergency is to provide a simple, clear set of instructions.

The two preconditions named: **slow rate of change** and **bounded workforce skill**. Software services breach the first; SRE staffing breaches the second. Hence SRE's playbooks are genuinely useful as orienting reference (see [[on-call-playbook]]) but the operational discipline is *informed reasoning under pressure* (see [[hypothetico-deductive-debugging]] and [[improvisational-troubleshooting]]) rather than execution-of-binder.

### Controlled-experiment culture

Manufacturing and research environments rely on hypothesis testing (source: chapter-33-lessons-learned-from-other-industries.md):

> Research and manufacturing environments are characterized by a rigorous experimentation culture that relies heavily on formulating and testing hypotheses. These industries regularly conduct controlled experiments to make sure that a given change yields the expected result at a statistically significant level and that nothing unexpected occurs. Changes are only implemented when data yielded by the experiment supports the decision.

This is the closest analogue to SRE's preferred shape. The match is direct: [[canary-test|canary]] and [[gradual-rollout|gradual rollout]] are controlled experiments; [[testing-for-reliability|the testing pyramid]] is hypothesis testing applied to code; [[risk-management-sre|risk management]] is decision-under-uncertainty with explicit inputs.

### Enforcement-team separation

Proprietary trading splits decision-making to manage risk (source: chapter-33-lessons-learned-from-other-industries.md):

> This industry features an enforcement team separate from the traders to ensure that undue risks aren't taken in pursuit of achieving a profit. The enforcement team is responsible for monitoring events on the floor and halting trading if events spin out of hand. If a system abnormality occurs, the enforcement team's first response is to shut down the system. As put by John Li, "If we aren't trading, we aren't losing money. We aren't making money either, but at least we aren't losing money." Only the enforcement team can bring the system back up, despite how excruciating a delay might seem to traders who are missing a potentially profitable opportunity.

The structural insight: the people incentivised to take risk are not the people empowered to stop. SRE's [[error-budget|error budget]] is a softer version of the same separation — when the budget runs out, launches stop, and the structural lever isn't *the SRE team's discretion at the moment* but a *pre-agreed rule* that activates regardless of who wants what at the time.

The 2010 Flash Crash and the 2012 Knight Capital $440M loss are Chapter 33's named cautionary tales for what happens when the enforcement separation is missing or too slow.

## Where SRE sits on the spectrum

SRE's decision-making practice is closest to the **controlled-experiment** mode, with significant borrowings:

- From **playbook-and-binder**: the [[on-call-playbook]] and [[architectural-checklists]] capture institutional knowledge so the engineer in the moment isn't reasoning from first principles
- From **enforcement separation**: the [[error-budget|error budget]] mechanism that halts launches when reliability is overspent; the [[change-management-sre|change-management trio]] of progressive rollout, fast detection, safe rollback as a structural circuit breaker
- From **conservative non-change**: [[virtue-of-boring|the virtue of boring]] — boring source code is a desirable property, dramatic changes inside critical components are usually wrong

What SRE rejects from the spectrum: the HiPPO mode, where seniority substitutes for inputs.

## Cross-book connections

- [[error-budget]] (SRE Ch 1, 3) — the structural mechanism by which SRE imports proprietary trading's enforcement-separation pattern: the budget halts launches without requiring an in-the-moment authority call
- [[architectural-checklists]] (Richards & Ford) — Gawande's *Checklist Manifesto* sits in the same family as the playbook-and-binder approach Chapter 33 catalogues; Richards & Ford's specific use of checklists is for code completion, unit/functional testing, and software release rather than emergency response
- [[on-call-playbook]] (SRE Ch 1, 11) — the SRE compromise between binder-execution and improvisation: orienting reference, not script
- [[hypothetico-deductive-debugging]] (SRE Ch 12) — the controlled-experiment mode applied at incident-response time: hypothesis, prediction, test, refine
- [[risk-management-sre]] (SRE Ch 3) — the SRE framing of decision-under-uncertainty with explicit cost dimensions
- [[architecture-decisions-vs-design-principles]] (Richards & Ford) — the *decision basis agreed in advance* property is the [[architecture-decision-record|ADR]] discipline applied to operational decisions
- [[lessons-from-other-industries]] — the Chapter 33 hub

## Related pages

- [[lessons-from-other-industries]]
- [[error-budget]]
- [[on-call-playbook]]
- [[architectural-checklists]]
- [[hypothetico-deductive-debugging]]
- [[improvisational-troubleshooting]]
- [[risk-management-sre]]
- [[change-management-sre]]
- [[canary-test]]
- [[gradual-rollout]]
- [[virtue-of-boring]]
