# Disengaging from a Service

**Summary**: A valid outcome of the [[early-engagement-model|Early Engagement Model]] in which SRE ends its engagement without taking over the service. Chapter 32 frames disengagement as a positive outcome when it happens for the right reasons: either the service has been engineered well enough to stay with the development team, or it did not reach the scale that justified SRE attention in the first place.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Two valid disengagement outcomes

Chapter 32 names both of them (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Service is reliable enough to stay with the development team.** "Sometimes a service doesn't warrant full-fledged SRE team management. . . . This is a positive outcome, because the service has been engineered to be reliable and low maintenance, and can therefore remain with the development team." Disengagement here is evidence the Early Engagement worked.
- **Service fails to reach projected scale.** "It is also possible that SRE engages early with a service that fails to meet the levels of usage projected. In such cases, the SRE effort spent is simply part of the overall business risk that comes with new projects, and a small cost relative to the success of projects that meet expected scale." Disengagement here is the company bearing the cost of a new-project bet that didn't pay off.

In both cases the SRE team reassigns, and the lessons from the engagement are incorporated back into the engagement process.

## Why this is worth naming

Without an explicit disengagement path, the Early Engagement Model would be structurally biased toward takeover regardless of whether takeover is warranted. Naming disengagement as a positive outcome de-risks the model: SRE can engage early on speculative candidates without committing to a forever-ownership outcome that might not make sense. The cost of an engagement that ends in disengagement is real but bounded, and the alternative (not engaging at all) is worse because it forecloses the design-phase benefits.

## Contrast with Simple PRR

The [[simple-prr-model|Simple PRR Model]] doesn't have a symmetric "disengage" concept because it runs on already-launched services — by the time PRR starts, the service's importance and scale are known. Early Engagement takes the bet earlier, so it needs an explicit release valve for cases where the bet doesn't pay off.

## Related pages

- [[early-engagement-model]]
- [[early-engagement-candidates]]
- [[simple-prr-model]]
- [[sre-engagement-model]]
- [[site-reliability-engineering]]
