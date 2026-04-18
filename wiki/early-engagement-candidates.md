# Early Engagement Candidates

**Summary**: The three service patterns Chapter 32 names as eligible for the [[early-engagement-model|Early Engagement Model]]. Early engagement requires being able to judge a service's importance before it has production evidence, which means SRE limits it to services whose importance can be inferred from context.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The three qualifying patterns

Chapter 32 lists three characteristics for services that warrant Early Engagement (source: chapter-32-the-evolving-sre-engagement-model.md):

1. **Significant new functionality in an existing SRE-managed system.** The surrounding system is already under SRE care; a significant addition inherits the same reliability requirements by extension
2. **Significant rewrite or alternative targeting the same use cases as an existing system.** The replacement target is known, the reliability bar is known, and the risk of getting it wrong is concrete because there's a system in production to compare against
3. **The development team sought SRE advice or approached SRE for takeover upon launch.** Proactive engagement is a signal; teams that come to SRE early usually know their service needs the attention

All three share the same structural feature: SRE can judge scale, complexity, or importance without having to wait for production traffic to prove it.

## What the judgement requires

Chapter 32 frames the eligibility as a precondition (source: chapter-32-the-evolving-sre-engagement-model.md):

> Applying the Early Engagement Model requires identifying the importance and/or business value of a service early in the development lifecycle, and determining if the service will have sufficient scale or complexity to benefit from SRE expertise.

This is the entrance criterion for [[early-engagement-model|Early Engagement]] the same way service-merits-support + staffing-available is the entrance criterion for the [[simple-prr-model|Simple PRR Model]]. The difference is that Early Engagement's criterion has to be satisfied without production evidence — which is why it's restricted to the three patterns above.

## What SRE is not committing to

Eligibility for Early Engagement does not guarantee SRE takeover. The engagement can end in [[disengaging-from-a-service|disengagement]]: if the service turns out not to warrant full-fledged SRE management post-launch, or if it fails to reach the projected scale, SRE can hand it back or reassign the team. Either outcome is positive — the first because the service has been engineered to be reliable and low-maintenance, the second because the SRE effort is simply the cost of business risk on new projects (source: chapter-32-the-evolving-sre-engagement-model.md).

## Related pages

- [[early-engagement-model]]
- [[simple-prr-model]]
- [[production-readiness-review]]
- [[disengaging-from-a-service]]
- [[sre-engagement-model]]
- [[site-reliability-engineering]]
