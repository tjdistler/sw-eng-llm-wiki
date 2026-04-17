# Continuous Integration, Delivery, and Deployment

**Summary**: Three related-but-distinct CI/CD stages for getting code changes into production. **Continuous integration** automates build and test on every merge. **Continuous delivery** keeps the codebase deployable but leaves the deploy step manual. **Continuous deployment** fully automates release. Bellemare treats the first two as essential [[microservice-tax]] for any EDM platform and warns that the third is much harder for stateful services.

**Sources**: `raw/building-event-driven-microservices/chapter-16-deploying-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The three stages

(source: chapter-16-deploying-event-driven-microservices.md)

### Continuous integration (CI)

Automating the integration of code changes from multiple contributors into one codebase. A merge to main triggers:

- Build.
- Unit tests.
- Integration tests.
- Style/lint.
- **Schema-evolution validation** for [[event-streams]] — distinctive to EDM.

The output is a ready-to-deploy container or VM image. The goal is to shrink the window between code change and production.

### Continuous delivery

The codebase is **kept deployable**. The CI pipeline validates that every commit could go to production, but the actual deploy is a manual action by the service owner. This is the default posture Bellemare recommends for most EDM services — the owner decides when to deploy.

### Continuous deployment

End-to-end automation: a committed change flows through CI, becomes a deliverable, and is automatically deployed to production per the deployment configuration. No human gate.

Bellemare's warning: "Continuous deployment is difficult to do in practice. Stateful services are particularly challenging, as deployments may require rebuilding state stores and reprocessing event streams, which are especially disruptive to dependent services." (source: chapter-16-deploying-event-driven-microservices.md)

In other words: the moment a deploy might trigger a [[state-store-rebuilding-vs-migrating|state rebuild]] or [[reprocessing-event-streams|stream reprocessing]], you want a human decision between *"is green"* and *"is in prod"*.

## Predeployment validation steps distinctive to EDM

Beyond the usual unit/integration tests, Bellemare calls out two checks that belong specifically in an EDM CI pipeline (source: chapter-16-deploying-event-driven-microservices.md):

- **Event-stream validation** — verify that input streams exist, output streams exist (or are auto-createable), and the service has the required read/write permissions.
- **Schema validation** — run [[schema-evolution]] comparisons for every input and output schema; detect incompatibilities before they reach production. A common convention: schemas live in a known directory structure with a map from schema → stream; the CI step ingests them and runs the compatibility check mechanically.

## Integration tests need their own environment

Bellemare recommends **independent integration testing environments** per service (source: chapter-16-deploying-event-driven-microservices.md). A long-running shared test cluster suffers from multitenancy — one team's test data corrupts another team's assertions. The CI pipeline should be able to spin up a transient, isolated environment for each run (see the [[edm-supportive-tooling|supportive tooling]] section on integration testing).

## Relationship to existing wiki coverage

- **[[microservice-tax]]** — CI/CD is one of the line items Bellemare enumerates.
- **[[container-management-system]]** — the usual deployment target for the CI output.
- **[[progressive-delivery]]** — adds canary / dark-launch / parallel-run on top of the CI/CD foundation.
- **[[end-to-end-testing]]** — Newman's warning about E2E test suite limits applies; EDM CI leans more heavily on integration tests and schema validation.
- **[[deployment-vs-release]]** — the continuous-delivery stance is an operational application of that separation.

## Related pages

- [[microservice-tax]]
- [[container-management-system]]
- [[deployment-vs-release]]
- [[progressive-delivery]]
- [[end-to-end-testing]]
- [[schema-evolution]]
- [[edm-deployment-principles]]
- [[edm-supportive-tooling]]
- [[basic-full-stop-deployment]]
