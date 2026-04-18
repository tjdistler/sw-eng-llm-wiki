# Near-Miss Reporting

**Summary**: Chapter 33's preemptive-postmortem mechanism imported from manufacturing, chemical, aviation, and maritime industries — events where a given action could have caused serious harm but did not are scrutinised the same way actual incidents are. VM Brasseur's framing: *"There are multiple near misses in just about every disaster and business crisis, and typically they're ignored at the time they occur. Latent error, plus an enabling condition, equals things not working quite the way you planned."* The UK's CHIRP (Confidential Reporting Programme for Aviation and Maritime) provides a central confidential reporting point with periodic newsletters analysing the reports.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## What a near miss is

Chapter 33's definition (source: chapter-33-lessons-learned-from-other-industries.md):

> "Near misses" — when a given event could have caused serious harm, but did not — are carefully scrutinized.

The structural argument: a near miss has the same root causes as the disaster it would have become; it merely lacked the final triggering condition. Treating near misses as ignorable wastes the diagnostic information they carry, and guarantees that the next near miss in the same chain will eventually be the actual disaster.

VM Brasseur's framing from a 2015 talk (source: chapter-33-lessons-learned-from-other-industries.md):

> Latent error, plus an enabling condition, equals things not working quite the way you planned.

A near miss is the latent error visible without the enabling condition having lined up. Once you see one near miss, you know the latent error is in the system; the only question is when it will catch the enabling condition.

## Examples Chapter 33 names

Chapter 33 lists three concrete near-miss scenarios (source: chapter-33-lessons-learned-from-other-industries.md):

- A worker doesn't follow the standard operating procedure — but nothing happens this time.
- An employee jumps out of the way at the last second to avoid a splash.
- A spill on the staircase isn't cleaned up — but nobody falls today.

Each is a free observation of a failure mode that the system is currently surviving by luck rather than by design.

## CHIRP — confidential reporting infrastructure

Chapter 33's named mechanism (source: chapter-33-lessons-learned-from-other-industries.md):

> The United Kingdom's CHIRP (Confidential Reporting Programme for Aviation and Maritime) seeks to raise awareness about such incidents across the industry by providing a central reporting point where aviation and maritime personnel can report near misses confidentially. Reports and analyses of these near misses are then published in periodic newsletters.

Two structural choices encoded:

- **Confidential reporting** — removes the personal cost of surfacing a near miss the reporter was involved in. Without confidentiality, near-miss reports reduce to *"someone else almost made a mistake"* and the genuinely informative *"I almost made a mistake"* reports go missing.
- **Cross-industry aggregation** — periodic newsletters distribute the lesson beyond the originating organisation. The next aviation operator on the other side of the world doesn't have to re-encounter the same near miss to learn from it.

## How this maps onto SRE practice

SRE has partial near-miss coverage but Chapter 33 doesn't claim Google does this fully. The closest analogues:

- **[[blameless-postmortem|Blameless postmortems for non-paging incidents]]** — Chapter 1 specifically calls out that postmortems should be written even when they didn't page, because non-paging postmortems often signal monitoring gaps. A non-paging postmortem is functionally a near-miss report at the team level: *something went wrong but the impact was below the alerting threshold*.
- **[[outage-tracking|Outage tracking]] (Ch 16)** — captures every alert and outage, including the chronic-low-impact ones that don't trigger postmortems. The aggregation produces the cross-event view CHIRP provides cross-industry.
- **[[postmortems-at-google-working-group|Postmortems at Google working group]] (Ch 15)** — does the cross-product trend analysis that periodic CHIRP newsletters do for aviation.

What's structurally missing in the SRE picture: **confidential reporting** as a first-class mechanism. Postmortems are blameless but not confidential. The implicit assumption is that blamelessness suffices to remove the personal cost of disclosure. CHIRP's existence in safety-critical fields suggests confidentiality and blamelessness solve overlapping but distinct problems.

## Why this matters

Near-miss reporting is the structural answer to the *significance bar* problem in [[postmortem-philosophy|Chapter 15]]: postmortems are written for incidents above a threshold, leaving the most informative low-impact-but-systemic events uncaptured. Adding a deliberate near-miss channel — even informally — extends the postmortem corpus into the territory where most of the latent-error population actually lives.

A practical reframe: every page that *fired but turned out to be low-impact* is a near-miss in disguise. Tracking those, not just the post-mortem-eligible incidents, is the discipline.

## Cross-book connections

- [[blameless-postmortem]] (SRE Ch 1, 11, 12, 13, 14, 15) — non-paging postmortems are SRE's partial near-miss mechanism
- [[postmortem-philosophy]] (SRE Ch 15) — the significance-bar problem near-miss reporting is designed to address
- [[postmortem-triggers]] (SRE Ch 15) — Google's documented triggers include monitoring failures (a near-miss in disguise) and stakeholder requests
- [[outage-tracking]] (SRE Ch 16) — the breadth-not-depth complement that captures chronic low-impact events
- [[postmortems-at-google-working-group]] (SRE Ch 15) — the cross-product trend analysis that does CHIRP-style aggregation inside Google
- [[organizational-safety-culture]] (SRE Ch 33) — the empowered-to-speak-up cultural precondition that near-miss reporting depends on
- [[lessons-from-other-industries]] (SRE Ch 33) — Chapter 33 hub

## Related pages

- [[lessons-from-other-industries]]
- [[organizational-safety-culture]]
- [[blameless-postmortem]]
- [[postmortem-philosophy]]
- [[postmortem-triggers]]
- [[outage-tracking]]
- [[postmortems-at-google-working-group]]
