# Worker Container Interface

**Summary**: The consumer side of Burns's [[work-queue-pattern]]. A **worker container** processes one work item and exits; the queue-manager spawns a fresh worker per item via the container orchestrator. Burns uses a **file-based API** — an environment variable points at a file containing the work item's data — rather than HTTP, for reasons of simplicity, security, and shell-script ergonomics.

**Sources**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`

**Last updated**: 2026-04-16

---

## How it differs from the source interface

The worker interface differs from the [[source-container-interface]] in three important ways (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

1. **It is a one-off API.** A single call starts the work; no further calls happen during the worker's life. Contrast the source, which the queue-manager polls repeatedly.
2. **It is cross-pod, not in-pod.** The worker runs in its own container group, scheduled by the orchestrator to wherever capacity is available — not coresident with the queue-manager the way the source ambassador is.
3. **Cross-pod means security matters.** Anything listening on the network in a cluster could in principle receive work from a different, malicious user. A file-based API inside the worker's own filesystem is harder to abuse.

## The file-based API

When the orchestrator schedules a worker container, the queue-manager arranges for an environment variable named `WORK_ITEM_FILE` to point at a file in the worker's filesystem; the `data` field from the work item has been written into that file (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).

Concretely, Burns implements this on Kubernetes via a **ConfigMap** mounted into the worker pod as a file. The worker reads the file, does its work, and exits — zero, one-time HTTP handshake required.

### Why files beat HTTP for this case

Burns explicitly argues for the file-based API over HTTP on ergonomic grounds: "a work queue worker is simply a shell script across a few command line tools. In that context, spinning up a web server to manage the work to perform is an unnecessary complexity" (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). Any shell script that reads an env var and an input file can be a worker; the worker does not have to be an HTTP server.

The same argument that pushed the source interface to HTTP (repeated polling between tightly coscheduled containers) pushes the worker interface *away* from HTTP (one-shot, isolated, possibly non-server code).

## Kubernetes Job as the reliability substrate

A worker is scheduled as a **Kubernetes Job** (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). A Job can be configured to run the worker container until it completes successfully, and Kubernetes guarantees that even if a machine in the cluster fails, the job will eventually run to success. The orchestrator, not the queue-manager, is responsible for the reliable execution of each item.

Two additional Kubernetes facilities make this work cleanly:

- **Job annotations** let the queue-manager tag each Job with the work item it is processing, so a later `list_namespaced_job` call can reveal exactly which items are in flight and which have completed (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md).
- **Restart policy `Never`** on the pod template (used in Burns's Python driver) means the pod runs once per attempt and is replaced from scratch on failure, rather than being restarted in-place.

The net effect is that the queue-manager needs **no storage of its own** — Kubernetes tracks running-vs-completed jobs, and the queue-manager reconstructs the queue state by diffing the orchestrator's job list against the source's item list.

### Implications for idempotence

Because Kubernetes may retry a worker after a machine failure, a work item may be processed more than once. Workers should therefore be **idempotent** or at least safe to retry — writing outputs to an item-keyed path in a bucket, for instance, so re-runs overwrite rather than duplicate. This is the same idempotence discipline that appears in [[exactly-once-semantics]] at the stream-processing layer, surfaced here at the batch-processing layer.

## Generic vs bespoke workers

As with sources, most workers are application-specific, but Burns notes that a useful generic shape recurs: a worker that downloads an input file from cloud storage, runs a user-supplied shell script against it, and uploads the result back (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md). Such a container is almost entirely reusable; only the shell command differs per application.

### Worked example: ffmpeg thumbnailer

The chapter's worker is the off-the-shelf `jrottenberg/ffmpeg` Docker image, invoked as (source: raw/designing-distributed-systems/chapter-10-work-queue-systems.md):

```
ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png
```

The `INPUT_FILE` env var points at the mounted file; the command produces PNG thumbnails. No bespoke container is needed at all — an existing community image plus one flag is the whole worker.

## Composing multiple workers

When a single item requires several distinct processing stages, the [[multi-worker-pattern]] composes multiple worker containers behind a single unified worker interface. That page covers the aggregator shape, which Burns treats as a specialization of the [[adapter-pattern]].

## Relationship to other wiki concepts

### Work queue pattern

See [[work-queue-pattern]] for the full pattern. This page covers the consumer-side interface; [[source-container-interface]] covers the producer-side interface.

### Orchestrator-backed state

The worker design leans on Kubernetes Jobs as both the execution substrate *and* the queue's durable state. This is the same orchestrator-as-database pattern that [[operator-pattern]] and Burns's Chapter 9 constructions use.

### Exactly-once semantics

The idempotence requirement echoes DDIA's [[exactly-once-semantics]] discussion: when retries are possible, effectively-once behaviour comes from making each operation safe to repeat. In a batch work queue the "operation id" is the work item's name, used implicitly as the Job's annotation key.

## Related pages

- [[work-queue-pattern]]
- [[source-container-interface]]
- [[multi-worker-pattern]]
- [[operator-pattern]]
- [[exactly-once-semantics]]
- [[idempotence]]
- [[modular-reusable-containers]]
- [[pod]]
- [[designing-distributed-systems]]
