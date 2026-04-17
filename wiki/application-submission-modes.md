# Application Submission Modes

**Summary**: Heavyweight stream-processing frameworks accept a job through one of two submission modes — **driver mode** and **cluster mode**. The mode determines where the application's coordination logic runs, how the application is identified by the cluster, and how it is deployed, monitored, and terminated. The choice matters for how well the streaming job fits into an ordinary microservice deployment pipeline (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## Driver mode

Supported by Spark and Flink (source: chapter-11-heavyweight-framework-microservices.md).

A **driver** is a single standalone process — local to the deploying team, not to the cluster — that coordinates execution of the application. The work itself still runs on cluster workers; the driver:

- Negotiates resources with the cluster.
- Sends the topology to the workers.
- Tracks progress and handles errors.
- Emits logs.
- Owns the lifecycle: **terminating the driver terminates the application.**

This lifecycle ownership is why driver mode fits naturally into a [[container-management-system|CMS]]-managed microservice deployment pipeline. The driver can be deployed as an ordinary container managed by the CMS. Worker resources are acquired from the streaming cluster (or from the CMS directly, depending on deployment mode). To deploy a new version, you deploy a new driver container; to stop the job, you stop the container. The streaming job inherits the same rollout and rollback story as any other microservice.

## Cluster mode

Supported by Spark and Flink; the default for Storm and Heron (source: chapter-11-heavyweight-framework-microservices.md).

The entire application — coordination logic included — is submitted to the cluster for management. The cluster returns a **unique job ID**, which is now the only handle to the running application. All subsequent deploy/terminate/monitor commands must go through the cluster's own API using that ID.

This mode works well when the cluster is the operational center of gravity for streaming workloads, but it **does not fit a generic microservice deploy pipeline**: the CI/CD system has to learn the cluster's API, track job IDs out of band, and coordinate version upgrades and terminations against the cluster rather than against a container orchestrator.

## Which mode to pick

| Situation | Preferred mode |
|---|---|
| Team wants streaming jobs to look like ordinary microservices | Driver mode |
| Team deploys via a generic CMS pipeline | Driver mode |
| Team has a mature cluster-ops team and cluster-native tooling | Cluster mode |
| Framework is Storm or Heron | Cluster mode (driver mode not supported) |

The CMS-native deployment trend (Spark-on-Kubernetes, Flink session clusters on Kubernetes — see [[heavyweight-framework-microservice]]) blurs the distinction further: the "cluster" is now just a collection of CMS-managed pods per job, and the deploy pipeline can treat the whole thing as a microservice unit.

## Related pages

- [[heavyweight-framework-microservice]]
- [[stream-processing-cluster]]
- [[container-management-system]]
- [[event-driven-microservices]]
