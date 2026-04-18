# Fake Backend Versions

**Summary**: A hermetic release test typically combines a candidate frontend binary with a **fake backend** maintained by the peer service's engineering team. Chapter 17's argument: that fake should be cut at the same revision as the peer's main backend and its [[production-probes|probes]], so the frontend release tests are exercising a known coordinate in the cross-product of frontend and backend versions.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The release-time pairing

> When implementing release tests, the fake backend is often maintained by the peer service's engineering team and merely referenced as a build dependency. The hermetic test that is executed by the testing infrastructure always combines the fake backend and the test frontend at the same build point in the revision control history. (source: chapter-17-testing-for-reliability.md)

Two consequences of the pairing discipline:

- The fake backend's behaviour tracks the real backend's behaviour. When the peer changes a contract, the fake updates too, which fails the frontend's release test immediately — the exact behaviour you want.
- The fake is a **runnable hermetic binary**, cut on the same release schedule as the peer's main backend. This is what makes the "combination of front and back at same revision" property achievable.

## The release-package addition

> If that backend release is available, it might be worthwhile to include hermetic frontend release tests (without the fake backend binary) in the frontend release package. (source: chapter-17-testing-for-reliability.md)

The release package can then ship with tests that can run against either the fake (for hermetic validation) or the real backend (for production probe runs). One asset, two uses.

## Testing every combination

> Your monitoring should be aware of all release versions on both sides of a given service interface between two peers. This setup ensures that retrieving every combination of the two releases and determining whether the test still passes doesn't take much extra configuration. This monitoring doesn't have to happen continuously — you only need to run new combinations that are the result of either team cutting a new release. (source: chapter-17-testing-for-reliability.md)

The combination testing happens opportunistically: when either side cuts a new release, the monitoring runs the cross-product against the fake backends (or production probes) of every other version. Failures in specific combinations become release-gate signals.

## When to block rollout

> Such problems don't have to block that new release itself. On the other hand, rollout automation should ideally block the associated production rollout until the problematic combinations are no longer possible. Similarly, the peer team's automation may consider draining (and upgrading) the replicas that haven't yet moved from a problematic combination. (source: chapter-17-testing-for-reliability.md)

The nuance: a broken combination **doesn't block the release** — it blocks the **rollout** of the release into an environment where the broken combination could occur. The distinction preserves release cadence for the producing team while protecting users from the version skew.

## Cross-book connections

- [[production-probes]] — the runtime complement; probes and fake backends are the two sides of the same test-in-production idea
- [[backward-forward-compatibility]] (Kleppmann) — the compatibility property fake-backend cross-product testing verifies; Kleppmann treats it at the encoding layer, Ch 17 at the deployment layer
- [[deployment-vs-release]] (Newman) — the "release doesn't have to block, rollout does" distinction is Newman's deployment/release split applied to cross-service coordination
- [[consumer-driven-contracts]] (Newman) — CDC is an alternative to maintaining a fake backend: rather than faking the peer, express the peer's expectations as executable specs the peer itself runs
- [[hosted-service-mocks]] (Bellemare) — the EDM-era analogue: emulators / mocks for hosted services; same idea, same maintenance-of-alignment problem

## Related pages

- [[testing-for-reliability]]
- [[production-probes]]
- [[integration-tests]]
- [[system-tests]]
- [[consumer-driven-contracts]]
- [[hosted-service-mocks]]
