# Lessons from Other Industries

**Summary**: Chapter 33's hub — Jennifer Petoff's cross-industry survey of how aviation, healthcare, nuclear power, military, manufacturing, telecom, finance, and emergency response handle reliability, distilled into four SRE themes. The chapter's takeaway is that Google has imported many practices from these older fields, but distinguishes itself by tolerating a higher rate of change because most Google products operate where lives are not at stake.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## Why this chapter exists

Chapter 33 was written to answer a comparative question prompted by compiling the SRE book itself (source: chapter-33-lessons-learned-from-other-industries.md):

- Are SRE principles also important outside of Google, or do other industries handle high reliability differently?
- If they share the principles, how are they manifested?
- What are the similarities and differences?
- What drives those differences?
- What can Google and the tech industry learn from the comparison?

Petoff interviewed Google engineers who had previously worked in defense, lifeguarding, refractive eye surgery (LASIK), telecommunications and E911, medical devices, military aircraft and naval avionics, railway signaling, synthetic-diamond manufacturing (Six Sigma), proprietary trading, civil nuclear power, the US Navy submarine nuclear program, and air traffic control. The chapter then distils SRE practice into four themes and walks each across the interviewed industries.

## The four themes

Chapter 33 organises the comparison around four SRE themes (source: chapter-33-lessons-learned-from-other-industries.md):

1. **[[preparedness-and-disaster-testing]]** — *hope is not a strategy*; testing, drilling, and designing for failure before it happens. Google's [[testing-disaster-recovery|DiRT]] sits next to nuclear-Navy weekly live drills, lifeguard mystery-shopper drowning scenarios, aviation simulators, and telecom switch-on-wheels swing capacity.
2. **Postmortem culture** — corrective and preventive action (CAPA) embodied as [[blameless-postmortem|blameless postmortems]]. The non-software analogues: regulator-driven postmortems (FAA, FCC, FDA, OSHA), Alcoa's safety culture under Paul O'Neill, [[near-miss-reporting|near-miss reporting]] in chemical manufacturing and the UK's CHIRP programme, and lifeguard post-incident analysis with mandatory write-ups.
3. **Automation and reduced operational overhead** — covered at [[automation-at-google]]; Chapter 33 surveys industries that *don't* automate (the US nuclear Navy's trusted human decision chain) and industries that do (manufacturing for cost, UK nuclear for sub-30-minute response, LASIK for data-entry safety).
4. **[[structured-and-rational-decision-making]]** — data-driven decisions, the HiPPO anti-pattern, and the spectrum from "if it ain't broke, don't fix it" (telecom 1980s long-distance switches, civil nuclear) through playbook-and-binder approaches (limited-skill workforces) through experimental cultures (manufacturing) to enforcement-team-separation (proprietary trading).

The four themes are not the chapter's invention — they are SRE-internal vocabulary mapped onto external industries to make the comparison legible.

## What Google does differently

Chapter 33's main takeaway is that Google has **a higher appetite for velocity** than most other high-reliability industries (source: chapter-33-lessons-learned-from-other-industries.md):

> The ability to move or change quickly must be weighed against the differing implications of a failure. In the nuclear, aviation, or medical industries, for example, people could be injured or even die in the event of an outage or failure. When the stakes are high, a conservative approach to achieving high reliability is warranted.

The Google escape valve is the [[error-budget|error budget]]: most Google services operate where users are inconvenienced, not injured, and the spare reliability above the SLO can be deliberately spent on innovation. See [[velocity-vs-reliability-tradeoff]] for the full framing.

This is also the implicit answer to "why did Google adopt only some of these practices?" — Google selectively imported the parts compatible with its rate of change. The detailed-design-then-three-weeks-of-coding culture Peter Dahl describes from defense work doesn't survive contact with launch-and-iterate; the US nuclear Navy's manual valve operation with three humans on the call doesn't survive the [[toil-and-engineering-balance|50% engineering cap]].

## The industries surveyed

The chapter's profiled industries and their reliability stakes (source: chapter-33-lessons-learned-from-other-industries.md):

| Industry | Stake | Distinctive practice |
|---|---|---|
| Defense systems (GPS, inertial guidance) | Vehicle loss; financial loss | Year of design, three weeks of code |
| Lifeguarding | Lives daily | Rigorous certification + recert; mystery-shopper drills; mandatory post-incident write-ups |
| Refractive eye surgery (LASIK) | Eyesight; FDA regulation | Foolproofed machines; iris-photo automation eliminated entire error class |
| Telecommunications / E911 | User inconvenience to fatalities | [[swing-capacity|Switch-on-wheels]]; weatherproof generators; conservative tech retention |
| Medical devices, automotive (EKG-over-cellular) | Equipment recall; indirect health impact | Cross-industry interface engineering; regulator-driven design |
| Military aircraft, naval avionics, rail signaling | Multimillion-dollar loss; injuries; fatalities | Defined safety standards (UK Defence Standard 00-56, IEC 61508, DO-178B/C, DO-254); [[safety-integrity-level|SIL 1-4]] |
| Synthetic-diamond manufacturing (Six Sigma) | Daily worker safety hazards | "Every management meeting started with a discussion of safety" |
| Proprietary trading | Fiscal | Separation of trading from enforcement; shut down on abnormality |
| Civil nuclear power (UK) | Outage millions/day; community risk | [[defense-in-depth-data|Defense in depth]]; multiple physical barriers; 30-minute automation rule |
| US Navy nuclear (submarine) | Equipment damage; environment; life | Religious live drills 2-3x/week; trusted human decision chain |
| Air traffic control | Inconvenience to crash | Realistic simulators with live data feeds; defense in depth |

## Cross-book connections

- [[blameless-postmortem]] (SRE Ch 1, 11, 12, 13, 14, 15) — Chapter 33 widens the cross-industry origin story Chapter 15 already named (healthcare and avionics) to a fuller catalogue of postmortem analogues
- [[testing-disaster-recovery]] / [[disaster-role-playing]] / [[recovery-testing]] (SRE Ch 17, 26, 28) — DiRT and Wheel of Misfortune are the SRE side of the simulation/drill family Chapter 33 surveys
- [[automation-at-google]] (SRE Ch 7) — Chapter 7's enthusiasm for automation acquires a cross-industry foil: nuclear Navy and proprietary trading deliberately limit automation precisely because computers commit irreparable mistakes faster than humans can stop them
- [[incident-command-system]] (SRE Ch 14) — already names the FEMA/aviation pedigree; Chapter 33 generalises the borrow-the-practice instinct
- [[error-budget]] (SRE Ch 1, 3) — Chapter 33's closing argument explicitly cites error budgets as the mechanism that funds Google's higher-velocity reliability stance
- [[defense-in-depth-data]] (SRE Ch 26) — Chapter 33 names nuclear power as the canonical defense-in-depth industry; the data-integrity layer cake is the pattern adapted to data
- [[architectural-checklists]] (Richards & Ford) — Chapter 33's discussion of playbook-and-binder approaches in industries with limited-skill workforces sits in the same tradition as Gawande's Checklist Manifesto

## Related pages

- [[preparedness-and-disaster-testing]]
- [[structured-and-rational-decision-making]]
- [[organizational-safety-culture]]
- [[near-miss-reporting]]
- [[velocity-vs-reliability-tradeoff]]
- [[swing-capacity]]
- [[safety-integrity-level]]
- [[blameless-postmortem]]
- [[automation-at-google]]
- [[testing-disaster-recovery]]
- [[disaster-role-playing]]
- [[incident-command-system]]
- [[defense-in-depth-data]]
- [[error-budget]]
- [[site-reliability-engineering]]
