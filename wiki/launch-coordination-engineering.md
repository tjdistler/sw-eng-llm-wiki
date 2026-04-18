# Launch Coordination Engineering (LCE)

**Summary**: Google's dedicated consulting team within SRE, tasked with the technical side of launching new products and features. LCE audits for compliance with Google's reliability standards, acts as a liaison between teams, drives technical momentum on launches, signs off as gatekeeper, and educates developers. Formally staffed in 2004 to resolve the tension between SRE's caution and the product developers' need for velocity.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`, `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Why a dedicated team

Good software engineers understand their own products deeply but are often unfamiliar with the challenges of launching to millions of users while maintaining performance and minimising outages (source: chapter-27-reliable-product-launches-at-scale.md). LCE centralises that knowledge in a team that sees hundreds of launches across Google's product areas rather than one or two per product.

The five LCE activities (source: chapter-27-reliable-product-launches-at-scale.md):

1. **Audit** products and services for compliance with Google's reliability standards and best practices, and provide specific actions to improve reliability.
2. **Liaise** between the multiple teams involved in a launch.
3. **Drive** the technical aspects so tasks maintain momentum.
4. **Gatekeep** — sign off on launches determined to be safe.
5. **Educate** developers on best practices, equipping them with documentation and training resources.

Most audits happen before launch. Even products with strong SRE support engage LCE for critical launches, because launch challenges differ substantially from steady-state operation — and LCE draws on hundreds of launches' worth of experience. LCE also facilitates service audits when SRE first onboards a service.

## Advantages of centralising

The team structure produces three cross-cutting advantages that a product-embedded launch expert could not (source: chapter-27-reliable-product-launches-at-scale.md):

- **Breadth of experience.** A true cross-product team with active engagement across nearly all of Google's product areas. Extensive cross-product knowledge and cross-team relationships make LCEs excellent knowledge-transfer vehicles.
- **Cross-functional perspective.** LCEs hold a holistic launch view and coordinate disparate teams across SRE, development, and product management — particularly useful for complex launches spanning half a dozen teams in multiple time zones.
- **Objectivity.** As a non-partisan advisor, LCE balances and mediates between stakeholders (SRE, product developers, PMs, marketing). Because LCE is structurally an SRE role, **LCEs are incentivized to prioritise reliability over other concerns**. The incentive structure is a deliberate design choice, and a company with different priorities may need a different structure.

## How launches pass through LCE

LCE [[launch-checklist|runs each launch through a curated checklist]] that has been accumulated and re-curated over more than a decade. The checklist is LCE's central artifact — a reproducibly reliable launch requires that the right questions are asked and the right action items are completed. Beyond the checklist, LCE provides specific technical guidance, often escalating pain points to owners of common infrastructure to drive convergence and simplification (see below).

## Driving convergence

LCE's cross-cutting view makes it an unusual vehicle for **driving convergence on shared infrastructure**. In a large organisation without a coordinating function, engineers reimplement common capabilities (rate limiting, quotas, push systems, release tooling) because they're unaware of existing solutions. LCE recommends existing hardened infrastructure as building blocks, which:

- Cuts duplicate effort
- Makes knowledge transferable between services
- Produces higher engineering quality via concentrated infrastructure attention

The checklist benefits too: long sections on rate-limiting requirements became "Implement rate limiting using system X." LCE also identifies simplification opportunities by witnessing common stumbling blocks firsthand — which approval processes are arduous, which steps are slow, which problems get re-solved, where common infrastructure is lacking.

## Launching into novel territory

When a launch enters a genuinely new product space (Android, Chrome, Google Fiber), much of the existing checklist may not apply. The chapter's discipline for these cases (source: chapter-27-reliable-product-launches-at-scale.md):

> An LCE facing an unusual launch must return to abstract first principles of how to execute a safe launch, then respecialize to make the checklist concrete and useful to developers.

The Android example: the checklist was built around services Google could fix in hours by pushing new JavaScript. Mobile devices with client-side logic Google didn't directly control changed everything. LCE engaged mobile domain experts to identify which existing checklist items translated, and which new ones were needed. The **intent** of each question — not its concrete wording — is what generalises.

## LCE's structural origin

LCE began as an informal group of experienced "Launch Engineers" running "Launch Reviews" days-to-weeks before launch. As Google doubled every year and deployment requirements multiplied, two trends collided:

- Inexperienced product engineers couldn't stay current on safe deployment practices
- Inexperienced SREs were becoming overly cautious, slowing launches

The resulting SRE-dev negotiations threatened launch velocity. In 2004, SRE staffed LCE full-time with the dual mandate: **accelerate launches** while **applying SRE expertise** to keep availability and latency high. Launch Reviews became Production Reviews.

By 2008, 30% of LCE reviews were classed low-risk (no new server executables, traffic increase under 10%) and got a trivial checklist; higher-risk launches got the full review. Meanwhile, infrastructure investment (larger datacenters, better network) moved many previously-risky launches into the easy tier.

## LCE as SRE consultation (Chapter 32)

Chapter 32 places LCE inside the broader [[sre-alternative-support|alternative support]] framing: LCE is the consultation arm of SRE, used primarily at launch time. "The Launch Coordination Engineering (LCE) team spends a majority of its time consulting with development teams" (source: chapter-32-the-evolving-sre-engagement-model.md). For services that will never receive full SRE engagement, an LCE launch consultation may be the only direct SRE involvement they get — the chapter frames this explicitly as one of the two fallback support modes (docs + consulting) for services that don't warrant takeover.

Chapter 32 also notes that LCE facilitates service audits when SRE first onboards a service — so LCE effort overlaps with the [[prr-analysis-phase|PRR Analysis phase]] on takeover-bound services. The chapter's "a few hours studying the design and implementation" framing for launch consultation is narrower than a full PRR, which is why services that *do* need takeover run the [[simple-prr-model|Simple PRR Model]] rather than relying on LCE alone.

## Problems outside LCE's scope

LCE fixed launch-time risk but not three longer-horizon pathologies (source: chapter-27-reliable-product-launches-at-scale.md): **scalability rearchitectures**, **growing operational load** (see [[toil-and-engineering-balance]]), and **infrastructure churn**. The fix for these is structural — better platform APIs, test automation, standardisation, and a **churn-reduction policy** requiring infrastructure engineers to automate the migration of clients before releasing backward-incompatible features.

## Related pages

- [[reliable-product-launches]]
- [[launch-coordination-engineer-role]]
- [[launch-checklist]]
- [[launch-checklist-themes]]
- [[toil-and-engineering-balance]]
- [[change-management-sre]]
- [[sre-discipline]]
- [[autonomous-systems]]
- [[sre-engagement-model]]
- [[sre-alternative-support]]
- [[simple-prr-model]]
- [[production-readiness-review]]
- [[site-reliability-engineering]]
