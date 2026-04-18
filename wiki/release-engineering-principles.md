# Release Engineering Principles

**Summary**: The four principles that guide Google's [[release-engineering]] discipline — **self-service**, **high velocity**, **hermetic builds**, and **enforcement of policies and procedures**. Together they enable thousands of engineers across many products to release frequently and reproducibly without central bottlenecks.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The four principles

> Release engineering is guided by an engineering and service philosophy that's expressed through four major principles. (source: chapter-08-release-engineering.md)

Each principle is catalogued as a separate page so it can be cross-linked from specific mechanisms:

- [[self-service-release-model]] — teams run their own releases; release engineering builds the tools and the defaults
- [[high-release-velocity]] — frequent releases with few changes per version; some teams build hourly and push-on-green
- [[hermetic-builds]] — builds are reproducible; same revision + same build tools = identical output; build tools themselves are versioned
- [[release-policy-enforcement]] — layered access control on who can approve CLs, create releases, approve cherry picks, and deploy

## How they reinforce each other

The principles are not independent — they compose:

- **Self-service + high velocity**: teams can only release hourly if they don't wait for a central release team. The self-service model is the prerequisite for high velocity at Google's scale.
- **Hermetic builds + high velocity**: frequent releases only produce fewer changes per version if each release is reliably identifiable. Hermetic builds make it possible to rebuild the *same* version months later for a bug fix without picking up unrelated drift.
- **Hermetic builds + policy enforcement**: the release audit trail (what CLs, what binaries, what cherry picks) is only trustworthy if the build itself is deterministic.
- **Self-service + policy enforcement**: giving teams autonomy without gated operations would turn the release path into a free-for-all. Policy enforcement makes self-service safe.

## Cross-book connections

- [[change-management-sre]] — the four principles are the foundation on which the "progressive rollout + detection + safe rollback" automation trio rests
- [[continuous-integration-delivery-deployment]] (Bellemare) — the EDM CI/CD pipeline shape presupposes the same four properties (each team owns its pipeline; fast; reproducible; policy-gated)
- [[automation-at-google]] — release engineering is where the [[hierarchy-of-automation-classes|level-4]] discipline of "internally maintained system-specific automation" pays off most visibly

## Related pages

- [[release-engineering]]
- [[self-service-release-model]]
- [[high-release-velocity]]
- [[hermetic-builds]]
- [[release-policy-enforcement]]
- [[change-management-sre]]
