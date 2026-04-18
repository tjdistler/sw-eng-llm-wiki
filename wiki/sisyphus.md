# Sisyphus

**Summary**: A **general-purpose rollout automation framework** developed by Google SRE and used for deployments that are too complicated for [[rapid-release-system|Rapid]] to drive directly. A rollout is a logical unit of work composed of one or more tasks; Sisyphus provides a set of Python classes that can be extended to support any deployment process, plus a dashboard for monitoring and control. Sisyphus is how Google fits the deployment process to the **risk profile of a given service**.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## What Sisyphus is

> For more complicated deployments, we use Sisyphus, which is a general-purpose rollout automation framework developed by SRE. A rollout is a logical unit of work that is composed of one or more individual tasks. Sisyphus provides a set of Python classes that can be extended to support any deployment process. (source: chapter-08-release-engineering.md)

The chapter frames it as a framework (not a system): teams supply the actual deployment logic as Python subclasses, and Sisyphus provides the scaffolding — orchestration, monitoring, dashboard, progress tracking, control.

## Integration with Rapid

Sisyphus is typically driven from Rapid (source: chapter-08-release-engineering.md):

1. Rapid builds and packages the new version.
2. Rapid creates a rollout in a long-running Sisyphus job.
3. Rapid passes the **build label** for the [[midas-package-manager|MPM]] package to Sisyphus.
4. Sisyphus uses the build label to specify which version of the MPM packages should be deployed.

Rapid is good at "build and canary"; Sisyphus is good at "stretch this rollout over eight clusters interleaved across five geographic regions with an exponential expansion schedule." The split keeps each tool focused.

## The risk-matched rollout

The chapter's summary of Sisyphus's purpose (source: chapter-08-release-engineering.md):

> With Sisyphus, the rollout process can be as simple or complicated as necessary. For example, it can update all the associated jobs immediately or it can roll out a new binary to successive clusters over a period of several hours. Our goal is to fit the deployment process to the risk profile of a given service.

Three worked examples the chapter gives:

- **Development / pre-production**: build hourly, push automatically when tests pass.
- **Large user-facing services**: start in one cluster and expand exponentially until all clusters are updated.
- **Sensitive infrastructure**: extend the rollout over several days, interleaving across instances in different geographic regions.

The same Sisyphus primitives produce all three shapes.

## Where Sisyphus sits in the [[change-management-sre]] trio

Sisyphus is primarily the **progressive rollout** half of the trio: exponentially expanding clusters, interleaving regions, risk-matched pacing. Monitoring provides the **detection** half. Rollback (redeploying the previous MPM package via label move) is the **safe-rollback** half.

## Cross-book connections

- [[progressive-delivery]] (Newman / Burns) — Sisyphus is the Google-scale orchestrator for canary and staged rollouts; the "automated release remediation" Newman describes (Spinnaker) is the same idea
- [[desired-state-management]] (Newman) — a Sisyphus rollout is a declarative target state for a population of jobs; the framework drives actual state toward it
- [[operator-pattern]] (Burns) — subclassing Sisyphus's Python classes to implement service-specific rollout logic is structurally equivalent to writing a Kubernetes operator
- [[autonomous-systems]] — Sisyphus is the rollout-engine instance of Google's preference for autonomous orchestration over automated scripts

## Related pages

- [[release-engineering]]
- [[rapid-release-system]]
- [[midas-package-manager]]
- [[change-management-sre]]
- [[progressive-delivery]]
- [[blue-green-deployment]]
- [[rolling-update-pattern]]
