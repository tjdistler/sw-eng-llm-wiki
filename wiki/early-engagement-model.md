# Early Engagement Model

**Summary**: The [[sre-engagement-model|SRE engagement]] pattern that moves the [[production-readiness-review|PRR]] conversation from post-launch to the Design phase. SRE joins the development team during design, collaborates through Build and Launch, and eventually takes over any time during or after Build. The earlier SRE engages, the cheaper the reliability fixes and the smoother the launch.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Why earlier is better

Chapter 32 opens with the software-engineering analogy: the earlier a bug is found, the cheaper it is to fix. SRE consultation is the same shape (source: chapter-32-the-evolving-sre-engagement-model.md):

> When SRE is engaged during the earliest stages of design, the time to onboard is lowered and the service is more reliable "out of the gate," usually because we don't have to spend the time unwinding suboptimal design or implementation.

The [[simple-prr-model|Simple PRR Model]] is structurally late: by the time SRE reviews a launched service, expensive design choices have already been made and many of them are expensive to reverse. The Early Engagement Model puts SRE in the room before those choices become expensive.

## Where SRE plugs into the lifecycle

Under Early Engagement, SRE participates in every phase of the service lifecycle (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Design phase.** SRE collaborates on architecture, dependency choices, and reliability-affecting trade-offs. The chapter's framing: "The best production incidents are those that never happen." Difficult design trade-offs are made with SRE awareness, minimising future disputes about choices once the service is in production.
- **Build phase.** SRE influences implementation through recommending specific libraries and components and helping build controls (instrumentation, metrics, operational and emergency controls, resource efficiency) into the system. Participation here also lets SRE accumulate operational experience in advance of launch.
- **Launch phase.** SRE helps implement widely used launch patterns — [[reliable-product-launches|gradual rollouts]], [[canary-test|canaries]], and dark launches (traffic mirrored to the new service, responses thrown away). A smooth launch keeps post-launch operational burden low and development momentum high.
- **Post-launch.** With a stable system at launch time, the product-development team faces fewer conflicting priorities between reliability and new features. Refactoring or redesign decisions in later phases are better informed by the lessons from earlier phases.

The PRR's objectives (verify readiness, improve reliability) don't change — but most of the work that the [[prr-improvements-and-refactoring|Improvements phase]] does under the Simple PRR Model is distributed across Design and Build under Early Engagement, so Onboarding happens much earlier and much more cheaply.

## Who's eligible

Not every service warrants Early Engagement. See [[early-engagement-candidates]] for the three patterns Chapter 32 identifies (significant new functionality in an SRE-managed system, significant rewrites of SRE-managed services, dev teams that proactively approach SRE).

## Benefits over Simple PRR

Chapter 32 enumerates the gains (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Cheaper design fixes.** Changes at design time cost far less than changes after launch
- **Less future dispute.** SRE's participation in the design trade-offs means fewer later arguments about "why was it done this way?"
- **Faster onboarding.** The SRE team is ready to take over much sooner than the Simple PRR Model allows
- **Stronger relationship.** Long, close collaboration builds the ownership and solidarity the steady-state partnership runs on
- **Lower operational burden post-launch.** Stability at launch means fewer conflicting priorities for the development team

## Disengagement as a valid outcome

One subtlety Chapter 32 calls out: SRE may engage early and then [[disengaging-from-a-service|disengage]]. Some services turn out to be reliable and low-maintenance enough that SRE takeover isn't warranted — a positive outcome, because the service has been engineered to be reliable. Others fail to meet projected scale, in which case the SRE effort is part of the business risk of new projects (source: chapter-32-the-evolving-sre-engagement-model.md).

## Limits

Chapter 32 is honest about the costs (source: chapter-32-the-evolving-sre-engagement-model.md): additional communication between teams, demand on the right SRE reviewers' time, and the requirement that SRE work be highly visible for knowledge transfer. Early Engagement reduces the late-stage tax but doesn't eliminate coordination cost. The [[frameworks-and-sre-platform|Frameworks and SRE Platform]] model is the next step — rather than engage early on each service, build SRE expertise into the platform so services inherit it by construction.

## Related pages

- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[production-readiness-review]]
- [[early-engagement-candidates]]
- [[disengaging-from-a-service]]
- [[frameworks-and-sre-platform]]
- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
- [[canary-test]]
- [[site-reliability-engineering]]
