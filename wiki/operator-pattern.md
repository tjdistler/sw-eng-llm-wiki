# Operator Pattern

**Summary**: An online program that runs inside a container orchestrator whose single job is to create, scale, upgrade, and maintain a specific application — exposed to users as a declarative desired-state API and itself subject to the same orchestrator's reconciliation.

**Sources**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## Definition

Burns introduces the pattern in the Chapter 9 hands-on deployment of etcd. An **operator** is "an online program that runs inside your container orchestrator with the express purpose of running one or more applications. The operator is responsible for creating, scaling, and maintaining the successful operation of the program. Users configure the application through a desired state API." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md)

The pattern originated at CoreOS. Burns describes it as "still a new idea but [representing] an important new direction in building reliable distributed systems." (source: raw/designing-distributed-systems/chapter-09-ownership-election.md) At the time of the book (2018), operators were an emerging concept; they have since become the standard Kubernetes packaging for complex stateful applications.

## How it works

An operator is itself a container running in the cluster. It (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. Registers a **custom resource definition** with the orchestrator — a new kind of declarative object that users can create, get, and delete like any native object
2. Watches the orchestrator for changes to resources of that custom kind
3. Reconciles the world to match those resources — creating pods, services, persistent volumes, config maps, rotating credentials, handling version upgrades

This makes operators a specialisation of the more general [[desired-state-management]] philosophy: rather than forcing users to compose a stateful application out of raw primitives (StatefulSets, headless services, PVCs, backup CronJobs), the operator encapsulates the application's operational knowledge and presents a single declarative API.

## The etcd operator as worked example

Burns's hands-on walkthrough installs the CoreOS etcd operator via Helm (the Kubernetes package manager, originally developed by Deis, acquired by Microsoft in 2017) (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

```
helm init
helm install stable/etcd-operator
```

Once the operator is running, users describe an etcd cluster declaratively:

```yaml
apiVersion: "etcd.coreos.com/v1beta1"
kind: "Cluster"
metadata:
  name: "my-etcd-cluster"
spec:
  size: 3
  version: "3.1.0"
```

Applying this YAML with `kubectl create` causes the operator to bring up the three-pod etcd cluster (source: raw/designing-distributed-systems/chapter-09-ownership-election.md). The user never writes a pod spec, a service spec, or an init container — those are the operator's implementation detail.

## The recursion: packaging operational expertise

The operator pattern is what allows complex distributed systems to be deployed by anyone who can write a few lines of YAML. It also means the operator itself becomes a place where operational best practices (for leader elections, rolling upgrades, backup scheduling, certificate rotation) accumulate and get shared across organisations.

This is structurally similar to the "community-contribution" closing argument Burns makes about the [[adapter-pattern]] in Chapter 4: by packaging operational knowledge in a container interface, a single author's expertise becomes reusable by any team.

## Relationship to existing patterns

- [[desired-state-management]] — operators are the application-specific implementation of the general principle. Newman discusses desired-state management at the orchestrator level; operators take it one layer up, to specific application management.
- [[ownership-election-pattern]] — operators themselves typically need to be highly available, which means they are usually deployed with [[renewable-leases|leader election]] so exactly one replica is reconciling at a time. The etcd operator is meta-circular: it manages etcd, while often itself using etcd for its own leader election.
- [[modular-reusable-containers]] — operators are the most elaborate expression of Burns's general thesis that operational logic should live in reusable containers rather than scattered across bespoke configuration.

## Related pages

- [[desired-state-management]]
- [[ownership-election-pattern]]
- [[renewable-leases]]
- [[modular-reusable-containers]]
- [[zookeeper]]
- [[consensus]]
- [[microservices]]
- [[designing-distributed-systems]]
