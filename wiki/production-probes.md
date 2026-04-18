# Production Probes

**Summary**: A family of monitoring requests built from the same bank of known-good and known-bad inputs used in integration and release testing. Chapter 17's argument: the **frontend + backend combinations present in production are different from any that the release tests have previously exercised**, because the two components have independent release cycles. Replaying the test inputs as monitoring probes catches the cross-version skew.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Three request sets

Chapter 17's categorisation (source: chapter-17-testing-for-reliability.md):

- **Known bad requests** — inputs that should produce an error; any other response is a failure.
- **Known good requests that can be replayed against production** — inputs that don't mutate user data; safe to send at any time.
- **Known good requests that can't be replayed against production** — inputs that would mutate state (place an order, delete a resource); usable in hermetic tests only.

The first two sets can be used as integration tests, release tests, **and** monitoring probes. Each context reveals different failures.

## Why probes catch what tests don't

The tests don't see production's topology:

> The release test probably wrapped the integrated server with a frontend and a fake backend. The probe test probably wrapped the release binary with a load balancing frontend and a separate scalable persistent backend. Frontends and backends probably have independent release cycles. It's likely that the schedules for those cycles occur at different rates (due to their adaptive release cadences). Therefore, the monitoring probe running in production is a configuration that wasn't previously tested. Those probes should never fail, but what does it mean if they do fail? Either the frontend API (from the load balancer) or the backend API (to the persistent store) is not equivalent between the production and release environments. Unless you already know why the production and release environments aren't equivalent, the site is likely broken. (source: chapter-17-testing-for-reliability.md)

Production is a matrix of frontend versions × backend versions. Every cell in that matrix is a configuration the release test pipeline didn't fully exercise. Probes are the runtime coverage of those cells.

## Rolling the probes with the service

> The same production updater that gradually replaces the application also gradually replaces the probes so that all four combinations of old-or-new probes sending requests to old-or-new applications are being continuously generated. That updater can detect when one of the four combinations is generating errors and roll back to the last known good state. (source: chapter-17-testing-for-reliability.md)

The probes aren't static; they're released alongside the application. During a rollout there are four combinations to worry about (old/new probe × old/new app), and the updater watches all four.

## Probes as release gate

> Usually, the updater expects each newly started application instance to be unhealthy for a short time as it prepares to start receiving lots of user traffic. If the probes are already inspected as part of the readiness check, the update safely fails indefinitely, and no user traffic is ever routed to the new version. The update remains paused until engineers have time and inclination to diagnose the fault condition and then encourage the production updater to cleanly roll back. (source: chapter-17-testing-for-reliability.md)

A probe failure on a new instance becomes an indefinite pause in the rollout. The instance never takes user traffic; engineers have time to investigate; the rollback can happen cleanly. This is the **integration of [[zero-mttr-testing|zero-MTTR testing]] into the deploy pipeline itself**.

## Forward/backward compatibility probes

> Assume that each component has the older software version that's being replaced and the newer version that's rolling out (now or very soon). The newer version might be talking to the old version's peer, which forces it to use the deprecated API. Or the older version might be talking to a peer's newer version, using the API which (at the time the older version was released) didn't work properly yet. But it works now, honest! You'd better hope those tests for future compatibility (which are running as monitoring probes) had good API coverage. (source: chapter-17-testing-for-reliability.md)

Probes are the mechanism that validate backward and forward compatibility at the API surface during overlap windows. The chapter is dry about how often "it works now, honest" turns out to be wrong.

## Cross-book connections

- [[prober]] (Ch 10) — the tool that runs production probes at Google; Ch 17's conceptual framing is Ch 10's architectural tool made explicit
- [[synthetic-transactions]] (Newman) — Newman's name for scripted end-to-end probes against live production; Ch 17's probes are the same idea with test-pedigree inputs
- [[backward-forward-compatibility]] (Kleppmann / Bellemare) — the compatibility discipline probes verify in production; Kleppmann treats it at the encoding level, Ch 17 at the runtime level
- [[health-probes]] (Burns) — Kubernetes liveness/readiness probes are coarser-grained versions; readiness checks that include full probe runs realise Ch 17's "probe as release gate" idea on Kubernetes
- [[consumer-driven-contracts]] (Newman) — CDCs check compatibility at release time; Ch 17's probes check at runtime; belt + braces

## Related pages

- [[testing-for-reliability]]
- [[prober]]
- [[fake-backend-versions]]
- [[synthetic-transactions]]
- [[zero-mttr-testing]]
