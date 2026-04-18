# Velocity vs Reliability Trade-off

**Summary**: Chapter 33's closing argument — Google has *a higher appetite for velocity* than most other high-reliability industries because most of its products operate where users are inconvenienced, not injured, when something goes wrong. Nuclear, aviation, and medical industries warrant a more conservative approach because incidents can cost lives. Where lives are not at stake, the [[error-budget|error budget]] mechanism funds a culture of innovation and calculated risk-taking. Google's reliability work is therefore an *adaptation* of practices honed in other industries, not a copy.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## The closing argument

Chapter 33's main takeaway from the cross-industry survey (source: chapter-33-lessons-learned-from-other-industries.md):

> A main takeaway of our cross-industry survey was that in many parts of its software business, Google has a higher appetite for velocity than players in most other industries. The ability to move or change quickly must be weighed against the differing implications of a failure. In the nuclear, aviation, or medical industries, for example, people could be injured or even die in the event of an outage or failure. When the stakes are high, a conservative approach to achieving high reliability is warranted.

The structural claim: the conservative practice of regulated industries is **correctly calibrated** to their failure cost. They aren't slower than they need to be; they are exactly as slow as the failure consequences require. Google can be faster because most Google failures aren't in the same consequence class.

## How error budgets fund the difference

Chapter 33 names [[error-budget|error budgets]] explicitly as the mechanism (source: chapter-33-lessons-learned-from-other-industries.md):

> At Google, we constantly walk a tightrope between user expectations for high reliability versus a laser-sharp focus on rapid change and innovation. While Google is incredibly serious about reliability, we must adapt our approaches to our high rate of change. As discussed in earlier chapters, many of our software businesses such as Search make conscious decisions as to how reliable "reliable enough" really is. Google has that flexibility in most of our software products and services, which operate in an environment in which lives are not directly at risk if something goes wrong. Therefore, we're able to use tools such as error budgets as a means to "fund" a culture of innovation and calculated risk taking.

The chain:

1. **Lives are not directly at risk** → 100% reliability is not the right target.
2. **A target below 100% is acceptable** → there is unreliability budget left over.
3. **The leftover budget funds velocity** → launches, experiments, risky changes are paid for from that budget.
4. **Velocity is the competitive lever** → faster iteration produces better products at the consequence-cost the business has decided to accept.

In an industry where step 1 fails (lives *are* at risk), the entire chain unwinds and you end up at the conservative end with the rest of nuclear and aviation.

## Where Google itself sits at the conservative end

The chapter is careful to acknowledge that not all of Google's products are velocity-optimised. The SRE book's own Chapter 1 names *pacemakers and anti-lock brakes* as the rare cases where 100% reliability is the right target. Within Google's portfolio, the applications closer to safety-critical (Google Maps used for navigation, payment systems, health-data products) get treated more like the regulated industries the chapter surveys.

The error-budget mechanism doesn't *force* high velocity; it *enables* it where the consequence cost permits. A Google service whose product owner picks 99.999% has a much smaller budget to spend than one that picks 99.9%, and the velocity that smaller budget funds is correspondingly lower.

## What Google adopts and what it doesn't

The Chapter 33 survey makes the import-or-not pattern visible:

- **Adopted from healthcare/avionics**: blameless postmortem culture (see [[blameless-postmortem]])
- **Adopted from FEMA/firefighting**: incident command structure (see [[incident-command-system]])
- **Adopted from aviation cockpits**: triage discipline (see [[triage-sre]] — *fly the airplane first*)
- **Adopted from nuclear power**: defense in depth (see [[defense-in-depth-data]])
- **Adopted from manufacturing/research**: controlled-experiment culture (see [[structured-and-rational-decision-making]])
- **Adopted from manufacturing**: checklist discipline (see [[architectural-checklists]])
- **Not adopted from defense contracting**: a year of design before three weeks of code
- **Not adopted from US nuclear Navy**: three-human valve operation; manual chain-of-trust over automation
- **Not adopted from telecom**: keep the 1980s switches because they work
- **Not adopted from regulated industries**: government-imposed safety standards as the target setter

The pattern: Google takes the **practices that compose with high velocity** and leaves the **practices that structurally limit velocity**. Both sets of practices are correct in their original contexts — the choice of which ones to import is an intentional design decision keyed to Google's distinctive failure-cost profile.

## Why this is a chapter-closing argument

Chapter 33's organising thesis is that SRE didn't invent reliability engineering — most of the practices have older analogues in older industries. The closing argument explains *why* the SRE adaptation looks different from the source disciplines: not because SRE is sloppier or more clever, but because Google's products live at a different point on the velocity-vs-reliability trade-off curve, and the engineering response is correctly different at that point.

This framing matters because it both **legitimises** SRE (by tracing its practices to industries with proven reliability records) and **delimits** SRE (by being clear that the higher-velocity adaptation isn't suitable for industries where lives are at stake).

## Cross-book connections

- [[error-budget]] (SRE Ch 1, 3) — the structural mechanism by which the velocity-vs-reliability trade-off is operationalised; Chapter 33 names it explicitly as the funding source for innovation culture
- [[risk-management-sre]] (SRE Ch 3) — the explicit framing of risk as a continuum that can be tuned per service rather than maximised universally
- [[risk-tolerance]] (SRE Ch 3) — the per-service framing of acceptable risk, including the consumer-vs-infrastructure distinction
- [[service-level-objective]] (SRE Ch 1, 4) — the SLO is the per-service expression of where on the velocity-vs-reliability curve a product sits
- [[high-release-velocity]] (SRE Ch 8) — release engineering's frequent-releases-mean-fewer-changes-per-version argument is the *technical* enabler of the velocity Chapter 33 argues the *cultural* basis for
- [[push-on-green]] (SRE Ch 2, 8) — the operational endpoint of high velocity: every passing build is automatically deployed
- [[lessons-from-other-industries]] (SRE Ch 33) — the chapter hub
- [[architecture-fitness-function]] (Richards & Ford) — fitness functions are the architecture-side mechanism for keeping reliability characteristics within the budget; same conceptual move

## Related pages

- [[lessons-from-other-industries]]
- [[error-budget]]
- [[risk-management-sre]]
- [[risk-tolerance]]
- [[service-level-objective]]
- [[high-release-velocity]]
- [[push-on-green]]
- [[blameless-postmortem]]
- [[incident-command-system]]
- [[triage-sre]]
- [[defense-in-depth-data]]
- [[architectural-checklists]]
- [[structured-and-rational-decision-making]]
