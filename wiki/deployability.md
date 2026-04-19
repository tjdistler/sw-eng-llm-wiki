# Deployability

**Summary**: An architecture characteristic that covers three dimensions together: **ease of deployment**, **frequency of deployment**, and **risk of deployment**. One of the three components of [[agility]] in Ford and Richards's decomposition. Monoliths score low on all three; architectural modularity improves all three provided services remain independently deployable.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`

**Last updated**: 2026-04-19

---

## Three dimensions, not one

Chapter 3 of *Software Architecture: The Hard Parts* (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> Deployability is not only about the ease of deployment—it is also about the frequency of deployment and the overall risk of deployment. To support agility and respond quickly to change, applications must support all three of these factors.

All three dimensions must be good; improving one at the expense of another does not yield deployability. A team that deploys daily but rolls back 30% of deployments has high frequency and high risk — net negative. A team that deploys effortlessly once per quarter has high ease and low frequency — also net negative.

**Ease** — the mechanical cost of a deployment. CI/CD pipelines, infrastructure-as-code, container registries, orchestration platforms all contribute.

**Frequency** — how often a deployment can happen. Coupled to ease (hard deployments happen rarely) and to risk (risky deployments are gated by change-advisory boards). Deployment frequency is one of the four [[dora-metrics|DORA metrics]] of engineering organisation health.

**Risk** — the probability that a deployment causes an incident, plus the blast radius if it does. Reduced by small deploy units (smaller diff per release), [[progressive-delivery|progressive delivery]], and [[blue-green-deployment|blue-green]] / [[canary-test|canary]] techniques.

## Why monoliths score low

Chapter 3's argument:

- **Ceremony.** Code freezes, mock deployments, release windows, change-approval boards.
- **Risk.** Any change may break any feature because the whole application is in one process; a UI change can regress an unrelated payment path.
- **Long intervals.** Weeks to months between deployments. Long intervals force each deployment to bundle many changes, which amplifies risk and makes post-deployment diagnosis harder.

The three failure modes compound. Long intervals make deployments big; big deployments carry high risk; high risk justifies heavy ceremony; heavy ceremony increases the interval.

## How architectural modularity improves deployability

[[architectural-modularity|Smaller independently-deployed units]] invert the compounding:

- **Less ceremony** because the blast radius of a failed deploy is one service.
- **Less risk** because each deploy contains only that service's changes.
- **Higher frequency** because small low-risk deploys can happen many times a day.

This is Newman's [[independent-deployability]] argument dressed in the five-driver rubric. The architect's prize is not "deployments happen" but "deployments happen often enough that small changes can ship individually, and *that* keeps risk-per-deploy low, and *that* is what makes agility real."

## The chatter / lock-step failure mode

Deployability's modularity benefit collapses if services must deploy together. Chapter 3 quotes Matt Stine's article on orchestrating microservices (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> If your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain.

This is the [[distributed-monolith]] pathology. Deploy-time coupling between services is a deployability anti-pattern; it negates the reason for adopting modularity in the first place.

Chapter 3 calls the endpoint — where so much chatter exists that no service can deploy without coordinating with several others — the **"big ball of distributed mud"**. The architect's defences are the usual trio: stable contracts, versioned APIs, and asynchronous messaging, plus [[consumer-driven-contracts]] to keep contracts honest without requiring every change to be tested cross-service pre-deploy.

## Deployability and the other drivers

Deployability is tightly interleaved with the other architectural-modularity drivers:

- **[[testability]]** is a pre-requisite. Can't deploy frequently if the test suite takes hours.
- **[[fault-tolerance]]** covers runtime risk; deployability covers deploy-time risk. Progressive-delivery techniques are the bridge (canaries catch deploy-time regressions as they occur rather than after they propagate).
- **[[elasticity]]** benefits from fast deployments — if a service instance can be brought up quickly (low MTTS), horizontal scaling is essentially "deploy another instance."

## Measurement

Chapter 6 of *Fundamentals of Software Architecture* places deployability on the **process axis** of architecture-characteristic measurement (source: `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`, referenced via [[architecture-characteristics]]). Typical fitness functions:

- Deployment frequency (deployments per day / week).
- Deployment lead time (commit to production).
- Change failure rate (percentage of deploys requiring rollback or hotfix).
- Mean time to recovery (MTTR) after a failed deploy.

These are three of the four DORA metrics — deployability is the architecture-level counterpart of the engineering-practice measurements DORA made mainstream.

## The deployment-vs-release distinction

Deployability is about *deployment* — getting the artefact to the production environment. It is distinct from *release* — exposing new behaviour to users. See [[deployment-vs-release]]: the two are decoupled via [[feature-toggle|feature toggles]], dark launches, and progressive rollout, which let an architecture deploy continuously while releasing features on a separate cadence. This split is what makes high-frequency deployment safe in practice: most deploys contain no user-visible change.

## Relation to other wiki concepts

- [[independent-deployability]] — Newman's formulation of the same concept: "deploy one service without deploying anything else."
- [[agility]] — deployability is one of its three components.
- [[maintainability]], [[testability]] — the sibling components; agility requires all three.
- [[architectural-modularity]] — the structural enabler.
- [[distributed-monolith]] — the failure mode that kills deployability despite superficial modularity.
- [[progressive-delivery]], [[blue-green-deployment]], [[canary-test]] — the techniques that reduce risk-per-deploy.
- [[continuous-integration-delivery-deployment]] — the engineering practice that makes high-frequency deployability routine.

## Related pages

- [[agility]]
- [[maintainability]]
- [[testability]]
- [[architectural-modularity]]
- [[architecture-characteristics]]
- [[architecture-fitness-function]]
- [[independent-deployability]]
- [[distributed-monolith]]
- [[deployment-vs-release]]
- [[blue-green-deployment]]
- [[canary-test]]
- [[continuous-integration-delivery-deployment]]
- [[feature-toggle]]
- [[software-architecture-the-hard-parts]]
