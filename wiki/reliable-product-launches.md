# Reliable Product Launches at Scale

**Summary**: SRE Chapter 27's hub — Google's approach to the distinctive reliability challenges of launching new products and features at internet-company velocity. A launch is any new code that introduces an externally visible change, and Google performs up to 70 per week; at that rate, a codified launch process becomes worth building. The chapter is organized around three pieces: a dedicated [[launch-coordination-engineering|Launch Coordination Engineering]] team, a curated [[launch-checklist]] that consolidates launch-disaster lessons, and a set of [[gradual-rollout|gradual-rollout]] and [[feature-flag-framework|feature-flag]] techniques that make the launch act itself safer.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## What counts as a launch

Google's operative definition (source: chapter-27-reliable-product-launches-at-scale.md):

> Google defines a launch as any new code that introduces an externally visible change to an application.

The definition is wide on purpose. A new domain name, a UI language rollout, a backend capacity change behind a feature that becomes user-visible — all count. Launches span a huge range of complexity, and the process adapts to each combination of attributes, timing, step count, and complexity.

The rate matters: Google sometimes performs up to 70 launches per week. This is both the **rationale** for and the **opportunity** to build a streamlined process (source: chapter-27-reliable-product-launches-at-scale.md):

> A company that only launches a product every three years doesn't need a detailed launch process. By the time a new launch occurs, most components of the previously developed launch process will be outdated. Nor do traditional companies have the opportunity to design a detailed launch process, because they don't accumulate enough experience performing launches to generate a robust and mature process.

## The NORAD Tracks Santa opening

The chapter opens with [[norad-tracks-santa|NORAD Tracks Santa]]: a Christmas-Eve website that drove Google's Keyhole service to 25x its normal peak (up to one million requests per second) with a hard deadline, heavy publicity, a worldwide audience, and a steep traffic ramp. It had every attribute of a difficult launch in one project. The "Make-children-cry switches" — kill switches protecting services from overload — were named in this context. The case motivates why coordination across engineering groups for risky launches is a distinct SRE activity, not a generic one.

## Criteria for a good launch process

Google's honed criteria (source: chapter-27-reliable-product-launches-at-scale.md):

- **Lightweight** — easy on developers
- **Robust** — catches obvious errors
- **Thorough** — addresses important details consistently and reproducibly
- **Scalable** — accommodates many simple launches and a few complex ones
- **Adaptable** — works for common launches (a new UI language) and novel ones (the initial launch of Chrome or Google Fiber)

Some criteria obviously conflict (lightweight vs thorough). Balancing them is continuous work. The tactics Google uses:

- **Simplicity.** Get the basics right. Don't plan for every eventuality.
- **High touch.** Experienced engineers customize the process to each launch.
- **Fast common paths.** Identify launch classes (e.g. launching in a new country) that follow a pattern, and give them a simplified track.

The underlying observation: engineers will sidestep processes they consider too burdensome, especially in crunch mode. LCE must continuously optimise for the cost/benefit balance.

## The three pieces

### Launch Coordination Engineering (LCE)

A dedicated SRE consulting team that [[launch-coordination-engineering|owns the technical side of launching new products or features]]. LCE audits, mediates, gatekeeps, and educates. See [[launch-coordination-engineer-role]] for the individual role.

### The launch checklist

The central artifact: a curated list of questions, each tied to an action item and a pointer to supporting infrastructure. The checklist is the mechanism that makes the process reproducible. See [[launch-checklist]] for the curation discipline and [[launch-checklist-themes]] for the themes the checklist covers.

### Selected techniques for reliable launches

The chapter closes with three techniques that are particularly load-bearing during launches:

- [[gradual-rollout]] — canary then staged rollout at every layer
- [[feature-flag-framework]] — parallel, small-scope, reversible feature exposure
- [[abusive-client-behavior]] — defending services from client-initiated action without user input
- [[overload-behavior-launches]] — nonlinear degradation and load testing as its counter

## The LCE evolution

The team began informally in Google's early years as a handful of experienced engineers running "Launch Reviews" (source: chapter-27-reliable-product-launches-at-scale.md). As the organisation doubled every year for several years and product deployment requirements grew, a formal LCE team was staffed in 2004 with a dual responsibility: accelerate launches *and* apply SRE expertise to keep reliability and availability high. Launch Reviews became Production Reviews.

By 2008, LCE had processed 1,500+ launches over 3.5 years; about 30% of reviews used a trivial low-risk checklist, because infrastructure and organisational investment had moved many launches out of the high-risk tier. The YouTube acquisition forced network build-out that let smaller launches "fit within the cracks." Larger datacenters let new products co-locate with existing services.

### What LCE did not solve

LCE addressed launch-time risk, but three post-launch pathologies remained structural problems in 2009 (source: chapter-27-reliable-product-launches-at-scale.md):

- **Scalability changes** — products succeeding two orders of magnitude beyond estimates need rearchitecting; migration is expensive and slow
- **Growing operational load** — alert noise, deploy complexity, and manual maintenance creep up and consume service-owner bandwidth (the [[toil-and-engineering-balance|50% toil cap]] is the counter)
- **Infrastructure churn** — when underlying substrate evolves without automated migration, every service owner "runs fast just to stay in the same place"

The chapter names the fixes as company-wide rather than LCE-scoped: better platform APIs, continuous build and test automation, standardisation, and a **churn-reduction policy** that prohibits infrastructure engineers from releasing backward-incompatible features without automated client migration. This is the precondition for [[autonomous-systems|autonomous]] platform evolution that doesn't tax every tenant.

## The central point

The LCE team was Google's answer to achieving **safety without impeding change**. Any company with rapid product growth (doubling product developers every 1-2 years), planning to scale to hundreds of millions of users, and depending on reliability despite high change rates, may benefit from an equivalent function.

## Related pages

- [[launch-coordination-engineering]]
- [[launch-coordination-engineer-role]]
- [[launch-checklist]]
- [[launch-checklist-themes]]
- [[gradual-rollout]]
- [[feature-flag-framework]]
- [[abusive-client-behavior]]
- [[overload-behavior-launches]]
- [[norad-tracks-santa]]
- [[change-management-sre]]
- [[progressive-delivery]]
- [[canary-test]]
- [[sisyphus]]
- [[error-budget]]
- [[toil-and-engineering-balance]]
- [[capacity-planning]]
- [[site-reliability-engineering]]
