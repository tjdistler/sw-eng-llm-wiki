# Preparedness and Disaster Testing

**Summary**: Chapter 33's first cross-industry theme — *hope is not a strategy*. SRE's [[testing-disaster-recovery|DiRT]] exercises and [[disaster-role-playing|Wheel of Misfortune]] drills sit inside a much older family of preparedness practices: nuclear-power defense-in-depth, US Navy submarine drills 2-3 times per week, lifeguard mystery-shopper drownings, aviation simulators with live data feeds, telecom switch-on-wheels swing capacity, and the safety-standards regime in military aircraft and rail signaling.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## SRE's framing

Chapter 33 opens this theme with an SRE rallying cry (source: chapter-33-lessons-learned-from-other-industries.md):

> "Hope is not a strategy." This rallying cry of the SRE team at Google sums up what we mean by preparedness and disaster testing.

The vigilance loop: *what could go wrong; what action can we take to address those issues before they lead to an outage or data loss*. Annual [[testing-disaster-recovery|Disaster and Recovery Testing (DiRT)]] drills push production systems to the limit and inflict actual outages to ensure systems react the way SRE thinks they will, expose unexpected weaknesses, and toughen the system against uncontrolled outages.

## The seven cross-industry strategies Chapter 33 catalogues

Chapter 33 pulls seven distinct preparedness strategies from the interviews (source: chapter-33-lessons-learned-from-other-industries.md):

1. **Relentless organisational focus on safety** — see [[organizational-safety-culture]]. *"Every management meeting started with a discussion of safety"* (Eddie Kennedy on Six Sigma synthetic-diamond manufacturing). Workers must feel empowered to speak up.
2. **Attention to detail** — Jeff Stevenson on the US Navy nuclear submarine: a lapse in lube-oil maintenance can lead to major submarine failure because systems are highly interconnected. Routine maintenance prevents small issues from snowballing.
3. **[[swing-capacity|Swing capacity]]** — telecom's *switch on wheels* (SOW), a mobile telco office that can be deployed in an emergency or in anticipation of a known overload event (Olympics, natural disaster, the 2005 leaked celebrity phone number that produced DDoS-shaped traffic).
4. **Simulations and live drills** — when the consequences of a real outage are too high, simulators substitute. Aviation builds simulators down to the smallest control-room detail with live data feeds. The US nuclear Navy combines *what-if* thought exercises with live drills 2-3 days per week, *"actually breaking real stuff but with control parameters."* Lifeguards run mystery-shopper-style mock drownings staged to be indistinguishable from the real thing.
5. **Training and certification** — particularly important when lives are at stake. Lifeguard certification requires fitness components (holding someone heavier than yourself with shoulders out of the water), technical components (first aid, CPR), operational elements (team coordination), plus site-specific recertification (pool vs lakeside vs ocean differ).
6. **Detailed requirements gathering and design** — defense-contractor practice (per Peter Dahl): a year of design followed by three weeks of code. LASIK machines are designed to be foolproof, so requirements come from the surgeons who use them and the technicians who maintain them, not the product designers.
7. **[[defense-in-depth-data|Defense in depth and breadth]]** — nuclear power's redundancy on all systems, fallback systems behind primary systems, multiple layers of protection ending in a final physical barrier around the plant itself. Zero-tolerance domains pay for full layering.

## How the strategies map onto SRE practice

Each external strategy has at least one SRE analogue. The mapping is informative because it reveals which SRE practices are imported and which are invented:

| External strategy | SRE practice |
|---|---|
| Live drills (nuclear Navy, lifeguards) | [[testing-disaster-recovery|DiRT]], [[disaster-role-playing|Wheel of Misfortune]], [[breaking-real-systems|Break Real Things]] |
| Simulators with live data (aviation) | [[disaster-role-playing|Wheel of Misfortune]] (the GM simulates the world; players issue text-adventure-style actions) |
| Training and certification (lifeguards) | [[sre-onboarding]], [[on-call-learning-checklist]], [[shadow-on-call]] |
| Defense in depth (nuclear) | [[defense-in-depth-data]], [[barrier-defenses]] |
| Swing capacity (telecom) | Cluster-level [[capacity-planning]], surge capacity for [[norad-tracks-santa]]-class events |
| Detailed requirements (defense, medical) | [[launch-checklist]], [[production-readiness-review]] — but at design time, not pre-launch |
| Attention to detail (Navy) | [[architectural-checklists]], [[operational-overload|toil-discipline keeping engineers fresh enough to notice]] |

## Why the simulation/live-drill split matters

Chapter 33 makes a precise observation about why aviation can't just *test in production* (source: chapter-33-lessons-learned-from-other-industries.md):

> The aviation industry can't perform a live test "in production" without putting equipment and passengers at risk. Instead, they employ extremely realistic simulators with live data feeds, in which the control rooms and equipment are modeled down to the tiniest details to ensure a realistic experience without putting real people at risk.

The trade-off is the same one SRE faces between [[testing-disaster-recovery|DiRT]] (real systems, real customer impact possible) and [[disaster-role-playing|Wheel of Misfortune]] (simulated, no impact). Industries pick the side that matches their failure cost. Lifeguards can stage a near-real drowning because the staged drowning is recoverable in the same way a real one is. Aviation cannot stage a near-real engine failure mid-flight at the same level of fidelity, so the simulator carries more of the load.

The US nuclear Navy's blend — thought exercises *plus* live drills *plus* live drills with control parameters — is a layered version of the same trade-off, with the live-drill cadence (2-3 days per week) calibrated to the failure cost (catastrophic) and the consequence of forgetting (responses must be practised so they are not forgotten).

## Cross-book connections

- [[testing-disaster-recovery]] (SRE Ch 17, 26) — DiRT is Google's annual large-scale exercise; Chapter 33 places it in the live-drill family and pairs it with the simulation family covered by Wheel of Misfortune
- [[disaster-role-playing]] (SRE Ch 28) — the SRE simulator analogue of aviation's control-room simulators; both work because they are realistic enough that practice transfers
- [[recovery-testing]] (SRE Ch 26) — Chapter 26's continuous-recovery-testing argument is the *attention to detail* theme applied to backup pipelines: small drift in unexercised processes accumulates into emergency-time failure
- [[defense-in-depth-data]] (SRE Ch 26) — explicit cross-industry citation: Google's data-integrity defense-in-depth borrows the framing from nuclear-power industry practice
- [[automation-at-google]] (SRE Ch 7) — the *attention to detail* theme is also why Chapter 7's autonomous-system push is so valuable: humans cannot maintain Navy-Submarine-grade vigilance at Google scale, so the systems themselves must
- [[norad-tracks-santa]] (SRE Ch 27) — the Christmas Eve traffic surge is the swing-capacity case Google has actually faced; the launch hardening Petoff covers in Ch 27 is preparedness applied at the launch boundary

## Related pages

- [[lessons-from-other-industries]]
- [[organizational-safety-culture]]
- [[swing-capacity]]
- [[safety-integrity-level]]
- [[testing-disaster-recovery]]
- [[disaster-role-playing]]
- [[recovery-testing]]
- [[defense-in-depth-data]]
- [[breaking-real-systems]]
- [[barrier-defenses]]
- [[architectural-checklists]]
- [[norad-tracks-santa]]
